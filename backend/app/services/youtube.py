import logging
from urllib.parse import parse_qs, urlparse

import httpx

logger = logging.getLogger(__name__)

_SUPPORTED_HOSTS = frozenset(
    {
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
        "music.youtube.com",
        "youtu.be",
    }
)

_CANONICAL = "https://www.youtube.com/watch?v={video_id}"
_OEMBED_URL = "https://www.youtube.com/oembed"
_OEMBED_TIMEOUT = 8.0


def parse_youtube_url(url: str) -> str:
    """Extract and return a valid YouTube video ID from ``url``.

    Raises ``ValueError`` with a user-facing message when the URL is not a
    supported YouTube video URL (watch, youtu.be, short, embed, live, or v).
    """
    raw = (url or "").strip()
    if not raw:
        raise ValueError("Please enter a YouTube video URL.")

    normalized = raw if "://" in raw else f"https://{raw}"
    try:
        parsed = urlparse(normalized)
    except ValueError as exc:
        raise ValueError("This doesn't look like a valid URL.") from exc

    host = parsed.netloc.lower()
    if host.startswith("www."):
        host = host[4:]

    if host not in _SUPPORTED_HOSTS:
        raise ValueError(
            "This isn't a YouTube video URL. Use a www.youtube.com or youtu.be link."
        )

    video_id = _extract_video_id(parsed, host)
    if not video_id or not _is_valid_video_id(video_id):
        raise ValueError("This YouTube URL doesn't contain a valid video ID.")

    return video_id


def canonical_url(video_id: str) -> str:
    """Return the canonical watch URL for a video ID."""
    return _CANONICAL.format(video_id=video_id)


def fetch_video_metadata(video_id: str) -> dict:
    """Return lightweight metadata (title, channel, thumbnail) via oEmbed.

    Never raises for network/metadata failures — returns ``{}`` so ingest can
    always proceed with at least the transcript text. Runs entirely server-side;
    no API keys are used or exposed.
    """
    try:
        response = httpx.get(
            _OEMBED_URL,
            params={
                "url": canonical_url(video_id),
                "format": "json",
            },
            timeout=_OEMBED_TIMEOUT,
            follow_redirects=True,
        )
        if response.status_code != 200:
            logger.warning(
                "oEmbed for video %s returned HTTP %s", video_id, response.status_code
            )
            return {}
        data = response.json()
        return {
            "title": str(data.get("title", "")).strip(),
            "author_name": str(data.get("author_name", "")).strip(),
            "author_url": str(data.get("author_url", "")).strip(),
            "thumbnail_url": str(data.get("thumbnail_url", "")).strip(),
        }
    except Exception as exc:  # network errors, bad JSON, timeouts
        logger.warning("Could not fetch oEmbed metadata for %s: %s", video_id, exc)
        return {}


def _extract_video_id(parsed, host: str) -> str | None:
    if host == "youtu.be":
        return _first_path_segment(parsed.path)

    path = parsed.path.lstrip("/")
    if path.startswith("watch"):
        return parse_qs(parsed.query).get("v", [None])[0]

    for prefix in ("shorts/", "embed/", "v/", "live/"):
        if path.startswith(prefix):
            return path[len(prefix):].split("/")[0]
    return None


def _first_path_segment(path: str) -> str | None:
    parts = [p for p in path.split("/") if p]
    return parts[0] if parts else None


def _is_valid_video_id(video_id: str) -> bool:
    return len(video_id) == 11 and all(
        c.isalnum() or c in "-_" for c in video_id
    )