from manim import *
import numpy as np

class DecisionTreeHyperparameters(Scene):
    def construct(self):
        # Title
        title = Text("Decision Tree Hyperparameters", font_size=48, color=BLUE)
        subtitle = Text("Controlling Tree Construction", font_size=32, color=GRAY)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.3)
        title_group.to_edge(UP)
        
        self.play(Write(title))
        self.play(Write(subtitle))
        self.wait(1)
        
        # Introduction
        intro_text = Text(
            "Three key hyperparameters control how decision trees are built:",
            font_size=28, color=WHITE
        ).next_to(title_group, DOWN, buff=1)
        
        self.play(Write(intro_text))
        self.wait(2)
        
        # Create the three parameter sections
        self.create_minsplit_section()
        self.create_minbucket_section()
        self.create_complexity_parameter_section()
        
        # Summary
        self.create_summary()
    
    def create_minsplit_section(self):
        # Clear previous content
        self.clear()
        
        # Title for minsplit
        title = Text("1. minsplit", font_size=40, color=YELLOW)
        title.to_edge(UP)
        
        # Definition
        definition = Text(
            "Minimum number of observations in a node before it can be split",
            font_size=24, color=WHITE, line_spacing=1.2
        ).next_to(title, DOWN, buff=0.5)
        
        self.play(Write(title))
        self.play(Write(definition))
        self.wait(1)
        
        # Visual example
        self.create_minsplit_visual_example(definition)
    
    def create_minsplit_visual_example(self, definition):
        # Create a simple dataset visualization
        data_points = VGroup()
        colors = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE]
        
        # Create sample data points
        for i in range(12):
            point = Circle(radius=0.1, fill_color=colors[i % len(colors)], fill_opacity=0.8)
            point.move_to([(i % 4 - 1.5) * 0.8, (i // 4 - 1) * 0.8, 0])
            data_points.add(point)
        
        data_points.next_to(definition, DOWN, buff=1)
        
        # Show data points
        self.play(FadeIn(data_points))
        self.wait(1)
        
        # Show different minsplit values
        minsplit_values = [2, 4, 6]
        current_y = -2
        
        for i, minsplit in enumerate(minsplit_values):
            n = 12  # total points
            
            # Create tree node
            node = Rectangle(width=2, height=0.8, color=WHITE)
            node.move_to([-3, current_y, 0])
            
            # Node label
            node_label = Text(f"Node\n{n} points", font_size=16)
            node_label.move_to(node.get_center())
            
            # minsplit indicator
            minsplit_text = Text(f"minsplit = {minsplit}", font_size=20, color=YELLOW)
            minsplit_text.move_to([2, current_y, 0])
            
            # Decision arrow
            if n >= minsplit:
                arrow = Arrow(start=node.get_right(), end=minsplit_text.get_left(), color=GREEN)
                decision = Text("CAN SPLIT", font_size=16, color=GREEN)
            else:
                arrow = Arrow(start=node.get_right(), end=minsplit_text.get_left(), color=RED)
                decision = Text("CANNOT SPLIT", font_size=16, color=RED)
            
            decision.next_to(arrow, UP)
            
            self.play(
                Create(node),
                Write(node_label),
                Write(minsplit_text),
                Create(arrow),
                Write(decision)
            )
            
            current_y -= 1.5
            self.wait(1)
        
        self.wait(2)
    
    def create_minbucket_section(self):
        # Clear previous content
        self.clear()
        
        # Title for minbucket
        title = Text("2. minbucket", font_size=40, color=GREEN)
        title.to_edge(UP)
        
        # Definition
        definition = Text(
            "Minimum number of observations in a terminal node",
            font_size=24, color=WHITE, line_spacing=1.2
        ).next_to(title, DOWN, buff=0.5)
        
        self.play(Write(title))
        self.play(Write(definition))
        self.wait(1)
        
        # Visual example
        self.create_minbucket_visual_example()
    
    def create_minbucket_visual_example(self):
        # Create a tree structure
        root = Rectangle(width=2, height=0.8, color=WHITE)
        root.move_to([0, 2, 0])
        root_label = Text("Root\n12 points", font_size=16)
        root_label.move_to(root.get_center())
        
        # Split line
        split_line = Line(start=[-1, 1.6, 0], end=[1, 1.6, 0], color=YELLOW)
        
        # Left child
        left_child = Rectangle(width=1.5, height=0.6, color=WHITE)
        left_child.move_to([-1.5, 0.5, 0])
        left_label = Text("Left\n3 points", font_size=14)
        left_label.move_to(left_child.get_center())
        
        # Right child
        right_child = Rectangle(width=1.5, height=0.6, color=WHITE)
        right_child.move_to([1.5, 0.5, 0])
        right_label = Text("Right\n9 points", font_size=14)
        right_label.move_to(right_child.get_center())
        
        # Connect nodes
        left_line = Line(start=root.get_bottom(), end=left_child.get_top(), color=WHITE)
        right_line = Line(start=root.get_bottom(), end=right_child.get_top(), color=WHITE)
        
        # Show tree
        self.play(Create(root), Write(root_label))
        self.wait(1)
        self.play(Create(split_line))
        self.wait(1)
        self.play(
            Create(left_line), Create(right_line),
            Create(left_child), Create(right_child),
            Write(left_label), Write(right_label)
        )
        self.wait(1)
        
        # Show minbucket constraints
        minbucket_values = [1, 3, 5]
        current_y = -2
        
        for i, minbucket in enumerate(minbucket_values):
            # Left child evaluation
            left_eval = Text(f"Left: 3 points", font_size=16)
            left_eval.move_to([-3, current_y, 0])
            
            # Right child evaluation
            right_eval = Text(f"Right: 9 points", font_size=16)
            right_eval.move_to([3, current_y, 0])
            
            # minbucket indicator
            minbucket_text = Text(f"minbucket = {minbucket}", font_size=20, color=GREEN)
            minbucket_text.move_to([0, current_y - 0.8, 0])
            
            # Decisions
            left_decision = Text("VALID" if 3 >= minbucket else "INVALID", 
                               font_size=16, color=GREEN if 3 >= minbucket else RED)
            left_decision.move_to([-3, current_y - 0.8, 0])
            
            right_decision = Text("VALID" if 9 >= minbucket else "INVALID", 
                                font_size=16, color=GREEN if 9 >= minbucket else RED)
            right_decision.move_to([3, current_y - 0.8, 0])
            
            self.play(
                Write(left_eval), Write(right_eval),
                Write(minbucket_text),
                Write(left_decision), Write(right_decision)
            )
            
            current_y -= 1.2
            self.wait(1)
        
        self.wait(2)
    
    def create_complexity_parameter_section(self):
        # Clear previous content
        self.clear()
        
        # Title for complexity parameter
        title = Text("3. cp (Complexity Parameter)", font_size=40, color=PURPLE)
        title.to_edge(UP)
        
        # Definition
        definition = Text(
            "Minimum improvement in model fit required to make a split",
            font_size=24, color=WHITE, line_spacing=1.2
        ).next_to(title, DOWN, buff=0.5)
        
        self.play(Write(title))
        self.play(Write(definition))
        self.wait(1)
        
        # Visual example
        self.create_cp_visual_example()
    
    def create_cp_visual_example(self):
        # Create a simple tree with split evaluation
        root = Rectangle(width=2, height=0.8, color=WHITE)
        root.move_to([0, 2, 0])
        root_label = Text("Root\nImpurity: 0.5", font_size=16)
        root_label.move_to(root.get_center())
        
        # Show potential split
        split_line = DashedLine(start=[-1, 1.6, 0], end=[1, 1.6, 0], color=YELLOW)
        
        # Left child
        left_child = Rectangle(width=1.5, height=0.6, color=WHITE)
        left_child.move_to([-1.5, 0.5, 0])
        left_label = Text("Left\nImpurity: 0.3", font_size=14)
        left_label.move_to(left_child.get_center())
        
        # Right child
        right_child = Rectangle(width=1.5, height=0.6, color=WHITE)
        right_child.move_to([1.5, 0.5, 0])
        right_label = Text("Right\nImpurity: 0.2", font_size=14)
        right_label.move_to(right_child.get_center())
        
        # Show tree
        self.play(Create(root), Write(root_label))
        self.wait(1)
        self.play(Create(split_line))
        self.wait(1)
        self.play(
            Create(left_child), Create(right_child),
            Write(left_label), Write(right_label)
        )
        self.wait(1)
        
        # Calculate improvement
        improvement_formula = MathTex(
            r"\text{Improvement} = \text{Parent Impurity} - \text{Weighted Child Impurity}",
            font_size=20
        )
        improvement_formula.move_to([0, -1, 0])
        
        calculation = MathTex(
            r"= 0.5 - (0.5 \times 0.3 + 0.5 \times 0.2) = 0.25",
            font_size=20
        )
        calculation.move_to([0, -1.5, 0])
        
        self.play(Write(improvement_formula))
        self.wait(1)
        self.play(Write(calculation))
        self.wait(1)
        
        # Show different cp values
        cp_values = [0.1, 0.2, 0.3]
        current_y = -3
        
        for i, cp in enumerate(cp_values):
            cp_text = Text(f"cp = {cp}", font_size=20, color=PURPLE)
            cp_text.move_to([-2, current_y, 0])
            
            # Decision
            decision = Text("SPLIT" if 0.25 >= cp else "NO SPLIT", 
                          font_size=20, color=GREEN if 0.25 >= cp else RED)
            decision.move_to([2, current_y, 0])
            
            self.play(Write(cp_text), Write(decision))
            current_y -= 0.8
            self.wait(1)
        
        self.wait(2)
    
    def create_summary(self):
        # Clear previous content
        self.clear()
        
        # Summary title
        title = Text("Summary: Decision Tree Hyperparameters", font_size=40, color=BLUE)
        title.to_edge(UP)
        
        # Summary points
        summary_points = VGroup(
            Text("1. minsplit: Controls when nodes can be split", font_size=24, color=YELLOW),
            Text("2. minbucket: Controls terminal node size", font_size=24, color=GREEN),
            Text("3. cp: Controls split quality threshold", font_size=24, color=PURPLE)
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        
        summary_points.next_to(title, DOWN, buff=1)
        
        # Effect visualization
        effect_text = Text("These parameters help control tree complexity and prevent overfitting", 
                          font_size=20, color=WHITE)
        effect_text.next_to(summary_points, DOWN, buff=1)
        
        self.play(Write(title))
        self.wait(1)
        
        for point in summary_points:
            self.play(Write(point))
            self.wait(0.5)
        
        self.play(Write(effect_text))
        self.wait(2)
        
        # Final fade out
        self.play(FadeOut(VGroup(title, summary_points, effect_text)))
        self.wait(1)
