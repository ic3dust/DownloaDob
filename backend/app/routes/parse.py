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

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

TIKTOK_EXTRACTOR_ARGS = {
    "tiktok": {
        "api_hostname": ["api22-normal-c-useast2a.tiktokv.com"],
        "app_version": ["33.3.3"],
    }
}


# -------------------------
# cleanup
# -------------------------
def cleanup_temp_dir(path: str):
    if os.path.exists(path):
        shutil.rmtree(path)


def sanitize_filename(name: str) -> str:
    return "".join(c for c in name if c.isalnum() or c in " _-").strip()


def get_single_file(directory: str) -> str:
    return next(
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
    )


# -------------------------
# PARSE
# -------------------------
@router.post("/parse")
def parse_url(data: ParseRequest):
    return extract_metadata(data.url)


# -------------------------
# VIDEO DOWNLOAD
# -------------------------
@router.get("/video")
def download_video(
    url: str = Query(...),
    format_id: str = Query(...),
    with_audio: bool = Query(True),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    temp_dir = tempfile.mkdtemp()
    raw_dir = os.path.join(temp_dir, "raw")
    os.makedirs(raw_dir, exist_ok=True)

    if format_id == "video_muted":
        format_spec = "bestvideo/best"
        remove_audio = True
    elif not with_audio:
        format_spec = format_id
        remove_audio = True
    else:
        # Always attempt to merge with best audio.
        # yt-dlp will use the existing audio if the format already has it,
        # or fetch a separate audio stream if it doesn't.
        format_spec = f"{format_id}+bestaudio/bestvideo+bestaudio/best"
        remove_audio = False

    ydl_opts = {
        "format": format_spec,
        "outtmpl": os.path.join(raw_dir, "%(title)s.%(ext)s"),
        "quiet": True,
        "http_headers": HEADERS,
        "merge_output_format": "mp4",
        "retries": 10,
        "fragment_retries": 10,
        "socket_timeout": 30,
        "concurrent_fragment_downloads": 3,
        "extractor_args": TIKTOK_EXTRACTOR_ARGS,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        title = sanitize_filename(info.get("title", "video"))
        input_file = get_single_file(raw_dir)
        output_file = os.path.join(temp_dir, f"{title}.mp4")

        ffmpeg_cmd = [
            "ffmpeg", "-y", "-i", input_file,
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            "-movflags", "+faststart",
        ]

        if remove_audio:
            ffmpeg_cmd += ["-an"]
        else:
            ffmpeg_cmd += ["-c:a", "aac", "-b:a", "192k"]

        ffmpeg_cmd.append(output_file)

        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(result.stderr)

    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        return {"error": str(e)}

    background_tasks.add_task(cleanup_temp_dir, temp_dir)

    return FileResponse(
        path=output_file,
        media_type="video/mp4",
        filename=f"{title}.mp4",
    )


# -------------------------
# AUDIO DOWNLOAD
# -------------------------
@router.get("/audio")
def download_audio(
    url: str = Query(...),
    format_id: str = Query(...),
    codec: str = Query("m4a"),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    temp_dir = tempfile.mkdtemp()
    raw_dir = os.path.join(temp_dir, "raw")
    os.makedirs(raw_dir, exist_ok=True)

    format_spec = "bestaudio/best" if format_id == "audio_extract" else format_id

    ydl_opts = {
        "format": format_spec,
        "outtmpl": os.path.join(raw_dir, "%(title)s.%(ext)s"),
        "quiet": True,
        "http_headers": HEADERS,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": codec,
                "preferredquality": "0",
            }
        ],
        "retries": 10,
        "fragment_retries": 10,
        "socket_timeout": 30,
        "extractor_args": TIKTOK_EXTRACTOR_ARGS,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        title = sanitize_filename(info.get("title", "audio"))

        output_file = None
        for file in os.listdir(raw_dir):
            if file.endswith(f".{codec}"):
                output_file = os.path.join(raw_dir, file)
                break

        if not output_file:
            raise RuntimeError("Audio extraction failed")

    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        return {"error": str(e)}

    background_tasks.add_task(cleanup_temp_dir, temp_dir)

    return FileResponse(
        path=output_file,
        media_type="audio/mp4" if codec == "m4a" else "audio/mpeg",
        filename=f"{title}.{codec}",
    )