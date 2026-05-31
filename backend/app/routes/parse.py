import os
import shutil
import tempfile
import subprocess
from fastapi import APIRouter, Query, BackgroundTasks
from fastapi.responses import FileResponse
import yt_dlp

from app.models.req import ParseRequest
from app.services.parser import extract_metadata

router = APIRouter(prefix="/api")


@router.post("/parse")
def parse_url(data: ParseRequest):
    return extract_metadata(data.url)


def cleanup_temp_dir(path: str):
    if os.path.exists(path):
        shutil.rmtree(path)


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
}


def find_output_file(directory: str) -> str:
    """Return the first file found in directory, ignoring subdirs."""
    for name in os.listdir(directory):
        full = os.path.join(directory, name)
        if os.path.isfile(full):
            return full
    raise FileNotFoundError(f"No output file found in {directory}")


@router.get("/download-video")
@router.get("/download-video")
def download_video(
    url: str = Query(...),
    format_id: str = Query(...),
    with_audio: bool = Query(False),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    temp_dir = tempfile.mkdtemp()
    raw_dir = os.path.join(temp_dir, "raw")
    os.makedirs(raw_dir)

    # For +audio: try merging with bestaudio, fall back to format alone
    # (TikTok formats are pre-muxed so separate bestaudio doesn't exist)
    format_spec = f"{format_id}+bestaudio/{format_id}" if with_audio else format_id

    ydl_opts = {
        "format": format_spec,
        "outtmpl": os.path.join(raw_dir, "raw.%(ext)s"),
        "quiet": True,
        "http_headers": HEADERS,
        "merge_output_format": "mkv",
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=True)

        raw_file = find_output_file(raw_dir)
        output_file = os.path.join(temp_dir, "output.mp4")

        if with_audio:
            ffmpeg_cmd = [
                "ffmpeg", "-y",
                "-i", raw_file,
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "23",
                "-c:a", "aac",
                "-b:a", "192k",
                "-movflags", "+faststart",
                output_file,
            ]
        else:
            ffmpeg_cmd = [
                "ffmpeg", "-y",
                "-i", raw_file,
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "23",
                "-an",
                "-movflags", "+faststart",
                output_file,
            ]

        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg failed: {result.stderr}")

    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        return {"error": str(e)}

    background_tasks.add_task(cleanup_temp_dir, temp_dir)
    return FileResponse(path=output_file, media_type="video/mp4", filename="video.mp4")


@router.get("/download-audio")
def download_audio(
    url: str = Query(...),
    format_id: str = Query(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    temp_dir = tempfile.mkdtemp()

    ydl_opts = {
        "format": format_id,
        "outtmpl": os.path.join(temp_dir, "audio.%(ext)s"),
        "quiet": True,
        "http_headers": HEADERS,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "m4a",
                "preferredquality": "0",
            }
        ],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=True)

        output = find_output_file(temp_dir)
    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        return {"error": str(e)}

    background_tasks.add_task(cleanup_temp_dir, temp_dir)
    return FileResponse(path=output, media_type="audio/mp4", filename="audio.m4a")