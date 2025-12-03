from manim import *
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.utils import resample

class RandomForestAnimation(Scene):
    def construct(self):
        self.next_section("Introduction")
        title = Text("Random Forest Animation").to_edge(UP)
        subtitle = Text("Focus: Bagging and Ensemble Learning").next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        self.wait(1)

        # Create Axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            x_length=6,
            y_length=6,
            axis_config={
                "color": GRAY,
                "include_numbers": False,
            },
        ).to_edge(LEFT).shift(RIGHT*1.5)

        self.play(Create(axes))
        self.wait(0.5)

        # Generate Data Points
        np.random.seed(0)
        n_samples = 50
        X = np.random.rand(n_samples, 2) * 10
        y = (X[:, 0] + X[:, 1] > 10).astype(int) # Simple diagonal split

        original_points_group = VGroup()
        for i in range(n_samples):
            color = GREEN if y[i] == 1 else RED
            dot = Dot(axes.coords_to_point(X[i, 0], X[i, 1]), color=color, radius=0.05)
            original_points_group.add(dot)
        
        self.play(FadeIn(original_points_group))
        self.wait(1)

        # Explain Bagging
        self.next_section("BaggingExplanation")
        bagging_text = Text("1. Bagging (Bootstrap Aggregating)").to_edge(UP).shift(DOWN*0.5)
        self.play(FadeOut(title), FadeOut(subtitle), Write(bagging_text))

        # Show multiple trees
        num_trees = 3
        tree_groups = VGroup()
        tree_labels = VGroup()

        for i in range(num_trees):
            # Create a sub-axes for each tree
            tree_axes = Axes(
                x_range=[0, 10, 1],
                y_range=[0, 10, 1],
                x_length=3,
                y_length=3,
                axis_config={"color": GRAY, "include_numbers": False},
            ).scale(0.8).next_to(axes, RIGHT, buff=1.0).shift(DOWN*i*2.5)
            
            tree_label = Text(f"Tree {i+1}").next_to(tree_axes, UP, buff=0.1).scale(0.6)
            tree_labels.add(tree_label)
            tree_groups.add(tree_axes)

            # Simulate bootstrapped sample (conceptual)
            resampled_X, resampled_y = resample(X, y, n_samples=n_samples, random_state=i)
            
            # Show points for this tree (conceptual, not exact positions)
            tree_points_group = VGroup()
            for j in range(n_samples):
                color = GREEN if resampled_y[j] == 1 else RED
                dot = Dot(tree_axes.coords_to_point(resampled_X[j, 0], resampled_X[j, 1]), color=color, radius=0.03)
                tree_points_group.add(dot)
            
            # Simulate a simple decision boundary for this tree
            # (This is a simplification, actual trees are more complex)
            if i == 0:
                boundary = Line(tree_axes.coords_to_point(5, 0), tree_axes.coords_to_point(5, 10), color=YELLOW)
            elif i == 1:
                boundary = Line(tree_axes.coords_to_point(0, 6), tree_axes.coords_to_point(10, 6), color=YELLOW)
            else:
                boundary = Line(tree_axes.coords_to_point(3, 0), tree_axes.coords_to_point(10, 7), color=YELLOW)
            
            self.play(Create(tree_axes), Write(tree_label), FadeIn(tree_points_group), Create(boundary))
            self.wait(0.5)

        self.wait(1)

        # Explain Ensemble Prediction
        self.next_section("EnsemblePrediction")
        ensemble_text = Text("2. Ensemble Prediction (Voting/Averaging)").to_edge(UP).shift(DOWN*0.5)
        self.play(FadeOut(bagging_text), Write(ensemble_text))

        # Simulate a new data point
        new_point_coords = np.array([4, 4])
        new_point_manim = axes.coords_to_point(new_point_coords[0], new_point_coords[1])
        new_point_dot = Dot(new_point_manim, color=WHITE, radius=0.1)
        new_point_label = Text("New Point").next_to(new_point_dot, UP).scale(0.6)
        self.play(FadeIn(new_point_dot), Write(new_point_label))
        self.wait(0.5)

        # Show prediction from each tree
        predictions = []
        for i in range(num_trees):
            # Simulate prediction based on the simple boundaries
            if i == 0: # Tree 1: X[:, 0] > 5
                pred = 1 if new_point_coords[0] > 5 else 0
            elif i == 1: # Tree 2: X[:, 1] > 6
                pred = 1 if new_point_coords[1] > 6 else 0
            else: # Tree 3: X[:, 0] > 3 and X[:, 1] > (X[:, 0] * 0.7 + 0.9)
                pred = 1 if new_point_coords[0] > 3 and new_point_coords[1] > (new_point_coords[0] * 0.7 + 0.9) else 0
            predictions.append(pred)
            
            pred_text = Text(f"Tree {i+1} predicts: {pred}").next_to(tree_labels[i], DOWN, buff=0.1).scale(0.5)
            self.play(Write(pred_text))
            self.wait(0.5)

        # Final prediction (majority vote)
        final_prediction = 1 if sum(predictions) > num_trees / 2 else 0
        final_pred_text = Text(f"Final Prediction (Majority Vote): {final_prediction}").to_edge(DOWN).shift(UP*0.5)
        self.play(Write(final_pred_text))
        self.wait(2)

        self.next_section("Conclusion")
        final_scene_text = Text("Random Forest Ensemble Demonstrated").to_edge(UP)
        self.play(FadeOut(ensemble_text), FadeOut(new_point_dot), FadeOut(new_point_label), FadeOut(final_pred_text), 
                  FadeOut(original_points_group), FadeOut(axes), FadeOut(tree_groups), FadeOut(tree_labels), 
                  Write(final_scene_text))
        self.wait(2)
