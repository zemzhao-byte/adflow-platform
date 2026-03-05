import random
from fastapi import APIRouter, Query
from app.common.schemas import APIResponse

router = APIRouter(prefix="/api/data", tags=["标准数据"])

PLATFORMS = ["Meta", "TikTok", "AppLovin", "Almedia", "Trademob"]
GEOS = ["US", "JP", "KR", "DE", "GB", "BR", "IN", "ID", "TW", "TH"]


def _daily_data(days: int = 30):
    rows = []
    for d in range(days):
        day = f"2026-{1 + (25 + d) // 30:02d}-{(25 + d) % 30 + 1:02d}"
        for p in PLATFORMS:
            spend = round(random.uniform(500, 15000), 2)
            impressions = random.randint(50000, 2000000)
            clicks = random.randint(2000, 100000)
            installs = random.randint(100, 10000)
            rows.append({
                "date": day,
                "platform": p,
                "spend": spend,
                "impressions": impressions,
                "clicks": clicks,
                "installs": installs,
                "cpi": round(spend / max(installs, 1), 2),
                "ctr": round(clicks / max(impressions, 1) * 100, 2),
                "cvr": round(installs / max(clicks, 1) * 100, 2),
                "ipm": round(installs / max(impressions, 1) * 1000, 2),
                "roas_d1": round(random.uniform(0.05, 0.6), 2),
                "roas_d7": round(random.uniform(0.15, 1.2), 2),
            })
    return rows


DAILY_DATA = _daily_data(30)


@router.get("/overview")
async def data_overview():
    total_spend = round(sum(r["spend"] for r in DAILY_DATA), 2)
    total_installs = sum(r["installs"] for r in DAILY_DATA)
    total_impressions = sum(r["impressions"] for r in DAILY_DATA)
    total_clicks = sum(r["clicks"] for r in DAILY_DATA)
    avg_cpi = round(total_spend / max(total_installs, 1), 2)
    avg_ctr = round(total_clicks / max(total_impressions, 1) * 100, 2)
    avg_roas_d7 = round(sum(r["roas_d7"] for r in DAILY_DATA) / max(len(DAILY_DATA), 1), 2)

    spend_by_day = {}
    for r in DAILY_DATA:
        spend_by_day[r["date"]] = round(spend_by_day.get(r["date"], 0) + r["spend"], 2)

    spend_by_platform = {}
    installs_by_platform = {}
    for r in DAILY_DATA:
        p = r["platform"]
        spend_by_platform[p] = round(spend_by_platform.get(p, 0) + r["spend"], 2)
        installs_by_platform[p] = installs_by_platform.get(p, 0) + r["installs"]

    trend = [{"date": d, "spend": s} for d, s in sorted(spend_by_day.items())]

    return APIResponse(data={
        "total_spend": total_spend,
        "total_installs": total_installs,
        "total_impressions": total_impressions,
        "avg_cpi": avg_cpi,
        "avg_ctr": avg_ctr,
        "avg_roas_d7": avg_roas_d7,
        "spend_trend": trend,
        "spend_by_platform": spend_by_platform,
        "installs_by_platform": installs_by_platform,
    })


@router.get("/report")
async def report(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    platform: str = Query(None),
    geo: str = Query(None),
    dimension: str = Query("date"),
):
    if dimension == "platform":
        agg = {}
        for r in DAILY_DATA:
            p = r["platform"]
            if platform and p != platform:
                continue
            if p not in agg:
                agg[p] = {"platform": p, "spend": 0, "impressions": 0, "clicks": 0, "installs": 0}
            for k in ("spend", "impressions", "clicks", "installs"):
                agg[p][k] += r[k]
        items = list(agg.values())
        for item in items:
            item["spend"] = round(item["spend"], 2)
            item["cpi"] = round(item["spend"] / max(item["installs"], 1), 2)
            item["ctr"] = round(item["clicks"] / max(item["impressions"], 1) * 100, 2)
            item["ipm"] = round(item["installs"] / max(item["impressions"], 1) * 1000, 2)
    elif dimension == "geo":
        items = []
        for geo_code in GEOS:
            spend = round(random.uniform(5000, 80000), 2)
            installs = random.randint(500, 30000)
            impressions = random.randint(100000, 5000000)
            clicks = random.randint(5000, 300000)
            items.append({
                "geo": geo_code,
                "spend": spend, "impressions": impressions, "clicks": clicks, "installs": installs,
                "cpi": round(spend / max(installs, 1), 2),
                "ctr": round(clicks / max(impressions, 1) * 100, 2),
                "ipm": round(installs / max(impressions, 1) * 1000, 2),
                "roas_d7": round(random.uniform(0.2, 1.5), 2),
            })
    else:
        agg = {}
        for r in DAILY_DATA:
            if platform and r["platform"] != platform:
                continue
            d = r["date"]
            if d not in agg:
                agg[d] = {"date": d, "spend": 0, "impressions": 0, "clicks": 0, "installs": 0}
            for k in ("spend", "impressions", "clicks", "installs"):
                agg[d][k] += r[k]
        items = sorted(agg.values(), key=lambda x: x["date"], reverse=True)
        for item in items:
            item["spend"] = round(item["spend"], 2)
            item["cpi"] = round(item["spend"] / max(item["installs"], 1), 2)
            item["ctr"] = round(item["clicks"] / max(item["impressions"], 1) * 100, 2)
            item["ipm"] = round(item["installs"] / max(item["impressions"], 1) * 1000, 2)

    total = len(items)
    start = (page - 1) * page_size
    page_items = items[start: start + page_size]
    return APIResponse(data={"items": page_items, "total": total, "page": page, "page_size": page_size})
