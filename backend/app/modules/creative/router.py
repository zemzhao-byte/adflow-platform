import random
from fastapi import APIRouter, Query
from app.common.schemas import APIResponse

router = APIRouter(prefix="/api/creatives", tags=["素材管理"])

PLATFORMS = ["Meta", "TikTok", "AppLovin", "Almedia", "Trademob"]
TYPES = ["video", "image", "playable", "carousel"]
STYLES = ["UGC", "Gameplay", "Cinematic", "Tutorial", "Testimonial", "Mixed", "2D Animation", "3D Render"]
STATUSES = ["active", "fatigued", "paused", "pending_review", "rejected"]
TAGS_POOL = ["action", "puzzle", "RPG", "casual", "strategy", "high_ctr", "top_performer", "new", "test", "retarget", "lookalike", "broad"]
LANGUAGES = ["EN", "JA", "KO", "DE", "PT", "ZH", "FR", "ES"]
ASPECT_RATIOS = ["9:16", "1:1", "16:9", "4:5"]
COLORS = ["#4a90d9", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6", "#1abc9c", "#e67e22", "#34495e"]

MOCK_CREATIVES = []
for i in range(1, 61):
    ctype = random.choice(TYPES)
    aspect = random.choice(ASPECT_RATIOS)
    res_map = {"9:16": "1080x1920", "1:1": "1080x1080", "16:9": "1920x1080", "4:5": "1080x1350"}
    dur = random.randint(5, 60) if ctype == "video" else None
    size_mb = round(random.uniform(0.5, 50), 1) if ctype != "playable" else round(random.uniform(1, 5), 1)
    platforms = random.sample(PLATFORMS, random.randint(1, 4))
    impressions = random.randint(10000, 5000000)
    clicks = random.randint(500, 200000)
    installs = random.randint(50, 50000)
    spend = round(random.uniform(100, 50000), 2)
    score = round(random.uniform(20, 100), 1)
    days_live = random.randint(1, 45)
    fatigue_trend = [round(score - i * random.uniform(0.2, 1.5), 1) for i_day in range(min(7, days_live)) for i in [i_day]]

    spec_compliance = {}
    for p in platforms:
        issues = []
        if ctype == "video" and dur and dur > 60:
            issues.append("时长超限")
        if ctype == "image" and size_mb > 30:
            issues.append("文件过大")
        spec_compliance[p] = {"pass": len(issues) == 0, "issues": issues}

    MOCK_CREATIVES.append({
        "id": f"CRE-{i:04d}",
        "name": f"Creative_{random.choice(STYLES)}_{i:03d}.{'mp4' if ctype == 'video' else 'png' if ctype == 'image' else 'html' if ctype == 'playable' else 'zip'}",
        "type": ctype,
        "style": random.choice(STYLES),
        "status": random.choice(STATUSES),
        "aspect_ratio": aspect,
        "resolution": res_map.get(aspect, "1080x1080"),
        "duration": dur,
        "duration_str": f"{dur}s" if dur else "-",
        "file_size_mb": size_mb,
        "language": random.choice(LANGUAGES),
        "thumb_color": random.choice(COLORS),
        "platforms": platforms,
        "spec_compliance": spec_compliance,
        "tags": random.sample(TAGS_POOL, random.randint(1, 4)),
        "associated_campaigns": random.randint(0, 12),
        "associated_adsets": random.randint(0, 30),
        "impressions": impressions,
        "clicks": clicks,
        "installs": installs,
        "spend": spend,
        "ipm": round(installs / max(impressions, 1) * 1000, 2),
        "ctr": round(clicks / max(impressions, 1) * 100, 2),
        "cvr": round(installs / max(clicks, 1) * 100, 2),
        "cpi": round(spend / max(installs, 1), 2),
        "score": score,
        "days_live": days_live,
        "fatigue_trend": fatigue_trend,
        "created_at": f"2026-0{random.randint(1, 2)}-{random.randint(10, 28):02d}",
    })


@router.get("")
async def list_creatives(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    type: str = Query(None),
    status: str = Query(None),
    platform: str = Query(None),
    sort_by: str = Query("score"),
    sort_order: str = Query("desc"),
    search: str = Query(None),
):
    filtered = MOCK_CREATIVES[:]
    if type:
        filtered = [c for c in filtered if c["type"] == type]
    if status:
        filtered = [c for c in filtered if c["status"] == status]
    if platform:
        filtered = [c for c in filtered if platform in c["platforms"]]
    if search:
        q = search.lower()
        filtered = [c for c in filtered if q in c["name"].lower() or q in c["id"].lower()]

    reverse = sort_order == "desc"
    if sort_by in ("score", "ipm", "ctr", "cvr", "spend", "impressions", "installs", "cpi"):
        filtered.sort(key=lambda x: x.get(sort_by, 0), reverse=reverse)

    total = len(filtered)
    start = (page - 1) * page_size
    items = filtered[start: start + page_size]
    return APIResponse(data={"items": items, "total": total, "page": page, "page_size": page_size})


@router.get("/stats")
async def creative_stats():
    total = len(MOCK_CREATIVES)
    active = sum(1 for c in MOCK_CREATIVES if c["status"] == "active")
    fatigued = sum(1 for c in MOCK_CREATIVES if c["status"] == "fatigued")
    pending = sum(1 for c in MOCK_CREATIVES if c["status"] == "pending_review")
    by_type = {}
    for c in MOCK_CREATIVES:
        by_type[c["type"]] = by_type.get(c["type"], 0) + 1
    by_platform = {}
    for c in MOCK_CREATIVES:
        for p in c["platforms"]:
            by_platform[p] = by_platform.get(p, 0) + 1
    total_spend = round(sum(c["spend"] for c in MOCK_CREATIVES), 2)
    avg_score = round(sum(c["score"] for c in MOCK_CREATIVES) / max(total, 1), 1)
    return APIResponse(data={
        "total": total, "active": active, "fatigued": fatigued, "pending": pending,
        "by_type": by_type, "by_platform": by_platform,
        "total_spend": total_spend, "avg_score": avg_score,
    })
