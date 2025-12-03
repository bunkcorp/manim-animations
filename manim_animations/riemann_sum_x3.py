from manim import *
import numpy as np

class RiemannSumX3(Scene):
    def construct(self):
        # Configuration
        x_min, x_max = 0, 2
        n_rectangles_start = 4
        n_rectangles_end = 20
        
        # Create axes
        axes = Axes(
            x_range=[0, 2.5, 0.5],
            y_range=[0, 9, 1],
            x_length=10,
            y_length=6,
            axis_config={
                "color": BLUE,
                "include_numbers": True,
                "font_size": 24,
            },
            tips=False,
        ).to_edge(LEFT).shift(RIGHT * 0.5)
        
        # Labels
        x_label = axes.get_x_axis_label("x", direction=DOWN)
        y_label = axes.get_y_axis_label("y", direction=LEFT)
        
        # Function: f(x) = x^3
        def f(x):
            return x ** 3
        
        # Create the curve
        curve = axes.plot(f, x_range=[0, 2], color=GREEN, stroke_width=3)
        curve_label = MathTex("f(x) = x^3", color=GREEN, font_size=36).to_corner(UR)
        
        # Title
        title = Text("Riemann Sum for ∫x³ dx", font_size=42, color=YELLOW).to_edge(UP)
        
        self.play(
            Create(axes),
            Write(x_label),
            Write(y_label),
            Write(title)
        )
        self.wait(0.5)
        
        self.play(Create(curve), Write(curve_label))
        self.wait(1)
        
        # Animation: Show increasing number of rectangles
        for n in [n_rectangles_start, 8, 12, n_rectangles_end]:
            # Clear previous rectangles
            if n != n_rectangles_start:
                self.play(FadeOut(rectangles_group), FadeOut(sum_text))
            
            # Calculate rectangle width
            dx = (x_max - x_min) / n
            
            # Create rectangles (right endpoint method)
            rectangles = VGroup()
            rectangles_group = VGroup()
            
            for i in range(n):
                x_left = x_min + i * dx
                x_right = x_left + dx
                x_mid = (x_left + x_right) / 2
                
                # Height at right endpoint
                height = f(x_right)
                
                # Create rectangle
                rect = Rectangle(
                    width=axes.x_axis.unit_size * dx,
                    height=axes.y_axis.unit_size * height,
                    color=BLUE,
                    fill_opacity=0.5,
                    stroke_width=2,
                )
                
                # Position rectangle
                rect.move_to(
                    axes.coords_to_point(x_mid, height / 2)
                )
                
                rectangles.add(rect)
            
            rectangles_group.add(rectangles)
            
            # Calculate Riemann sum
            riemann_sum = sum([f(x_min + (i + 1) * dx) * dx for i in range(n)])
            exact_integral = (x_max ** 4) / 4 - (x_min ** 4) / 4  # ∫x³ dx = x⁴/4
            
            # Display Riemann sum
            sum_text = VGroup(
                MathTex(
                    f"n = {n}",
                    font_size=32,
                    color=WHITE
                ),
                MathTex(
                    f"R_n = {riemann_sum:.4f}",
                    font_size=32,
                    color=BLUE
                ),
                MathTex(
                    f"\\int_0^2 x^3 \\, dx = {exact_integral:.4f}",
                    font_size=32,
                    color=GREEN
                ),
                MathTex(
                    f"Error = {abs(riemann_sum - exact_integral):.4f}",
                    font_size=28,
                    color=RED
                )
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_corner(DR, buff=0.5)
            
            # Animate rectangles appearing
            self.play(
                *[Create(rect) for rect in rectangles],
                Write(sum_text),
                run_time=2
            )
            self.wait(1)
        
        # Show convergence
        convergence_text = Text(
            "As n → ∞, R_n → ∫x³ dx = 4.0",
            font_size=36,
            color=YELLOW
        ).to_edge(DOWN, buff=0.5)
        
        self.play(Write(convergence_text))
        self.wait(2)
        
        # Highlight the exact area
        area_under_curve = axes.get_area(
            curve,
            x_range=[0, 2],
            color=GREEN,
            opacity=0.3
        )
        
        self.play(
            FadeOut(rectangles_group),
            Create(area_under_curve),
            run_time=2
        )
        
        final_text = MathTex(
            "\\int_0^2 x^3 \\, dx = \\frac{x^4}{4} \\Big|_0^2 = \\frac{16}{4} - 0 = 4",
            font_size=40,
            color=GREEN
        ).to_edge(DOWN, buff=0.3)
        
        self.play(
            Transform(convergence_text, final_text),
            run_time=2
        )
        self.wait(3)

