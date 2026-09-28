from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


class VideoService:
    """Create MP4 story videos from a still image and narration audio."""

    def __init__(
        self,
        output_dir: Path | None = None,
        ffmpeg_path: str | None = None,
    ) -> None:
        self.output_dir = output_dir or (
            Path(__file__).resolve().parents[1] / "generated" / "video"
        )
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.ffmpeg_path = (
            ffmpeg_path
            or os.getenv("FFMPEG_PATH")
            or shutil.which("ffmpeg")
        )

        if not self.ffmpeg_path:
            raise RuntimeError(
                "FFmpeg was not found. Install FFmpeg or set the "
                "FFMPEG_PATH environment variable."
            )

    def create_video(
        self,
        image_path: Path,
        audio_path: Path,
        filename: str,
    ) -> Path:
        """
        Create an MP4 video from a still image and an audio file.

        The image remains on screen for the duration of the narration.
        """

        if not image_path.exists():
            raise FileNotFoundError(
                f"Image file not found: {image_path}"
            )

        if not audio_path.exists():
            raise FileNotFoundError(
                f"Audio file not found: {audio_path}"
            )

        if not filename.endswith(".mp4"):
            filename = f"{filename}.mp4"

        output_path = self.output_dir / filename

        command = [
            self.ffmpeg_path,
            "-y",
            "-loop",
            "1",
            "-i",
            str(image_path),
            "-i",
            str(audio_path),
            "-c:v",
            "libx264",
            "-tune",
            "stillimage",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-pix_fmt",
            "yuv420p",
            "-shortest",
            str(output_path),
        ]

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )
        except OSError as exc:
            raise RuntimeError(
                f"Failed to execute FFmpeg: {exc}"
            ) from exc

        if result.returncode != 0:
            raise RuntimeError(
                "FFmpeg video generation failed.\n"
                f"Command: {' '.join(command)}\n"
                f"FFmpeg stderr:\n{result.stderr}"
            )

        if not output_path.exists():
            raise RuntimeError(
                f"FFmpeg completed but output was not created: "
                f"{output_path}"
            )

        if output_path.stat().st_size == 0:
            raise RuntimeError(
                f"FFmpeg created an empty video: {output_path}"
            )

        return output_path