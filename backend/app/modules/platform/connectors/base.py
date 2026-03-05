"""
统一平台Connector抽象接口

所有广告平台Adapter必须实现此接口，屏蔽平台差异，
对上层业务提供统一的广告管理、数据拉取能力。
"""
from __future__ import annotations

import time
import asyncio
import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Optional
from dataclasses import dataclass, field
from datetime import date

logger = logging.getLogger(__name__)


class PlatformType(str, Enum):
    META = "meta"
    TIKTOK = "tiktok"
    GOOGLE = "google"
    APPLOVIN = "applovin"


class AdObjective(str, Enum):
    APP_INSTALLS = "APP_INSTALLS"
    AEO = "APP_EVENT_OPTIMIZATION"
    VALUE_OPTIMIZATION = "VALUE_OPTIMIZATION"
    CONVERSIONS = "CONVERSIONS"
    TRAFFIC = "TRAFFIC"
    REACH = "REACH"
    IMPRESSIONS = "IMPRESSIONS"
    VIDEO_VIEWS = "VIDEO_VIEWS"
    LEAD_GENERATION = "LEAD_GENERATION"


class AdStatus(str, Enum):
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    DELETED = "DELETED"
    ARCHIVED = "ARCHIVED"
    IN_REVIEW = "IN_REVIEW"
    REJECTED = "REJECTED"
    DRAFT = "DRAFT"


class BidStrategy(str, Enum):
    LOWEST_COST = "LOWEST_COST"
    COST_CAP = "COST_CAP"
    BID_CAP = "BID_CAP"
    TARGET_CPA = "TARGET_CPA"
    TARGET_ROAS = "TARGET_ROAS"


@dataclass
class TokenInfo:
    access_token: str
    token_type: str = "bearer"
    expires_at: Optional[float] = None
    refresh_token: Optional[str] = None
    scopes: list[str] = field(default_factory=list)

    @property
    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at - 300  # 5分钟提前量


@dataclass
class AdAccount:
    """广告账户统一模型"""
    id: str
    platform: PlatformType
    name: str
    currency: str = "USD"
    timezone: str = "UTC"
    status: str = "ACTIVE"
    spend_cap: Optional[float] = None
    balance: Optional[float] = None
    business_id: Optional[str] = None
    extra: dict = field(default_factory=dict)


@dataclass
class CampaignData:
    """Campaign统一模型"""
    id: str
    account_id: str
    platform: PlatformType
    name: str
    objective: str
    status: AdStatus
    daily_budget: Optional[float] = None
    lifetime_budget: Optional[float] = None
    bid_strategy: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    created_time: Optional[str] = None
    updated_time: Optional[str] = None
    extra: dict = field(default_factory=dict)


@dataclass
class AdSetData:
    """Ad Set/Ad Group统一模型"""
    id: str
    campaign_id: str
    account_id: str
    platform: PlatformType
    name: str
    status: AdStatus
    targeting: dict = field(default_factory=dict)
    daily_budget: Optional[float] = None
    lifetime_budget: Optional[float] = None
    bid_strategy: Optional[str] = None
    bid_amount: Optional[float] = None
    optimization_goal: Optional[str] = None
    placements: list[str] = field(default_factory=list)
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    extra: dict = field(default_factory=dict)


@dataclass
class AdData:
    """Ad统一模型"""
    id: str
    adset_id: str
    campaign_id: str
    account_id: str
    platform: PlatformType
    name: str
    status: AdStatus
    creative_id: Optional[str] = None
    creative_type: Optional[str] = None
    creative_url: Optional[str] = None
    headline: Optional[str] = None
    body: Optional[str] = None
    cta: Optional[str] = None
    tracking_url: Optional[str] = None
    extra: dict = field(default_factory=dict)


@dataclass
class InsightsRow:
    """报表数据行"""
    date: str
    account_id: str
    campaign_id: Optional[str] = None
    adset_id: Optional[str] = None
    ad_id: Optional[str] = None
    spend: float = 0.0
    impressions: int = 0
    clicks: int = 0
    installs: int = 0
    conversions: int = 0
    revenue: float = 0.0
    ctr: float = 0.0
    cpc: float = 0.0
    cpi: float = 0.0
    cpm: float = 0.0
    cvr: float = 0.0
    roas: float = 0.0
    extra: dict = field(default_factory=dict)


@dataclass
class APIResult:
    """Connector操作统一返回"""
    success: bool
    data: Any = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    rate_limit_remaining: Optional[int] = None
    request_id: Optional[str] = None


class RateLimiter:
    """简易令牌桶限流器"""
    def __init__(self, max_calls: int, period: float):
        self._max = max_calls
        self._period = period
        self._tokens = max_calls
        self._last_refill = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self):
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self._last_refill
            self._tokens = min(self._max, self._tokens + elapsed * (self._max / self._period))
            self._last_refill = now
            if self._tokens < 1:
                wait = (1 - self._tokens) * (self._period / self._max)
                await asyncio.sleep(wait)
                self._tokens = 0
            else:
                self._tokens -= 1


