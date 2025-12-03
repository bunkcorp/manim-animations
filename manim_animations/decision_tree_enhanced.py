#!/usr/bin/env python3
"""
Enhanced Decision Tree Animation
Shows the complete concept: partitioning, tree structure, and predictions
Based on the comprehensive decision tree concepts
"""

from manim import *
import numpy as np

class DecisionTreeEnhanced(Scene):
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Show title card
        self.show_title()
        
        # Show basic concept
        self.show_basic_concept()
        
        # Show feature space partitioning
        self.show_feature_space_partitioning()
        
        # Show tree structure
        self.show_tree_structure()
        
        # Show predictions
        self.show_predictions()
        
        # Show summary
        self.show_summary()
    
    def show_title(self):
        """Title card"""
        title = Text("Single Decision Tree", font_size=42, color=YELLOW, weight=BOLD)
        subtitle = Text("Basic Idea & Structure", font_size=28, color=WHITE)
        concept = Text("Partition feature space → rules → constant prediction per leaf", 
                      font_size=22, color=LIGHT_GRAY, slant=ITALIC)
        
        title_group = VGroup(title, subtitle, concept).arrange(DOWN, buff=0.5)
        
        self.play(Write(title))
        self.play(Write(subtitle))
        self.play(Write(concept))
        self.wait(2)
        self.play(FadeOut(title_group))
    
    def show_basic_concept(self):
        """Show what decision trees do"""
        title = Text("What is a Decision Tree?", font_size=32, color=BLUE, weight=BOLD).to_edge(UP)
        self.play(Write(title))
        
        # Key concepts
        concepts = VGroup(
            Text("🎯 Goal: Make predictions by learning simple decision rules", font_size=24, color=WHITE),
            Text("📊 Method: Partition data into homogeneous regions", font_size=24, color=WHITE),
            Text("🌳 Structure: Binary tree with splits and predictions", font_size=24, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to(ORIGIN)
        
        for concept in concepts:
            self.play(FadeIn(concept, shift=UP))
            self.wait(1)
        
        self.wait(2)
        self.play(FadeOut(concepts))
        self.title = title
    
    def show_feature_space_partitioning(self):
        """Show how trees partition feature space"""
        partition_title = Text("Feature Space Partitioning", font_size=28, color=GREEN, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.title, partition_title))
        
        # Create 2D feature space
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            x_length=5,
            y_length=5,
            axis_config={"stroke_color": WHITE, "stroke_width": 2}
        ).move_to(LEFT*3)
        
        x_label = Text("x₁", font_size=18, color=WHITE).next_to(axes, DOWN)
        y_label = Text("x₂", font_size=18, color=WHITE).next_to(axes, LEFT).rotate(PI/2)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Add sample data points (similar to original code pattern)
        np.random.seed(7)
        
        # Create clustered points for two classes
        def create_blob(center, n_points, spread, color):
            points = []
            for _ in range(n_points):
                x, y = np.random.normal(center, spread, 2)
                x, y = max(0.2, min(4.8, x)), max(0.2, min(4.8, y))
                point = Dot(axes.coords_to_point(x, y), color=color, radius=0.06)
                points.append(point)
            return points
        
        # Class A (Green) - bottom left and top right
        class_a_points = (create_blob([1.2, 3.8], 18, 0.35, GREEN) + 
                         create_blob([0.9, 1.0], 12, 0.35, GREEN))
        
        # Class B (Red) - top left and bottom right  
        class_b_points = (create_blob([3.6, 1.2], 16, 0.35, RED) +
                         create_blob([3.4, 4.0], 14, 0.35, RED))
        
        # Show data points
        self.play(
            *[FadeIn(p, scale=0.7) for p in class_a_points],
            *[FadeIn(p, scale=0.7) for p in class_b_points]
        )
        
        # Add legend
        legend = VGroup(
            VGroup(Dot(color=GREEN, radius=0.08), Text("Class A", font_size=16, color=WHITE)).arrange(RIGHT, buff=0.2),
            VGroup(Dot(color=RED, radius=0.08), Text("Class B", font_size=16, color=WHITE)).arrange(RIGHT, buff=0.2)
        ).arrange(DOWN, buff=0.3).next_to(axes, RIGHT, buff=1)
        
        self.play(FadeIn(legend))
        
        # Show splits progressively
        # Split 1: x₁ < 2.2?
        x_split = 2.2
        vline = Line(
            axes.coords_to_point(x_split, 0),
            axes.coords_to_point(x_split, 5),
            color=BLUE,
            stroke_width=4
        )
        
        split1_label = Text("Split: x₁ < 2.2?", font_size=18, color=BLUE, slant=ITALIC)
        split1_label.next_to(vline, UP, buff=0.3)
        
        self.play(Create(vline), FadeIn(split1_label, shift=UP))
        self.wait(1.5)
        
        # Split 2 on left side: x₂ < 2.2?
        y_split_left = 2.2
        hline_left = Line(
            axes.coords_to_point(0, y_split_left),
            axes.coords_to_point(x_split, y_split_left),
            color=BLUE,
            stroke_width=4
        )
        
        split2_label = Text("Split: x₂ < 2.2?", font_size=18, color=BLUE, slant=ITALIC)
        split2_label.next_to(hline_left, LEFT, buff=0.2)
        
        self.play(Create(hline_left), FadeIn(split2_label, shift=LEFT))
        self.wait(1.5)
        
        # Split 3 on right side: x₂ < 2.8?
        y_split_right = 2.8
        hline_right = Line(
            axes.coords_to_point(x_split, y_split_right),
            axes.coords_to_point(5, y_split_right),
            color=BLUE,
            stroke_width=4
        )
        
        split3_label = Text("Split: x₂ < 2.8?", font_size=18, color=BLUE, slant=ITALIC)
        split3_label.next_to(hline_right, RIGHT, buff=0.2)
        
        self.play(Create(hline_right), FadeIn(split3_label, shift=RIGHT))
        self.wait(1.5)
        
        # Shade the four leaf regions
        def create_region_poly(x0, x1, y0, y1, color, alpha=0.15):
            return Polygon(
                axes.coords_to_point(x0, y0),
                axes.coords_to_point(x1, y0),
                axes.coords_to_point(x1, y1),
                axes.coords_to_point(x0, y1),
                stroke_width=2,
                stroke_color=color,
                fill_color=color,
                fill_opacity=alpha
            )
        
        R1 = create_region_poly(0, x_split, 0, y_split_left, RED)        # bottom-left → Class B
        R2 = create_region_poly(0, x_split, y_split_left, 5, GREEN)      # top-left → Class A  
        R3 = create_region_poly(x_split, 5, 0, y_split_right, RED)       # bottom-right → Class B
        R4 = create_region_poly(x_split, 5, y_split_right, 5, GREEN)     # top-right → Class A
        
        self.play(FadeIn(R1), FadeIn(R2), FadeIn(R3), FadeIn(R4))
        
        # Caption
        caption = Text("Idea: Partition feature space into homogeneous regions", 
                      font_size=18, color=WHITE, slant=ITALIC)
        caption.next_to(axes, DOWN, buff=0.5)
        self.play(FadeIn(caption, shift=DOWN))
        
        self.wait(2)
        
        # Store elements for cleanup
        self.partition_elements = VGroup(
            axes, x_label, y_label, legend, vline, hline_left, hline_right,
            split1_label, split2_label, split3_label, R1, R2, R3, R4, caption,
            *class_a_points, *class_b_points
        )
        self.partition_title = partition_title
    
    def show_tree_structure(self):
        """Show corresponding tree structure"""
        tree_title = Text("Corresponding Tree Structure", font_size=28, color=PURPLE, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.partition_title, tree_title))
        
        # Fade out partition view
        self.play(FadeOut(self.partition_elements))
        
        # Create tree structure manually (simplified tree builder)
        # Root node
        root_box = RoundedRectangle(
            corner_radius=0.15, width=3.5, height=0.9,
            stroke_color=BLUE, stroke_width=2,
            fill_color=BLACK, fill_opacity=0.9
        )
        root_text = Text("x₁ < 2.2?", font_size=20, color=WHITE, slant=ITALIC)
        root_group = VGroup(root_box, root_text).move_to(UP*2.5)
        
        # Left internal node
        left_box = RoundedRectangle(
            corner_radius=0.15, width=3.5, height=0.9,
            stroke_color=BLUE, stroke_width=2,
            fill_color=BLACK, fill_opacity=0.9
        )
        left_text = Text("x₂ < 2.2?", font_size=20, color=WHITE, slant=ITALIC)
        left_group = VGroup(left_box, left_text).move_to(LEFT*2.5 + UP*0.5)
        
        # Right internal node
        right_box = RoundedRectangle(
            corner_radius=0.15, width=3.5, height=0.9,
            stroke_color=BLUE, stroke_width=2,
            fill_color=BLACK, fill_opacity=0.9
        )
        right_text = Text("x₂ < 2.8?", font_size=20, color=WHITE, slant=ITALIC)
        right_group = VGroup(right_box, right_text).move_to(RIGHT*2.5 + UP*0.5)
        
        # Leaf nodes
        leaf_bl_box = RoundedRectangle(
            corner_radius=0.15, width=3.5, height=0.9,
            stroke_color=GREEN, stroke_width=2,
            fill_color=BLACK, fill_opacity=0.9
        )
        leaf_bl_text = Text("Leaf: predict Class B", font_size=16, color=WHITE)
        leaf_bl_group = VGroup(leaf_bl_box, leaf_bl_text).move_to(LEFT*4.5 + DOWN*1.5)
        
        leaf_tl_box = RoundedRectangle(
            corner_radius=0.15, width=3.5, height=0.9,
            stroke_color=GREEN, stroke_width=2,
            fill_color=BLACK, fill_opacity=0.9
        )
        leaf_tl_text = Text("Leaf: predict Class A", font_size=16, color=WHITE)
        leaf_tl_group = VGroup(leaf_tl_box, leaf_tl_text).move_to(LEFT*0.5 + DOWN*1.5)
        
        leaf_br_box = RoundedRectangle(
            corner_radius=0.15, width=3.5, height=0.9,
            stroke_color=GREEN, stroke_width=2,
            fill_color=BLACK, fill_opacity=0.9
        )
        leaf_br_text = Text("Leaf: predict Class B", font_size=16, color=WHITE)
        leaf_br_group = VGroup(leaf_br_box, leaf_br_text).move_to(RIGHT*0.5 + DOWN*1.5)
        
        leaf_tr_box = RoundedRectangle(
            corner_radius=0.15, width=3.5, height=0.9,
            stroke_color=GREEN, stroke_width=2,
            fill_color=BLACK, fill_opacity=0.9
        )
        leaf_tr_text = Text("Leaf: predict Class A", font_size=16, color=WHITE)
        leaf_tr_group = VGroup(leaf_tr_box, leaf_tr_text).move_to(RIGHT*4.5 + DOWN*1.5)
        
        # Edges
        edge1 = Line(root_group.get_bottom(), left_group.get_top(), stroke_width=3, color=GRAY)
        edge2 = Line(root_group.get_bottom(), right_group.get_top(), stroke_width=3, color=GRAY)
        edge3 = Line(left_group.get_bottom(), leaf_bl_group.get_top(), stroke_width=3, color=GRAY)
        edge4 = Line(left_group.get_bottom(), leaf_tl_group.get_top(), stroke_width=3, color=GRAY)
        edge5 = Line(right_group.get_bottom(), leaf_br_group.get_top(), stroke_width=3, color=GRAY)
        edge6 = Line(right_group.get_bottom(), leaf_tr_group.get_top(), stroke_width=3, color=GRAY)
        
        # Build tree progressively
        self.play(FadeIn(root_group, scale=0.8))
        self.wait(0.8)
        
        self.play(
            Create(edge1), Create(edge2),
            FadeIn(left_group, scale=0.8), FadeIn(right_group, scale=0.8)
        )
        self.wait(0.8)
        
        self.play(
            Create(edge3), Create(edge4), Create(edge5), Create(edge6),
            FadeIn(leaf_bl_group, scale=0.8), FadeIn(leaf_tl_group, scale=0.8),
            FadeIn(leaf_br_group, scale=0.8), FadeIn(leaf_tr_group, scale=0.8)
        )
        
        # Add annotations
        deliver_text = Text("Deliverable: a set of rules represented as a TREE", 
                           font_size=20, color=ORANGE, weight=BOLD)
        deliver_text.to_edge(DOWN, buff=1.5)
        self.play(FadeIn(deliver_text, shift=UP))
        
        self.wait(2)
        
        # Store tree elements
        self.tree_elements = VGroup(
            root_group, left_group, right_group,
            leaf_bl_group, leaf_tl_group, leaf_br_group, leaf_tr_group,
            edge1, edge2, edge3, edge4, edge5, edge6, deliver_text
        )
        self.tree_title = tree_title
    
    def show_predictions(self):
        """Show how predictions work"""
        pred_title = Text("How Predictions Work", font_size=28, color=ORANGE, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.tree_title, pred_title))
        
        # Keep tree but fade it slightly
        self.play(self.tree_elements.animate.set_opacity(0.3))
        
        # Show prediction principles
        principles = VGroup(
            Text("Prediction Principles:", font_size=24, color=YELLOW, weight=BOLD),
            Text("• All observations in a terminal node share the same prediction", font_size=20, color=WHITE),
            Text("• Classification: same predicted class per leaf", font_size=20, color=WHITE),
            Text("• Regression: same predicted mean per leaf", font_size=20, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(ORIGIN)
        
        for principle in principles:
            self.play(Write(principle))
            self.wait(0.8)
        
        self.wait(2)
        
        # Show regression example briefly
        reg_note = Text("For regression: leaves predict mean values (e.g., 0.82, 0.23)", 
                       font_size=18, color=LIGHT_GRAY, slant=ITALIC)
        reg_note.next_to(principles, DOWN, buff=0.8)
        self.play(FadeIn(reg_note, shift=UP))
        self.wait(1.5)
        self.play(FadeOut(reg_note))
        
        self.play(FadeOut(principles), self.tree_elements.animate.set_opacity(1))
        self.pred_title = pred_title
    
    def show_summary(self):
        """Show final summary"""
        summary_title = Text("Decision Tree Summary", font_size=32, color=YELLOW, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.pred_title, summary_title))
        self.play(FadeOut(self.tree_elements))
        
        # Create summary card
        card = RoundedRectangle(
            corner_radius=0.2, width=12.0, height=3.5,
            stroke_color=WHITE, stroke_width=2,
            fill_color=BLACK, fill_opacity=0.95
        ).move_to(ORIGIN)
        
        # Two-column summary
        left_col = VGroup(
            Text("Basic Idea", font_size=22, color=YELLOW, weight=BOLD),
            Text("Divide X into non-overlapping,", font_size=18, color=WHITE, slant=ITALIC),
            Text("homogeneous regions.", font_size=18, color=WHITE, slant=ITALIC),
            Text("Rules form a tree; each leaf =", font_size=18, color=WHITE, slant=ITALIC),
            Text("constant prediction.", font_size=18, color=WHITE, slant=ITALIC)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        right_col = VGroup(
            Text("Structure & Predictions", font_size=22, color=YELLOW, weight=BOLD),
            Text("• Numeric targets → predict the mean in the leaf", font_size=18, color=WHITE),
            Text("• Categorical targets → predict majority class", font_size=18, color=WHITE), 
            Text("• All samples in a leaf share same prediction", font_size=18, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        summary_content = VGroup(left_col, right_col).arrange(RIGHT, buff=1.5).move_to(card.get_center())
        
        self.play(FadeIn(card, shift=UP), FadeIn(summary_content, shift=UP))
        self.wait(3)
        
        # Final insight
        final_insight = Text(
            "Understanding decision trees: Simple rules, powerful predictions!",
            font_size=22, color=YELLOW, weight=BOLD
        ).next_to(card, DOWN, buff=0.8)
        
        self.play(Write(final_insight))
        self.wait(3)