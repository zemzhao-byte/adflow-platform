"""
Meta Marketing API Adapter

基于 Graph API v21.0 的 Meta(Facebook/Instagram) 广告平台 Connector 实现。
当前为 Mock 模式，数据结构完全模拟真实 Meta API 返回。
后续替换 _api_call 为真实 HTTP 调用即可。

真实API文档: https://developers.facebook.com/docs/marketing-apis
"""
from __future__ import annotations

import random
import hashlib
from datetime import date, datetime, timedelta
from typing import Optional

from .base import (
    BaseConnector, PlatformType, TokenInfo, APIResult,
    AdAccount, CampaignData, AdSetData, AdData, InsightsRow,
    AdStatus, AdObjective, BidStrategy,
)

META_OBJECTIVES_MAP = {
    AdObjective.APP_INSTALLS: "OUTCOME_APP_PROMOTION",
    AdObjective.AEO: "OUTCOME_APP_PROMOTION",
    AdObjective.VALUE_OPTIMIZATION: "OUTCOME_APP_PROMOTION",
    AdObjective.TRAFFIC: "OUTCOME_TRAFFIC",
    AdObjective.CONVERSIONS: "OUTCOME_SALES",
    AdObjective.REACH: "OUTCOME_AWARENESS",
    AdObjective.IMPRESSIONS: "OUTCOME_AWARENESS",
    AdObjective.VIDEO_VIEWS: "OUTCOME_ENGAGEMENT",
    AdObjective.LEAD_GENERATION: "OUTCOME_LEADS",
}

META_BID_MAP = {
    BidStrategy.LOWEST_COST: "LOWEST_COST_WITHOUT_CAP",
    BidStrategy.COST_CAP: "COST_CAP",
    BidStrategy.BID_CAP: "BID_CAP",
    BidStrategy.TARGET_ROAS: "MINIMUM_ROAS",
}

PLACEMENTS = [
    "Facebook Feed", "Facebook Stories", "Facebook Reels",
    "Instagram Feed", "Instagram Stories", "Instagram Reels",
    "Audience Network", "Messenger",
]

GEOS = ["US", "JP", "KR", "DE", "GB", "BR", "IN", "ID", "TW", "TH", "FR", "AU", "CA"]
APPS_POOL = [
    {"app_id": "com.game.puzzle", "name": "Puzzle Quest", "os": "iOS"},
    {"app_id": "com.game.rpg", "name": "Epic RPG", "os": "Android"},
    {"app_id": "com.app.social", "name": "ChatWorld", "os": "iOS"},
    {"app_id": "com.game.strategy", "name": "War Empire", "os": "Android"},
]


def _gen_id(prefix: str = "") -> str:
    return prefix + str(random.randint(10000000000, 99999999999))


def _gen_date(days_ago_max: int = 60) -> str:
    d = datetime.now() - timedelta(days=random.randint(1, days_ago_max))
    return d.strftime("%Y-%m-%dT%H:%M:%S+0000")


