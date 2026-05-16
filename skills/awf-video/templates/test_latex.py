"""Quick test: LaTeX rendering in ManimCE"""
from manim import *

class TestLatex(Scene):
    def construct(self):
        self.camera.background_color = "#1C1C2E"
        
        title = Text("LaTeX Test", font_size=48, color="#58C4DD")
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP))
        
        # Test MathTex
        formulas = VGroup(
            MathTex(r"\nabla f = \frac{\partial f}{\partial x}", font_size=42),
            MathTex(r"\sigma(x) = \frac{1}{1+e^{-x}}", font_size=42, color=YELLOW),
            MathTex(r"J(\theta) = \frac{1}{2m}\sum_{i=1}^{m}(h_\theta(x^{(i)})-y^{(i)})^2", font_size=36, color="#83C167"),
        )
        formulas.arrange(DOWN, buff=0.6)
        
        for f in formulas:
            self.play(Write(f, run_time=1.5))
            self.wait(0.5)
        
        self.wait(1)
