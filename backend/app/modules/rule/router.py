import random
from fastapi import APIRouter, Query
from app.common.schemas import APIResponse

router = APIRouter(prefix="/api/rules", tags=["规则盯盘"])

RULE_TYPES = ["adjustment", "monitoring"]
CATEGORIES = {
    "adjustment": ["素材与受众质量", "成本控制", "短期判断", "长期判断", "防跑飞"],
    "monitoring": ["游戏异常", "回传异常", "余额异常"],
}
ACTIONS = ["pause_ad", "pause_adset", "increase_budget", "decrease_budget", "decrease_bid", "alert_only"]
STATUSES = ["enabled", "disabled"]
SEVERITY = ["critical", "warning", "info"]


def _gen_conditions(category):
    conds = {
        "素材与受众质量": [{"metric": "CTR", "operator": "<", "value": 0.5, "min_impressions": 1000}],
        "成本控制": [{"metric": "CPI", "operator": ">", "value": 5.0, "duration_hours": 6}],
        "短期判断": [{"metric": "CPI", "operator": ">", "value_multiplier": 3.0, "within_hours": 2}],
        "长期判断": [{"metric": "ROAS_D7", "operator": "<", "value": 0.3, "min_spend": 500}],
        "防跑飞": [{"metric": "spend_velocity", "operator": ">", "value_multiplier": 5.0}],
        "游戏异常": [{"metric": "event_rate_drop", "operator": ">", "value_pct": 40, "vs_days": 7}],
        "回传异常": [{"metric": "postback_delay", "operator": ">", "value_minutes": 30}],
        "余额异常": [{"metric": "account_balance_days", "operator": "<", "value": 3}],
    }
    return conds.get(category, [])


MOCK_RULES = []
for i in range(1, 31):
    rtype = random.choice(RULE_TYPES)
    category = random.choice(CATEGORIES[rtype])
    MOCK_RULES.append({
        "id": f"RULE-{i:04d}",
        "name": f"{'调整' if rtype == 'adjustment' else '监控'}_{category}_{i:03d}",
        "type": rtype,
        "category": category,
        "status": random.choice(STATUSES),
        "conditions": _gen_conditions(category),
        "action": random.choice(ACTIONS) if rtype == "adjustment" else "alert_only",
        "severity": random.choice(SEVERITY),
        "app": random.choice(["Puzzle Quest", "Battle Arena", "Farm Story", "Galaxy RPG", "ALL"]),
        "platforms": random.sample(["Meta", "TikTok", "AppLovin"], random.randint(1, 3)),
        "triggered_count": random.randint(0, 150),
        "last_triggered": f"2026-02-{random.randint(20, 26)} {random.randint(0, 23):02d}:{random.randint(0, 59):02d}",
        "created_at": f"2026-01-{random.randint(10, 28)}",
    })

MOCK_LOGS = []
for i in range(1, 101):
    rule = random.choice(MOCK_RULES)
    MOCK_LOGS.append({
        "id": f"LOG-{i:04d}",
        "rule_id": rule["id"],
        "rule_name": rule["name"],
        "severity": rule["severity"],
        "action": rule["action"],
        "target_type": random.choice(["campaign", "adset", "ad"]),
        "target_id": f"CMP-{random.randint(1, 80):04d}",
        "metric_snapshot": {
            "cpi": round(random.uniform(0.5, 15), 2),
            "ctr": round(random.uniform(0.1, 5), 2),
            "spend": round(random.uniform(10, 5000), 2),
        },
        "result": random.choice(["executed", "pending_approval", "rejected", "failed"]),
        "operator": random.choice(["system", "admin@company.com"]),
        "executed_at": f"2026-02-{random.randint(20, 26)} {random.randint(0, 23):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}",
    })


@router.get("")
async def list_rules(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    type: str = Query(None),
    status: str = Query(None),
    category: str = Query(None),
):
    filtered = MOCK_RULES[:]
    if type:
        filtered = [r for r in filtered if r["type"] == type]
    if status:
        filtered = [r for r in filtered if r["status"] == status]
    if category:
        filtered = [r for r in filtered if r["category"] == category]
    total = len(filtered)
    start = (page - 1) * page_size
    items = filtered[start: start + page_size]
    return APIResponse(data={"items": items, "total": total, "page": page, "page_size": page_size})


@router.get("/logs")
async def list_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    rule_id: str = Query(None),
    result: str = Query(None),
):
    filtered = MOCK_LOGS[:]
    if rule_id:
        filtered = [l for l in filtered if l["rule_id"] == rule_id]
    if result:
        filtered = [l for l in filtered if l["result"] == result]
    total = len(filtered)
    start = (page - 1) * page_size
    items = filtered[start: start + page_size]
    return APIResponse(data={"items": items, "total": total, "page": page, "page_size": page_size})


@router.get("/stats")
async def rule_stats():
    total = len(MOCK_RULES)
    enabled = sum(1 for r in MOCK_RULES if r["status"] == "enabled")
    total_triggers = sum(r["triggered_count"] for r in MOCK_RULES)
    by_category = {}
    for r in MOCK_RULES:
        cat = r["category"]
        by_category[cat] = by_category.get(cat, 0) + 1
    recent_logs = sorted(MOCK_LOGS, key=lambda x: x["executed_at"], reverse=True)[:10]
    return APIResponse(data={
        "total": total, "enabled": enabled,
        "total_triggers": total_triggers,
        "by_category": by_category,
        "recent_logs": recent_logs,
    })
