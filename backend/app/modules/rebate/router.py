"""
渠道返点 / 扣款管理 API

管理不同渠道的代理商信息、返点规则（时间段+阶梯）、扣款记录。
"""
from __future__ import annotations

import time
import uuid
from datetime import date
from typing import Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.common.schemas import APIResponse

router = APIRouter(prefix="/api/rebate", tags=["渠道返点"])

# ========== 内存存储（设计阶段 Mock） ==========

PLATFORMS = ["Meta", "TikTok", "Google Ads", "AppLovin", "Snapchat", "Twitter"]

_agencies: dict[str, dict] = {}
_rebate_rules: dict[str, dict] = {}
_deductions: dict[str, dict] = {}


def _seed():
    if _agencies:
        return
    agencies_data = [
        {"platform": "Meta", "name": "Nativex", "contact": "Alice Wang", "email": "alice@nativex.com", "region": "APAC", "currency": "USD", "status": "active"},
        {"platform": "Meta", "name": "Papaya", "contact": "Bob Li", "email": "bob@papaya.com", "region": "Global", "currency": "USD", "status": "active"},
        {"platform": "TikTok", "name": "Oceanengine Direct", "contact": "Cathy Zhang", "email": "cathy@oceanengine.com", "region": "APAC", "currency": "USD", "status": "active"},
        {"platform": "Google Ads", "name": "Mobvista", "contact": "David Chen", "email": "david@mobvista.com", "region": "Global", "currency": "USD", "status": "active"},
        {"platform": "AppLovin", "name": "Direct", "contact": "-", "email": "support@applovin.com", "region": "Global", "currency": "USD", "status": "active"},
    ]
    for a in agencies_data:
        aid = str(uuid.uuid4())[:8]
        _agencies[aid] = {**a, "id": aid, "created_at": time.time(), "notes": ""}

    for aid, ag in _agencies.items():
        if ag["name"] == "Nativex":
            _add_rule(aid, "fixed", "2025-01-01", "2025-06-30", 8.0, None, "H1 2025合同返点")
            _add_rule(aid, "fixed", "2025-07-01", "2025-12-31", 10.0, None, "H2 2025合同返点")
            _add_rule(aid, "tiered", "2026-01-01", "2026-12-31", None,
                      [{"min_spend": 0, "max_spend": 50000, "rate": 8.0},
                       {"min_spend": 50000, "max_spend": 150000, "rate": 10.0},
                       {"min_spend": 150000, "max_spend": None, "rate": 13.0}],
                      "2026年阶梯返点")
        elif ag["name"] == "Papaya":
            _add_rule(aid, "fixed", "2025-01-01", "2025-12-31", 5.0, None, "年度固定返点")
        elif ag["name"] == "Oceanengine Direct":
            _add_rule(aid, "tiered", "2025-01-01", "2025-12-31", None,
                      [{"min_spend": 0, "max_spend": 100000, "rate": 3.0},
                       {"min_spend": 100000, "max_spend": 500000, "rate": 5.0},
                       {"min_spend": 500000, "max_spend": None, "rate": 8.0}],
                      "TikTok阶梯返点")
        elif ag["name"] == "Mobvista":
            _add_rule(aid, "fixed", "2025-01-01", "2025-12-31", 6.0, None, "Google代理返点")

    for aid, ag in _agencies.items():
        if ag["name"] in ("Nativex", "Papaya"):
            _add_deduction(aid, "service_fee", "2025-01-15", 2500.0, "USD", "Q4 2024服务费结算")
            _add_deduction(aid, "rebate_payout", "2025-04-10", 12800.0, "USD", "Q1 2025返点结算")
        if ag["name"] == "Oceanengine Direct":
            _add_deduction(aid, "penalty", "2025-03-01", 500.0, "USD", "违规素材罚款")


def _add_rule(agency_id, rule_type, start, end, rate, tiers, note):
    rid = str(uuid.uuid4())[:8]
    _rebate_rules[rid] = {
        "id": rid, "agency_id": agency_id, "type": rule_type,
        "start_date": start, "end_date": end,
        "rate": rate, "tiers": tiers or [],
        "note": note, "status": "active", "created_at": time.time(),
    }


