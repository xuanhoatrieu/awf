"""Batch TTS for Bai 03 - Generate audio for all slides."""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from tts_client import synthesize

SCRIPT = r"g:\My Drive\1Work\BoMon_Tin\6_Deep_learning\pptx\output\bai_03\slide_script.json"
AUDIO_DIR = r"g:\My Drive\1Work\BoMon_Tin\6_Deep_learning\pptx\output\bai_03\audio"

with open(SCRIPT, 'r', encoding='utf-8') as f:
    slides = json.load(f)

os.makedirs(AUDIO_DIR, exist_ok=True)
updated = False

for i, s in enumerate(slides):
    note = s.get("note", "")
    if not note:
        continue
    fname = f"slide_{i+1:02d}.wav"
    fpath = os.path.join(AUDIO_DIR, fname)
    if os.path.exists(fpath):
        print(f"[SKIP] {fname} already exists")
        s["audio"] = fname
        updated = True
        continue
    print(f"\n[{i+1}/{len(slides)}] Generating {fname}...")
    try:
        synthesize(text=note, mode="system", voice="female", output_path=fpath)
        s["audio"] = fname
        updated = True
    except Exception as e:
        print(f"[ERROR] {fname}: {e}")

# Save updated script with audio paths
if updated:
    with open(SCRIPT, 'w', encoding='utf-8') as f:
        json.dump(slides, f, indent=2, ensure_ascii=False)
    print(f"\n[DONE] Updated {SCRIPT} with audio paths")
