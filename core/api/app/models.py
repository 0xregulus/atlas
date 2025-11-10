"""Domain models for the Atlas core API."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field as SQLField

PlanTier = Literal["trial", "growth", "scale"]


class PlanTierEnum(str, Enum):
    trial = "trial"
    growth = "growth"
    scale = "scale"


class UsageMetrics(BaseModel):
    tokens: int = Field(ge=0)
    requests: int = Field(ge=0)
    plan: PlanTier


class DatasetContract(BaseModel):
    name: str
    description: str
    freshness: str


class TenantSummary(BaseModel):
    tenant: str
    usage: UsageMetrics
    refreshed_at: datetime


class BillingPreview(BaseModel):
    tenant: str
    plan: PlanTier
    estimated_amount_usd: float
    next_charge_date: datetime


class Tenant(SQLModel, table=True):
    id: str = SQLField(primary_key=True, index=True)
    plan: PlanTierEnum = SQLField(default=PlanTierEnum.trial)


class Usage(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    tenant_id: str = SQLField(foreign_key="tenant.id")
    tokens: int = SQLField(default=0)
    requests: int = SQLField(default=0)


class UsageEvent(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    tenant_id: str = SQLField(foreign_key="tenant.id")
    source: str = SQLField(default="ai-service")
    tokens: int = SQLField(default=0)
    latency_ms: float | None = SQLField(default=None)
    created_at: datetime = SQLField(default_factory=lambda: datetime.now(timezone.utc))


class AdminUser(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    username: str = SQLField(unique=True, index=True)
    password_hash: str
    created_at: datetime = SQLField(default_factory=lambda: datetime.now(timezone.utc))
