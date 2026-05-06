"""
loss_landscape.py — Loss function surface and landscape visualization.

Scenes:
  - LossLandscape3D: 3D surface plot of a loss function with gradient descent path

Usage:
  manim -qm loss_landscape.py LossLandscape3D
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from manim import *
import numpy as np
from common_styles import *


class LossLandscape3D(ThreeDScene):
    """
    3D visualization of a loss function surface.
    Shows the loss landscape as a 3D surface with gradient descent path.

    L(w1, w2) = w1^2 + w2^2 + 0.5*sin(2*w1)*cos(2*w2) (non-convex landscape)
    """

    def construct(self):
        self.camera.background_color = C_DARK_BG

        # ─── Title (2D overlay) ───
        title = Text("Loss Landscape", font_size=TITLE_SIZE, color=C_BLUE)
        title.to_edge(UP, buff=0.5)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title, run_time=1))
        self.wait(0.5)
        self.play(FadeOut(title))

        # ─── 3D Setup ───
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[0, 6, 1],
            x_length=6,
            y_length=6,
            z_length=4,
            axis_config={"color": C_MUTED, "stroke_width": 1.5},
        )

        # Loss function
        def loss_func(u, v):
            return 0.4 * (u ** 2 + v ** 2) + 0.3

        surface = Surface(
            lambda u, v: axes.c2p(u, v, loss_func(u, v)),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(40, 40),
            fill_opacity=0.7,
            stroke_width=0.5,
            stroke_color=WHITE,
            stroke_opacity=0.1,
        )

        # Color the surface based on height
        surface.set_fill_by_value(
            axes=axes,
            colorscale=[
                (ManimColor(C_BLUE), 0),
                (ManimColor(C_TEAL), 1.5),
                (ManimColor(C_GREEN), 3),
                (ManimColor(C_YELLOW), 4.5),
                (ManimColor(C_RED), 6),
            ],
            axis=2,
        )

        # Camera angle
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)

        # Animate
        self.play(Create(axes), run_time=1)
        self.play(Create(surface), run_time=3)
        self.wait(1)

        # ─── Gradient Descent Path on Surface ───
        w1, w2 = 2.5, -2.0
        lr = 0.15
        n_steps = 20

        path_points = []
        for _ in range(n_steps):
            path_points.append(axes.c2p(w1, w2, loss_func(w1, w2)))
            # Gradient: [0.8*w1, 0.8*w2]
            gw1 = 0.8 * w1
            gw2 = 0.8 * w2
            w1 -= lr * gw1
            w2 -= lr * gw2

        path_points.append(axes.c2p(w1, w2, loss_func(w1, w2)))

        # Create path
        gd_path = VMobject(color=C_YELLOW, stroke_width=3)
        gd_path.set_points_smoothly(path_points)

        # Start and end dots
        start_dot = Dot3D(path_points[0], color=C_RED, radius=0.08)
        end_dot = Dot3D(path_points[-1], color=C_GREEN, radius=0.08)

        self.play(FadeIn(start_dot))
        self.play(
            Create(gd_path, run_time=4),
        )
        self.play(FadeIn(end_dot))
        self.wait(1)

        # ─── Rotate camera for dramatic effect ───
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(6)
        self.stop_ambient_camera_rotation()

        # ─── Label ───
        label = Text("Gradient Descent Path", font_size=BODY_SIZE, color=C_YELLOW)
        label.to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(label)
        self.play(FadeIn(label))
        self.wait(2)

        # Cleanup
        self.play(
            FadeOut(surface), FadeOut(axes), FadeOut(gd_path),
            FadeOut(start_dot), FadeOut(end_dot), FadeOut(label),
            run_time=2
        )
