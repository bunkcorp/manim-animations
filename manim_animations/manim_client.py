import asyncio
from fastmcp import Client

MANIM_CODE = """from manim import *
import numpy as np

class ElasticNetAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Part 1: Bias-Variance Decomposition
        self.next_section("BiasVarianceDecomposition", skip_animations=False)
        self.show_bias_variance_decomposition()

        # Part 2: Unregularized Model
        self.next_section("UnregularizedModel", skip_animations=False)
        self.show_unregularized_model()

        # Part 3: Elastic Net Regularization
        self.next_section("ElasticNetEffect", skip_animations=False)
        self.show_elastic_net_effect()

        # Part 4: Quantitative Comparison
        self.next_section("QuantitativeComparison", skip_animations=False)
        self.show_quantitative_comparison()

        # Part 5: Regularization Path
        self.next_section("RegularizationPath", skip_animations=False)
        self.show_regularization_path()
        
        # Summary
        self.next_section("Summary", skip_animations=False)
        self.show_summary()

    def show_bias_variance_decomposition(self):
        title = Text("Bias-Variance Tradeoff", font_size=48, color=YELLOW).to_edge(UP)
        formula = MathTex(
            r"E[(y - \\hat{y})^2]", r"=", r"\\text{Bias}^2", r"+", r"\\text{Variance}", r"+", r"\\text{Irreducible Error}",
            font_size=36
        ).next_to(title, DOWN)
        
        formula.set_color_by_tex("Bias", RED)
        formula.set_color_by_tex("Variance", BLUE)
        formula.set_color_by_tex("Irreducible", GRAY)

        self.play(Write(title))
        self.play(Write(formula))
        self.wait(2)

        # Seesaw animation
        seesaw = VGroup(
            Line(LEFT * 3, RIGHT * 3, color=WHITE),
            Triangle(color=ORANGE, fill_opacity=1).scale(0.5).shift(DOWN * 0.25)
        ).next_to(formula, DOWN, buff=1)
        
        bias_label = Text("Bias", color=RED).next_to(seesaw[0].get_start(), DOWN)
        variance_label = Text("Variance", color=BLUE).next_to(seesaw[0].get_end(), DOWN)
        
        self.play(Create(seesaw), Write(bias_label), Write(variance_label))
        self.play(seesaw[0].animate.rotate(0.2, about_point=seesaw.get_center()))
        self.wait(0.5)
        self.play(seesaw[0].animate.rotate(-0.4, about_point=seesaw.get_center()))
        self.wait(0.5)
        self.play(seesaw[0].animate.rotate(0.2, about_point=seesaw.get_center()))
        self.wait(1)
        
        self.play(FadeOut(title, formula, seesaw, bias_label, variance_label))

    def show_unregularized_model(self):
        title = Text("Unregularized Model", font_size=36, color=WHITE).to_edge(UP)
        subtitle = Text("Low Bias, High Variance", font_size=28).next_to(title, DOWN)
        subtitle[0][0:8].set_color(RED)
        subtitle[0][10:].set_color(BLUE)
        
        self.play(Write(title), Write(subtitle))

        # Setup axes and data
        axes = Axes(x_range=[0, 10, 1], y_range=[-2, 2, 1], x_length=10, y_length=5).add_coordinates()
        
        # True function
        def true_func(x):
            return np.sin(x * 0.8)
        
        true_curve = axes.plot(true_func, color=GREEN)
        
        # Generate data points
        np.random.seed(42)
        x_data = np.linspace(1, 9, 20)
        y_data = true_func(x_data) + np.random.normal(0, 0.5, len(x_data))
        dots = VGroup(*[Dot(axes.c2p(x, y), color=LIGHT_GRAY) for x, y in zip(x_data, y_data)])

        self.play(Create(axes), Create(true_curve), FadeIn(dots))
        self.wait(1)

        # Fit multiple high-degree polynomial models (simulating bootstrap)
        fitted_curves = VGroup()
        for i in range(5):
            sample_indices = np.random.choice(len(x_data), len(x_data), replace=True)
            x_sample = x_data[sample_indices]
            y_sample = y_data[sample_indices]
            
            poly_fit = np.poly1d(np.polyfit(x_sample, y_sample, 9))
            
            curve = axes.plot(lambda x: poly_fit(x), color=BLUE, stroke_width=2, stroke_opacity=0.7)
            fitted_curves.add(curve)

        self.play(Create(fitted_curves, lag_ratio=0.5))
        
        variance_text = Text("Many different prediction curves\n(High Variance)", font_size=24, color=BLUE).to_corner(UR)
        self.play(Write(variance_text))
        self.wait(2)
        
        self.play(FadeOut(title, subtitle, axes, true_curve, dots, fitted_curves, variance_text))

    def show_elastic_net_effect(self):
        title = Text("Elastic Net Regularization", font_size=36, color=WHITE).to_edge(UP)
        subtitle = Text("Higher Bias, Lower Variance", font_size=28).next_to(title, DOWN)
        subtitle[0][0:11].set_color(RED)
        subtitle[0][13:].set_color(BLUE)
        
        self.play(Write(title), Write(subtitle))

        axes = Axes(x_range=[0, 10, 1], y_range=[-2, 2, 1], x_length=10, y_length=5).add_coordinates()
        
        def true_func(x):
            return np.sin(x * 0.8)
            
        np.random.seed(42)
        x_data = np.linspace(1, 9, 20)
        y_data = true_func(x_data) + np.random.normal(0, 0.5, len(x_data))
        dots = VGroup(*[Dot(axes.c2p(x, y), color=LIGHT_GRAY) for x, y in zip(x_data, y_data)])

        self.play(Create(axes), FadeIn(dots))

        # Animate from unregularized to regularized
        regularized_curves = VGroup()
        unregularized_curves = VGroup()

        for i in range(5):
            sample_indices = np.random.choice(len(x_data), len(x_data), replace=True)
            x_sample = x_data[sample_indices]
            y_sample = y_data[sample_indices]
            
            # Unregularized
            poly_fit_unreg = np.poly1d(np.polyfit(x_sample, y_sample, 9))
            curve_unreg = axes.plot(lambda x: poly_fit_unreg(x), color=BLUE, stroke_width=2, stroke_opacity=0.7)
            unregularized_curves.add(curve_unreg)

            # Regularized (simulated by fitting a lower-degree polynomial)
            poly_fit_reg = np.poly1d(np.polyfit(x_sample, y_sample, 3))
            curve_reg = axes.plot(lambda x: poly_fit_reg(x), color=RED, stroke_width=2, stroke_opacity=0.7)
            regularized_curves.add(curve_reg)

        self.play(Create(unregularized_curves))
        self.wait(1)
        
        shrink_text = Text("Coefficients pulled toward zero", font_size=24).to_corner(UR)
        self.play(Write(shrink_text))
        self.play(Transform(unregularized_curves, regularized_curves))
        
        variance_text = Text("Predictions are more similar\n(Lower Variance)", font_size=24, color=BLUE).move_to(shrink_text)
        self.play(FadeOut(shrink_text), Write(variance_text))
        self.wait(2)

        self.play(FadeOut(title, subtitle, axes, dots, unregularized_curves, variance_text))

    def show_quantitative_comparison(self):
        title = Text("Quantitative Comparison", font_size=36, color=WHITE).to_edge(UP)
        self.play(Write(title))

        # Data for charts
        unreg_data = [0.1, 0.8]
        elastic_data = [0.3, 0.2] 
        
        # Unregularized Chart
        chart_unreg = BarChart(
            values=unreg_data,
            bar_names=["Bias²", "Variance"],
            y_range=[0, 1, 0.2],
            bar_colors=[RED, BLUE],
            y_length=5,
            x_length=4,
        ).to_edge(LEFT, buff=1)
        
        unreg_title = Text("Unregularized", font_size=24).next_to(chart_unreg, UP)
        total_unreg = Text(f"Total Error = {sum(unreg_data):.1f}", font_size=20).next_to(chart_unreg, DOWN)

        # Elastic Net Chart
        chart_elastic = BarChart(
            values=elastic_data,
            bar_names=["Bias²", "Variance"],
            y_range=[0, 1, 0.2],
            bar_colors=[RED, BLUE],
            y_length=5,
            x_length=4,
        ).to_edge(RIGHT, buff=1)
        
        elastic_title = Text("Elastic Net", font_size=24).next_to(chart_elastic, UP)
        total_elastic = Text(f"Total Error = {sum(elastic_data):.1f}", font_size=20).next_to(chart_elastic, DOWN)

        self.play(
            Write(unreg_title), Create(chart_unreg), Write(total_unreg),
            Write(elastic_title), Create(chart_elastic), Write(total_elastic)
        )
        self.wait(2)

        # Show net improvement
        improvement = ((sum(unreg_data) - sum(elastic_data)) / sum(unreg_data)) * 100
        improvement_text = Text(f"Net Improvement: {improvement:.0f}% reduction in error", font_size=28, color=GREEN)
        improvement_text.next_to(VGroup(chart_unreg, chart_elastic), DOWN, buff=1)
        
        self.play(Write(improvement_text))
        self.wait(2)
        
        self.play(FadeOut(title, unreg_title, chart_unreg, total_unreg, elastic_title, chart_elastic, total_elastic, improvement_text))

    def show_regularization_path(self):
        title = Text("Finding the Sweet Spot", font_size=36, color=WHITE).to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[0, 10, 1], y_range=[0, 1.2, 0.2],
            x_length=10, y_length=5,
            axis_config={"color": GRAY},
            x_axis_config={"include_numbers": True}
        ).add_coordinates()
        
        x_label = axes.get_x_axis_label(Tex("Regularization Strength \\lambda"), edge=DOWN, direction=DOWN)
        y_label = axes.get_y_axis_label(Tex("Error"), edge=LEFT, direction=LEFT)
        
        self.play(Create(axes), Write(x_label), Write(y_label))

        # Define curves
        x_vals = np.linspace(0.1, 10, 100)
        bias_sq = 0.05 + 0.3 * (1 - np.exp(-x_vals/3))
        variance = 0.8 * np.exp(-x_vals/2) + 0.1
        total_error = bias_sq + variance

        bias_curve = axes.plot_line_graph(x_vals, bias_sq, line_color=RED)
        var_curve = axes.plot_line_graph(x_vals, variance, line_color=BLUE)
        total_curve = axes.plot_line_graph(x_vals, total_error, line_color=GREEN)

        bias_label = Text("Bias²", font_size=24, color=RED).next_to(bias_curve.get_end(), UR)
        var_label = Text("Variance", font_size=24, color=BLUE).next_to(var_curve.get_start(), UR)
        total_label = Text("Total Error", font_size=24, color=GREEN).next_to(total_curve.get_end(), DR)

        self.play(Create(bias_curve), Write(bias_label))
        self.play(Create(var_curve), Write(var_label))
        self.play(Create(total_curve), Write(total_label))
        self.wait(1)

        # Highlight optimal lambda
        optimal_idx = np.argmin(total_error)
        optimal_lambda = x_vals[optimal_idx]
        optimal_point = Dot(axes.c2p(optimal_lambda, total_error[optimal_idx]), color=YELLOW)
        arrow = Arrow(optimal_point.get_center() + UP*1.5, optimal_point.get_center(), color=YELLOW)
        sweet_spot_text = Text("Sweet Spot", font_size=24, color=YELLOW).next_to(arrow, UP)

        self.play(GrowArrow(arrow), Write(sweet_spot_text), FadeIn(optimal_point))
        self.wait(2)
        
        self.play(FadeOut(title, axes, x_label, y_label, bias_curve, var_curve, total_curve, bias_label, var_label, total_label, arrow, sweet_spot_text, optimal_point))

    def show_summary(self):
        title = Text("Key Takeaways", font_size=42, color=YELLOW).to_edge(UP)
        self.play(Write(title))

        insights = VGroup(
            Text("• Regularization trades a small increase in bias...", color=WHITE, font_size=28),
            Text("  ...for a large decrease in variance.", color=BLUE, font_size=28),
            Text("• This leads to a lower overall prediction error.", color=GREEN, font_size=28),
            Text("• The optimal λ minimizes the bias-variance tradeoff.", color=YELLOW, font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(title, DOWN, buff=1)

        self.play(FadeIn(insights, lag_ratio=0.5, shift=UP))
        self.wait(4)
        self.play(FadeOut(*self.mobjects))
"""

async def main():
    server_command = "/Users/kevinwoods/Desktop/buddhist-stone-app/manim-mcp-server/src/manim_server.py"
    async with Client(server_command) as client:
        result = await client.call_tool("execute_manim_code", {"manim_code": MANIM_CODE})
        print(result)

if __name__ == "__main__":
    asyncio.run(main())