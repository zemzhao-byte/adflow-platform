import random
from fastapi import APIRouter, Query
from app.common.schemas import APIResponse

router = APIRouter(prefix="/api/campaigns", tags=["广告管理"])

PLATFORMS = ["Meta", "TikTok", "AppLovin", "Almedia", "Trademob"]
OBJECTIVES = [
    {"value": "APP_INSTALLS", "label": "应用安装", "desc": "最大化应用安装量"},
    {"value": "APP_EVENT_OPTIMIZATION", "label": "应用事件优化(AEO)", "desc": "优化应用内特定事件"},
    {"value": "VALUE_OPTIMIZATION", "label": "价值优化(VO)", "desc": "优化付费用户价值"},
    {"value": "CONVERSIONS", "label": "转化", "desc": "优化关键转化事件"},
    {"value": "LINK_CLICKS", "label": "链接点击", "desc": "最大化广告链接点击量"},
    {"value": "REACH", "label": "覆盖量", "desc": "最大化触达独立用户数"},
    {"value": "IMPRESSIONS", "label": "曝光量", "desc": "最大化广告展示次数"},
    {"value": "VIDEO_VIEWS", "label": "视频观看", "desc": "最大化视频播放量"},
    {"value": "BRAND_AWARENESS", "label": "品牌认知", "desc": "提升品牌认知度和记忆度"},
]
OBJECTIVE_VALUES = [o["value"] for o in OBJECTIVES]
STATUSES = ["ACTIVE", "PAUSED", "DRAFT", "ARCHIVED", "IN_REVIEW", "BUDGET_DEPLETED"]
BID_STRATEGIES = ["LOWEST_COST", "COST_CAP", "BID_CAP", "TARGET_ROAS", "MINIMUM_ROAS"]
GEOS = ["US", "JP", "KR", "DE", "GB", "BR", "IN", "ID", "TW", "TH", "FR", "AU", "CA", "MX", "SA"]
APPS = [
    {"id": "app_001", "name": "Puzzle Quest", "icon": "🧩", "category": "Puzzle"},
    {"id": "app_002", "name": "Battle Arena", "icon": "⚔️", "category": "Strategy"},
    {"id": "app_003", "name": "Farm Story", "icon": "🌾", "category": "Casual"},
    {"id": "app_004", "name": "Galaxy RPG", "icon": "🚀", "category": "RPG"},
]
OS_LIST = ["iOS", "Android", "All"]
PLACEMENTS = ["Feed", "Stories", "Reels", "In-Stream", "Search", "Audience Network", "Automatic"]
BUDGET_TYPES = ["DAILY", "LIFETIME"]

