from fastapi import APIRouter

from ..models import BillingPreview
from ..services import tenants as tenant_service

router = APIRouter(prefix="/billing", tags=["billing"])


@router.get("/{tenant}/preview", response_model=BillingPreview)
def preview(tenant: str) -> BillingPreview:
    return tenant_service.billing_preview(tenant)
