#!/usr/bin/env python3
"""
Decision Tree Tuning Animation
Shows xerror vs relerror curves and how to interpret them for cp tuning
"""

from manim import *
import numpy as np

class TreeTuningAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Show title card
        self.show_title()
        
        # Show basic concept
        self.show_basic_concept()
        
        # Show the curves
        self.show_error_curves()
        
        # Show interpretation
        self.show_interpretation()
        
        # Show optimal selection
        self.show_optimal_selection()
        
        # Show summary
        self.show_summary()
    
    def show_title(self):
        """Title card"""
        title = Text("Decision Tree Tuning", font_size=36, color=YELLOW, weight=BOLD)
        subtitle = Text("Identifying xerror vs relerror", font_size=28, color=WHITE)
        concept = Text("xerror = CV error (U-shaped) • relerror = training relative error (↓ as cp ↓)", 
                      font_size=20, color=LIGHT_GRAY, slant=ITALIC)
        
        title_group = VGroup(title, subtitle, concept).arrange(DOWN, buff=0.4)
        
        self.play(Write(title))
        self.play(Write(subtitle))
        self.play(Write(concept))
        self.wait(2)
        self.play(FadeOut(title_group))
    
    def show_basic_concept(self):
        """Explain cp parameter and its effects"""
        title = Text("Complexity Parameter (cp) Tuning", font_size=32, color=BLUE, weight=BOLD).to_edge(UP)
        self.play(Write(title))
        
        # Key concepts
        concepts = VGroup(
            Text("🎯 Goal: Find optimal tree complexity to avoid overfitting", font_size=24, color=WHITE),
            Text("📊 cp parameter: Controls tree pruning (lower cp = more complex tree)", font_size=24, color=WHITE),
            Text("⚖️ Trade-off: Training accuracy vs generalization ability", font_size=24, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to(ORIGIN)
        
        for concept in concepts:
            self.play(FadeIn(concept, shift=UP))
            self.wait(1)
        
        # Show complexity spectrum
        spectrum = VGroup(
            Text("Tree Complexity Spectrum:", font_size=22, color=ORANGE, weight=BOLD),
            VGroup(
                Text("High cp", font_size=18, color=WHITE),
                Text("→", font_size=18, color=WHITE),
                Text("Simple tree", font_size=18, color=GREEN),
                Text("→", font_size=18, color=WHITE), 
                Text("Underfitting risk", font_size=18, color=RED)
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("Low cp", font_size=18, color=WHITE),
                Text("→", font_size=18, color=WHITE),
                Text("Complex tree", font_size=18, color=GREEN),
                Text("→", font_size=18, color=WHITE),
                Text("Overfitting risk", font_size=18, color=RED)
            ).arrange(RIGHT, buff=0.3)
        ).arrange(DOWN, buff=0.4).next_to(concepts, DOWN, buff=1)
        
        for item in spectrum:
            self.play(Write(item))
            self.wait(0.8)
        
        self.wait(2)
        self.play(FadeOut(concepts, spectrum))
        self.title = title
    
    def show_error_curves(self):
        """Show xerror and relerror curves"""
        curves_title = Text("Error Curves: xerror vs relerror", font_size=28, color=GREEN, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.title, curves_title))
        
        # Create axes
        axes = Axes(
            x_range=[0.0, 0.06, 0.01],
            y_range=[0.0, 1.05, 0.2],
            x_length=10,
            y_length=5.5,
            axis_config={"stroke_color": WHITE, "stroke_width": 2},
            x_axis_config={"decimal_number_config": {"num_decimal_places": 2}}
        ).move_to(DOWN*0.3)
        
        x_label = Text("cp (complexity parameter)", font_size=18, color=WHITE).next_to(axes, DOWN)
        y_label = Text("Error (relative scale)", font_size=18, color=WHITE).next_to(axes, LEFT).rotate(PI/2)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Generate synthetic data
        np.random.seed(42)
        xs = np.linspace(0.001, 0.06, 60)
        
        # relerror: decreases as cp decreases (training error improves with complexity)
        relerror = 0.2 + 0.7 * (xs / xs.max())**1.2
        relerror = np.clip(relerror, 0.05, 0.95)
        
        # xerror: U-shaped (CV error drops then rises due to overfitting)
        xerror_base = 0.35 + 0.22*((xs-0.015)/0.022)**2
        noise = 0.015*np.sin(40*xs)
        xerror = np.clip(xerror_base + noise, 0.1, 0.95)
        
        # Convert to plot points
        def to_points(y_values):
            return [axes.coords_to_point(x, y) for x, y in zip(xs, y_values)]
        
        # Create curves
        relerror_curve = VMobject(color=BLUE, stroke_width=4)
        relerror_curve.set_points_smoothly(to_points(relerror))
        
        xerror_curve = VMobject(color=YELLOW, stroke_width=4)
        xerror_curve.set_points_smoothly(to_points(xerror))
        
        # Show relerror first
        relerror_label = Text("relerror (training error)", font_size=18, color=BLUE, slant=ITALIC)
        relerror_label.next_to(axes, RIGHT, buff=1).shift(UP*1.5)
        
        self.play(Create(relerror_curve), Write(relerror_label))
        self.wait(1)
        
        # Add explanation for relerror
        relerror_explanation = VGroup(
            Text("• Training relative error", font_size=16, color=WHITE),
            Text("• Decreases as cp decreases", font_size=16, color=WHITE),
            Text("• More complex tree fits training data better", font_size=16, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(relerror_label, DOWN, buff=0.3)
        
        for exp in relerror_explanation:
            self.play(Write(exp))
            self.wait(0.5)
        
        # Show xerror
        xerror_label = Text("xerror (CV error)", font_size=18, color=YELLOW, slant=ITALIC)
        xerror_label.next_to(relerror_explanation, DOWN, buff=0.8)
        
        self.play(Create(xerror_curve), Write(xerror_label))
        self.wait(1)
        
        # Add explanation for xerror
        xerror_explanation = VGroup(
            Text("• Cross-validation error", font_size=16, color=WHITE),
            Text("• U-shaped curve", font_size=16, color=WHITE),
            Text("• Drops then rises (overfitting)", font_size=16, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(xerror_label, DOWN, buff=0.3)
        
        for exp in xerror_explanation:
            self.play(Write(exp))
            self.wait(0.5)
        
        # Add complexity direction arrow
        complexity_arrow = Arrow(
            start=axes.coords_to_point(0.055, -0.08),
            end=axes.coords_to_point(0.005, -0.08),
            stroke_width=3,
            color=WHITE,
            max_tip_length_to_length_ratio=0.1
        )
        complexity_text = Text("Lower cp → More complex tree", font_size=16, color=WHITE, slant=ITALIC)
        complexity_text.next_to(complexity_arrow, DOWN, buff=0.2)
        
        self.play(GrowArrow(complexity_arrow), Write(complexity_text))
        
        self.wait(2)
        
        # Store elements
        self.error_elements = VGroup(
            relerror_curve, xerror_curve, relerror_label, xerror_label,
            relerror_explanation, xerror_explanation, complexity_arrow, complexity_text
        )
        self.axes = axes
        self.x_label = x_label
        self.y_label = y_label
        self.xs = xs
        self.xerror = xerror
        self.curves_title = curves_title
    
    def show_interpretation(self):
        """Show how to interpret the curves"""
        interp_title = Text("Interpreting the Curves", font_size=28, color=PURPLE, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.curves_title, interp_title))
        
        # Fade out explanations to focus on curves
        self.play(self.error_elements.animate.set_opacity(0.3))
        
        # Find minimum xerror point
        min_idx = np.argmin(self.xerror)
        cp_min = self.xs[min_idx]
        xerror_min = self.xerror[min_idx]
        
        # Mark minimum point
        min_dot = Dot(
            self.axes.coords_to_point(cp_min, xerror_min),
            radius=0.1,
            color=RED
        )
        
        min_label = VGroup(
            Text("Minimum xerror", font_size=18, color=RED, weight=BOLD),
            Text(f"cp = {cp_min:.3f}", font_size=16, color=WHITE),
            Text(f"xerror = {xerror_min:.2f}", font_size=16, color=WHITE)
        ).arrange(DOWN, buff=0.1).next_to(min_dot, UP+LEFT, buff=0.3)
        
        self.play(FadeIn(min_dot, scale=1.5), Write(min_label))
        
        # Highlight overfitting region
        overfit_region = Rectangle(
            width=self.axes.x_axis.unit_size * 0.012,
            height=self.axes.y_axis.get_length(),
            stroke_width=0,
            fill_color=RED,
            fill_opacity=0.2
        ).move_to(self.axes.coords_to_point(0.006, 0.5))
        
        overfit_label = Text("Overfitting Region", font_size=16, color=RED, weight=BOLD)
        overfit_label.next_to(overfit_region, UP, buff=0.2)
        
        overfit_note = VGroup(
            Text("Very low cp:", font_size=14, color=WHITE),
            Text("• xerror increases", font_size=14, color=WHITE),
            Text("• Tree too complex", font_size=14, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(overfit_label, DOWN, buff=0.2)
        
        self.play(
            FadeIn(overfit_region),
            Write(overfit_label),
            *[Write(note) for note in overfit_note]
        )
        
        # Show the U-shape behavior
        u_shape_arrow1 = CurvedArrow(
            self.axes.coords_to_point(0.045, 0.8),
            self.axes.coords_to_point(cp_min, xerror_min + 0.1),
            angle=-PI/3,
            color=GREEN
        )
        
        u_shape_arrow2 = CurvedArrow(
            self.axes.coords_to_point(cp_min, xerror_min + 0.1),
            self.axes.coords_to_point(0.008, 0.6),
            angle=-PI/3,
            color=GREEN
        )
        
        u_shape_text = Text("U-shaped: drops then rises", font_size=16, color=GREEN, weight=BOLD)
        u_shape_text.next_to(self.axes.coords_to_point(cp_min, xerror_min), DOWN, buff=0.8)
        
        self.play(
            Create(u_shape_arrow1),
            Create(u_shape_arrow2),
            Write(u_shape_text)
        )
        
        self.wait(2)
        
        # Store interpretation elements
        self.interp_elements = VGroup(
            min_dot, min_label, overfit_region, overfit_label, overfit_note,
            u_shape_arrow1, u_shape_arrow2, u_shape_text
        )
        self.cp_min = cp_min
        self.interp_title = interp_title
    
    def show_optimal_selection(self):
        """Show how to select optimal cp"""
        optimal_title = Text("Selecting Optimal cp", font_size=28, color=ORANGE, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.interp_title, optimal_title))
        
        # Restore curve visibility
        self.play(self.error_elements.animate.set_opacity(1))
        
        # Show optimal region
        optimal_cp_range = [self.cp_min - 0.005, self.cp_min + 0.005]
        
        optimal_region = Rectangle(
            width=self.axes.x_axis.unit_size * 0.01,
            height=self.axes.y_axis.get_length(),
            stroke_color=GREEN,
            stroke_width=3,
            fill_color=GREEN,
            fill_opacity=0.1
        ).move_to(self.axes.coords_to_point(self.cp_min, 0.5))
        
        optimal_label = Text("Optimal cp Range", font_size=18, color=GREEN, weight=BOLD)
        optimal_label.next_to(optimal_region, LEFT, buff=0.8)
        
        # Selection strategies
        strategies = VGroup(
            Text("Selection Strategies:", font_size=20, color=YELLOW, weight=BOLD),
            Text("1. Minimum xerror cp", font_size=16, color=WHITE),
            Text("2. 1-SE rule: cp within 1 std error of minimum", font_size=16, color=WHITE),
            Text("3. Grid search with cross-validation", font_size=16, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(optimal_label, DOWN, buff=0.5)
        
        self.play(
            FadeIn(optimal_region),
            Write(optimal_label),
            *[Write(strategy) for strategy in strategies]
        )
        
        # Show 1-SE rule visually
        se_upper = self.axes.coords_to_point(self.cp_min, min(self.xerror) + 0.05)
        se_lower = self.axes.coords_to_point(self.cp_min, min(self.xerror) - 0.05)
        
        se_line = Line(se_upper, se_lower, stroke_color=ORANGE, stroke_width=3)
        se_text = Text("1-SE range", font_size=14, color=ORANGE)
        se_text.next_to(se_line, RIGHT, buff=0.2)
        
        self.play(Create(se_line), Write(se_text))
        
        self.wait(2)
        self.play(FadeOut(self.interp_elements, optimal_region, optimal_label, strategies, se_line, se_text))
        self.optimal_title = optimal_title
    
    def show_summary(self):
        """Show final summary"""
        summary_title = Text("Decision Tree Tuning Summary", font_size=32, color=YELLOW, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.optimal_title, summary_title))
        
        # Fade axes and curves
        self.play(
            FadeOut(self.axes, self.x_label, self.y_label),
            self.error_elements.animate.set_opacity(0.2)
        )
        
        # Create summary card
        summary_card = RoundedRectangle(
            corner_radius=0.2, width=12, height=4,
            stroke_color=WHITE, stroke_width=2,
            fill_color=BLACK, fill_opacity=0.95
        ).move_to(ORIGIN)
        
        # Summary content
        summary_content = VGroup(
            Text("Key Concepts:", font_size=24, color=YELLOW, weight=BOLD),
            VGroup(
                Text("📈 relerror = training relative error → decreases as cp decreases", font_size=18, color=WHITE),
                Text("📊 xerror = cross-validation error → typically U-shaped vs cp", font_size=18, color=WHITE),
                Text("⚠️ At very low cp: xerror rises again (overfitting)", font_size=18, color=WHITE),
                Text("🎯 Optimal cp: minimum xerror or 1-SE rule", font_size=18, color=WHITE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3),
            
            Text("Best Practice:", font_size=20, color=GREEN, weight=BOLD),
            Text("Use cross-validation curves to select cp that balances bias-variance trade-off", 
                 font_size=16, color=WHITE, slant=ITALIC)
        ).arrange(DOWN, buff=0.4).move_to(summary_card.get_center())
        
        self.play(FadeIn(summary_card), *[Write(item) for item in summary_content])
        
        # Final message
        final_message = Text(
            "Master cp tuning to build robust, well-generalized decision trees!",
            font_size=20,
            color=YELLOW,
            weight=BOLD
        ).next_to(summary_card, DOWN, buff=0.8)
        
        self.play(Write(final_message))
        self.wait(3)