def _add_deduction(agency_id, dtype, d, amount, currency, note):
    did = str(uuid.uuid4())[:8]
    _deductions[did] = {
        "id": did, "agency_id": agency_id, "type": dtype,
        "date": d, "amount": amount, "currency": currency,
        "note": note, "status": "confirmed", "created_at": time.time(),
    }


_seed()

# ========== Schemas ==========


class AgencyCreate(BaseModel):
    platform: str
    name: str
    contact: Optional[str] = ""
    email: Optional[str] = ""
    region: Optional[str] = "Global"
    currency: str = "USD"
    notes: Optional[str] = ""


class AgencyUpdate(BaseModel):
    name: Optional[str] = None
    contact: Optional[str] = None
    email: Optional[str] = None
    region: Optional[str] = None
    currency: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class RebateRuleCreate(BaseModel):
    agency_id: str
    type: str  # fixed | tiered
    start_date: str
    end_date: str
    rate: Optional[float] = None
    tiers: Optional[list[dict]] = None
    note: Optional[str] = ""


class RebateRuleUpdate(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    rate: Optional[float] = None
    tiers: Optional[list[dict]] = None
    note: Optional[str] = None
    status: Optional[str] = None


class DeductionCreate(BaseModel):
    agency_id: str
    type: str  # service_fee | rebate_payout | penalty | adjustment | other
    date: str
    amount: float
    currency: str = "USD"
    note: Optional[str] = ""


class DeductionUpdate(BaseModel):
    amount: Optional[float] = None
    date: Optional[str] = None
    note: Optional[str] = None
    status: Optional[str] = None


# ========== 代理商 CRUD ==========


@router.get("/platforms")
async def list_platforms():
    return APIResponse(data=PLATFORMS)


@router.get("/agencies")
async def list_agencies(platform: Optional[str] = Query(None),
                        status: Optional[str] = Query(None)):
    items = list(_agencies.values())
    if platform:
        items = [a for a in items if a["platform"] == platform]
    if status:
        items = [a for a in items if a["status"] == status]
    for a in items:
        a["rules_count"] = sum(1 for r in _rebate_rules.values() if r["agency_id"] == a["id"])
        a["deductions_count"] = sum(1 for d in _deductions.values() if d["agency_id"] == a["id"])
    return APIResponse(data=sorted(items, key=lambda x: x["created_at"], reverse=True))


@router.get("/agencies/{agency_id}")
async def get_agency(agency_id: str):
    ag = _agencies.get(agency_id)
    if not ag:
        return APIResponse(code=404, message="Agency not found")
    rules = sorted([r for r in _rebate_rules.values() if r["agency_id"] == agency_id],
                   key=lambda x: x["start_date"], reverse=True)
    deds = sorted([d for d in _deductions.values() if d["agency_id"] == agency_id],
                  key=lambda x: x["date"], reverse=True)
    return APIResponse(data={**ag, "rules": rules, "deductions": deds})


@router.post("/agencies")
async def create_agency(req: AgencyCreate):
    aid = str(uuid.uuid4())[:8]
    ag = {
        "id": aid, "platform": req.platform, "name": req.name,
        "contact": req.contact, "email": req.email,
        "region": req.region, "currency": req.currency,
        "status": "active", "notes": req.notes or "",
        "created_at": time.time(),
    }
    _agencies[aid] = ag
    return APIResponse(data=ag)


@router.put("/agencies/{agency_id}")
async def update_agency(agency_id: str, req: AgencyUpdate):
    ag = _agencies.get(agency_id)
    if not ag:
        return APIResponse(code=404, message="Agency not found")
    for k, v in req.model_dump(exclude_none=True).items():
        ag[k] = v
    return APIResponse(data=ag)


@router.delete("/agencies/{agency_id}")
async def delete_agency(agency_id: str):
    if agency_id not in _agencies:
        return APIResponse(code=404, message="Agency not found")
    del _agencies[agency_id]
    to_del = [r for r in _rebate_rules if _rebate_rules[r]["agency_id"] == agency_id]
    for r in to_del:
        del _rebate_rules[r]
    to_del_d = [d for d in _deductions if _deductions[d]["agency_id"] == agency_id]
    for d in to_del_d:
        del _deductions[d]
    return APIResponse(data={"deleted": True})


# ========== 返点规则 CRUD ==========


@router.get("/rules")
async def list_rules(agency_id: Optional[str] = Query(None)):
    items = list(_rebate_rules.values())
    if agency_id:
        items = [r for r in items if r["agency_id"] == agency_id]
    for r in items:
        ag = _agencies.get(r["agency_id"])
        r["agency_name"] = ag["name"] if ag else "-"
        r["platform"] = ag["platform"] if ag else "-"
    return APIResponse(data=sorted(items, key=lambda x: x["start_date"], reverse=True))


@router.post("/rules")
async def create_rule(req: RebateRuleCreate):
    if req.agency_id not in _agencies:
        return APIResponse(code=404, message="Agency not found")
    rid = str(uuid.uuid4())[:8]
    rule = {
        "id": rid, "agency_id": req.agency_id, "type": req.type,
        "start_date": req.start_date, "end_date": req.end_date,
        "rate": req.rate, "tiers": req.tiers or [],
        "note": req.note or "", "status": "active",
        "created_at": time.time(),
    }
    _rebate_rules[rid] = rule
    return APIResponse(data=rule)


@router.put("/rules/{rule_id}")
async def update_rule(rule_id: str, req: RebateRuleUpdate):
    rule = _rebate_rules.get(rule_id)
    if not rule:
        return APIResponse(code=404, message="Rule not found")
    for k, v in req.model_dump(exclude_none=True).items():
        rule[k] = v
    return APIResponse(data=rule)


@router.delete("/rules/{rule_id}")
async def delete_rule(rule_id: str):
    if rule_id not in _rebate_rules:
        return APIResponse(code=404, message="Rule not found")
    del _rebate_rules[rule_id]
    return APIResponse(data={"deleted": True})


# ========== 扣款记录 CRUD ==========


@router.get("/deductions")
async def list_deductions(agency_id: Optional[str] = Query(None),
                          dtype: Optional[str] = Query(None)):
    items = list(_deductions.values())
    if agency_id:
        items = [d for d in items if d["agency_id"] == agency_id]
    if dtype:
        items = [d for d in items if d["type"] == dtype]
    for d in items:
        ag = _agencies.get(d["agency_id"])
        d["agency_name"] = ag["name"] if ag else "-"
        d["platform"] = ag["platform"] if ag else "-"
    return APIResponse(data=sorted(items, key=lambda x: x["date"], reverse=True))


@router.post("/deductions")
async def create_deduction(req: DeductionCreate):
    if req.agency_id not in _agencies:
        return APIResponse(code=404, message="Agency not found")
    did = str(uuid.uuid4())[:8]
    ded = {
        "id": did, "agency_id": req.agency_id, "type": req.type,
        "date": req.date, "amount": req.amount,
        "currency": req.currency, "note": req.note or "",
        "status": "confirmed", "created_at": time.time(),
    }
    _deductions[did] = ded
    return APIResponse(data=ded)


@router.put("/deductions/{deduction_id}")
async def update_deduction(deduction_id: str, req: DeductionUpdate):
    ded = _deductions.get(deduction_id)
    if not ded:
        return APIResponse(code=404, message="Deduction not found")
    for k, v in req.model_dump(exclude_none=True).items():
        ded[k] = v
    return APIResponse(data=ded)


@router.delete("/deductions/{deduction_id}")
async def delete_deduction(deduction_id: str):
    if deduction_id not in _deductions:
        return APIResponse(code=404, message="Deduction not found")
    del _deductions[deduction_id]
    return APIResponse(data={"deleted": True})


# ========== 汇总 ==========


@router.get("/summary")
async def summary():
    total_agencies = len(_agencies)
    active_agencies = sum(1 for a in _agencies.values() if a["status"] == "active")
    total_rules = len(_rebate_rules)
    active_rules = sum(1 for r in _rebate_rules.values() if r["status"] == "active")
    total_deductions = len(_deductions)
    total_deduction_amount = sum(d["amount"] for d in _deductions.values())
    total_rebate_payouts = sum(d["amount"] for d in _deductions.values() if d["type"] == "rebate_payout")
    platforms_with_agency = list(set(a["platform"] for a in _agencies.values()))
    return APIResponse(data={
        "total_agencies": total_agencies,
        "active_agencies": active_agencies,
        "total_rules": total_rules,
        "active_rules": active_rules,
        "total_deductions": total_deductions,
        "total_deduction_amount": round(total_deduction_amount, 2),
        "total_rebate_payouts": round(total_rebate_payouts, 2),
        "platforms_with_agency": platforms_with_agency,
    })
