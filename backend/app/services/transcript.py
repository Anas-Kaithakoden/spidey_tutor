import logging

from youtube_transcript_api import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
    VideoUnplayable,
    YouTubeTranscriptApi,
    YouTubeTranscriptApiException,
)
from youtube_transcript_api._errors import (
    AgeRestricted,
    InvalidVideoId,
    IpBlocked,
    RequestBlocked,
    YouTubeRequestFailed,
)

logger = logging.getLogger(__name__)

_PREFERRED_LANGUAGES = ("en", "en-US", "en-GB")


class TranscriptError(Exception):
    """User-facing error raised when a video's transcript cannot be retrieved."""


def fetch_transcript(video_id: str) -> str:
    """Return the plain-text transcript for a YouTube video.

    Prefers an English manually-created transcript, then English auto-generated
    captions, then any available transcript. The result is flattened to a single
    readable block of text that can serve as study material.

    Raises ``TranscriptError`` (message safe for end users) when no usable
    transcript exists: disabled captions, no captions found, unavailable video,
    age/region restrictions, IP blocks, or transient YouTube failures.
    """
    api = YouTubeTranscriptApi()
    try:
        transcript = _pick_transcript(api, video_id)
    except (IpBlocked, RequestBlocked):
        raise TranscriptError(
            "YouTube is blocking transcript requests from this network. "
            "Please try again later or from a different network."
        )
    except AgeRestricted:
        raise TranscriptError(
            "This video is age-restricted, so its transcript can't be retrieved."
        )
    except TranscriptsDisabled:
        raise TranscriptError(
            "Transcripts are disabled for this video. "
            "Only videos with captions enabled can be processed."
        )
    except VideoUnavailable:
        raise TranscriptError(
            "This video is unavailable, so it can't be processed."
        )
    except VideoUnplayable:
        raise TranscriptError(
            "This video can't be played or embedded, so its transcript "
            "can't be retrieved."
        )
    except InvalidVideoId:
        raise TranscriptError(
            "This YouTube video ID is invalid, so it can't be processed."
        )
    except NoTranscriptFound:
        raise TranscriptError(
            "No transcript or captions are available for this video. "
            "Only videos with captions enabled can be processed."
        )
    except YouTubeRequestFailed:
        raise TranscriptError(
            "YouTube couldn't provide a transcript for this video right now. "
            "Please try again later."
        )
    except YouTubeTranscriptApiException as exc:
        logger.warning("Unexpected youtube-transcript-api error for %s: %s", video_id, exc)
        raise TranscriptError(
            "The transcript for this video could not be retrieved. "
            "Please try again later."
        )

    try:
        snippets = transcript.fetch()
    except (IpBlocked, RequestBlocked):
        raise TranscriptError(
            "YouTube is blocking transcript requests from this network. "
            "Please try again later or from a different network."
        )
    except (TranscriptsDisabled, NoTranscriptFound):
        raise TranscriptError(
            "No transcript or captions are available for this video. "
            "Only videos with captions enabled can be processed."
        )
    except YouTubeRequestFailed:
        raise TranscriptError(
            "YouTube couldn't provide a transcript for this video right now. "
            "Please try again later."
        )
    except YouTubeTranscriptApiException as exc:
        logger.warning("Unexpected fetch error for %s: %s", video_id, exc)
        raise TranscriptError(
            "The transcript for this video could not be retrieved. "
            "Please try again later."
        )

    text = _flatten(snippets)
    if not text:
        raise TranscriptError(
            "The transcript for this video is empty, so it can't be used "
            "as study material."
        )
    return text


def _pick_transcript(api: YouTubeTranscriptApi, video_id: str):
    """Choose the best available transcript for a video.

    Raises the library's ``NoTranscriptFound`` when nothing is available.
    """
    transcript_list = api.list(video_id)
    try:
        return transcript_list.find_transcript(_PREFERRED_LANGUAGES)
    except NoTranscriptFound:
        pass

    manual = None
    generated = None
    for transcript in transcript_list:
        if manual is None and not transcript.is_generated:
            manual = transcript
        if generated is None:
            generated = transcript
    if manual is not None:
        return manual
    if generated is not None:
        return generated
    raise NoTranscriptFound(video_id, _PREFERRED_LANGUAGES, transcript_list)


def _flatten(snippets) -> str:
    """Join transcript snippet text into one readable block."""
    parts = []
    for snippet in snippets:
        text = (getattr(snippet, "text", "") or "").strip()
        if text:
            parts.append(text)
    return " ".join(parts).strip()