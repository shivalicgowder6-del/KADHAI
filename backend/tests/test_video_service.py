from pathlib import Path

import pytest

from app.services.video_service import VideoService


def test_video_service_creates_video(tmp_path: Path) -> None:
    image_path = (
        Path(__file__).resolve().parents[1]
        / "app"
        / "generated"
        / "images"
        / "test-ellie.png"
    )

    audio_path = (
        Path(__file__).resolve().parents[1]
        / "app"
        / "generated"
        / "audio"
        / "test-ellie.mp3"
    )

    if not image_path.exists() or not audio_path.exists():
        pytest.skip("Media test assets are not available.")

    output_dir = tmp_path / "video"

    service = VideoService(output_dir=output_dir)

    result = service.create_video(
        image_path=image_path,
        audio_path=audio_path,
        filename="test-service.mp4",
    )

    assert result.exists()
    assert result.suffix == ".mp4"
    assert result.stat().st_size > 0


def test_video_service_rejects_missing_image(tmp_path: Path) -> None:
    service = VideoService(output_dir=tmp_path / "video")

    with pytest.raises(FileNotFoundError):
        service.create_video(
            image_path=tmp_path / "missing.png",
            audio_path=tmp_path / "audio.mp3",
            filename="test.mp4",
        )


def test_video_service_rejects_missing_audio(tmp_path: Path) -> None:
    image_path = tmp_path / "image.png"
    image_path.write_bytes(b"fake-image")

    service = VideoService(output_dir=tmp_path / "video")

    with pytest.raises(FileNotFoundError):
        service.create_video(
            image_path=image_path,
            audio_path=tmp_path / "missing.mp3",
            filename="test.mp4",
        )