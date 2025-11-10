from typing import Annotated

from fastapi import Depends, Header, HTTPException, status

from .config import get_settings, Settings


def get_settings_dep() -> Settings:
    return get_settings()


def get_tenant(
    x_atlas_tenant: Annotated[str | None, Header(alias="X-Atlas-Tenant")] = None,
    settings: Annotated[Settings, Depends(get_settings_dep)] = None,
) -> str:
    tenant = x_atlas_tenant or settings.default_tenant
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant header missing and no default configured",
        )
    return tenant
