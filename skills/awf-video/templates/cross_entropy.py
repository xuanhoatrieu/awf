"""
cross_entropy.py — Cross Entropy Loss explained visually (~2 min)

Phases:
  1. Title slide (5s)
  2. True vs Predicted probability distributions (18s)
  3. Entropy intuition: surprise & uncertainty (18s)
  4. Cross Entropy formula with annotations (18s)
  5. Step-by-step numerical example (25s)
  6. Good vs Bad prediction comparison (18s)
  7. Binary Cross Entropy: -log(q) graph (22s)
  8. Summary / Key Takeaways (16s)

  Total ≈ 140s ≈ 2 min 20s

Engine: ManimCE
"""

from manim import *
import numpy as np

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common_styles import *


class CrossEntropyScene(Scene):
    def construct(self):
        self.camera.background_color = C_DARK_BG

        # ── Phase 1: Title (5s) ──────────────────────────────────
        self.phase_title()

        # ── Phase 2: Two distributions (18s) ─────────────────────
        self.phase_distributions()

        # ── Phase 3: Entropy intuition (18s) ─────────────────────
        self.phase_entropy_intuition()

        # ── Phase 4: Cross Entropy formula (18s) ─────────────────
        self.phase_formula()

        # ── Phase 5: Numerical example (25s) ─────────────────────
        self.phase_example()

        # ── Phase 6: Good vs Bad prediction (18s) ────────────────
        self.phase_comparison()

        # ── Phase 7: Binary Cross Entropy graph (22s) ────────────
        self.phase_binary_ce()

        # ── Phase 8: Softmax + CE pipeline (20s) ─────────────────
        self.phase_softmax_pipeline()

        # ── Phase 9: Summary (16s) ───────────────────────────────
        self.phase_summary()

    # ================================================================
    # PHASE 1 — Title
    # ================================================================
    def phase_title(self):
        title = Text("Cross Entropy Loss", font_size=52, color=C_BLUE, font=DEFAULT_FONT)
        subtitle = Text(
            "Measuring the gap between prediction and truth",
            font_size=BODY_SIZE, color=C_MUTED, font=DEFAULT_FONT,
        )
        subtitle.next_to(title, DOWN, buff=0.5)

        self.play(Write(title, run_time=1.5))
        self.play(FadeIn(subtitle, shift=UP * 0.3, run_time=1))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))

    # ================================================================
    # PHASE 2 — True vs Predicted distributions
    # ================================================================
    def phase_distributions(self):
        header = Text("Two Probability Distributions", font_size=SUBTITLE_SIZE,
                       color=WHITE, font=DEFAULT_FONT).to_edge(UP, buff=0.5)
        self.play(Write(header, run_time=1))

        # Class labels
        classes = ["Cat", "Dog", "Bird"]
        true_probs = [1.0, 0.0, 0.0]       # one-hot: Cat
        pred_probs = [0.7, 0.2, 0.1]       # model prediction

        # Build bar charts side by side
        true_bars = self._create_bar_chart(
            classes, true_probs, C_GREEN, "True  p(x)", LEFT * 3.2
        )
        pred_bars = self._create_bar_chart(
            classes, pred_probs, C_BLUE, "Predicted  q(x)", RIGHT * 3.2
        )

        self.play(FadeIn(true_bars, shift=UP * 0.3, run_time=1.2))
        self.wait(1)
        self.play(FadeIn(pred_bars, shift=UP * 0.3, run_time=1.2))
        self.wait(2)

        # Explanatory text
        explain = Text(
            "Cross Entropy measures how well q approximates p",
            font_size=LABEL_SIZE, color=C_YELLOW, font=DEFAULT_FONT,
        ).to_edge(DOWN, buff=0.6)
        self.play(Write(explain, run_time=1.5))
        self.wait(3)

        self.play(*[FadeOut(m) for m in self.mobjects])

    def _create_bar_chart(self, labels, values, color, title_text, position):
        """Helper: create a simple vertical bar chart."""
        group = VGroup()

        # Title
        title = Text(title_text, font_size=LABEL_SIZE, color=color, font=DEFAULT_FONT)

        # Bars
        bar_width = 0.6
        bar_spacing = 0.9
        max_height = 2.5
        bars = VGroup()
        bar_labels = VGroup()

        for i, (lbl, val) in enumerate(zip(labels, values)):
            h = max(val * max_height, 0.05)
            bar = Rectangle(
                width=bar_width, height=h,
                fill_color=color, fill_opacity=0.7,
                stroke_color=color, stroke_width=1.5,
            )
            bar.move_to(ORIGIN + RIGHT * (i - 1) * bar_spacing)
            bar.align_to(ORIGIN + DOWN * 1.2, DOWN)

            # Value label on top
            val_text = Text(f"{val:.1f}", font_size=SMALL_SIZE, color=WHITE, font=DEFAULT_FONT)
            val_text.next_to(bar, UP, buff=0.1)

            # Class label below
            cls_text = Text(lbl, font_size=SMALL_SIZE, color=C_MUTED, font=DEFAULT_FONT)
            cls_text.next_to(bar, DOWN, buff=0.15)
            cls_text.align_to(ORIGIN + DOWN * 1.2, UP)
            cls_text.shift(DOWN * 0.3)

            bars.add(VGroup(bar, val_text))
            bar_labels.add(cls_text)

        group.add(title, bars, bar_labels)
        title.next_to(bars, UP, buff=0.4)
        group.move_to(position + DOWN * 0.3)
        return group

    # ================================================================
    # PHASE 3 — Entropy intuition (NEW)
    # ================================================================
    def phase_entropy_intuition(self):
        header = Text("Entropy: Measuring Surprise", font_size=SUBTITLE_SIZE,
                       color=WHITE, font=DEFAULT_FONT).to_edge(UP, buff=0.5)
        self.play(Write(header, run_time=1))

        # Entropy formula
        entropy_formula = MathTex(
            r"H(p) = -\sum_{x} p(x) \log p(x)",
            font_size=40, color=WHITE,
        )
        entropy_formula.next_to(header, DOWN, buff=0.6)
        self.play(Write(entropy_formula, run_time=1.5))
        self.wait(1.5)

        # Show two contrasting distributions
        # Certain: [1, 0, 0] → H = 0
        certain_title = Text("Certain", font_size=LABEL_SIZE, color=C_GREEN, font=DEFAULT_FONT)
        certain_dist = MathTex(r"p = [1, 0, 0]", font_size=26, color=WHITE)
        certain_h = MathTex(r"H = 0", font_size=28, color=C_GREEN)
        certain_note = Text("No surprise", font_size=18, color=C_MUTED, font=DEFAULT_FONT)
        certain_group = VGroup(certain_title, certain_dist, certain_h, certain_note).arrange(DOWN, buff=0.25)

        # Uncertain: [0.33, 0.33, 0.33] → H = log(3) ≈ 1.099
        uncertain_title = Text("Uncertain", font_size=LABEL_SIZE, color=C_RED, font=DEFAULT_FONT)
        uncertain_dist = MathTex(r"p = [0.33, 0.33, 0.33]", font_size=26, color=WHITE)
        uncertain_h = MathTex(r"H = 1.099", font_size=28, color=C_RED)
        uncertain_note = Text("Maximum surprise", font_size=18, color=C_MUTED, font=DEFAULT_FONT)
        uncertain_group = VGroup(uncertain_title, uncertain_dist, uncertain_h, uncertain_note).arrange(DOWN, buff=0.25)

        # Position side by side
        both = VGroup(certain_group, uncertain_group).arrange(RIGHT, buff=2.5)
        both.next_to(entropy_formula, DOWN, buff=0.8)

        self.play(FadeIn(certain_group, shift=UP * 0.3, run_time=1))
        self.wait(1)
        self.play(FadeIn(uncertain_group, shift=UP * 0.3, run_time=1))
        self.wait(1.5)

        # Transition text
        transition = Text(
            "Cross Entropy extends this to compare TWO distributions",
            font_size=LABEL_SIZE, color=C_YELLOW, font=DEFAULT_FONT,
        ).to_edge(DOWN, buff=0.6)
        self.play(Write(transition, run_time=1.5))
        self.wait(2.5)

        self.play(*[FadeOut(m) for m in self.mobjects])

    # ================================================================
    # PHASE 4 — The Formula
    # ================================================================
    def phase_formula(self):
        header = Text("The Cross Entropy Formula", font_size=SUBTITLE_SIZE,
                       color=WHITE, font=DEFAULT_FONT).to_edge(UP, buff=0.5)
        self.play(Write(header, run_time=1))

        # Main formula
        formula = MathTex(
            r"H(p, q) = -\sum_{x} p(x) \log q(x)",
            font_size=44, color=WHITE,
        )
        formula.move_to(UP * 0.5)
        box = SurroundingRectangle(
            formula, buff=0.3, color=C_BLUE, corner_radius=0.15,
            fill_color=C_BLUE, fill_opacity=0.08, stroke_width=2,
        )

        self.play(Write(formula, run_time=2))
        self.play(Create(box, run_time=0.8))
        self.wait(1.5)

        # Annotations
        p_label = Text("true distribution", font_size=SMALL_SIZE,
                        color=C_GREEN, font=DEFAULT_FONT)
        q_label = Text("predicted distribution", font_size=SMALL_SIZE,
                        color=C_BLUE, font=DEFAULT_FONT)

        p_label.next_to(formula, DOWN, buff=0.8).shift(LEFT * 2.5)
        q_label.next_to(formula, DOWN, buff=0.8).shift(RIGHT * 2.5)

        # Arrows from labels to formula parts
        p_arrow = Arrow(p_label.get_top(), formula.get_bottom() + LEFT * 1.0,
                         color=C_GREEN, stroke_width=2, buff=0.15)
        q_arrow = Arrow(q_label.get_top(), formula.get_bottom() + RIGHT * 1.0,
                         color=C_BLUE, stroke_width=2, buff=0.15)

        self.play(
            FadeIn(p_label, shift=UP * 0.2),
            GrowArrow(p_arrow),
            run_time=1,
        )
        self.play(
            FadeIn(q_label, shift=UP * 0.2),
            GrowArrow(q_arrow),
            run_time=1,
        )
        self.wait(2)

        # Key insight
        insight = Text(
            "Lower CE = better prediction",
            font_size=BODY_SIZE, color=C_YELLOW, font=DEFAULT_FONT,
        ).to_edge(DOWN, buff=0.7)
        self.play(Write(insight, run_time=1))
        self.wait(2.5)

        self.play(*[FadeOut(m) for m in self.mobjects])

    # ================================================================
    # PHASE 5 — Numerical example
    # ================================================================
    def phase_example(self):
        header = Text("Step-by-Step Calculation", font_size=SUBTITLE_SIZE,
                       color=WHITE, font=DEFAULT_FONT).to_edge(UP, buff=0.5)
        self.play(Write(header, run_time=1))

        # Setup
        setup = MathTex(
            r"p = [1, 0, 0]", r"\quad", r"q = [0.7, 0.2, 0.1]",
            font_size=32, color=WHITE,
        )
        setup[0].set_color(C_GREEN)
        setup[2].set_color(C_BLUE)
        setup.next_to(header, DOWN, buff=0.6)
        self.play(Write(setup, run_time=1.2))
        self.wait(1.5)

        # Expansion
        expand = MathTex(
            r"H = -\Big[",
            r"1 \cdot \log(0.7)",
            r"+\, 0 \cdot \log(0.2)",
            r"+\, 0 \cdot \log(0.1)",
            r"\Big]",
            font_size=30, color=WHITE,
        )
        expand.next_to(setup, DOWN, buff=0.7)
        self.play(Write(expand, run_time=2))
        self.wait(2)

        # Highlight non-zero term
        highlight_box = SurroundingRectangle(
            expand[1], color=C_YELLOW, stroke_width=2, buff=0.1,
        )
        note = Text(
            "Only the true class matters!",
            font_size=LABEL_SIZE, color=C_YELLOW, font=DEFAULT_FONT,
        )
        note.next_to(highlight_box, DOWN, buff=0.5)

        self.play(Create(highlight_box), Write(note, run_time=1))

        # Grey out zero terms
        self.play(
            expand[2].animate.set_opacity(0.3),
            expand[3].animate.set_opacity(0.3),
            run_time=0.8,
        )
        self.wait(2)

        # Final result
        result = MathTex(
            r"H = -\log(0.7) \approx 0.357",
            font_size=36, color=C_YELLOW,
        )
        result.next_to(note, DOWN, buff=0.7)
        result_box = SurroundingRectangle(
            result, buff=0.25, color=C_YELLOW, corner_radius=0.1,
            fill_color=C_YELLOW, fill_opacity=0.08, stroke_width=2,
        )
        self.play(Write(result, run_time=1.2), Create(result_box, run_time=0.8))
        self.wait(3)

        self.play(*[FadeOut(m) for m in self.mobjects])

    # ================================================================
    # PHASE 6 — Good vs Bad prediction comparison
    # ================================================================
    def phase_comparison(self):
        header = Text("Good vs Bad Prediction", font_size=SUBTITLE_SIZE,
                       color=WHITE, font=DEFAULT_FONT).to_edge(UP, buff=0.5)
        self.play(Write(header, run_time=1))

        # ── Good prediction ──
        good_title = Text("Good prediction", font_size=LABEL_SIZE,
                           color=C_GREEN, font=DEFAULT_FONT)
        good_q = MathTex(r"q = [0.9, 0.05, 0.05]", font_size=28, color=WHITE)
        good_ce_val = -np.log(0.9)
        good_ce = MathTex(
            rf"H = -\log(0.9) = {good_ce_val:.3f}",
            font_size=28, color=C_GREEN,
        )
        good_group = VGroup(good_title, good_q, good_ce).arrange(DOWN, buff=0.35)
        good_box = SurroundingRectangle(
            good_group, buff=0.35, color=C_GREEN, corner_radius=0.15,
            fill_color=C_GREEN, fill_opacity=0.06, stroke_width=2,
        )

        # ── Bad prediction ──
        bad_title = Text("Bad prediction", font_size=LABEL_SIZE,
                          color=C_RED, font=DEFAULT_FONT)
        bad_q = MathTex(r"q = [0.1, 0.6, 0.3]", font_size=28, color=WHITE)
        bad_ce_val = -np.log(0.1)
        bad_ce = MathTex(
            rf"H = -\log(0.1) = {bad_ce_val:.3f}",
            font_size=28, color=C_RED,
        )
        bad_group = VGroup(bad_title, bad_q, bad_ce).arrange(DOWN, buff=0.35)
        bad_box = SurroundingRectangle(
            bad_group, buff=0.35, color=C_RED, corner_radius=0.15,
            fill_color=C_RED, fill_opacity=0.06, stroke_width=2,
        )

        # Position
        VGroup(
            VGroup(good_box, good_group),
            VGroup(bad_box, bad_group),
        ).arrange(RIGHT, buff=1.5).next_to(header, DOWN, buff=0.8)

        self.play(
            FadeIn(good_group, shift=UP * 0.3),
            Create(good_box),
            run_time=1.2,
        )
        self.wait(1.5)
        self.play(
            FadeIn(bad_group, shift=UP * 0.3),
            Create(bad_box),
            run_time=1.2,
        )
        self.wait(2)

        # Arrow + conclusion
        arrow_left = Arrow(ORIGIN, LEFT * 1.5, color=C_GREEN, stroke_width=3)
        arrow_right = Arrow(ORIGIN, RIGHT * 1.5, color=C_RED, stroke_width=3)

        low_text = Text("Low loss", font_size=LABEL_SIZE, color=C_GREEN, font=DEFAULT_FONT)
        high_text = Text("High loss", font_size=LABEL_SIZE, color=C_RED, font=DEFAULT_FONT)

        compare_row = VGroup(
            VGroup(low_text, arrow_left).arrange(DOWN, buff=0.2),
            VGroup(high_text, arrow_right).arrange(DOWN, buff=0.2),
        ).arrange(RIGHT, buff=2).to_edge(DOWN, buff=0.7)

        self.play(
            FadeIn(compare_row, shift=UP * 0.3),
            run_time=1,
        )
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects])

    # ================================================================
    # PHASE 7 — Binary Cross Entropy graph
    # ================================================================
    def phase_binary_ce(self):
        header = Text("Binary Cross Entropy", font_size=SUBTITLE_SIZE,
                       color=WHITE, font=DEFAULT_FONT).to_edge(UP, buff=0.5)
        self.play(Write(header, run_time=1))

        # Formula
        bce_formula = MathTex(
            r"L = -\big[ y \log(\hat{y}) + (1-y) \log(1-\hat{y}) \big]",
            font_size=32, color=WHITE,
        )
        bce_formula.next_to(header, DOWN, buff=0.4)
        self.play(Write(bce_formula, run_time=1.5))
        self.wait(1)

        # Graph: -log(q) for true class y=1
        axes = Axes(
            x_range=[0.01, 1.0, 0.2],
            y_range=[0, 5, 1],
            x_length=8,
            y_length=4,
            axis_config={"color": C_MUTED, "stroke_width": 2, "include_ticks": True},
            tips=False,
        ).shift(DOWN * 0.5)

        x_label = axes.get_x_axis_label(
            MathTex(r"\hat{y}", font_size=28, color=C_MUTED),
            direction=DOWN,
        )
        y_label = axes.get_y_axis_label(
            MathTex(r"-\log(\hat{y})", font_size=26, color=C_MUTED),
            direction=LEFT,
        )

        self.play(Create(axes, run_time=1), FadeIn(x_label), FadeIn(y_label))

        # Plot curve
        graph = axes.plot(
            lambda x: -np.log(x),
            x_range=[0.02, 1.0, 0.005],
            color=C_YELLOW,
            stroke_width=3,
        )
        graph_label = Text(
            "Loss when y = 1", font_size=SMALL_SIZE,
            color=C_YELLOW, font=DEFAULT_FONT,
        )
        graph_label.next_to(axes, RIGHT, buff=0.3).shift(UP * 0.5)

        self.play(Create(graph, run_time=2))
        self.play(FadeIn(graph_label))
        self.wait(1.5)

        # Annotate key points
        # q close to 1 → loss ≈ 0
        dot_good = Dot(axes.c2p(0.9, -np.log(0.9)), color=C_GREEN, radius=0.1)
        label_good = Text("q=0.9 : low loss", font_size=18,
                           color=C_GREEN, font=DEFAULT_FONT)
        label_good.next_to(dot_good, UR, buff=0.15)

        # q close to 0 → loss → ∞
        dot_bad = Dot(axes.c2p(0.1, min(-np.log(0.1), 4.8)),
                       color=C_RED, radius=0.1)
        label_bad = Text("q=0.1 : high loss", font_size=18,
                          color=C_RED, font=DEFAULT_FONT)
        label_bad.next_to(dot_bad, RIGHT, buff=0.15)

        self.play(
            FadeIn(dot_good, scale=0.5),
            Write(label_good, run_time=0.8),
        )
        self.wait(1)
        self.play(
            FadeIn(dot_bad, scale=0.5),
            Write(label_bad, run_time=0.8),
        )
        self.wait(3)

        self.play(*[FadeOut(m) for m in self.mobjects])

    # ================================================================
    # PHASE 8 — Softmax + Cross Entropy pipeline
    # ================================================================
    def phase_softmax_pipeline(self):
        header = Text("In Practice: Softmax + Cross Entropy", font_size=SUBTITLE_SIZE,
                       color=WHITE, font=DEFAULT_FONT).to_edge(UP, buff=0.5)
        self.play(Write(header, run_time=1))

        # Step 1: Raw logits
        logits_label = Text("Raw logits (model output)", font_size=LABEL_SIZE,
                             color=C_MUTED, font=DEFAULT_FONT)
        logits = MathTex(r"z = [2.0,\; 1.0,\; 0.1]", font_size=30, color=WHITE)
        logits_group = VGroup(logits_label, logits).arrange(DOWN, buff=0.2)
        logits_group.next_to(header, DOWN, buff=0.6)
        self.play(FadeIn(logits_group, shift=UP * 0.3, run_time=1))
        self.wait(1.5)

        # Step 2: Softmax arrow
        softmax_arrow = Arrow(logits_group.get_bottom(), logits_group.get_bottom() + DOWN * 1.0,
                               color=C_ORANGE, stroke_width=3, buff=0.1)
        softmax_label = Text("Softmax", font_size=LABEL_SIZE,
                              color=C_ORANGE, font=DEFAULT_FONT)
        softmax_label.next_to(softmax_arrow, RIGHT, buff=0.2)

        # Compute softmax manually
        z = np.array([2.0, 1.0, 0.1])
        probs = np.exp(z) / np.exp(z).sum()

        prob_text = MathTex(
            rf"q = [{probs[0]:.3f},\; {probs[1]:.3f},\; {probs[2]:.3f}]",
            font_size=30, color=C_BLUE,
        )
        prob_text.next_to(softmax_arrow, DOWN, buff=0.3)

        self.play(GrowArrow(softmax_arrow), Write(softmax_label, run_time=0.8))
        self.play(Write(prob_text, run_time=1.2))
        self.wait(1.5)

        # Step 3: Cross Entropy arrow
        ce_arrow = Arrow(prob_text.get_bottom(), prob_text.get_bottom() + DOWN * 1.0,
                          color=C_YELLOW, stroke_width=3, buff=0.1)
        ce_label = Text("Cross Entropy", font_size=LABEL_SIZE,
                         color=C_YELLOW, font=DEFAULT_FONT)
        ce_label.next_to(ce_arrow, RIGHT, buff=0.2)

        # CE with true = class 0
        ce_val = -np.log(probs[0])
        loss_text = MathTex(
            rf"L = -\log({probs[0]:.3f}) = {ce_val:.3f}",
            font_size=30, color=C_YELLOW,
        )
        loss_text.next_to(ce_arrow, DOWN, buff=0.3)
        loss_box = SurroundingRectangle(
            loss_text, buff=0.2, color=C_YELLOW, corner_radius=0.1,
            fill_color=C_YELLOW, fill_opacity=0.08, stroke_width=2,
        )

        self.play(GrowArrow(ce_arrow), Write(ce_label, run_time=0.8))
        self.play(Write(loss_text, run_time=1.2), Create(loss_box, run_time=0.8))
        self.wait(3)

        self.play(*[FadeOut(m) for m in self.mobjects])

    # ================================================================
    # PHASE 9 — Summary
    # ================================================================
    def phase_summary(self):
        title = Text("Key Takeaways", font_size=SUBTITLE_SIZE,
                      color=C_BLUE, font=DEFAULT_FONT).to_edge(UP, buff=0.8)
        self.play(Write(title, run_time=1))

        points = [
            "Entropy = average surprise of a distribution",
            "Cross Entropy = expected surprise using q instead of p",
            "Only the true class probability matters (one-hot)",
            "Lower CE = better prediction",
            "Standard loss for classification in Deep Learning",
        ]

        bullet_group = VGroup()
        for i, text in enumerate(points):
            bullet = Text(f"  {text}", font_size=22,
                          color=WHITE, font=DEFAULT_FONT)
            bullet_group.add(bullet)

        bullet_group.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        bullet_group.next_to(title, DOWN, buff=0.7)

        for bullet in bullet_group:
            self.play(FadeIn(bullet, shift=RIGHT * 0.3, run_time=0.8))
            self.wait(0.5)

        self.wait(2)

        # Final formula flash
        final = MathTex(
            r"H(p, q) = -\sum p(x) \log q(x)",
            font_size=44, color=C_YELLOW,
        ).to_edge(DOWN, buff=1)
        final_box = SurroundingRectangle(
            final, buff=0.3, color=C_YELLOW, corner_radius=0.15,
            fill_color=C_YELLOW, fill_opacity=0.1, stroke_width=2,
        )
        self.play(Write(final, run_time=1.5), Create(final_box, run_time=1))
        self.wait(3)

        self.play(*[FadeOut(m) for m in self.mobjects])
