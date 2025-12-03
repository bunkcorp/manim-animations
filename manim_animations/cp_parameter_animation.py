#!/usr/bin/env python3
"""
Complexity Parameter (cp) Control Animation
Shows how cp controls decision tree splitting and pruning
"""

from manim import *
import numpy as np

class CPParameterAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Show title card
        self.show_title()
        
        # Show basic concept
        self.show_basic_concept()
        
        # Show cp threshold mechanism
        self.show_cp_threshold()
        
        # Show tree complexity levels
        self.show_complexity_levels()
        
        # Show overfitting prevention
        self.show_overfitting_prevention()
        
        # Show summary
        self.show_summary()
    
    def show_title(self):
        """Title card"""
        title = Text("Complexity Parameter (cp)", font_size=36, color=YELLOW, weight=BOLD)
        subtitle = Text("Controlling Decision Tree Splitting", font_size=28, color=WHITE)
        concept = Text("cp = minimum improvement required to make a split", 
                      font_size=20, color=LIGHT_GRAY, slant=ITALIC)
        
        title_group = VGroup(title, subtitle, concept).arrange(DOWN, buff=0.4)
        
        self.play(Write(title))
        self.play(Write(subtitle))
        self.play(Write(concept))
        self.wait(2)
        self.play(FadeOut(title_group))
    
    def show_basic_concept(self):
        """Explain what cp controls"""
        title = Text("What does cp control?", font_size=32, color=BLUE, weight=BOLD).to_edge(UP)
        self.play(Write(title))
        
        # Key concept
        main_concept = VGroup(
            Text("🎯 cp = Complexity Parameter", font_size=24, color=YELLOW, weight=BOLD),
            Text("Controls the minimum improvement needed to split a node", font_size=20, color=WHITE),
            Text("Acts as a 'threshold' for tree growth", font_size=20, color=WHITE, slant=ITALIC)
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        
        for concept in main_concept:
            self.play(FadeIn(concept, shift=UP))
            self.wait(1)
        
        # Show the trade-off
        tradeoff = VGroup(
            Text("The Trade-off:", font_size=22, color=ORANGE, weight=BOLD),
            VGroup(
                Text("High cp", font_size=18, color=WHITE, weight=BOLD),
                Text("→", font_size=18, color=WHITE),
                Text("Fewer splits", font_size=18, color=GREEN),
                Text("→", font_size=18, color=WHITE), 
                Text("Simpler tree", font_size=18, color=BLUE),
                Text("→", font_size=18, color=WHITE),
                Text("Less overfitting", font_size=18, color=GREEN)
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Text("Low cp", font_size=18, color=WHITE, weight=BOLD),
                Text("→", font_size=18, color=WHITE),
                Text("More splits", font_size=18, color=GREEN),
                Text("→", font_size=18, color=WHITE),
                Text("Complex tree", font_size=18, color=BLUE),
                Text("→", font_size=18, color=WHITE),
                Text("Risk overfitting", font_size=18, color=RED)
            ).arrange(RIGHT, buff=0.2)
        ).arrange(DOWN, buff=0.4).next_to(main_concept, DOWN, buff=1)
        
        for item in tradeoff:
            self.play(Write(item))
            self.wait(1)
        
        self.wait(2)
        self.play(FadeOut(main_concept, tradeoff))
        self.title = title
    
    def show_cp_threshold(self):
        """Show how cp acts as a threshold"""
        threshold_title = Text("cp as a Splitting Threshold", font_size=28, color=GREEN, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.title, threshold_title))
        
        # Create a visual representation of improvement vs threshold
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 0.1, 0.02],
            x_length=8,
            y_length=4,
            axis_config={"stroke_color": WHITE, "stroke_width": 2}
        ).move_to(DOWN*0.5)
        
        x_label = Text("Potential Splits (ranked by improvement)", font_size=16, color=WHITE).next_to(axes, DOWN)
        y_label = Text("Improvement", font_size=16, color=WHITE).next_to(axes, LEFT).rotate(PI/2)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Create bars showing improvement for different splits
        improvements = [0.08, 0.06, 0.04, 0.03, 0.015, 0.01, 0.005, 0.002]
        bars = VGroup()
        
        for i, imp in enumerate(improvements):
            bar = Rectangle(
                width=0.8,
                height=axes.y_axis.unit_size * imp / 0.02,
                fill_color=BLUE,
                fill_opacity=0.7,
                stroke_color=WHITE
            ).move_to(axes.coords_to_point(i + 1, imp/2))
            bars.add(bar)
        
        self.play(*[Create(bar) for bar in bars])
        
        # Show different cp thresholds
        cp_values = [0.05, 0.02, 0.01]
        colors = [RED, ORANGE, GREEN]
        
        for i, (cp, color) in enumerate(zip(cp_values, colors)):
            # Draw threshold line
            threshold_line = Line(
                axes.coords_to_point(0, cp),
                axes.coords_to_point(9, cp),
                stroke_color=color,
                stroke_width=4
            )
            
            threshold_label = Text(f"cp = {cp}", font_size=16, color=color, weight=BOLD)
            threshold_label.next_to(threshold_line, RIGHT, buff=0.2)
            
            self.play(Create(threshold_line), Write(threshold_label))
            
            # Highlight which splits would be made
            approved_bars = VGroup()
            rejected_bars = VGroup()
            
            for j, (bar, imp) in enumerate(zip(bars, improvements)):
                if imp > cp:
                    approved_bars.add(bar)
                else:
                    rejected_bars.add(bar)
            
            if len(approved_bars) > 0:
                self.play(approved_bars.animate.set_fill(color=GREEN, opacity=0.8))
            if len(rejected_bars) > 0:
                self.play(rejected_bars.animate.set_fill(color=RED, opacity=0.3))
            
            # Show result
            result_text = Text(f"Splits made: {len(approved_bars)}/{len(bars)}", 
                             font_size=18, color=color, weight=BOLD)
            result_text.next_to(axes, UP, buff=0.5)
            
            self.play(Write(result_text))
            self.wait(2)
            
            if i < len(cp_values) - 1:  # Not the last iteration
                self.play(
                    FadeOut(threshold_line, threshold_label, result_text),
                    *[bar.animate.set_fill(color=BLUE, opacity=0.7) for bar in bars]
                )
        
        # Clean up for next section
        self.play(FadeOut(axes, x_label, y_label, bars, threshold_line, threshold_label, result_text))
        self.threshold_title = threshold_title
    
    def show_complexity_levels(self):
        """Show trees at different complexity levels"""
        complexity_title = Text("Tree Complexity at Different cp Values", font_size=26, color=PURPLE, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.threshold_title, complexity_title))
        
        # Create three trees side by side
        tree_positions = [LEFT*4, ORIGIN, RIGHT*4]
        cp_values = [0.1, 0.01, 0.001]
        cp_labels = ["High cp = 0.1", "Medium cp = 0.01", "Low cp = 0.001"]
        colors = [GREEN, YELLOW, RED]
        
        trees = VGroup()
        
        for i, (pos, cp, label, color) in enumerate(zip(tree_positions, cp_values, cp_labels, colors)):
            # Tree title
            tree_title = Text(label, font_size=18, color=color, weight=BOLD).move_to(pos + UP*2.5)
            
            # Create tree structure based on cp
            if i == 0:  # High cp - simple tree
                tree = self.create_simple_tree(pos, color)
                description = VGroup(
                    Text("Simple tree", font_size=14, color=WHITE),
                    Text("Few splits", font_size=14, color=WHITE),
                    Text("May underfit", font_size=14, color=ORANGE)
                ).arrange(DOWN, buff=0.1).next_to(tree, DOWN, buff=0.3)
                
            elif i == 1:  # Medium cp - balanced tree  
                tree = self.create_medium_tree(pos, color)
                description = VGroup(
                    Text("Balanced tree", font_size=14, color=WHITE),
                    Text("Good complexity", font_size=14, color=WHITE),
                    Text("Often optimal", font_size=14, color=GREEN)
                ).arrange(DOWN, buff=0.1).next_to(tree, DOWN, buff=0.3)
                
            else:  # Low cp - complex tree
                tree = self.create_complex_tree(pos, color)
                description = VGroup(
                    Text("Complex tree", font_size=14, color=WHITE),
                    Text("Many splits", font_size=14, color=WHITE),
                    Text("May overfit", font_size=14, color=RED)
                ).arrange(DOWN, buff=0.1).next_to(tree, DOWN, buff=0.3)
            
            tree_group = VGroup(tree_title, tree, description)
            trees.add(tree_group)
            
            self.play(FadeIn(tree_group, shift=UP))
            self.wait(1)
        
        # Add arrows showing progression
        arrow1 = Arrow(tree_positions[0] + RIGHT*1.5, tree_positions[1] + LEFT*1.5, color=WHITE)
        arrow2 = Arrow(tree_positions[1] + RIGHT*1.5, tree_positions[2] + LEFT*1.5, color=WHITE)
        
        arrow_label = Text("Decreasing cp →", font_size=16, color=WHITE, slant=ITALIC)
        arrow_label.move_to((tree_positions[0] + tree_positions[2])/2 + DOWN*3)
        
        self.play(Create(arrow1), Create(arrow2), Write(arrow_label))
        self.wait(2)
        
        self.play(FadeOut(trees, arrow1, arrow2, arrow_label))
        self.complexity_title = complexity_title
    
    def create_simple_tree(self, center, color):
        """Create a simple tree with few nodes"""
        root = Circle(radius=0.15, color=color, fill_opacity=0.3).move_to(center)
        
        left_child = Circle(radius=0.12, color=color, fill_opacity=0.3).move_to(center + LEFT*0.8 + DOWN*0.8)
        right_child = Circle(radius=0.12, color=color, fill_opacity=0.3).move_to(center + RIGHT*0.8 + DOWN*0.8)
        
        line1 = Line(root.get_bottom(), left_child.get_top(), color=color)
        line2 = Line(root.get_bottom(), right_child.get_top(), color=color)
        
        return VGroup(root, left_child, right_child, line1, line2)
    
    def create_medium_tree(self, center, color):
        """Create a medium complexity tree"""
        root = Circle(radius=0.15, color=color, fill_opacity=0.3).move_to(center)
        
        left_child = Circle(radius=0.12, color=color, fill_opacity=0.3).move_to(center + LEFT*0.8 + DOWN*0.8)
        right_child = Circle(radius=0.12, color=color, fill_opacity=0.3).move_to(center + RIGHT*0.8 + DOWN*0.8)
        
        ll_child = Circle(radius=0.1, color=color, fill_opacity=0.3).move_to(center + LEFT*1.3 + DOWN*1.6)
        lr_child = Circle(radius=0.1, color=color, fill_opacity=0.3).move_to(center + LEFT*0.3 + DOWN*1.6)
        rl_child = Circle(radius=0.1, color=color, fill_opacity=0.3).move_to(center + RIGHT*0.3 + DOWN*1.6)
        
        lines = VGroup(
            Line(root.get_bottom(), left_child.get_top(), color=color),
            Line(root.get_bottom(), right_child.get_top(), color=color),
            Line(left_child.get_bottom(), ll_child.get_top(), color=color),
            Line(left_child.get_bottom(), lr_child.get_top(), color=color),
            Line(right_child.get_bottom(), rl_child.get_top(), color=color)
        )
        
        return VGroup(root, left_child, right_child, ll_child, lr_child, rl_child, lines)
    
    def create_complex_tree(self, center, color):
        """Create a complex tree with many nodes"""
        nodes = VGroup()
        lines = VGroup()
        
        # Root
        root = Circle(radius=0.12, color=color, fill_opacity=0.3).move_to(center)
        nodes.add(root)
        
        # Level 1
        positions_l1 = [center + LEFT*0.8 + DOWN*0.6, center + RIGHT*0.8 + DOWN*0.6]
        for pos in positions_l1:
            node = Circle(radius=0.1, color=color, fill_opacity=0.3).move_to(pos)
            nodes.add(node)
            lines.add(Line(root.get_bottom(), node.get_top(), color=color, stroke_width=2))
        
        # Level 2
        positions_l2 = [
            center + LEFT*1.2 + DOWN*1.2, center + LEFT*0.4 + DOWN*1.2,
            center + RIGHT*0.4 + DOWN*1.2, center + RIGHT*1.2 + DOWN*1.2
        ]
        for i, pos in enumerate(positions_l2):
            node = Circle(radius=0.08, color=color, fill_opacity=0.3).move_to(pos)
            nodes.add(node)
            parent_idx = i // 2 + 1  # Connect to appropriate level 1 node
            lines.add(Line(nodes[parent_idx].get_bottom(), node.get_top(), color=color, stroke_width=2))
        
        # Level 3 (some nodes)
        positions_l3 = [
            center + LEFT*1.4 + DOWN*1.8, center + LEFT*1.0 + DOWN*1.8,
            center + LEFT*0.2 + DOWN*1.8, center + RIGHT*0.6 + DOWN*1.8,
            center + RIGHT*1.0 + DOWN*1.8, center + RIGHT*1.4 + DOWN*1.8
        ]
        for i, pos in enumerate(positions_l3):
            if i < 6:  # Only create some nodes to show complexity
                node = Circle(radius=0.06, color=color, fill_opacity=0.3).move_to(pos)
                nodes.add(node)
                parent_idx = i // 2 + 3  # Connect to appropriate level 2 node
                if parent_idx < len(nodes) - 1:
                    lines.add(Line(nodes[parent_idx].get_bottom(), node.get_top(), color=color, stroke_width=1))
        
        return VGroup(nodes, lines)
    
    def show_overfitting_prevention(self):
        """Show how cp prevents overfitting"""
        prevention_title = Text("cp Prevents Overfitting", font_size=28, color=ORANGE, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.complexity_title, prevention_title))
        
        # Create a graph showing training vs validation error
        axes = Axes(
            x_range=[0, 1, 0.2],
            y_range=[0, 1, 0.2],
            x_length=8,
            y_length=5,
            axis_config={"stroke_color": WHITE, "stroke_width": 2}
        ).move_to(ORIGIN)
        
        x_label = Text("Tree Complexity (1/cp)", font_size=16, color=WHITE).next_to(axes, DOWN)
        y_label = Text("Error", font_size=16, color=WHITE).next_to(axes, LEFT).rotate(PI/2)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Create error curves
        x_vals = np.linspace(0.1, 0.9, 50)
        
        # Training error decreases with complexity
        train_error = 0.8 - 0.6 * x_vals
        train_points = [axes.coords_to_point(x, y) for x, y in zip(x_vals, train_error)]
        train_curve = VMobject(color=BLUE, stroke_width=4)
        train_curve.set_points_smoothly(train_points)
        
        # Validation error: U-shaped
        val_error = 0.4 + 0.5 * (x_vals - 0.5)**2
        val_points = [axes.coords_to_point(x, y) for x, y in zip(x_vals, val_error)]
        val_curve = VMobject(color=RED, stroke_width=4)
        val_curve.set_points_smoothly(val_points)
        
        # Labels
        train_label = Text("Training Error", font_size=16, color=BLUE).next_to(axes, RIGHT).shift(UP*1)
        val_label = Text("Validation Error", font_size=16, color=RED).next_to(train_label, DOWN, buff=0.2)
        
        self.play(Create(train_curve), Write(train_label))
        self.wait(1)
        self.play(Create(val_curve), Write(val_label))
        self.wait(1)
        
        # Show optimal cp region
        optimal_x = 0.3
        optimal_line = DashedLine(
            axes.coords_to_point(optimal_x, 0),
            axes.coords_to_point(optimal_x, 1),
            color=GREEN,
            stroke_width=3
        )
        
        optimal_label = Text("Optimal cp", font_size=16, color=GREEN, weight=BOLD)
        optimal_label.next_to(optimal_line, UP, buff=0.2)
        
        self.play(Create(optimal_line), Write(optimal_label))
        
        # Show regions
        underfit_region = Rectangle(
            width=axes.x_axis.unit_size * optimal_x,
            height=axes.y_axis.get_length(),
            stroke_width=0,
            fill_color=YELLOW,
            fill_opacity=0.1
        ).move_to(axes.coords_to_point(optimal_x/2, 0.5))
        
        overfit_region = Rectangle(
            width=axes.x_axis.unit_size * (1 - optimal_x),
            height=axes.y_axis.get_length(),
            stroke_width=0,
            fill_color=RED,
            fill_opacity=0.1
        ).move_to(axes.coords_to_point((1 + optimal_x)/2, 0.5))
        
        underfit_text = Text("High cp\n(Underfit)", font_size=14, color=YELLOW, weight=BOLD)
        underfit_text.move_to(axes.coords_to_point(optimal_x/2, 0.8))
        
        overfit_text = Text("Low cp\n(Overfit)", font_size=14, color=RED, weight=BOLD)
        overfit_text.move_to(axes.coords_to_point((1 + optimal_x)/2, 0.8))
        
        self.play(
            FadeIn(underfit_region), FadeIn(overfit_region),
            Write(underfit_text), Write(overfit_text)
        )
        
        self.wait(3)
        self.play(FadeOut(
            axes, x_label, y_label, train_curve, val_curve,
            train_label, val_label, optimal_line, optimal_label,
            underfit_region, overfit_region, underfit_text, overfit_text
        ))
        self.prevention_title = prevention_title
    
    def show_summary(self):
        """Show final summary"""
        summary_title = Text("cp Parameter Summary", font_size=32, color=YELLOW, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.prevention_title, summary_title))
        
        # Create summary card
        summary_card = RoundedRectangle(
            corner_radius=0.2, width=12, height=5,
            stroke_color=WHITE, stroke_width=2,
            fill_color=BLACK, fill_opacity=0.95
        ).move_to(ORIGIN)
        
        # Summary content
        summary_content = VGroup(
            Text("Key Points:", font_size=24, color=YELLOW, weight=BOLD),
            VGroup(
                Text("🎛️ cp = complexity parameter controlling tree splits", font_size=18, color=WHITE),
                Text("🚪 Acts as threshold: only splits improving fit by > cp are made", font_size=18, color=WHITE),
                Text("📈 Higher cp → simpler trees (fewer splits)", font_size=18, color=WHITE),
                Text("📉 Lower cp → complex trees (more splits, overfitting risk)", font_size=18, color=WHITE),
                Text("⚖️ Optimal cp balances bias-variance tradeoff", font_size=18, color=WHITE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3),
            
            Text("Best Practice:", font_size=20, color=GREEN, weight=BOLD),
            Text("Use cross-validation to find cp that minimizes validation error", 
                 font_size=16, color=WHITE, slant=ITALIC)
        ).arrange(DOWN, buff=0.4).move_to(summary_card.get_center())
        
        self.play(FadeIn(summary_card), *[Write(item) for item in summary_content])
        
        # Final message
        final_message = Text(
            "Master cp tuning to control tree complexity and prevent overfitting!",
            font_size=20,
            color=YELLOW,
            weight=BOLD
        ).next_to(summary_card, DOWN, buff=0.8)
        
        self.play(Write(final_message))
        self.wait(3)