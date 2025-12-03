from manim import *
import numpy as np

class RecursiveBinarySplitting(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = "#1E1E2A"
        
        # Title
        title = Text("Recursive Binary Splitting", font_size=48, color=WHITE, weight=BOLD)
        title.to_edge(UP)
        subtitle = Text("Decision Tree Algorithm", font_size=32, color=YELLOW)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(Write(subtitle))
        self.wait(2)
        
        # Fade out title
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # Introduction
        self.show_introduction()
        
        # Show the algorithm steps
        self.show_algorithm_steps()
        
        # Demonstrate with example data
        self.show_example_splitting()
        
        # Show stopping criteria
        self.show_stopping_criteria()
        
        # Summary
        self.show_summary()

    def show_introduction(self):
        # Introduction section
        intro_title = Text("What is Recursive Binary Splitting?", font_size=36, color=WHITE, weight=BOLD)
        intro_title.to_edge(UP)
        
        intro_text = VGroup(
            Text("• Splits are made sequentially based on feature values", color=WHITE, font_size=24),
            Text("• Greedy: Choose split with greatest impurity reduction", color=GREEN, font_size=24),
            Text("• Top-down: Start from root and split downward", color=BLUE, font_size=24),
            Text("• Continue until stopping criterion is reached", color=RED, font_size=24),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        intro_text.next_to(intro_title, DOWN, buff=0.5)
        
        self.play(Write(intro_title))
        self.play(FadeIn(intro_text, shift=LEFT*0.3))
        self.wait(3)
        
        # Store for later
        self.intro_title = intro_title
        self.intro_text = intro_text

    def show_algorithm_steps(self):
        # Fade out introduction
        self.play(FadeOut(self.intro_text))
        
        # Algorithm title
        algo_title = Text("The Algorithm", font_size=36, color=WHITE, weight=BOLD)
        algo_title.to_edge(UP)
        self.play(Transform(self.intro_title, algo_title))
        
        # Create algorithm steps
        steps = VGroup()
        
        step1 = VGroup(
            Text("1. Start with all data at root node", color=WHITE, font_size=24, weight=BOLD),
            Text("   Calculate impurity (Gini/Entropy)", color=GRAY, font_size=20),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        
        step2 = VGroup(
            Text("2. For each feature and threshold:", color=WHITE, font_size=24, weight=BOLD),
            Text("   • Split data into two groups", color=GRAY, font_size=20),
            Text("   • Calculate impurity reduction", color=GRAY, font_size=20),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        
        step3 = VGroup(
            Text("3. Choose best split (greedy choice)", color=WHITE, font_size=24, weight=BOLD),
            Text("   • Maximum impurity reduction", color=GREEN, font_size=20),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        
        step4 = VGroup(
            Text("4. Create child nodes", color=WHITE, font_size=24, weight=BOLD),
            Text("   • Left child: ≤ threshold", color=BLUE, font_size=20),
            Text("   • Right child: > threshold", color=RED, font_size=20),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        
        step5 = VGroup(
            Text("5. Repeat recursively", color=WHITE, font_size=24, weight=BOLD),
            Text("   • Apply steps 1-4 to each child", color=GRAY, font_size=20),
            Text("   • Until stopping criterion met", color=GRAY, font_size=20),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        
        steps.add(step1, step2, step3, step4, step5)
        steps.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        steps.next_to(algo_title, DOWN, buff=0.5)
        
        # Animate steps appearing
        for i, step in enumerate(steps):
            self.play(FadeIn(step, shift=LEFT*0.3))
            self.wait(1)
        
        self.wait(2)
        
        # Store for later
        self.algo_title = algo_title
        self.steps = steps

    def show_example_splitting(self):
        # Fade out algorithm steps
        self.play(FadeOut(self.steps))
        
        # Example title
        example_title = Text("Example: House Price Prediction", font_size=36, color=WHITE, weight=BOLD)
        example_title.to_edge(UP)
        self.play(Transform(self.intro_title, example_title))
        
        # Create sample data
        self.create_sample_data()
        
        # Show first split
        self.show_first_split()
        
        # Show second split
        self.show_second_split()
        
        # Show final tree
        self.show_final_tree()

    def create_sample_data(self):
        # Create sample data table
        data_title = Text("Sample Data", font_size=24, color=YELLOW, weight=BOLD)
        data_title.to_edge(LEFT).shift(UP*2)
        
        # Sample data
        data = [
            ["House", "Size (sqft)", "Age (years)", "Price ($K)"],
            ["1", "1200", "5", "250"],
            ["2", "1500", "3", "300"],
            ["3", "800", "15", "180"],
            ["4", "2000", "2", "400"],
            ["5", "1000", "8", "220"],
            ["6", "1800", "1", "350"],
        ]
        
        # Create table
        table = VGroup()
        for i, row in enumerate(data):
            row_group = VGroup()
            for j, cell in enumerate(row):
                color = YELLOW if i == 0 else WHITE
                weight = BOLD if i == 0 else NORMAL
                text = Text(cell, font_size=16, color=color, weight=weight)
                row_group.add(text)
            row_group.arrange(RIGHT, buff=0.5)
            table.add(row_group)
        
        table.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        table.next_to(data_title, DOWN, buff=0.3)
        table.to_edge(LEFT, buff=0.5)
        
        self.play(Write(data_title))
        self.play(FadeIn(table, shift=LEFT*0.3))
        
        # Store for later
        self.data_title = data_title
        self.table = table

    def show_first_split(self):
        # Split evaluation title
        split_title = Text("Step 1: Evaluate All Possible Splits", font_size=28, color=GREEN, weight=BOLD)
        split_title.to_edge(RIGHT).shift(UP*2)
        
        # Show split options
        split_options = VGroup(
            Text("Size ≤ 1200: Impurity reduction = 0.15", color=WHITE, font_size=18),
            Text("Size ≤ 1500: Impurity reduction = 0.25", color=GREEN, font_size=18, weight=BOLD),
            Text("Size ≤ 1800: Impurity reduction = 0.20", color=WHITE, font_size=18),
            Text("Age ≤ 3: Impurity reduction = 0.10", color=WHITE, font_size=18),
            Text("Age ≤ 8: Impurity reduction = 0.12", color=WHITE, font_size=18),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        split_options.next_to(split_title, DOWN, buff=0.3)
        split_options.to_edge(RIGHT, buff=0.5)
        
        self.play(Write(split_title))
        self.play(FadeIn(split_options, shift=RIGHT*0.3))
        
        # Highlight best split
        best_split = Text("Best Split: Size ≤ 1500", font_size=20, color=GREEN, weight=BOLD)
        best_split.next_to(split_options, DOWN, buff=0.3)
        self.play(Write(best_split))
        
        self.wait(2)
        
        # Store for later
        self.split_title = split_title
        self.split_options = split_options
        self.best_split = best_split

    def show_second_split(self):
        # Fade out split evaluation
        self.play(FadeOut(self.split_title), FadeOut(self.split_options), FadeOut(self.best_split))
        
        # Create tree visualization
        tree_title = Text("Building the Tree", font_size=28, color=BLUE, weight=BOLD)
        tree_title.to_edge(RIGHT).shift(UP*2)
        
        # Root node
        root_node = Rectangle(width=2, height=0.8, color=WHITE)
        root_node.move_to(ORIGIN)
        root_text = Text("Size ≤ 1500?", font_size=16, color=WHITE)
        root_text.move_to(root_node.get_center())
        
        # Left child (≤ 1500)
        left_node = Rectangle(width=1.5, height=0.6, color=BLUE)
        left_node.move_to(root_node.get_center() + LEFT*2 + DOWN*1.5)
        left_text = Text("≤ 1500", font_size=14, color=WHITE)
        left_text.move_to(left_node.get_center())
        
        # Right child (> 1500)
        right_node = Rectangle(width=1.5, height=0.6, color=RED)
        right_node.move_to(root_node.get_center() + RIGHT*2 + DOWN*1.5)
        right_text = Text("> 1500", font_size=14, color=WHITE)
        right_text.move_to(right_node.get_center())
        
        # Arrows
        left_arrow = Arrow(root_node.get_bottom(), left_node.get_top(), color=WHITE)
        right_arrow = Arrow(root_node.get_bottom(), right_node.get_top(), color=WHITE)
        
        # Create tree
        tree = VGroup(root_node, root_text, left_arrow, left_node, left_text, 
                     right_arrow, right_node, right_text)
        tree.scale(0.8).move_to(RIGHT*3)
        
        self.play(Write(tree_title))
        self.play(Create(root_node), Write(root_text))
        self.wait(1)
        self.play(Create(left_arrow), Create(left_node), Write(left_text))
        self.play(Create(right_arrow), Create(right_node), Write(right_text))
        
        # Show data distribution
        data_dist = VGroup(
            Text("Left Node (≤ 1500):", font_size=16, color=BLUE, weight=BOLD),
            Text("Houses 1, 3, 5", font_size=14, color=WHITE),
            Text("Avg Price: $217K", font_size=14, color=WHITE),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        data_dist.next_to(left_node, DOWN, buff=0.3)
        
        data_dist2 = VGroup(
            Text("Right Node (> 1500):", font_size=16, color=RED, weight=BOLD),
            Text("Houses 2, 4, 6", font_size=14, color=WHITE),
            Text("Avg Price: $350K", font_size=14, color=WHITE),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        data_dist2.next_to(right_node, DOWN, buff=0.3)
        
        self.play(FadeIn(data_dist), FadeIn(data_dist2))
        
        self.wait(2)
        
        # Store for later
        self.tree_title = tree_title
        self.tree = tree
        self.data_dist = data_dist
        self.data_dist2 = data_dist2

    def show_final_tree(self):
        # Fade out current tree
        self.play(FadeOut(self.tree), FadeOut(self.data_dist), FadeOut(self.data_dist2))
        
        # Final tree title
        final_title = Text("Final Decision Tree", font_size=28, color=GREEN, weight=BOLD)
        final_title.to_edge(RIGHT).shift(UP*2)
        self.play(Transform(self.tree_title, final_title))
        
        # Create complete tree
        self.create_complete_tree()
        
        # Show predictions
        self.show_predictions()

    def create_complete_tree(self):
        # Root node
        root_node = Rectangle(width=2, height=0.8, color=WHITE)
        root_node.move_to(ORIGIN)
        root_text = Text("Size ≤ 1500?", font_size=16, color=WHITE)
        root_text.move_to(root_node.get_center())
        
        # Level 1 nodes
        left_node = Rectangle(width=1.5, height=0.6, color=BLUE)
        left_node.move_to(root_node.get_center() + LEFT*2 + DOWN*1.5)
        left_text = Text("Age ≤ 8?", font_size=14, color=WHITE)
        left_text.move_to(left_node.get_center())
        
        right_node = Rectangle(width=1.5, height=0.6, color=RED)
        right_node.move_to(root_node.get_center() + RIGHT*2 + DOWN*1.5)
        right_text = Text("Age ≤ 2?", font_size=14, color=WHITE)
        right_text.move_to(right_node.get_center())
        
        # Level 2 nodes (leaves)
        leaf1 = Rectangle(width=1.2, height=0.5, color=GREEN)
        leaf1.move_to(left_node.get_center() + LEFT*1.5 + DOWN*1.2)
        leaf1_text = Text("$180K", font_size=12, color=WHITE)
        leaf1_text.move_to(leaf1.get_center())
        
        leaf2 = Rectangle(width=1.2, height=0.5, color=GREEN)
        leaf2.move_to(left_node.get_center() + RIGHT*1.5 + DOWN*1.2)
        leaf2_text = Text("$235K", font_size=12, color=WHITE)
        leaf2_text.move_to(leaf2.get_center())
        
        leaf3 = Rectangle(width=1.2, height=0.5, color=GREEN)
        leaf3.move_to(right_node.get_center() + LEFT*1.5 + DOWN*1.2)
        leaf3_text = Text("$400K", font_size=12, color=WHITE)
        leaf3_text.move_to(leaf3.get_center())
        
        leaf4 = Rectangle(width=1.2, height=0.5, color=GREEN)
        leaf4.move_to(right_node.get_center() + RIGHT*1.5 + DOWN*1.2)
        leaf4_text = Text("$300K", font_size=12, color=WHITE)
        leaf4_text.move_to(leaf4.get_center())
        
        # Arrows
        arrows = VGroup()
        arrows.add(Arrow(root_node.get_bottom(), left_node.get_top(), color=WHITE))
        arrows.add(Arrow(root_node.get_bottom(), right_node.get_top(), color=WHITE))
        arrows.add(Arrow(left_node.get_bottom(), leaf1.get_top(), color=WHITE))
        arrows.add(Arrow(left_node.get_bottom(), leaf2.get_top(), color=WHITE))
        arrows.add(Arrow(right_node.get_bottom(), leaf3.get_top(), color=WHITE))
        arrows.add(Arrow(right_node.get_bottom(), leaf4.get_top(), color=WHITE))
        
        # Create complete tree
        complete_tree = VGroup(
            root_node, root_text, left_node, left_text, right_node, right_text,
            leaf1, leaf1_text, leaf2, leaf2_text, leaf3, leaf3_text, leaf4, leaf4_text,
            arrows
        )
        complete_tree.scale(0.7).move_to(RIGHT*3)
        
        # Animate tree building
        self.play(Create(root_node), Write(root_text))
        self.wait(0.5)
        self.play(Create(arrows[0]), Create(left_node), Write(left_text))
        self.play(Create(arrows[1]), Create(right_node), Write(right_text))
        self.wait(0.5)
        self.play(Create(arrows[2]), Create(leaf1), Write(leaf1_text))
        self.play(Create(arrows[3]), Create(leaf2), Write(leaf2_text))
        self.play(Create(arrows[4]), Create(leaf3), Write(leaf3_text))
        self.play(Create(arrows[5]), Create(leaf4), Write(leaf4_text))
        
        self.wait(2)
        
        # Store for later
        self.complete_tree = complete_tree

    def show_predictions(self):
        # Prediction example
        pred_title = Text("Making Predictions", font_size=24, color=YELLOW, weight=BOLD)
        pred_title.next_to(self.complete_tree, DOWN, buff=0.5)
        
        pred_example = VGroup(
            Text("New House: Size = 1600 sqft, Age = 4 years", font_size=16, color=WHITE),
            Text("Path: Size > 1500 → Age > 2 → Predicted Price: $300K", font_size=16, color=GREEN),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        pred_example.next_to(pred_title, DOWN, buff=0.3)
        
        self.play(Write(pred_title))
        self.play(FadeIn(pred_example, shift=UP*0.3))
        
        self.wait(2)
        
        # Store for later
        self.pred_title = pred_title
        self.pred_example = pred_example

    def show_stopping_criteria(self):
        # Fade out example
        self.play(
            FadeOut(self.data_title), FadeOut(self.table),
            FadeOut(self.tree_title), FadeOut(self.complete_tree),
            FadeOut(self.pred_title), FadeOut(self.pred_example)
        )
        
        # Stopping criteria title
        stop_title = Text("Stopping Criteria", font_size=36, color=WHITE, weight=BOLD)
        stop_title.to_edge(UP)
        self.play(Transform(self.intro_title, stop_title))
        
        # Stopping criteria
        criteria = VGroup(
            Text("1. Maximum tree depth reached", color=WHITE, font_size=24),
            Text("2. Minimum samples per node", color=WHITE, font_size=24),
            Text("3. No impurity reduction possible", color=WHITE, font_size=24),
            Text("4. All samples belong to same class", color=WHITE, font_size=24),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        criteria.next_to(stop_title, DOWN, buff=0.8)
        
        self.play(FadeIn(criteria, shift=LEFT*0.3))
        self.wait(3)
        
        # Store for later
        self.stop_title = stop_title
        self.criteria = criteria

    def show_summary(self):
        # Fade out stopping criteria
        self.play(FadeOut(self.criteria))
        
        # Summary title
        summary_title = Text("Key Takeaways", font_size=36, color=WHITE, weight=BOLD)
        summary_title.to_edge(UP)
        self.play(Transform(self.intro_title, summary_title))
        
        # Summary points
        summary_points = VGroup(
            Text("• Greedy algorithm: Choose best split at each step", color=GREEN, font_size=24),
            Text("• Top-down approach: Build tree from root to leaves", color=BLUE, font_size=24),
            Text("• Binary splits: Each node has exactly two children", color=WHITE, font_size=24),
            Text("• Recursive: Apply same process to each child node", color=WHITE, font_size=24),
            Text("• Stopping criteria prevent overfitting", color=RED, font_size=24),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        summary_points.next_to(summary_title, DOWN, buff=0.5)
        
        self.play(FadeIn(summary_points, shift=LEFT*0.3))
        self.wait(3)
        
        # Final message
        final_message = Text(
            "Recursive binary splitting creates\ninterpretable decision boundaries",
            font_size=28, color=YELLOW, weight=BOLD
        )
        final_message.move_to(ORIGIN)
        
        self.play(
            FadeOut(self.intro_title),
            FadeOut(summary_points)
        )
        self.play(Write(final_message))
        self.wait(3)
