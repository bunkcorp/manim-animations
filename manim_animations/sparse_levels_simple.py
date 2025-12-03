#!/usr/bin/env python3
"""
Sparse Levels Simple Animation
Simplified demonstration of sparse levels problem and solutions
"""

from manim import *
import numpy as np

class SparseLevelsSimple(Scene):
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Show the problem
        self.show_sparse_problem()
        
        # Show the solution
        self.show_grouping_solution()
        
        # Show guidelines
        self.show_guidelines()
    
    def show_sparse_problem(self):
        """Show sparse levels problem"""
        title = Text("Sparse Levels Problem", 
                    font_size=32, color=YELLOW, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Example: Hour of Day
        example = Text("Example: Hour of Day (0-23)", 
                      font_size=20, color=WHITE, weight=BOLD)
        example.move_to(UP*2.5)
        self.play(Write(example))
        
        # Show the problem visually
        problem_text = Text("The Problem:", font_size=18, color=RED, weight=BOLD)
        problem_text.move_to(UP*1.8)
        self.play(Write(problem_text))
        
        # Create simple bar chart representation
        bars_group = VGroup()
        
        # High bars for business hours
        for i in range(9, 18):  # 9 AM to 5 PM
            bar = Rectangle(width=0.3, height=1.5, fill_color=GREEN, fill_opacity=0.8)
            bar.move_to(LEFT*5 + RIGHT*(i-9)*0.4 + UP*0.5)
            bars_group.add(bar)
        
        # Low bars for night hours
        night_hours = [2, 3, 4, 5]
        for i, hour in enumerate(night_hours):
            bar = Rectangle(width=0.3, height=0.2, fill_color=RED, fill_opacity=0.8)
            bar.move_to(LEFT*3 + RIGHT*i*0.4 + DOWN*0.3)
            bars_group.add(bar)
        
        # Labels
        high_label = Text("Business Hours\n5000+ obs each", font_size=12, color=GREEN)
        high_label.move_to(LEFT*2 + UP*1.3)
        
        low_label = Text("Night Hours\n<50 obs each", font_size=12, color=RED)
        low_label.move_to(LEFT*2 + DOWN*0.8)
        
        self.play(*[GrowFromEdge(bar, DOWN) for bar in bars_group])
        self.play(Write(high_label), Write(low_label))
        
        # Show problems
        problems = VGroup(
            Text("• 24 separate categories", font_size=16, color=WHITE),
            Text("• Sparse levels = Unstable estimates", font_size=16, color=RED),
            Text("• Overfitting risk in models", font_size=16, color=RED),
            Text("• Poor generalization", font_size=16, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        problems.move_to(RIGHT*3 + DOWN*0.5)
        
        for problem in problems:
            self.play(Write(problem), run_time=0.8)
        
        self.wait(2)
        self.play(FadeOut(*self.mobjects[1:]))  # Keep title
        self.title = title
    
    def show_grouping_solution(self):
        """Show intelligent grouping solution"""
        solution_title = Text("Smart Grouping Solution", 
                             font_size=28, color=GREEN, weight=BOLD)
        self.play(ReplacementTransform(self.title, solution_title))
        
        # Show target behavior analysis
        analysis_text = Text("Step 1: Analyze Target Behavior", 
                           font_size=20, color=BLUE, weight=BOLD)
        analysis_text.move_to(UP*2.5)
        self.play(Write(analysis_text))
        
        # Simple line showing target behavior pattern
        axes = Axes(
            x_range=[0, 24, 6],
            y_range=[0.3, 0.7, 0.1],
            x_length=8,
            y_length=3,
            axis_config={"stroke_color": WHITE, "stroke_width": 2}
        ).move_to(UP*0.8)
        
        x_label = Text("Hour", font_size=14, color=WHITE)
        x_label.next_to(axes.x_axis, DOWN)
        
        y_label = Text("Target Rate", font_size=14, color=WHITE)
        y_label.next_to(axes.y_axis, LEFT)
        y_label.rotate(PI/2)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Create target behavior curve
        hours = np.linspace(0, 24, 100)
        # Morning dip, afternoon peak, evening moderate
        target_rates = 0.5 + 0.1*np.sin((hours-14)*PI/12) + 0.05*np.random.normal(size=100)
        target_rates = np.clip(target_rates, 0.3, 0.7)
        
        curve_points = [axes.coords_to_point(h, r) for h, r in zip(hours, target_rates)]
        curve = VMobject()
        curve.set_points_smoothly(curve_points)
        curve.set_stroke(BLUE, width=3)
        
        self.play(Create(curve), run_time=2)
        
        # Show grouping strategy
        grouping_text = Text("Step 2: Group by Similar Behavior", 
                           font_size=20, color=ORANGE, weight=BOLD)
        grouping_text.move_to(DOWN*1.5)
        self.play(Write(grouping_text))
        
        # Show three groups
        groups = VGroup(
            Text("Morning (6-11): Rate = 0.45", font_size=14, color=ORANGE),
            Text("Afternoon (12-17): Rate = 0.62", font_size=14, color=GREEN),
            Text("Evening/Night (18-5): Rate = 0.38", font_size=14, color=PURPLE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        groups.move_to(DOWN*2.5)
        
        for group in groups:
            self.play(Write(group), run_time=0.8)
        
        # Show the transformation
        transformation = Text("24 Categories → 3 Robust Groups", 
                            font_size=18, color=YELLOW, weight=BOLD)
        transformation.move_to(DOWN*3.5)
        self.play(Write(transformation))
        
        self.wait(3)
        self.play(FadeOut(*self.mobjects[1:]))  # Keep title
        self.solution_title = solution_title
    
    def show_guidelines(self):
        """Show practical guidelines"""
        guidelines_title = Text("Practical Guidelines", 
                              font_size=32, color=YELLOW, weight=BOLD)
        self.play(ReplacementTransform(self.solution_title, guidelines_title))
        
        # Key principles
        principles = VGroup(
            Text("Key Principles:", font_size=24, color=WHITE, weight=BOLD),
            Text("", font_size=4),  # Spacer
            Text("1. Group by target behavior, not just frequency", font_size=18, color=GREEN),
            Text("2. Ensure adequate sample size (100+ per group)", font_size=18, color=BLUE),
            Text("3. Use domain knowledge to guide grouping", font_size=18, color=PURPLE),
            Text("4. Test statistical significance of differences", font_size=18, color=ORANGE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        principles.move_to(UP*1)
        
        for principle in principles:
            self.play(Write(principle), run_time=1)
        
        # Examples
        examples_title = Text("Common Examples:", font_size=20, color=YELLOW, weight=BOLD)
        examples_title.move_to(DOWN*1)
        
        examples = VGroup(
            Text("• Geographic: States → Regions", font_size=16, color=WHITE),
            Text("• Age: Individual ages → Life stages", font_size=16, color=WHITE),
            Text("• Industry: NAICS codes → Sectors", font_size=16, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        examples.move_to(DOWN*2.2)
        
        self.play(Write(examples_title))
        for example in examples:
            self.play(Write(example), run_time=0.8)
        
        # Warning
        warning = Text("⚠️ Don't group different behaviors together!", 
                      font_size=16, color=RED, weight=BOLD)
        warning.move_to(DOWN*3.5)
        self.play(Write(warning))
        
        self.wait(4)

if __name__ == "__main__":
    # For testing
    pass