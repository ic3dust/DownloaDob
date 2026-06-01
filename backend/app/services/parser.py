import yt_dlp


def extract_thumbnail(info: dict):
    """
    Robust thumbnail extraction for TikTok / Instagram / YouTube
    """
    if info.get("thumbnail"):
        return info["thumbnail"]

    thumbnails = info.get("thumbnails") or []
    for t in thumbnails:
        if isinstance(t, dict) and t.get("url"):
            return t["url"]

    return None


def extract_metadata(url: str):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "format": "bestvideo+bestaudio/best",
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
        },
        "extractor_args": {
        "tiktok": {
            "api_hostname": ["api22-normal-c-useast2a.tiktokv.com"],
            "app_version": ["33.3.3"],
        }},
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        formats_list = []
        seen = set()

        for f in info.get("formats", []):
            vcodec = f.get("vcodec") or ""
            acodec = f.get("acodec") or ""

            has_video = vcodec != "none" and vcodec != ""
            has_audio = acodec != "none" and acodec != ""

            if not has_video and not has_audio:
                continue

            if has_video and has_audio:
                stream_type = "muxed"
            elif has_video:
                stream_type = "video_only"
            else:
                stream_type = "audio_only"

            ext = f.get("ext") or "mp4"

            # normalize audio extension
            if stream_type == "audio_only" and ext == "mp4":
                ext = "m4a"

            # resolution handling
            if stream_type == "audio_only":
                abr = f.get("abr")
                resolution = f"{int(abr)}kbps" if abr else "Audio Track"
            else:
                resolution = f.get("resolution")

                if not resolution or resolution == "null":
                    w, h = f.get("width"), f.get("height")
                    resolution = f"{w}x{h}" if w and h else "Adaptive"

                key = (stream_type, resolution)
                if key in seen:
                    continue
                seen.add(key)

            formats_list.append({
                "format_id": f.get("format_id"),
                "ext": ext,
                "resolution": resolution,
                "filesize": f.get("filesize") or f.get("filesize_approx"),
                "type": stream_type,
                "note": f.get("format_note") or "",
            })

        # Always inject audio fallback option
        formats_list.append({
            "format_id": "audio_extract",
            "ext": "m4a",
            "resolution": "Audio Only",
            "filesize": None,
            "type": "audio_only",
            "note": "Extract best available audio",
        })

        # Optional: inject silent video fallback (for TikTok-like sources)
        formats_list.append({
            "format_id": "video_muted",
            "ext": "mp4",
            "resolution": "Best Video (No Audio)",
            "filesize": None,
            "type": "video_only",
            "note": "Remove audio after download",
        })

        return {
            "title": info.get("title"),
            "thumbnail": extract_thumbnail(info),
            "duration": info.get("duration"),
            "url": url,
            "formats": formats_list,
        }