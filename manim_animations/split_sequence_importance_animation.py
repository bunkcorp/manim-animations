from manim import *
import numpy as np

class SplitSequenceImportance(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = "#1E1E2A"
        
        # Title
        title = Text("Decision Tree Split Sequence Importance", font_size=40, color=WHITE, weight=BOLD)
        title.to_edge(UP)
        subtitle = Text("Why Early Splits Matter", font_size=28, color=YELLOW)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(Write(subtitle))
        self.wait(2)
        
        # Fade out title
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # Create the main visualization
        self.create_main_visualization()
        
        # Show split sequence
        self.show_split_sequence()
        
        # Demonstrate importance
        self.demonstrate_importance()
        
        # Summary
        self.show_summary()

    def create_main_visualization(self):
        # Create coordinate system
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": WHITE, "stroke_width": 2},
            x_axis_config={"numbers_to_include": np.arange(-4, 5, 1)},
            y_axis_config={"numbers_to_include": np.arange(-3, 4, 1)},
        )
        
        # Add axis labels using MathTex
        x_label = MathTex("X_1", font_size=24, color=WHITE).next_to(axes.x_axis, DOWN)
        y_label = MathTex("X_2", font_size=24, color=WHITE).next_to(axes.y_axis, LEFT).rotate(90*DEGREES)
        
        # Create data points with 3 classes
        np.random.seed(42)
        n_points = 60
        
        # Class 1 (Red) - Top right
        class1_x = np.random.normal(2, 0.5, n_points//3)
        class1_y = np.random.normal(1.5, 0.5, n_points//3)
        
        # Class 2 (Blue) - Bottom left
        class2_x = np.random.normal(-2, 0.5, n_points//3)
        class2_y = np.random.normal(-1.5, 0.5, n_points//3)
        
        # Class 3 (Green) - Center
        class3_x = np.random.normal(0, 0.8, n_points//3)
        class3_y = np.random.normal(0, 0.8, n_points//3)
        
        # Combine all data
        all_x = np.concatenate([class1_x, class2_x, class3_x])
        all_y = np.concatenate([class1_y, class2_y, class3_y])
        
        # Create dots with different colors
        dots = VGroup()
        colors = [RED, BLUE, GREEN]
        
        for i in range(len(all_x)):
            color = colors[i // (n_points//3)]
            dot = Dot(axes.coords_to_point(all_x[i], all_y[i]), color=color, radius=0.05)
            dots.add(dot)
        
        # Create the plot group
        plot_group = VGroup(axes, x_label, y_label, dots)
        plot_group.move_to(LEFT * 2)
        
        # Animate plot creation
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(LaggedStart(*[FadeIn(dot, scale=0.5) for dot in dots], lag_ratio=0.01))
        
        # Add legend
        legend = VGroup(
            Text("Class 1", font_size=16, color=RED),
            Text("Class 2", font_size=16, color=BLUE),
            Text("Class 3", font_size=16, color=GREEN),
        ).arrange(DOWN, buff=0.2)
        legend.to_edge(LEFT).shift(DOWN * 2)
        
        self.play(FadeIn(legend))
        
        # Store for later
        self.axes = axes
        self.dots = dots
        self.legend = legend
        self.all_x = all_x
        self.all_y = all_y
        self.plot_group = plot_group

    def show_split_sequence(self):
        # Split sequence title
        split_title = Text("Split Sequence", font_size=32, color=WHITE, weight=BOLD)
        split_title.to_edge(UP)
        
        # Data points counter
        counter = Text("Data points affected: 60", font_size=20, color=YELLOW, weight=BOLD)
        counter.to_edge(RIGHT).shift(UP * 2)
        
        self.play(Write(split_title), Write(counter))
        
        # Create tree structure on the right
        tree_group = VGroup()
        tree_group.to_edge(RIGHT).shift(DOWN * 1)
        
        # Split 1: X1 < 0 (vertical line)
        split1_text = Text("Split 1: X₁ < 0", font_size=18, color=GREEN, weight=BOLD)
        split1_text.to_edge(RIGHT).shift(UP * 1)
        
        # Draw vertical line
        vertical_line = Line(
            start=self.axes.coords_to_point(0, -3),
            end=self.axes.coords_to_point(0, 3),
            color=GREEN,
            stroke_width=4
        )
        
        self.play(Write(split1_text))
        self.play(Create(vertical_line, rate_func=smooth))
        
        # Update counter
        left_count = sum(1 for x in self.all_x if x < 0)
        right_count = sum(1 for x in self.all_x if x >= 0)
        counter_new = Text(f"Left: {left_count}, Right: {right_count}", font_size=18, color=YELLOW)
        counter_new.to_edge(RIGHT).shift(UP * 2)
        self.play(Transform(counter, counter_new))
        
        # Create tree node
        root_node = Rectangle(width=2, height=0.6, color=GREEN)
        root_text = MathTex("X_1 < 0", font_size=16, color=WHITE)
        root_node.move_to(tree_group.get_center())
        root_text.move_to(root_node.get_center())
        
        self.play(Create(root_node), Write(root_text))
        
        # Add arrow from tree to split
        arrow1 = Arrow(root_node.get_left(), vertical_line.get_center(), color=GREEN, buff=0.2)
        self.play(Create(arrow1))
        
        self.wait(1)
        
        # Split 2: X2 < 0 (horizontal line in left region)
        split2_text = Text("Split 2: X₂ < 0", font_size=18, color=BLUE, weight=BOLD)
        split2_text.next_to(split1_text, DOWN, buff=0.3)
        
        # Draw horizontal line in left region
        horizontal_line = Line(
            start=self.axes.coords_to_point(-4, 0),
            end=self.axes.coords_to_point(0, 0),
            color=BLUE,
            stroke_width=3
        )
        
        self.play(Write(split2_text))
        self.play(Create(horizontal_line, rate_func=smooth))
        
        # Update counter for left region splits
        bottom_left = sum(1 for i, (x, y) in enumerate(zip(self.all_x, self.all_y)) if x < 0 and y < 0)
        top_left = sum(1 for i, (x, y) in enumerate(zip(self.all_x, self.all_y)) if x < 0 and y >= 0)
        counter_new2 = Text(f"Bottom-Left: {bottom_left}, Top-Left: {top_left}, Right: {right_count}", font_size=16, color=YELLOW)
        counter_new2.to_edge(RIGHT).shift(UP * 2)
        self.play(Transform(counter, counter_new2))
        
        # Create child nodes
        left_node = Rectangle(width=1.5, height=0.5, color=BLUE)
        left_text = MathTex("X_2 < 0", font_size=14, color=WHITE)
        left_node.move_to(root_node.get_center() + LEFT * 1.5 + DOWN * 1)
        left_text.move_to(left_node.get_center())
        
        right_node = Rectangle(width=1.5, height=0.5, color=RED)
        right_text = MathTex("X_1 \\geq 0", font_size=14, color=WHITE)
        right_node.move_to(root_node.get_center() + RIGHT * 1.5 + DOWN * 1)
        right_text.move_to(right_node.get_center())
        
        # Arrows from root to children
        left_arrow = Arrow(root_node.get_bottom(), left_node.get_top(), color=WHITE)
        right_arrow = Arrow(root_node.get_bottom(), right_node.get_top(), color=WHITE)
        
        self.play(Create(left_node), Write(left_text), Create(left_arrow))
        self.play(Create(right_node), Write(right_text), Create(right_arrow))
        
        # Add arrow from left node to horizontal split
        arrow2 = Arrow(left_node.get_left(), horizontal_line.get_center(), color=BLUE, buff=0.2)
        self.play(Create(arrow2))
        
        self.wait(1)
        
        # Split 3: X1 < 1.5 (vertical line in right region)
        split3_text = Text("Split 3: X₁ < 1.5", font_size=18, color=RED, weight=BOLD)
        split3_text.next_to(split2_text, DOWN, buff=0.3)
        
        # Draw vertical line in right region
        vertical_line2 = Line(
            start=self.axes.coords_to_point(1.5, -3),
            end=self.axes.coords_to_point(1.5, 3),
            color=RED,
            stroke_width=2
        )
        
        self.play(Write(split3_text))
        self.play(Create(vertical_line2, rate_func=smooth))
        
        # Update counter for right region splits
        right_left = sum(1 for i, (x, y) in enumerate(zip(self.all_x, self.all_y)) if x >= 0 and x < 1.5)
        right_right = sum(1 for i, (x, y) in enumerate(zip(self.all_x, self.all_y)) if x >= 1.5)
        counter_new3 = Text(f"Bottom-Left: {bottom_left}, Top-Left: {top_left}, Right-Left: {right_left}, Right-Right: {right_right}", font_size=14, color=YELLOW)
        counter_new3.to_edge(RIGHT).shift(UP * 2)
        self.play(Transform(counter, counter_new3))
        
        # Create leaf nodes
        leaf1 = Rectangle(width=1.2, height=0.4, color=GREEN)
        leaf1_text = Text("Class 2", font_size=12, color=WHITE)
        leaf1.move_to(left_node.get_center() + LEFT * 1.2 + DOWN * 0.8)
        leaf1_text.move_to(leaf1.get_center())
        
        leaf2 = Rectangle(width=1.2, height=0.4, color=GREEN)
        leaf2_text = Text("Class 3", font_size=12, color=WHITE)
        leaf2.move_to(left_node.get_center() + RIGHT * 1.2 + DOWN * 0.8)
        leaf2_text.move_to(leaf2.get_center())
        
        leaf3 = Rectangle(width=1.2, height=0.4, color=GREEN)
        leaf3_text = Text("Class 3", font_size=12, color=WHITE)
        leaf3.move_to(right_node.get_center() + LEFT * 1.2 + DOWN * 0.8)
        leaf3_text.move_to(leaf3.get_center())
        
        leaf4 = Rectangle(width=1.2, height=0.4, color=GREEN)
        leaf4_text = Text("Class 1", font_size=12, color=WHITE)
        leaf4.move_to(right_node.get_center() + RIGHT * 1.2 + DOWN * 0.8)
        leaf4_text.move_to(leaf4.get_center())
        
        # Arrows to leaves
        leaf_arrows = VGroup()
        leaf_arrows.add(Arrow(left_node.get_bottom(), leaf1.get_top(), color=WHITE))
        leaf_arrows.add(Arrow(left_node.get_bottom(), leaf2.get_top(), color=WHITE))
        leaf_arrows.add(Arrow(right_node.get_bottom(), leaf3.get_top(), color=WHITE))
        leaf_arrows.add(Arrow(right_node.get_bottom(), leaf4.get_top(), color=WHITE))
        
        self.play(Create(leaf1), Write(leaf1_text), Create(leaf_arrows[0]))
        self.play(Create(leaf2), Write(leaf2_text), Create(leaf_arrows[1]))
        self.play(Create(leaf3), Write(leaf3_text), Create(leaf_arrows[2]))
        self.play(Create(leaf4), Write(leaf4_text), Create(leaf_arrows[3]))
        
        # Add arrow from right node to second vertical split
        arrow3 = Arrow(right_node.get_left(), vertical_line2.get_center(), color=RED, buff=0.2)
        self.play(Create(arrow3))
        
        self.wait(2)
        
        # Store for later
        self.split_title = split_title
        self.counter = counter
        self.vertical_line = vertical_line
        self.horizontal_line = horizontal_line
        self.vertical_line2 = vertical_line2
        self.root_node = root_node
        self.root_text = root_text
        self.left_node = left_node
        self.left_text = left_text
        self.right_node = right_node
        self.right_text = right_text
        self.leaf1 = leaf1
        self.leaf1_text = leaf1_text
        self.leaf2 = leaf2
        self.leaf2_text = leaf2_text
        self.leaf3 = leaf3
        self.leaf3_text = leaf3_text
        self.leaf4 = leaf4
        self.leaf4_text = leaf4_text
        self.arrow1 = arrow1
        self.arrow2 = arrow2
        self.arrow3 = arrow3
        self.leaf_arrows = leaf_arrows

    def demonstrate_importance(self):
        # Fade out split sequence elements
        self.play(
            FadeOut(self.split_title), FadeOut(self.counter),
            FadeOut(self.arrow1), FadeOut(self.arrow2), FadeOut(self.arrow3),
            FadeOut(self.leaf_arrows)
        )
        
        # Importance title
        importance_title = Text("Why Split Sequence Matters", font_size=32, color=WHITE, weight=BOLD)
        importance_title.to_edge(UP)
        
        # Highlight early splits
        early_split_highlight = SurroundingRectangle(self.vertical_line, color=YELLOW, buff=0.1)
        early_split_highlight.set_stroke(width=3)
        
        # Add emphasis text
        emphasis_text = Text("Early splits affect MORE data points!", font_size=20, color=YELLOW, weight=BOLD)
        emphasis_text.next_to(self.vertical_line, UP, buff=0.5)
        
        self.play(Transform(self.split_title, importance_title))
        self.play(Create(early_split_highlight))
        self.play(Write(emphasis_text))
        
        # Show data point counts
        left_count = sum(1 for x in self.all_x if x < 0)
        right_count = sum(1 for x in self.all_x if x >= 0)
        
        count_text = VGroup(
            Text(f"Split 1 affects ALL {len(self.all_x)} points", font_size=18, color=GREEN, weight=BOLD),
            Text(f"Left region: {left_count} points", font_size=16, color=BLUE),
            Text(f"Right region: {right_count} points", font_size=16, color=RED),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        count_text.to_edge(RIGHT).shift(UP * 1)
        
        self.play(FadeIn(count_text, shift=RIGHT*0.3))
        
        # Show later splits affect fewer points
        later_split_text = VGroup(
            Text("Later splits affect FEWER points", font_size=18, color=RED, weight=BOLD),
            Text("Split 2 affects only left region", font_size=16, color=BLUE),
            Text("Split 3 affects only right region", font_size=16, color=RED),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        later_split_text.next_to(count_text, DOWN, buff=0.5)
        
        self.play(FadeIn(later_split_text, shift=RIGHT*0.3))
        
        # Highlight the difference
        comparison_text = Text(
            "Early splits create the FOUNDATION\nfor all subsequent decisions",
            font_size=20, color=YELLOW, weight=BOLD
        )
        comparison_text.next_to(later_split_text, DOWN, buff=0.5)
        
        self.play(Write(comparison_text))
        
        self.wait(3)
        
        # Store for later
        self.importance_title = importance_title
        self.early_split_highlight = early_split_highlight
        self.emphasis_text = emphasis_text
        self.count_text = count_text
        self.later_split_text = later_split_text
        self.comparison_text = comparison_text

    def show_summary(self):
        # Fade out importance demonstration
        self.play(
            FadeOut(self.early_split_highlight), FadeOut(self.emphasis_text),
            FadeOut(self.count_text), FadeOut(self.later_split_text), FadeOut(self.comparison_text)
        )
        
        # Summary title
        summary_title = Text("Key Insights", font_size=36, color=WHITE, weight=BOLD)
        summary_title.to_edge(UP)
        self.play(Transform(self.importance_title, summary_title))
        
        # Summary points
        summary_points = VGroup(
            Text("• Early splits affect the MOST data points", color=GREEN, font_size=24, weight=BOLD),
            Text("• They create the foundational structure", color=BLUE, font_size=24),
            Text("• Later splits refine smaller regions", color=RED, font_size=24),
            Text("• Split order determines tree efficiency", color=WHITE, font_size=24),
            Text("• Greedy algorithms prioritize early splits", color=YELLOW, font_size=24),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        summary_points.next_to(summary_title, DOWN, buff=0.5)
        
        self.play(FadeIn(summary_points, shift=LEFT*0.3))
        self.wait(3)
        
        # Final message
        final_message = Text(
            "Split sequence determines\nthe tree's effectiveness",
            font_size=28, color=YELLOW, weight=BOLD
        )
        final_message.move_to(ORIGIN)
        
        self.play(
            FadeOut(self.importance_title),
            FadeOut(summary_points)
        )
        self.play(Write(final_message))
        self.wait(3)
