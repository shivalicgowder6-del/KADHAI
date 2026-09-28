from __future__ import annotations

from pathlib import Path

import edge_tts


VOICE_MAP = {
    "en": "en-US-AriaNeural",
    "ta": "ta-IN-PallaviNeural",
}


class TTSService:
    """Text-to-speech service for KADHAI."""

    def __init__(self, output_dir: Path | None = None) -> None:
        self.output_dir = output_dir or (
            Path(__file__).resolve().parents[1] / "generated" / "audio"
        )
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def get_voice(self, language: str) -> str:
        """Return the configured voice for a supported language."""
        try:
            return VOICE_MAP[language]
        except KeyError as exc:
            raise ValueError(
                f"Unsupported TTS language: {language}. "
                f"Supported languages: {', '.join(VOICE_MAP)}"
            ) from exc

    def synthesize(
        self,
        text: str,
        language: str,
        filename: str,
    ) -> Path:
        """
        Convert narration text into an MP3 file.

        Args:
            text: Narration text.
            language: KADHAI language code ("en" or "ta").
            filename: Output filename, e.g. "scene-n1.mp3".

        Returns:
            Path to the generated MP3 file.
        """
        if not text.strip():
            raise ValueError("TTS text cannot be empty.")

        if not filename.endswith(".mp3"):
            filename = f"{filename}.mp3"

        output_path = self.output_dir / filename
        voice = self.get_voice(language)

        communicator = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate="-5%",
            volume="+0%",
            pitch="+0Hz",
        )

        communicator.save_sync(str(output_path))

        if not output_path.exists() or output_path.stat().st_size == 0:
            raise RuntimeError(
                f"TTS generation failed: {output_path}"
            )

        return output_path