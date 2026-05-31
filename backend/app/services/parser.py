import yt_dlp


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
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        formats_list = []
        seen_resolutions = set()

        for f in info.get("formats", []):
            acodec = f.get("acodec") or ""
            vcodec = f.get("vcodec") or ""

            has_video = vcodec not in ("none", "")
            has_audio = acodec not in ("none", "")

            if not has_audio and not has_video:
                continue

            stream_type = (
                "muxed"      if (has_video and has_audio) else
                "video_only" if has_video                 else
                "audio_only"
            )

            ext = f.get("ext") or "mp4"

            # Skip webm audio — converts to m4a anyway, redundant
            if stream_type == "audio_only" and ext == "webm":
                continue

            # Fix mp4-container audio label
            if stream_type == "audio_only" and ext == "mp4":
                ext = "m4a"

            if stream_type == "audio_only":
                abr = f.get("abr")
                resolution = f"{int(abr)}kbps" if abr else "Audio Track"
            else:
                resolution = f.get("resolution")
                if not resolution or resolution == "null":
                    w, h = f.get("width"), f.get("height")
                    resolution = f"{w}x{h}" if (w and h) else "Adaptive"

                res_key = (stream_type, resolution)
                if res_key in seen_resolutions:
                    continue
                seen_resolutions.add(res_key)

            # THIS was outside the loop before — now correctly indented inside
            formats_list.append({
                "format_id": f.get("format_id"),
                "ext": ext,
                "resolution": resolution,
                "filesize": f.get("filesize") or f.get("filesize_approx"),
                "type": stream_type,
                "note": f.get("format_note") or "",
            })

        return {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),
            "url": url,
            "formats": formats_list,
        }