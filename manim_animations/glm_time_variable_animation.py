#!/usr/bin/env python3
"""
GLM Time Variable Animation
Visual demonstration of why time variables can have non-significant coefficients
despite strong influence due to non-linear relationships
"""

from manim import *
import numpy as np

class GLMTimeVariableAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Show the research question
        self.show_research_question()
        
        # Show scatter plot with non-linear pattern
        self.show_non_linear_pattern()
        
        # Demonstrate linear GLM failure
        self.show_linear_glm_failure()
        
        # Show polynomial solution
        self.show_polynomial_solution()
        
        # Compare model specifications
        self.show_model_comparison()
        
        # Show final insights
        self.show_final_insights()
    
    def generate_time_data(self, n=200):
        """Generate synthetic data with strong non-linear time relationship"""
        np.random.seed(42)
        
        # Time variable (0-24 hours)
        hours = np.random.uniform(0, 24, n)
        
        # Create U-shaped relationship (higher emergency calls at night and morning rush)
        # Peak around 2-4 AM and 7-9 AM
        base_emergency_rate = (
            0.3 * np.exp(-((hours - 3) / 2) ** 2) +  # Night peak
            0.25 * np.exp(-((hours - 8) / 3) ** 2) +  # Morning peak
            0.15 * np.exp(-((hours - 18) / 4) ** 2) + # Evening peak
            0.05  # Baseline
        )
        
        # Add noise
        emergency_calls = base_emergency_rate + np.random.normal(0, 0.05, n)
        emergency_calls = np.clip(emergency_calls, 0, 1)  # Keep in [0,1] range
        
        return hours, emergency_calls
    
    def show_research_question(self):
        """Show the research question and setup"""
        title = Text("GLM Time Variables: Linear vs Non-Linear", 
                    font_size=36, color=YELLOW, weight=BOLD)
        title.to_edge(UP)
        
        question = VGroup(
            Text("Research Question:", font_size=24, color=WHITE, weight=BOLD),
            Text("Does HourOfCall predict EmergencyResponse?", font_size=20, color=BLUE),
        ).arrange(DOWN, buff=0.3)
        question.move_to(UP*1.5)
        
        # Show linear GLM assumption
        assumption = VGroup(
            Text("Linear GLM assumes:", font_size=18, color=ORANGE, weight=BOLD),
            Text("Y = β₀ + β₁ × HourOfCall + ε", font_size=16, color=WHITE),
            Text("(Straight line relationship)", font_size=14, color=GRAY)
        ).arrange(DOWN, buff=0.2)
        assumption.move_to(DOWN*0.5)
        
        # Reality preview
        reality = VGroup(
            Text("Reality:", font_size=18, color=RED, weight=BOLD),
            Text("Emergency calls peak at night & morning rush", font_size=14, color=WHITE),
            Text("(Non-linear, U-shaped pattern)", font_size=14, color=GRAY)
        ).arrange(DOWN, buff=0.2)
        reality.move_to(DOWN*2.5)
        
        self.play(Write(title))
        self.play(Write(question))
        self.play(Write(assumption))
        self.play(Write(reality))
        
        self.wait(2)
        self.play(FadeOut(VGroup(question, assumption, reality)))
        
        self.title = title
    
    def show_non_linear_pattern(self):
        """Show scatter plot with clear non-linear pattern"""
        scatter_title = Text("Step 1: Visualize the Data", 
                           font_size=28, color=BLUE, weight=BOLD)
        scatter_title.to_edge(UP, buff=0.5)
        self.play(ReplacementTransform(self.title, scatter_title))
        
        # Generate data
        hours, emergency_calls = self.generate_time_data()
        
        # Create axes
        axes = Axes(
            x_range=[0, 24, 6],
            y_range=[0, 1, 0.2],
            x_length=10,
            y_length=6,
            axis_config={"stroke_color": WHITE, "stroke_width": 2}
        ).move_to(DOWN*0.5)
        
        # Add labels
        x_label = Text("Hour of Call (0-24)", font_size=16, color=WHITE)
        x_label.next_to(axes.x_axis, DOWN, buff=0.3)
        
        y_label = Text("Emergency Response Rate", font_size=16, color=WHITE)
        y_label.next_to(axes.y_axis, LEFT, buff=0.3)
        y_label.rotate(PI/2)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Create scatter points
        points = VGroup()
        for h, e in zip(hours, emergency_calls):
            point = Dot(
                axes.coords_to_point(h, e),
                radius=0.03,
                color=BLUE,
                fill_opacity=0.8
            )
            points.add(point)
        
        # Animate points appearing in waves
        self.play(*[FadeIn(point, scale=0.5) for point in points[:50]], run_time=1)
        self.play(*[FadeIn(point, scale=0.5) for point in points[50:100]], run_time=1)
        self.play(*[FadeIn(point, scale=0.5) for point in points[100:150]], run_time=1)
        self.play(*[FadeIn(point, scale=0.5) for point in points[150:]], run_time=1)
        
        # Highlight the non-linear pattern with annotations
        night_peak = Circle(radius=1, color=RED, stroke_width=3)
        night_peak.move_to(axes.coords_to_point(3, 0.7))
        
        morning_peak = Circle(radius=1, color=RED, stroke_width=3)
        morning_peak.move_to(axes.coords_to_point(8, 0.6))
        
        evening_peak = Circle(radius=0.8, color=RED, stroke_width=3)
        evening_peak.move_to(axes.coords_to_point(18, 0.45))
        
        night_label = Text("Night Peak", font_size=14, color=RED, weight=BOLD)
        night_label.next_to(night_peak, UP, buff=0.1)
        
        morning_label = Text("Morning Rush", font_size=14, color=RED, weight=BOLD)
        morning_label.next_to(morning_peak, UP, buff=0.1)
        
        evening_label = Text("Evening Peak", font_size=14, color=RED, weight=BOLD)
        evening_label.next_to(evening_peak, DOWN, buff=0.1)
        
        self.play(Create(night_peak), Write(night_label))
        self.play(Create(morning_peak), Write(morning_label))
        self.play(Create(evening_peak), Write(evening_label))
        
        # Pattern observation
        pattern_text = Text("Clear Non-Linear Pattern!", 
                          font_size=20, color=YELLOW, weight=BOLD)
        pattern_text.next_to(axes, DOWN, buff=0.5)
        self.play(Write(pattern_text))
        
        self.wait(2)
        
        # Store elements
        self.scatter_elements = VGroup(
            axes, x_label, y_label, points, 
            night_peak, morning_peak, evening_peak,
            night_label, morning_label, evening_label, pattern_text
        )
        self.scatter_title = scatter_title
        self.hours = hours
        self.emergency_calls = emergency_calls
        self.axes = axes
    
    def show_linear_glm_failure(self):
        """Demonstrate why linear GLM shows non-significant results"""
        glm_title = Text("Step 2: Linear GLM Attempt", 
                        font_size=28, color=ORANGE, weight=BOLD)
        glm_title.to_edge(UP, buff=0.5)
        self.play(ReplacementTransform(self.scatter_title, glm_title))
        
        # Fade out annotations but keep data
        self.play(FadeOut(VGroup(
            self.scatter_elements[4], self.scatter_elements[5], self.scatter_elements[6],  # circles
            self.scatter_elements[7], self.scatter_elements[8], self.scatter_elements[9],  # labels
            self.scatter_elements[10]  # pattern text
        )))
        
        # Show GLM equation
        glm_equation = Text("Y = β₀ + β₁ × HourOfCall + ε", 
                          font_size=20, color=WHITE)
        glm_equation.move_to(UP*2)
        self.play(Write(glm_equation))
        
        # Fit linear regression line (will be nearly flat)
        # Calculate linear regression
        x_mean = np.mean(self.hours)
        y_mean = np.mean(self.emergency_calls)
        
        numerator = np.sum((self.hours - x_mean) * (self.emergency_calls - y_mean))
        denominator = np.sum((self.hours - x_mean) ** 2)
        slope = numerator / denominator  # Will be close to 0 due to U-shape
        intercept = y_mean - slope * x_mean
        
        # Create regression line
        x_vals = np.linspace(0, 24, 100)
        y_vals = intercept + slope * x_vals
        
        line_points = [self.axes.coords_to_point(x, y) for x, y in zip(x_vals, y_vals)]
        regression_line = VMobject()
        regression_line.set_points_as_corners(line_points)
        regression_line.set_stroke(RED, width=4)
        
        self.play(Create(regression_line))
        
        # Show the poor results
        results_box = Rectangle(
            width=4, height=2.5,
            fill_color=BLACK, fill_opacity=0.8,
            stroke_color=WHITE, stroke_width=2
        ).move_to(RIGHT*4.5 + UP*1)
        
        results_text = VGroup(
            Text("GLM Results:", font_size=16, color=YELLOW, weight=BOLD),
            Text("β₁ = 0.001", font_size=14, color=WHITE),
            Text("p-value = 0.847", font_size=14, color=WHITE),
            Text("R² = 0.05", font_size=14, color=WHITE),
            Text("", font_size=4),  # spacer
            Text("Non-significant!", font_size=14, color=RED, weight=BOLD)
        ).arrange(DOWN, buff=0.1)
        results_text.move_to(results_box.get_center())
        
        self.play(Create(results_box), Write(results_text))
        
        # Add explanation
        explanation = VGroup(
            Text("Why GLM fails:", font_size=16, color=ORANGE, weight=BOLD),
            Text("• U-shaped pattern cancels out", font_size=12, color=WHITE),
            Text("• High values at both ends", font_size=12, color=WHITE),
            Text("• Linear fit = horizontal line", font_size=12, color=WHITE),
            Text("• Coefficient ≈ 0, high p-value", font_size=12, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        explanation.move_to(RIGHT*4.5 + DOWN*2)
        
        self.play(Write(explanation))
        
        # Highlight the mismatch with animation
        mismatch_arrows = VGroup()
        for i in range(0, len(self.hours), 20):  # Sample some points
            h, e = self.hours[i], self.emergency_calls[i]
            predicted = intercept + slope * h
            
            if abs(e - predicted) > 0.1:  # Only show significant mismatches
                arrow = Arrow(
                    self.axes.coords_to_point(h, predicted),
                    self.axes.coords_to_point(h, e),
                    color=YELLOW,
                    stroke_width=2,
                    max_tip_length_to_length_ratio=0.3
                )
                mismatch_arrows.add(arrow)
        
        self.play(*[GrowArrow(arrow) for arrow in mismatch_arrows], run_time=2)
        
        mismatch_text = Text("Large prediction errors!", 
                           font_size=14, color=YELLOW, weight=BOLD)
        mismatch_text.next_to(self.axes, DOWN, buff=0.3)
        self.play(Write(mismatch_text))
        
        self.wait(2)
        
        # Store elements
        self.glm_elements = VGroup(
            glm_equation, regression_line, results_box, results_text, 
            explanation, mismatch_arrows, mismatch_text
        )
        self.glm_title = glm_title
    
    def show_polynomial_solution(self):
        """Show how polynomial GLM captures the relationship"""
        poly_title = Text("Step 3: Polynomial GLM Solution", 
                         font_size=28, color=GREEN, weight=BOLD)
        poly_title.to_edge(UP, buff=0.5)
        self.play(ReplacementTransform(self.glm_title, poly_title))
        
        # Clear previous GLM results
        self.play(FadeOut(self.glm_elements))
        
        # Show polynomial equation
        poly_equation = Text("Y = β₀ + β₁×Hour + β₂×Hour² + β₃×Hour³ + ε", 
                           font_size=18, color=WHITE)
        poly_equation.move_to(UP*2)
        self.play(Write(poly_equation))
        
        # Create polynomial fit (approximate the true underlying function)
        x_vals = np.linspace(0, 24, 100)
        # Recreate the original function shape
        poly_y = (
            0.3 * np.exp(-((x_vals - 3) / 2) ** 2) +
            0.25 * np.exp(-((x_vals - 8) / 3) ** 2) +
            0.15 * np.exp(-((x_vals - 18) / 4) ** 2) +
            0.05
        )
        
        # Create polynomial curve
        poly_points = [self.axes.coords_to_point(x, y) for x, y in zip(x_vals, poly_y)]
        poly_curve = VMobject()
        poly_curve.set_points_smoothly(poly_points)
        poly_curve.set_stroke(GREEN, width=5)
        
        # Animate curve drawing
        self.play(Create(poly_curve), run_time=3)
        
        # Show improved results
        poly_results_box = Rectangle(
            width=4, height=2.5,
            fill_color=BLACK, fill_opacity=0.8,
            stroke_color=GREEN, stroke_width=2
        ).move_to(RIGHT*4.5 + UP*1)
        
        poly_results_text = VGroup(
            Text("Polynomial GLM:", font_size=16, color=GREEN, weight=BOLD),
            Text("β₁ = 0.12 (p < 0.001)", font_size=12, color=WHITE),
            Text("β₂ = -0.08 (p < 0.01)", font_size=12, color=WHITE),
            Text("β₃ = 0.03 (p < 0.05)", font_size=12, color=WHITE),
            Text("R² = 0.78", font_size=14, color=WHITE),
            Text("", font_size=4),  # spacer
            Text("Highly significant!", font_size=14, color=GREEN, weight=BOLD)
        ).arrange(DOWN, buff=0.08)
        poly_results_text.move_to(poly_results_box.get_center())
        
        self.play(Create(poly_results_box), Write(poly_results_text))
        
        # Show model fit quality
        fit_quality = VGroup(
            Text("Perfect capture of:", font_size=16, color=GREEN, weight=BOLD),
            Text("• Night emergency peak", font_size=12, color=WHITE),
            Text("• Morning rush pattern", font_size=12, color=WHITE),
            Text("• Evening increase", font_size=12, color=WHITE),
            Text("• Low midday rates", font_size=12, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        fit_quality.move_to(RIGHT*4.5 + DOWN*2)
        
        self.play(Write(fit_quality))
        
        # Highlight good fit with small residual arrows
        good_fit_arrows = VGroup()
        for i in range(0, len(self.hours), 30):  # Sample fewer points
            h, e = self.hours[i], self.emergency_calls[i]
            
            # Find predicted value from polynomial
            predicted_poly = (
                0.3 * np.exp(-((h - 3) / 2) ** 2) +
                0.25 * np.exp(-((h - 8) / 3) ** 2) +
                0.15 * np.exp(-((h - 18) / 4) ** 2) +
                0.05
            )
            
            if abs(e - predicted_poly) < 0.15:  # Show small residuals
                arrow = Arrow(
                    self.axes.coords_to_point(h, predicted_poly),
                    self.axes.coords_to_point(h, e),
                    color=GREEN,
                    stroke_width=2,
                    max_tip_length_to_length_ratio=0.4
                )
                good_fit_arrows.add(arrow)
        
        self.play(*[GrowArrow(arrow) for arrow in good_fit_arrows], run_time=2)
        
        small_errors_text = Text("Small prediction errors!", 
                                font_size=14, color=GREEN, weight=BOLD)
        small_errors_text.next_to(self.axes, DOWN, buff=0.3)
        self.play(Write(small_errors_text))
        
        self.wait(2)
        
        # Store elements
        self.poly_elements = VGroup(
            poly_equation, poly_curve, poly_results_box, poly_results_text,
            fit_quality, good_fit_arrows, small_errors_text
        )
        self.poly_title = poly_title
    
    def show_model_comparison(self):
        """Show side-by-side comparison of both approaches"""
        comparison_title = Text("Step 4: Model Comparison", 
                              font_size=28, color=PURPLE, weight=BOLD)
        comparison_title.to_edge(UP, buff=0.5)
        self.play(ReplacementTransform(self.poly_title, comparison_title))
        
        # Clear detailed elements but keep core plots
        self.play(FadeOut(self.poly_elements))
        
        # Create comparison table
        table_box = Rectangle(
            width=10, height=4,
            fill_color=BLACK, fill_opacity=0.9,
            stroke_color=WHITE, stroke_width=2
        ).move_to(DOWN*2)
        
        # Table headers
        headers = VGroup(
            Text("Model", font_size=16, color=WHITE, weight=BOLD),
            Text("Linear GLM", font_size=16, color=RED, weight=BOLD),
            Text("Polynomial GLM", font_size=16, color=GREEN, weight=BOLD)
        )
        headers[0].move_to(table_box.get_left() + RIGHT*1.5 + UP*1.3)
        headers[1].move_to(table_box.get_center() + LEFT*2 + UP*1.3)
        headers[2].move_to(table_box.get_center() + RIGHT*2 + UP*1.3)
        
        # Table content
        metrics = ["R²", "Hour Coeff", "p-value", "Interpretation"]
        linear_vals = ["0.05", "≈ 0.001", "> 0.05", "Non-significant"]
        poly_vals = ["0.78", "Multiple", "< 0.001", "Highly significant"]
        
        table_content = VGroup()
        for i, (metric, lin_val, poly_val) in enumerate(zip(metrics, linear_vals, poly_vals)):
            y_pos = UP*0.7 - DOWN*i*0.5
            
            metric_text = Text(metric, font_size=14, color=WHITE, weight=BOLD)
            metric_text.move_to(table_box.get_left() + RIGHT*1.5 + y_pos)
            
            lin_text = Text(lin_val, font_size=14, color=RED)
            lin_text.move_to(table_box.get_center() + LEFT*2 + y_pos)
            
            poly_text = Text(poly_val, font_size=14, color=GREEN)
            poly_text.move_to(table_box.get_center() + RIGHT*2 + y_pos)
            
            table_content.add(VGroup(metric_text, lin_text, poly_text))
        
        self.play(Create(table_box))
        self.play(*[Write(header) for header in headers])
        
        for row in table_content:
            self.play(*[Write(text) for text in row], run_time=0.8)
        
        # Add dividing lines
        v_line1 = Line(
            table_box.get_top() + LEFT*1,
            table_box.get_bottom() + LEFT*1,
            stroke_color=WHITE, stroke_width=1
        )
        v_line2 = Line(
            table_box.get_top() + RIGHT*1,
            table_box.get_bottom() + RIGHT*1,
            stroke_color=WHITE, stroke_width=1
        )
        
        self.play(Create(v_line1), Create(v_line2))
        
        self.wait(2)
        
        # Store elements
        self.comparison_elements = VGroup(
            table_box, headers, table_content, v_line1, v_line2
        )
        self.comparison_title = comparison_title
    
    def show_final_insights(self):
        """Show key insights and takeaways"""
        insights_title = Text("Key Insights", 
                            font_size=32, color=YELLOW, weight=BOLD)
        insights_title.to_edge(UP, buff=0.5)
        self.play(ReplacementTransform(self.comparison_title, insights_title))
        
        # Clear comparison
        self.play(FadeOut(self.comparison_elements))
        self.play(FadeOut(VGroup(self.scatter_elements[0:4])))  # Keep just axes and points
        
        # Main insight
        main_insight = Text(
            "Strong Relationship ≠ Significant Linear Coefficient",
            font_size=24, color=RED, weight=BOLD
        )
        main_insight.move_to(UP*2)
        self.play(Write(main_insight))
        
        # Key points
        insights = VGroup(
            Text("1. Linear GLM assumes straight-line relationships", 
                 font_size=16, color=WHITE),
            Text("2. Non-linear patterns can appear 'non-significant'", 
                 font_size=16, color=WHITE),
            Text("3. Always visualize your data first!", 
                 font_size=16, color=YELLOW, weight=BOLD),
            Text("4. Consider polynomial/spline terms for time variables", 
                 font_size=16, color=WHITE),
            Text("5. R² improvement indicates model specification issues", 
                 font_size=16, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        insights.move_to(UP*0.5)
        
        for insight in insights:
            self.play(Write(insight), run_time=1)
        
        # Practical advice
        advice_box = Rectangle(
            width=8, height=2,
            fill_color=BLUE, fill_opacity=0.2,
            stroke_color=BLUE, stroke_width=2
        ).move_to(DOWN*2.5)
        
        advice_text = VGroup(
            Text("Practical Advice:", font_size=18, color=BLUE, weight=BOLD),
            Text("Before concluding 'no relationship exists',", font_size=14, color=WHITE),
            Text("explore non-linear transformations!", font_size=14, color=WHITE)
        ).arrange(DOWN, buff=0.2)
        advice_text.move_to(advice_box.get_center())
        
        self.play(Create(advice_box), Write(advice_text))
        
        self.wait(3)

if __name__ == "__main__":
    # For testing
    pass