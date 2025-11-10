from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .routers import billing, health, tenants, auth, webhooks, metrics
from .telemetry import configure_logging, RequestMetricsMiddleware
from .services.tenants import ensure_seed_data
from .services.auth import seed_admin_user

settings = get_settings()
configure_logging()
ensure_seed_data()
seed_admin_user()

app = FastAPI(title=settings.app_name, version="0.1.0")
app.include_router(health.router)
app.include_router(tenants.router)
app.include_router(billing.router)
app.include_router(auth.router)
app.include_router(webhooks.router)
app.include_router(metrics.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestMetricsMiddleware)


@app.get("/", summary="API metadata")
def root() -> dict[str, object]:
    return {
        "name": settings.app_name,
        "environment": settings.environment,
        "docs_url": "/docs",
    }
