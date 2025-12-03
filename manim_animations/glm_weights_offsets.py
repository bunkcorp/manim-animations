from manim import *

# Render:
# manim -pqh glm_weights_offsets.py WeightsOffsetsGLM

class WeightsOffsetsGLM(Scene):
    def construct(self):
        title = Text("Weights vs. Offsets in GLMs", weight=BOLD)
        subtitle = Text("Different roles in fitting & prediction", font_size=28)
        subtitle.next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(title, shift=UP*0.5), FadeIn(subtitle, shift=UP*0.5))
        self.wait(0.5)

        # --- Base GLM formula ---
        formula = Tex(r"GLM: \quad \eta = X\beta", tex_environment="align").scale(1.1)
        formula.next_to(subtitle, DOWN, buff=0.8)
        self.play(Write(formula))
        self.wait(0.5)

        # Split screen: left=Weights, right=Offsets
        weights_title = Text("Weights", font_size=28, color=BLUE).to_edge(LEFT).shift(DOWN*1.0)
        offsets_title = Text("Offsets", font_size=28, color=GREEN).to_edge(RIGHT).shift(DOWN*1.0)
        self.play(FadeIn(weights_title), FadeIn(offsets_title))

        # --- Weights panel ---
        # Simulated "data points" with varying sizes
        axes_w = Axes(x_range=[0,5], y_range=[0,5], x_length=4.0, y_length=3.0,
                      axis_config={"stroke_color": GREY_B, "stroke_width": 2}).to_edge(LEFT, buff=0.7).shift(DOWN*0.8)
        pts = VGroup(
            Dot(axes_w.c2p(1,1), radius=0.05, color=BLUE),
            Dot(axes_w.c2p(2,2.5), radius=0.12, color=BLUE),
            Dot(axes_w.c2p(3,3.2), radius=0.08, color=BLUE),
            Dot(axes_w.c2p(4,4.1), radius=0.15, color=BLUE),
        )
        self.play(Create(axes_w), FadeIn(pts, lag_ratio=0.2))
        note_w = Text("Weights → adjust influence in fitting", color=BLUE, font_size=20)
        note_w.next_to(axes_w, DOWN, buff=0.2)
        self.play(Write(note_w))
        self.wait(0.4)

        # Formula stays the same
        formula_w = Tex(r"\eta = X\beta", color=BLUE, tex_environment="align").scale(0.9).next_to(axes_w, UP, buff=0.2)
        self.play(Write(formula_w))
        self.wait(0.3)

        # --- Offsets panel ---
        axes_o = Axes(x_range=[0,5], y_range=[0,5], x_length=4.0, y_length=3.0,
                      axis_config={"stroke_color": GREY_B, "stroke_width": 2}).to_edge(RIGHT, buff=0.7).shift(DOWN*0.8)
        pts_o = VGroup(
            Dot(axes_o.c2p(1,1.6), radius=0.08, color=GREEN),
            Dot(axes_o.c2p(2,2.9), radius=0.08, color=GREEN),
            Dot(axes_o.c2p(3,3.7), radius=0.08, color=GREEN),
            Dot(axes_o.c2p(4,4.8), radius=0.08, color=GREEN),
        )
        self.play(Create(axes_o), FadeIn(pts_o, lag_ratio=0.2))
        note_o = Text("Offset → enters predictor with coeff = 1", color=GREEN, font_size=20)
        note_o.next_to(axes_o, DOWN, buff=0.2)
        self.play(Write(note_o))
        self.wait(0.4)

        formula_o = Tex(r"\eta = X\beta + \text{offset}", color=GREEN, tex_environment="align").scale(0.9).next_to(axes_o, UP, buff=0.2)
        self.play(Write(formula_o))
        self.wait(0.5)

        # --- Poisson Exposure Example ---
        exposure_title = Text("Actuarial Example: Poisson with Exposure", font_size=24)
        exposure_title.to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title, exposure_title))
        
        # Show exposure offset
        exposure_formula = VGroup(
            Text("Claim Count ~ Poisson(λ × Exposure)", color=YELLOW, font_size=20),
            Text("log(λ) = Xβ + log(Exposure)", color=YELLOW, font_size=20),
            Text("η = Xβ + offset", color=YELLOW, font_size=20)
        ).arrange(DOWN, buff=0.3)
        exposure_formula.to_edge(LEFT, buff=0.5).shift(DOWN*0.5)
        self.play(FadeIn(exposure_formula))
        
        # Show the effect
        effect = VGroup(
            Text("Effect:", font_size=20, weight=BOLD),
            Text("• Exposure = 2 years → offset = log(2) ≈ 0.69", font_size=18),
            Text("• Model predicts log(rate), not log(count)", font_size=18),
            Text("• Rate = exp(Xβ) × exposure", font_size=18)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        effect.to_edge(RIGHT, buff=0.5).shift(DOWN*0.5)
        self.play(FadeIn(effect))
        self.wait(0.8)

        # --- Summary card ---
        takeaway = VGroup(
            RoundedRectangle(width=12.5, height=1.7, corner_radius=0.2).set_stroke(WHITE,2).set_fill(DARK_GREY,0.08),
            Tex(
                r"\textbf{Summary:} Weights change how much each obs influences fitting. ",
                r"Offsets enter directly into $\eta$ (linear predictor) with coeff 1.",
                tex_environment="flushleft"
            ).scale(0.9)
        )
        takeaway[1].move_to(takeaway[0].get_center())
        takeaway.to_edge(DOWN, buff=0.4)
        self.play(Create(takeaway[0]), Write(takeaway[1]))
        self.wait(1.0)
