"""
gradient_descent.py — Animated visualization of Gradient Descent algorithm.

Scenes:
  - GradientDescent2D: Classic 2D GD on a quadratic loss curve
  - GradientDescentContour: Contour plot with GD path (multi-variable)

Usage:
  manim -qm gradient_descent.py GradientDescent2D
  manim -qh gradient_descent.py GradientDescent2D
"""

import sys
from pathlib import Path

# Add templates directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from manim import *
import numpy as np
from common_styles import *


class GradientDescent2D(Scene):
    """
    Visualize Gradient Descent on a 1D quadratic loss function:
    L(w) = (w - w*)^2 + noise

    Shows:
    1. Title slide
    2. Loss function curve
    3. Initial point (random)
    4. Gradient computation (tangent line)
    5. Step-by-step descent with arrows
    6. Convergence to minimum
    7. Learning rate effect annotation
    """

    def construct(self):
        self.camera.background_color = C_DARK_BG

        # ─── Phase 1: Title ───
        create_title_slide(self, "Gradient Descent", "Tìm điểm cực tiểu của hàm mất mát")

        # ─── Phase 2: Setup axes and loss function ───
        axes = Axes(
            x_range=[-4, 6, 1],
            y_range=[-1, 10, 2],
            x_length=10,
            y_length=5.5,
            axis_config={"color": C_MUTED, "stroke_width": 2},
            tips=False,
        ).shift(DOWN * 0.3)

        x_label = axes.get_x_axis_label(
            Text("w (weight)", font_size=LABEL_SIZE, color=C_MUTED, font=DEFAULT_FONT)
        )
        y_label = axes.get_y_axis_label(
            Text("L(w)", font_size=LABEL_SIZE, color=C_MUTED, font=DEFAULT_FONT),
            edge=LEFT, direction=LEFT
        )

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=1.5)

        # Loss function: L(w) = 0.3 * (w - 2)^2 + 0.5
        def loss_func(w):
            return 0.3 * (w - 2) ** 2 + 0.5

        def loss_derivative(w):
            return 0.6 * (w - 2)

        curve = axes.plot(
            loss_func,
            x_range=[-3.5, 5.5],
            color=C_BLUE,
            stroke_width=3
        )
        curve_label = Text("L(w) = 0.3(w − 2)² + 0.5", font_size=SMALL_SIZE, color=C_BLUE, font=DEFAULT_FONT)
        curve_label.to_corner(UR, buff=0.5)

        self.play(Create(curve, run_time=2), FadeIn(curve_label))
        self.wait(0.5)

        # Mark the minimum
        min_dot = Dot(axes.c2p(2, loss_func(2)), color=C_GREEN, radius=0.06)
        min_label = Text("Minimum", font_size=SMALL_SIZE, color=C_GREEN, font=DEFAULT_FONT)
        min_label.next_to(min_dot, DOWN, buff=0.3)

        self.play(FadeIn(min_dot, scale=0.5), FadeIn(min_label))
        self.wait(0.5)

        # ─── Phase 3: Gradient Descent Animation ───
        # Starting point
        w = -2.0  # Start far from minimum
        learning_rate = 0.5
        n_steps = 20

        # Current position dot
        current_dot = Dot(axes.c2p(w, loss_func(w)), color=C_RED, radius=0.12)
        current_dot.set_z_index(10)

        w_text = Text(f"w = {w:.1f}", font_size=LABEL_SIZE, color=C_RED, font=DEFAULT_FONT)
        w_text.to_corner(UL, buff=0.5)

        lr_text = Text(f"η = {learning_rate}", font_size=LABEL_SIZE, color=C_ORANGE, font=DEFAULT_FONT)
        lr_text.next_to(w_text, DOWN, aligned_edge=LEFT, buff=0.2)

        step_text = Text("Step: 0", font_size=LABEL_SIZE, color=C_YELLOW, font=DEFAULT_FONT)
        step_text.next_to(lr_text, DOWN, aligned_edge=LEFT, buff=0.2)

        self.play(
            FadeIn(current_dot, scale=0.5),
            FadeIn(w_text),
            FadeIn(lr_text),
            FadeIn(step_text),
        )
        self.wait(1)

        # Show first gradient as tangent line
        grad = loss_derivative(w)
        tangent_x_range = [w - 1.5, w + 1.5]
        tangent = axes.plot(
            lambda x: loss_func(w) + grad * (x - w),
            x_range=tangent_x_range,
            color=C_YELLOW,
            stroke_width=2,
            stroke_opacity=0.7
        )
        grad_text = Text(
            f"∇L = {grad:.2f}",
            font_size=SMALL_SIZE, color=C_YELLOW, font=DEFAULT_FONT
        )
        grad_text.next_to(current_dot, UR, buff=0.3)

        self.play(Create(tangent), FadeIn(grad_text), run_time=1)
        self.wait(1)
        self.play(FadeOut(tangent), FadeOut(grad_text), run_time=0.5)

        # Descent loop
        trail_dots = VGroup()
        arrows_group = VGroup()

        for step in range(1, n_steps + 1):
            grad = loss_derivative(w)
            w_new = w - learning_rate * grad

            # Clamp to visible range
            w_new = np.clip(w_new, -3.5, 5.5)

            new_pos = axes.c2p(w_new, loss_func(w_new))
            old_pos = current_dot.get_center()

            # Trail dot at old position
            trail = Dot(old_pos, color=C_RED, radius=0.05, fill_opacity=0.4)
            trail_dots.add(trail)

            # Arrow showing direction
            arrow = Arrow(
                old_pos, new_pos,
                color=C_YELLOW,
                buff=0.12,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.15
            )
            arrows_group.add(arrow)

            # Update texts
            new_w_text = Text(f"w = {w_new:.2f}", font_size=LABEL_SIZE, color=C_RED, font=DEFAULT_FONT)
            new_w_text.to_corner(UL, buff=0.5)

            new_step_text = Text(f"Step: {step}", font_size=LABEL_SIZE, color=C_YELLOW, font=DEFAULT_FONT)
            new_step_text.next_to(lr_text, DOWN, aligned_edge=LEFT, buff=0.2)

            self.play(
                FadeIn(trail),
                GrowArrow(arrow),
                current_dot.animate.move_to(new_pos),
                Transform(w_text, new_w_text),
                Transform(step_text, new_step_text),
                run_time=0.8 if step > 2 else 1.2,
            )
            self.wait(0.3)

            w = w_new

            # Fade old arrows for clarity
            if step > 3:
                self.play(
                    arrows_group[:-1].animate.set_opacity(0.2),
                    run_time=0.3
                )

        # ─── Phase 4: Convergence highlight ───
        self.wait(0.5)

        converge_text = Text(
            "Hội tụ tại minimum!",
            font_size=BODY_SIZE,
            color=C_GREEN,
            font=DEFAULT_FONT
        )
        converge_text.next_to(axes, DOWN, buff=0.3)

        # Flash effect at minimum
        flash_circle = Circle(radius=0.3, color=C_GREEN, stroke_width=3)
        flash_circle.move_to(current_dot.get_center())

        self.play(
            FadeIn(converge_text),
            ShowPassingFlash(flash_circle, run_time=1.5, time_width=0.5),
        )
        self.wait(2)

        # ─── Phase 5: Cleanup ───
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1.5
        )
        self.wait(0.5)


