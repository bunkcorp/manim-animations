from manim import *
import numpy as np

class ThresholdMetricsAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a1a"
        
        # Generate realistic prediction data
        np.random.seed(42)
        self.generate_sample_data()
        
        # Main sections
        self.show_title()
        self.show_threshold_slider_with_metrics()
        self.show_metrics_plots()
        self.show_roc_curve()
        self.show_precision_recall_curve()
        self.show_optimal_threshold()
        
    def generate_sample_data(self):
        """Generate realistic binary classification data"""
        n_samples = 1000
        
        # Class 0 (negative): lower probabilities, centered around 0.3
        class_0_probs = np.random.beta(2, 5, n_samples // 2)
        
        # Class 1 (positive): higher probabilities, centered around 0.7  
        class_1_probs = np.random.beta(5, 2, n_samples // 2)
        
        # Combine data
        self.y_true = np.concatenate([np.zeros(n_samples // 2), np.ones(n_samples // 2)])
        self.y_probs = np.concatenate([class_0_probs, class_1_probs])
        
        # Shuffle
        idx = np.random.permutation(n_samples)
        self.y_true = self.y_true[idx]
        self.y_probs = self.y_probs[idx]
    
    def calculate_metrics(self, threshold):
        """Calculate confusion matrix and metrics for given threshold"""
        y_pred = (self.y_probs >= threshold).astype(int)
        
        # Confusion matrix components
        tn = np.sum((self.y_true == 0) & (y_pred == 0))
        fp = np.sum((self.y_true == 0) & (y_pred == 1))
        fn = np.sum((self.y_true == 1) & (y_pred == 0))
        tp = np.sum((self.y_true == 1) & (y_pred == 1))
        
        # Metrics
        accuracy = (tp + tn) / (tp + tn + fp + fn)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        
        return {
            'tn': tn, 'fp': fp, 'fn': fn, 'tp': tp,
            'accuracy': accuracy, 'precision': precision, 'recall': recall,
            'specificity': specificity, 'f1': f1
        }
    
    def show_title(self):
        title = Text("Dynamic Threshold Analysis", font_size=48, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1)
    
    def show_threshold_slider_with_metrics(self):
        # Create layout
        left_group = VGroup()  # Confusion matrix
        center_group = VGroup()  # Slider
        right_group = VGroup()  # Metrics
        
        # === CONFUSION MATRIX (LEFT) ===
        matrix_title = Text("Confusion Matrix", font_size=24, color=WHITE)
        
        # Create 2x2 grid
        cell_size = 1.0
        matrix_cells = VGroup()
        for i in range(2):
            for j in range(2):
                cell = Square(side_length=cell_size, stroke_color=WHITE, stroke_width=2)
                cell.move_to([j * cell_size - cell_size/2, -i * cell_size + cell_size/2, 0])
                matrix_cells.add(cell)
        
        # Labels
        matrix_labels = VGroup(
            Text("Actual", font_size=16, color=GRAY).move_to([-1.8, 0.25, 0]),
            Text("0", font_size=14, color=BLUE).move_to([-1.8, 0.5, 0]),
            Text("1", font_size=14, color=RED).move_to([-1.8, -0.5, 0]),
            Text("Predicted", font_size=16, color=GRAY).move_to([0, 1.3, 0]),
            Text("0", font_size=14, color=BLUE).move_to([-0.5, 1.3, 0]),
            Text("1", font_size=14, color=RED).move_to([0.5, 1.3, 0])
        )
        
        # Values (will be updated)
        self.matrix_values = VGroup()
        positions = [(-0.5, 0.5), (0.5, 0.5), (-0.5, -0.5), (0.5, -0.5)]
        colors = [GREEN, RED, RED, GREEN]
        labels = ["TN", "FP", "FN", "TP"]
        
        for i, (pos, color, label) in enumerate(zip(positions, colors, labels)):
            value_text = Text("0", font_size=20, color=color)
            value_text.move_to([pos[0], pos[1], 0])
            label_text = Text(label, font_size=12, color=color)
            label_text.move_to([pos[0], pos[1] - 0.3, 0])
            self.matrix_values.add(VGroup(value_text, label_text))
        
        left_group.add(matrix_title, matrix_cells, matrix_labels, self.matrix_values)
        left_group.arrange(DOWN, buff=0.3)
        left_group.to_edge(LEFT, buff=1)
        
        # === THRESHOLD SLIDER (CENTER) ===
        slider_title = Text("Threshold", font_size=24, color=WHITE)
        
        # Vertical slider
        slider_track = Rectangle(width=0.3, height=4, color=GRAY, fill_opacity=0.3)
        self.slider_handle = Circle(radius=0.2, color=YELLOW, fill_opacity=0.8)
        self.slider_handle.move_to([0, 1, 0])  # Start at threshold 0.75
        
        # Threshold labels
        threshold_labels = VGroup()
        for i, val in enumerate([1.0, 0.75, 0.5, 0.25, 0.0]):
            label = Text(f"{val:.2f}", font_size=14, color=GRAY)
            label.move_to([0.8, 2 - i, 0])
            threshold_labels.add(label)
        
        # Current threshold display
        self.threshold_display = Text("Threshold = 0.75", font_size=18, color=YELLOW)
        self.threshold_display.move_to([0, -3, 0])
        
        center_group.add(slider_title, slider_track, self.slider_handle, 
                        threshold_labels, self.threshold_display)
        center_group.arrange(DOWN, buff=0.3)
        center_group.move_to([0, 0, 0])
        
        # === METRICS (RIGHT) ===
        metrics_title = Text("Performance Metrics", font_size=24, color=WHITE)
        
        self.metrics_display = VGroup()
        metric_names = ["Accuracy", "Precision", "Recall", "Specificity", "F1-Score"]
        metric_colors = [WHITE, BLUE, GREEN, ORANGE, PURPLE]
        
        for i, (name, color) in enumerate(zip(metric_names, metric_colors)):
            metric_text = Text(f"{name}: 0.000", font_size=16, color=color)
            metric_text.move_to([0, 1 - i * 0.4, 0])
            self.metrics_display.add(metric_text)
        
        right_group.add(metrics_title, self.metrics_display)
        right_group.arrange(DOWN, buff=0.3)
        right_group.to_edge(RIGHT, buff=1)
        
        # Show all components
        self.play(
            Create(left_group),
            Create(center_group),  
            Create(right_group)
        )
        self.wait(1)
        
        # Animate threshold changes
        thresholds = np.linspace(0.9, 0.1, 9)
        slider_positions = np.linspace(1.6, -1.6, 9)
        
        for threshold, pos in zip(thresholds, slider_positions):
            # Calculate metrics for current threshold
            metrics = self.calculate_metrics(threshold)
            
            # Update displays
            self.update_displays(threshold, pos, metrics)
            self.wait(0.8)
    
    def update_displays(self, threshold, slider_pos, metrics):
        """Update all displays with new threshold and metrics"""
        # Update slider position
        new_handle = Circle(radius=0.2, color=YELLOW, fill_opacity=0.8)
        new_handle.move_to([0, slider_pos, 0])
        
        # Update threshold display
        new_threshold_display = Text(f"Threshold = {threshold:.2f}", 
                                   font_size=18, color=YELLOW)
        new_threshold_display.move_to([0, -3, 0])
        
        # Update confusion matrix values
        new_matrix_values = VGroup()
        positions = [(-0.5, 0.5), (0.5, 0.5), (-0.5, -0.5), (0.5, -0.5)]
        colors = [GREEN, RED, RED, GREEN]
        labels = ["TN", "FP", "FN", "TP"]
        values = [metrics['tn'], metrics['fp'], metrics['fn'], metrics['tp']]
        
        for i, (pos, color, label, value) in enumerate(zip(positions, colors, labels, values)):
            value_text = Text(str(value), font_size=20, color=color)
            value_text.move_to([pos[0], pos[1], 0])
            label_text = Text(label, font_size=12, color=color)
            label_text.move_to([pos[0], pos[1] - 0.3, 0])
            new_matrix_values.add(VGroup(value_text, label_text))
        
        # Update metrics display
        new_metrics_display = VGroup()
        metric_names = ["Accuracy", "Precision", "Recall", "Specificity", "F1-Score"]
        metric_values = [metrics['accuracy'], metrics['precision'], metrics['recall'],
                        metrics['specificity'], metrics['f1']]
        metric_colors = [WHITE, BLUE, GREEN, ORANGE, PURPLE]
        
        for i, (name, value, color) in enumerate(zip(metric_names, metric_values, metric_colors)):
            metric_text = Text(f"{name}: {value:.3f}", font_size=16, color=color)
            metric_text.move_to([0, 1 - i * 0.4, 0])
            new_metrics_display.add(metric_text)
        
        # Animate updates
        self.play(
            Transform(self.slider_handle, new_handle),
            Transform(self.threshold_display, new_threshold_display),
            Transform(self.matrix_values, new_matrix_values),
            Transform(self.metrics_display, new_metrics_display),
            run_time=0.5
        )
    
    def show_metrics_plots(self):
        """Show how metrics change across all thresholds"""
        self.clear()
        
        # Title
        title = Text("Metrics vs Threshold", font_size=48, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        
        # Calculate metrics for all thresholds
        thresholds = np.linspace(0.01, 0.99, 50)
        all_metrics = [self.calculate_metrics(t) for t in thresholds]
        
        # Create axes
        axes = Axes(
            x_range=[0, 1, 0.1],
            y_range=[0, 1, 0.1],
            x_length=10,
            y_length=6,
            axis_config={"color": GRAY}
        )
        axes.to_edge(DOWN, buff=1)
        
        # Labels
        x_label = axes.get_x_axis_label("Threshold", direction=DOWN)
        y_label = axes.get_y_axis_label("Metric Value", direction=LEFT)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Plot metrics
        metric_names = ["Accuracy", "Precision", "Recall", "Specificity", "F1-Score"]
        metric_colors = [WHITE, BLUE, GREEN, ORANGE, PURPLE]
        metric_keys = ["accuracy", "precision", "recall", "specificity", "f1"]
        
        curves = VGroup()
        legend = VGroup()
        
        for i, (name, color, key) in enumerate(zip(metric_names, metric_colors, metric_keys)):
            # Extract metric values
            metric_values = [m[key] for m in all_metrics]
            
            # Create curve points
            points = [axes.coords_to_point(t, v) for t, v in zip(thresholds, metric_values)]
            
            # Create curve
            curve = VMobject(color=color, stroke_width=3)
            curve.set_points_smoothly(points)
            curves.add(curve)
            
            # Legend entry
            legend_item = VGroup(
                Line(ORIGIN, RIGHT * 0.5, color=color, stroke_width=3),
                Text(name, font_size=16, color=color)
            ).arrange(RIGHT, buff=0.2)
            legend_item.move_to([4, 2.5 - i * 0.4, 0])
            legend.add(legend_item)
        
        # Animate curves
        for curve in curves:
            self.play(Create(curve), run_time=1.5)
        
        self.play(Write(legend))
        
        # Highlight optimal threshold
        optimal_idx = np.argmax([m['f1'] for m in all_metrics])
        optimal_threshold = thresholds[optimal_idx]
        optimal_metrics = all_metrics[optimal_idx]
        
        # Vertical line at optimal threshold
        optimal_line = DashedLine(
            axes.coords_to_point(optimal_threshold, 0),
            axes.coords_to_point(optimal_threshold, 1),
            color=YELLOW,
            stroke_width=3
        )
        
        optimal_label = Text(f"Optimal: {optimal_threshold:.3f}", 
                           font_size=18, color=YELLOW)
        optimal_label.next_to(optimal_line, UP)
        
        self.play(Create(optimal_line), Write(optimal_label))
        
        # Show optimal metrics
        optimal_text = VGroup(
            Text("Optimal Threshold Metrics:", font_size=20, color=YELLOW),
            Text(f"F1-Score: {optimal_metrics['f1']:.3f}", font_size=16, color=PURPLE),
            Text(f"Accuracy: {optimal_metrics['accuracy']:.3f}", font_size=16, color=WHITE),
            Text(f"Precision: {optimal_metrics['precision']:.3f}", font_size=16, color=BLUE),
            Text(f"Recall: {optimal_metrics['recall']:.3f}", font_size=16, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        optimal_text.to_corner(UL, buff=1)
        
        self.play(Write(optimal_text))
        self.wait(3)
    
    def show_roc_curve(self):
        """Show ROC curve with threshold points"""
        self.clear()
        
        title = Text("ROC Curve Analysis", font_size=48, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        
        # Calculate ROC curve data
        thresholds = np.linspace(0.99, 0.01, 100)
        fpr_values = []
        tpr_values = []
        
        for threshold in thresholds:
            metrics = self.calculate_metrics(threshold)
            fpr = 1 - metrics['specificity']  # 1 - specificity = FP/(FP+TN)
            tpr = metrics['recall']  # recall = TP/(TP+FN)
            fpr_values.append(fpr)
            tpr_values.append(tpr)
        
        # Create axes
        axes = Axes(
            x_range=[0, 1, 0.1],
            y_range=[0, 1, 0.1],
            x_length=8,
            y_length=8,
            axis_config={"color": GRAY}
        )
        axes.move_to([0, -0.5, 0])
        
        # Labels
        x_label = axes.get_x_axis_label("False Positive Rate (1 - Specificity)", direction=DOWN)
        y_label = axes.get_y_axis_label("True Positive Rate (Sensitivity)", direction=LEFT)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Random classifier diagonal line
        diagonal = Line(
            axes.coords_to_point(0, 0),
            axes.coords_to_point(1, 1),
            color=GRAY,
            stroke_width=2,
            stroke_opacity=0.7
        )
        diagonal_label = Text("Random Classifier", font_size=14, color=GRAY)
        diagonal_label.move_to(axes.coords_to_point(0.7, 0.8))
        
        self.play(Create(diagonal), Write(diagonal_label))
        
        # Create ROC curve
        roc_points = [axes.coords_to_point(fpr, tpr) for fpr, tpr in zip(fpr_values, tpr_values)]
        
        roc_curve = VMobject(color=BLUE, stroke_width=4)
        roc_curve.set_points_smoothly(roc_points)
        
        self.play(Create(roc_curve), run_time=2)
        
        # Calculate AUC using trapezoidal rule
        auc = np.trapz(tpr_values, fpr_values)
        
        # Show AUC
        auc_text = Text(f"AUC = {auc:.3f}", font_size=24, color=BLUE)
        auc_text.to_corner(UR, buff=1)
        self.play(Write(auc_text))
        
        # Show specific threshold points
        threshold_points = [0.1, 0.3, 0.5, 0.7, 0.9]
        colors = [RED, ORANGE, YELLOW, GREEN, PURPLE]
        
        points_group = VGroup()
        labels_group = VGroup()
        
        for i, (thresh, color) in enumerate(zip(threshold_points, colors)):
            # Find closest threshold in our data
            idx = np.argmin(np.abs(thresholds - thresh))
            fpr = fpr_values[idx]
            tpr = tpr_values[idx]
            
            # Create point
            point = Dot(axes.coords_to_point(fpr, tpr), color=color, radius=0.08)
            points_group.add(point)
            
            # Create label
            label = Text(f"T={thresh}", font_size=12, color=color)
            label.next_to(point, UP + RIGHT, buff=0.1)
            labels_group.add(label)
        
        self.play(Create(points_group), Write(labels_group))
        
        # ROC interpretation
        interpretation = VGroup(
            Text("📊 ROC Curve Interpretation:", font_size=20, color=WHITE),
            Text("• Perfect classifier: AUC = 1.0", font_size=16, color=GREEN),
            Text("• Good classifier: AUC > 0.8", font_size=16, color=BLUE),
            Text("• Fair classifier: AUC 0.6-0.8", font_size=16, color=YELLOW),
            Text("• Poor classifier: AUC < 0.6", font_size=16, color=RED),
            Text("• Random classifier: AUC = 0.5", font_size=16, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        interpretation.to_corner(UL, buff=0.5)
        
        self.play(Write(interpretation))
        self.wait(3)
        
        # Animate threshold movement along curve
        moving_point = Dot(roc_points[0], color=YELLOW, radius=0.12)
        threshold_tracker = Text("Threshold = 0.99", font_size=16, color=YELLOW)
        threshold_tracker.next_to(moving_point, UP, buff=0.3)
        
        self.play(Create(moving_point), Write(threshold_tracker))
        
        # Move point along curve
        for i in range(0, len(roc_points), 5):
            new_point = Dot(roc_points[i], color=YELLOW, radius=0.12)
            new_label = Text(f"Threshold = {thresholds[i]:.2f}", font_size=16, color=YELLOW)
            new_label.next_to(new_point, UP, buff=0.3)
            
            self.play(
                Transform(moving_point, new_point),
                Transform(threshold_tracker, new_label),
                run_time=0.1
            )
        
        self.wait(2)
    
    def show_precision_recall_curve(self):
        """Show Precision-Recall curve"""
        self.clear()
        
        title = Text("Precision-Recall Curve", font_size=48, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        
        # Calculate Precision-Recall curve data
        thresholds = np.linspace(0.99, 0.01, 100)
        precision_values = []
        recall_values = []
        
        for threshold in thresholds:
            metrics = self.calculate_metrics(threshold)
            precision_values.append(metrics['precision'])
            recall_values.append(metrics['recall'])
        
        # Create axes
        axes = Axes(
            x_range=[0, 1, 0.1],
            y_range=[0, 1, 0.1],
            x_length=8,
            y_length=8,
            axis_config={"color": GRAY}
        )
        axes.move_to([0, -0.5, 0])
        
        # Labels
        x_label = axes.get_x_axis_label("Recall (True Positive Rate)", direction=DOWN)
        y_label = axes.get_y_axis_label("Precision", direction=LEFT)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Baseline (random classifier for imbalanced data)
        baseline_precision = np.sum(self.y_true) / len(self.y_true)  # Proportion of positive class
        baseline_line = Line(
            axes.coords_to_point(0, baseline_precision),
            axes.coords_to_point(1, baseline_precision),
            color=GRAY,
            stroke_width=2,
            stroke_opacity=0.7
        )
        baseline_label = Text(f"Random Classifier (P={baseline_precision:.3f})", 
                            font_size=14, color=GRAY)
        baseline_label.next_to(baseline_line, RIGHT, buff=0.1)
        
        self.play(Create(baseline_line), Write(baseline_label))
        
        # Create PR curve
        pr_points = [axes.coords_to_point(recall, precision) 
                    for recall, precision in zip(recall_values, precision_values)]
        
        pr_curve = VMobject(color=GREEN, stroke_width=4)
        pr_curve.set_points_smoothly(pr_points)
        
        self.play(Create(pr_curve), run_time=2)
        
        # Calculate Average Precision (AP) - approximation using trapezoidal rule
        # Sort by recall for proper integration
        sorted_indices = np.argsort(recall_values)
        sorted_recall = np.array(recall_values)[sorted_indices]
        sorted_precision = np.array(precision_values)[sorted_indices]
        
        ap = np.trapz(sorted_precision, sorted_recall)
        
        # Show AP
        ap_text = Text(f"Average Precision = {ap:.3f}", font_size=24, color=GREEN)
        ap_text.to_corner(UR, buff=1)
        self.play(Write(ap_text))
        
        # Show specific threshold points
        threshold_points = [0.1, 0.3, 0.5, 0.7, 0.9]
        colors = [RED, ORANGE, YELLOW, BLUE, PURPLE]
        
        points_group = VGroup()
        labels_group = VGroup()
        
        for thresh, color in zip(threshold_points, colors):
            # Find closest threshold in our data
            idx = np.argmin(np.abs(thresholds - thresh))
            precision = precision_values[idx]
            recall = recall_values[idx]
            
            # Create point
            point = Dot(axes.coords_to_point(recall, precision), color=color, radius=0.08)
            points_group.add(point)
            
            # Create label
            label = Text(f"T={thresh}", font_size=12, color=color)
            if precision > 0.5:  # Place label below if point is in upper area
                label.next_to(point, DOWN + LEFT, buff=0.1)
            else:
                label.next_to(point, UP + RIGHT, buff=0.1)
            labels_group.add(label)
        
        self.play(Create(points_group), Write(labels_group))
        
        # PR curve interpretation
        interpretation = VGroup(
            Text("📊 Precision-Recall Analysis:", font_size=20, color=WHITE),
            Text("• Higher curve = better performance", font_size=16, color=GREEN),
            Text("• Top-right corner = perfect classifier", font_size=16, color=BLUE),
            Text("• Useful for imbalanced datasets", font_size=16, color=YELLOW),
            Text("• Trade-off: ↑Recall often means ↓Precision", font_size=16, color=ORANGE),
            Text("• Average Precision summarizes curve", font_size=16, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        interpretation.to_corner(UL, buff=0.5)
        
        self.play(Write(interpretation))
        
        # Show the trade-off more clearly
        tradeoff_arrow = DoubleArrow(
            axes.coords_to_point(0.2, 0.9),
            axes.coords_to_point(0.9, 0.3),
            color=RED,
            stroke_width=3
        )
        tradeoff_label = Text("Precision-Recall Trade-off", font_size=14, color=RED)
        tradeoff_label.next_to(tradeoff_arrow, LEFT, buff=0.1)
        
        self.play(Create(tradeoff_arrow), Write(tradeoff_label))
        
        self.wait(3)
        
        # Animate threshold movement along curve
        moving_point = Dot(pr_points[0], color=YELLOW, radius=0.12)
        threshold_tracker = Text("Threshold = 0.99", font_size=16, color=YELLOW)
        threshold_tracker.next_to(moving_point, UP, buff=0.3)
        
        self.play(Create(moving_point), Write(threshold_tracker))
        
        # Move point along curve
        for i in range(0, len(pr_points), 5):
            new_point = Dot(pr_points[i], color=YELLOW, radius=0.12)
            new_label = Text(f"T={thresholds[i]:.2f}", font_size=16, color=YELLOW)
            new_label.next_to(new_point, UP, buff=0.3)
            
            self.play(
                Transform(moving_point, new_point),
                Transform(threshold_tracker, new_label),
                run_time=0.1
            )
        
        self.wait(2)
    
    def show_optimal_threshold(self):
        """Show analysis of optimal threshold selection"""
        self.clear()
        
        title = Text("Threshold Selection Strategy", font_size=48, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        
        # Create sections
        strategies = VGroup(
            Text("🎯 Business Context Matters", font_size=24, color=YELLOW),
            Text("• Medical Diagnosis: High Recall (catch all diseases)", font_size=16, color=GREEN),
            Text("• Spam Detection: High Precision (avoid false positives)", font_size=16, color=BLUE),
            Text("• Fraud Detection: Balance based on cost of errors", font_size=16, color=ORANGE),
            Text("", font_size=16),  # Spacer
            Text("📊 Curve Comparison Summary", font_size=24, color=YELLOW),
            Text("• ROC Curve: Good for balanced datasets", font_size=16, color=BLUE),
            Text("• PR Curve: Better for imbalanced datasets", font_size=16, color=GREEN),
            Text("• Both curves help choose optimal thresholds", font_size=16, color=PURPLE),
            Text("", font_size=16),  # Spacer
            Text("📈 Optimization Strategies", font_size=24, color=YELLOW),
            Text("• F1-Score: Balance precision and recall", font_size=16, color=PURPLE),
            Text("• ROC-AUC: Overall discriminative ability", font_size=16, color=RED),
            Text("• Business metric: Minimize cost or maximize profit", font_size=16, color=ORANGE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        strategies.move_to(ORIGIN)
        self.play(Write(strategies))
        
        self.wait(5)
        
        # Final message
        final_msg = Text("Choose thresholds based on your specific use case!", 
                        font_size=32, color=GREEN)
        final_msg.to_edge(DOWN)
        self.play(Write(final_msg))
        self.wait(3)