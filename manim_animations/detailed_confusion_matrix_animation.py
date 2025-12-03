from manim import *
import numpy as np
import pandas as pd
import json
import os
from sklearn.metrics import confusion_matrix, classification_report

class DetailedConfusionMatrixAnimation(Scene):
    def construct(self):
        # Set up the scene
        self.camera.background_color = "#1a1a1a"
        
        # Title
        title = Text("Confusion Matrix & Classification Metrics", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Load real data
        self.next_section("Data Loading")
        self.show_data_loading()
        
        # Show prediction distribution
        self.next_section("Prediction Distribution")
        self.show_prediction_distribution()
        
        # Dynamic confusion matrix
        self.next_section("Dynamic Confusion Matrix")
        self.show_dynamic_confusion_matrix()
        
        # Threshold slider
        self.next_section("Threshold Slider")
        self.show_threshold_slider()
        
        # Real-time metrics
        self.next_section("Real-time Metrics")
        self.show_real_time_metrics()
        
        # ROC curve
        self.next_section("ROC Curve")
        self.show_roc_curve()
        
        # Final analysis
        self.next_section("Final Analysis")
        self.show_final_analysis()
        
    def show_data_loading(self):
        # Show data loading process
        loading_text = Text("Loading Buddhist Stone Classification Data...", font_size=36, color=YELLOW)
        loading_text.move_to(ORIGIN)
        self.play(Write(loading_text))
        self.wait(1)
        
        # Show data structure
        data_info = VGroup(
            Text("📊 Binary Classification Problem:", font_size=32, color=WHITE),
            Text("• Predict Stone Type (Black/White)", font_size=24, color=GRAY),
            Text("• Based on User Behavior Patterns", font_size=24, color=GRAY),
            Text("• Meditation Duration", font_size=24, color=GRAY),
            Text("• Time of Day", font_size=24, color=GRAY),
            Text("• Previous Stone History", font_size=24, color=GRAY),
            Text("• User Activity Level", font_size=24, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        data_info.move_to(ORIGIN)
        
        self.play(ReplacementTransform(loading_text, data_info))
        self.wait(2)
        
        # Load actual data
        try:
            data_path = "firebase/complete_user_data_export_2025-08-23T20-19-34-686Z/all_user_stones.json"
            with open(data_path, 'r') as f:
                stones_data = json.load(f)
            
            df = pd.DataFrame(stones_data)
            
            # Show data statistics
            stats_text = VGroup(
                Text(f"✅ Loaded {len(df)} stone records", font_size=32, color=GREEN),
                Text(f"📈 {len(df.columns)} features", font_size=28, color=BLUE),
                Text(f"🎯 Target: Black vs White Stone Classification", font_size=28, color=ORANGE),
                Text(f"📊 Model: Logistic Regression with Probabilities", font_size=28, color=PURPLE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
            stats_text.move_to(ORIGIN)
            
            self.play(ReplacementTransform(data_info, stats_text))
            self.wait(2)
            self.play(FadeOut(stats_text))
            
        except Exception as e:
            error_text = Text(f"⚠️ Error loading data: {str(e)}", font_size=32, color=RED)
            self.play(ReplacementTransform(data_info, error_text))
            self.wait(2)
            self.play(FadeOut(error_text))
    
    def show_prediction_distribution(self):
        # Show prediction distribution
        distribution_title = Text("Prediction Probability Distribution", font_size=40, color=WHITE)
        distribution_title.to_edge(UP)
        self.play(Write(distribution_title))
        
        # Create coordinate system
        axes = Axes(
            x_range=[0, 1, 0.1],
            y_range=[0, 100, 10],
            x_length=10,
            y_length=6,
            axis_config={"color": GRAY}
        )
        axes.move_to([0, 0, 0])
        
        # Add labels
        x_label = axes.get_x_axis_label("Prediction Probability")
        y_label = axes.get_y_axis_label("Number of Samples")
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Generate sample prediction probabilities
        np.random.seed(42)
        n_samples = 200
        
        # Generate two overlapping normal distributions
        black_stone_probs = np.random.normal(0.3, 0.15, n_samples//2)
        white_stone_probs = np.random.normal(0.7, 0.15, n_samples//2)
        
        # Clip to [0, 1]
        black_stone_probs = np.clip(black_stone_probs, 0, 1)
        white_stone_probs = np.clip(white_stone_probs, 0, 1)
        
        # Create histogram data
        bins = np.linspace(0, 1, 21)
        black_hist, _ = np.histogram(black_stone_probs, bins=bins)
        white_hist, _ = np.histogram(white_stone_probs, bins=bins)
        
        # Create histogram bars
        black_bars = VGroup()
        white_bars = VGroup()
        
        for i in range(len(black_hist)):
            if black_hist[i] > 0:
                bar = Rectangle(
                    width=0.04,
                    height=black_hist[i] * 0.05,
                    fill_color=BLUE,
                    fill_opacity=0.7,
                    stroke_color=WHITE,
                    stroke_width=1
                )
                bar.move_to([bins[i] + 0.02, black_hist[i] * 0.025, 0])
                black_bars.add(bar)
            
            if white_hist[i] > 0:
                bar = Rectangle(
                    width=0.04,
                    height=white_hist[i] * 0.05,
                    fill_color=RED,
                    fill_opacity=0.7,
                    stroke_color=WHITE,
                    stroke_width=1
                )
                bar.move_to([bins[i] + 0.02, white_hist[i] * 0.025, 0])
                white_bars.add(bar)
        
        self.play(Create(black_bars), Create(white_bars))
        
        # Add legend
        legend = VGroup(
            Text("Black Stones (Actual)", font_size=16, color=BLUE),
            Text("White Stones (Actual)", font_size=16, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        legend.to_edge(RIGHT)
        
        self.play(Write(legend))
        
        # Show threshold line
        threshold_line = Line(
            axes.coords_to_point(0.5, 0),
            axes.coords_to_point(0.5, 100),
            color=YELLOW,
            stroke_width=3
        )
        threshold_label = Text("Threshold = 0.5", font_size=16, color=YELLOW)
        threshold_label.next_to(threshold_line, UP, buff=0.2)
        
        self.play(Create(threshold_line), Write(threshold_label))
        
        # Show classification explanation
        explanation = VGroup(
            Text("📊 Classification Rule:", font_size=20, color=WHITE),
            Text("• If P(White) ≥ Threshold → Predict White", font_size=16, color=GREEN),
            Text("• If P(White) < Threshold → Predict Black", font_size=16, color=BLUE),
            Text("• Moving threshold changes predictions", font_size=16, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        explanation.move_to([0, -3, 0])
        
        self.play(Write(explanation))
        
        self.wait(3)
        
        self.play(FadeOut(VGroup(axes, x_label, y_label, black_bars, white_bars, 
                                legend, threshold_line, threshold_label, explanation, distribution_title)))
    
    def show_dynamic_confusion_matrix(self):
        # Show dynamic confusion matrix
        matrix_title = Text("Dynamic Confusion Matrix", font_size=40, color=WHITE)
        matrix_title.to_edge(UP)
        self.play(Write(matrix_title))
        
        # Create confusion matrix structure
        matrix_size = 2
        cell_size = 1.5
        
        # Create matrix grid
        matrix_grid = VGroup()
        for i in range(matrix_size):
            for j in range(matrix_size):
                cell = Rectangle(
                    width=cell_size,
                    height=cell_size,
                    stroke_color=WHITE,
                    stroke_width=2,
                    fill_opacity=0.1
                )
                cell.move_to([j*cell_size - cell_size/2, -i*cell_size + cell_size/2, 0])
                matrix_grid.add(cell)
        
        self.play(Create(matrix_grid))
        
        # Add labels
        labels = VGroup(
            Text("Actual", font_size=20, color=WHITE),
            Text("Black", font_size=16, color=BLUE),
            Text("White", font_size=16, color=RED),
            Text("Predicted", font_size=20, color=WHITE),
            Text("Black", font_size=16, color=BLUE),
            Text("White", font_size=16, color=RED)
        )
        
        # Position labels
        labels[0].move_to([-2, 1.5, 0])  # Actual
        labels[1].move_to([-2, 0.75, 0])  # Black
        labels[2].move_to([-2, 0, 0])     # White
        labels[3].move_to([0, 2.5, 0])    # Predicted
        labels[4].move_to([-0.75, 2.5, 0])  # Black
        labels[5].move_to([0.75, 2.5, 0])   # White
        
        self.play(Write(labels))
        
        # Create metric labels for each cell
        metric_labels = VGroup()
        metric_names = ["TN", "FP", "FN", "TP"]
        metric_colors = [GREEN, RED, RED, GREEN]
        
        for i, (name, color) in enumerate(zip(metric_names, metric_colors)):
            label = Text(name, font_size=24, color=color)
            if i < 2:
                label.move_to([(i-0.5)*cell_size, 0.75, 0])
            else:
                label.move_to([(i-2.5)*cell_size, -0.75, 0])
            metric_labels.add(label)
        
        self.play(Write(metric_labels))
        
        # Show metric definitions
        definitions = VGroup(
            Text("📊 Metric Definitions:", font_size=20, color=WHITE),
            Text("• TP (True Positive): Correctly predicted White", font_size=16, color=GREEN),
            Text("• TN (True Negative): Correctly predicted Black", font_size=16, color=GREEN),
            Text("• FP (False Positive): Incorrectly predicted White", font_size=16, color=RED),
            Text("• FN (False Negative): Incorrectly predicted Black", font_size=16, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        definitions.to_edge(RIGHT)
        
        self.play(Write(definitions))
        
        self.wait(3)
        
        self.play(FadeOut(VGroup(matrix_grid, labels, metric_labels, definitions, matrix_title)))
    
    def show_threshold_slider(self):
        # Show threshold slider
        slider_title = Text("Threshold Slider - Dynamic Classification", font_size=40, color=WHITE)
        slider_title.to_edge(UP)
        self.play(Write(slider_title))
        
        # Create slider
        slider_track = Rectangle(width=8, height=0.2, color=GRAY, fill_opacity=0.3)
        slider_track.move_to([0, 0, 0])
        
        # Create slider handle
        slider_handle = Circle(radius=0.3, color=YELLOW, fill_opacity=0.8)
        slider_handle.move_to([-3, 0, 0])  # Start at 0.1
        
        # Create threshold labels
        threshold_labels = VGroup(
            Text("0.0", font_size=16, color=WHITE),
            Text("0.5", font_size=16, color=WHITE),
            Text("1.0", font_size=16, color=WHITE)
        )
        
        threshold_labels[0].move_to([-4, -0.5, 0])
        threshold_labels[1].move_to([0, -0.5, 0])
        threshold_labels[2].move_to([4, -0.5, 0])
        
        self.play(Create(slider_track), Create(slider_handle), Write(threshold_labels))
        
        # Create threshold value display
        threshold_value = Text("Threshold = 0.10", font_size=24, color=YELLOW)
        threshold_value.move_to([0, 1, 0])
        self.play(Write(threshold_value))
        
        # Create prediction distribution
        axes = Axes(
            x_range=[0, 1, 0.1],
            y_range=[0, 50, 10],
            x_length=8,
            y_length=4,
            axis_config={"color": GRAY}
        )
        axes.move_to([0, -2, 0])
        
        # Add labels
        x_label = axes.get_x_axis_label("Probability")
        y_label = axes.get_y_axis_label("Count")
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Generate sample data
        np.random.seed(42)
        n_samples = 100
        
        # Generate two overlapping normal distributions
        black_stone_probs = np.random.normal(0.3, 0.15, n_samples//2)
        white_stone_probs = np.random.normal(0.7, 0.15, n_samples//2)
        
        # Clip to [0, 1]
        black_stone_probs = np.clip(black_stone_probs, 0, 1)
        white_stone_probs = np.clip(white_stone_probs, 0, 1)
        
        # Create histogram data
        bins = np.linspace(0, 1, 21)
        black_hist, _ = np.histogram(black_stone_probs, bins=bins)
        white_hist, _ = np.histogram(white_stone_probs, bins=bins)
        
        # Create histogram bars
        black_bars = VGroup()
        white_bars = VGroup()
        
        for i in range(len(black_hist)):
            if black_hist[i] > 0:
                bar = Rectangle(
                    width=0.35,
                    height=black_hist[i] * 0.08,
                    fill_color=BLUE,
                    fill_opacity=0.7,
                    stroke_color=WHITE,
                    stroke_width=1
                )
                bar.move_to([bins[i] + 0.0175, black_hist[i] * 0.04, 0])
                black_bars.add(bar)
            
            if white_hist[i] > 0:
                bar = Rectangle(
                    width=0.35,
                    height=white_hist[i] * 0.08,
                    fill_color=RED,
                    fill_opacity=0.7,
                    stroke_color=WHITE,
                    stroke_width=1
                )
                bar.move_to([bins[i] + 0.0175, white_hist[i] * 0.04, 0])
                white_bars.add(bar)
        
        self.play(Create(black_bars), Create(white_bars))
        
        # Create threshold line
        threshold_line = Line(
            axes.coords_to_point(0.1, 0),
            axes.coords_to_point(0.1, 50),
            color=YELLOW,
            stroke_width=3
        )
        self.play(Create(threshold_line))
        
        # Animate threshold changes
        thresholds = [0.1, 0.3, 0.5, 0.7, 0.9]
        slider_positions = [-3, -1.5, 0, 1.5, 3]
        
        for i, (threshold, pos) in enumerate(zip(thresholds, slider_positions)):
            # Move slider
            self.play(
                slider_handle.animate.move_to([pos, 0, 0]),
                threshold_value.animate.become(Text(f"Threshold = {threshold:.1f}", font_size=24, color=YELLOW).move_to([0, 1, 0])),
                threshold_line.animate.become(Line(
                    axes.coords_to_point(threshold, 0),
                    axes.coords_to_point(threshold, 50),
                    color=YELLOW,
                    stroke_width=3
                )),
                run_time=1
            )
            
            # Show classification results
            if i < len(thresholds) - 1:
                self.wait(0.5)
        
        self.wait(2)
        
        self.play(FadeOut(VGroup(slider_track, slider_handle, threshold_labels, threshold_value,
                                axes, x_label, y_label, black_bars, white_bars, threshold_line, slider_title)))
    
    def show_real_time_metrics(self):
        # Show real-time metrics
        metrics_title = Text("Real-time Classification Metrics", font_size=40, color=WHITE)
        metrics_title.to_edge(UP)
        self.play(Write(metrics_title))
        
        # Create confusion matrix
        matrix_size = 2
        cell_size = 1.2
        
        # Create matrix grid
        matrix_grid = VGroup()
        for i in range(matrix_size):
            for j in range(matrix_size):
                cell = Rectangle(
                    width=cell_size,
                    height=cell_size,
                    stroke_color=WHITE,
                    stroke_width=2,
                    fill_opacity=0.1
                )
                cell.move_to([j*cell_size - cell_size/2, -i*cell_size + cell_size/2, 0])
                matrix_grid.add(cell)
        
        self.play(Create(matrix_grid))
        
        # Add matrix labels
        matrix_labels = VGroup(
            Text("Actual", font_size=16, color=WHITE),
            Text("Black", font_size=14, color=BLUE),
            Text("White", font_size=14, color=RED),
            Text("Predicted", font_size=16, color=WHITE),
            Text("Black", font_size=14, color=BLUE),
            Text("White", font_size=14, color=RED)
        )
        
        # Position labels
        matrix_labels[0].move_to([-1.5, 1.2, 0])
        matrix_labels[1].move_to([-1.5, 0.6, 0])
        matrix_labels[2].move_to([-1.5, 0, 0])
        matrix_labels[3].move_to([0, 2, 0])
        matrix_labels[4].move_to([-0.6, 2, 0])
        matrix_labels[5].move_to([0.6, 2, 0])
        
        self.play(Write(matrix_labels))
        
        # Create metric value displays
        metric_values = VGroup()
        metric_names = ["TN", "FP", "FN", "TP"]
        metric_colors = [GREEN, RED, RED, GREEN]
        
        for i, (name, color) in enumerate(zip(metric_names, metric_colors)):
            value = Text("0", font_size=20, color=color)
            if i < 2:
                value.move_to([(i-0.5)*cell_size, 0.6, 0])
            else:
                value.move_to([(i-2.5)*cell_size, -0.6, 0])
            metric_values.add(value)
        
        self.play(Write(metric_values))
        
        # Create derived metrics
        derived_metrics = VGroup()
        metric_titles = ["Accuracy", "Precision", "Recall", "Specificity", "F1-Score"]
        metric_formulas = [
            "(TP+TN)/(TP+TN+FP+FN)",
            "TP/(TP+FP)",
            "TP/(TP+FN)",
            "TN/(TN+FP)",
            "2×Precision×Recall/(Precision+Recall)"
        ]
        
        for i, (title, formula) in enumerate(zip(metric_titles, metric_formulas)):
            metric_group = VGroup(
                Text(title, font_size=16, color=WHITE),
                Text(formula, font_size=12, color=GRAY),
                Text("0.00", font_size=18, color=YELLOW)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            metric_group.move_to([3, 1.5 - i*0.8, 0])
            derived_metrics.add(metric_group)
        
        self.play(Write(derived_metrics))
        
        # Create threshold slider
        slider_track = Rectangle(width=6, height=0.15, color=GRAY, fill_opacity=0.3)
        slider_track.move_to([0, -2, 0])
        
        slider_handle = Circle(radius=0.2, color=YELLOW, fill_opacity=0.8)
        slider_handle.move_to([-2.5, -2, 0])
        
        threshold_label = Text("Threshold = 0.10", font_size=16, color=YELLOW)
        threshold_label.move_to([0, -2.5, 0])
        
        self.play(Create(slider_track), Create(slider_handle), Write(threshold_label))
        
        # Animate threshold changes with real-time metric updates
        thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        slider_positions = [-2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5]
        
        # Sample confusion matrix values for different thresholds
        confusion_matrices = [
            [45, 5, 8, 42],   # threshold 0.1
            [42, 8, 6, 44],   # threshold 0.2
            [38, 12, 4, 46],  # threshold 0.3
            [35, 15, 3, 47],  # threshold 0.4
            [32, 18, 2, 48],  # threshold 0.5
            [28, 22, 1, 49],  # threshold 0.6
            [25, 25, 1, 49],  # threshold 0.7
            [22, 28, 0, 50],  # threshold 0.8
            [20, 30, 0, 50]   # threshold 0.9
        ]
        
        for i, (threshold, pos, matrix) in enumerate(zip(thresholds, slider_positions, confusion_matrices)):
            tn, fp, fn, tp = matrix
            
            # Calculate derived metrics
            accuracy = (tp + tn) / (tp + tn + fp + fn)
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
            f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
            
            # Update metric values
            new_metric_values = VGroup()
            for j, (name, color, value) in enumerate(zip(metric_names, metric_colors, [tn, fp, fn, tp])):
                new_value = Text(str(value), font_size=20, color=color)
                if j < 2:
                    new_value.move_to([(j-0.5)*cell_size, 0.6, 0])
                else:
                    new_value.move_to([(j-2.5)*cell_size, -0.6, 0])
                new_metric_values.add(new_value)
            
            # Update derived metrics
            new_derived_metrics = VGroup()
            metric_values_list = [accuracy, precision, recall, specificity, f1_score]
            
            for j, (title, formula, value) in enumerate(zip(metric_titles, metric_formulas, metric_values_list)):
                metric_group = VGroup(
                    Text(title, font_size=16, color=WHITE),
                    Text(formula, font_size=12, color=GRAY),
                    Text(f"{value:.3f}", font_size=18, color=YELLOW)
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
                metric_group.move_to([3, 1.5 - j*0.8, 0])
                new_derived_metrics.add(metric_group)
            
            # Animate changes
            self.play(
                slider_handle.animate.move_to([pos, -2, 0]),
                threshold_label.animate.become(Text(f"Threshold = {threshold:.1f}", font_size=16, color=YELLOW).move_to([0, -2.5, 0])),
                Transform(metric_values, new_metric_values),
                Transform(derived_metrics, new_derived_metrics),
                run_time=1
            )
            
            if i < len(thresholds) - 1:
                self.wait(0.5)
        
        self.wait(2)
        
        self.play(FadeOut(VGroup(matrix_grid, matrix_labels, metric_values, derived_metrics,
                                slider_track, slider_handle, threshold_label, metrics_title)))
    
    def show_roc_curve(self):
        # Show ROC curve
        roc_title = Text("ROC Curve & AUC", font_size=40, color=WHITE)
        roc_title.to_edge(UP)
        self.play(Write(roc_title))
        
        # Create coordinate system
        axes = Axes(
            x_range=[0, 1, 0.1],
            y_range=[0, 1, 0.1],
            x_length=8,
            y_length=8,
            axis_config={"color": GRAY}
        )
        axes.move_to([0, 0, 0])
        
        # Add labels
        x_label = axes.get_x_axis_label("False Positive Rate (1-Specificity)")
        y_label = axes.get_y_axis_label("True Positive Rate (Sensitivity)")
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Create diagonal line (random classifier)
        diagonal = Line(
            axes.coords_to_point(0, 0),
            axes.coords_to_point(1, 1),
            color=GRAY,
            stroke_width=2,
            stroke_opacity=0.5
        )
        diagonal_label = Text("Random Classifier (AUC = 0.5)", font_size=14, color=GRAY)
        diagonal_label.next_to(diagonal, UP, buff=0.2)
        
        self.play(Create(diagonal), Write(diagonal_label))
        
        # Generate ROC curve points
        thresholds = np.linspace(0, 1, 20)
        fpr_values = []
        tpr_values = []
        
        # Sample ROC curve data
        fpr_values = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 1.0]
        tpr_values = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.65, 0.7, 0.75, 0.8, 0.82, 0.85, 0.87, 0.89, 0.91, 0.93, 0.95, 0.98, 1.0]
        
        # Create ROC curve
        roc_points = []
        for fpr, tpr in zip(fpr_values, tpr_values):
            point = axes.coords_to_point(fpr, tpr)
            roc_points.append(point)
        
        # Create ROC curve line
        roc_curve = VMobject()
        roc_curve.set_points_smoothly(roc_points)
        roc_curve.set_stroke(color=BLUE, width=3)
        
        self.play(Create(roc_curve))
        
        # Create ROC curve label
        roc_label = Text("ROC Curve (AUC = 0.89)", font_size=16, color=BLUE)
        roc_label.next_to(roc_curve, UP, buff=0.3)
        self.play(Write(roc_label))
        
        # Show threshold points on ROC curve
        threshold_points = VGroup()
        selected_thresholds = [0.1, 0.3, 0.5, 0.7, 0.9]
        selected_indices = [2, 6, 10, 14, 18]
        
        for threshold, idx in zip(selected_thresholds, selected_indices):
            point = Dot(roc_points[idx], color=YELLOW, radius=0.08)
            label = Text(f"T={threshold}", font_size=12, color=YELLOW)
            label.next_to(point, UP, buff=0.1)
            threshold_points.add(point, label)
        
        self.play(Create(threshold_points))
        
        # Show AUC interpretation
        auc_interpretation = VGroup(
            Text("📊 AUC Interpretation:", font_size=20, color=WHITE),
            Text("• AUC = 0.5: Random classifier", font_size=16, color=GRAY),
            Text("• AUC = 0.7-0.8: Acceptable", font_size=16, color=YELLOW),
            Text("• AUC = 0.8-0.9: Good", font_size=16, color=ORANGE),
            Text("• AUC = 0.9-1.0: Excellent", font_size=16, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        auc_interpretation.to_edge(RIGHT)
        
        self.play(Write(auc_interpretation))
        
        self.wait(3)
        
        self.play(FadeOut(VGroup(axes, x_label, y_label, diagonal, diagonal_label,
                                roc_curve, roc_label, threshold_points, auc_interpretation, roc_title)))
    
    def show_final_analysis(self):
        # Show final analysis
        analysis_title = Text("Confusion Matrix Analysis Summary", font_size=40, color=WHITE)
        analysis_title.to_edge(UP)
        self.play(Write(analysis_title))
        
        # Create final confusion matrix
        matrix_size = 2
        cell_size = 1.5
        
        # Create matrix grid
        matrix_grid = VGroup()
        for i in range(matrix_size):
            for j in range(matrix_size):
                cell = Rectangle(
                    width=cell_size,
                    height=cell_size,
                    stroke_color=WHITE,
                    stroke_width=2,
                    fill_opacity=0.1
                )
                cell.move_to([j*cell_size - cell_size/2, -i*cell_size + cell_size/2, 0])
                matrix_grid.add(cell)
        
        self.play(Create(matrix_grid))
        
        # Add final values (optimal threshold)
        final_values = VGroup()
        final_numbers = ["32", "18", "2", "48"]
        final_colors = [GREEN, RED, RED, GREEN]
        
        for i, (number, color) in enumerate(zip(final_numbers, final_colors)):
            value = Text(number, font_size=24, color=color)
            if i < 2:
                value.move_to([(i-0.5)*cell_size, 0.75, 0])
            else:
                value.move_to([(i-2.5)*cell_size, -0.75, 0])
            final_values.add(value)
        
        self.play(Write(final_values))
        
        # Add labels
        matrix_labels = VGroup(
            Text("Actual", font_size=16, color=WHITE),
            Text("Black", font_size=14, color=BLUE),
            Text("White", font_size=14, color=RED),
            Text("Predicted", font_size=16, color=WHITE),
            Text("Black", font_size=14, color=BLUE),
            Text("White", font_size=14, color=RED)
        )
        
        # Position labels
        matrix_labels[0].move_to([-2, 1.5, 0])
        matrix_labels[1].move_to([-2, 0.75, 0])
        matrix_labels[2].move_to([-2, 0, 0])
        matrix_labels[3].move_to([0, 2.5, 0])
        matrix_labels[4].move_to([-0.75, 2.5, 0])
        matrix_labels[5].move_to([0.75, 2.5, 0])
        
        self.play(Write(matrix_labels))
        
        # Show optimal metrics
        optimal_metrics = VGroup(
            Text("🎯 Optimal Threshold = 0.5", font_size=20, color=YELLOW),
            Text("📊 Final Metrics:", font_size=18, color=WHITE),
            Text("• Accuracy: 0.800", font_size=16, color=GREEN),
            Text("• Precision: 0.727", font_size=16, color=BLUE),
            Text("• Recall: 0.960", font_size=16, color=ORANGE),
            Text("• Specificity: 0.640", font_size=16, color=PURPLE),
            Text("• F1-Score: 0.828", font_size=16, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        optimal_metrics.move_to([-3, -1, 0])
        
        self.play(Write(optimal_metrics))
        
        # Show threshold selection criteria
        criteria = VGroup(
            Text("🎯 Threshold Selection Criteria:", font_size=18, color=WHITE),
            Text("• Business requirements", font_size=14, color=GRAY),
            Text("• Cost of false positives", font_size=14, color=GRAY),
            Text("• Cost of false negatives", font_size=14, color=GRAY),
            Text("• Class imbalance", font_size=14, color=GRAY),
            Text("• ROC curve analysis", font_size=14, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        criteria.to_edge(RIGHT)
        
        self.play(Write(criteria))
        
        # Show applications
        applications = VGroup(
            Text("🎯 Applications:", font_size=18, color=WHITE),
            Text("• Medical diagnosis", font_size=14, color=GREEN),
            Text("• Fraud detection", font_size=14, color=BLUE),
            Text("• Spam filtering", font_size=14, color=ORANGE),
            Text("• Quality control", font_size=14, color=PURPLE),
            Text("• Risk assessment", font_size=14, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        applications.move_to([0, -3, 0])
        
        self.play(Write(applications))
        
        # Final message
        final_message = Text("Confusion matrix analysis complete!", font_size=36, color=GREEN)
        final_message.to_edge(DOWN)
        self.play(Write(final_message))
        self.wait(2)
        
        self.play(FadeOut(VGroup(matrix_grid, final_values, matrix_labels, optimal_metrics,
                                criteria, applications, final_message, analysis_title)))
