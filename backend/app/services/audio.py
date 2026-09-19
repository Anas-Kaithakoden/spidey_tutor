import base64
import logging

from app.config import settings
from app.services import gemini, groq, ollama, openrouter
from app.services.openai_compat import chat_text

logger = logging.getLogger(__name__)

# ~150 words ≈ 60 seconds at ~150 wpm
SUMMARY_WORD_TARGET = "130-150 words"


def generate_summary_text(
    material_text: str,
    provider: str = "gemini",
    model_name: str = "",
    language: str = "en",
) -> tuple[str, str]:
    """Generate 1-min summary text. Returns (generated_by, summary_text)."""
    if model_name in ("gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.5-flash-lite", ""):
        model_name = settings.gemini_model
    truncated = material_text[:40000]
    is_ml = language.lower().startswith("ml")

    if is_ml:
        prompt = (
            "You are a friendly Malayalam tutor recording a 1-minute voice note in Malayalam.\n"
            "Explain ONLY this material in natural spoken Malayalam (മലയാളം) as if talking to a friend — warm, expressive, high/low pitch variation.\n"
            f"Rules:\n"
            f"- Exactly {SUMMARY_WORD_TARGET} in Malayalam, one flowing paragraph, spoken style\n"
            "- Start naturally like \"ഓക്കേ, ഒരു മിനിറ്റിൽ പറയാം —\" or \"ശരി, ഇതാ ചുരുക്കം...\"\n"
            "- Use natural Malayalam contractions, short sentences, expressive pauses.\n"
            "- Cover ONLY the key concepts FROM THIS MATERIAL with emphasis and engaging tone, dramatic but clear. Do NOT add topics not in the material.\n"
            "- No asterisks, no English headings, no markup — pure spoken Malayalam (keep any technical terms exactly as in material).\n"
            "- Ignore formatting noise (***). Do NOT mix with previous uploads. End with encouraging close like \"ഇത്രയേ ഉള്ളൂ — നിനക്ക് പറ്റും!\"\n\n"
            f"Study material:\n{truncated}"
        )
    else:
        prompt = (
            "You are a friendly study buddy recording a highly expressive 1-minute voice note.\n"
            "Explain ONLY this material as if you're on a podcast — dramatic, warm, high-energy, with clear high/low pitch swings.\n"
            f"Rules:\n"
            f"- Exactly {SUMMARY_WORD_TARGET} (about 60 seconds), one flowing paragraph, ultra-expressive spoken style\n"
            "- Start with a natural opener like \"Okay, here's the quick one-minute rundown —\" or \"Alright, imagine this...\"\n"
            "- Use contractions, very short punchy sentences, dramatic pauses, rising excitement on key ideas, soft calm on explanations.\n"
            "- Vary tone: energetic highs, thoughtful lows, emphasize ONLY the key terms FROM THIS MATERIAL with vocal stress. Do NOT hallucinate terms like A-star/Minimax unless they are in the material.\n"
            "- No asterisks, no bullet points, no headings, no syllabus codes — just pure spoken English.\n"
            "- Use ONLY this material. Do NOT combine with previous files. Ignore formatting noise (***). End with encouraging close like \"And that's the core — you've got this!\"\n\n"
            f"Study material:\n{truncated}"
        )

    # try provider -> fallback to mock (first 150 words truncated)
    try:
        if provider == "ollama":
            name = model_name or "qwen3:8b"
            # ollama doesn't have dedicated summary, use generic chat json
            from app.services.ollama import _chat_json, _robust_parse

            system = (
                f"You are a study assistant. Summarize into {SUMMARY_WORD_TARGET} spoken paragraph. "
                "Respond with STRICT JSON: {\"summary\": string}"
            )
            raw = _chat_json(name, system, prompt)
            data = _robust_parse(raw)
            summary = str(data.get("summary", "")).strip()
            if not summary:
                raise ValueError("Empty summary from ollama")
            return "ai", summary
        elif provider in ("groq", "openrouter"):
            system = (
                f"You are a study assistant. Summarize into {SUMMARY_WORD_TARGET} spoken paragraph. "
                "Return only the summary text, no markdown, no JSON."
            )
            module = groq if provider == "groq" else openrouter
            cfg = module._ready_cfg()
            name = model_name or cfg.default_model
            summary = chat_text(cfg, name, system, prompt, temperature=0.7)
            summary = summary.strip()
            if not summary:
                raise ValueError(f"Empty summary from {provider}")
            return "ai", summary
        else:
            # gemini text generation
            from google.genai import types

            name = model_name or settings.gemini_model
            client = gemini._client()
            resp = client.models.generate_content(
                model=name,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.7),
            )
            summary = (resp.text or "").strip()
            if not summary:
                raise ValueError("Empty summary from gemini")
            # ensure ~150 words max
            words = summary.split()
            if len(words) > 180:
                summary = " ".join(words[:150])
            return "ai", summary
    except Exception as exc:
        logger.exception("Summary generation failed (provider=%s): %s", provider, exc)
        # mock fallback: first 150 words of material
        words = truncated.split()
        mock = " ".join(words[:150]) or "Summary unavailable."
        return "mock", mock


