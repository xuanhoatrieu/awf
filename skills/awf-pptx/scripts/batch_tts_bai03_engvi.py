"""Batch TTS for Bai 03 eng-vi - Clone voice with fallback to system."""
import json, sys, os, unicodedata, re
sys.path.insert(0, os.path.dirname(__file__))
from tts_client import synthesize

SCRIPT = r"g:\My Drive\1Work\BoMon_Tin\6_Deep_learning\pptx\output\bai_03_engvi\slide_script.json"
AUDIO_DIR = r"g:\My Drive\1Work\BoMon_Tin\6_Deep_learning\pptx\output\bai_03_engvi\audio"

def remove_diacritics(text):
    """Remove Vietnamese diacritics for clone voice compatibility."""
    # Normalize to decomposed form, remove combining marks
    nfkd = unicodedata.normalize('NFKD', text)
    result = ''.join(c for c in nfkd if not unicodedata.combining(c))
    # Fix special Vietnamese chars not handled by NFKD
    replacements = {'đ': 'd', 'Đ': 'D'}
    for k, v in replacements.items():
        result = result.replace(k, v)
    return result

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
    
    # Try clone with original text (keep diacritics)
    try:
        synthesize(text=note, mode="clone", output_path=fpath)
        s["audio"] = fname
        updated = True
        continue
    except Exception as e:
        print(f"[CLONE FAILED] {e}")
    
    # Fallback to system voice with original text
    try:
        print(f"[FALLBACK] Using system voice for {fname}")
        synthesize(text=note, mode="system", voice="female", output_path=fpath)
        s["audio"] = fname
        updated = True
    except Exception as e2:
        print(f"[ERROR] Both failed for {fname}: {e2}")

if updated:
    with open(SCRIPT, 'w', encoding='utf-8') as f:
        json.dump(slides, f, indent=2, ensure_ascii=False)
    print(f"\n[DONE] Updated {SCRIPT} with audio paths")
