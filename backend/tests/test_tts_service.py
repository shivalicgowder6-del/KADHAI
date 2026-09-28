from pathlib import Path

import pytest

from app.services.tts_service import TTSService


def test_tts_service_gets_english_voice() -> None:
    service = TTSService()
    assert service.get_voice("en") == "en-US-AriaNeural"


def test_tts_service_gets_tamil_voice() -> None:
    service = TTSService()
    assert service.get_voice("ta") == "ta-IN-PallaviNeural"


def test_tts_service_rejects_unsupported_language() -> None:
    service = TTSService()

    with pytest.raises(ValueError):
        service.get_voice("fr")


def test_tts_service_rejects_empty_text() -> None:
    service = TTSService()

    with pytest.raises(ValueError):
        service.synthesize(
            text="",
            language="en",
            filename="empty-test.mp3",
        )


def test_tts_service_creates_english_audio(tmp_path: Path) -> None:
    service = TTSService(output_dir=tmp_path)

    result = service.synthesize(
        text="Hello Ellie.",
        language="en",
        filename="test-en.mp3",
    )

    assert result.exists()
    assert result.suffix == ".mp3"
    assert result.stat().st_size > 0


def test_tts_service_creates_tamil_audio(tmp_path: Path) -> None:
    service = TTSService(output_dir=tmp_path)

    result = service.synthesize(
        text="வணக்கம் எல்லி.",
        language="ta",
        filename="test-ta.mp3",
    )

    assert result.exists()
    assert result.suffix == ".mp3"
    assert result.stat().st_size > 0