class GradientDescentContour(Scene):
    """
    2D contour plot showing Gradient Descent path on a 2-variable function.
    f(x, y) = x^2 + 2*y^2

    Shows the descent trajectory from a starting point to the minimum (0,0).
    """

    def construct(self):
        self.camera.background_color = C_DARK_BG

        # ─── Title ───
        create_title_slide(
            self,
            "Gradient Descent — 2 Biến",
            "f(x, y) = x² + 2y²"
        )

        # ─── Setup ───
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": C_MUTED, "stroke_width": 1.5},
            tips=False,
        )

        x_label = axes.get_x_axis_label(
            Text("x₁", font_size=LABEL_SIZE, color=C_MUTED, font=DEFAULT_FONT)
        )
        y_label = axes.get_y_axis_label(
            Text("x₂", font_size=LABEL_SIZE, color=C_MUTED, font=DEFAULT_FONT),
            edge=LEFT, direction=LEFT
        )

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=1)

        # Draw contour lines (ellipses for f = x^2 + 2y^2 = c)
        contours = VGroup()
        for c in [0.5, 1, 2, 4, 8, 12, 18]:
            # x^2 + 2y^2 = c → ellipse with a=sqrt(c), b=sqrt(c/2)
            a = np.sqrt(c)
            b = np.sqrt(c / 2)
            if a > 4 or b > 3:
                continue
            ellipse = Ellipse(
                width=2 * a * (axes.x_length / 8),
                height=2 * b * (axes.y_length / 6),
                color=interpolate_color(
                    ManimColor(C_BLUE),
                    ManimColor(C_RED),
                    c / 18
                ),
                stroke_width=1.5,
                stroke_opacity=0.6,
                fill_opacity=0.03,
            )
            ellipse.move_to(axes.c2p(0, 0))
            contours.add(ellipse)

        self.play(
            LaggedStart(
                *[Create(c) for c in contours],
                lag_ratio=0.15,
                run_time=2
            )
        )

        # Mark minimum
        min_dot = Dot(axes.c2p(0, 0), color=C_GREEN, radius=0.1)
        min_label = Text("min", font_size=SMALL_SIZE, color=C_GREEN, font=DEFAULT_FONT)
        min_label.next_to(min_dot, DR, buff=0.15)
        self.play(FadeIn(min_dot), FadeIn(min_label))

        # ─── Gradient Descent Path ───
        x, y = 3.5, 2.5  # Starting point
        lr = 0.15
        n_steps = 15

        start_dot = Dot(axes.c2p(x, y), color=C_RED, radius=0.12)
        start_dot.set_z_index(10)
        start_label = Text("Start", font_size=SMALL_SIZE, color=C_RED, font=DEFAULT_FONT)
        start_label.next_to(start_dot, UR, buff=0.15)

        self.play(FadeIn(start_dot, scale=0.5), FadeIn(start_label))
        self.wait(0.5)

        path_points = [axes.c2p(x, y)]

        for step in range(n_steps):
            # Gradient of f = x^2 + 2y^2 is [2x, 4y]
            gx = 2 * x
            gy = 4 * y

            x_new = x - lr * gx
            y_new = y - lr * gy

            new_pos = axes.c2p(x_new, y_new)
            path_points.append(new_pos)

            x, y = x_new, y_new

        # Animate the path
        path_line = VMobject(color=C_YELLOW, stroke_width=2.5)
        path_line.set_points_as_corners(path_points)

        moving_dot = Dot(color=C_YELLOW, radius=0.08)
        moving_dot.set_z_index(11)
        moving_dot.move_to(path_points[0])

        self.play(FadeOut(start_label))
        self.play(
            Create(path_line, run_time=4),
            MoveAlongPath(moving_dot, path_line, run_time=4),
        )

        # Final position
        final_label = Text(
            f"({x:.2f}, {y:.2f})",
            font_size=SMALL_SIZE, color=C_YELLOW, font=DEFAULT_FONT
        )
        final_label.next_to(moving_dot, UL, buff=0.15)
        self.play(FadeIn(final_label))
        self.wait(2)

        # Cleanup
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1.5)
