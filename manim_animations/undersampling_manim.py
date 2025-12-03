#!/usr/bin/env python3
"""
Undersampling Animation - Pros and Cons
Visual explanation of undersampling technique in imbalanced datasets
"""

from manim import *
import numpy as np

class UndersamplingAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Show intro
        self.show_intro()
        
        # Show imbalanced dataset problem
        self.show_imbalanced_problem()
        
        # Demonstrate undersampling process
        self.show_undersampling_process()
        
        # Show pros and cons
        self.show_pros_and_cons()
        
        # Show final comparison
        self.show_final_comparison()
    
    def show_intro(self):
        """Introduction to undersampling"""
        title = Text("Undersampling", font_size=48, color=YELLOW).to_edge(UP)
        subtitle = Text("Balancing Imbalanced Datasets", font_size=28, color=WHITE).next_to(title, DOWN)
        
        self.play(Write(title), Write(subtitle))
        self.wait(2)
        
        # Definition
        definition = VGroup(
            Text("What is Undersampling?", font_size=24, color=LIGHT_GRAY),
            Text("• Keep ALL observations from minority class", font_size=20, color=BLUE).shift(LEFT * 1),
            Text("• Randomly remove observations from majority class", font_size=20, color=RED).shift(LEFT * 1),
            Text("• Goal: Create balanced dataset", font_size=20, color=GREEN).shift(LEFT * 1)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(subtitle, DOWN, buff=1)
        
        for item in definition:
            self.play(FadeIn(item, shift=UP))
            self.wait(0.5)
        
        self.wait(2)
        self.play(FadeOut(title, subtitle, definition))
    
    def show_imbalanced_problem(self):
        """Show the imbalanced dataset problem"""
        title = Text("The Imbalanced Dataset Problem", font_size=36, color=YELLOW).to_edge(UP)
        self.play(Write(title))
        
        # Create imbalanced dataset visualization
        # Majority class (Red) - many points
        np.random.seed(42)
        majority_points = []
        for _ in range(80):
            x = np.random.uniform(-3, 3)
            y = np.random.uniform(-2, 2)
            point = Dot([x, y, 0], color=RED, radius=0.05)
            majority_points.append(point)
        
        # Minority class (Blue) - few points
        minority_points = []
        for _ in range(10):
            x = np.random.uniform(-3, 3)
            y = np.random.uniform(-2, 2)
            point = Dot([x, y, 0], color=BLUE, radius=0.08)
            minority_points.append(point)
        
        majority_group = VGroup(*majority_points)
        minority_group = VGroup(*minority_points)
        
        # Labels and counts
        majority_label = Text("Majority Class: 80 samples", font_size=20, color=RED).to_corner(UL, buff=0.8)
        minority_label = Text("Minority Class: 10 samples", font_size=20, color=BLUE).next_to(majority_label, DOWN, aligned_edge=LEFT)
        ratio_label = Text("Ratio: 8:1 (Highly Imbalanced!)", font_size=20, color=YELLOW).next_to(minority_label, DOWN, aligned_edge=LEFT)
        
        self.play(
            FadeIn(majority_group, lag_ratio=0.1),
            FadeIn(minority_group, lag_ratio=0.1),
            Write(majority_label),
            Write(minority_label),
            Write(ratio_label)
        )
        
        # Show problems with imbalanced data
        problems = VGroup(
            Text("Problems:", font_size=24, color=ORANGE),
            Text("• Model bias toward majority class", font_size=18, color=WHITE),
            Text("• Poor minority class detection", font_size=18, color=WHITE),
            Text("• Misleading accuracy metrics", font_size=18, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_corner(UR, buff=0.8)
        
        for problem in problems:
            self.play(FadeIn(problem))
            self.wait(0.5)
        
        self.wait(2)
        self.play(FadeOut(title, problems))
        
        # Store for next scene
        self.majority_group = majority_group
        self.minority_group = minority_group
        self.majority_label = majority_label
        self.minority_label = minority_label
        self.ratio_label = ratio_label
    
    def show_undersampling_process(self):
        """Demonstrate the undersampling process"""
        title = Text("Undersampling Process", font_size=36, color=YELLOW).to_edge(UP)
        self.play(Write(title))
        
        # Step 1: Keep all minority class
        step1_text = Text("Step 1: Keep ALL minority class samples", font_size=24, color=BLUE).next_to(title, DOWN, buff=0.5)
        self.play(Write(step1_text))
        
        # Highlight minority class
        minority_box = SurroundingRectangle(self.minority_group, color=BLUE, buff=0.2)
        self.play(Create(minority_box))
        self.wait(1)
        
        # Step 2: Randomly remove from majority class
        step2_text = Text("Step 2: Randomly remove from majority class", font_size=24, color=RED).next_to(step1_text, DOWN, buff=0.3)
        self.play(Write(step2_text), FadeOut(minority_box))
        
        # Randomly select points to keep (undersampling)
        majority_points = list(self.majority_group)
        np.random.shuffle(majority_points)
        
        # Keep only 10 points to match minority class
        points_to_keep = majority_points[:10]
        points_to_remove = majority_points[10:]
        
        # Animate removal
        removal_group = VGroup(*points_to_remove)
        kept_group = VGroup(*points_to_keep)
        
        # Highlight points to remove
        for i, point in enumerate(points_to_remove):
            if i % 8 == 0:  # Animate every 8th point for speed
                self.play(point.animate.set_color(GRAY).scale(0.5), run_time=0.1)
        
        # Remove the points
        self.play(FadeOut(removal_group))
        
        # Update labels
        new_majority_label = Text("Majority Class: 10 samples", font_size=20, color=RED).move_to(self.majority_label)
        new_ratio_label = Text("Ratio: 1:1 (Balanced!)", font_size=20, color=GREEN).move_to(self.ratio_label)
        
        self.play(
            ReplacementTransform(self.majority_label, new_majority_label),
            ReplacementTransform(self.ratio_label, new_ratio_label)
        )
        
        # Highlight the balanced result
        balanced_box = SurroundingRectangle(
            VGroup(kept_group, self.minority_group), 
            color=GREEN, 
            buff=0.3
        )
        balanced_text = Text("Balanced Dataset!", font_size=20, color=GREEN).next_to(balanced_box, DOWN)
        
        self.play(Create(balanced_box), Write(balanced_text))
        self.wait(2)
        
        self.play(FadeOut(title, step1_text, step2_text, balanced_box, balanced_text))
        
        # Store final groups
        self.final_majority = kept_group
        self.final_minority = self.minority_group
        self.final_majority_label = new_majority_label
        self.final_minority_label = self.minority_label
        self.final_ratio_label = new_ratio_label
    
    def show_pros_and_cons(self):
        """Show pros and cons of undersampling"""
        title = Text("Undersampling: Pros & Cons", font_size=36, color=YELLOW).to_edge(UP)
        self.play(Write(title))
        
        # Create two columns
        pros_title = Text("PROS ✅", font_size=28, color=GREEN).to_corner(UL, buff=1).shift(RIGHT * 0.5)
        cons_title = Text("CONS ❌", font_size=28, color=RED).to_corner(UR, buff=1).shift(LEFT * 0.5)
        
        self.play(Write(pros_title), Write(cons_title))
        
        # Pros
        pros_list = VGroup(
            Text("• Balances the dataset", font_size=20, color=WHITE),
            Text("• Reduces training time", font_size=20, color=WHITE),
            Text("• Improves minority class recall", font_size=20, color=WHITE),
            Text("• Simple to implement", font_size=20, color=WHITE),
            Text("• Reduces computational cost", font_size=20, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(pros_title, DOWN, buff=0.5)
        
        # Cons
        cons_list = VGroup(
            Text("• Less training data", font_size=20, color=WHITE),
            Text("• Information loss", font_size=20, color=WHITE),
            Text("• Risk of overfitting", font_size=20, color=WHITE),
            Text("• Less robust models", font_size=20, color=WHITE),
            Text("• May remove important patterns", font_size=20, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(cons_title, DOWN, buff=0.5)
        
        # Animate pros and cons
        for pro, con in zip(pros_list, cons_list):
            self.play(FadeIn(pro, shift=RIGHT), FadeIn(con, shift=LEFT))
            self.wait(0.8)
        
        # Visual demonstration of information loss
        self.wait(1)
        
        # Show original dataset size
        original_size_text = Text("Original: 90 samples", font_size=18, color=YELLOW).next_to(cons_list, DOWN, buff=0.8)
        final_size_text = Text("After Undersampling: 20 samples", font_size=18, color=ORANGE).next_to(original_size_text, DOWN)
        loss_text = Text("Information Loss: 78%", font_size=18, color=RED).next_to(final_size_text, DOWN)
        
        self.play(Write(original_size_text))
        self.play(Write(final_size_text))
        self.play(Write(loss_text))
        
        self.wait(3)
        self.play(FadeOut(title, pros_title, cons_title, pros_list, cons_list, 
                         original_size_text, final_size_text, loss_text))
    
    def show_final_comparison(self):
        """Show before and after comparison"""
        title = Text("Before vs After Undersampling", font_size=36, color=YELLOW).to_edge(UP)
        self.play(Write(title))
        
        # Before section
        before_title = Text("BEFORE", font_size=24, color=RED).to_corner(UL, buff=1)
        before_stats = VGroup(
            Text("Total: 90 samples", font_size=18, color=WHITE),
            Text("Majority: 80 (89%)", font_size=18, color=RED),
            Text("Minority: 10 (11%)", font_size=18, color=BLUE),
            Text("Ratio: 8:1", font_size=18, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(before_title, DOWN, buff=0.3)
        
        # After section
        after_title = Text("AFTER", font_size=24, color=GREEN).to_corner(UR, buff=1)
        after_stats = VGroup(
            Text("Total: 20 samples", font_size=18, color=WHITE),
            Text("Majority: 10 (50%)", font_size=18, color=RED),
            Text("Minority: 10 (50%)", font_size=18, color=BLUE),
            Text("Ratio: 1:1", font_size=18, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(after_title, DOWN, buff=0.3)
        
        self.play(Write(before_title), Write(after_title))
        
        for before_stat, after_stat in zip(before_stats, after_stats):
            self.play(FadeIn(before_stat), FadeIn(after_stat))
            self.wait(0.5)
        
        # Key recommendations
        recommendations = VGroup(
            Text("RECOMMENDATIONS:", font_size=24, color=YELLOW),
            Text("• Use when you have LOTS of majority class data", font_size=18, color=WHITE),
            Text("• Consider Random Undersampling vs Informed methods", font_size=18, color=WHITE),
            Text("• Combine with oversampling (SMOTE) for best results", font_size=18, color=WHITE),
            Text("• Always validate on separate test set", font_size=18, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(DOWN * 2)
        
        for rec in recommendations:
            self.play(FadeIn(rec))
            self.wait(0.6)
        
        # Final message
        self.wait(2)
        final_message = Text(
            "Undersampling: Quick balance, but use wisely!",
            font_size=28,
            color=YELLOW
        ).next_to(recommendations, DOWN, buff=0.8)
        
        self.play(Write(final_message))
        self.wait(3)