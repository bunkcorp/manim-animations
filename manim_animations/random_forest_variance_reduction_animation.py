from manim import *
import numpy as np

# --- Configuration ---
CONFIG = {
    "colors": {
        "background": "#1E1E2A",
        "primary_text": WHITE,
        "secondary_text": LIGHT_GREY,
        "tree_color": GREEN,
        "bootstrap_color": BLUE,
        "randomization_color": YELLOW,
        "variance_color": RED,
        "prediction_color": ORANGE,
        "ensemble_color": PURPLE,
    },
    "font_sizes": {
        "title": 48,
        "header": 32,
        "text": 24,
        "label": 20,
    },
}

class RandomForestVarianceReduction(Scene):
    def construct(self):
        self.camera.background_color = CONFIG["colors"]["background"]
        self.show_intro()
        self.show_core_idea()
        self.show_bootstrapping()
        self.show_randomization()
        self.show_variance_reduction()
        self.show_ensemble_prediction()
        self.show_summary()

    def show_intro(self):
        # Title
        title = Text("Random Forests: Core Idea & Variance Reduction", 
                    font_size=CONFIG["font_sizes"]["title"], 
                    color=CONFIG["colors"]["primary_text"])
        title.to_edge(UP)
        
        # Subtitle
        subtitle = Text("How combining multiple trees reduces prediction variance", 
                       font_size=CONFIG["font_sizes"]["text"], 
                       color=CONFIG["colors"]["secondary_text"])
        subtitle.next_to(title, DOWN, buff=0.5)
        
        self.play(Write(title))
        self.play(Write(subtitle))
        self.wait(2)
        
        # Fade out intro
        self.play(FadeOut(VGroup(title, subtitle)))
        self.wait(1)

    def show_core_idea(self):
        # Section title
        section_title = Text("Core Idea: Ensemble of Decision Trees", 
                           font_size=CONFIG["font_sizes"]["header"], 
                           color=CONFIG["colors"]["tree_color"])
        section_title.to_edge(UP)
        self.play(Write(section_title))
        
        # Create multiple decision trees
        trees = VGroup()
        for i in range(5):
            tree = self.create_simple_tree()
            tree.scale(0.4)
            trees.add(tree)
        
        # Arrange trees in a circle
        trees.arrange_in_grid(2, 3, buff=1.5)
        trees.move_to(ORIGIN)
        
        # Show trees appearing one by one
        for tree in trees:
            self.play(FadeIn(tree), run_time=0.5)
        
        self.wait(2)
        
        # Add ensemble arrow
        ensemble_arrow = Arrow(LEFT * 4, RIGHT * 4, color=CONFIG["colors"]["ensemble_color"], stroke_width=4)
        ensemble_arrow.next_to(trees, DOWN, buff=1)
        
        # Final prediction
        prediction_circle = Circle(radius=0.5, color=CONFIG["colors"]["prediction_color"], fill_opacity=0.3)
        prediction_circle.next_to(ensemble_arrow, DOWN, buff=0.5)
        prediction_text = Text("Final\nPrediction", font_size=CONFIG["font_sizes"]["label"], 
                             color=CONFIG["colors"]["prediction_color"])
        prediction_text.move_to(prediction_circle)
        
        self.play(Create(ensemble_arrow))
        self.play(Create(prediction_circle), Write(prediction_text))
        self.wait(2)
        
        # Fade out for next section
        self.play(FadeOut(VGroup(section_title, trees, ensemble_arrow, prediction_circle, prediction_text)))
        self.wait(1)

    def show_bootstrapping(self):
        # Section title
        section_title = Text("Variance Reduction Technique 1: Bootstrapping", 
                           font_size=CONFIG["font_sizes"]["header"], 
                           color=CONFIG["colors"]["bootstrap_color"])
        section_title.to_edge(UP)
        self.play(Write(section_title))
        
        # Original dataset
        original_title = Text("Original Dataset", font_size=CONFIG["font_sizes"]["text"], 
                            color=CONFIG["colors"]["primary_text"])
        original_title.move_to(UP * 2 + LEFT * 4)
        
        # Create sample data points
        data_points = VGroup()
        for i in range(8):
            point = Circle(radius=0.1, color=BLUE, fill_opacity=0.7)
            point.move_to(UP * 1.5 + LEFT * 4 + RIGHT * (i * 0.3) + DOWN * (i % 2 * 0.2))
            data_points.add(point)
        
        self.play(Write(original_title), FadeIn(data_points))
        self.wait(1)
        
        # Bootstrap samples
        bootstrap_samples = VGroup()
        for i in range(3):
            sample_title = Text(f"Bootstrap Sample {i+1}", font_size=CONFIG["font_sizes"]["text"], 
                              color=CONFIG["colors"]["bootstrap_color"])
            sample_title.move_to(UP * 0.5 + RIGHT * (i - 1) * 3)
            
            # Create bootstrapped data points (some repeated)
            sample_points = VGroup()
            for j in range(8):
                point = Circle(radius=0.08, color=CONFIG["colors"]["bootstrap_color"], fill_opacity=0.7)
                point.move_to(UP * 0 + RIGHT * (i - 1) * 3 + RIGHT * (j * 0.25) + DOWN * (j % 2 * 0.15))
                sample_points.add(point)
            
            # Add some repeated points (bootstrap effect)
            if i == 0:
                sample_points[2].set_color(RED)  # Highlight repeated point
            elif i == 1:
                sample_points[5].set_color(RED)
            elif i == 2:
                sample_points[1].set_color(RED)
            
            bootstrap_samples.add(VGroup(sample_title, sample_points))
        
        self.play(FadeIn(bootstrap_samples))
        self.wait(2)
        
        # Explanation text
        explanation = VGroup(
            Text("• Each tree trained on different bootstrap sample", font_size=CONFIG["font_sizes"]["label"], 
                color=CONFIG["colors"]["secondary_text"]),
            Text("• Some data points appear multiple times", font_size=CONFIG["font_sizes"]["label"], 
                color=CONFIG["colors"]["secondary_text"]),
            Text("• Creates diversity in tree predictions", font_size=CONFIG["font_sizes"]["label"], 
                color=CONFIG["colors"]["secondary_text"])
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        explanation.move_to(DOWN * 2.5)
        
        self.play(Write(explanation))
        self.wait(3)
        
        # Fade out for next section
        self.play(FadeOut(VGroup(section_title, original_title, data_points, bootstrap_samples, explanation)))
        self.wait(1)

    def show_randomization(self):
        # Section title
        section_title = Text("Variance Reduction Technique 2: Randomization", 
                           font_size=CONFIG["font_sizes"]["header"], 
                           color=CONFIG["colors"]["randomization_color"])
        section_title.to_edge(UP)
        self.play(Write(section_title))
        
        # Show feature selection at each split
        split_title = Text("At Each Split: Random Feature Subset", 
                          font_size=CONFIG["font_sizes"]["text"], 
                          color=CONFIG["colors"]["primary_text"])
        split_title.move_to(UP * 2)
        
        # All features
        all_features = VGroup()
        feature_names = ["Age", "Income", "Education", "Location", "Credit Score", "Employment"]
        for i, name in enumerate(feature_names):
            feature = Rectangle(width=1.5, height=0.4, color=BLUE, fill_opacity=0.3)
            feature.move_to(UP * 1.2 + RIGHT * (i - 2.5) * 1.8)
            feature_text = Text(name, font_size=CONFIG["font_sizes"]["label"], color=WHITE)
            feature_text.move_to(feature)
            all_features.add(VGroup(feature, feature_text))
        
        self.play(Write(split_title), FadeIn(all_features))
        self.wait(1)
        
        # Random subset selection
        subset_title = Text("Random Subset (e.g., 3 features)", 
                           font_size=CONFIG["font_sizes"]["text"], 
                           color=CONFIG["colors"]["randomization_color"])
        subset_title.move_to(UP * 0.2)
        
        # Highlight random subset
        selected_features = VGroup()
        selected_indices = [0, 2, 4]  # Age, Education, Credit Score
        for i in selected_indices:
            selected_features.add(all_features[i].copy())
        
        selected_features.arrange(RIGHT, buff=0.5)
        selected_features.move_to(UP * -0.3)
        
        # Highlight the selected features
        for i in selected_indices:
            self.play(all_features[i].animate.set_color(CONFIG["colors"]["randomization_color"]))
        
        self.play(Write(subset_title), FadeIn(selected_features))
        self.wait(2)
        
        # Show multiple trees with different random subsets
        trees_with_features = VGroup()
        for i in range(3):
            tree = self.create_simple_tree()
            tree.scale(0.3)
            tree.move_to(DOWN * 1.5 + RIGHT * (i - 1) * 3)
            
            # Add feature labels
            if i == 0:
                features = ["Age", "Income", "Location"]
            elif i == 1:
                features = ["Education", "Credit Score", "Age"]
            else:
                features = ["Employment", "Income", "Education"]
            
            feature_text = Text(f"Features: {', '.join(features)}", 
                              font_size=CONFIG["font_sizes"]["label"], 
                              color=CONFIG["colors"]["randomization_color"])
            feature_text.next_to(tree, DOWN, buff=0.3)
            
            trees_with_features.add(VGroup(tree, feature_text))
        
        self.play(FadeIn(trees_with_features))
        self.wait(2)
        
        # Explanation
        explanation = VGroup(
            Text("• Each tree considers different random feature subset", font_size=CONFIG["font_sizes"]["label"], 
                color=CONFIG["colors"]["secondary_text"]),
            Text("• Reduces correlation between trees", font_size=CONFIG["font_sizes"]["label"], 
                color=CONFIG["colors"]["secondary_text"]),
            Text("• Further decreases overall prediction variance", font_size=CONFIG["font_sizes"]["label"], 
                color=CONFIG["colors"]["secondary_text"])
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        explanation.move_to(DOWN * 3.5)
        
        self.play(Write(explanation))
        self.wait(3)
        
        # Fade out for next section
        self.play(FadeOut(VGroup(section_title, split_title, all_features, subset_title, 
                                selected_features, trees_with_features, explanation)))
        self.wait(1)

    def show_variance_reduction(self):
        # Section title
        section_title = Text("How Variance Reduction Works", 
                           font_size=CONFIG["font_sizes"]["header"], 
                           color=CONFIG["colors"]["variance_color"])
        section_title.to_edge(UP)
        self.play(Write(section_title))
        
        # Create axes for variance visualization
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 1, 0.2],
            x_length=6,
            y_length=4,
            axis_config={"color": WHITE},
            x_axis_config={"numbers_to_include": np.arange(0, 11, 2)},
            y_axis_config={"numbers_to_include": np.arange(0, 1.1, 0.2)},
        ).add_coordinates()
        
        axes_labels = axes.get_axis_labels(
            x_label="Number of Trees", y_label="Prediction Variance"
        )
        
        axes.move_to(LEFT * 2)
        self.play(Create(axes), Write(axes_labels))
        
        # Single tree variance
        single_tree_variance = axes.plot(lambda x: 0.8, color=RED, x_range=[0, 10])
        single_tree_label = axes.get_graph_label(single_tree_variance, "Single Tree", x_val=8)
        
        # Multiple trees variance (decreasing)
        multiple_trees_variance = axes.plot(lambda x: 0.8 / np.sqrt(x), color=GREEN, x_range=[1, 10])
        multiple_trees_label = axes.get_graph_label(multiple_trees_variance, "Random Forest", x_val=8)
        
        self.play(Create(single_tree_variance), Write(single_tree_label))
        self.wait(1)
        self.play(Create(multiple_trees_variance), Write(multiple_trees_label))
        self.wait(2)
        
        # Mathematical explanation
        math_explanation = VGroup(
            Text("Variance Reduction Formula:", font_size=CONFIG["font_sizes"]["text"], 
                color=CONFIG["colors"]["primary_text"]),
            MathTex(r"\text{Var}(\text{Random Forest}) = \frac{\text{Var}(\text{Single Tree})}{\sqrt{n}}", 
                   color=CONFIG["colors"]["variance_color"]),
            Text("where n = number of trees", font_size=CONFIG["font_sizes"]["label"], 
                color=CONFIG["colors"]["secondary_text"])
        ).arrange(DOWN, buff=0.5)
        math_explanation.move_to(RIGHT * 3)
        
        self.play(Write(math_explanation))
        self.wait(3)
        
        # Fade out for next section
        self.play(FadeOut(VGroup(section_title, axes, axes_labels, single_tree_variance, 
                                single_tree_label, multiple_trees_variance, multiple_trees_label, 
                                math_explanation)))
        self.wait(1)

    def show_ensemble_prediction(self):
        # Section title
        section_title = Text("Ensemble Prediction Process", 
                           font_size=CONFIG["font_sizes"]["header"], 
                           color=CONFIG["colors"]["ensemble_color"])
        section_title.to_edge(UP)
        self.play(Write(section_title))
        
        # Show multiple trees making predictions
        trees = VGroup()
        predictions = []
        for i in range(5):
            tree = self.create_simple_tree()
            tree.scale(0.3)
            tree.move_to(UP * 1 + RIGHT * (i - 2) * 2)
            
            # Add prediction value
            pred_value = np.random.uniform(0.3, 0.7)
            predictions.append(pred_value)
            pred_text = Text(f"{pred_value:.2f}", font_size=CONFIG["font_sizes"]["label"], 
                           color=CONFIG["colors"]["prediction_color"])
            pred_text.next_to(tree, DOWN, buff=0.3)
            
            trees.add(VGroup(tree, pred_text))
        
        self.play(FadeIn(trees))
        self.wait(2)
        
        # Show averaging process
        avg_title = Text("Average Predictions", font_size=CONFIG["font_sizes"]["text"], 
                        color=CONFIG["colors"]["ensemble_color"])
        avg_title.move_to(DOWN * 0.5)
        
        avg_value = np.mean(predictions)
        avg_text = MathTex(f"\\text{{Final Prediction}} = \\frac{{1}}{{5}}\\sum_{{i=1}}^{{5}} p_i = {avg_value:.2f}", 
                          color=CONFIG["colors"]["ensemble_color"])
        avg_text.move_to(DOWN * 1.5)
        
        # Arrows pointing to average
        arrows = VGroup()
        for tree in trees:
            arrow = Arrow(tree.get_center(), DOWN * 1.5, color=CONFIG["colors"]["ensemble_color"])
            arrows.add(arrow)
        
        self.play(Write(avg_title), Create(arrows))
        self.play(Write(avg_text))
        self.wait(3)
        
        # Fade out for next section
        self.play(FadeOut(VGroup(section_title, trees, avg_title, arrows, avg_text)))
        self.wait(1)

    def show_summary(self):
        # Section title
        section_title = Text("Summary: Random Forest Variance Reduction", 
                           font_size=CONFIG["font_sizes"]["header"], 
                           color=CONFIG["colors"]["primary_text"])
        section_title.to_edge(UP)
        self.play(Write(section_title))
        
        # Key points
        key_points = VGroup(
            Text("🎯 Core Idea: Ensemble of decision trees", font_size=CONFIG["font_sizes"]["text"], 
                color=CONFIG["colors"]["tree_color"]),
            Text("🔄 Bootstrapping: Each tree on different data sample", font_size=CONFIG["font_sizes"]["text"], 
                color=CONFIG["colors"]["bootstrap_color"]),
            Text("🎲 Randomization: Random feature subset at each split", font_size=CONFIG["font_sizes"]["text"], 
                color=CONFIG["colors"]["randomization_color"]),
            Text("📉 Variance Reduction: Var(RF) = Var(Tree)/√n", font_size=CONFIG["font_sizes"]["text"], 
                color=CONFIG["colors"]["variance_color"]),
            Text("⚖️ Final Prediction: Average of all tree predictions", font_size=CONFIG["font_sizes"]["text"], 
                color=CONFIG["colors"]["prediction_color"])
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        key_points.move_to(ORIGIN)
        
        self.play(Write(key_points))
        self.wait(4)
        
        # Final message
        final_message = Text("Random Forests: Powerful ensemble method for variance reduction!", 
                           font_size=CONFIG["font_sizes"]["text"], 
                           color=CONFIG["colors"]["ensemble_color"])
        final_message.move_to(DOWN * 3)
        
        self.play(Write(final_message))
        self.wait(3)
        
        # Fade out everything
        self.play(FadeOut(VGroup(section_title, key_points, final_message)))
        self.wait(1)

    def create_simple_tree(self):
        """Create a simple decision tree visualization"""
        # Root node
        root = Circle(radius=0.2, color=CONFIG["colors"]["tree_color"], fill_opacity=0.3)
        root_text = Text("?", font_size=CONFIG["font_sizes"]["label"], color=WHITE)
        root_text.move_to(root)
        
        # Left child
        left_child = Circle(radius=0.15, color=CONFIG["colors"]["tree_color"], fill_opacity=0.3)
        left_child.move_to(root.get_center() + LEFT * 1 + DOWN * 0.8)
        left_text = Text("Yes", font_size=CONFIG["font_sizes"]["label"], color=WHITE)
        left_text.move_to(left_child)
        
        # Right child
        right_child = Circle(radius=0.15, color=CONFIG["colors"]["tree_color"], fill_opacity=0.3)
        right_child.move_to(root.get_center() + RIGHT * 1 + DOWN * 0.8)
        right_text = Text("No", font_size=CONFIG["font_sizes"]["label"], color=WHITE)
        right_text.move_to(right_child)
        
        # Edges
        left_edge = Line(root.get_center(), left_child.get_center(), color=CONFIG["colors"]["tree_color"])
        right_edge = Line(root.get_center(), right_child.get_center(), color=CONFIG["colors"]["tree_color"])
        
        return VGroup(root, root_text, left_child, left_text, right_child, right_text, left_edge, right_edge)
