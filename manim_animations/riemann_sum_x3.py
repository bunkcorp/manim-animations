from manim import *
import numpy as np

class RiemannSumX3(Scene):
    def construct(self):
        # Configuration - more steps to show gradual refinement
        x_min, x_max = 0, 2
        n_values = [4, 8, 16, 32, 64]  # More steps showing gradual refinement
        
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
        
        # Title - emphasize parameter tuning
        title = Text("Refining Parameters: ∫x³ dx", font_size=38, color=YELLOW).to_edge(UP, buff=0.3)
        subtitle = Text("Smaller units → Better approximation", font_size=24, color=GRAY).next_to(title, DOWN, buff=0.2)
        
        self.play(
            Create(axes),
            Write(x_label),
            Write(y_label),
            Write(title),
            Write(subtitle)
        )
        self.wait(0.5)
        
        self.play(Create(curve), Write(curve_label))
        self.wait(1)
        
        # Store previous rectangles for smooth transition
        prev_rectangles = None
        prev_sum_text = None
        
        # Animation: Show rectangles shrinking as we refine
        for idx, n in enumerate(n_values):
            # Calculate rectangle width (gets smaller each iteration)
            dx = (x_max - x_min) / n
            
            # Create rectangles (right endpoint method)
            rectangles = VGroup()
            
            for i in range(n):
                x_left = x_min + i * dx
                x_right = x_left + dx
                x_mid = (x_left + x_right) / 2
                
                # Height at right endpoint
                height = f(x_right)
                
                # Create rectangle - smaller stroke for smaller rectangles
                stroke_width = max(1, 3 - idx * 0.4)
                rect = Rectangle(
                    width=axes.x_axis.unit_size * dx,
                    height=axes.y_axis.unit_size * height,
                    color=BLUE,
                    fill_opacity=0.6 - idx * 0.08,  # Slightly more transparent as they shrink
                    stroke_width=stroke_width,
                )
                
                # Position rectangle
                rect.move_to(
                    axes.coords_to_point(x_mid, height / 2)
                )
                
                rectangles.add(rect)
            
            # Calculate Riemann sum
            riemann_sum = sum([f(x_min + (i + 1) * dx) * dx for i in range(n)])
            exact_integral = (x_max ** 4) / 4 - (x_min ** 4) / 4  # ∫x³ dx = x⁴/4
            error = abs(riemann_sum - exact_integral)
            
            # Display information with emphasis on refinement
            unit_size_text = f"Unit size: {dx:.4f}" if dx >= 0.01 else f"Unit size: {dx:.6f}"
            
            sum_text = VGroup(
                Text(
                    f"Refinement Step {idx + 1}",
                    font_size=26,
                    color=YELLOW,
                    weight=BOLD
                ),
                Text(
                    f"Units: {n}",
                    font_size=22,
                    color=WHITE
                ),
                Text(
                    unit_size_text,
                    font_size=20,
                    color=BLUE
                ),
                MathTex(
                    f"\\text{{Approx}} = {riemann_sum:.6f}",
                    font_size=24,
                    color=BLUE
                ),
                MathTex(
                    f"\\text{{Exact}} = {exact_integral:.6f}",
                    font_size=24,
                    color=GREEN
                ),
                MathTex(
                    f"\\text{{Error}} = {error:.6f}",
                    font_size=20,
                    color=RED
                )
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(axes, RIGHT, buff=1.0).align_to(axes, DOWN).shift(UP * 2.0)
            
            # Smooth transition: shrink previous rectangles into new ones
            if prev_rectangles is not None:
                # Fade out old text first, then transform rectangles and show new text
                self.play(
                    FadeOut(prev_sum_text),
                    run_time=0.3
                )
                self.play(
                    Transform(prev_rectangles, rectangles, run_time=1.5),
                    FadeIn(sum_text),
                    run_time=1.5
                )
            else:
                # First iteration - create rectangles
                self.play(
                    *[Create(rect) for rect in rectangles],
                    Write(sum_text),
                    run_time=2
                )
            
            # Highlight that rectangles are getting smaller
            if idx < len(n_values) - 1:
                shrink_indicator = Text(
                    "↓ Refining parameters...",
                    font_size=22,
                    color=YELLOW
                ).next_to(sum_text, DOWN, buff=0.5)
                self.play(Write(shrink_indicator), run_time=0.8)
                self.play(FadeOut(shrink_indicator), run_time=0.5)
            
            self.wait(1)
            
            # Store for next iteration
            prev_rectangles = rectangles
            prev_sum_text = sum_text
        
        # Show convergence message
        convergence_text = VGroup(
            Text(
                "As units shrink → Parameters refined",
                font_size=30,
                color=YELLOW,
                weight=BOLD
            ),
            MathTex(
                "\\text{Approx} \\rightarrow \\int_0^2 x^3 \\, dx = 4.0",
                font_size=32,
                color=GREEN
            )
        ).arrange(DOWN, buff=0.4).to_edge(DOWN, buff=0.6)
        
        self.play(
            Write(convergence_text),
            run_time=2
        )
        self.wait(2)
        
        # Highlight the exact area - show what we're converging to
        area_under_curve = axes.get_area(
            curve,
            x_range=[0, 2],
            color=GREEN,
            opacity=0.3
        )
        
        self.play(
            FadeOut(prev_rectangles),
            Create(area_under_curve),
            run_time=2
        )
        
        final_text = VGroup(
            Text(
                "Perfect refinement achieved!",
                font_size=30,
                color=RED_D,
                weight=BOLD
            ),
            MathTex(
                "\\int_0^2 x^3 \\, dx = \\frac{x^4}{4} \\Big|_0^2 = \\frac{16}{4} - 0 = 4",
                font_size=32,
                color=RED_D
            )
        ).arrange(DOWN, buff=0.4).next_to(axes, RIGHT, buff=1.0).align_to(axes, UP).shift(DOWN * 0.5)
        
        self.play(
            Transform(convergence_text, final_text),
            run_time=2
        )
        self.wait(3)

