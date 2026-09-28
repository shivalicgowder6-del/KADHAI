from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.video_service import VideoService


router = APIRouter(
    prefix="/api/media",
    tags=["media"],
)


class CreateVideoRequest(BaseModel):
    image_path: str
    audio_path: str
    filename: str = "story-scene.mp4"


class CreateVideoResponse(BaseModel):
    video_path: str


@router.post("/video", response_model=CreateVideoResponse)
def create_video(request: CreateVideoRequest) -> CreateVideoResponse:
    image_path = Path(request.image_path)
    audio_path = Path(request.audio_path)

    try:
        service = VideoService()

        output_path = service.create_video(
            image_path=image_path,
            audio_path=audio_path,
            filename=request.filename,
        )

        return CreateVideoResponse(
            video_path=str(output_path),
        )

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc