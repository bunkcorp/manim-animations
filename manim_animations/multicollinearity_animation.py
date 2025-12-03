from manim import *
import numpy as np

# --- Configuration ---
CONFIG = {
    "colors": {
        "background": "#1E1E2A",
        "primary_text": WHITE,
        "secondary_text": LIGHT_GREY,
        "model_color": TEAL,
        "predictor1_color": BLUE,
        "predictor2_color": YELLOW,
        "correlated_color": ORANGE,
        "response_color": GREEN,
        "error_color": RED,
    },
    "font_sizes": {
        "title": 48,
        "header": 32,
        "text": 24,
        "label": 20,
    },
}

class MulticollinearityAnimation(Scene):
    def construct(self):
        self.camera.background_color = CONFIG["colors"]["background"]

        # --- Scene 1: Introduction to the GLM ---
        self.show_intro()

        # --- Scene 2: The Ideal Model (Uncorrelated Predictors) ---
        self.show_ideal_model()

        # --- Scene 3: Introducing Multicollinearity ---
        self.introduce_multicollinearity()

        # --- Scene 4: The Problem & Consequences ---
        self.show_the_problem()

        # --- Scene 5: Summary ---
        self.show_summary()

    def show_intro(self):
        """Sets the stage by introducing the topic."""
        title = Text("The Problem with Correlated Predictors", font_size=CONFIG["font_sizes"]["title"])
        subtitle = Text("Understanding Multicollinearity in a GLM", font_size=CONFIG["font_sizes"]["header"], color=CONFIG["colors"]["secondary_text"]).next_to(title, DOWN)
        
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(2)
        self.play(FadeOut(VGroup(title, subtitle)))

    def show_ideal_model(self):
        """Shows a healthy model with independent predictors."""
        title = Text("The Ideal Model: Independent Predictors", font_size=CONFIG["font_sizes"]["header"]).to_edge(UP)
        self.play(Write(title))

        # The Model Equation
        equation = MathTex(
            r"\text{Health}", r" \approx \beta_1(", r"\text{Sunlight}", r") + \beta_2(", r"\text{Water}", r")",
            tex_to_color_map={
                "Health": CONFIG["colors"]["response_color"],
                "Sunlight": CONFIG["colors"]["predictor1_color"],
                "Water": CONFIG["colors"]["predictor2_color"],
            }
        ).next_to(title, DOWN, buff=0.7)
        self.play(Write(equation))
        self.wait(1)

        # Analogy: Levers controlling plant health
        levers_text = Text("The model can easily tell their effects apart.", font_size=CONFIG["font_sizes"]["text"]).next_to(equation, DOWN, buff=1)
        self.play(Write(levers_text))

        sun_lever = self._create_control_lever("Sunlight", CONFIG["colors"]["predictor1_color"], -1)
        water_lever = self._create_control_lever("Water", CONFIG["colors"]["predictor2_color"], 1)
        VGroup(sun_lever, water_lever).arrange(RIGHT, buff=2).next_to(levers_text, DOWN, buff=0.7)

        self.play(FadeIn(sun_lever), FadeIn(water_lever))
        
        # Show stable, independent control
        self.play(sun_lever.slider.animate.set_value(1), rate_func=there_and_back, run_time=2)
        self.play(water_lever.slider.animate.set_value(1), rate_func=there_and_back, run_time=2)
        self.wait(1)

        conclusion = Text("The coefficients (β) are stable and interpretable.", font_size=CONFIG["font_sizes"]["text"], color=GREEN).next_to(sun_lever.get_bottom() + DOWN, DOWN)
        self.play(Write(conclusion))
        self.wait(2)

        self.play(FadeOut(VGroup(title, equation, levers_text, sun_lever, water_lever, conclusion)))

    def introduce_multicollinearity(self):
        """Introduces two highly correlated variables."""
        title = Text("The Problem Model: Correlated Predictors", font_size=CONFIG["font_sizes"]["header"]).to_edge(UP)
        self.play(Write(title))

        # New equation with correlated predictors
        equation = MathTex(
            r"\text{Health}", r" \approx \beta_1(", r"\text{Fertilizer A}", r") + \beta_2(", r"\text{Fertilizer B}", r")",
            tex_to_color_map={
                "Health": CONFIG["colors"]["response_color"],
                "Fertilizer A": CONFIG["colors"]["correlated_color"],
                "Fertilizer B": CONFIG["colors"]["correlated_color"],
            }
        ).next_to(title, DOWN, buff=0.7)
        self.play(Write(equation))

        explanation = Text("But what if Fertilizers A and B are almost identical?", font_size=CONFIG["font_sizes"]["text"]).next_to(equation, DOWN, buff=0.5)
        self.play(Write(explanation))

        # Show the correlation visually
        correlation_text = Text("They are used together and do the same thing.", font_size=CONFIG["font_sizes"]["text"]).next_to(explanation, DOWN, buff=0.7)
        self.play(Write(correlation_text))

        axes = Axes(x_range=[0, 10], y_range=[0, 10], x_length=5, y_length=5, axis_config={"include_tip": False}).next_to(correlation_text, DOWN, buff=0.5)
        x_label = axes.get_x_axis_label(Tex("Fertilizer A"), edge=DOWN, direction=DOWN)
        y_label = axes.get_y_axis_label(Tex("Fertilizer B"), edge=LEFT, direction=LEFT)
        
        dots = VGroup()
        for i in range(25):
            x = np.random.uniform(1, 9)
            y = x + np.random.normal(0, 0.3)
            dots.add(Dot(axes.c2p(x, y), radius=0.05, color=CONFIG["colors"]["correlated_color"]))

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(LaggedStart(*[Create(d) for d in dots], lag_ratio=0.1))

        multicollinearity_label = Text("This is MULTICOLLINEARITY", font_size=CONFIG["font_sizes"]["header"], color=CONFIG["colors"]["correlated_color"]).next_to(axes, RIGHT, buff=1)
        self.play(Write(multicollinearity_label))
        self.wait(3)

        self.play(FadeOut(VGroup(title, equation, explanation, correlation_text, axes, x_label, y_label, dots, multicollinearity_label)))

    def show_the_problem(self):
        """Explains the consequences of multicollinearity."""
        title = Text("The Model Gets Confused", font_size=CONFIG["font_sizes"]["header"]).to_edge(UP)
        self.play(Write(title))

        question = Text("Which fertilizer gets the credit for improving plant health?", font_size=CONFIG["font_sizes"]["text"]).next_to(title, DOWN, buff=0.7)
        self.play(Write(question))
        self.wait(1)

        # Analogy: Unstable seesaw for coefficients
        seesaw = Line(LEFT * 2.5, RIGHT * 2.5, stroke_width=8, color=GRAY)
        fulcrum = Triangle(fill_opacity=1, color=GRAY).scale(0.3).next_to(seesaw, DOWN, buff=0)
        seesaw_group = VGroup(seesaw, fulcrum).next_to(question, DOWN, buff=1)
        self.play(Create(seesaw_group))

        beta1_label = MathTex(r"\beta_1 (\text{Fert. A})", color=CONFIG["colors"]["correlated_color"]).next_to(seesaw.get_start(), DOWN)
        beta2_label = MathTex(r"\beta_2 (\text{Fert. B})", color=CONFIG["colors"]["correlated_color"]).next_to(seesaw.get_end(), DOWN)
        self.play(Write(beta1_label), Write(beta2_label))

        explanation = Text("The model only knows their combined effect is positive.", font_size=CONFIG["font_sizes"]["text"]).next_to(seesaw_group, UP, buff=0.5)
        self.play(Write(explanation))

        # Animate the unstable coefficients
        self.play(Rotate(seesaw, angle=0.2, about_point=seesaw.get_center()), run_time=1.5, rate_func=wiggle)
        
        # Show one possible (but weird) solution
        solution1_text = Text("Maybe: β₁ = +10, β₂ = -8", font_size=CONFIG["font_sizes"]["text"]).next_to(seesaw_group, DOWN, buff=1)
        self.play(Write(solution1_text))
        self.play(Rotate(seesaw, angle=-0.3, about_point=seesaw.get_center()), run_time=1)
        self.wait(1)

        # Show another possible solution
        solution2_text = Text("Or maybe: β₁ = -5, β₂ = +7", font_size=CONFIG["font_sizes"]["text"]).next_to(solution1_text, DOWN)
        self.play(ReplacementTransform(solution1_text, solution2_text))
        self.play(Rotate(seesaw, angle=0.2, about_point=seesaw.get_center()), run_time=1)
        self.wait(1)
        self.play(FadeOut(solution2_text))
        self.play(Rotate(seesaw, angle=-seesaw.get_angle(), about_point=seesaw.get_center()), run_time=0.5) # Reset angle

        # Key consequences
        consequences = VGroup(
            Text("Consequence 1: Unreliable Coefficients", color=CONFIG["colors"]["error_color"]),
            Text("The individual values of β₁ and β₂ are untrustworthy.", font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["secondary_text"]),
            Text("Consequence 2: Inflated Standard Errors", color=CONFIG["colors"]["error_color"]),
            Text("The model is very uncertain about the true values.", font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["secondary_text"])
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(seesaw_group, DOWN, buff=1)
        
        self.play(LaggedStart(*[Write(c) for c in consequences], lag_ratio=0.7))
        self.wait(4)
        
        self.play(FadeOut(VGroup(title, question, seesaw_group, beta1_label, beta2_label, explanation, consequences)))

    def show_summary(self):
        """Summarizes the key takeaways."""
        title = Text("Summary", font_size=CONFIG["font_sizes"]["title"]).to_edge(UP)
        self.play(Write(title))

        summary_points = VGroup(
            Text("Including highly correlated predictors (Multicollinearity) leads to:", font_size=CONFIG["font_sizes"]["text"]),
            VGroup(
                Dot(color=CONFIG["colors"]["error_color"]),
                Text("Unstable and unreliable coefficient estimates (β).", font_size=CONFIG["font_sizes"]["text"])
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Dot(color=CONFIG["colors"]["error_color"]),
                Text("Inflated standard errors, showing high uncertainty.", font_size=CONFIG["font_sizes"]["text"])
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Dot(color=CONFIG["colors"]["error_color"]),
                Text("Difficulty interpreting the individual effect of each variable.", font_size=CONFIG["font_sizes"]["text"])
            ).arrange(RIGHT, buff=0.2)
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT).next_to(title, DOWN, buff=1)

        self.play(LaggedStart(*[FadeIn(p, shift=UP) for p in summary_points], lag_ratio=0.7))
        self.wait(3)

        final_note = Text(
            "While the model's overall prediction might still be okay,\nthe interpretation of its parts becomes compromised.",
            font_size=CONFIG["font_sizes"]["text"],
            color=GREEN,
            t2c={"interpretation": CONFIG["colors"]["error_color"]}
        ).next_to(summary_points, DOWN, buff=1)
        self.play(Write(final_note))
        self.wait(4)
        self.play(FadeOut(VGroup(title, summary_points, final_note)))

    def _create_control_lever(self, label_text, color, position_x):
        """Helper to create a slider-like lever."""
        label = Text(label_text, font_size=CONFIG["font_sizes"]["label"], color=color)
        slider = ValueTracker(0)
        number_line = NumberLine(
            x_range=[-1, 1, 1],
            length=3,
            include_tip=False,
            label_direction=DOWN,
            stroke_width=3
        ).move_to(ORIGIN)
        handle = Dot(radius=0.1, color=color, fill_opacity=1).move_to(number_line.n2p(slider.get_value()))
        handle.add_updater(lambda m: m.move_to(number_line.n2p(slider.get_value())))

        # Create visual group without the tracker
        visual_group = VGroup(label, number_line, handle).arrange(DOWN, buff=0.3)
        visual_group.move_to(DOWN * 1.5 + LEFT * 3 * position_x)
        
        # Add the slider as an attribute so we can access it later
        visual_group.slider = slider
        return visual_group
