from fastapi import APIRouter, Header, HTTPException, status

from ..config import get_settings

router = APIRouter(prefix="/webhooks", tags=["webhooks"])
settings = get_settings()


@router.post("/stripe")
def stripe_webhook(
    payload: dict,
    stripe_signature: str | None = Header(None, alias="Stripe-Signature"),
) -> dict[str, str]:
    if stripe_signature != settings.stripe_webhook_secret:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")
    # TODO: process event types (invoice.paid, usage.report, etc.)
    return {"status": "accepted"}
