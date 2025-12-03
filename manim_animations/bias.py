#
# A Refactored Manim Animation for explaining Confusion Matrices
#
# To run this code:
# 1. Make sure you have Manim installed (pip install manim)
# 2. Make sure you have the required libraries (pip install numpy scikit-learn)
# 3. Save this code as a Python file (e.g., matrix_animation.py)
# 4. Run from your terminal: manim -pql matrix_animation.py DetailedConfusionMatrixAnimation
#

from manim import *
import numpy as np
from sklearn.metrics import confusion_matrix, roc_curve, auc

# Centralized configuration for styling and parameters
CONFIG = {
    "colors": {
        "background": "#1E1E1E",
        "primary_text": WHITE,
        "secondary_text": LIGHT_GRAY,
        "class_neg": PURE_BLUE,   # Class 0 (e.g., "Black Stone")
        "class_pos": PURE_RED,    # Class 1 (e.g., "White Stone")
        "tn": GREEN_C,
        "tp": GREEN_C,
        "fn": ORANGE,
        "fp": ORANGE,
        "accent": YELLOW,
        "slider": YELLOW,
        "roc_curve": PURE_BLUE,
    },
    "font_sizes": {
        "title": 42,
        "header": 28,
        "text": 22,
        "label": 18,
        "small_text": 14,
    },
    "data_params": {
        "n_samples": 500,
        "seed": 42,
        "class_0_mean": 0.35,
        "class_0_std": 0.15,
        "class_1_mean": 0.65,
        "class_1_std": 0.15,
    }
}

