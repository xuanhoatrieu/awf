"""
common_styles.py — Shared color palette, fonts, and utility functions
for all AWF-Video Manim scenes.

Inspired by 3Blue1Brown's visual design system.
"""

from manim import *
import numpy as np

# ============================================================
# COLOR PALETTE — 3b1b-inspired, extended for ML education
# ============================================================

# Primary colors
C_BLUE = "#58C4DD"       # 3b1b classic blue
C_TEAL = "#5CD0B3"       # 3b1b teal
C_GREEN = "#83C167"      # 3b1b green  
C_YELLOW = "#FFFF00"     # 3b1b yellow
C_RED = "#FC6255"        # 3b1b red/pink
C_MAROON = "#C55F73"     # 3b1b maroon
C_PURPLE = "#9A72AC"     # 3b1b purple
C_ORANGE = "#FF8C00"     # 3b1b orange

# Dark background
C_DARK_BG = "#1C1C2E"    # Deep dark blue-black
C_DARK_GREY = "#333333"

# Accent / functional colors
C_POSITIVE = "#83C167"   # For positive values, correct answers
C_NEGATIVE = "#FC6255"   # For negative values, errors
C_HIGHLIGHT = "#FFFF00"  # For emphasis
C_MUTED = "#888888"      # For secondary elements
C_GRADIENT_START = "#3B82F6"
C_GRADIENT_END = "#8B5CF6"

# Neural Network specific
C_NEURON = "#58C4DD"
C_WEIGHT_POS = "#83C167"
C_WEIGHT_NEG = "#FC6255"
C_ACTIVATION = "#FFFF00"
C_BIAS = "#FF8C00"

# Data visualization
C_DATA_1 = "#58C4DD"     # Class 1
C_DATA_2 = "#FC6255"     # Class 2
C_DATA_3 = "#83C167"     # Class 3
C_REGRESSION_LINE = "#FFFF00"
C_DECISION_BOUNDARY = "#9A72AC"


# ============================================================
# FONT CONFIG
# ============================================================

DEFAULT_FONT = "Times New Roman"  # Supports Vietnamese diacritics

TITLE_SIZE = 48
SUBTITLE_SIZE = 36
BODY_SIZE = 28
LABEL_SIZE = 24
SMALL_SIZE = 20
FORMULA_SIZE = 36


# ============================================================
# COMMON CONFIGURATIONS
# ============================================================

DEFAULT_AXES_CONFIG = {
    "x_range": [-5, 5, 1],
    "y_range": [-3, 3, 1],
    "x_length": 10,
    "y_length": 6,
    "axis_config": {
        "color": C_MUTED,
        "stroke_width": 2,
        "include_ticks": True,
        "tick_size": 0.05,
    },
    "tips": False,
}

DEFAULT_3D_AXES_CONFIG = {
    "x_range": [-3, 3, 1],
    "y_range": [-3, 3, 1],
    "z_range": [-2, 2, 1],
    "x_length": 6,
    "y_length": 6,
    "z_length": 4,
}


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def create_title_slide(scene, title_text, subtitle_text=None, wait_time=2):
    """Create a standard title slide with optional subtitle."""
    title = Text(title_text, font_size=TITLE_SIZE, color=C_BLUE, font=DEFAULT_FONT)
    title.to_edge(UP, buff=1.5)

    elements = [Write(title, run_time=1.5)]

    if subtitle_text:
        subtitle = Text(subtitle_text, font_size=SUBTITLE_SIZE, color=C_MUTED, font=DEFAULT_FONT)
        subtitle.next_to(title, DOWN, buff=0.5)
        elements.append(FadeIn(subtitle, shift=UP * 0.3, run_time=1))

    scene.play(*elements)
    scene.wait(wait_time)

    if subtitle_text:
        scene.play(FadeOut(title), FadeOut(subtitle))
    else:
        scene.play(FadeOut(title))


def create_labeled_dot(position, label_text, color=C_BLUE, label_direction=UP, radius=0.08):
    """Create a dot with a label next to it."""
    dot = Dot(point=position, radius=radius, color=color)
    label = Text(label_text, font_size=SMALL_SIZE, color=color, font=DEFAULT_FONT)
    label.next_to(dot, label_direction, buff=0.15)
    return VGroup(dot, label)


def create_data_points(x_data, y_data, axes, color=C_DATA_1, radius=0.06):
    """Create a group of data point dots on given axes."""
    dots = VGroup()
    for x, y in zip(x_data, y_data):
        dot = Dot(
            point=axes.c2p(x, y),
            radius=radius,
            color=color,
            fill_opacity=0.8
        )
        dots.add(dot)
    return dots


def create_equation_box(equation_text, color=C_BLUE, buff=0.3):
    """Create a highlighted equation in a rounded rectangle."""
    try:
        eq = MathTex(equation_text, font_size=FORMULA_SIZE, color=WHITE)
    except Exception:
        # Fallback if LaTeX is not available
        eq = Text(equation_text, font_size=BODY_SIZE, color=WHITE)

    box = SurroundingRectangle(
        eq, buff=buff,
        color=color,
        corner_radius=0.1,
        fill_color=color,
        fill_opacity=0.1,
        stroke_width=2
    )
    return VGroup(box, eq)


def animate_arrow_sequence(scene, items, direction=RIGHT, buff=0.5, arrow_color=C_MUTED):
    """Animate a sequence of items connected by arrows."""
    arrows = []
    for i in range(len(items) - 1):
        arrow = Arrow(
            items[i].get_right() if direction == RIGHT else items[i].get_bottom(),
            items[i + 1].get_left() if direction == RIGHT else items[i + 1].get_top(),
            color=arrow_color,
            buff=0.1,
            stroke_width=2,
        )
        arrows.append(arrow)

    for item in items:
        scene.play(FadeIn(item, shift=direction * 0.3), run_time=0.5)
    for arrow in arrows:
        scene.play(GrowArrow(arrow), run_time=0.3)

    return VGroup(*items, *arrows)


def sigmoid(x):
    """Sigmoid activation function."""
    return 1 / (1 + np.exp(-x))


def relu(x):
    """ReLU activation function."""
    return np.maximum(0, x)


def softmax(x):
    """Softmax function for arrays."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()
