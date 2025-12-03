#!/usr/bin/env python3
"""
AIC vs BIC Model Selection Animation
Shows the differences between AIC and BIC criteria and when to use each
"""

from manim import *
import numpy as np

class AICBICAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Show title card
        self.show_title()
        
        # Show basic concepts
        self.show_basic_concepts()
        
        # Show formulas
        self.show_formulas()
        
        # Show penalty comparison
        self.show_penalty_comparison()
        
        # Show worked example
        self.show_worked_example()
        
        # Show summary
        self.show_summary()
    
    def show_title(self):
        """Title card"""
        title = Text("Model Selection Criteria", font_size=36, color=YELLOW, weight=BOLD)
        subtitle = Text("AIC vs. BIC", font_size=28, color=WHITE)
        concept = Text("Lower value = better • BIC penalizes complexity more (≈ simpler models)", 
                      font_size=18, color=LIGHT_GRAY, slant=ITALIC)
        
        title_group = VGroup(title, subtitle, concept).arrange(DOWN, buff=0.4)
        
        self.play(Write(title))
        self.play(Write(subtitle))
        self.play(Write(concept))
        self.wait(2)
        self.play(FadeOut(title_group))
    
    def show_basic_concepts(self):
        """Show what AIC and BIC are for"""
        title = Text("Why Do We Need Model Selection Criteria?", font_size=32, color=BLUE, weight=BOLD).to_edge(UP)
        self.play(Write(title))
        
        # Model selection problem
        problem = VGroup(
            Text("The Model Selection Problem:", font_size=24, color=ORANGE, weight=BOLD),
            Text("• Multiple candidate models with different complexities", font_size=20, color=WHITE),
            Text("• More parameters usually improve fit to training data", font_size=20, color=WHITE),
            Text("• But complex models may overfit and generalize poorly", font_size=20, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP*1)
        
        for item in problem:
            self.play(Write(item))
            self.wait(0.8)
        
        # Solution
        solution = VGroup(
            Text("Solution: Information Criteria", font_size=24, color=GREEN, weight=BOLD),
            Text("• Balance model fit (likelihood) vs complexity (parameters)", font_size=20, color=WHITE),
            Text("• AIC and BIC are two popular approaches", font_size=20, color=WHITE),
            Text("• Both follow: Criterion = Goodness of Fit + Complexity Penalty", font_size=20, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(DOWN*1)
        
        for item in solution:
            self.play(Write(item))
            self.wait(0.8)
        
        self.wait(2)
        self.play(FadeOut(problem, solution))
        self.title = title
    
    def show_formulas(self):
        """Show AIC and BIC formulas"""
        formula_title = Text("AIC vs BIC Formulas", font_size=28, color=GREEN, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.title, formula_title))
        
        # Create comparison table
        table_data = [
            ["Criterion", "Formula", "Penalty per Parameter"],
            ["AIC", "AIC = -2ℓ + 2(p+1)", "2"],
            ["BIC", "BIC = -2ℓ + ln(n)(p+1)", "ln(n)"]
        ]
        
        # Create table manually for better control
        headers = VGroup(
            Text("Criterion", font_size=20, color=YELLOW, weight=BOLD),
            Text("Formula", font_size=20, color=YELLOW, weight=BOLD),
            Text("Penalty per Parameter", font_size=20, color=YELLOW, weight=BOLD)
        ).arrange(RIGHT, buff=1.5).move_to(UP*1.5)
        
        aic_row = VGroup(
            Text("AIC", font_size=18, color=BLUE, weight=BOLD),
            Text("AIC = -2ℓ + 2(p+1)", font_size=18, color=WHITE),
            Text("2", font_size=18, color=WHITE)
        ).arrange(RIGHT, buff=1.5).move_to(UP*0.5)
        
        bic_row = VGroup(
            Text("BIC", font_size=18, color=YELLOW, weight=BOLD),
            Text("BIC = -2ℓ + ln(n)(p+1)", font_size=18, color=WHITE),
            Text("ln(n)", font_size=18, color=WHITE)
        ).arrange(RIGHT, buff=1.5).move_to(DOWN*0.5)
        
        # Create table box
        table_box = RoundedRectangle(
            width=12, height=3,
            stroke_color=WHITE, stroke_width=2,
            fill_color=BLACK, fill_opacity=0.1
        ).move_to(ORIGIN)
        
        self.play(FadeIn(table_box))
        self.play(Write(headers))
        self.play(Write(aic_row))
        self.play(Write(bic_row))
        
        # Add notation explanation
        notation = VGroup(
            Text("Where:", font_size=18, color=ORANGE, weight=BOLD),
            Text("ℓ = log-likelihood of the model", font_size=16, color=WHITE),
            Text("p = number of parameters (excluding intercept)", font_size=16, color=WHITE),
            Text("n = sample size", font_size=16, color=WHITE),
            Text("-2ℓ = deviance (in R terminology)", font_size=16, color=LIGHT_GRAY, slant=ITALIC)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(table_box, DOWN, buff=0.8)
        
        for note in notation:
            self.play(Write(note))
            self.wait(0.5)
        
        self.wait(2)
        
        # Store elements
        self.formula_elements = VGroup(table_box, headers, aic_row, bic_row, notation)
        self.formula_title = formula_title

    def show_penalty_comparison(self):
        """Show how penalties differ with sample size"""
        penalty_title = Text("Key Difference: Penalty Grows with Sample Size", font_size=28, color=PURPLE, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.formula_title, penalty_title))
        
        # Fade out formula table
        self.play(self.formula_elements.animate.set_opacity(0.2))
        
        # Create penalty plot
        axes = Axes(
            x_range=[10, 1000, 100],
            y_range=[0, 8, 1],
            x_length=8,
            y_length=5,
            axis_config={"stroke_color": WHITE, "stroke_width": 2}
        ).move_to(ORIGIN)
        
        x_label = Text("Sample Size (n)", font_size=16, color=WHITE).next_to(axes, DOWN)
        y_label = Text("Penalty per Parameter", font_size=16, color=WHITE).next_to(axes, LEFT).rotate(PI/2)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Generate penalty curves
        n_values = np.linspace(10, 1000, 200)
        aic_penalties = np.full_like(n_values, 2.0)  # Constant at 2
        bic_penalties = np.log(n_values)  # Growing with ln(n)
        
        # Create curves
        aic_curve = VMobject(color=BLUE, stroke_width=4)
        aic_points = [axes.coords_to_point(n, 2) for n in n_values]
        aic_curve.set_points_smoothly(aic_points)
        
        bic_curve = VMobject(color=YELLOW, stroke_width=4)
        bic_points = [axes.coords_to_point(n, np.log(n)) for n in n_values]
        bic_curve.set_points_smoothly(bic_points)
        
        # Show curves
        self.play(Create(aic_curve))
        self.play(Create(bic_curve))
        
        # Add legend
        legend = VGroup(
            VGroup(
                Rectangle(width=0.4, height=0.1, fill_color=BLUE, fill_opacity=1, stroke_width=0),
                Text("AIC penalty = 2 (constant)", font_size=16, color=WHITE)
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Rectangle(width=0.4, height=0.1, fill_color=YELLOW, fill_opacity=1, stroke_width=0),
                Text("BIC penalty = ln(n) (growing)", font_size=16, color=WHITE)
            ).arrange(RIGHT, buff=0.3)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(axes, RIGHT, buff=1)
        
        self.play(FadeIn(legend))
        
        # Show specific values with moving dot
        n_tracker = ValueTracker(50)
        
        bic_dot = always_redraw(
            lambda: Dot(
                axes.coords_to_point(n_tracker.get_value(), np.log(n_tracker.get_value())),
                color=YELLOW,
                radius=0.08
            )
        )
        
        value_label = always_redraw(
            lambda: VGroup(
                Text(f"n = {n_tracker.get_value():.0f}", font_size=14, color=WHITE),
                Text(f"ln(n) = {np.log(n_tracker.get_value()):.2f}", font_size=14, color=YELLOW)
            ).arrange(DOWN, buff=0.1).next_to(bic_dot, UP, buff=0.3)
        )
        
        self.play(FadeIn(bic_dot), FadeIn(value_label))
        
        # Animate the growing penalty
        self.play(n_tracker.animate.set_value(100), run_time=1.5)
        self.play(n_tracker.animate.set_value(500), run_time=1.5)
        self.play(n_tracker.animate.set_value(800), run_time=1.5)
        
        # Key insight
        insight = Text("BIC's penalty grows → tends to favor simpler models as n increases",
                      font_size=18, color=GREEN, weight=BOLD, slant=ITALIC)
        insight.next_to(axes, DOWN, buff=0.8)
        self.play(Write(insight))
        
        self.wait(2)
        
        # Store penalty elements
        self.penalty_elements = VGroup(
            axes, x_label, y_label, aic_curve, bic_curve, 
            legend, bic_dot, value_label, insight
        )
        self.penalty_title = penalty_title

    def show_worked_example(self):
        """Show concrete example with two models"""
        example_title = Text("Worked Example: Comparing Two Models", font_size=28, color=ORANGE, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.penalty_title, example_title))
        
        # Clear previous elements
        self.play(FadeOut(self.formula_elements, self.penalty_elements))
        
        # Example setup
        setup_box = RoundedRectangle(
            width=11, height=2,
            stroke_color=BLUE, stroke_width=2,
            fill_color=BLUE, fill_opacity=0.1
        ).move_to(UP*2)
        
        setup_content = VGroup(
            Text("Example Setup:", font_size=20, color=BLUE, weight=BOLD),
            Text("n = 120 observations", font_size=16, color=WHITE),
            Text("Two candidate models with different complexities", font_size=16, color=WHITE)
        ).arrange(DOWN, buff=0.3).move_to(setup_box.get_center())
        
        self.play(FadeIn(setup_box), Write(setup_content))
        
        # Model specifications
        n = 120
        ln_n = np.log(n)
        
        model_a_specs = VGroup(
            Text("Model A (Simple):", font_size=20, color=GREEN, weight=BOLD),
            Text("Log-likelihood (ℓ) = -210", font_size=16, color=WHITE),
            Text("Parameters (p) = 3", font_size=16, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(LEFT*3)
        
        model_b_specs = VGroup(
            Text("Model B (Complex):", font_size=20, color=RED, weight=BOLD),
            Text("Log-likelihood (ℓ) = -206", font_size=16, color=WHITE),
            Text("Parameters (p) = 6", font_size=16, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(RIGHT*3)
        
        self.play(Write(model_a_specs), Write(model_b_specs))
        
        # Calculate AIC and BIC
        def calc_aic(log_lik, p):
            return -2 * log_lik + 2 * (p + 1)
        
        def calc_bic(log_lik, p, n):
            return -2 * log_lik + np.log(n) * (p + 1)
        
        # Model A calculations
        aic_a = calc_aic(-210, 3)
        bic_a = calc_bic(-210, 3, n)
        
        # Model B calculations
        aic_b = calc_aic(-206, 6)
        bic_b = calc_bic(-206, 6, n)
        
        # Show calculations
        calc_box = RoundedRectangle(
            width=12, height=3,
            stroke_color=WHITE, stroke_width=2,
            fill_color=BLACK, fill_opacity=0.9
        ).move_to(DOWN*1.5)
        
        calculations = VGroup(
            Text("Calculations:", font_size=20, color=YELLOW, weight=BOLD),
            VGroup(
                Text(f"Model A: AIC = -2(-210) + 2(4) = {aic_a:.1f}", font_size=16, color=WHITE),
                Text(f"        BIC = -2(-210) + ln(120)(4) = {bic_a:.1f}", font_size=16, color=WHITE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(
                Text(f"Model B: AIC = -2(-206) + 2(7) = {aic_b:.1f}", font_size=16, color=WHITE),
                Text(f"        BIC = -2(-206) + ln(120)(7) = {bic_b:.1f}", font_size=16, color=WHITE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(calc_box.get_center())
        
        self.play(FadeIn(calc_box), Write(calculations))
        
        # Show winners
        aic_winner = "A" if aic_a < aic_b else "B"
        bic_winner = "A" if bic_a < bic_b else "B"
        
        winners = VGroup(
            Text("Results (Lower is Better):", font_size=18, color=ORANGE, weight=BOLD),
            Text(f"AIC chooses Model {aic_winner} ({min(aic_a, aic_b):.1f} < {max(aic_a, aic_b):.1f})", 
                 font_size=16, color=BLUE, weight=BOLD),
            Text(f"BIC chooses Model {bic_winner} ({min(bic_a, bic_b):.1f} < {max(bic_a, bic_b):.1f})", 
                 font_size=16, color=YELLOW, weight=BOLD)
        ).arrange(DOWN, buff=0.3).next_to(calc_box, DOWN, buff=0.5)
        
        for winner in winners:
            self.play(Write(winner))
            self.wait(0.8)
        
        # Highlight the difference
        if aic_winner != bic_winner:
            difference_note = Text(
                "Different choices! BIC favors the simpler model due to higher penalty.",
                font_size=16, color=GREEN, weight=BOLD, slant=ITALIC
            ).next_to(winners, DOWN, buff=0.3)
            self.play(Write(difference_note))
        
        self.wait(2)
        
        # Store example elements
        self.example_elements = VGroup(
            setup_box, setup_content, model_a_specs, model_b_specs,
            calc_box, calculations, winners
        )
        if aic_winner != bic_winner:
            self.example_elements.add(difference_note)
        self.example_title = example_title

    def show_summary(self):
        """Show final summary"""
        summary_title = Text("AIC vs BIC: Summary & Guidelines", font_size=32, color=YELLOW, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.example_title, summary_title))
        
        # Clear example
        self.play(FadeOut(self.example_elements))
        
        # Create comprehensive comparison
        comparison_card = RoundedRectangle(
            corner_radius=0.2, width=13, height=6,
            stroke_color=WHITE, stroke_width=2,
            fill_color=BLACK, fill_opacity=0.95
        ).move_to(ORIGIN)
        
        # Comparison content
        comparison_content = VGroup(
            # Formulas
            VGroup(
                Text("📋 Formulas:", font_size=22, color=YELLOW, weight=BOLD),
                Text("AIC = -2ℓ + 2(p+1)  →  penalty = 2 per parameter", font_size=18, color=BLUE),
                Text("BIC = -2ℓ + ln(n)(p+1)  →  penalty = ln(n) per parameter", font_size=18, color=YELLOW)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2),
            
            # Key differences
            VGroup(
                Text("🔍 Key Differences:", font_size=22, color=GREEN, weight=BOLD),
                Text("• AIC: Constant penalty, more liberal (allows complex models)", font_size=18, color=WHITE),
                Text("• BIC: Growing penalty with n, more conservative (favors simple models)", font_size=18, color=WHITE),
                Text("• As n increases, BIC penalty grows while AIC stays constant", font_size=18, color=WHITE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2),
            
            # When to use
            VGroup(
                Text("🎯 When to Use:", font_size=22, color=ORANGE, weight=BOLD),
                Text("• AIC: Prediction focus, want to minimize expected prediction error", font_size=18, color=WHITE),
                Text("• BIC: Interpretation focus, want to find the 'true' model structure", font_size=18, color=WHITE),
                Text("• Large n: BIC becomes much more conservative than AIC", font_size=18, color=WHITE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        ).arrange(DOWN, buff=0.6).move_to(comparison_card.get_center())
        
        self.play(FadeIn(comparison_card))
        
        # Animate sections
        for section in comparison_content:
            self.play(Write(section[0]))
            for item in section[1:]:
                self.play(Write(item))
                self.wait(0.4)
            self.wait(0.8)
        
        # Final key insight
        key_insight = Text(
            "Remember: Both seek to balance fit vs complexity, but BIC is more conservative!",
            font_size=20, color=YELLOW, weight=BOLD
        ).next_to(comparison_card, DOWN, buff=0.8)
        
        self.play(Write(key_insight))
        self.wait(3)
        
        # Update todos
        self.mark_todos_complete()
    
    def mark_todos_complete(self):
        """Mark all todos as complete"""
        pass  # TodoWrite calls would go here if needed