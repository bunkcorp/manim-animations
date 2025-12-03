#!/usr/bin/env python3
"""
Lambda Regularization Animation
Visual demonstration of how λ controls regularized regression
Focus on movement and visual effects
"""

from manim import *
import numpy as np

class LambdaRegularizationAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Show coefficient shrinkage
        self.show_coefficient_shrinkage()
        
        # Show bias-variance tradeoff
        self.show_bias_variance_tradeoff()
        
        # Show feature selection
        self.show_feature_selection()
        
        # Show CV tuning
        self.show_cv_tuning()
        
        # Show final comparison
        self.show_final_comparison()
    
    def show_coefficient_shrinkage(self):
        """Show how lambda shrinks coefficients"""
        title = Text("λ Controls Coefficient Shrinkage", font_size=32, color=YELLOW, weight=BOLD).to_edge(UP)
        self.play(Write(title))
        
        # Create coefficient bars for different features
        feature_names = ["Feature 1", "Feature 2", "Feature 3", "Feature 4", "Feature 5"]
        original_coeffs = [2.5, -1.8, 3.2, -0.9, 1.6]  # Original coefficients
        
        # Create bars
        bars = VGroup()
        labels = VGroup()
        
        for i, (name, coeff) in enumerate(zip(feature_names, original_coeffs)):
            # Bar
            bar = Rectangle(
                width=0.8,
                height=abs(coeff),
                fill_color=BLUE if coeff > 0 else RED,
                fill_opacity=0.8,
                stroke_color=WHITE,
                stroke_width=2
            )
            bar.move_to(LEFT*4 + RIGHT*i*1.8 + UP*0.5)
            if coeff < 0:
                bar.shift(DOWN*abs(coeff)/2)
            else:
                bar.shift(UP*coeff/2)
            
            # Label
            label = Text(f"{name}\n{coeff:.1f}", font_size=12, color=WHITE)
            label.next_to(bar, DOWN, buff=0.3)
            
            bars.add(bar)
            labels.add(label)
        
        # Show original coefficients
        self.play(*[GrowFromEdge(bar, DOWN) for bar in bars])
        self.play(*[Write(label) for label in labels])
        
        # Lambda slider
        lambda_slider = Rectangle(width=8, height=0.3, stroke_color=WHITE, fill_color=GRAY, fill_opacity=0.5)
        lambda_slider.move_to(DOWN*2.5)
        
        lambda_knob = Circle(radius=0.2, fill_color=ORANGE, fill_opacity=1, stroke_color=WHITE)
        lambda_knob.move_to(lambda_slider.get_left() + RIGHT*0.5)
        
        lambda_text = Text("λ = 0.0", font_size=18, color=ORANGE, weight=BOLD)
        lambda_text.next_to(lambda_slider, DOWN, buff=0.3)
        
        self.play(Create(lambda_slider), FadeIn(lambda_knob), Write(lambda_text))
        
        # Show shrinkage as lambda increases
        lambda_values = [0.0, 0.5, 1.0, 2.0, 5.0]
        
        for lambda_val in lambda_values[1:]:
            # Move slider knob
            new_knob_pos = lambda_slider.get_left() + RIGHT*(lambda_val/5.0 * 7 + 0.5)
            
            # Calculate shrunk coefficients
            shrunk_coeffs = [coeff/(1 + lambda_val) for coeff in original_coeffs]
            
            # Create new bars
            new_bars = VGroup()
            new_labels = VGroup()
            
            for i, (name, orig_coeff, shrunk_coeff) in enumerate(zip(feature_names, original_coeffs, shrunk_coeffs)):
                new_bar = Rectangle(
                    width=0.8,
                    height=abs(shrunk_coeff),
                    fill_color=BLUE if shrunk_coeff > 0 else RED,
                    fill_opacity=0.8,
                    stroke_color=WHITE,
                    stroke_width=2
                )
                new_bar.move_to(LEFT*4 + RIGHT*i*1.8 + UP*0.5)
                if shrunk_coeff < 0:
                    new_bar.shift(DOWN*abs(shrunk_coeff)/2)
                else:
                    new_bar.shift(UP*shrunk_coeff/2)
                
                new_label = Text(f"{name}\n{shrunk_coeff:.1f}", font_size=12, color=WHITE)
                new_label.next_to(new_bar, DOWN, buff=0.3)
                
                new_bars.add(new_bar)
                new_labels.add(new_label)
            
            # Update lambda text
            new_lambda_text = Text(f"λ = {lambda_val:.1f}", font_size=18, color=ORANGE, weight=BOLD)
            new_lambda_text.next_to(lambda_slider, DOWN, buff=0.3)
            
            # Animate changes
            self.play(
                lambda_knob.animate.move_to(new_knob_pos),
                ReplacementTransform(lambda_text, new_lambda_text),
                *[Transform(bars[i], new_bars[i]) for i in range(len(bars))],
                *[Transform(labels[i], new_labels[i]) for i in range(len(labels))],
                run_time=1
            )
            
            lambda_text = new_lambda_text
            self.wait(0.5)
        
        # Add shrinkage arrows
        shrinkage_arrows = VGroup()
        for i in range(len(bars)):
            arrow = Arrow(
                bars[i].get_top() + UP*0.3,
                bars[i].get_center(),
                color=YELLOW,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.3
            )
            shrinkage_arrows.add(arrow)
        
        shrinkage_text = Text("Shrinkage!", font_size=20, color=YELLOW, weight=BOLD)
        shrinkage_text.next_to(shrinkage_arrows, UP, buff=0.5)
        
        self.play(*[GrowArrow(arrow) for arrow in shrinkage_arrows], Write(shrinkage_text))
        
        self.wait(2)
        self.play(FadeOut(VGroup(
            bars, labels, lambda_slider, lambda_knob, lambda_text, 
            shrinkage_arrows, shrinkage_text
        )))
        self.shrinkage_title = title
    
    def show_bias_variance_tradeoff(self):
        """Show bias-variance tradeoff with lambda"""
        tradeoff_title = Text("λ Controls Bias-Variance Tradeoff", font_size=28, color=PURPLE, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.shrinkage_title, tradeoff_title))
        
        # Create axes
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 3, 0.5],
            x_length=8,
            y_length=5,
            axis_config={"stroke_color": WHITE, "stroke_width": 2}
        ).move_to(ORIGIN)
        
        x_label = Text("λ (Regularization)", font_size=16, color=WHITE).next_to(axes, DOWN)
        y_label = Text("Error", font_size=16, color=WHITE).next_to(axes, LEFT).rotate(PI/2)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Create bias and variance curves
        lambda_vals = np.linspace(0.1, 4.5, 50)
        
        # Bias increases with lambda (model becomes simpler)
        bias_vals = 0.3 + 0.4 * lambda_vals
        bias_points = [axes.coords_to_point(x, y) for x, y in zip(lambda_vals, bias_vals)]
        bias_curve = VMobject(color=RED, stroke_width=4)
        bias_curve.set_points_smoothly(bias_points)
        
        # Variance decreases with lambda (less overfitting)
        variance_vals = 2.5 * np.exp(-lambda_vals) + 0.2
        variance_points = [axes.coords_to_point(x, y) for x, y in zip(lambda_vals, variance_vals)]
        variance_curve = VMobject(color=BLUE, stroke_width=4)
        variance_curve.set_points_smoothly(variance_points)
        
        # Total error (bias + variance)
        total_vals = bias_vals + variance_vals
        total_points = [axes.coords_to_point(x, y) for x, y in zip(lambda_vals, total_vals)]
        total_curve = VMobject(color=GREEN, stroke_width=4)
        total_curve.set_points_smoothly(total_points)
        
        # Animate curves appearing
        bias_label = Text("Bias²", font_size=16, color=RED, weight=BOLD).move_to(axes.coords_to_point(4, 2))
        variance_label = Text("Variance", font_size=16, color=BLUE, weight=BOLD).move_to(axes.coords_to_point(0.5, 2.2))
        total_label = Text("Total Error", font_size=16, color=GREEN, weight=BOLD).move_to(axes.coords_to_point(2, 2.5))
        
        self.play(Create(variance_curve), Write(variance_label))
        self.wait(0.5)
        self.play(Create(bias_curve), Write(bias_label))
        self.wait(0.5)
        self.play(Create(total_curve), Write(total_label))
        
        # Show optimal lambda
        optimal_lambda = lambda_vals[np.argmin(total_vals)]
        optimal_line = DashedLine(
            axes.coords_to_point(optimal_lambda, 0),
            axes.coords_to_point(optimal_lambda, 3),
            color=YELLOW,
            stroke_width=3
        )
        optimal_text = Text("Optimal λ", font_size=14, color=YELLOW, weight=BOLD)
        optimal_text.next_to(optimal_line, UP, buff=0.2)
        
        self.play(Create(optimal_line), Write(optimal_text))
        
        # Add directional arrows
        lambda_arrow = Arrow(
            axes.coords_to_point(0.5, -0.3),
            axes.coords_to_point(4, -0.3),
            color=WHITE,
            stroke_width=2
        )
        lambda_arrow_text = Text("Increasing λ", font_size=14, color=WHITE)
        lambda_arrow_text.next_to(lambda_arrow, DOWN, buff=0.1)
        
        self.play(GrowArrow(lambda_arrow), Write(lambda_arrow_text))
        
        self.wait(2)
        self.play(FadeOut(VGroup(
            axes, x_label, y_label, bias_curve, variance_curve, total_curve,
            bias_label, variance_label, total_label, optimal_line, optimal_text,
            lambda_arrow, lambda_arrow_text
        )))
        self.tradeoff_title = tradeoff_title
    
    def show_feature_selection(self):
        """Show feature selection with elastic net"""
        selection_title = Text("Feature Selection: Coefficients → 0", font_size=28, color=ORANGE, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.tradeoff_title, selection_title))
        
        # Create coefficient paths as lambda increases
        features = ["Feature A", "Feature B", "Feature C", "Feature D", "Feature E"]
        colors = [RED, BLUE, GREEN, PURPLE, ORANGE]
        
        # Simulate coefficient paths (some go to zero, others shrink)
        lambda_range = np.linspace(0, 3, 100)
        coefficient_paths = [
            2.5 * np.exp(-lambda_range * 0.5),  # Feature A: shrinks slowly
            -1.8 * np.exp(-lambda_range * 2),   # Feature B: shrinks fast to zero
            3.0 * np.maximum(0, 1 - lambda_range),  # Feature C: hits zero at λ=1
            -0.9 * np.exp(-lambda_range * 1.5),     # Feature D: shrinks to zero
            1.6 * np.exp(-lambda_range * 0.3)      # Feature E: shrinks slowly
        ]
        
        # Create axes
        axes = Axes(
            x_range=[0, 3, 0.5],
            y_range=[-2, 3, 1],
            x_length=10,
            y_length=6,
            axis_config={"stroke_color": WHITE, "stroke_width": 2}
        ).move_to(ORIGIN)
        
        x_label = Text("λ", font_size=18, color=WHITE).next_to(axes, DOWN)
        y_label = Text("Coefficient Value", font_size=16, color=WHITE).next_to(axes, LEFT).rotate(PI/2)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Draw coefficient paths
        paths = VGroup()
        path_labels = VGroup()
        
        for i, (feature, color, path_values) in enumerate(zip(features, colors, coefficient_paths)):
            points = [axes.coords_to_point(lam, coeff) for lam, coeff in zip(lambda_range, path_values)]
            path = VMobject(color=color, stroke_width=3)
            path.set_points_smoothly(points)
            paths.add(path)
            
            # Label at the end
            final_point = points[-1]
            label = Text(feature, font_size=12, color=color, weight=BOLD)
            label.next_to(final_point, RIGHT, buff=0.1)
            path_labels.add(label)
        
        # Animate paths being drawn
        for path, label in zip(paths, path_labels):
            self.play(Create(path), Write(label), run_time=0.8)
        
        # Add zero line
        zero_line = DashedLine(
            axes.coords_to_point(0, 0),
            axes.coords_to_point(3, 0),
            color=GRAY,
            stroke_width=2,
            stroke_opacity=0.7
        )
        self.play(Create(zero_line))
        
        # Highlight features that go to zero
        zero_features = [1, 2, 3]  # Features B, C, D go to zero
        for idx in zero_features:
            highlight_circle = Circle(
                radius=0.2,
                color=YELLOW,
                stroke_width=3,
                fill_opacity=0
            ).move_to(axes.coords_to_point(3, 0))
            
            self.play(FadeIn(highlight_circle, scale=0.5))
            self.wait(0.3)
            self.play(FadeOut(highlight_circle))
        
        # Add selection text
        selection_text = Text("Some coefficients shrink to ZERO!", font_size=18, color=YELLOW, weight=BOLD)
        selection_text.next_to(axes, UP, buff=0.5)
        self.play(Write(selection_text))
        
        self.wait(2)
        self.play(FadeOut(VGroup(
            axes, x_label, y_label, paths, path_labels, zero_line, selection_text
        )))
        self.selection_title = selection_title
    
    def show_cv_tuning(self):
        """Show cross-validation tuning process"""
        cv_title = Text("Cross-Validation Tuning", font_size=28, color=TEAL, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.selection_title, cv_title))
        
        # Create CV error curve
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 2, 0.5],
            x_length=8,
            y_length=5,
            axis_config={"stroke_color": WHITE, "stroke_width": 2}
        ).move_to(ORIGIN)
        
        x_label = Text("λ", font_size=18, color=WHITE).next_to(axes, DOWN)
        y_label = Text("CV Error", font_size=16, color=WHITE).next_to(axes, LEFT).rotate(PI/2)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Create CV error curve (U-shaped)
        lambda_vals = np.linspace(0.1, 4.5, 50)
        cv_errors = 0.5 + 0.3 * (lambda_vals - 2)**2 + 0.05 * np.random.normal(0, 1, len(lambda_vals))
        cv_points = [axes.coords_to_point(x, y) for x, y in zip(lambda_vals, cv_errors)]
        
        # Animate CV process with moving dots
        cv_dots = VGroup()
        for i, point in enumerate(cv_points[::5]):  # Show every 5th point
            dot = Dot(point, color=BLUE, radius=0.08)
            cv_dots.add(dot)
        
        # Show "testing" process
        testing_text = Text("Testing different λ values...", font_size=16, color=WHITE)
        testing_text.to_edge(DOWN)
        self.play(Write(testing_text))
        
        # Animate dots appearing
        for dot in cv_dots:
            self.play(FadeIn(dot, scale=1.5), run_time=0.1)
        
        # Draw curve through points
        cv_curve = VMobject(color=BLUE, stroke_width=3)
        cv_curve.set_points_smoothly(cv_points)
        self.play(Create(cv_curve))
        
        # Find and highlight minimum
        min_idx = np.argmin(cv_errors)
        optimal_lambda_cv = lambda_vals[min_idx]
        min_point = cv_points[min_idx]
        
        # Highlight minimum
        min_circle = Circle(radius=0.3, color=GREEN, stroke_width=4, fill_opacity=0)
        min_circle.move_to(min_point)
        
        optimal_text = Text(f"Optimal λ = {optimal_lambda_cv:.2f}", font_size=16, color=GREEN, weight=BOLD)
        optimal_text.next_to(min_circle, UP, buff=0.3)
        
        self.play(
            ReplacementTransform(testing_text, optimal_text),
            FadeIn(min_circle, scale=0.5)
        )
        
        # Add pulsing effect to highlight
        self.play(min_circle.animate.scale(1.2), run_time=0.5)
        self.play(min_circle.animate.scale(1/1.2), run_time=0.5)
        
        self.wait(2)
        self.play(FadeOut(VGroup(
            axes, x_label, y_label, cv_dots, cv_curve, min_circle, optimal_text
        )))
        self.cv_title = cv_title
    
    def show_final_comparison(self):
        """Show final comparison of different lambda values"""
        comparison_title = Text("λ Summary: Regularization Control", font_size=32, color=YELLOW, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.cv_title, comparison_title))
        
        # Create three scenarios
        scenarios = ["λ = 0 (No Reg)", "λ = Optimal", "λ = High"]
        positions = [LEFT*4, ORIGIN, RIGHT*4]
        colors = [RED, GREEN, BLUE]
        
        scenario_groups = VGroup()
        
        for i, (scenario, pos, color) in enumerate(zip(scenarios, positions, colors)):
            # Title
            scenario_title = Text(scenario, font_size=16, color=color, weight=BOLD)
            scenario_title.move_to(pos + UP*2.5)
            
            # Coefficient representation
            if i == 0:  # No regularization
                coeff_heights = [2.5, 1.8, 3.2, 0.9, 1.6, 2.1, 1.4]  # Many large coefficients
                description = VGroup(
                    Text("Complex Model", font_size=12, color=WHITE),
                    Text("High Variance", font_size=12, color=RED),
                    Text("Overfitting", font_size=12, color=RED)
                ).arrange(DOWN, buff=0.1)
            elif i == 1:  # Optimal
                coeff_heights = [1.5, 0.8, 1.8, 0, 0.9, 1.1, 0]  # Some coefficients zero
                description = VGroup(
                    Text("Balanced Model", font_size=12, color=WHITE),
                    Text("Good Tradeoff", font_size=12, color=GREEN),
                    Text("Feature Selection", font_size=12, color=GREEN)
                ).arrange(DOWN, buff=0.1)
            else:  # High regularization
                coeff_heights = [0.3, 0.2, 0.4, 0, 0.1, 0.2, 0]  # All coefficients small
                description = VGroup(
                    Text("Simple Model", font_size=12, color=WHITE),
                    Text("High Bias", font_size=12, color=ORANGE),
                    Text("Underfitting", font_size=12, color=ORANGE)
                ).arrange(DOWN, buff=0.1)
            
            # Create coefficient bars
            bars = VGroup()
            for j, height in enumerate(coeff_heights):
                if height > 0:
                    bar = Rectangle(
                        width=0.15,
                        height=height,
                        fill_color=color,
                        fill_opacity=0.7,
                        stroke_color=WHITE,
                        stroke_width=1
                    )
                    bar.move_to(pos + LEFT*0.5 + RIGHT*j*0.15 + UP*height/2)
                    bars.add(bar)
            
            description.next_to(bars, DOWN, buff=0.5)
            
            scenario_group = VGroup(scenario_title, bars, description)
            scenario_groups.add(scenario_group)
        
        # Animate scenarios appearing
        for group in scenario_groups:
            self.play(FadeIn(group), run_time=1)
        
        # Add final message
        final_message = Text("Tune λ with CV to balance bias-variance tradeoff!", 
                           font_size=18, color=YELLOW, weight=BOLD)
        final_message.to_edge(DOWN)
        
        self.play(Write(final_message))
        self.wait(3)