def _wav_bytes_from_pcm(pcm_bytes: bytes, sample_rate: int = 24000) -> bytes:
    """Wrap raw PCM (L16, mono) bytes in a WAV container browsers can play."""
    import struct

    num_channels = 1
    bits_per_sample = 16
    byte_rate = sample_rate * num_channels * bits_per_sample // 8
    block_align = num_channels * bits_per_sample // 8
    data_len = len(pcm_bytes)
    # WAV header 44 bytes
    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",
        36 + data_len,
        b"WAVE",
        b"fmt ",
        16,
        1,  # PCM
        num_channels,
        sample_rate,
        byte_rate,
        block_align,
        bits_per_sample,
        b"data",
        data_len,
    )
    return header + pcm_bytes


def _pcm_to_wav_base64(pcm_b64: str, sample_rate: int = 24000) -> tuple[str, str]:
    """Convert raw PCM base64 (L16) to WAV base64 so <audio> can play it."""
    pcm_bytes = base64.b64decode(pcm_b64)
    wav_bytes = _wav_bytes_from_pcm(pcm_bytes, sample_rate)
    return "audio/wav", base64.b64encode(wav_bytes).decode("utf-8")


def _wave_pcm_and_rate(wav_bytes: bytes) -> tuple[bytes, int]:
    """Extract raw PCM payload + sample rate from a WAV file, skipping the header."""
    if len(wav_bytes) < 44 or wav_bytes[:4] != b"RIFF":
        raise ValueError("Not a WAV file")
    # fmt chunk: bytes 12-15 = "fmt ", 16-19 = chunk size, 20-21 = audio format,
    # 22-23 = channels, 24-27 = sample rate
    rate = int.from_bytes(wav_bytes[24:28], "little")
    data_offset = 44
    data_len = len(wav_bytes) - data_offset
    # The data chunk may not start at 44; scan chunk headers to be safe.
    offset = 12
    while offset + 8 <= len(wav_bytes):
        chunk_id = wav_bytes[offset : offset + 4]
        size = int.from_bytes(wav_bytes[offset + 4 : offset + 8], "little")
        if chunk_id == b"data":
            start = offset + 8
            return wav_bytes[start : start + size], rate
        offset += 8 + size + (size % 2)
    return wav_bytes[data_offset:], rate