class BaseConnector(ABC):
    """
    广告平台Connector基类

    所有平台Adapter继承此类，实现具体的API调用逻辑。
    基类提供：限流、重试、Token管理、统一错误处理。
    """

    def __init__(self, platform: PlatformType, token: TokenInfo,
                 rate_limit: int = 10, rate_period: float = 1.0,
                 max_retries: int = 3):
        self.platform = platform
        self.token = token
        self._limiter = RateLimiter(rate_limit, rate_period)
        self._max_retries = max_retries

    async def _call_with_retry(self, func, *args, **kwargs) -> APIResult:
        """统一调用封装：限流 + 重试 + 异常处理"""
        last_error = None
        for attempt in range(self._max_retries):
            try:
                await self._limiter.acquire()
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                last_error = e
                wait = 2 ** attempt
                logger.warning(
                    "API call failed (attempt %d/%d): %s, retrying in %ds",
                    attempt + 1, self._max_retries, str(e), wait,
                )
                await asyncio.sleep(wait)
        return APIResult(
            success=False,
            error_code="RETRY_EXHAUSTED",
            error_message=f"All {self._max_retries} attempts failed: {last_error}",
        )

    # --- 认证 ---
    @abstractmethod
    async def validate_token(self) -> APIResult:
        """验证Token有效性，返回账户基本信息"""
        ...

    @abstractmethod
    async def refresh_token(self) -> APIResult:
        """刷新Token（如果平台支持）"""
        ...

    # --- 账户 ---
    @abstractmethod
    async def get_ad_accounts(self) -> APIResult:
        """获取Token下所有广告账户"""
        ...

    @abstractmethod
    async def get_account_info(self, account_id: str) -> APIResult:
        """获取单个广告账户详情"""
        ...

    # --- Campaign ---
    @abstractmethod
    async def list_campaigns(self, account_id: str,
                             status_filter: Optional[list[AdStatus]] = None,
                             limit: int = 100) -> APIResult:
        """获取Campaign列表"""
        ...

    @abstractmethod
    async def get_campaign(self, campaign_id: str) -> APIResult:
        """获取单个Campaign详情"""
        ...

    @abstractmethod
    async def create_campaign(self, account_id: str, config: dict) -> APIResult:
        """创建Campaign"""
        ...

    @abstractmethod
    async def update_campaign(self, campaign_id: str, updates: dict) -> APIResult:
        """更新Campaign"""
        ...

    @abstractmethod
    async def update_campaign_status(self, campaign_id: str, status: AdStatus) -> APIResult:
        """更新Campaign状态（启停）"""
        ...

    # --- Ad Set ---
    @abstractmethod
    async def list_adsets(self, campaign_id: str,
                          status_filter: Optional[list[AdStatus]] = None,
                          limit: int = 100) -> APIResult:
        """获取Ad Set列表"""
        ...

    @abstractmethod
    async def create_adset(self, campaign_id: str, config: dict) -> APIResult:
        """创建Ad Set"""
        ...

    @abstractmethod
    async def update_adset(self, adset_id: str, updates: dict) -> APIResult:
        """更新Ad Set"""
        ...

    @abstractmethod
    async def update_adset_status(self, adset_id: str, status: AdStatus) -> APIResult:
        """更新Ad Set状态"""
        ...

    # --- Ad ---
    @abstractmethod
    async def list_ads(self, adset_id: str,
                       status_filter: Optional[list[AdStatus]] = None,
                       limit: int = 100) -> APIResult:
        """获取Ad列表"""
        ...

    @abstractmethod
    async def create_ad(self, adset_id: str, config: dict) -> APIResult:
        """创建Ad"""
        ...

    @abstractmethod
    async def update_ad_status(self, ad_id: str, status: AdStatus) -> APIResult:
        """更新Ad状态"""
        ...

    # --- 数据报表 ---
    @abstractmethod
    async def get_insights(self, account_id: str,
                           date_start: date, date_end: date,
                           level: str = "campaign",
                           breakdowns: Optional[list[str]] = None,
                           fields: Optional[list[str]] = None) -> APIResult:
        """获取效果数据报表"""
        ...

    # --- 素材 ---
    @abstractmethod
    async def upload_image(self, account_id: str, image_path: str) -> APIResult:
        """上传图片素材"""
        ...

    @abstractmethod
    async def upload_video(self, account_id: str, video_path: str) -> APIResult:
        """上传视频素材"""
        ...

    # --- 辅助 ---
    @abstractmethod
    async def dry_run(self, account_id: str, config: dict) -> APIResult:
        """创建预校验(validation_only)"""
        ...
