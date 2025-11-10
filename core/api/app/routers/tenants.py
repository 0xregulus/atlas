from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ..dependencies import get_tenant
from ..models import DatasetContract, TenantSummary
from ..security import get_current_user
from ..services import tenants as tenant_service

router = APIRouter(prefix="/tenants", tags=["tenants"])


class TenantCreateRequest(BaseModel):
    tenant: str
    plan: str = "trial"


class UsageUpdateRequest(BaseModel):
    tokens_delta: int = Field(0, description="Tokens to add/subtract")
    requests_delta: int = Field(0, description="Requests to add/subtract")


@router.get("/current", response_model=TenantSummary, summary="Current tenant context")
def current_tenant(tenant: Annotated[str, Depends(get_tenant)]) -> TenantSummary:
    return tenant_service.get_summary(tenant)


@router.post("/", response_model=TenantSummary, summary="Create or upsert tenant")
def create_or_update(
    req: TenantCreateRequest,
    _: Annotated[str, Depends(get_current_user)],
) -> TenantSummary:
    return tenant_service.upsert_tenant(req.tenant, req.plan)


@router.post("/{tenant}/usage", response_model=TenantSummary, summary="Update usage counters")
def update_usage(
    tenant: str,
    req: UsageUpdateRequest,
    _: Annotated[str, Depends(get_current_user)],
) -> TenantSummary:
    return tenant_service.update_usage(
        tenant, tokens_delta=req.tokens_delta, requests_delta=req.requests_delta
    )


@router.get(
    "/{tenant}/catalog",
    response_model=list[DatasetContract],
    summary="Datasets available to the AI layer",
)
def catalog(tenant: str) -> list[DatasetContract]:
    return tenant_service.list_datasets(tenant)
