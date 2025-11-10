"""Tenant service backed by SQLModel."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlmodel import select

from ..database import get_session, init_db
from ..models import (
    BillingPreview,
    DatasetContract,
    TenantSummary,
    UsageMetrics,
    Tenant,
    Usage,
    PlanTierEnum,
)

_DATASETS = {
    "demo": [
        DatasetContract(name="knowledge_base", description="Approved articles", freshness="15m"),
        DatasetContract(name="sales_notes", description="Synced from CRM", freshness="1h"),
    ],
    "acme": [
        DatasetContract(name="portfolio_docs", description="Product briefs", freshness="30m"),
    ],
}


def ensure_seed_data() -> None:
    init_db()
    with get_session() as session:
        if not session.get(Tenant, "demo"):
            session.add(Tenant(id="demo", plan=PlanTierEnum.scale))
            session.add(Usage(tenant_id="demo", tokens=120_000, requests=540))
        if not session.get(Tenant, "acme"):
            session.add(Tenant(id="acme", plan=PlanTierEnum.growth))
            session.add(Usage(tenant_id="acme", tokens=42_000, requests=210))
        session.commit()


def upsert_tenant(tenant: str, plan: str = "trial") -> TenantSummary:
    ensure_seed_data()
    with get_session() as session:
        db_tenant = session.get(Tenant, tenant)
        if not db_tenant:
            db_tenant = Tenant(id=tenant, plan=PlanTierEnum(plan))
            session.add(db_tenant)
            session.add(Usage(tenant_id=tenant))
        else:
            db_tenant.plan = PlanTierEnum(plan)
        session.commit()
    return get_summary(tenant)


def list_datasets(tenant: str) -> list[DatasetContract]:
    return _DATASETS.get(tenant, [])


def get_summary(tenant: str) -> TenantSummary:
    ensure_seed_data()
    with get_session() as session:
        db_usage = session.exec(select(Usage).where(Usage.tenant_id == tenant)).first()
        db_tenant = session.get(Tenant, tenant)
        if not db_usage or not db_tenant:
            return TenantSummary(
                tenant=tenant,
                usage=UsageMetrics(tokens=0, requests=0, plan="trial"),
                refreshed_at=datetime.now(timezone.utc),
            )
        usage = UsageMetrics(tokens=db_usage.tokens, requests=db_usage.requests, plan=db_tenant.plan.value)
        return TenantSummary(tenant=tenant, usage=usage, refreshed_at=datetime.now(timezone.utc))


def update_usage(tenant: str, *, tokens_delta: int = 0, requests_delta: int = 0) -> TenantSummary:
    ensure_seed_data()
    with get_session() as session:
        db_usage = session.exec(select(Usage).where(Usage.tenant_id == tenant)).first()
        if not db_usage:
            db_usage = Usage(tenant_id=tenant)
            session.add(db_usage)
        db_usage.tokens += tokens_delta
        db_usage.requests += requests_delta
        session.commit()
    return get_summary(tenant)


def billing_preview(tenant: str) -> BillingPreview:
    summary = get_summary(tenant)
    rate = {
        "trial": 0.0,
        "growth": 249.0,
        "scale": 999.0,
    }[summary.usage.plan]
    overage = max(summary.usage.tokens - 150_000, 0) * 0.0005
    estimated = rate + overage
    next_charge = datetime.now(timezone.utc) + timedelta(days=7)
    return BillingPreview(
        tenant=tenant,
        plan=summary.usage.plan,
        estimated_amount_usd=round(estimated, 2),
        next_charge_date=next_charge,
    )