MOCK_CAMPAIGNS = []
for i in range(1, 81):
    platform = random.choice(PLATFORMS)
    status = random.choice(STATUSES[:4])  # main statuses
    if random.random() < 0.05:
        status = "IN_REVIEW"
    if random.random() < 0.05:
        status = "BUDGET_DEPLETED"
    obj = random.choice(OBJECTIVE_VALUES)
    daily_budget = round(random.uniform(100, 10000), 2)
    spend = round(daily_budget * random.uniform(0.3, 1.15), 2) if status == "ACTIVE" else 0
    pacing = round(spend / daily_budget * 100, 1) if daily_budget > 0 and status == "ACTIVE" else 0
    app = random.choice(APPS)
    os = random.choice(OS_LIST)
    impressions = random.randint(5000, 2000000) if status == "ACTIVE" else 0
    clicks = random.randint(200, 100000) if status == "ACTIVE" else 0
    installs = random.randint(20, 20000) if status == "ACTIVE" and "INSTALL" in obj else (random.randint(5, 5000) if status == "ACTIVE" else 0)
    cpi = round(spend / max(installs, 1), 2) if installs > 0 else 0
    cpc = round(spend / max(clicks, 1), 2) if clicks > 0 else 0
    cpm = round(spend / max(impressions, 1) * 1000, 2) if impressions > 0 else 0
    spend_velocity = round(spend / 16, 2) if status == "ACTIVE" else 0  # $/hour assuming 16h active

    MOCK_CAMPAIGNS.append({
        "id": f"CMP-{i:04d}",
        "platform": platform,
        "platform_id": f"{platform.lower()}_{random.randint(100000, 999999)}",
        "app_id": app["id"],
        "app": app["name"],
        "app_icon": app["icon"],
        "app_category": app["category"],
        "name": f"{app['name']}_{platform}_{obj[:6]}_{random.choice(GEOS)}_{i:03d}",
        "objective": obj,
        "status": status,
        "os": os,
        "placements": random.sample(PLACEMENTS, random.randint(1, 3)),
        "budget_type": random.choice(BUDGET_TYPES),
        "daily_budget": daily_budget,
        "lifetime_budget": round(daily_budget * random.randint(7, 30), 2) if random.random() > 0.7 else None,
        "spend_today": spend,
        "spend_total": round(spend * random.randint(1, 30), 2),
        "budget_pacing": pacing,
        "spend_velocity": spend_velocity,
        "bid_strategy": random.choice(BID_STRATEGIES),
        "bid_amount": round(random.uniform(0.5, 20), 2) if random.random() > 0.4 else None,
        "geo": random.sample(GEOS, random.randint(1, 4)),
        "impressions": impressions,
        "clicks": clicks,
        "installs": installs,
        "cpi": cpi,
        "cpc": cpc,
        "cpm": cpm,
        "ctr": round(clicks / max(impressions, 1) * 100, 2) if impressions > 0 else 0,
        "cvr": round(installs / max(clicks, 1) * 100, 2) if clicks > 0 else 0,
        "ipm": round(installs / max(impressions, 1) * 1000, 2) if impressions > 0 else 0,
        "roas_d1": round(random.uniform(0.05, 0.8), 2) if status == "ACTIVE" else 0,
        "roas_d7": round(random.uniform(0.1, 1.5), 2) if status == "ACTIVE" else 0,
        "pltv_d7": round(random.uniform(0.5, 8.0), 2) if status == "ACTIVE" else 0,
        "adsets_count": random.randint(1, 8),
        "ads_count": random.randint(2, 20),
        "start_date": f"2026-0{random.randint(1, 2)}-{random.randint(10, 28):02d}",
        "created_at": f"2026-0{random.randint(1, 2)}-{random.randint(10, 28):02d} {random.randint(8, 18):02d}:{random.randint(0, 59):02d}",
        "updated_at": f"2026-02-{random.randint(20, 26):02d} {random.randint(8, 22):02d}:{random.randint(0, 59):02d}",
    })

MOCK_ADSETS = []
for i in range(1, 200):
    camp = random.choice(MOCK_CAMPAIGNS)
    daily_budget = round(random.uniform(50, 3000), 2)
    spend = round(random.uniform(10, 2000), 2)
    impressions = random.randint(1000, 500000)
    clicks = random.randint(50, 30000)
    installs = random.randint(10, 5000)
    MOCK_ADSETS.append({
        "id": f"AS-{i:04d}",
        "campaign_id": camp["id"],
        "platform": camp["platform"],
        "name": f"AdSet_{random.choice(GEOS)}_{random.choice(BID_STRATEGIES)[:4]}_{i:03d}",
        "status": random.choice(STATUSES[:4]),
        "bid_strategy": random.choice(BID_STRATEGIES),
        "bid_amount": round(random.uniform(0.5, 15), 2),
        "daily_budget": daily_budget,
        "spend_today": spend,
        "budget_pacing": round(spend / max(daily_budget, 1) * 100, 1),
        "geo": random.sample(GEOS, random.randint(1, 2)),
        "os": random.choice(OS_LIST),
        "placements": random.sample(PLACEMENTS, random.randint(1, 3)),
        "impressions": impressions,
        "clicks": clicks,
        "installs": installs,
        "cpi": round(spend / max(installs, 1), 2),
        "cpc": round(spend / max(clicks, 1), 2),
        "ctr": round(clicks / max(impressions, 1) * 100, 2),
    })


@router.get("")
async def list_campaigns(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    platform: str = Query(None),
    status: str = Query(None),
    app: str = Query(None),
    objective: str = Query(None),
    os: str = Query(None),
    search: str = Query(None),
):
    filtered = MOCK_CAMPAIGNS[:]
    if platform:
        filtered = [c for c in filtered if c["platform"] == platform]
    if status:
        filtered = [c for c in filtered if c["status"] == status]
    if app:
        filtered = [c for c in filtered if c["app"] == app]
    if objective:
        filtered = [c for c in filtered if c["objective"] == objective]
    if os:
        filtered = [c for c in filtered if c["os"] == os]
    if search:
        q = search.lower()
        filtered = [c for c in filtered if q in c["name"].lower() or q in c["id"].lower()]

    total = len(filtered)
    start = (page - 1) * page_size
    items = filtered[start: start + page_size]
    return APIResponse(data={"items": items, "total": total, "page": page, "page_size": page_size})