class MetaConnector(BaseConnector):
    """Meta Marketing API Connector (Mock 模式)"""

    API_VERSION = "v21.0"
    BASE_URL = "https://graph.facebook.com"

    def __init__(self, token: TokenInfo):
        super().__init__(
            platform=PlatformType.META,
            token=token,
            rate_limit=50,
            rate_period=1.0,
            max_retries=3,
        )
        self._mock_accounts: list[AdAccount] = []
        self._mock_campaigns: dict[str, list[CampaignData]] = {}
        self._mock_adsets: dict[str, list[AdSetData]] = {}
        self._mock_ads: dict[str, list[AdData]] = {}
        self._initialized = False

    def _ensure_mock_data(self):
        if self._initialized:
            return
        self._initialized = True
        bm_id = "bm_" + hashlib.md5(self.token.access_token.encode()).hexdigest()[:8]

        for ai in range(random.randint(2, 4)):
            acct_id = "act_" + str(10000000 + ai * 1111 + random.randint(0, 999))
            acct = AdAccount(
                id=acct_id,
                platform=PlatformType.META,
                name=["Growth Team - US", "Brand Team - APAC", "UA Team - EU", "Retargeting - Global"][ai % 4],
                currency=["USD", "JPY", "USD", "EUR"][ai % 4],
                timezone=["America/Los_Angeles", "Asia/Tokyo", "America/New_York", "Europe/Berlin"][ai % 4],
                status="ACTIVE" if random.random() > 0.1 else "DISABLED",
                spend_cap=random.choice([None, 10000, 50000, 100000]),
                balance=round(random.uniform(500, 20000), 2),
                business_id=bm_id,
                extra={"account_status": 1, "age": random.uniform(0.5, 5.0)},
            )
            self._mock_accounts.append(acct)

            campaigns = []
            for ci in range(random.randint(4, 10)):
                obj = random.choice(list(AdObjective))
                status = random.choices(
                    [AdStatus.ACTIVE, AdStatus.PAUSED, AdStatus.DRAFT, AdStatus.ARCHIVED],
                    weights=[50, 25, 10, 15],
                )[0]
                app = random.choice(APPS_POOL)
                daily_b = round(random.choice([50, 100, 200, 500, 1000, 2000]) * 1.0, 2)
                camp = CampaignData(
                    id=_gen_id("camp_"),
                    account_id=acct_id,
                    platform=PlatformType.META,
                    name=f"{app['name']}_{obj.value[:3]}_{random.choice(GEOS)}_{ci+1:02d}",
                    objective=obj.value,
                    status=status,
                    daily_budget=daily_b,
                    bid_strategy=random.choice(list(BidStrategy)).value,
                    start_time=_gen_date(90),
                    created_time=_gen_date(120),
                    extra={
                        "meta_objective": META_OBJECTIVES_MAP.get(obj, "OUTCOME_APP_PROMOTION"),
                        "special_ad_categories": [],
                        "campaign_budget_optimization": random.choice([True, False]),
                        "buying_type": "AUCTION",
                        "app_name": app["name"],
                        "app_id": app["app_id"],
                        "os": app["os"],
                    },
                )
                campaigns.append(camp)

                adsets = []
                for si in range(random.randint(1, 4)):
                    geo = random.sample(GEOS, k=random.randint(1, 3))
                    plc = random.sample(PLACEMENTS, k=random.randint(2, 5))
                    bid_amt = round(random.uniform(0.5, 15.0), 2)
                    aset = AdSetData(
                        id=_gen_id("aset_"),
                        campaign_id=camp.id,
                        account_id=acct_id,
                        platform=PlatformType.META,
                        name=f"{camp.name}_{'_'.join(geo[:2])}_{si+1}",
                        status=status if random.random() > 0.3 else random.choice([AdStatus.ACTIVE, AdStatus.PAUSED]),
                        targeting={
                            "geo_locations": {"countries": geo},
                            "age_min": random.choice([18, 21, 25]),
                            "age_max": random.choice([45, 55, 65]),
                            "genders": random.choice([[0], [1], [2], [1, 2]]),
                            "device_platforms": [app["os"].lower()] if app["os"] != "All" else ["ios", "android"],
                            "publisher_platforms": ["facebook", "instagram"],
                        },
                        daily_budget=round(daily_b / random.randint(1, 3), 2),
                        bid_strategy=camp.bid_strategy,
                        bid_amount=bid_amt,
                        optimization_goal=random.choice(["APP_INSTALLS", "OFFSITE_CONVERSIONS", "VALUE"]),
                        placements=plc,
                        start_time=camp.start_time,
                        extra={
                            "attribution_spec": [{"event_type": "CLICK_THROUGH", "window_days": 7},
                                                  {"event_type": "VIEW_THROUGH", "window_days": 1}],
                            "learning_phase_status": random.choice(["LEARNING", "SUCCESS", "LEARNING_LIMITED"]),
                            "conversion_events": random.randint(0, 80),
                        },
                    )
                    adsets.append(aset)

                    ads = []
                    for di in range(random.randint(1, 3)):
                        creative_type = random.choice(["VIDEO", "IMAGE", "CAROUSEL"])
                        ad = AdData(
                            id=_gen_id("ad_"),
                            adset_id=aset.id,
                            campaign_id=camp.id,
                            account_id=acct_id,
                            platform=PlatformType.META,
                            name=f"{aset.name}_cr{di+1}",
                            status=aset.status,
                            creative_id=_gen_id("cr_"),
                            creative_type=creative_type,
                            headline=random.choice(["Play Now!", "Download Free", "Join Millions", "Epic Adventure Awaits"]),
                            body=random.choice(["The #1 puzzle game", "Strategy at its finest", "Connect with friends"]),
                            cta=random.choice(["INSTALL_MOBILE_APP", "LEARN_MORE", "SIGN_UP", "PLAY_GAME"]),
                            tracking_url=f"https://app.adjust.com/{app['app_id']}?campaign={{{{campaign.id}}}}",
                            extra={
                                "effective_status": aset.status.value,
                                "preview_url": f"https://www.facebook.com/ads/preview/?d=cr_{di}",
                            },
                        )
                        ads.append(ad)
                    self._mock_ads[aset.id] = ads
                self._mock_adsets[camp.id] = adsets
            self._mock_campaigns[acct_id] = campaigns

    # --- 认证 ---
    async def validate_token(self) -> APIResult:
        self._ensure_mock_data()
        if not self.token.access_token or len(self.token.access_token) < 5:
            return APIResult(success=False, error_code="INVALID_TOKEN", error_message="Token is invalid or empty")
        return APIResult(success=True, data={
            "user_id": "user_" + hashlib.md5(self.token.access_token.encode()).hexdigest()[:8],
            "name": "AdFlow System User",
            "token_type": "System User Token",
            "scopes": ["ads_management", "ads_read", "business_management"],
            "expires_at": self.token.expires_at,
        })

    async def refresh_token(self) -> APIResult:
        return APIResult(success=False, error_code="NOT_SUPPORTED",
                         error_message="Meta System User tokens do not support refresh. Generate a new long-lived token from BM.")

    # --- 账户 ---
    async def get_ad_accounts(self) -> APIResult:
        self._ensure_mock_data()
        return APIResult(success=True, data=[
            {"id": a.id, "name": a.name, "currency": a.currency, "timezone": a.timezone,
             "status": a.status, "spend_cap": a.spend_cap, "balance": a.balance,
             "business_id": a.business_id}
            for a in self._mock_accounts
        ])

    async def get_account_info(self, account_id: str) -> APIResult:
        self._ensure_mock_data()
        for a in self._mock_accounts:
            if a.id == account_id:
                return APIResult(success=True, data={
                    "id": a.id, "name": a.name, "currency": a.currency,
                    "timezone": a.timezone, "status": a.status,
                    "spend_cap": a.spend_cap, "balance": a.balance,
                    "business_id": a.business_id, **a.extra,
                })
        return APIResult(success=False, error_code="NOT_FOUND", error_message=f"Account {account_id} not found")

    # --- Campaign ---
    async def list_campaigns(self, account_id: str,
                             status_filter: Optional[list[AdStatus]] = None,
                             limit: int = 100) -> APIResult:
        self._ensure_mock_data()
        camps = self._mock_campaigns.get(account_id, [])
        if status_filter:
            sf = set(s.value if isinstance(s, AdStatus) else s for s in status_filter)
            camps = [c for c in camps if c.status.value in sf]
        return APIResult(success=True, data=[{
            "id": c.id, "name": c.name, "objective": c.objective,
            "status": c.status.value, "daily_budget": c.daily_budget,
            "lifetime_budget": c.lifetime_budget, "bid_strategy": c.bid_strategy,
            "start_time": c.start_time, "created_time": c.created_time,
            **c.extra,
        } for c in camps[:limit]])

    async def get_campaign(self, campaign_id: str) -> APIResult:
        self._ensure_mock_data()
        for camps in self._mock_campaigns.values():
            for c in camps:
                if c.id == campaign_id:
                    return APIResult(success=True, data={
                        "id": c.id, "name": c.name, "objective": c.objective,
                        "status": c.status.value, "daily_budget": c.daily_budget,
                        "bid_strategy": c.bid_strategy, "start_time": c.start_time,
                        **c.extra,
                    })
        return APIResult(success=False, error_code="NOT_FOUND")

    async def create_campaign(self, account_id: str, config: dict) -> APIResult:
        self._ensure_mock_data()
        new_id = _gen_id("camp_")
        return APIResult(success=True, data={"id": new_id, **config})

    async def update_campaign(self, campaign_id: str, updates: dict) -> APIResult:
        return APIResult(success=True, data={"id": campaign_id, "updated_fields": list(updates.keys())})

    async def update_campaign_status(self, campaign_id: str, status: AdStatus) -> APIResult:
        return APIResult(success=True, data={"id": campaign_id, "status": status.value})

    # --- Ad Set ---
    async def list_adsets(self, campaign_id: str,
                          status_filter: Optional[list[AdStatus]] = None,
                          limit: int = 100) -> APIResult:
        self._ensure_mock_data()
        asets = self._mock_adsets.get(campaign_id, [])
        if status_filter:
            sf = set(s.value if isinstance(s, AdStatus) else s for s in status_filter)
            asets = [a for a in asets if a.status.value in sf]
        return APIResult(success=True, data=[{
            "id": a.id, "name": a.name, "status": a.status.value,
            "targeting": a.targeting, "daily_budget": a.daily_budget,
            "bid_strategy": a.bid_strategy, "bid_amount": a.bid_amount,
            "optimization_goal": a.optimization_goal, "placements": a.placements,
            **a.extra,
        } for a in asets[:limit]])

    async def create_adset(self, campaign_id: str, config: dict) -> APIResult:
        new_id = _gen_id("aset_")
        return APIResult(success=True, data={"id": new_id, **config})

    async def update_adset(self, adset_id: str, updates: dict) -> APIResult:
        return APIResult(success=True, data={"id": adset_id, "updated_fields": list(updates.keys())})

    async def update_adset_status(self, adset_id: str, status: AdStatus) -> APIResult:
        return APIResult(success=True, data={"id": adset_id, "status": status.value})

    # --- Ad ---
    async def list_ads(self, adset_id: str,
                       status_filter: Optional[list[AdStatus]] = None,
                       limit: int = 100) -> APIResult:
        self._ensure_mock_data()
        ads = self._mock_ads.get(adset_id, [])
        return APIResult(success=True, data=[{
            "id": a.id, "name": a.name, "status": a.status.value,
            "creative_id": a.creative_id, "creative_type": a.creative_type,
            "headline": a.headline, "body": a.body, "cta": a.cta,
            "tracking_url": a.tracking_url, **a.extra,
        } for a in ads[:limit]])

    async def create_ad(self, adset_id: str, config: dict) -> APIResult:
        new_id = _gen_id("ad_")
        return APIResult(success=True, data={"id": new_id, **config})

    async def update_ad_status(self, ad_id: str, status: AdStatus) -> APIResult:
        return APIResult(success=True, data={"id": ad_id, "status": status.value})

    # --- 数据报表 ---
    async def get_insights(self, account_id: str,
                           date_start: date, date_end: date,
                           level: str = "campaign",
                           breakdowns: Optional[list[str]] = None,
                           fields: Optional[list[str]] = None) -> APIResult:
        self._ensure_mock_data()
        rows = []
        campaigns = self._mock_campaigns.get(account_id, [])
        d = date_start
        while d <= date_end:
            for camp in campaigns:
                if camp.status in (AdStatus.ACTIVE, AdStatus.PAUSED):
                    spend = round(random.uniform(10, camp.daily_budget or 500), 2)
                    imps = int(spend / random.uniform(3, 12) * 1000)
                    clicks = int(imps * random.uniform(0.008, 0.035))
                    installs = int(clicks * random.uniform(0.05, 0.25))
                    revenue = round(installs * random.uniform(0.5, 8.0), 2)
                    row = InsightsRow(
                        date=d.isoformat(),
                        account_id=account_id,
                        campaign_id=camp.id,
                        spend=spend, impressions=imps, clicks=clicks,
                        installs=installs, revenue=revenue,
                        ctr=round(clicks / imps * 100, 2) if imps else 0,
                        cpc=round(spend / clicks, 2) if clicks else 0,
                        cpi=round(spend / installs, 2) if installs else 0,
                        cpm=round(spend / imps * 1000, 2) if imps else 0,
                        cvr=round(installs / clicks * 100, 2) if clicks else 0,
                        roas=round(revenue / spend, 2) if spend else 0,
                    )
                    rows.append(row)
            d += timedelta(days=1)
        return APIResult(success=True, data=[{
            "date": r.date, "campaign_id": r.campaign_id,
            "spend": r.spend, "impressions": r.impressions, "clicks": r.clicks,
            "installs": r.installs, "revenue": r.revenue,
            "ctr": r.ctr, "cpc": r.cpc, "cpi": r.cpi, "cpm": r.cpm,
            "cvr": r.cvr, "roas": r.roas,
        } for r in rows])

    # --- 素材 ---
    async def upload_image(self, account_id: str, image_path: str) -> APIResult:
        return APIResult(success=True, data={
            "hash": hashlib.md5(image_path.encode()).hexdigest(),
            "url": f"https://scontent.xx.fbcdn.net/{hashlib.md5(image_path.encode()).hexdigest()[:12]}.jpg",
        })

    async def upload_video(self, account_id: str, video_path: str) -> APIResult:
        return APIResult(success=True, data={
            "video_id": _gen_id("vid_"),
            "status": "processing",
        })

    # --- 预校验 ---
    async def dry_run(self, account_id: str, config: dict) -> APIResult:
        errors = []
        if not config.get("name"):
            errors.append({"code": "MISSING_FIELD", "message": "Campaign name is required"})
        if not config.get("objective"):
            errors.append({"code": "MISSING_FIELD", "message": "Objective is required"})
        budget = config.get("daily_budget", 0)
        if budget and budget < 1:
            errors.append({"code": "INVALID_VALUE", "message": "Daily budget must be at least $1"})
        if errors:
            return APIResult(success=False, error_code="VALIDATION_ERROR",
                             error_message="Dry-run failed", data={"errors": errors})
        return APIResult(success=True, data={"validation": "passed"})
