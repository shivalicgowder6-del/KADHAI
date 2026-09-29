from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.safety.models import SafetyResult
from app.safety.safety_service import SafetyService


router = APIRouter(
    prefix="/api/safety",
    tags=["safety"],
)


class SafetyCheckRequest(BaseModel):
    """Request body for checking a child input."""

    text: str = Field(min_length=0)


@router.post("/check", response_model=SafetyResult)
def check_safety(request: SafetyCheckRequest) -> SafetyResult:
    """Run the KADHAI safety gateway against user input."""

    service = SafetyService()
    return service.check(request.text)