@router.get("/stats")
async def campaign_stats():
    total = len(MOCK_CAMPAIGNS)
    active = sum(1 for c in MOCK_CAMPAIGNS if c["status"] == "ACTIVE")
    paused = sum(1 for c in MOCK_CAMPAIGNS if c["status"] == "PAUSED")
    draft = sum(1 for c in MOCK_CAMPAIGNS if c["status"] == "DRAFT")
    total_spend = round(sum(c["spend_today"] for c in MOCK_CAMPAIGNS), 2)
    total_installs = sum(c["installs"] for c in MOCK_CAMPAIGNS)
    total_clicks = sum(c["clicks"] for c in MOCK_CAMPAIGNS)
    total_impressions = sum(c["impressions"] for c in MOCK_CAMPAIGNS)
    avg_cpi = round(total_spend / max(total_installs, 1), 2)
    avg_ctr = round(total_clicks / max(total_impressions, 1) * 100, 2)
    avg_roas = round(sum(c["roas_d7"] for c in MOCK_CAMPAIGNS if c["roas_d7"] > 0) / max(sum(1 for c in MOCK_CAMPAIGNS if c["roas_d7"] > 0), 1), 2)
    by_platform = {}
    for c in MOCK_CAMPAIGNS:
        p = c["platform"]
        if p not in by_platform:
            by_platform[p] = {"count": 0, "active": 0, "spend": 0, "installs": 0, "clicks": 0, "impressions": 0}
        by_platform[p]["count"] += 1
        if c["status"] == "ACTIVE":
            by_platform[p]["active"] += 1
        by_platform[p]["spend"] = round(by_platform[p]["spend"] + c["spend_today"], 2)
        by_platform[p]["installs"] += c["installs"]
        by_platform[p]["clicks"] += c["clicks"]
        by_platform[p]["impressions"] += c["impressions"]
    by_objective = {}
    for c in MOCK_CAMPAIGNS:
        o = c["objective"]
        by_objective[o] = by_objective.get(o, 0) + 1
    by_status = {"ACTIVE": active, "PAUSED": paused, "DRAFT": draft}

    return APIResponse(data={
        "total": total, "active": active, "paused": paused, "draft": draft,
        "total_spend": total_spend, "total_installs": total_installs,
        "total_clicks": total_clicks, "total_impressions": total_impressions,
        "avg_cpi": avg_cpi, "avg_ctr": avg_ctr, "avg_roas": avg_roas,
        "by_platform": by_platform, "by_objective": by_objective, "by_status": by_status,
    })


@router.get("/objectives")
async def list_objectives():
    return APIResponse(data=OBJECTIVES)


@router.get("/adsets")
async def list_adsets(campaign_id: str = Query(None), page: int = Query(1), page_size: int = Query(20)):
    filtered = MOCK_ADSETS[:]
    if campaign_id:
        filtered = [a for a in filtered if a["campaign_id"] == campaign_id]
    total = len(filtered)
    start = (page - 1) * page_size
    items = filtered[start: start + page_size]
    return APIResponse(data={"items": items, "total": total, "page": page, "page_size": page_size})


@router.get("/apps")
async def list_apps():
    return APIResponse(data=APPS)


@router.get("/platforms")
async def list_platforms():
    return APIResponse(data=PLATFORMS)


