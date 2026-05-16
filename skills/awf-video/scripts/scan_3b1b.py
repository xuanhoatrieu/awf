"""Scan 3b1b_videos repo for ML-related scenes"""
import re
from pathlib import Path

repo = Path(r"g:\My Drive\1Work\BoMon_Tin\6_Deep_learning\3b1b_videos")

files = [
    ("_2017/nn/part1.py", "NN Part1"),
    ("_2017/nn/part2.py", "NN Part2"),
    ("_2017/nn/part3.py", "NN Part3"),
    ("_2017/gradient.py", "Gradient"),
    ("_2024/transformers/ml_basics.py", "ML Basics"),
    ("_2024/transformers/mlp.py", "MLP"),
    ("_2024/transformers/attention.py", "Attention"),
    ("_2024/transformers/embedding.py", "Embedding"),
]

# Check cross_entropy
ce_dir = repo / "_2026" / "cross_entropy"
if ce_dir.exists():
    for f in ce_dir.glob("*.py"):
        files.append((f"_2026/cross_entropy/{f.name}", f"CrossEntropy/{f.name}"))

for path, name in files:
    fpath = repo / path
    if fpath.exists():
        content = fpath.read_text(encoding="utf-8", errors="ignore")
        scenes = re.findall(r"^class (\w+)\(", content, re.M)
        size_kb = fpath.stat().st_size / 1024
        print(f"\n{name} ({size_kb:.0f}KB) — {len(scenes)} scenes:")
        for s in scenes[:15]:
            print(f"  - {s}")
    else:
        print(f"\n{name}: NOT FOUND")