class DetailedConfusionMatrixAnimation(Scene):
    """
    A comprehensive animation explaining the components and dynamics of a confusion matrix,
    classification metrics, and the ROC curve.
    """
    def construct(self):
        self.camera.background_color = CONFIG["colors"]["background"]
        self.setup_data()

        # Storyboard of the animation
        self.show_intro()
        self.show_probability_distribution()
        self.show_interactive_metrics()
        self.show_roc_curve_and_auc()
        self.show_summary()

    def setup_data(self):
        """Generates consistent mock data for the entire animation."""
        params = CONFIG["data_params"]
        np.random.seed(params["seed"])
        
        # Probabilities for the negative class (class 0)
        probs_0 = np.random.normal(
            params["class_0_mean"], params["class_0_std"], params["n_samples"] // 2
        )
        # Probabilities for the positive class (class 1)
        probs_1 = np.random.normal(
            params["class_1_mean"], params["class_1_std"], params["n_samples"] // 2
        )

        # Combine and clip probabilities to be within [0, 1]
        self.y_pred_proba = np.clip(np.concatenate([probs_0, probs_1]), 0, 1)
        
        # True labels: 0 for the first half, 1 for the second half
        self.y_true = np.array([0] * (params["n_samples"] // 2) + [1] * (params["n_samples"] // 2))

    ## -----------------------------------------------------------------
    ## Scene 1: Introduction
    ## -----------------------------------------------------------------
    def show_intro(self):
        """Displays the title and introduces the classification problem."""
        title = Text("Understanding the Confusion Matrix", font_size=CONFIG["font_sizes"]["title"])
        self.play(Write(title))
        self.wait(1)

        problem_desc = VGroup(
            Text("A Binary Classification Problem", font_size=CONFIG["font_sizes"]["header"]),
            Text("Goal: Predict if a stone is 'White' (Positive) or 'Black' (Negative)", font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["secondary_text"]),
            Text("Model Output: A probability (0 to 1) of the stone being 'White'", font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["secondary_text"])
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(title, DOWN, buff=0.7)

        self.play(ReplacementTransform(title, problem_desc))
        self.wait(3)
        self.play(FadeOut(problem_desc))

    ## -----------------------------------------------------------------
    ## Scene 2: Probability Distribution
    ## -----------------------------------------------------------------
    def show_probability_distribution(self):
        """Visualizes the distribution of predicted probabilities for each class."""
        title = Text("Model Prediction Probabilities", font_size=CONFIG["font_sizes"]["title"]).to_edge(UP)
        self.play(Write(title))
        
        # Create axes for the histogram
        axes = Axes(
            x_range=[0, 1, 0.2], y_range=[0, 60, 10],
            x_length=10, y_length=5,
            axis_config={"color": GRAY}
        ).next_to(title, DOWN, buff=0.5)
        labels = axes.get_labels(
            x_label=Text("P(Stone = White)", font_size=CONFIG["font_sizes"]["label"]),
            y_label=Text("Count", font_size=CONFIG["font_sizes"]["label"])
        )
        self.play(Create(axes), Write(labels))

        # Create histogram bars
        hist_0, bins = np.histogram(self.y_pred_proba[self.y_true == 0], bins=25, range=(0, 1))
        hist_1, _ = np.histogram(self.y_pred_proba[self.y_true == 1], bins=bins)
        
        bars_0 = BarChart(hist_0, bar_names=None, y_range=[0, 60, 10], colors=[CONFIG["colors"]["class_neg"]]).move_to(axes.c2p(0.5, 0), aligned_edge=DL)
        bars_1 = BarChart(hist_1, bar_names=None, y_range=[0, 60, 10], colors=[CONFIG["colors"]["class_pos"]]).move_to(axes.c2p(0.5, 0), aligned_edge=DL)
        
        legend = VGroup(
            VGroup(Square(color=CONFIG["colors"]["class_neg"]), Text("Actual: Black", font_size=CONFIG["font_sizes"]["small_text"])).arrange(RIGHT),
            VGroup(Square(color=CONFIG["colors"]["class_pos"]), Text("Actual: White", font_size=CONFIG["font_sizes"]["small_text"])).arrange(RIGHT)
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UR)
        
        self.play(FadeIn(bars_0), FadeIn(bars_1), Write(legend))

        # Threshold line and label
        threshold_line = axes.get_vertical_line(axes.c2p(0.5, 60), color=CONFIG["colors"]["accent"], line_func=Line)
        threshold_label = Text("Threshold = 0.5", font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["accent"]).next_to(threshold_line, UP)

        explanation = VGroup(
            Text("If P(White) >= Threshold → Predict 'White'", font_size=CONFIG["font_sizes"]["text"]),
            Text("If P(White) < Threshold → Predict 'Black'", font_size=CONFIG["font_sizes"]["text"])
        ).arrange(DOWN, aligned_edge=LEFT).next_to(axes, DOWN, buff=0.5)

        self.play(Create(threshold_line), Write(threshold_label), Write(explanation))
        self.wait(4)
        self.play(FadeOut(VGroup(title, axes, labels, bars_0, bars_1, legend, threshold_line, threshold_label, explanation)))

    ## -----------------------------------------------------------------
    ## Scene 3: Interactive Confusion Matrix & Metrics
    ## -----------------------------------------------------------------
    def show_interactive_metrics(self):
        """Creates an interactive scene where a slider controls the threshold,
           and the confusion matrix and metrics update in real-time."""
        title = Text("Real-Time Classification Metrics", font_size=CONFIG["font_sizes"]["title"]).to_edge(UP)
        self.play(Write(title))

        # Create the visual layout
        matrix_layout, matrix_values = self._create_matrix_layout()
        metrics_display, metrics_values = self._create_metrics_display()
        
        display_group = VGroup(matrix_layout, metrics_display).arrange(RIGHT, buff=1.5).next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(display_group))

        # Create interactive slider and threshold tracker
        threshold_tracker = ValueTracker(0.5)
        slider, threshold_label = self._create_slider(threshold_tracker)
        slider_group = VGroup(slider, threshold_label).next_to(display_group, DOWN, buff=0.7)
        self.play(FadeIn(slider_group))

        # Add updaters to link matrix and metrics to the threshold
        matrix_values.add_updater(lambda m: self._update_matrix_values(m, threshold_tracker.get_value(), matrix_values))
        metrics_values.add_updater(lambda m: self._update_metrics_values(m, threshold_tracker.get_value(), metrics_values))

        # Animate the slider to show the dynamic changes
        self.play(threshold_tracker.animate.set_value(0.2), run_time=3)
        self.wait(1)
        self.play(threshold_tracker.animate.set_value(0.8), run_time=4)
        self.wait(1)
        self.play(threshold_tracker.animate.set_value(0.5), run_time=2)
        self.wait(2)

        # Cleanup
        matrix_values.clear_updaters()
        metrics_values.clear_updaters()
        self.play(FadeOut(VGroup(title, display_group, slider_group)))

    ## -----------------------------------------------------------------
    ## Scene 4: ROC Curve
    ## -----------------------------------------------------------------
    def show_roc_curve_and_auc(self):
        """Displays the ROC curve and AUC, calculated from the data."""
        title = Text("Receiver Operating Characteristic (ROC) Curve", font_size=CONFIG["font_sizes"]["title"]).to_edge(UP)
        self.play(Write(title))

        # Create axes for the ROC curve
        axes = Axes(
            x_range=[0, 1, 0.2], y_range=[0, 1, 0.2],
            x_length=7, y_length=5,
            axis_config={"color": GRAY}
        ).next_to(title, DOWN, buff=0.5)
        labels = axes.get_labels(
            x_label=Text("False Positive Rate", font_size=CONFIG["font_sizes"]["label"]),
            y_label=Text("True Positive Rate", font_size=CONFIG["font_sizes"]["label"])
        )
        self.play(Create(axes), Write(labels))

        # Plot random classifier line
        random_line = DashedLine(axes.c2p(0, 0), axes.c2p(1, 1), color=GRAY)
        self.play(Create(random_line))

        # Calculate and plot the actual ROC curve
        fpr, tpr, thresholds = roc_curve(self.y_true, self.y_pred_proba)
        roc_points = [axes.c2p(f, t) for f, t in zip(fpr, tpr)]
        curve = VMobject().set_points_as_corners(roc_points).set_color(CONFIG["colors"]["roc_curve"])
        
        auc_score = auc(fpr, tpr)
        auc_label = Text(f"AUC = {auc_score:.3f}", font_size=CONFIG["font_sizes"]["header"]).to_corner(UR)

        self.play(Create(curve), Write(auc_label))

        # Animate a dot moving along the curve corresponding to a threshold change
        moving_dot = Dot(color=CONFIG["colors"]["accent"])
        threshold_text = Text("", font_size=CONFIG["font_sizes"]["text"]).next_to(moving_dot, UR)

        def dot_updater(dot):
            # Find the closest point on the curve for a given threshold
            # Note: This is a simplified mapping for visualization
            target_t = 0.5 # A sample threshold to target
            idx = np.argmin(np.abs(thresholds - target_t))
            dot.move_to(axes.c2p(fpr[idx], tpr[idx]))
            threshold_text.become(Text(f"T={thresholds[idx]:.2f}", font_size=CONFIG["font_sizes"]["small_text"]).next_to(dot, UR))

        # For this scene, we just show a few points rather than a full dynamic link
        self.wait(1)
        key_thresholds = [0.2, 0.5, 0.8]
        for t in key_thresholds:
            idx = np.argmin(np.abs(thresholds - t))
            dot = Dot(axes.c2p(fpr[idx], tpr[idx]), color=CONFIG["colors"]["accent"])
            label = Text(f"T={t}", font_size=CONFIG["font_sizes"]["small_text"]).next_to(dot, UR)
            self.play(FadeIn(dot), Write(label))
            self.wait(1)

        self.wait(3)
        self.play(FadeOut(VGroup(title, axes, labels, random_line, curve, auc_label), self.mobjects[-6:])) # Fade out created dots and labels

    ## -----------------------------------------------------------------
    ## Scene 5: Summary
    ## -----------------------------------------------------------------
    def show_summary(self):
        """Provides a final summary of key takeaways."""
        title = Text("Key Takeaways", font_size=CONFIG["font_sizes"]["title"]).to_edge(UP)
        
        summary_points = VGroup(
            Text("• The Confusion Matrix evaluates model performance.", ttm={"Confusion Matrix": BOLD}),
            Text("• The threshold is a critical hyperparameter to tune.", ttm={"threshold": BOLD}),
            Text("• Metrics like Precision and Recall reveal trade-offs.", ttm={"Precision": BOLD, "Recall": BOLD}),
            Text("• The ROC curve visualizes this trade-off across all thresholds.", ttm={"ROC curve": BOLD})
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).scale(0.8)

        self.play(Write(title), FadeIn(summary_points, shift=UP))
        self.wait(5)
        self.play(FadeOut(title, summary_points))

    ## -----------------------------------------------------------------
    ## Helper Methods for Scene 3
    ## -----------------------------------------------------------------
    def _create_matrix_layout(self):
        """Creates the visual grid and labels for the confusion matrix."""
        # Main grid
        grid = VGroup(*[
            Square(side_length=1.5).set_stroke(GRAY) for _ in range(4)
        ]).arrange_in_grid(2, 2, buff=0)

        # Labels
        predicted_label = Text("Predicted", font_size=CONFIG["font_sizes"]["label"]).next_to(grid, UP)
        actual_label = Text("Actual", font_size=CONFIG["font_sizes"]["label"]).next_to(grid, LEFT, buff=0.5).rotate(PI/2)
        
        pred_neg = Text("Black (0)", font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["class_neg"]).next_to(grid[0], UP)
        pred_pos = Text("White (1)", font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["class_pos"]).next_to(grid[1], UP)
        
        act_neg = Text("Black (0)", font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["class_neg"]).next_to(grid[0], LEFT)
        act_pos = Text("White (1)", font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["class_pos"]).next_to(grid[2], LEFT)

        # Cell names (TN, FP, etc.)
        tn_label = Text("TN", font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["tn"]).move_to(grid[0]).shift(UP*0.5)
        fp_label = Text("FP", font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["fp"]).move_to(grid[1]).shift(UP*0.5)
        fn_label = Text("FN", font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["fn"]).move_to(grid[2]).shift(UP*0.5)
        tp_label = Text("TP", font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["tp"]).move_to(grid[3]).shift(UP*0.5)
        
        # Numeric value placeholders
        tn_val, fp_val, fn_val, tp_val = [Integer(0).move_to(cell).shift(DOWN*0.1) for cell in grid]

        layout = VGroup(grid, predicted_label, actual_label, pred_neg, pred_pos, act_neg, act_pos, tn_label, fp_label, fn_label, tp_label)
        values = VGroup(tn_val, fp_val, fn_val, tp_val)
        return layout, values

    def _create_metrics_display(self):
        """Creates the text display for derived classification metrics."""
        titles = ["Accuracy", "Precision", "Recall (TPR)", "Specificity (TNR)", "F1-Score"]
        v_group = VGroup()
        value_placeholders = VGroup()

        for title in titles:
            label = Text(f"{title}:", font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["secondary_text"])
            value = DecimalNumber(0, num_decimal_places=3, font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["accent"])
            row = VGroup(label, value).arrange(RIGHT, buff=0.2)
            v_group.add(row)
            value_placeholders.add(value)

        v_group.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        return v_group, value_placeholders

    def _create_slider(self, tracker):
        """Creates a slider linked to a ValueTracker."""
        slider = NumberLine(x_range=[0, 1, 0.1], length=7, include_numbers=True, font_size=CONFIG["font_sizes"]["small_text"])
        handle = Triangle(fill_opacity=1, color=CONFIG["colors"]["slider"]).scale(0.15).rotate(-PI).move_to(slider.n2p(tracker.get_value()), DOWN)
        handle.add_updater(lambda m: m.move_to(slider.n2p(tracker.get_value()), DOWN))

        label = Text("Threshold:", font_size=CONFIG["font_sizes"]["text"]).next_to(slider, UP, buff=0.5)
        value_text = DecimalNumber(tracker.get_value(), num_decimal_places=2).next_to(label, RIGHT)
        value_text.add_updater(lambda m: m.set_value(tracker.get_value()))
        
        return VGroup(slider, handle), VGroup(label, value_text)

    def _update_matrix_values(self, mobject_group, threshold, value_placeholders):
        """Updater function to recalculate and set confusion matrix values."""
        y_pred = (self.y_pred_proba >= threshold).astype(int)
        tn, fp, fn, tp = confusion_matrix(self.y_true, y_pred).ravel()
        
        value_placeholders[0].set_value(tn).set_color(CONFIG["colors"]["tn"])
        value_placeholders[1].set_value(fp).set_color(CONFIG["colors"]["fp"])
        value_placeholders[2].set_value(fn).set_color(CONFIG["colors"]["fn"])
        value_placeholders[3].set_value(tp).set_color(CONFIG["colors"]["tp"])

    def _update_metrics_values(self, mobject_group, threshold, value_placeholders):
        """Updater function to recalculate and set derived metric values."""
        y_pred = (self.y_pred_proba >= threshold).astype(int)
        tn, fp, fn, tp = confusion_matrix(self.y_true, y_pred).ravel()
        
        # Calculate metrics, handling division by zero
        accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        metrics = [accuracy, precision, recall, specificity, f1]
        for placeholder, value in zip(value_placeholders, metrics):
            placeholder.set_value(value)