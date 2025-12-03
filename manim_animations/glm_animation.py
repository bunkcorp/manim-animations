from manim import *
import numpy as np
from scipy.special import expit # Sigmoid function

class GLMAnimation(Scene):
    def construct(self):
        self.next_section("Introduction")
        title = Text("Generalized Linear Models (GLM) Animation").to_edge(UP)
        subtitle = Text("Focus: The Link Function (Logistic Regression)").next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        self.wait(1)

        # Create Axes
        axes = Axes(
            x_range=[-2, 12, 1],
            y_range=[-0.1, 1.1, 0.2],
            x_length=10,
            y_length=6,
            axis_config={
                "color": GRAY,
                "include_numbers": True,
                "font_size": 24,
            },
            y_axis_config={
                "numbers_to_include": [0, 0.5, 1],
                "decimal_number_config": {"num_decimal_places": 1},
            }
        ).to_edge(DOWN).shift(UP*0.5)

        x_label = axes.get_x_axis_label("Feature (X)")
        y_label = axes.get_y_axis_label("Outcome (Y)")

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(0.5)

        # Generate Data Points
        np.random.seed(0)
        x_data = np.random.uniform(0, 10, 50)
        # Simulate a logistic relationship
        linear_predictor_true = -5 + 1 * x_data
        probabilities_true = expit(linear_predictor_true)
        y_data = (np.random.rand(50) < probabilities_true).astype(int)

        points_group = VGroup()
        for i in range(len(x_data)):
            color = GREEN if y_data[i] == 1 else RED
            dot = Dot(axes.coords_to_point(x_data[i], y_data[i]), color=color)
            points_group.add(dot)
        
        self.play(FadeIn(points_group))
        self.wait(1)

        # Linear Predictor
        self.next_section("LinearPredictor")
        linear_text = Text("1. Linear Predictor (X * Beta)").to_edge(UP).shift(DOWN*0.5)
        self.play(FadeOut(title), FadeOut(subtitle), Write(linear_text))

        # A simple linear line (e.g., y = 0.1x + 0.2)
        linear_function = lambda x: 0.1 * x + 0.2
        linear_graph = axes.plot(linear_function, color=BLUE)
        linear_label = axes.get_graph_label(linear_graph, label="Linear Predictor")

        self.play(Create(linear_graph), Write(linear_label))
        self.wait(1)

        # Link Function (Sigmoid)
        self.next_section("LinkFunction")
        link_text = Text("2. Link Function (Sigmoid)").next_to(linear_text, DOWN)
        self.play(FadeOut(linear_text), Write(link_text))

        # Sigmoid function applied to the linear predictor
        # We'll use the same linear function for demonstration
        sigmoid_function = lambda x: expit(0.5 * x - 2.5) # Adjusted to fit the axes range better
        sigmoid_graph = axes.plot(sigmoid_function, color=PURPLE)
        sigmoid_label = axes.get_graph_label(sigmoid_graph, label="Probabilities (Sigmoid)", x_val=8)

        self.play(Transform(linear_graph, sigmoid_graph), Transform(linear_label, sigmoid_label))
        self.wait(1)

        # Explanation
        self.next_section("Explanation")
        explanation_text = Text(
            "The link function transforms the linear predictor\n"
            "into the expected value of the response variable.\n"
            "For logistic regression, it maps to probabilities (0-1)."
        ).scale(0.7).to_edge(UP).shift(DOWN*1.5)

        self.play(FadeOut(link_text), Write(explanation_text))
        self.wait(3)

        self.next_section("Conclusion")
        final_text = Text("GLM Link Function Demonstrated").to_edge(UP)
        self.play(FadeOut(explanation_text), FadeOut(linear_graph), FadeOut(linear_label), FadeOut(points_group), FadeOut(axes), FadeOut(x_label), FadeOut(y_label), Write(final_text))
        self.wait(2)