MOCK_TEMPLATES = [
    {
        "id": "tpl_001",
        "name": "US iOS 拉新标准模板",
        "description": "适用于美国市场 iOS 应用安装投放，Meta+TikTok 双平台",
        "platforms": ["Meta", "TikTok"],
        "objective": "APP_INSTALLS",
        "budgetType": "DAILY",
        "budget": 500,
        "geo": ["US"],
        "os": "iOS",
        "placements": ["Feed", "Stories", "Reels"],
        "bidStrategy": "LOWEST_COST",
        "bidAmount": None,
        "adsetBudget": 200,
        "cta": "Install Now",
        "created_at": "2026-02-10 14:30",
        "used_count": 23,
    },
    {
        "id": "tpl_002",
        "name": "日韩 Android AEO 模板",
        "description": "日韩市场 Android 应用事件优化，出价上限策略",
        "platforms": ["Meta", "TikTok", "AppLovin"],
        "objective": "APP_EVENT_OPTIMIZATION",
        "budgetType": "DAILY",
        "budget": 1000,
        "geo": ["JP", "KR"],
        "os": "Android",
        "placements": ["Feed", "In-Stream", "Automatic"],
        "bidStrategy": "COST_CAP",
        "bidAmount": 5.0,
        "adsetBudget": 300,
        "cta": "Install Now",
        "created_at": "2026-02-15 09:00",
        "used_count": 15,
    },
    {
        "id": "tpl_003",
        "name": "全球品牌曝光模板",
        "description": "多地区品牌曝光投放，CPM 最低成本策略",
        "platforms": ["Meta"],
        "objective": "REACH",
        "budgetType": "LIFETIME",
        "budget": 5000,
        "geo": ["US", "GB", "DE", "FR", "AU", "CA"],
        "os": "All",
        "placements": ["Feed", "Stories", "Audience Network"],
        "bidStrategy": "LOWEST_COST",
        "bidAmount": None,
        "adsetBudget": 1000,
        "cta": "Learn More",
        "created_at": "2026-02-18 11:20",
        "used_count": 8,
    },
    {
        "id": "tpl_004",
        "name": "东南亚 CPC 引流模板",
        "description": "东南亚市场链接点击投放，适合预注册和落地页引流",
        "platforms": ["TikTok", "Meta"],
        "objective": "LINK_CLICKS",
        "budgetType": "DAILY",
        "budget": 300,
        "geo": ["ID", "TH", "TW"],
        "os": "All",
        "placements": ["Feed", "Reels"],
        "bidStrategy": "BID_CAP",
        "bidAmount": 0.15,
        "adsetBudget": 100,
        "cta": "Learn More",
        "created_at": "2026-02-20 16:45",
        "used_count": 12,
    },
    {
        "id": "tpl_005",
        "name": "巴西 VO 高价值用户模板",
        "description": "巴西市场价值优化投放，目标 ROAS 策略",
        "platforms": ["Meta", "AppLovin"],
        "objective": "VALUE_OPTIMIZATION",
        "budgetType": "DAILY",
        "budget": 800,
        "geo": ["BR"],
        "os": "Android",
        "placements": ["Feed", "Stories", "In-Stream"],
        "bidStrategy": "TARGET_ROAS",
        "bidAmount": 1.5,
        "adsetBudget": 400,
        "cta": "Shop Now",
        "created_at": "2026-02-22 10:00",
        "used_count": 6,
    },
]


@router.get("/templates")
async def list_templates():
    return APIResponse(data=MOCK_TEMPLATES)


from fastapi import Request


@router.post("/templates")
async def save_template(request: Request):
    body = await request.json()
    tpl_id = f"tpl_{len(MOCK_TEMPLATES) + 1:03d}"
    tpl = {
        "id": tpl_id,
        "name": body.get("name", "未命名模板"),
        "description": body.get("description", ""),
        "platforms": body.get("platforms", []),
        "objective": body.get("objective"),
        "budgetType": body.get("budgetType", "DAILY"),
        "budget": body.get("budget", 500),
        "geo": body.get("geo", []),
        "os": body.get("os", "All"),
        "placements": body.get("placements", []),
        "bidStrategy": body.get("bidStrategy", "LOWEST_COST"),
        "bidAmount": body.get("bidAmount"),
        "adsetBudget": body.get("adsetBudget", 200),
        "cta": body.get("cta", "Install Now"),
        "created_at": "2026-02-26 12:00",
        "used_count": 0,
    }
    MOCK_TEMPLATES.append(tpl)
    return APIResponse(data=tpl)


@router.delete("/templates/{tpl_id}")
async def delete_template(tpl_id: str):
    global MOCK_TEMPLATES
    MOCK_TEMPLATES = [t for t in MOCK_TEMPLATES if t["id"] != tpl_id]
    return APIResponse(data={"deleted": tpl_id})
