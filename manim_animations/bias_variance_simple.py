#!/usr/bin/env python3
"""
Simple Bias-Variance Tradeoff Manim Animation (No LaTeX)
Shows how bias, variance, and model complexity interact
"""

from manim import *
import numpy as np

class SimpleBiasVarianceAnimation(Scene):
    """
    A simple Manim animation explaining bias-variance tradeoff without LaTeX
    """
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Show intro
        self.show_intro()
        
        # Show the foundation
        self.show_foundation()
        
        # Show complexity effects  
        self.show_complexity_effects()
        
        # Show summary
        self.show_summary()
    
    def show_intro(self):
        """Introduction to bias-variance tradeoff"""
        title = Text("Bias-Variance Tradeoff", font_size=48, color=YELLOW).to_edge(UP)
        subtitle = Text("Model Complexity Effects", font_size=32, color=WHITE).next_to(title, DOWN)
        
        self.play(Write(title), Write(subtitle))
        self.wait(2)
        
        # Question
        question = VGroup(
            Text("As Model Complexity DECREASES:", font_size=28, color=LIGHT_GRAY),
            Text("• Bias?", font_size=24, color=BLUE).shift(LEFT * 2),
            Text("• Variance?", font_size=24, color=RED).shift(LEFT * 2), 
            Text("• Training Error?", font_size=24, color=GREEN).shift(LEFT * 2)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(subtitle, DOWN, buff=1)
        
        self.play(FadeIn(question, shift=UP))
        self.wait(3)
        self.play(FadeOut(title, subtitle, question))
    
    def show_foundation(self):
        """Show the basic concepts"""
        title = Text("Key Concepts", font_size=36, color=YELLOW).to_edge(UP)
        self.play(Write(title))
        
        # Error decomposition in text
        formula = Text("Total Error = Bias² + Variance + Noise", font_size=32, color=WHITE).next_to(title, DOWN, buff=0.8)
        self.play(Write(formula))
        
        # Definitions
        definitions = VGroup(
            VGroup(
                Text("Bias²:", font_size=24, color=BLUE),
                Text("How far predictions are from truth", font_size=18, color=LIGHT_GRAY)
            ).arrange(RIGHT, buff=0.3),
            
            VGroup(
                Text("Variance:", font_size=24, color=RED),
                Text("How much predictions vary", font_size=18, color=LIGHT_GRAY)
            ).arrange(RIGHT, buff=0.3),
            
            VGroup(
                Text("Training Error:", font_size=24, color=GREEN),
                Text("Error on training data", font_size=18, color=LIGHT_GRAY)
            ).arrange(RIGHT, buff=0.3)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(formula, DOWN, buff=1)
        
        for definition in definitions:
            self.play(FadeIn(definition))
            self.wait(0.5)
        
        self.wait(2)
        self.play(FadeOut(title, formula, definitions))
    
    def show_complexity_effects(self):
        """Show how complexity affects each component"""
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
        
        # Create curves with smooth parametric functions
        x_vals = np.linspace(0.5, 9.5, 50)
        
        # Bias curve (decreasing exponential)
        bias_vals = 0.7 * np.exp(-x_vals/3) + 0.15
        bias_points = [axes.c2p(x, y) for x, y in zip(x_vals, bias_vals)]
        bias_curve = VMobject(color=BLUE, stroke_width=4)
        bias_curve.set_points_smoothly(bias_points)
        
        # Variance curve (increasing quadratic)  
        variance_vals = 0.05 + 0.08 * (x_vals - 0.5)**1.5
        variance_points = [axes.c2p(x, y) for x, y in zip(x_vals, variance_vals)]
        variance_curve = VMobject(color=RED, stroke_width=4)
        variance_curve.set_points_smoothly(variance_points)
        
        # Training error (decreasing exponential)
        train_vals = 0.6 * np.exp(-x_vals/2.5) + 0.08
        train_points = [axes.c2p(x, y) for x, y in zip(x_vals, train_vals)]
        train_curve = VMobject(color=GREEN, stroke_width=4)
        train_curve.set_points_smoothly(train_points)
        
        # Total error (U-shaped)
        total_vals = bias_vals + variance_vals + 0.1
        total_points = [axes.c2p(x, y) for x, y in zip(x_vals, total_vals)]
        total_curve = VMobject(color=YELLOW, stroke_width=4)
        total_curve.set_points_smoothly(total_points)
        
        # Animate curves one by one
        self.play(Create(bias_curve))
        bias_label = Text("Bias²", font_size=18, color=BLUE).move_to(axes.c2p(2, 0.45))
        self.play(Write(bias_label))
        self.wait(1)
        
        self.play(Create(variance_curve)) 
        var_label = Text("Variance", font_size=18, color=RED).move_to(axes.c2p(8, 0.6))
        self.play(Write(var_label))
        self.wait(1)
        
        self.play(Create(train_curve))
        train_label = Text("Training Error", font_size=18, color=GREEN).move_to(axes.c2p(1.5, 0.25))
        self.play(Write(train_label))
        self.wait(1)
        
        self.play(Create(total_curve))
        total_label = Text("Total Error", font_size=18, color=YELLOW).move_to(axes.c2p(5, 0.8))
        self.play(Write(total_label))
        
        # Mark optimal point
        optimal_idx = np.argmin(total_vals)
        optimal_x = x_vals[optimal_idx]
        optimal_y = total_vals[optimal_idx]
        optimal_dot = Dot(axes.c2p(optimal_x, optimal_y), color=WHITE, radius=0.1)
        optimal_label = Text("Optimal", font_size=16, color=WHITE).next_to(optimal_dot, UP)
        
        self.play(FadeIn(optimal_dot), Write(optimal_label))
        
        # Add complexity arrow
        arrow = Arrow(
            axes.c2p(8.5, 0.15), axes.c2p(1.5, 0.15),
            color=WHITE, stroke_width=3
        )
        arrow_label = Text("Decreasing Complexity", font_size=16, color=WHITE).next_to(arrow, DOWN)
        
        self.play(GrowArrow(arrow), Write(arrow_label))
        
        self.wait(4)
        self.play(FadeOut(*self.mobjects))
    
    def show_summary(self):
        """Show the key takeaways"""
        title = Text("Key Takeaways", font_size=42, color=YELLOW).to_edge(UP)
        self.play(Write(title))
        
        # Main insights
        insights = VGroup(
            VGroup(
                Text("📈", font_size=36),
                Text("Bias INCREASES", font_size=28, color=BLUE),
                Text("as complexity decreases", font_size=20, color=LIGHT_GRAY)
            ).arrange(RIGHT, buff=0.3),
            
            VGroup(
                Text("📉", font_size=36), 
                Text("Variance DECREASES", font_size=28, color=RED),
                Text("as complexity decreases", font_size=20, color=LIGHT_GRAY)
            ).arrange(RIGHT, buff=0.3),
            
            VGroup(
                Text("🎯", font_size=36),
                Text("Training Error INCREASES", font_size=28, color=GREEN), 
                Text("as complexity decreases", font_size=20, color=LIGHT_GRAY)
            ).arrange(RIGHT, buff=0.3),
            
            VGroup(
                Text("⚖️", font_size=36),
                Text("Find the sweet spot!", font_size=28, color=YELLOW),
                Text("Balance bias and variance", font_size=20, color=LIGHT_GRAY)
            ).arrange(RIGHT, buff=0.3)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).next_to(title, DOWN, buff=1)
        
        # Animate each insight
        for i, insight in enumerate(insights):
            self.play(FadeIn(insight, shift=UP))
            self.wait(1)
        
        self.wait(2)
        
        # Final message
        final_msg = Text("Understanding helps you choose the right model complexity!", 
                        font_size=24, color=WHITE).next_to(insights, DOWN, buff=1)
        self.play(Write(final_msg))
        self.wait(3)