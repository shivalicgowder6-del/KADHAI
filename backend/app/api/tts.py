from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.tts_service import TTSService


router = APIRouter(
    prefix="/api/media",
    tags=["media"],
)


class CreateTTSRequest(BaseModel):
    text: str
    language: str
    filename: str = "narration.mp3"


class CreateTTSResponse(BaseModel):
    audio_path: str


@router.post("/tts", response_model=CreateTTSResponse)
def create_tts(request: CreateTTSRequest) -> CreateTTSResponse:
    try:
        service = TTSService()

        output_path = service.synthesize(
            text=request.text,
            language=request.language,
            filename=request.filename,
        )

        return CreateTTSResponse(
            audio_path=str(output_path),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc