from manim import *
import numpy as np

class ImpurityAndInformationGain(Scene):
    def construct(self):
        # Title
        title = Text("Impurity vs Information Gain in Decision Trees", font_size=36, color=BLUE)
        subtitle = Text("How impurity decrease creates information gain", font_size=24, color=GRAY)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.3)
        title_group.to_edge(UP)
        
        self.play(Write(title))
        self.play(Write(subtitle))
        self.wait(2)
        
        # Show the key concepts
        self.show_impurity_measures()
        self.show_information_gain_formula()
        self.show_practical_example()
        self.show_relationship_visualization()
    
    def show_impurity_measures(self):
        # Clear previous content
        self.clear()
        
        # Title
        title = Text("Measures of Impurity", font_size=32, color=BLUE)
        title.to_edge(UP)
        
        # Create impurity measures
        measures = VGroup(
            Text("1. Gini Impurity", font_size=24, color=YELLOW),
            Text("2. Entropy", font_size=24, color=GREEN),
            Text("3. Classification Error", font_size=24, color=PURPLE)
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        
        measures.move_to([-3, 0, 0])
        
        self.play(Write(title))
        self.wait(1)
        
        for measure in measures:
            self.play(Write(measure))
            self.wait(0.5)
        
        # Show formulas
        formulas = VGroup(
            MathTex(r"\text{Gini} = 1 - \sum_{i=1}^{c} p_i^2", font_size=20),
            MathTex(r"\text{Entropy} = -\sum_{i=1}^{c} p_i \log_2(p_i)", font_size=20),
            MathTex(r"\text{Error} = 1 - \max_i(p_i)", font_size=20)
        ).arrange(DOWN, buff=0.5)
        
        formulas.move_to([3, 0, 0])
        
        for formula in formulas:
            self.play(Write(formula))
            self.wait(1)
        
        self.wait(2)
    
    def show_information_gain_formula(self):
        # Clear previous content
        self.clear()
        
        # Title
        title = Text("Information Gain Formula", font_size=32, color=BLUE)
        title.to_edge(UP)
        
        # Main formula
        main_formula = MathTex(
            r"\text{Information Gain} = \text{Impurity}(S) - \sum_{v \in \text{Values}(A)} \frac{|S_v|}{|S|} \text{Impurity}(S_v)",
            font_size=24
        )
        main_formula.move_to([0, 1, 0])
        
        # Explanation
        explanation = VGroup(
            Text("Where:", font_size=20, color=WHITE),
            Text("• S = Parent node", font_size=16),
            Text("• A = Feature being split on", font_size=16),
            Text("• S_v = Child node for value v", font_size=16),
            Text("• |S| = Number of samples in parent", font_size=16),
            Text("• |S_v| = Number of samples in child", font_size=16)
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        
        explanation.move_to([0, -1, 0])
        
        self.play(Write(title))
        self.wait(1)
        self.play(Write(main_formula))
        self.wait(2)
        
        for exp in explanation:
            self.play(Write(exp))
            self.wait(0.3)
        
        self.wait(2)
    
    def show_practical_example(self):
        # Clear previous content
        self.clear()
        
        # Title
        title = Text("Practical Example", font_size=32, color=BLUE)
        title.to_edge(UP)
        
        # Create sample dataset
        dataset = self.create_sample_dataset()
        dataset.move_to([-3, 0, 0])
        
        self.play(Write(title))
        self.play(FadeIn(dataset))
        self.wait(2)
        
        # Show parent node impurity
        parent_impurity = self.calculate_parent_impurity()
        parent_impurity.move_to([3, 1, 0])
        
        self.play(Write(parent_impurity))
        self.wait(2)
        
        # Show potential splits
        splits = self.show_potential_splits()
        splits.move_to([3, -1, 0])
        
        self.play(FadeIn(splits))
        self.wait(2)
        
        # Calculate information gain
        self.calculate_information_gain()
    
    def create_sample_dataset(self):
        # Create a simple dataset visualization
        dataset_group = VGroup()
        
        # Dataset title
        dataset_title = Text("Sample Dataset", font_size=20, color=WHITE)
        dataset_title.to_edge(LEFT).shift(UP * 2)
        
        # Create data points with labels
        data_points = []
        labels = ["Yes", "No", "Yes", "No", "Yes", "No", "Yes", "Yes"]
        colors = [GREEN if label == "Yes" else RED for label in labels]
        
        for i, (label, color) in enumerate(zip(labels, colors)):
            point = Circle(radius=0.2, fill_color=color, fill_opacity=0.8)
            point.move_to([-4 + (i % 4) * 0.6, 1 - (i // 4) * 0.6, 0])
            
            label_text = Text(label, font_size=12, color=WHITE)
            label_text.move_to(point.get_center())
            
            data_points.append(VGroup(point, label_text))
        
        dataset_group.add(dataset_title)
        dataset_group.add(*data_points)
        
        return dataset_group
    
    def calculate_parent_impurity(self):
        # Show parent node impurity calculation
        parent_group = VGroup(
            Text("Parent Node:", font_size=20, color=YELLOW),
            Text("Total samples: 8", font_size=16),
            Text("Yes: 5, No: 3", font_size=16),
            Text("p(Yes) = 5/8 = 0.625", font_size=16),
            Text("p(No) = 3/8 = 0.375", font_size=16)
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        
        # Calculate Gini impurity
        gini_calc = MathTex(
            r"\text{Gini} = 1 - (0.625^2 + 0.375^2) = 1 - 0.531 = 0.469",
            font_size=16
        )
        gini_calc.next_to(parent_group, DOWN, buff=0.3)
        
        return VGroup(parent_group, gini_calc)
    
    def show_potential_splits(self):
        # Show potential splits
        splits_group = VGroup(
            Text("Potential Splits:", font_size=18, color=BLUE),
            Text("Split 1: Feature A", font_size=14),
            Text("Split 2: Feature B", font_size=14),
            Text("Split 3: Feature C", font_size=14)
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        
        return splits_group
    
    def calculate_information_gain(self):
        # Clear and show detailed calculation
        self.clear()
        
        title = Text("Information Gain Calculation", font_size=32, color=BLUE)
        title.to_edge(UP)
        
        # Show the split
        split_visual = self.create_split_visualization()
        split_visual.move_to([-3, 0, 0])
        
        # Show calculation
        calculation = VGroup(
            Text("Best Split: Feature A", font_size=20, color=GREEN),
            Text("Left Child: 4 samples (3 Yes, 1 No)", font_size=16),
            Text("Right Child: 4 samples (2 Yes, 2 No)", font_size=16),
            Text("Weighted Impurity:", font_size=16),
            MathTex(r"= \frac{4}{8} \times 0.375 + \frac{4}{8} \times 0.5 = 0.4375", font_size=16),
            Text("Information Gain:", font_size=16),
            MathTex(r"= 0.469 - 0.4375 = 0.0315", font_size=16)
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        
        calculation.move_to([3, 0, 0])
        
        self.play(Write(title))
        self.play(FadeIn(split_visual))
        self.wait(1)
        
        for calc in calculation:
            self.play(Write(calc))
            self.wait(0.5)
        
        self.wait(2)
    
    def create_split_visualization(self):
        # Create a visual representation of the split
        split_group = VGroup()
        
        # Parent node
        parent = Rectangle(width=2, height=0.8, color=WHITE)
        parent.move_to([0, 1, 0])
        parent_label = Text("Parent\nGini = 0.469", font_size=14)
        parent_label.move_to(parent.get_center())
        
        # Split line
        split_line = Line(start=[-1, 0.6, 0], end=[1, 0.6, 0], color=YELLOW)
        
        # Left child
        left_child = Rectangle(width=1.5, height=0.6, color=WHITE)
        left_child.move_to([-1.5, -0.5, 0])
        left_label = Text("Left\nGini = 0.375", font_size=12)
        left_label.move_to(left_child.get_center())
        
        # Right child
        right_child = Rectangle(width=1.5, height=0.6, color=WHITE)
        right_child.move_to([1.5, -0.5, 0])
        right_label = Text("Right\nGini = 0.5", font_size=12)
        right_label.move_to(right_child.get_center())
        
        # Connect nodes
        left_line = Line(start=parent.get_bottom(), end=left_child.get_top(), color=WHITE)
        right_line = Line(start=parent.get_bottom(), end=right_child.get_top(), color=WHITE)
        
        split_group.add(parent, parent_label, split_line, left_child, left_label, right_child, right_label, left_line, right_line)
        
        return split_group
    
    def show_relationship_visualization(self):
        # Clear and show the relationship
        self.clear()
        
        title = Text("Relationship: Impurity ↔ Information Gain", font_size=32, color=BLUE)
        title.to_edge(UP)
        
        # Key relationship points
        relationship = VGroup(
            Text("Key Relationships:", font_size=24, color=WHITE),
            Text("• Lower impurity = Higher information gain", font_size=18, color=GREEN),
            Text("• Perfect split: Impurity = 0, Max gain", font_size=18, color=GREEN),
            Text("• No improvement: Gain = 0", font_size=18, color=RED),
            Text("• Information gain guides feature selection", font_size=18, color=BLUE)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        
        relationship.move_to([0, 0, 0])
        
        self.play(Write(title))
        self.wait(1)
        
        for rel in relationship:
            self.play(Write(rel))
            self.wait(0.5)
        
        self.wait(2)
        
        # Show mathematical relationship
        math_relationship = VGroup(
            Text("Mathematical Relationship:", font_size=20, color=YELLOW),
            MathTex(r"\text{Gain} = \text{Parent Impurity} - \text{Weighted Child Impurity}", font_size=18),
            Text("The goal: Maximize information gain", font_size=16, color=GREEN),
            Text("This minimizes overall tree impurity", font_size=16, color=GREEN)
        ).arrange(DOWN, buff=0.3)
        
        math_relationship.move_to([0, -3, 0])
        
        for math_rel in math_relationship:
            self.play(Write(math_rel))
            self.wait(0.5)
        
        self.wait(3)
