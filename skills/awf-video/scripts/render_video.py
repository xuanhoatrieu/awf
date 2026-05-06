"""
render_video.py — Wrapper script for rendering Manim videos.

Supports DUAL ENGINE:
  - ManimCE (manim)  — CLI batch render, default
  - ManimGL (manimgl) — 3b1b's interactive/record engine

Handles:
  1. Render using ManimCE or ManimGL
  2. Auto-create video/ output directory
  3. Copy final output to video/<name>.mp4
  4. Support custom resolution/orientation

Usage:
  python render_video.py <scene_file> <SceneName> [options]

Examples:
  # ManimCE (default): 1080p landscape
  python render_video.py gradient_descent.py GradientDescent2D

  # ManimGL (3b1b engine): record to file
  python render_video.py 3b1b_videos/_2017/nn/part1.py NetworkScene --engine 3b1b

  # Custom output name + quality
  python render_video.py scene.py MyScene --name my_video --quality draft
"""

import argparse
import subprocess
import shutil
import sys
import re
from pathlib import Path

# ============================================================
# CONFIG
# ============================================================

# Project root (where video/ directory will be created)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
# → g:\My Drive\1Work\BoMon_Tin\6_Deep_learning

VIDEO_OUTPUT_DIR = PROJECT_ROOT / "video"

# 3b1b videos repo location
VIDEOS_3B1B_DIR = PROJECT_ROOT / "3b1b_videos"

# Quality presets (ManimCE)
QUALITY_PRESETS = {
    "preview": {
        "flag": "-ql",
        "resolution": "480p",
        "fps": 15,
        "subdir": "480p15",
    },
    "draft": {
        "flag": "-qm",
        "resolution": "720p",
        "fps": 30,
        "subdir": "720p30",
    },
    "final": {
        "flag": "-qh",
        "resolution": "1080p",
        "fps": 60,
        "subdir": "1080p60",
    },
    "ultra": {
        "flag": "-qp",
        "resolution": "1440p",
        "fps": 60,
        "subdir": "1440p60",
    },
    "4k": {
        "flag": "-qk",
        "resolution": "2160p",
        "fps": 60,
        "subdir": "2160p60",
    },
}

# Orientation presets
ORIENTATION_PRESETS = {
    "landscape": None,          # Use default 16:9
    "portrait": "1080,1920",    # 9:16
    "square": "1080,1080",      # 1:1
}


# ============================================================
# ManimCE RENDER
# ============================================================

def render_manimce(
    scene_path: Path,
    scene_name: str,
    quality: str,
    orientation: str,
) -> Path:
    """Render using ManimCE (manim). Returns path to rendered file."""
    preset = QUALITY_PRESETS[quality]

    # Build command
    cmd = ["manim"]

    orientation_res = ORIENTATION_PRESETS.get(orientation)
    if orientation_res is not None:
        cmd.extend(["-r", orientation_res])
        cmd.extend(["--fps", str(preset["fps"])])
    else:
        cmd.append(preset["flag"])

    cmd.extend([str(scene_path), scene_name])

    print(f"[ManimCE] Command: {' '.join(cmd)}")
    print(f"[ManimCE] Quality: {preset['resolution']} @ {preset['fps']}fps")
    print(f"[ManimCE] Orientation: {orientation}")
    print()

    result = subprocess.run(cmd, cwd=str(scene_path.parent))

    if result.returncode != 0:
        print(f"\n[ERROR] ManimCE render failed (exit code {result.returncode})")
        sys.exit(1)

    # Find rendered file
    media_dir = scene_path.parent / "media" / "videos" / scene_path.stem
    rendered_file = None

    for subdir in media_dir.iterdir() if media_dir.exists() else []:
        if subdir.is_dir():
            candidate = subdir / f"{scene_name}.mp4"
            if candidate.exists():
                rendered_file = candidate
                break

    if rendered_file is None and media_dir.exists():
        for f in media_dir.rglob(f"{scene_name}.mp4"):
            rendered_file = f
            break

    if rendered_file is None:
        print(f"\n[ERROR] Could not find rendered file in: {media_dir}")
        sys.exit(1)

    return rendered_file


# ============================================================
# ManimGL (3b1b) RENDER
# ============================================================

def render_manimgl(
    scene_path: Path,
    scene_name: str,
    quality: str,
) -> Path:
    """Render using ManimGL (3b1b's engine). Returns path to rendered file."""

    # ManimGL quality flags
    mgl_quality = {
        "preview": ["-l"],             # low quality
        "draft": ["-m"],               # medium
        "final": ["--hd"],             # 1080p
        "ultra": ["--uhd"],            # 4K
        "4k": ["--uhd"],               # 4K
    }

    flags = mgl_quality.get(quality, ["--hd"])

    # Build command: manimgl <file> <Scene> -w (write to file)
    cmd = ["manimgl", str(scene_path), scene_name, "-w"] + flags

    print(f"[ManimGL] Command: {' '.join(cmd)}")
    print(f"[ManimGL] Quality: {quality}")
    print(f"[ManimGL] Mode: Write to file (-w)")
    print()

    # ManimGL needs PYTHONPATH to include the repo root for imports
    import os
    env = os.environ.copy()
    repo_root = str(VIDEOS_3B1B_DIR)
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{repo_root};{scene_path.parent};{existing}"

    # Ensure FFmpeg and LaTeX (MiKTeX) are in PATH for ManimGL
    extra_paths = [
        r"D:\ffmpeg-2026\bin",
        r"C:\Users\xuanh\AppData\Local\Programs\MiKTeX\miktex\bin\x64",
    ]
    env["PATH"] = ";".join(extra_paths) + ";" + env.get("PATH", "")

    result = subprocess.run(
        cmd,
        cwd=str(scene_path.parent),
        env=env,
    )

    if result.returncode != 0:
        print(f"\n[ERROR] ManimGL render failed (exit code {result.returncode})")
        print("[HINT] ManimGL requires OpenGL. If on headless/remote, use ManimCE instead.")
        sys.exit(1)

    # ManimGL saves to: <repo>/videos/<year>/<topic>/<SceneName>.mp4
    # or <repo>/output/ depending on config
    search_dirs = [
        VIDEOS_3B1B_DIR / "videos",
        VIDEOS_3B1B_DIR / "output",
        scene_path.parent / "videos",
        scene_path.parent / "media" / "videos",
        Path.home() / "Videos",
    ]

    rendered_file = None
    for search_dir in search_dirs:
        if search_dir.exists():
            for f in search_dir.rglob(f"*{scene_name}*.mp4"):
                rendered_file = f
                break
        if rendered_file:
            break

    if rendered_file is None:
        print(f"\n[ERROR] Could not find ManimGL output for {scene_name}")
        print(f"[HINT] Searched in: {[str(d) for d in search_dirs]}")
        sys.exit(1)

    return rendered_file