def generate_tts_audio(
    text: str,
    voice_name: str = "Kore",
    model_name: str = "gemini-2.5-flash-preview-tts",
    language: str = "en",
) -> tuple[str, str, str]:
    """Generate audio via Gemini TTS. Returns (mime_type, base64_data, generated_by)."""
    try:
        from google.genai import types

        client = gemini._client()
        if language.lower().startswith("ml"):
            styled = (
                "Speak in warm, highly expressive Malayalam with dynamic high/low pitch, "
                "dramatic emphasis on the key terms present in the text, clear pauses, energetic and friendly — in Malayalam. "
                "Do not add new topics:\n\n" + text
            )
        else:
            styled = (
                "Speak in a highly expressive, warm tutor voice with dramatic high/low pitch variation — "
                "high and excited on key discoveries, low and thoughtful on explanations, "
                "strong emphasis on the key terms that actually appear in the text, with natural breaths and pauses. "
                "Do not add terms not in the text. Be very engaging and lively:\n\n" + text
            )
        resp = client.models.generate_content(
            model=model_name,
            contents=styled,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=voice_name
                        )
                    )
                ),
            ),
        )
        # extract audio inline data
        candidate = resp.candidates[0] if resp.candidates else None
        if candidate and candidate.content and candidate.content.parts:
            for part in candidate.content.parts:
                inline = getattr(part, "inline_data", None)
                if inline and inline.data:
                    mime = inline.mime_type or "audio/wav"
                    if isinstance(inline.data, str):
                        b64 = inline.data
                    else:
                        b64 = base64.b64encode(inline.data).decode("utf-8")
                    # Gemini returns audio/L16;codec=pcm;rate=24000 — browsers can't play raw PCM
                    if "L16" in mime or "pcm" in mime.lower():
                        rate = 24000
                        try:
                            for seg in mime.split(";"):
                                if "rate=" in seg:
                                    rate = int(seg.split("rate=")[1])
                        except Exception:
                            pass
                        wav_mime, wav_b64 = _pcm_to_wav_base64(b64, rate)
                        return wav_mime, wav_b64, "ai"
                    return mime, b64, "ai"
                blob = getattr(part, "inlineData", None)
                if blob:
                    mime = getattr(blob, "mimeType", "audio/wav")
                    data = getattr(blob, "data", b"")
                    b64 = data if isinstance(data, str) else base64.b64encode(data).decode("utf-8")
                    if "L16" in mime or "pcm" in mime.lower():
                        rate = 24000
                        try:
                            for seg in mime.split(";"):
                                if "rate=" in seg:
                                    rate = int(seg.split("rate=")[1])
                        except Exception:
                            pass
                        wav_mime, wav_b64 = _pcm_to_wav_base64(b64, rate)
                        return wav_mime, wav_b64, "ai"
                    return mime, b64, "ai"

        raise ValueError("No audio data in TTS response")

    except Exception as exc:
        logger.exception("Gemini TTS failed (voice=%s): %s", voice_name, exc)
        raise


def synthesize_podcast_audio(
    lines: list[dict],
    voice_one: str = "Kore",
    voice_two: str = "Puck",
    pause_ms: int = 300,
) -> tuple[str, bytes]:
    """Synthesize an alternating two-host episode into a single WAV.

    Each dialogue line is spoken by its host's voice (``host_one`` ->
    ``voice_one``, ``host_two`` -> ``voice_two``) and stitched together with a
    short silence gap between turns so speakers feel distinct and natural.

    Returns ``(mime_type, wav_bytes)``. Raises on any TTS failure — the router
    decides whether to keep the script-only episode and surface an error.
    """
    if not lines:
        raise ValueError("Cannot synthesize a podcast with no dialogue lines.")

    pcm_chunks: list[bytes] = []
    sample_rate = 24000
    silence = b"\x00\x00" * (sample_rate * pause_ms // 1000)

    for idx, line in enumerate(lines):
        text = str(line.get("text") or "").strip()
        speaker = str(line.get("speaker") or "host_one")
        if not text:
            continue
        voice = voice_one if speaker == "host_one" else voice_two
        _mime, b64, _generated = generate_tts_audio(text, voice_name=voice)
        wav = base64.b64decode(b64)
        pcm, rate = _wave_pcm_and_rate(wav)
        if idx == 0:
            sample_rate = rate
            silence = b"\x00\x00" * (sample_rate * pause_ms // 1000)
        else:
            pcm_chunks.append(silence)
        pcm_chunks.append(pcm)

    full_pcm = b"".join(pcm_chunks)
    if not full_pcm:
        raise ValueError("No audio was generated for the podcast.")
    return "audio/wav", _wav_bytes_from_pcm(full_pcm, sample_rate)


def podcast_duration_seconds(wav_bytes: bytes) -> float:
    """Best-effort duration of a WAV produced by ``synthesize_podcast_audio``."""
    try:
        _pcm, rate = _wave_pcm_and_rate(wav_bytes)
        return len(_pcm) / (rate * 2)
    except Exception:
        return 0.0
