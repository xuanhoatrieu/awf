"""
TTS Client for OmniVoice Studio
Port from vitts-tts.provider.ts to Python

3 modes:
  - auto: model picks best voice
  - clone: clone from saved reference (ref_id=9 for user's voice)
  - system: use preset system voices (Binh/Ngoc etc.)

Usage:
  python tts_client.py --text "Xin chao" --mode auto --output test.wav
  python tts_client.py --text "Xin chao" --mode clone --ref-id 9 --output test.wav
  python tts_client.py --text "Xin chao" --mode system --voice Ngoc --output test.wav
"""

import requests
import json
import sys
import os
import time
import argparse

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ============================================================
# CONFIG
# ============================================================

API_URL = "http://117.0.36.6:8888"
API_KEY = "vneu_-q_okdL9TzB-sIMW1AQqNt0Z_qIoE05TN4s6H5snGEs"

HEADERS = {"X-API-Key": API_KEY}

POLL_INTERVAL = 2       # seconds
MAX_POLL_DURATION = 180  # seconds

# Voice flag mapping
VOICE_PRESETS = {
    "male": "Binh",
    "female": "Ngoc",
}

# ============================================================
# OMNIVOICE MODES (async - job polling)
# ============================================================

def omni_auto(text, speed=1.0, num_step=32, normalize=True):
    """Auto mode - model picks best voice."""
    resp = requests.post(
        f"{API_URL}/api/v1/omnivoice/generate-auto",
        headers=HEADERS,
        json={"text": text, "speed": speed, "num_step": num_step, "normalize": normalize},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["job_id"]


def omni_clone_ref(text, ref_id, speed=1.0, num_step=32, normalize=True):
    """Clone mode - clone from saved reference."""
    # This endpoint uses form-urlencoded (matching TS provider)
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


def system_synthesize(text, voice="Ngoc", normalize=True):
    """System voice mode - uses /api/v1/tts/synthesize (sync)."""
    resp = requests.post(
        f"{API_URL}/api/v1/tts/synthesize",
        headers=HEADERS,
        json={"text": text, "voice": voice, "normalize": normalize},
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()


# ============================================================
# JOB POLLING (for omnivoice async endpoints)
# ============================================================

def poll_job(job_id):
    """Poll an async OmniVoice job until completion."""
    print(f"[TTS] Polling job {job_id}...")
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
                duration = job.get("duration_sec", 0)
                proc_time = job.get("processing_time_sec", 0)
                print(f"[TTS] Job done ({duration:.1f}s audio, {proc_time:.1f}s processing)")
                return download_audio(audio_url)
            raise RuntimeError(f"Job {job_id} completed but no audio_url")

        if status in ("failed", "error"):
            raise RuntimeError(f"Job failed: {job.get('error', 'Unknown')}")

    raise TimeoutError(f"Job {job_id} timed out after {MAX_POLL_DURATION}s")


def download_audio(audio_url):
    """Download audio bytes from URL."""
    full_url = audio_url if audio_url.startswith("http") else f"{API_URL}{audio_url}"
    resp = requests.get(full_url, headers=HEADERS, timeout=60)
    resp.raise_for_status()
    return resp.content


# ============================================================
# PUBLIC API
# ============================================================

def synthesize(text, mode="system", voice="female", ref_id=9,
               speed=1.0, num_step=32, normalize=True, output_path="output.wav"):
    """
    Synthesize text to speech.

    Args:
        text: Text to speak
        mode: "auto", "clone", or "system"
        voice: Voice preset for system mode (male/female/Binh/Ngoc/...)
        ref_id: Reference ID for clone mode (default 9 = user's clone)
        speed: Speech speed (1.0 = normal)
        num_step: Number of inference steps (32 default)
        normalize: Enable SEA-G2P normalization
        output_path: Path to save audio file

    Returns:
        Path to saved audio file
    """
    print(f"[TTS] Mode: {mode} | Voice: {voice} | Normalize: {normalize}")
    print(f"[TTS] Text: {text[:80]}{'...' if len(text) > 80 else ''}")

    audio_bytes = None

    if mode == "auto":
        job_id = omni_auto(text, speed, num_step, normalize)
        audio_bytes = poll_job(job_id)

    elif mode == "clone":
        # Retry with backoff — clone API may return 400 transiently under load
        max_retries = 3
        for attempt in range(max_retries):
            try:
                job_id = omni_clone_ref(text, ref_id, speed, num_step, normalize)
                audio_bytes = poll_job(job_id)
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    wait = 2 ** (attempt + 1)  # 2s, 4s, 8s
                    print(f"[TTS] Clone attempt {attempt+1} failed: {e}. Retry in {wait}s...")
                    time.sleep(wait)
                else:
                    raise

    elif mode == "system":
        # Resolve voice alias
        voice_id = VOICE_PRESETS.get(voice, voice)
        result = system_synthesize(text, voice_id, normalize)

        # System endpoint returns JSON with audio_url
        audio_url = result.get("audio_url", "")
        if audio_url:
            audio_bytes = download_audio(audio_url)
        else:
            raise RuntimeError(f"System TTS returned no audio_url: {result}")

    else:
        raise ValueError(f"Unknown mode: {mode}")

    # Save to file
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(audio_bytes)

    print(f"[TTS] Saved {len(audio_bytes)} bytes -> {output_path}")
    return output_path


# ============================================================
# VOICE DISCOVERY
# ============================================================

def list_voices():
    """List all available voices."""
    voices = []

    # System preset voices
    try:
        resp = requests.get(f"{API_URL}/api/v1/tts/voices", headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            for v in resp.json():
                voices.append({"id": v["id"], "name": v["name"], "type": "system"})
    except Exception as e:
        print(f"[WARN] System voices: {e}")

    # Saved references (for clone mode)
    try:
        resp = requests.get(f"{API_URL}/api/v1/refs", headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            for ref in resp.json():
                voices.append({
                    "id": f"ref:{ref['id']}",
                    "name": ref.get("name", f"Ref {ref['id']}"),
                    "type": "clone_ref",
                    "duration": ref.get("duration_sec"),
                })
    except Exception as e:
        print(f"[WARN] Refs: {e}")

    # Trained voices
    try:
        resp = requests.get(f"{API_URL}/api/v1/tts/trained-voices", headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            for v in resp.json():
                voices.append({
                    "id": f"trained:{v['id']}",
                    "name": v.get("name", f"Trained {v['id']}"),
                    "type": "trained",
                })
    except Exception as e:
        print(f"[WARN] Trained voices: {e}")

    return voices


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="TTS Client for OmniVoice Studio")
    sub = parser.add_subparsers(dest="command", help="Command")

    # Synthesize command
    syn = sub.add_parser("speak", help="Synthesize text to audio")
    syn.add_argument("--text", required=True, help="Text to synthesize")
    syn.add_argument("--mode", choices=["auto", "clone", "system"], default="system")
    syn.add_argument("--voice", default="female", help="Voice: male/female/Binh/Ngoc/...")
    syn.add_argument("--ref-id", default="c8495f76-c047-47e1-8a77-1cb651bb6511", help="Ref ID for clone mode (UUID)")
    syn.add_argument("--output", default="output.wav", help="Output file path")
    syn.add_argument("--speed", type=float, default=1.0)
    syn.add_argument("--normalize", action="store_true", default=True, help="SEA-G2P normalize (default: on)")
    syn.add_argument("--no-normalize", action="store_true", help="Disable SEA-G2P")

    # List voices command
    sub.add_parser("voices", help="List available voices")

    args = parser.parse_args()

    if args.command == "voices":
        voices = list_voices()
        print(json.dumps(voices, indent=2, ensure_ascii=False))
        return

    if args.command == "speak":
        normalize = not args.no_normalize
        result = synthesize(
            text=args.text, mode=args.mode, voice=args.voice,
            ref_id=args.ref_id, speed=args.speed, normalize=normalize,
            output_path=args.output,
        )
        print(f"\n[DONE] {result}")
        return

    # Default: quick test
    print("Quick test (system, female voice)...")
    synthesize("Xin chao, day la bai thu nghiem.", output_path="test_tts.wav")


if __name__ == "__main__":
    main()
