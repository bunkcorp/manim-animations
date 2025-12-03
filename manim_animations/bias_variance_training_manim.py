#!/usr/bin/env python3
"""
Bias-Variance Training Animation - Decreasing Complexity
Shows how bias, variance, and training error change as model complexity decreases
"""

from manim import *
import numpy as np

class BiasVarianceTrainingDecreasingComplexity(Scene):
    def construct(self):
        # Set background
        self.camera.background_color = "#1E1E1E"
        
        # Create axes
        axes = Axes(
            x_range=[0, 1, 0.2],
            y_range=[0, 1, 0.2], 
            x_length=10,
            y_length=5,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 24}
        ).to_edge(DOWN)

        # Labels
        x_label = Text("Model Complexity", font_size=20).next_to(axes, DOWN)
        y_label = Text("Magnitude", font_size=20).next_to(axes, LEFT).rotate(PI/2)

        # Title
        title = Text(
            "As complexity decreases: Bias ↑, Variance ↓, Training Error ↑",
            font_size=28,
            color=WHITE
        ).to_edge(UP)

        self.play(FadeIn(axes), Write(x_label), Write(y_label), FadeIn(title))
        self.wait(1)

        # Define functions
        # x in [0,1] where 0 = LOW complexity, 1 = HIGH complexity
        def bias_func(x):
            return 0.12 + 0.8 * np.exp(-2.0 * x)
        
        def var_func(x):
            return 0.10 + 0.75 * x**1.5
            
        def train_func(x):
            return 0.15 + 0.70 * (1 - x)**1.6

        # Create smooth curves
        x_vals = np.linspace(0.01, 0.99, 100)
        
        # Bias curve (decreases with complexity)
        bias_points = [axes.c2p(x, bias_func(x)) for x in x_vals]
        bias_graph = VMobject(color=YELLOW, stroke_width=6)
        bias_graph.set_points_smoothly(bias_points)
        
        # Variance curve (increases with complexity)
        var_points = [axes.c2p(x, var_func(x)) for x in x_vals]
        var_graph = VMobject(color=BLUE, stroke_width=6)
        var_graph.set_points_smoothly(var_points)
        
        # Training error curve (decreases with complexity)
        train_points = [axes.c2p(x, train_func(x)) for x in x_vals]
        train_graph = VMobject(color=RED, stroke_width=6)
        train_graph.set_points_smoothly(train_points)

        # Labels for curves
        bias_lab = Text("Bias", color=YELLOW, font_size=18).next_to(axes.c2p(0.25, bias_func(0.25)), UP, buff=0.3)
        var_lab = Text("Variance", color=BLUE, font_size=18).next_to(axes.c2p(0.8, var_func(0.8)), UP, buff=0.3)
        train_lab = Text("Training Error", color=RED, font_size=18).next_to(axes.c2p(0.2, train_func(0.2)), DOWN, buff=0.3)

        self.play(
            Create(bias_graph),
            Create(var_graph),
            Create(train_graph),
            FadeIn(bias_lab),
            FadeIn(var_lab),
            FadeIn(train_lab),
        )
        self.wait(1)

        # Complexity tracker - start at high complexity (right side)
        complexity = ValueTracker(0.9)

        # Vertical marker line
        def get_marker_line():
            return axes.get_vertical_line(
                axes.c2p(complexity.get_value(), 1), 
                color=GRAY,
                stroke_width=4
            )
        
        def get_marker_triangle():
            return Triangle(
                fill_opacity=1,
                fill_color=GRAY,
                stroke_width=0
            ).scale(0.1).next_to(axes.c2p(complexity.get_value(), 0), DOWN)

        marker_line = always_redraw(get_marker_line)
        marker_triangle = always_redraw(get_marker_triangle)

        # Dots on curves
        bias_dot = always_redraw(
            lambda: Dot(
                axes.c2p(complexity.get_value(), bias_func(complexity.get_value())),
                color=YELLOW,
                radius=0.08
            )
        )
        var_dot = always_redraw(
            lambda: Dot(
                axes.c2p(complexity.get_value(), var_func(complexity.get_value())),
                color=BLUE,
                radius=0.08
            )
        )
        train_dot = always_redraw(
            lambda: Dot(
                axes.c2p(complexity.get_value(), train_func(complexity.get_value())),
                color=RED,
                radius=0.08
            )
        )

        # Live readouts box
        readout_box = RoundedRectangle(
            corner_radius=0.15,
            width=4.5,
            height=2.2,
            stroke_color=GRAY,
            fill_color="#2E2E2E",
            fill_opacity=0.8
        ).to_corner(UR, buff=0.6)

        def format_percent(x):
            return f"{100*x:.0f}%"

        # Live updating text
        bias_readout = always_redraw(
            lambda: Text(
                f"Bias: {format_percent(bias_func(complexity.get_value()))}",
                color=YELLOW,
                font_size=18
            ).next_to(readout_box.get_top(), DOWN, buff=0.3).align_to(readout_box, LEFT).shift(RIGHT*0.3)
        )
        
        var_readout = always_redraw(
            lambda: Text(
                f"Variance: {format_percent(var_func(complexity.get_value()))}",
                color=BLUE,
                font_size=18
            ).next_to(bias_readout, DOWN, aligned_edge=LEFT, buff=0.25)
        )
        
        train_readout = always_redraw(
            lambda: Text(
                f"Training Error: {format_percent(train_func(complexity.get_value()))}",
                color=RED,
                font_size=18
            ).next_to(var_readout, DOWN, aligned_edge=LEFT, buff=0.25)
        )

        readout_title = Text("Current Level", color=WHITE, font_size=16).next_to(readout_box, UP, buff=0.1)

        # Add all tracking elements
        self.play(FadeIn(marker_line), FadeIn(marker_triangle))
        self.play(FadeIn(bias_dot), FadeIn(var_dot), FadeIn(train_dot))
        self.play(
            DrawBorderThenFill(readout_box), 
            FadeIn(readout_title),
            FadeIn(bias_readout), 
            FadeIn(var_readout), 
            FadeIn(train_readout)
        )
        self.wait(1)

        # Decreasing complexity arrow
        arrow = Arrow(
            start=axes.c2p(0.95, 1.05),
            end=axes.c2p(0.05, 1.05),
            color=WHITE,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.08
        )
        arrow_text = Text("Decreasing Complexity", font_size=18).next_to(arrow, UP, buff=0.15)

        self.play(GrowArrow(arrow), Write(arrow_text))
        self.wait(1)

        # Animate complexity decrease (high → low)
        self.play(
            complexity.animate.set_value(0.1), 
            run_time=6, 
            rate_func=rate_functions.ease_in_out_cubic
        )
        self.wait(1)

        # Show directional changes with braces
        # Bias increases (↑)
        bias_start_y = bias_func(0.9)
        bias_end_y = bias_func(0.1)
        bias_brace = Brace(
            Line(axes.c2p(0.05, bias_start_y), axes.c2p(0.05, bias_end_y)),
            direction=LEFT,
            color=YELLOW
        )
        bias_arrow_text = Text("↑ Bias", color=YELLOW, font_size=20).next_to(bias_brace, LEFT, buff=0.2)

        # Variance decreases (↓)
        var_start_y = var_func(0.9)
        var_end_y = var_func(0.1)
        var_brace = Brace(
            Line(axes.c2p(0.05, var_start_y), axes.c2p(0.05, var_end_y)),
            direction=RIGHT,
            color=BLUE
        )
        var_arrow_text = Text("↓ Variance", color=BLUE, font_size=20).next_to(var_brace, RIGHT, buff=0.2)

        # Training error increases (↑)
        train_start_y = train_func(0.9)
        train_end_y = train_func(0.1)
        train_brace = Brace(
            Line(axes.c2p(0.95, train_start_y), axes.c2p(0.95, train_end_y)),
            direction=LEFT,
            color=RED
        )
        train_arrow_text = Text("↑ Training Error", color=RED, font_size=20).next_to(train_brace, LEFT, buff=0.2)

        self.play(GrowFromCenter(bias_brace), FadeIn(bias_arrow_text))
        self.wait(0.5)
        self.play(GrowFromCenter(var_brace), FadeIn(var_arrow_text))
        self.wait(0.5)
        self.play(GrowFromCenter(train_brace), FadeIn(train_arrow_text))
        self.wait(2)

        # Optional: sweep back and forth
        self.play(
            complexity.animate.set_value(0.8), 
            run_time=2, 
            rate_func=there_and_back_with_pause
        )
        self.wait(1)

        # Clean up braces
        self.play(
            FadeOut(bias_brace, var_brace, train_brace), 
            FadeOut(bias_arrow_text, var_arrow_text, train_arrow_text)
        )
        self.wait(0.5)

        # Final summary
        summary = VGroup(
            Text("As complexity decreases:", font_size=28, color=WHITE),
            Text("• Bias increases", color=YELLOW, font_size=24),
            Text("• Variance decreases", color=BLUE, font_size=24), 
            Text("• Training error increases", color=RED, font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_corner(UL, buff=0.8)

        self.play(Write(summary[0]))
        for item in summary[1:]:
            self.play(Write(item))
            self.wait(0.3)
        
        self.wait(3)
        
        # Final message
        final_msg = Text(
            "Understanding these relationships helps optimize model complexity!",
            font_size=20,
            color=LIGHT_GRAY
        ).next_to(summary, DOWN, buff=0.5)
        
        self.play(Write(final_msg))
        self.wait(2)