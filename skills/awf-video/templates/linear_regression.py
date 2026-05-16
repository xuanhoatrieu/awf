"""
linear_regression.py — Linear Regression fitting animation.

Scenes:
  - LinearRegressionFit: Shows data points and the best-fit line being found
  - LinearRegressionGD: Gradient descent optimizing the line step by step

Usage:
  manim -qm linear_regression.py LinearRegressionFit
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from manim import *
import numpy as np
from common_styles import *


class LinearRegressionFit(Scene):
    """
    Visualize Linear Regression:
    1. Show scatter data
    2. Try a random line (bad fit)
    3. Show residuals (error lines)
    4. Rotate line to best fit
    5. Show MSE decreasing
    """

    def construct(self):
        self.camera.background_color = C_DARK_BG

        # ─── Title ───
        create_title_slide(self, "Linear Regression", "Tìm đường thẳng phù hợp nhất")

        # ─── Setup ───
        np.random.seed(42)
        n_points = 20

        # Generate data: y = 0.8x + 1 + noise
        true_slope = 0.8
        true_intercept = 1.0
        x_data = np.linspace(-3, 4, n_points) + np.random.normal(0, 0.3, n_points)
        y_data = true_slope * x_data + true_intercept + np.random.normal(0, 0.8, n_points)

        axes = Axes(
            x_range=[-5, 6, 1],
            y_range=[-3, 7, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": C_MUTED, "stroke_width": 2},
            tips=False,
        ).shift(DOWN * 0.3)

        x_label = axes.get_x_axis_label(
            Text("x", font_size=LABEL_SIZE, color=C_MUTED)
        )
        y_label = axes.get_y_axis_label(
            Text("y", font_size=LABEL_SIZE, color=C_MUTED),
            edge=LEFT, direction=LEFT
        )

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=1)

        # ─── Data Points ───
        dots = create_data_points(x_data, y_data, axes, color=C_DATA_1, radius=0.06)

        self.play(
            LaggedStart(
                *[FadeIn(d, scale=0.5) for d in dots],
                lag_ratio=0.05,
                run_time=2
            )
        )
        self.wait(0.5)

        # ─── Initial bad line ───
        bad_slope = -0.2
        bad_intercept = 3.0

        line = axes.plot(
            lambda x: bad_slope * x + bad_intercept,
            x_range=[-4.5, 5.5],
            color=C_RED,
            stroke_width=3,
        )
        line_label = Text(
            f"ŷ = {bad_slope:.1f}x + {bad_intercept:.1f}",
            font_size=SMALL_SIZE, color=C_RED
        )
        line_label.to_corner(UR, buff=0.5)

        self.play(Create(line), FadeIn(line_label), run_time=1)
        self.wait(0.5)

        # ─── Show residuals ───
        residuals = VGroup()
        for x, y in zip(x_data, y_data):
            y_pred = bad_slope * x + bad_intercept
            res_line = Line(
                axes.c2p(x, y), axes.c2p(x, y_pred),
                color=C_NEGATIVE, stroke_width=1.5, stroke_opacity=0.6
            )
            residuals.add(res_line)

        residual_label = Text("Residuals (sai số)", font_size=SMALL_SIZE, color=C_NEGATIVE)
        residual_label.next_to(axes, DOWN, buff=0.3)

        self.play(
            LaggedStart(
                *[Create(r) for r in residuals],
                lag_ratio=0.03, run_time=1.5
            ),
            FadeIn(residual_label),
        )
        self.wait(1)

        # ─── Animate line fitting ───
        n_frames = 30
        slopes = np.linspace(bad_slope, true_slope, n_frames)
        intercepts = np.linspace(bad_intercept, true_intercept, n_frames)

        for i in range(n_frames):
            s = slopes[i]
            b = intercepts[i]

            new_line = axes.plot(
                lambda x, s=s, b=b: s * x + b,
                x_range=[-4.5, 5.5],
                color=interpolate_color(
                    ManimColor(C_RED), ManimColor(C_GREEN),
                    i / n_frames
                ),
                stroke_width=3,
            )

            new_residuals = VGroup()
            for x, y in zip(x_data, y_data):
                y_pred = s * x + b
                res_line = Line(
                    axes.c2p(x, y), axes.c2p(x, y_pred),
                    color=C_NEGATIVE, stroke_width=1.5,
                    stroke_opacity=0.4
                )
                new_residuals.add(res_line)

            new_label = Text(
                f"ŷ = {s:.2f}x + {b:.2f}",
                font_size=SMALL_SIZE,
                color=interpolate_color(
                    ManimColor(C_RED), ManimColor(C_GREEN),
                    i / n_frames
                )
            )
            new_label.to_corner(UR, buff=0.5)

            if i % 3 == 0 or i == n_frames - 1:
                self.play(
                    Transform(line, new_line),
                    Transform(residuals, new_residuals),
                    Transform(line_label, new_label),
                    run_time=0.2
                )

        self.wait(0.5)

        # ─── Best fit highlight ───
        self.play(FadeOut(residuals), FadeOut(residual_label))

        best_label = Text("Best Fit!", font_size=BODY_SIZE, color=C_GREEN)
        best_label.next_to(axes, DOWN, buff=0.3)

        self.play(FadeIn(best_label))
        self.wait(2)

        # Cleanup
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1.5)
