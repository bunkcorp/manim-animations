#!/usr/bin/env python3
"""
Boosting Hyperparameters Simple Animation
Simplified demonstration of eta and nrounds effects in boosting
"""

from manim import *
import numpy as np

class BoostingSimpleAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Show boosting concept
        self.show_boosting_concept()
        
        # Show eta effects
        self.show_eta_effects()
        
        # Show nrounds effects
        self.show_nrounds_effects()
        
        # Show practical guidelines
        self.show_guidelines()
    
    def show_boosting_concept(self):
        """Show basic boosting concept"""
        title = Text("Boosting: η (eta) & nrounds", 
                    font_size=32, color=YELLOW, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Show formula
        formula = Text("Prediction = η×Tree₁ + η×Tree₂ + η×Tree₃ + ...", 
                      font_size=20, color=WHITE)
        formula.move_to(UP*1.5)
        self.play(Write(formula))
        
        # Show key parameters
        eta_param = Text("η (eta) = Learning Rate", font_size=18, color=BLUE, weight=BOLD)
        eta_param.move_to(ORIGIN)
        
        rounds_param = Text("nrounds = Number of Trees", font_size=18, color=GREEN, weight=BOLD)
        rounds_param.move_to(DOWN*0.7)
        
        self.play(Write(eta_param), Write(rounds_param))
        
        # Show interaction
        interaction = Text("These parameters work together!", 
                         font_size=16, color=YELLOW, weight=BOLD)
        interaction.move_to(DOWN*1.5)
        self.play(Write(interaction))
        
        self.wait(2)
        self.play(FadeOut(formula, eta_param, rounds_param, interaction))
        self.title = title
    
    def show_eta_effects(self):
        """Show eta effects with simple comparison"""
        eta_title = Text("Learning Rate (η) Effects", 
                        font_size=28, color=BLUE, weight=BOLD)
        self.play(ReplacementTransform(self.title, eta_title))
        
        # Create three scenarios
        scenarios = [
            ("High η = 0.8", "Fast but unstable", RED, LEFT*4),
            ("Medium η = 0.1", "Balanced approach", ORANGE, ORIGIN),
            ("Low η = 0.01", "Slow but stable", GREEN, RIGHT*4)
        ]
        
        for eta_text, desc_text, color, position in scenarios:
            # Create panel
            panel = Rectangle(
                width=3, height=4,
                fill_color=BLACK, fill_opacity=0.8,
                stroke_color=color, stroke_width=2
            ).move_to(position + DOWN*0.5)
            
            eta_label = Text(eta_text, font_size=16, color=color, weight=BOLD)
            eta_label.move_to(position + UP*1.8)
            
            desc_label = Text(desc_text, font_size=12, color=WHITE)
            desc_label.move_to(position + UP*1.4)
            
            # Simple learning curve representation
            if "High" in eta_text:
                # Jagged, oscillating line
                curve_points = []
                for x in np.linspace(-1, 1, 20):
                    y = -0.5 * x + 0.3 * np.sin(8*x) - 0.2
                    curve_points.append(position + [x*1.2, y, 0])
                warning = Text("⚠️ Overfitting", font_size=10, color=RED, weight=BOLD)
                warning.move_to(position + DOWN*1.5)
            elif "Medium" in eta_text:
                # Smooth decreasing curve
                curve_points = []
                for x in np.linspace(-1, 1, 20):
                    y = -0.8 * x - 0.2
                    curve_points.append(position + [x*1.2, y*0.8, 0])
                warning = Text("✓ Good balance", font_size=10, color=GREEN, weight=BOLD)
                warning.move_to(position + DOWN*1.5)
            else:
                # Very gradual curve
                curve_points = []
                for x in np.linspace(-1, 1, 20):
                    y = -0.3 * x - 0.1
                    curve_points.append(position + [x*1.2, y*1.2, 0])
                warning = Text("Too slow", font_size=10, color=ORANGE, weight=BOLD)
                warning.move_to(position + DOWN*1.5)
            
            curve = VMobject()
            curve.set_points_smoothly(curve_points)
            curve.set_stroke(color, width=3)
            
            self.play(Create(panel), Write(eta_label), Write(desc_label))
            self.play(Create(curve), Write(warning))
        
        # Key message
        message = Text("Lower η = More stable learning", 
                      font_size=18, color=YELLOW, weight=BOLD)
        message.move_to(DOWN*3)
        self.play(Write(message))
        
        self.wait(3)
        self.play(FadeOut(*self.mobjects[1:]))  # Keep title
        self.eta_title = eta_title
    
    def show_nrounds_effects(self):
        """Show nrounds effects"""
        nrounds_title = Text("Number of Rounds Effects", 
                           font_size=28, color=PURPLE, weight=BOLD)
        self.play(ReplacementTransform(self.eta_title, nrounds_title))
        
        # Show progression
        progression_text = Text("More rounds → More complex model", 
                              font_size=20, color=WHITE, weight=BOLD)
        progression_text.move_to(UP*2)
        self.play(Write(progression_text))
        
        # Create learning curve
        axes = Axes(
            x_range=[0, 200, 50],
            y_range=[0, 2, 0.5],
            x_length=8,
            y_length=4,
            axis_config={"stroke_color": WHITE, "stroke_width": 2}
        ).move_to(DOWN*0.5)
        
        x_label = Text("Number of Rounds", font_size=14, color=WHITE)
        x_label.next_to(axes.x_axis, DOWN)
        
        y_label = Text("Error", font_size=14, color=WHITE)
        y_label.next_to(axes.y_axis, LEFT)
        y_label.rotate(PI/2)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Training curve (always decreasing)
        rounds = np.linspace(0, 200, 50)
        train_error = 1.8 * np.exp(-rounds/50) + 0.1
        train_points = [axes.coords_to_point(r, e) for r, e in zip(rounds, train_error)]
        
        train_curve = VMobject()
        train_curve.set_points_smoothly(train_points)
        train_curve.set_stroke(BLUE, width=3)
        
        # Validation curve (U-shape)
        val_error = 1.8 * np.exp(-rounds/40) + 0.008 * rounds + 0.2
        val_points = [axes.coords_to_point(r, e) for r, e in zip(rounds, val_error)]
        
        val_curve = VMobject()
        val_curve.set_points_smoothly(val_points)
        val_curve.set_stroke(RED, width=3)
        
        self.play(Create(train_curve), run_time=2)
        self.play(Create(val_curve), run_time=2)
        
        # Labels
        train_label = Text("Training", font_size=12, color=BLUE, weight=BOLD)
        train_label.move_to(axes.coords_to_point(150, 0.3))
        
        val_label = Text("Validation", font_size=12, color=RED, weight=BOLD)
        val_label.move_to(axes.coords_to_point(120, 1.5))
        
        self.play(Write(train_label), Write(val_label))
        
        # Optimal point
        optimal_rounds = 80
        optimal_error = 1.8 * np.exp(-optimal_rounds/40) + 0.008 * optimal_rounds + 0.2
        
        optimal_dot = Dot(axes.coords_to_point(optimal_rounds, optimal_error), 
                         color=GREEN, radius=0.08)
        optimal_text = Text("Optimal", font_size=12, color=GREEN, weight=BOLD)
        optimal_text.next_to(optimal_dot, UP)
        
        self.play(FadeIn(optimal_dot, scale=2), Write(optimal_text))
        
        # Overfitting warning
        overfitting_text = Text("Too many rounds → Overfitting", 
                              font_size=16, color=RED, weight=BOLD)
        overfitting_text.move_to(DOWN*3)
        self.play(Write(overfitting_text))
        
        self.wait(3)
        self.play(FadeOut(*self.mobjects[1:]))  # Keep title
        self.nrounds_title = nrounds_title
    
    def show_guidelines(self):
        """Show practical guidelines"""
        guidelines_title = Text("Practical Guidelines", 
                              font_size=32, color=YELLOW, weight=BOLD)
        self.play(ReplacementTransform(self.nrounds_title, guidelines_title))
        
        # Key insight
        key_insight = Text("Key Insight: η and nrounds work together!", 
                          font_size=24, color=YELLOW, weight=BOLD)
        key_insight.move_to(UP*2)
        self.play(Write(key_insight))
        
        # Guidelines
        guidelines = VGroup(
            Text("• Lower η → Use more rounds", font_size=18, color=WHITE),
            Text("• Higher η → Use fewer rounds", font_size=18, color=WHITE),
            Text("• Start with η = 0.1, nrounds = 100", font_size=18, color=GREEN),
            Text("• Use early stopping to prevent overfitting", font_size=18, color=BLUE),
            Text("• Cross-validate to find optimal values", font_size=18, color=ORANGE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        
        guidelines.move_to(ORIGIN)
        
        for guideline in guidelines:
            self.play(Write(guideline), run_time=1)
        
        # Warning
        warning = Text("⚠️ High η + Many rounds = Guaranteed overfitting!", 
                      font_size=18, color=RED, weight=BOLD)
        warning.move_to(DOWN*3)
        self.play(Write(warning))
        
        # Formula
        formula = Text("Prediction = Σ η × Treeᵢ", font_size=16, color=WHITE)
        formula.move_to(RIGHT*4 + UP*1)
        self.play(Write(formula))
        
        self.wait(4)

if __name__ == "__main__":
    # For testing
    pass