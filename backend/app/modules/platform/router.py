"""
平台账户管理 API

提供平台绑定/解绑、账户同步、Campaign/AdSet/Ad数据拉取等接口。
"""
from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.common.schemas import APIResponse
from .connectors.base import PlatformType, AdStatus
from .manager import manager

router = APIRouter(prefix="/api/platform", tags=["平台管理"])


class BindRequest(BaseModel):
    platform: str
    token: str
    name: Optional[str] = None


class UpdateBindingRequest(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None


class UpdateTokenRequest(BaseModel):
    token: str


@router.get("/supported")
async def supported_platforms():
    """获取支持的广告平台列表"""
    platforms = [
        {"id": "meta", "name": "Meta (Facebook/Instagram)", "api_version": "v21.0",
         "auth_type": "System User Token", "status": "available",
         "icon": "M", "color": "#1877f2",
         "doc_url": "https://developers.facebook.com/docs/marketing-apis",
         "description": "全球最大社交广告平台，覆盖Facebook/Instagram/Audience Network/Messenger"},
        {"id": "tiktok", "name": "TikTok Business", "api_version": "v1.3",
         "auth_type": "OAuth Access Token", "status": "coming_soon",
         "icon": "T", "color": "#000000",
         "doc_url": "https://business-api.tiktok.com/portal/docs",
         "description": "全球增长最快的短视频广告平台"},
        {"id": "google", "name": "Google Ads", "api_version": "v18",
         "auth_type": "OAuth 2.0 + Developer Token", "status": "coming_soon",
         "icon": "G", "color": "#4285f4",
         "doc_url": "https://developers.google.com/google-ads/api/docs/start",
         "description": "全球最大搜索和展示广告平台"},
        {"id": "applovin", "name": "AppLovin", "api_version": "Mgmt API v1",
         "auth_type": "API Key", "status": "coming_soon",
         "icon": "A", "color": "#194e8b",
         "doc_url": "https://dash.applovin.com/documentation/mediation/api",
         "description": "移动应用广告平台，擅长App Install和变现"},
    ]
    return APIResponse(data=platforms)


@router.post("/bind")
async def bind_platform(req: BindRequest):
    """绑定广告平台"""
    try:
        platform = PlatformType(req.platform)
    except ValueError:
        return APIResponse(code=400, message=f"Unsupported platform: {req.platform}")

    result = await manager.bind_platform(platform, req.token, req.name)
    if not result["success"]:
        return APIResponse(code=400, message=result.get("error", "Bind failed"))
    return APIResponse(data=result)


@router.delete("/bind/{bind_id}")
async def unbind_platform(bind_id: str):
    """解绑广告平台"""
    ok = manager.unbind_platform(bind_id)
    if not ok:
        return APIResponse(code=404, message="Binding not found")
    return APIResponse(data={"unbind": True})


@router.get("/bindings")
async def list_bindings():
    """获取所有已绑定的平台"""
    return APIResponse(data=manager.list_bindings())


@router.get("/bindings/{bind_id}")
async def get_binding_detail(bind_id: str):
    """获取绑定详情（含Token预览和用户信息）"""
    detail = manager.get_binding_detail(bind_id)
    if not detail:
        return APIResponse(code=404, message="Binding not found")
    return APIResponse(data=detail)


@router.put("/bindings/{bind_id}")
async def update_binding(bind_id: str, req: UpdateBindingRequest):
    """编辑绑定信息（名称/状态）"""
    result = manager.update_binding(bind_id, name=req.name, status=req.status)
    if not result:
        return APIResponse(code=404, message="Binding not found")
    return APIResponse(data=result)


@router.put("/bindings/{bind_id}/token")
async def update_token(bind_id: str, req: UpdateTokenRequest):
    """更新Access Token"""
    result = await manager.update_token(bind_id, req.token)
    if not result["success"]:
        return APIResponse(code=400, message=result.get("error", "Token更新失败"))
    return APIResponse(data=result)


@router.post("/bindings/{bind_id}/sync")
async def sync_accounts(bind_id: str):
    """同步广告账户"""
    result = await manager.sync_accounts(bind_id)
    return APIResponse(data=result)


@router.get("/bindings/{bind_id}/campaigns")
async def list_campaigns(bind_id: str,
                         account_id: str = Query(...),
                         status: Optional[str] = Query(None)):
    """获取指定账户下的Campaign列表"""
    connector = manager.get_connector(bind_id)
    if not connector:
        return APIResponse(code=404, message="Binding not found")

    status_filter = None
    if status:
        try:
            status_filter = [AdStatus(s.strip()) for s in status.split(",")]
        except ValueError:
            pass

    result = await connector.list_campaigns(account_id, status_filter=status_filter)
    if not result.success:
        return APIResponse(code=400, message=result.error_message)
    return APIResponse(data=result.data)


@router.get("/bindings/{bind_id}/campaigns/{campaign_id}/adsets")
async def list_adsets(bind_id: str, campaign_id: str):
    """获取Campaign下的Ad Set列表"""
    connector = manager.get_connector(bind_id)
    if not connector:
        return APIResponse(code=404, message="Binding not found")
    result = await connector.list_adsets(campaign_id)
    if not result.success:
        return APIResponse(code=400, message=result.error_message)
    return APIResponse(data=result.data)


@router.get("/bindings/{bind_id}/adsets/{adset_id}/ads")
async def list_ads(bind_id: str, adset_id: str):
    """获取Ad Set下的Ad列表"""
    connector = manager.get_connector(bind_id)
    if not connector:
        return APIResponse(code=404, message="Binding not found")
    result = await connector.list_ads(adset_id)
    if not result.success:
        return APIResponse(code=400, message=result.error_message)
    return APIResponse(data=result.data)


@router.get("/bindings/{bind_id}/insights")
async def get_insights(bind_id: str,
                       account_id: str = Query(...),
                       date_start: Optional[str] = Query(None),
                       date_end: Optional[str] = Query(None),
                       level: str = Query("campaign")):
    """获取效果数据报表"""
    connector = manager.get_connector(bind_id)
    if not connector:
        return APIResponse(code=404, message="Binding not found")
    ds = date.fromisoformat(date_start) if date_start else date.today() - timedelta(days=7)
    de = date.fromisoformat(date_end) if date_end else date.today()
    result = await connector.get_insights(account_id, ds, de, level=level)
    if not result.success:
        return APIResponse(code=400, message=result.error_message)
    return APIResponse(data=result.data)


@router.post("/bindings/{bind_id}/campaigns/{campaign_id}/status")
async def update_campaign_status(bind_id: str, campaign_id: str,
                                  status: str = Query(...)):
    """更新Campaign状态（启停）"""
    connector = manager.get_connector(bind_id)
    if not connector:
        return APIResponse(code=404, message="Binding not found")
    try:
        st = AdStatus(status)
    except ValueError:
        return APIResponse(code=400, message=f"Invalid status: {status}")
    result = await connector.update_campaign_status(campaign_id, st)
    return APIResponse(data=result.data)


@router.post("/bindings/{bind_id}/dry-run")
async def dry_run(bind_id: str, account_id: str = Query(...)):
    """Dry-run校验"""
    connector = manager.get_connector(bind_id)
    if not connector:
        return APIResponse(code=404, message="Binding not found")
    result = await connector.dry_run(account_id, {})
    return APIResponse(data=result.data if result.success else {"errors": result.data})


MOCK_AD_ACCOUNTS = {
    "meta": [
        {"id": "act_10000966", "name": "Growth Team - US", "platform": "meta", "business_name": "AdFlow Inc.",
         "currency": "USD", "timezone": "America/Los_Angeles", "status": "ACTIVE",
         "spend_cap": 100000, "balance": 4823.28, "daily_spend_limit": 5000,
         "business_id": "bm_d5f73f16", "token_name": "Growth SU Token",
         "pixel_id": "px_382910", "app_id": "app_ios_001",
         "today_spend": 1234.56, "yesterday_spend": 2100.30, "month_spend": 38920.00,
         "active_campaigns": 12, "agent": "Nativex"},
        {"id": "act_10001024", "name": "Growth Team - JP", "platform": "meta", "business_name": "AdFlow Inc.",
         "currency": "JPY", "timezone": "Asia/Tokyo", "status": "ACTIVE",
         "spend_cap": 15000000, "balance": 892340.0, "daily_spend_limit": 800000,
         "business_id": "bm_d5f73f16", "token_name": "Growth SU Token",
         "pixel_id": "px_382911", "app_id": "app_ios_001",
         "today_spend": 152000, "yesterday_spend": 198000, "month_spend": 4230000,
         "active_campaigns": 8, "agent": "Nativex"},
        {"id": "act_10001088", "name": "Retarget - Global", "platform": "meta", "business_name": "AdFlow Inc.",
         "currency": "USD", "timezone": "America/New_York", "status": "ACTIVE",
         "spend_cap": 50000, "balance": 12350.60, "daily_spend_limit": 3000,
         "business_id": "bm_d5f73f16", "token_name": "Retarget SU Token",
         "pixel_id": "px_493021", "app_id": "app_android_001",
         "today_spend": 890.20, "yesterday_spend": 1520.00, "month_spend": 21300.00,
         "active_campaigns": 5, "agent": "Nativex"},
        {"id": "act_10001200", "name": "Brand - SEA", "platform": "meta", "business_name": "AdFlow Inc.",
         "currency": "USD", "timezone": "Asia/Singapore", "status": "PAUSED",
         "spend_cap": 30000, "balance": 8900.00, "daily_spend_limit": 2000,
         "business_id": "bm_a82c0001", "token_name": "SEA SU Token",
         "pixel_id": "px_102938", "app_id": "app_ios_002",
         "today_spend": 0, "yesterday_spend": 0, "month_spend": 5600.00,
         "active_campaigns": 0, "agent": "Mobvista"},
    ],
    "google": [
        {"id": "gad_320-001-9981", "name": "UAC - iOS Global", "platform": "google", "business_name": "AdFlow Inc.",
         "currency": "USD", "timezone": "America/Los_Angeles", "status": "ACTIVE",
         "spend_cap": 80000, "balance": None, "daily_spend_limit": 4000,
         "mcc_id": "mcc_520-100-0001", "token_name": "Google OAuth - Main",
         "conversion_action": "in_app_purchase", "app_id": "com.adflow.app",
         "today_spend": 2310.00, "yesterday_spend": 2890.50, "month_spend": 52100.00,
         "active_campaigns": 6, "agent": "Adtiger"},
        {"id": "gad_320-001-9982", "name": "UAC - Android JP", "platform": "google", "business_name": "AdFlow Inc.",
         "currency": "JPY", "timezone": "Asia/Tokyo", "status": "ACTIVE",
         "spend_cap": 12000000, "balance": None, "daily_spend_limit": 600000,
         "mcc_id": "mcc_520-100-0001", "token_name": "Google OAuth - Main",
         "conversion_action": "first_open", "app_id": "com.adflow.app",
         "today_spend": 98000, "yesterday_spend": 132000, "month_spend": 3100000,
         "active_campaigns": 4, "agent": "Adtiger"},
        {"id": "gad_320-002-5543", "name": "PMax - US E-commerce", "platform": "google", "business_name": "AdFlow Inc.",
         "currency": "USD", "timezone": "America/New_York", "status": "ACTIVE",
         "spend_cap": 60000, "balance": None, "daily_spend_limit": 3500,
         "mcc_id": "mcc_520-100-0001", "token_name": "Google OAuth - Main",
         "conversion_action": "purchase", "app_id": None,
         "today_spend": 1680.00, "yesterday_spend": 2100.00, "month_spend": 41200.00,
         "active_campaigns": 3, "agent": "Nativex"},
    ],
    "tiktok": [
        {"id": "tt_adv_7200001", "name": "TikTok - US Growth", "platform": "tiktok", "business_name": "AdFlow Inc.",
         "currency": "USD", "timezone": "America/Los_Angeles", "status": "ACTIVE",
         "spend_cap": 50000, "balance": 6200.00, "daily_spend_limit": 3000,
         "bc_id": "bc_9920001", "token_name": "TT OAuth Token",
         "pixel_id": "tt_px_001", "app_id": "app_ios_001",
         "today_spend": 920.00, "yesterday_spend": 1580.00, "month_spend": 28500.00,
         "active_campaigns": 7, "agent": "Mobvista"},
        {"id": "tt_adv_7200002", "name": "TikTok - SEA", "platform": "tiktok", "business_name": "AdFlow Inc.",
         "currency": "USD", "timezone": "Asia/Singapore", "status": "ACTIVE",
         "spend_cap": 30000, "balance": 4100.00, "daily_spend_limit": 2000,
         "bc_id": "bc_9920001", "token_name": "TT OAuth Token",
         "pixel_id": "tt_px_002", "app_id": "app_android_001",
         "today_spend": 650.00, "yesterday_spend": 1120.00, "month_spend": 18200.00,
         "active_campaigns": 4, "agent": "Mobvista"},
        {"id": "tt_adv_7200003", "name": "TikTok - KR Brand", "platform": "tiktok", "business_name": "AdFlow Inc.",
         "currency": "KRW", "timezone": "Asia/Seoul", "status": "PAUSED",
         "spend_cap": 40000000, "balance": 2200000, "daily_spend_limit": 2000000,
         "bc_id": "bc_9920002", "token_name": "TT OAuth Token KR",
         "pixel_id": None, "app_id": None,
         "today_spend": 0, "yesterday_spend": 0, "month_spend": 8500000,
         "active_campaigns": 0, "agent": "Nativex"},
    ],
    "applovin": [
        {"id": "al_app_90001", "name": "AppLovin - iOS US", "platform": "applovin", "business_name": "AdFlow Inc.",
         "currency": "USD", "timezone": "America/Los_Angeles", "status": "ACTIVE",
         "spend_cap": 40000, "balance": None, "daily_spend_limit": 2500,
         "api_key_name": "AL Production Key", "token_name": "AL API Key",
         "app_id": "com.adflow.app.ios", "mediation": "MAX",
         "today_spend": 780.00, "yesterday_spend": 1350.00, "month_spend": 22100.00,
         "active_campaigns": 5, "agent": "Direct"},
        {"id": "al_app_90002", "name": "AppLovin - Android Global", "platform": "applovin", "business_name": "AdFlow Inc.",
         "currency": "USD", "timezone": "UTC", "status": "ACTIVE",
         "spend_cap": 35000, "balance": None, "daily_spend_limit": 2000,
         "api_key_name": "AL Production Key", "token_name": "AL API Key",
         "app_id": "com.adflow.app.android", "mediation": "MAX",
         "today_spend": 520.00, "yesterday_spend": 980.00, "month_spend": 16800.00,
         "active_campaigns": 3, "agent": "Direct"},
    ],
}


class AccountUpdateRequest(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    spend_cap: Optional[float] = None
    daily_spend_limit: Optional[float] = None
    agent: Optional[str] = None


@router.get("/ad-accounts")
async def list_ad_accounts(platform: Optional[str] = Query(None),
                           status: Optional[str] = Query(None),
                           q: Optional[str] = Query(None)):
    """获取所有广告账户（支持按渠道、状态、关键词筛选）"""
    result = []
    platforms_to_query = [platform] if platform else list(MOCK_AD_ACCOUNTS.keys())
    for p in platforms_to_query:
        accts = MOCK_AD_ACCOUNTS.get(p, [])
        for a in accts:
            if status and a["status"] != status:
                continue
            if q:
                q_lower = q.lower()
                searchable = (a.get("id", "") + a.get("name", "") + a.get("agent", "")).lower()
                if q_lower not in searchable:
                    continue
            result.append(a)
    return APIResponse(data=result)


@router.get("/ad-accounts/{account_id}")
async def get_ad_account(account_id: str):
    """获取单个广告账户详情"""
    for accts in MOCK_AD_ACCOUNTS.values():
        for a in accts:
            if a["id"] == account_id:
                return APIResponse(data=a)
    return APIResponse(code=404, message="Account not found")


@router.put("/ad-accounts/{account_id}")
async def update_ad_account(account_id: str, req: AccountUpdateRequest):
    """编辑广告账户"""
    for accts in MOCK_AD_ACCOUNTS.values():
        for a in accts:
            if a["id"] == account_id:
                if req.name is not None:
                    a["name"] = req.name
                if req.status is not None:
                    a["status"] = req.status
                if req.spend_cap is not None:
                    a["spend_cap"] = req.spend_cap
                if req.daily_spend_limit is not None:
                    a["daily_spend_limit"] = req.daily_spend_limit
                if req.agent is not None:
                    a["agent"] = req.agent
                return APIResponse(data=a)
    return APIResponse(code=404, message="Account not found")


@router.delete("/ad-accounts/{account_id}")
async def delete_ad_account(account_id: str):
    """删除广告账户"""
    for p, accts in MOCK_AD_ACCOUNTS.items():
        for i, a in enumerate(accts):
            if a["id"] == account_id:
                accts.pop(i)
                return APIResponse(data={"deleted": True})
    return APIResponse(code=404, message="Account not found")


class CreateAccountRequest(BaseModel):
    platform: str
    name: str
    currency: str = "USD"
    timezone: str = "UTC"
    spend_cap: Optional[float] = None
    daily_spend_limit: Optional[float] = None
    agent: Optional[str] = None
    token_name: Optional[str] = None
    app_id: Optional[str] = None


@router.post("/ad-accounts")
async def create_ad_account(req: CreateAccountRequest):
    """新增广告账户"""
    import random, string
    prefix_map = {"meta": "act_", "google": "gad_", "tiktok": "tt_adv_", "applovin": "al_app_"}
    prefix = prefix_map.get(req.platform, "acct_")
    new_id = prefix + ''.join(random.choices(string.digits, k=8))
    new_acct = {
        "id": new_id,
        "name": req.name,
        "platform": req.platform,
        "business_name": "AdFlow Inc.",
        "currency": req.currency,
        "timezone": req.timezone,
        "status": "ACTIVE",
        "spend_cap": req.spend_cap,
        "balance": round(random.uniform(1000, 20000), 2) if req.platform in ("meta", "tiktok") else None,
        "daily_spend_limit": req.daily_spend_limit,
        "token_name": req.token_name or "Default Token",
        "app_id": req.app_id,
        "today_spend": 0,
        "yesterday_spend": 0,
        "month_spend": 0,
        "active_campaigns": 0,
        "agent": req.agent,
    }
    if req.platform not in MOCK_AD_ACCOUNTS:
        MOCK_AD_ACCOUNTS[req.platform] = []
    MOCK_AD_ACCOUNTS[req.platform].append(new_acct)
    return APIResponse(data=new_acct)
