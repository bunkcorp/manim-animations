#!/usr/bin/env python3
"""
Bias-Variance Tradeoff Manim Animation
Shows how bias, variance, and model complexity interact
"""

from manim import *
import numpy as np

class BiasVarianceAnimation(Scene):
    """
    A comprehensive Manim animation explaining bias-variance tradeoff
    """
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Show intro
        self.show_intro()
        
        # Show the mathematical foundation
        self.show_mathematical_foundation()
        
        # Show interactive bias-variance visualization
        self.show_bias_variance_visualization()
        
        # Show model complexity effects
        self.show_complexity_effects()
        
        # Show summary
        self.show_summary()
    
    def show_intro(self):
        """Introduction to bias-variance tradeoff"""
        title = Text("Bias-Variance Tradeoff", font_size=48, color=YELLOW).to_edge(UP)
        subtitle = Text("Understanding Model Complexity", font_size=32, color=WHITE).next_to(title, DOWN)
        
        self.play(Write(title), Write(subtitle))
        self.wait(2)
        
        # Problem description
        problem_text = VGroup(
            Text("Question: As model complexity decreases:", font_size=24, color=LIGHT_GRAY),
            Text("• What happens to bias?", font_size=20, color=BLUE).shift(LEFT * 2),
            Text("• What happens to variance?", font_size=20, color=RED).shift(LEFT * 2),
            Text("• What happens to training error?", font_size=20, color=GREEN).shift(LEFT * 2)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(subtitle, DOWN, buff=1)
        
        self.play(FadeIn(problem_text, shift=UP))
        self.wait(3)
        self.play(FadeOut(title, subtitle, problem_text))
    
    def show_mathematical_foundation(self):
        """Show the mathematical decomposition"""
        title = Text("Mathematical Foundation", font_size=36, color=YELLOW).to_edge(UP)
        self.play(Write(title))
        
        # Main formula
        formula = MathTex(
            r"\text{Expected Test Error} = \text{Bias}^2 + \text{Variance} + \text{Irreducible Error}",
            font_size=28
        ).next_to(title, DOWN, buff=0.8)
        
        self.play(Write(formula))
        self.wait(1)
        
        # Detailed breakdown
        bias_def = VGroup(
            Text("Bias² =", font_size=24, color=BLUE),
            MathTex(r"[\mathbb{E}[\hat{f}(x)] - f(x)]^2", font_size=20),
            Text("(Systematic error)", font_size=18, color=LIGHT_GRAY)
        ).arrange(RIGHT, buff=0.2).next_to(formula, DOWN, buff=0.8)
        
        variance_def = VGroup(
            Text("Variance =", font_size=24, color=RED),
            MathTex(r"\mathbb{E}[(\hat{f}(x) - \mathbb{E}[\hat{f}(x)])^2]", font_size=20),
            Text("(Prediction variability)", font_size=18, color=LIGHT_GRAY)
        ).arrange(RIGHT, buff=0.2).next_to(bias_def, DOWN, buff=0.3)
        
        noise_def = VGroup(
            Text("Irreducible =", font_size=24, color=ORANGE),
            MathTex(r"\sigma^2", font_size=20),
            Text("(Inherent noise)", font_size=18, color=LIGHT_GRAY)
        ).arrange(RIGHT, buff=0.2).next_to(variance_def, DOWN, buff=0.3)
        
        self.play(FadeIn(bias_def), FadeIn(variance_def), FadeIn(noise_def))
        self.wait(3)
        self.play(FadeOut(title, formula, bias_def, variance_def, noise_def))
    
    def show_bias_variance_visualization(self):
        """Interactive visualization of bias-variance with bulls-eye targets"""
        title = Text("Bias-Variance Visualization", font_size=36, color=YELLOW).to_edge(UP)
        self.play(Write(title))
        
        # Create four quadrants
        scenarios = [
            {"pos": UP * 1.5 + LEFT * 3, "title": "Low Bias, Low Variance", "color": GREEN, "bias": "low", "var": "low"},
            {"pos": UP * 1.5 + RIGHT * 3, "title": "Low Bias, High Variance", "color": ORANGE, "bias": "low", "var": "high"},
            {"pos": DOWN * 1.5 + LEFT * 3, "title": "High Bias, Low Variance", "color": BLUE, "bias": "high", "var": "low"},
            {"pos": DOWN * 1.5 + RIGHT * 3, "title": "High Bias, High Variance", "color": RED, "bias": "high", "var": "high"}
        ]
        
        for scenario in scenarios:
            # Create bulls-eye target
            target = VGroup(
                Circle(radius=1, color=WHITE, stroke_width=2),
                Circle(radius=0.7, color=WHITE, stroke_width=2),
                Circle(radius=0.4, color=WHITE, stroke_width=2),
                Dot(radius=0.05, color=YELLOW)  # True center
            ).move_to(scenario["pos"])
            
            # Create prediction points based on bias/variance
            points = self.create_prediction_points(scenario["bias"], scenario["var"])
            points.move_to(scenario["pos"])
            
            # Title
            scenario_title = Text(scenario["title"], font_size=16, color=scenario["color"]).next_to(target, UP, buff=0.2)
            
            self.play(Create(target), Create(points), Write(scenario_title))
        
        self.wait(4)
        
        # Add explanations
        explanation = VGroup(
            Text("🎯 Green: Ideal (accurate & precise)", font_size=20, color=GREEN),
            Text("🟠 Orange: High variance (imprecise)", font_size=20, color=ORANGE),  
            Text("🔵 Blue: High bias (inaccurate)", font_size=20, color=BLUE),
            Text("🔴 Red: Worst case (inaccurate & imprecise)", font_size=20, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(title, DOWN, buff=0.5).shift(DOWN * 2.5)
        
        self.play(FadeIn(explanation))
        self.wait(3)
        self.play(FadeOut(*self.mobjects))
    
    def create_prediction_points(self, bias_level, var_level):
        """Create prediction points for bulls-eye visualization"""
        np.random.seed(42)
        
        # Center offset based on bias
        if bias_level == "high":
            center_x, center_y = 0.5, 0.3
        else:
            center_x, center_y = 0, 0
        
        # Spread based on variance
        if var_level == "high":
            spread = 0.4
        else:
            spread = 0.15
        
        # Generate points
        points = VGroup()
        for _ in range(12):
            x = center_x + np.random.normal(0, spread)
            y = center_y + np.random.normal(0, spread)
            point = Dot(radius=0.03, color=BLUE).move_to([x, y, 0])
            points.add(point)
        
        return points
    
    def show_complexity_effects(self):
        """Show how complexity affects bias, variance, and training error"""
        title = Text("Model Complexity Effects", font_size=36, color=YELLOW).to_edge(UP)
        self.play(Write(title))
        
        # Create axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 1, 0.2],
            x_length=8,
            y_length=5,
            axis_config={"color": GRAY}
        ).shift(DOWN * 0.5)
        
        x_label = Text("Model Complexity", font_size=18).next_to(axes, DOWN)
        y_label = Text("Error", font_size=18).next_to(axes, LEFT).rotate(PI/2)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Define curves
        x_vals = np.linspace(0, 10, 100)
        
        # Bias curve (decreasing)
        bias_vals = 0.8 * np.exp(-x_vals/3) + 0.1
        bias_curve = axes.plot_line_graph(
            x_vals, bias_vals, 
            line_color=BLUE, 
            stroke_width=4
        )
        
        # Variance curve (increasing)  
        variance_vals = 0.1 + 0.6 * (x_vals/10)**2
        variance_curve = axes.plot_line_graph(
            x_vals, variance_vals,
            line_color=RED,
            stroke_width=4
        )
        
        # Total error (U-shaped)
        total_vals = bias_vals + variance_vals + 0.1  # Add irreducible error
        total_curve = axes.plot_line_graph(
            x_vals, total_vals,
            line_color=YELLOW,
            stroke_width=4
        )
        
        # Training error (decreasing)
        train_vals = 0.7 * np.exp(-x_vals/2) + 0.05
        train_curve = axes.plot_line_graph(
            x_vals, train_vals,
            line_color=GREEN,
            stroke_width=4
        )
        
        # Animate curves
        self.play(Create(bias_curve))
        bias_label = Text("Bias²", font_size=16, color=BLUE).next_to(axes.c2p(2, bias_vals[20]), UR)
        self.play(Write(bias_label))
        
        self.wait(0.5)
        
        self.play(Create(variance_curve))
        var_label = Text("Variance", font_size=16, color=RED).next_to(axes.c2p(8, variance_vals[80]), UL)
        self.play(Write(var_label))
        
        self.wait(0.5)
        
        self.play(Create(total_curve))
        total_label = Text("Total Error", font_size=16, color=YELLOW).next_to(axes.c2p(5, total_vals[50]), UP)
        self.play(Write(total_label))
        
        self.wait(0.5)
        
        self.play(Create(train_curve))
        train_label = Text("Training Error", font_size=16, color=GREEN).next_to(axes.c2p(1, train_vals[10]), UR)
        self.play(Write(train_label))
        
        # Mark optimal complexity
        optimal_idx = np.argmin(total_vals)
        optimal_x = x_vals[optimal_idx]
        optimal_dot = Dot(axes.c2p(optimal_x, total_vals[optimal_idx]), color=WHITE, radius=0.08)
        optimal_label = Text("Optimal\nComplexity", font_size=14, color=WHITE).next_to(optimal_dot, DOWN)
        
        self.play(FadeIn(optimal_dot), Write(optimal_label))
        
        # Add arrows showing trends
        complexity_arrow = Arrow(
            axes.c2p(8, 0.1), axes.c2p(2, 0.1), 
            color=WHITE, stroke_width=3
        )
        complexity_text = Text("Decreasing Complexity", font_size=14, color=WHITE).next_to(complexity_arrow, DOWN)
        
        self.play(GrowArrow(complexity_arrow), Write(complexity_text))
        
        self.wait(4)
        self.play(FadeOut(*self.mobjects))
    
    def show_summary(self):
        """Final summary of key insights"""
        title = Text("Key Insights", font_size=42, color=YELLOW).to_edge(UP)
        self.play(Write(title))
        
        insights = VGroup(
            VGroup(
                Text("📈", font_size=32),
                Text("As complexity decreases:", font_size=24, color=WHITE),
                Text("Bias INCREASES", font_size=20, color=BLUE)
            ).arrange(RIGHT, buff=0.3),
            
            VGroup(
                Text("📉", font_size=32),
                Text("As complexity decreases:", font_size=24, color=WHITE),
                Text("Variance DECREASES", font_size=20, color=RED)
            ).arrange(RIGHT, buff=0.3),
            
            VGroup(
                Text("🎯", font_size=32),
                Text("As complexity decreases:", font_size=24, color=WHITE),
                Text("Training Error INCREASES", font_size=20, color=GREEN)
            ).arrange(RIGHT, buff=0.3),
            
            VGroup(
                Text("⚖️", font_size=32),
                Text("Optimal complexity:", font_size=24, color=WHITE),
                Text("Minimizes total error", font_size=20, color=YELLOW)
            ).arrange(RIGHT, buff=0.3)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(title, DOWN, buff=1)
        
        for insight in insights:
            self.play(FadeIn(insight, shift=UP))
            self.wait(0.8)
        
        self.wait(2)
        
        # Final formula reminder
        final_formula = MathTex(
            r"\text{Total Error} = \text{Bias}^2 + \text{Variance} + \text{Noise}",
            font_size=32, color=YELLOW
        ).next_to(insights, DOWN, buff=1)
        
        self.play(Write(final_formula))
        self.wait(3)
        
        # Thank you message
        thanks = Text("Understanding Bias-Variance Tradeoff", font_size=28, color=WHITE).next_to(final_formula, DOWN, buff=1)
        self.play(Write(thanks))
        self.wait(2)