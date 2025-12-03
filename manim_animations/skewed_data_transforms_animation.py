#!/usr/bin/env python3
"""
Skewed Data Transformations Animation
Visual demonstration of transforming heavily skewed data with outliers
Focus on movement and visual transformation
"""

from manim import *
import numpy as np

class SkewedDataTransformsAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Show original skewed data
        self.show_original_data()
        
        # Show dummy variable transformation
        self.show_dummy_transformation()
        
        # Show log transformation
        self.show_log_transformation()
        
        # Show square root transformation
        self.show_sqrt_transformation()
        
        # Show comparison of all methods
        self.show_final_comparison()
    
    def generate_skewed_data(self, n=200):
        """Generate heavily skewed data with outliers"""
        np.random.seed(42)
        # Base exponential distribution
        base_data = np.random.exponential(scale=2, size=int(n*0.8))
        # Add extreme outliers
        outliers = np.random.exponential(scale=20, size=int(n*0.2)) + 15
        return np.concatenate([base_data, outliers])
    
    def show_original_data(self):
        """Show the original heavily skewed data"""
        title = Text("Heavily Skewed Data with Outliers", font_size=32, color=RED, weight=BOLD).to_edge(UP)
        self.play(Write(title))
        
        # Generate data
        data = self.generate_skewed_data()
        
        # Create histogram
        axes = Axes(
            x_range=[0, 50, 10],
            y_range=[0, 80, 20],
            x_length=10,
            y_length=5,
            axis_config={"stroke_color": WHITE, "stroke_width": 2}
        ).move_to(DOWN*0.5)
        
        # Create histogram bars
        bins = np.histogram(data, bins=20, range=(0, 50))
        bars = VGroup()
        
        for i, (count, left_edge) in enumerate(zip(bins[0], bins[1][:-1])):
            if count > 0:
                bar = Rectangle(
                    width=axes.x_axis.unit_size * 2.5,
                    height=axes.y_axis.unit_size * count / 4,
                    fill_color=RED,
                    fill_opacity=0.7,
                    stroke_color=WHITE,
                    stroke_width=1
                ).move_to(axes.coords_to_point(left_edge + 1.25, count/8))
                bars.add(bar)
        
        self.play(Create(axes))
        
        # Animate bars growing
        for bar in bars:
            self.play(GrowFromEdge(bar, DOWN), run_time=0.1)
        
        # Show problem indicators
        skew_arrow = CurvedArrow(
            axes.coords_to_point(10, 40),
            axes.coords_to_point(35, 20),
            angle=-PI/4,
            color=YELLOW
        )
        skew_text = Text("Heavy Right Skew", font_size=16, color=YELLOW, weight=BOLD)
        skew_text.next_to(skew_arrow.get_start(), UP)
        
        outlier_dots = VGroup()
        outlier_positions = [40, 42, 45, 48]
        for pos in outlier_positions:
            dot = Dot(axes.coords_to_point(pos, 5), color=ORANGE, radius=0.1)
            outlier_dots.add(dot)
        
        outlier_text = Text("Outliers", font_size=16, color=ORANGE, weight=BOLD)
        outlier_text.move_to(axes.coords_to_point(45, 15))
        
        self.play(Create(skew_arrow), Write(skew_text))
        self.play(*[FadeIn(dot, scale=2) for dot in outlier_dots], Write(outlier_text))
        
        self.wait(2)
        
        # Store elements
        self.original_data = data
        self.original_elements = VGroup(axes, bars, skew_arrow, skew_text, outlier_dots, outlier_text)
        self.title = title
    
    def show_dummy_transformation(self):
        """Show dummy variable transformation"""
        dummy_title = Text("Transformation 1: Dummy Variable", font_size=28, color=BLUE, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.title, dummy_title))
        
        # Show threshold selection
        threshold = 10
        threshold_line = DashedLine(
            self.original_elements[0].coords_to_point(threshold, 0),
            self.original_elements[0].coords_to_point(threshold, 80),
            color=GREEN,
            stroke_width=4
        )
        
        threshold_text = Text(f"Threshold = {threshold}", font_size=16, color=GREEN, weight=BOLD)
        threshold_text.next_to(threshold_line, UP, buff=0.2)
        
        self.play(Create(threshold_line), Write(threshold_text))
        self.wait(1)
        
        # Transform bars - color coding
        below_bars = VGroup()
        above_bars = VGroup()
        
        bins = np.histogram(self.original_data, bins=20, range=(0, 50))
        for i, (count, left_edge) in enumerate(zip(bins[0], bins[1][:-1])):
            if count > 0:
                bar_center = left_edge + 1.25
                if bar_center < threshold:
                    below_bars.add(self.original_elements[1][len(below_bars)])
                else:
                    above_bars.add(self.original_elements[1][len(below_bars) + len(above_bars)])
        
        # Animate color change
        if len(below_bars) > 0:
            self.play(below_bars.animate.set_fill(BLUE, opacity=0.7))
        if len(above_bars) > 0:
            self.play(above_bars.animate.set_fill(ORANGE, opacity=0.7))
        
        # Create dummy variable visualization
        dummy_axes = Axes(
            x_range=[0, 1, 1],
            y_range=[0, 150, 50],
            x_length=4,
            y_length=4,
            axis_config={"stroke_color": WHITE, "stroke_width": 2}
        ).move_to(RIGHT*4 + DOWN*1)
        
        # Count values
        below_count = np.sum(self.original_data < threshold)
        above_count = np.sum(self.original_data >= threshold)
        
        dummy_bar_0 = Rectangle(
            width=dummy_axes.x_axis.unit_size * 0.8,
            height=dummy_axes.y_axis.unit_size * below_count / 50,
            fill_color=BLUE,
            fill_opacity=0.7,
            stroke_color=WHITE
        ).move_to(dummy_axes.coords_to_point(0, below_count/100))
        
        dummy_bar_1 = Rectangle(
            width=dummy_axes.x_axis.unit_size * 0.8,
            height=dummy_axes.y_axis.unit_size * above_count / 50,
            fill_color=ORANGE,
            fill_opacity=0.7,
            stroke_color=WHITE
        ).move_to(dummy_axes.coords_to_point(1, above_count/100))
        
        label_0 = Text("0 (Below)", font_size=14, color=WHITE).next_to(dummy_bar_0, DOWN)
        label_1 = Text("1 (Above)", font_size=14, color=WHITE).next_to(dummy_bar_1, DOWN)
        
        self.play(Create(dummy_axes))
        self.play(GrowFromEdge(dummy_bar_0, DOWN), GrowFromEdge(dummy_bar_1, DOWN))
        self.play(Write(label_0), Write(label_1))
        
        # Add result text
        result_text = Text("Binary Variable Created!", font_size=16, color=GREEN, weight=BOLD)
        result_text.next_to(dummy_axes, UP, buff=0.5)
        self.play(Write(result_text))
        
        self.wait(2)
        self.play(FadeOut(VGroup(
            threshold_line, threshold_text, dummy_axes, dummy_bar_0, dummy_bar_1, 
            label_0, label_1, result_text
        )))
        self.dummy_title = dummy_title
    
    def show_log_transformation(self):
        """Show log transformation with visual movement"""
        log_title = Text("Transformation 2: Log Transform", font_size=28, color=PURPLE, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.dummy_title, log_title))
        
        # Reset bar colors
        self.play(self.original_elements[1].animate.set_fill(RED, opacity=0.7))
        
        # Show transformation happening
        transform_text = Text("y → log(y + 1)", font_size=24, color=YELLOW, weight=BOLD)
        transform_text.move_to(UP*1.5)
        self.play(Write(transform_text))
        
        # Create new axes for transformed data
        log_axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 50, 10],
            x_length=10,
            y_length=5,
            axis_config={"stroke_color": WHITE, "stroke_width": 2}
        ).move_to(DOWN*2)
        
        # Transform data
        log_data = np.log(self.original_data + 1)
        log_bins = np.histogram(log_data, bins=20, range=(0, 4))
        
        # Create new bars
        log_bars = VGroup()
        for i, (count, left_edge) in enumerate(zip(log_bins[0], log_bins[1][:-1])):
            if count > 0:
                bar = Rectangle(
                    width=log_axes.x_axis.unit_size * 0.2,
                    height=log_axes.y_axis.unit_size * count / 10,
                    fill_color=PURPLE,
                    fill_opacity=0.7,
                    stroke_color=WHITE,
                    stroke_width=1
                ).move_to(log_axes.coords_to_point(left_edge + 0.1, count/20))
                log_bars.add(bar)
        
        self.play(Create(log_axes))
        
        # Animate transformation - bars morph and move
        original_bars = self.original_elements[1]
        
        # Create morphing animation
        morph_animations = []
        for i, (orig_bar, new_bar) in enumerate(zip(original_bars, log_bars)):
            if i < len(log_bars):
                morph_animations.append(Transform(orig_bar.copy(), new_bar))
        
        self.play(*morph_animations[:len(log_bars)])
        
        # Show the result
        result_arrow = Arrow(
            self.original_elements[0].get_bottom() + DOWN*0.5,
            log_axes.get_top() + UP*0.2,
            color=GREEN,
            stroke_width=4
        )
        
        result_text = Text("Less Skewed!", font_size=20, color=GREEN, weight=BOLD)
        result_text.next_to(result_arrow, RIGHT)
        
        self.play(GrowArrow(result_arrow), Write(result_text))
        
        self.wait(2)
        self.play(FadeOut(VGroup(
            transform_text, log_axes, result_arrow, result_text
        )), *[FadeOut(anim.mobject) for anim in morph_animations[:len(log_bars)]])
        
        self.log_title = log_title
    
    def show_sqrt_transformation(self):
        """Show square root transformation"""
        sqrt_title = Text("Transformation 3: Square Root", font_size=28, color=ORANGE, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.log_title, sqrt_title))
        
        # Reset bar colors
        self.play(self.original_elements[1].animate.set_fill(RED, opacity=0.7))
        
        # Show transformation
        transform_text = Text("y → √y", font_size=24, color=YELLOW, weight=BOLD)
        transform_text.move_to(UP*1.5)
        self.play(Write(transform_text))
        
        # Create axes for sqrt transformed data
        sqrt_axes = Axes(
            x_range=[0, 8, 2],
            y_range=[0, 40, 10],
            x_length=10,
            y_length=5,
            axis_config={"stroke_color": WHITE, "stroke_width": 2}
        ).move_to(DOWN*2)
        
        # Transform data
        sqrt_data = np.sqrt(self.original_data)
        sqrt_bins = np.histogram(sqrt_data, bins=20, range=(0, 8))
        
        # Create bars
        sqrt_bars = VGroup()
        for i, (count, left_edge) in enumerate(zip(sqrt_bins[0], sqrt_bins[1][:-1])):
            if count > 0:
                bar = Rectangle(
                    width=sqrt_axes.x_axis.unit_size * 0.4,
                    height=sqrt_axes.y_axis.unit_size * count / 10,
                    fill_color=ORANGE,
                    fill_opacity=0.7,
                    stroke_color=WHITE,
                    stroke_width=1
                ).move_to(sqrt_axes.coords_to_point(left_edge + 0.2, count/20))
                sqrt_bars.add(bar)
        
        self.play(Create(sqrt_axes))
        
        # Animate transformation with shrinking effect
        original_bars = self.original_elements[1]
        
        # Create shrinking and moving animation
        shrink_animations = []
        for i in range(min(len(original_bars), len(sqrt_bars))):
            shrink_animations.append(Transform(original_bars[i].copy(), sqrt_bars[i]))
        
        self.play(*shrink_animations)
        
        # Show improvement
        improvement_text = Text("Moderately Reduced Skew", font_size=18, color=GREEN, weight=BOLD)
        improvement_text.next_to(sqrt_axes, DOWN, buff=0.5)
        self.play(Write(improvement_text))
        
        self.wait(2)
        self.play(FadeOut(VGroup(
            transform_text, sqrt_axes, improvement_text
        )), *[FadeOut(anim.mobject) for anim in shrink_animations])
        
        self.sqrt_title = sqrt_title
    
    def show_final_comparison(self):
        """Show side-by-side comparison of all transformations"""
        comparison_title = Text("Transformation Comparison", font_size=32, color=YELLOW, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.sqrt_title, comparison_title))
        
        # Clear original
        self.play(FadeOut(self.original_elements))
        
        # Create four panels
        panel_width = 2.5
        panel_positions = [LEFT*6, LEFT*2, RIGHT*2, RIGHT*6]
        panel_titles = ["Original", "Dummy Variable", "Log Transform", "√ Transform"]
        panel_colors = [RED, BLUE, PURPLE, ORANGE]
        
        panels = VGroup()
        
        for i, (pos, title, color) in enumerate(zip(panel_positions, panel_titles, panel_colors)):
            # Title
            panel_title = Text(title, font_size=14, color=color, weight=BOLD)
            panel_title.move_to(pos + UP*2.5)
            
            # Mini axes
            axes = Axes(
                x_range=[0, 1, 1] if i == 1 else [0, 10, 5],
                y_range=[0, 1, 1],
                x_length=panel_width,
                y_length=2,
                axis_config={"stroke_color": WHITE, "stroke_width": 1}
            ).move_to(pos + DOWN*0.5)
            
            # Create representative distribution shape
            if i == 0:  # Original - highly skewed
                bars_x = [0.1, 0.3, 0.5, 0.7, 0.9]
                bars_h = [0.8, 0.4, 0.2, 0.1, 0.05]
            elif i == 1:  # Dummy - binary
                bars_x = [0.25, 0.75]
                bars_h = [0.6, 0.4]
            elif i == 2:  # Log - more normal
                bars_x = [0.1, 0.3, 0.5, 0.7, 0.9]
                bars_h = [0.2, 0.5, 0.7, 0.4, 0.2]
            else:  # Sqrt - somewhat improved
                bars_x = [0.1, 0.3, 0.5, 0.7, 0.9]
                bars_h = [0.5, 0.6, 0.5, 0.3, 0.1]
            
            bars = VGroup()
            for x, h in zip(bars_x, bars_h):
                bar = Rectangle(
                    width=0.15,
                    height=h,
                    fill_color=color,
                    fill_opacity=0.7,
                    stroke_color=WHITE,
                    stroke_width=1
                ).move_to(axes.coords_to_point(x, h/2))
                bars.add(bar)
            
            panel = VGroup(panel_title, axes, bars)
            panels.add(panel)
        
        # Animate all panels appearing
        for panel in panels:
            self.play(FadeIn(panel), run_time=0.8)
        
        # Add final message
        final_message = Text("Choose transformation based on your data distribution and analysis goals!", 
                           font_size=16, color=WHITE, weight=BOLD)
        final_message.to_edge(DOWN)
        
        self.play(Write(final_message))
        self.wait(3)