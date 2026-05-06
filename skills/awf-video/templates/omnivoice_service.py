"""
omnivoice_service.py — Custom SpeechService adapter for OmniVoice Studio TTS.

Connects manim-voiceover plugin to the local OmniVoice Studio server,
supporting both Vietnamese (clone voice) and English (system voice).

Usage in Manim scene:
    from omnivoice_service import OmniVoiceService

    class MyScene(VoiceoverScene):
        def construct(self):
            # Vietnamese (clone voice)
            self.set_speech_service(OmniVoiceService(lang="vi"))

            # English (system voice, female)
            self.set_speech_service(OmniVoiceService(lang="en", gender="female"))
"""

import os
import json
import hashlib
import requests
import time
from pathlib import Path

from manim_voiceover.services.base import SpeechService

# ============================================================
# CONFIG — Same as tts_client.py
# ============================================================

API_URL = "http://117.0.36.6:8888"
API_KEY = "vneu_-q_okdL9TzB-sIMW1AQqNt0Z_qIoE05TN4s6H5snGEs"
HEADERS = {"X-API-Key": API_KEY}

POLL_INTERVAL = 2
MAX_POLL_DURATION = 180

# Default clone ref for Vietnamese voice
DEFAULT_CLONE_REF_ID = "c8495f76-c047-47e1-8a77-1cb651bb6511"

# System voice gender mapping
GENDER_MAP = {
    "male": "Binh",
    "female": "Ngoc",
}


# ============================================================
# TTS API FUNCTIONS (extracted from tts_client.py)
# ============================================================

def _omni_clone_ref(text, ref_id, speed=1.0, num_step=32, normalize=True):
    """Clone voice from saved reference."""
    form_data = {
        "text": text,
        "ref_id": str(ref_id),
        "speed": str(speed),
        "num_step": str(num_step),
        "normalize": str(normalize).lower(),
    }
    resp = requests.post(
        f"{API_URL}/api/v1/omnivoice/generate-clone-ref",
        headers=HEADERS,
        data=form_data,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["job_id"]


def _omni_auto(text, speed=1.0, num_step=32, normalize=True):
    """Auto mode — model picks best voice."""
    resp = requests.post(
        f"{API_URL}/api/v1/omnivoice/generate-auto",
        headers=HEADERS,
        json={"text": text, "speed": speed, "num_step": num_step, "normalize": normalize},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["job_id"]


def _system_synthesize(text, voice="Ngoc", normalize=True):
    """System voice TTS (sync)."""
    resp = requests.post(
        f"{API_URL}/api/v1/tts/synthesize",
        headers=HEADERS,
        json={"text": text, "voice": voice, "normalize": normalize},
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()


def _poll_job(job_id):
    """Poll async OmniVoice job until completion."""
    start = time.time()
    while time.time() - start < MAX_POLL_DURATION:
        time.sleep(POLL_INTERVAL)
        resp = requests.get(
            f"{API_URL}/api/v1/omnivoice/jobs/{job_id}",
            headers=HEADERS,
            timeout=10,
        )
        job = resp.json()
        status = job.get("status", "unknown")

        if status in ("completed", "done"):
            audio_url = job.get("audio_url")
            if audio_url:
                return _download_audio(audio_url)
            raise RuntimeError(f"Job {job_id} completed but no audio_url")

        if status in ("failed", "error"):
            raise RuntimeError(f"Job failed: {job.get('error', 'Unknown')}")

    raise TimeoutError(f"Job {job_id} timed out after {MAX_POLL_DURATION}s")


def _download_audio(audio_url):
    """Download audio bytes from URL."""
    full_url = audio_url if audio_url.startswith("http") else f"{API_URL}{audio_url}"
    resp = requests.get(full_url, headers=HEADERS, timeout=60)
    resp.raise_for_status()
    return resp.content


# ============================================================
# CUSTOM SPEECH SERVICE
# ============================================================

class OmniVoiceService(SpeechService):
    """
    Custom SpeechService for manim-voiceover that connects to OmniVoice Studio.

    Args:
        lang: "vi" for Vietnamese (clone voice), "en" for English (system voice)
        gender: "male" or "female" (only used for English system voice)
        ref_id: Clone reference ID (only used for Vietnamese)
        speed: Speech speed (1.0 = normal)
        normalize: Enable SEA-G2P normalization
    """

    def __init__(
        self,
        lang: str = "vi",
        gender: str = "female",
        ref_id: str = DEFAULT_CLONE_REF_ID,
        speed: float = 1.0,
        normalize: bool = True,
        **kwargs,
    ):
        self.lang = lang
        self.gender = gender
        self.ref_id = ref_id
        self.speed = speed
        self.normalize = normalize
        super().__init__(**kwargs)

    def generate_from_text(
        self, text: str, cache_dir: str = None, path: str = None, **kwargs
    ) -> dict:
        """Generate speech audio from text using OmniVoice Studio."""
        if cache_dir is None:
            cache_dir = self.cache_dir

        # Remove SSML bookmarks if any
        input_text = text.replace("<bookmark ", "").replace("/>", "")
        # Clean up any remaining XML-like tags
        import re
        input_text = re.sub(r"<[^>]+>", "", input_text).strip()

        # Build input data for cache key
        input_data = {
            "input_text": input_text,
            "service": "omnivoice",
            "lang": self.lang,
            "gender": self.gender,
            "speed": self.speed,
        }

        # Check cache
        cached_result = self.get_cached_result(input_data, cache_dir)
        if cached_result is not None:
            return cached_result

        # Determine output path
        if path is None:
            audio_path = self.get_audio_basename(input_data) + ".wav"
        else:
            audio_path = path

        output_file = Path(cache_dir) / audio_path

        # Call TTS
        print(f"[OmniVoice] Lang={self.lang} | Text: {input_text[:60]}...")

        audio_bytes = None
        max_retries = 3

        if self.lang == "vi":
            # Vietnamese: use clone voice
            for attempt in range(max_retries):
                try:
                    job_id = _omni_clone_ref(
                        input_text,
                        self.ref_id,
                        speed=self.speed,
                        normalize=self.normalize,
                    )
                    audio_bytes = _poll_job(job_id)
                    break
                except Exception as e:
                    if attempt < max_retries - 1:
                        wait = 2 ** (attempt + 1)
                        print(f"[OmniVoice] Clone attempt {attempt+1} failed: {e}. Retry in {wait}s...")
                        time.sleep(wait)
                    else:
                        raise
        else:
            # English: use system voice
            voice_name = GENDER_MAP.get(self.gender, self.gender)
            result = _system_synthesize(input_text, voice=voice_name, normalize=self.normalize)
            audio_url = result.get("audio_url", "")
            if audio_url:
                audio_bytes = _download_audio(audio_url)
            else:
                raise RuntimeError(f"System TTS returned no audio_url: {result}")

        if audio_bytes is None:
            raise RuntimeError("No audio bytes received from TTS")

        # Save audio file
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "wb") as f:
            f.write(audio_bytes)

        print(f"[OmniVoice] Saved {len(audio_bytes)} bytes -> {output_file}")

        # Return result dict (manim-voiceover format)
        json_dict = {
            "input_text": text,
            "input_data": input_data,
            "original_audio": audio_path,
        }

        return json_dict
