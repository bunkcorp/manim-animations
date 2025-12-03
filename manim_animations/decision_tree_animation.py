from manim import *
import numpy as np
from sklearn.tree import DecisionTreeClassifier

class DecisionTreeAnimation(Scene):
    def construct(self):
        self.next_section("Introduction")
        title = Text("Decision Tree Animation").to_edge(UP)
        subtitle = Text("Focus: Recursive Binary Splitting").next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        self.wait(1)

        # Create Axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            x_length=8,
            y_length=8,
            axis_config={
                "color": GRAY,
                "include_numbers": True,
                "font_size": 24,
            },
        ).to_edge(DOWN).shift(UP*0.5)

        x_label = axes.get_x_axis_label("Feature 1")
        y_label = axes.get_y_axis_label("Feature 2")

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(0.5)

        # Generate Data Points
        np.random.seed(0)
        n_samples = 100
        X = np.random.rand(n_samples, 2) * 10
        y = (X[:, 0] + X[:, 1] > 10).astype(int) # Simple diagonal split

        points_group = VGroup()
        for i in range(n_samples):
            color = GREEN if y[i] == 1 else RED
            dot = Dot(axes.coords_to_point(X[i, 0], X[i, 1]), color=color)
            points_group.add(dot)
        
        self.play(FadeIn(points_group))
        self.wait(1)

        # Train a simple Decision Tree
        clf = DecisionTreeClassifier(max_depth=2, random_state=0) # Limit depth for clear animation
        clf.fit(X, y)

        # Animate Splits
        self.next_section("Splitting")
        split_text = Text("Recursive Binary Splitting").to_edge(UP).shift(DOWN*0.5)
        self.play(FadeOut(title), FadeOut(subtitle), Write(split_text))

        # Get decision boundaries (simplified for visualization)
        # This part is conceptual; actual rpart output is more complex
        # We'll manually define a few splits based on the simple data

        # First Split (e.g., X[:, 0] > 5)
        first_split_value = 5.0
        first_split_line = Line(axes.coords_to_point(first_split_value, 0), 
                                axes.coords_to_point(first_split_value, 10), color=YELLOW, stroke_width=4)
        first_split_label = Text(f"Feature 1 > {first_split_value}").next_to(first_split_line, UP)

        self.play(Create(first_split_line), Write(first_split_label))
        self.wait(1)

        # Color regions based on majority class after first split
        rect1 = Rectangle(width=axes.x_axis.get_unit_size() * first_split_value, 
                          height=axes.y_axis.get_length(), 
                          fill_opacity=0.2, color=RED, 
                          stroke_width=0).move_to(axes.coords_to_point(first_split_value/2, 5))
        rect2 = Rectangle(width=axes.x_axis.get_unit_size() * (10 - first_split_value), 
                          height=axes.y_axis.get_length(), 
                          fill_opacity=0.2, color=GREEN, 
                          stroke_width=0).move_to(axes.coords_to_point(first_split_value + (10-first_split_value)/2, 5))
        
        self.play(FadeIn(rect1), FadeIn(rect2))
        self.wait(1)

        # Second Split (e.g., in the right region, X[:, 1] > 5)
        second_split_value = 5.0
        second_split_line = Line(axes.coords_to_point(first_split_value, second_split_value), 
                                 axes.coords_to_point(10, second_split_value), color=YELLOW, stroke_width=4)
        second_split_label = Text(f"Feature 2 > {second_split_value}").next_to(second_split_line, RIGHT)

        self.play(Create(second_split_line), Write(second_split_label))
        self.wait(1)

        # Update colors for new regions
        self.play(FadeOut(rect2))
        rect3 = Rectangle(width=axes.x_axis.get_unit_size() * (10 - first_split_value), 
                          height=axes.y_axis.get_unit_size() * second_split_value, 
                          fill_opacity=0.2, color=RED, 
                          stroke_width=0).move_to(axes.coords_to_point(first_split_value + (10-first_split_value)/2, second_split_value/2))
        rect4 = Rectangle(width=axes.x_axis.get_unit_size() * (10 - first_split_value), 
                          height=axes.y_axis.get_unit_size() * (10 - second_split_value), 
                          fill_opacity=0.2, color=GREEN, 
                          stroke_width=0).move_to(axes.coords_to_point(first_split_value + (10-first_split_value)/2, second_split_value + (10-second_split_value)/2))
        
        self.play(FadeIn(rect3), FadeIn(rect4))
        self.wait(1)

        self.next_section("Conclusion")
        final_text = Text("Decision Tree Splitting Demonstrated").to_edge(UP)
        self.play(FadeOut(split_text), FadeOut(first_split_line), FadeOut(first_split_label), 
                  FadeOut(second_split_line), FadeOut(second_split_label), 
                  FadeOut(rect1), FadeOut(rect3), FadeOut(rect4), 
                  FadeOut(points_group), FadeOut(axes), FadeOut(x_label), FadeOut(y_label), 
                  Write(final_text))
        self.wait(2)
