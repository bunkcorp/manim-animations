from manim import *
import numpy as np

# Render:
# manim -pqh categorical_regression_methods.py CategoricalRegressionMethods

class CategoricalRegressionMethods(Scene):
    def construct(self):
        title = Text("Categorical Variables with Many Levels", weight=BOLD)
        subtitle = Text("How Different Regression Methods Handle Them", font_size=28)
        subtitle.next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(title, shift=UP*0.5), FadeIn(subtitle, shift=UP*0.5))
        self.wait(0.5)

        # Show the categorical variable setup
        setup = VGroup(
            Text("Example: City variable with 50 levels", font_size=24, color=BLUE),
            Text("X_city = [City1, City2, City3, ..., City50]", font_size=20),
            Text("Each level gets its own coefficient β_i", font_size=20)
        ).arrange(DOWN, buff=0.3)
        setup.to_edge(UP, buff=1.0)
        self.play(FadeIn(setup))
        self.wait(0.8)

        # ==== Method 1: Linear Regression with Backward Selection ====
        method1_title = Text("1. Linear Regression + Backward Selection", font_size=26, color=RED)
        method1_title.to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title, method1_title))
        
        # Show all coefficients initially
        coeffs_initial = self.create_coefficient_bars(50, "Initial Model", color=BLUE)
        coeffs_initial.to_edge(LEFT, buff=0.5).shift(DOWN*0.5)
        self.play(FadeIn(coeffs_initial))
        
        # Show backward selection process
        selection_text = VGroup(
            Text("Backward Selection Process:", font_size=20, weight=BOLD),
            Text("• Tests removing entire variable", font_size=18),
            Text("• All 50 coefficients enter/leave together", font_size=18),
            Text("• Binary decision: keep all or remove all", font_size=18)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        selection_text.to_edge(RIGHT, buff=0.5).shift(DOWN*0.5)
        self.play(FadeIn(selection_text))
        
        # Show final result - either all kept or all removed
        result1 = VGroup(
            Text("Result:", font_size=20, weight=BOLD),
            Text("Either: All 50 coefficients kept", font_size=18, color=GREEN),
            Text("Or: All 50 coefficients removed", font_size=18, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        result1.next_to(selection_text, DOWN, buff=0.5)
        self.play(FadeIn(result1))
        self.wait(1.0)

        # ==== Method 2: Ridge Regression ====
        method2_title = Text("2. Ridge Regression", font_size=26, color=GREEN)
        method2_title.to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(method1_title, method2_title))
        
        # Clear previous content
        self.play(FadeOut(coeffs_initial), FadeOut(selection_text), FadeOut(result1))
        
        # Show Ridge coefficients
        coeffs_ridge = self.create_coefficient_bars(50, "Ridge Coefficients", color=GREEN, shrink_factor=0.7)
        coeffs_ridge.to_edge(LEFT, buff=0.5).shift(DOWN*0.5)
        self.play(FadeIn(coeffs_ridge))
        
        ridge_text = VGroup(
            Text("Ridge Regression:", font_size=20, weight=BOLD),
            Text("• Keeps all 50 coefficients", font_size=18),
            Text("• Shrinks coefficients toward zero", font_size=18),
            Text("• No coefficients exactly zero", font_size=18),
            Text("• L2 penalty: Σβ²", font_size=18)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        ridge_text.to_edge(RIGHT, buff=0.5).shift(DOWN*0.5)
        self.play(FadeIn(ridge_text))
        self.wait(1.0)

        # ==== Method 3: LASSO ====
        method3_title = Text("3. LASSO Regression", font_size=26, color=ORANGE)
        method3_title.to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(method2_title, method3_title))
        
        # Clear previous content
        self.play(FadeOut(coeffs_ridge), FadeOut(ridge_text))
        
        # Show LASSO coefficients with some zeros
        coeffs_lasso = self.create_coefficient_bars(50, "LASSO Coefficients", color=ORANGE, zero_out_ratio=0.6)
        coeffs_lasso.to_edge(LEFT, buff=0.5).shift(DOWN*0.5)
        self.play(FadeIn(coeffs_lasso))
        
        lasso_text = VGroup(
            Text("LASSO Regression:", font_size=20, weight=BOLD),
            Text("• Can shrink coefficients to exactly zero", font_size=18),
            Text("• Effectively removes some levels", font_size=18),
            Text("• Sparse solution", font_size=18),
            Text("• L1 penalty: Σ|β|", font_size=18)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        lasso_text.to_edge(RIGHT, buff=0.5).shift(DOWN*0.5)
        self.play(FadeIn(lasso_text))
        self.wait(1.0)

        # ==== Method 4: Elastic Net ====
        method4_title = Text("4. Elastic Net", font_size=26, color=PURPLE)
        method4_title.to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(method3_title, method4_title))
        
        # Clear previous content
        self.play(FadeOut(coeffs_lasso), FadeOut(lasso_text))
        
        # Show Elastic Net coefficients
        coeffs_elastic = self.create_coefficient_bars(50, "Elastic Net Coefficients", color=PURPLE, zero_out_ratio=0.3)
        coeffs_elastic.to_edge(LEFT, buff=0.5).shift(DOWN*0.5)
        self.play(FadeIn(coeffs_elastic))
        
        elastic_text = VGroup(
            Text("Elastic Net:", font_size=20, weight=BOLD),
            Text("• Combines Ridge + LASSO", font_size=18),
            Text("• Some coefficients to zero", font_size=18),
            Text("• But fewer than LASSO", font_size=18),
            Text("• Penalty: α×L1 + (1-α)×L2", font_size=18)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        elastic_text.to_edge(RIGHT, buff=0.5).shift(DOWN*0.5)
        self.play(FadeIn(elastic_text))
        self.wait(1.0)

        # ==== Comparison Table ====
        comparison_title = Text("Method Comparison", font_size=26)
        comparison_title.to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(method4_title, comparison_title))
        
        # Clear previous content
        self.play(FadeOut(coeffs_elastic), FadeOut(elastic_text))
        
        # Create comparison table
        table = self.create_comparison_table()
        table.to_edge(LEFT, buff=0.5).shift(DOWN*0.5)
        self.play(FadeIn(table))
        
        # Key insights
        insights = VGroup(
            Text("Key Insights:", font_size=20, weight=BOLD),
            Text("• Backward selection: All-or-nothing", font_size=18, color=RED),
            Text("• Ridge: Keeps all, shrinks", font_size=18, color=GREEN),
            Text("• LASSO: Can remove individual levels", font_size=18, color=ORANGE),
            Text("• Elastic Net: Balanced approach", font_size=18, color=PURPLE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        insights.to_edge(RIGHT, buff=0.5).shift(DOWN*0.5)
        self.play(FadeIn(insights))
        self.wait(1.0)

        # ==== Final Takeaway ====
        takeaway = VGroup(
            RoundedRectangle(width=13.0, height=1.8, corner_radius=0.2).set_stroke(WHITE,2).set_fill(DARK_GREY,0.08),
            Tex(
                r"\textbf{Takeaway:} For high-cardinality categorical variables, ",
                r"LASSO and Elastic Net offer more granular control than backward selection. ",
                r"Ridge keeps all levels but may overfit.",
                tex_environment="flushleft"
            ).scale(0.85)
        )
        takeaway[1].move_to(takeaway[0].get_center())
        takeaway.to_edge(DOWN, buff=0.25)
        self.play(Create(takeaway[0]), Write(takeaway[1]))
        self.wait(1.5)

    # ---------- Helper Methods ----------
    def create_coefficient_bars(self, n_coeffs, title, color=WHITE, shrink_factor=1.0, zero_out_ratio=0.0):
        """Create a visualization of coefficient bars."""
        title_text = Text(title, font_size=20, weight=BOLD)
        
        # Create coefficient bars
        bars = VGroup()
        for i in range(n_coeffs):
            # Random coefficient value
            if np.random.random() < zero_out_ratio:
                height = 0  # Zero coefficient
            else:
                height = np.random.uniform(0.1, 1.0) * shrink_factor
            
            bar = Rectangle(
                width=0.02, 
                height=height, 
                fill_color=color, 
                fill_opacity=0.8,
                stroke_width=0
            )
            bar.move_to([i*0.04 - 1.0, height/2, 0])
            bars.add(bar)
        
        # Add axis
        axis = Line(start=[-1.0, 0, 0], end=[1.0, 0, 0], stroke_color=GREY_B, stroke_width=2)
        
        return VGroup(title_text, axis, bars).arrange(DOWN, buff=0.3)

    def create_comparison_table(self):
        """Create a comparison table of the methods."""
        # Headers
        headers = VGroup(
            Text("Method", font_size=18, weight=BOLD),
            Text("Coefficients", font_size=18, weight=BOLD),
            Text("Selection", font_size=18, weight=BOLD),
            Text("Penalty", font_size=18, weight=BOLD)
        ).arrange(RIGHT, buff=0.8)
        
        # Rows
        row1 = VGroup(
            Text("Backward", font_size=16, color=RED),
            Text("All or None", font_size=16),
            Text("Binary", font_size=16),
            Text("None", font_size=16)
        ).arrange(RIGHT, buff=0.8)
        
        row2 = VGroup(
            Text("Ridge", font_size=16, color=GREEN),
            Text("All kept", font_size=16),
            Text("Shrink", font_size=16),
            Text("L2", font_size=16)
        ).arrange(RIGHT, buff=0.8)
        
        row3 = VGroup(
            Text("LASSO", font_size=16, color=ORANGE),
            Text("Some zero", font_size=16),
            Text("Sparse", font_size=16),
            Text("L1", font_size=16)
        ).arrange(RIGHT, buff=0.8)
        
        row4 = VGroup(
            Text("Elastic Net", font_size=16, color=PURPLE),
            Text("Some zero", font_size=16),
            Text("Balanced", font_size=16),
            Text("L1 + L2", font_size=16)
        ).arrange(RIGHT, buff=0.8)
        
        # Arrange all rows
        table = VGroup(headers, row1, row2, row3, row4).arrange(DOWN, buff=0.3)
        
        # Add borders
        border = Rectangle(
            width=table.width + 0.2,
            height=table.height + 0.2,
            stroke_color=WHITE,
            stroke_width=2,
            fill_opacity=0
        )
        border.move_to(table.get_center())
        
        return VGroup(border, table)