# ============================================================
# MAIN RENDER FUNCTION
# ============================================================

def render_video(
    scene_file: str,
    scene_name: str,
    output_name: str = None,
    quality: str = "final",
    orientation: str = "landscape",
    engine: str = "auto",
):
    """
    Render a Manim scene and copy output to video/ directory.

    Args:
        scene_file: Path to the .py file
        scene_name: Scene class name
        output_name: Output filename (no ext)
        quality: Quality preset
        orientation: Orientation preset
        engine: "ce" (ManimCE), "3b1b" (ManimGL), or "auto" (detect)
    """
    scene_path = Path(scene_file).resolve()
    if not scene_path.exists():
        print(f"[ERROR] Scene file not found: {scene_path}")
        sys.exit(1)

    # Determine output name
    if output_name is None:
        output_name = re.sub(r"(?<!^)(?=[A-Z])", "_", scene_name).lower()

    # Validate quality
    if quality not in QUALITY_PRESETS:
        print(f"[ERROR] Unknown quality: {quality}. Options: {list(QUALITY_PRESETS.keys())}")
        sys.exit(1)

    # Auto-detect engine
    if engine == "auto":
        # Check if the file uses manimlib (3b1b) imports
        try:
            content = scene_path.read_text(encoding="utf-8", errors="ignore")
            if "manimlib" in content or "from manimlib" in content:
                engine = "3b1b"
            elif str(scene_path).replace("\\", "/").find("3b1b_videos") != -1:
                engine = "3b1b"
            else:
                engine = "ce"
        except Exception:
            engine = "ce"

    print(f"{'='*60}")
    print(f"[RENDER] Engine: {'ManimGL (3b1b)' if engine == '3b1b' else 'ManimCE'}")
    print(f"[RENDER] File: {scene_path.name}")
    print(f"[RENDER] Scene: {scene_name}")
    print(f"{'='*60}")

    # Ensure video/ directory exists
    VIDEO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Render
    if engine == "3b1b":
        rendered_file = render_manimgl(scene_path, scene_name, quality)
    else:
        rendered_file = render_manimce(scene_path, scene_name, quality, orientation)

    # Copy to video/ directory
    final_output = VIDEO_OUTPUT_DIR / f"{output_name}.mp4"
    shutil.copy2(rendered_file, final_output)

    print(f"\n{'='*60}")
    print(f"[DONE] Video saved to: {final_output}")
    print(f"[DONE] Size: {final_output.stat().st_size / 1024 / 1024:.1f} MB")
    print(f"{'='*60}")

    return final_output


def main():
    parser = argparse.ArgumentParser(
        description="Render Manim video (dual engine) and save to video/",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Engine modes:
  auto  — Auto-detect based on imports (DEFAULT)
  ce    — Force ManimCE (manim, community edition)
  3b1b  — Force ManimGL (manimgl, 3b1b's engine)

Quality presets:
  preview  — 480p   (fast debug)
  draft    — 720p   (review)
  final    — 1080p  (production, DEFAULT)
  ultra    — 1440p
  4k       — 2160p  (very slow)

Examples:
  # Auto-detect engine (ManimCE for our templates, ManimGL for 3b1b code)
  python render_video.py gradient_descent.py GradientDescent2D

  # Force 3b1b engine for repo code
  python render_video.py 3b1b_videos/_2017/nn/part1.py NetworkScene --engine 3b1b

  # Preview quality
  python render_video.py scene.py MyScene --name my_video -q preview
        """,
    )

    parser.add_argument("scene_file", help="Path to the .py scene file")
    parser.add_argument("scene_name", help="Name of the Scene class to render")
    parser.add_argument("--name", "-n", help="Output filename (snake_case, no extension)")
    parser.add_argument(
        "--quality", "-q",
        choices=list(QUALITY_PRESETS.keys()),
        default="final",
        help="Quality preset (default: final = 1080p)",
    )
    parser.add_argument(
        "--orientation", "-o",
        choices=list(ORIENTATION_PRESETS.keys()),
        default="landscape",
        help="Orientation (default: landscape = 16:9)",
    )
    parser.add_argument(
        "--engine", "-e",
        choices=["auto", "ce", "3b1b"],
        default="auto",
        help="Render engine (default: auto-detect)",
    )

    args = parser.parse_args()

    render_video(
        scene_file=args.scene_file,
        scene_name=args.scene_name,
        output_name=args.name,
        quality=args.quality,
        orientation=args.orientation,
        engine=args.engine,
    )


if __name__ == "__main__":
    main()
