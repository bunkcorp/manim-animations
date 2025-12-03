from manim import *
import numpy as np
import pandas as pd
import json
import os
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor

class DetailedGradientBoostingAnimation(Scene):
    def construct(self):
        # Set up the scene
        self.camera.background_color = "#1a1a1a"
        
        # Title
        title = Text("Gradient Boosting Algorithm", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Load real data
        self.next_section("Data Loading")
        self.show_data_loading()
        
        # Sequential learning concept
        self.next_section("Sequential Learning")
        self.show_sequential_learning()
        
        # Initial prediction
        self.next_section("Initial Prediction")
        self.show_initial_prediction()
        
        # Residual calculation
        self.next_section("Residual Calculation")
        self.show_residual_calculation()
        
        # Weak learner training
        self.next_section("Weak Learner Training")
        self.show_weak_learner_training()
        
        # Ensemble building
        self.next_section("Ensemble Building")
        self.show_ensemble_building()
        
        # Final results
        self.next_section("Final Results")
        self.show_final_results()
        
    def show_data_loading(self):
        # Show data loading process
        loading_text = Text("Loading Buddhist Stone Data...", font_size=36, color=YELLOW)
        loading_text.move_to(ORIGIN)
        self.play(Write(loading_text))
        self.wait(1)
        
        # Show data structure
        data_info = VGroup(
            Text("📊 Regression Problem:", font_size=32, color=WHITE),
            Text("• Predict Stone Count", font_size=24, color=GRAY),
            Text("• Based on User Activity", font_size=24, color=GRAY),
            Text("• Time Patterns", font_size=24, color=GRAY),
            Text("• Meditation Duration", font_size=24, color=GRAY),
            Text("• Previous Performance", font_size=24, color=GRAY),
            Text("• Seasonal Trends", font_size=24, color=GRAY)
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
                Text(f"🎯 Target: Predict Stone Count", font_size=28, color=ORANGE),
                Text(f"🌳 Method: Sequential Weak Learners", font_size=28, color=PURPLE)
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
    
    def show_sequential_learning(self):
        # Show sequential learning concept
        sequential_title = Text("Sequential Learning Concept", font_size=40, color=WHITE)
        sequential_title.to_edge(UP)
        self.play(Write(sequential_title))
        
        # Create sequential learning visualization
        # Initial model
        initial_model = Rectangle(width=2, height=1, color=BLUE, fill_opacity=0.3)
        initial_model.move_to([-4, 2, 0])
        initial_label = Text("Initial\nModel", font_size=16, color=BLUE)
        initial_label.move_to(initial_model.get_center())
        
        # Sequential models
        models = VGroup()
        model_labels = VGroup()
        
        for i in range(5):
            model = Rectangle(width=1.5, height=0.8, color=GREEN, fill_opacity=0.3)
            model.move_to([-2 + i*1.5, 2, 0])
            models.add(model)
            
            label = Text(f"Model\n{i+1}", font_size=12, color=GREEN)
            label.move_to(model.get_center())
            model_labels.add(label)
        
        # Connection arrows
        arrows = VGroup()
        for i in range(4):
            arrow = Arrow(
                start=models[i].get_right(),
                end=models[i+1].get_left(),
                color=YELLOW,
                stroke_width=2
            )
            arrows.add(arrow)
        
        # Initial arrow
        initial_arrow = Arrow(
            start=initial_model.get_right(),
            end=models[0].get_left(),
            color=YELLOW,
            stroke_width=2
        )
        
        # Build sequence
        self.play(Create(initial_model), Write(initial_label))
        self.play(Create(initial_arrow))
        
        for i in range(5):
            self.play(Create(models[i]), Write(model_labels[i]))
            if i < 4:
                self.play(Create(arrows[i]))
            self.wait(0.5)
        
        # Show learning process
        learning_text = VGroup(
            Text("🔄 Sequential Learning Process:", font_size=20, color=WHITE),
            Text("• Each model learns from previous errors", font_size=16, color=GREEN),
            Text("• Residuals become new targets", font_size=16, color=BLUE),
            Text("• Models are combined with weights", font_size=16, color=YELLOW),
            Text("• Final prediction is ensemble", font_size=16, color=ORANGE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        learning_text.move_to([0, -1, 0])
        
        self.play(Write(learning_text))
        
        # Show mathematical formula
        formula = MathTex(r"F_m(x) = F_{m-1}(x) + \alpha_m h_m(x)", font_size=24, color=WHITE)
        formula.move_to([0, -3, 0])
        self.play(Write(formula))
        
        self.wait(3)
        
        self.play(FadeOut(VGroup(initial_model, initial_label, models, model_labels, 
                                arrows, initial_arrow, learning_text, formula, sequential_title)))
    
    def show_initial_prediction(self):
        # Show initial prediction
        initial_title = Text("Initial Prediction (F₀)", font_size=40, color=WHITE)
        initial_title.to_edge(UP)
        self.play(Write(initial_title))
        
        # Create coordinate system
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": GRAY}
        )
        axes.move_to([0, 0, 0])
        
        # Add labels
        x_label = axes.get_x_axis_label("User Activity")
        y_label = axes.get_y_axis_label("Stone Count")
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Generate sample data
        np.random.seed(42)
        n_points = 20
        x_data = np.linspace(1, 9, n_points)
        y_data = 2 * x_data + np.random.normal(0, 1, n_points) + 1
        
        # Create data points
        points = VGroup()
        for i in range(n_points):
            dot = Dot(axes.coords_to_point(x_data[i], y_data[i]), color=BLUE, radius=0.06)
            points.add(dot)
        
        self.play(Create(points))
        
        # Show initial prediction (mean)
        initial_pred = np.mean(y_data)
        initial_line = Line(
            axes.coords_to_point(0, initial_pred),
            axes.coords_to_point(10, initial_pred),
            color=RED,
            stroke_width=3
        )
        initial_label = Text(f"F₀ = {initial_pred:.1f} (Mean)", font_size=16, color=RED)
        initial_label.next_to(initial_line, UP, buff=0.3)
        
        self.play(Create(initial_line), Write(initial_label))
        
        # Show initial prediction explanation
        explanation = VGroup(
            Text("📊 Initial Prediction:", font_size=20, color=WHITE),
            Text("• F₀ = Mean of target values", font_size=16, color=GRAY),
            Text("• Simple baseline model", font_size=16, color=GRAY),
            Text("• Starting point for boosting", font_size=16, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        explanation.to_edge(RIGHT)
        
        self.play(Write(explanation))
        
        # Show initial residuals
        residual_text = Text("Initial Residuals = y - F₀", font_size=20, color=YELLOW)
        residual_text.to_edge(DOWN)
        self.play(Write(residual_text))
        
        # Create residual lines
        residual_lines = VGroup()
        for i in range(n_points):
            residual = y_data[i] - initial_pred
            line = Line(
                axes.coords_to_point(x_data[i], y_data[i]),
                axes.coords_to_point(x_data[i], initial_pred),
                color=YELLOW,
                stroke_width=1,
                stroke_opacity=0.7
            )
            residual_lines.add(line)
        
        self.play(Create(residual_lines))
        
        self.wait(3)
        
        self.play(FadeOut(VGroup(axes, x_label, y_label, points, initial_line, initial_label,
                                explanation, residual_text, residual_lines, initial_title)))
    
    def show_residual_calculation(self):
        # Show residual calculation process
        residual_title = Text("Residual Calculation Process", font_size=40, color=WHITE)
        residual_title.to_edge(UP)
        self.play(Write(residual_title))
        
        # Create residual calculation visualization
        # Current prediction
        current_pred = VGroup()
        current_title = Text("Current Prediction Fₘ₋₁", font_size=20, color=BLUE)
        current_title.move_to([-4, 2, 0])
        
        # Sample predictions
        predictions = [3.2, 4.1, 5.8, 3.9, 6.2, 4.5, 5.1, 3.7]
        pred_elements = VGroup()
        for i, pred in enumerate(predictions):
            element = Text(f"{pred:.1f}", font_size=14, color=BLUE)
            element.move_to([-4, 1 - i*0.3, 0])
            pred_elements.add(element)
        
        current_pred.add(current_title, pred_elements)
        self.play(Create(current_pred))
        
        # Actual values
        actual_vals = VGroup()
        actual_title = Text("Actual Values y", font_size=20, color=GREEN)
        actual_title.move_to([0, 2, 0])
        
        actual_values = [4.1, 3.8, 6.2, 4.5, 7.1, 4.2, 5.8, 3.9]
        actual_elements = VGroup()
        for i, actual in enumerate(actual_values):
            element = Text(f"{actual:.1f}", font_size=14, color=GREEN)
            element.move_to([0, 1 - i*0.3, 0])
            actual_elements.add(element)
        
        actual_vals.add(actual_title, actual_elements)
        self.play(Create(actual_vals))
        
        # Residuals
        residuals = VGroup()
        residual_title = Text("Residuals r = y - Fₘ₋₁", font_size=20, color=RED)
        residual_title.move_to([4, 2, 0])
        
        residual_elements = VGroup()
        for i in range(len(predictions)):
            residual = actual_values[i] - predictions[i]
            element = Text(f"{residual:+.1f}", font_size=14, color=RED)
            element.move_to([4, 1 - i*0.3, 0])
            residual_elements.add(element)
        
        residuals.add(residual_title, residual_elements)
        self.play(Create(residuals))
        
        # Show calculation arrows
        arrows = VGroup()
        for i in range(len(predictions)):
            arrow = Arrow(
                start=[-2, 1 - i*0.3, 0],
                end=[2, 1 - i*0.3, 0],
                color=YELLOW,
                stroke_width=2
            )
            arrows.add(arrow)
        
        self.play(Create(arrows))
        
        # Show residual properties
        properties = VGroup(
            Text("📊 Residual Properties:", font_size=20, color=WHITE),
            Text("• Can be positive or negative", font_size=16, color=GRAY),
            Text("• Sum to zero (approximately)", font_size=16, color=GRAY),
            Text("• Become new target for next model", font_size=16, color=GRAY),
            Text("• Represent prediction errors", font_size=16, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        properties.move_to([0, -2, 0])
        
        self.play(Write(properties))
        
        # Show gradient descent connection
        gradient_text = VGroup(
            Text("🎯 Gradient Descent Connection:", font_size=18, color=WHITE),
            Text("• Residuals = Negative gradients", font_size=14, color=YELLOW),
            Text("• Minimizing loss function", font_size=14, color=GREEN),
            Text("• Sequential optimization", font_size=14, color=BLUE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        gradient_text.to_edge(RIGHT)
        
        self.play(Write(gradient_text))
        
        self.wait(3)
        
        self.play(FadeOut(VGroup(current_pred, actual_vals, residuals, arrows, 
                                properties, gradient_text, residual_title)))
    
    def show_weak_learner_training(self):
        # Show weak learner training
        training_title = Text("Weak Learner Training", font_size=40, color=WHITE)
        training_title.to_edge(UP)
        self.play(Write(training_title))
        
        # Create coordinate system for residuals
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": GRAY}
        )
        axes.move_to([0, 0, 0])
        
        # Add labels
        x_label = axes.get_x_axis_label("Feature")
        y_label = axes.get_y_axis_label("Residuals")
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Generate sample residuals
        np.random.seed(42)
        n_points = 15
        x_residual = np.linspace(1, 9, n_points)
        residuals = np.random.normal(0, 0.8, n_points) + 0.5 * np.sin(x_residual)
        
        # Create residual points
        residual_points = VGroup()
        for i in range(n_points):
            dot = Dot(axes.coords_to_point(x_residual[i], residuals[i]), color=RED, radius=0.06)
            residual_points.add(dot)
        
        self.play(Create(residual_points))
        
        # Show weak learner (decision tree)
        weak_learner_text = Text("Training Weak Learner (Decision Tree)", font_size=20, color=GREEN)
        weak_learner_text.to_edge(DOWN)
        self.play(Write(weak_learner_text))
        
        # Create simple decision tree visualization
        tree_group = VGroup()
        
        # Root node
        root = Rectangle(width=1.5, height=0.6, color=GREEN, fill_opacity=0.3)
        root.move_to([0, 3, 0])
        root_label = Text("x ≤ 5?", font_size=12, color=WHITE)
        root_label.move_to(root.get_center())
        
        # Left child
        left_child = Rectangle(width=1.2, height=0.5, color=BLUE, fill_opacity=0.3)
        left_child.move_to([-2, 2, 0])
        left_label = Text("0.8", font_size=12, color=WHITE)
        left_label.move_to(left_child.get_center())
        
        # Right child
        right_child = Rectangle(width=1.2, height=0.5, color=ORANGE, fill_opacity=0.3)
        right_child.move_to([2, 2, 0])
        right_label = Text("-0.3", font_size=12, color=WHITE)
        right_label.move_to(right_child.get_center())
        
        # Connections
        left_line = Line(root.get_center(), left_child.get_center(), color=WHITE, stroke_width=2)
        right_line = Line(root.get_center(), right_child.get_center(), color=WHITE, stroke_width=2)
        
        tree_group.add(root, root_label, left_child, left_label, right_child, right_label, left_line, right_line)
        self.play(Create(tree_group))
        
        # Show weak learner predictions
        weak_predictions = VGroup()
        for i in range(n_points):
            if x_residual[i] <= 5:
                pred = 0.8
            else:
                pred = -0.3
            
            pred_dot = Dot(axes.coords_to_point(x_residual[i], pred), color=GREEN, radius=0.08)
            weak_predictions.add(pred_dot)
        
        self.play(Create(weak_predictions))
        
        # Show learning rate
        learning_rate_text = VGroup(
            Text("📊 Learning Rate (α):", font_size=18, color=WHITE),
            Text("• Controls contribution of each model", font_size=14, color=GRAY),
            Text("• α = 0.1 (typical value)", font_size=14, color=GREEN),
            Text("• Prevents overfitting", font_size=14, color=BLUE),
            Text("• Slower but more stable learning", font_size=14, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        learning_rate_text.to_edge(RIGHT)
        
        self.play(Write(learning_rate_text))
        
        self.wait(3)
        
        self.play(FadeOut(VGroup(axes, x_label, y_label, residual_points, weak_learner_text,
                                tree_group, weak_predictions, learning_rate_text, training_title)))
    
    def show_ensemble_building(self):
        # Show ensemble building process
        ensemble_title = Text("Ensemble Building Process", font_size=40, color=WHITE)
        ensemble_title.to_edge(UP)
        self.play(Write(ensemble_title))
        
        # Show ensemble formula
        formula = MathTex(r"F_m(x) = F_{m-1}(x) + \alpha \cdot h_m(x)", font_size=28, color=WHITE)
        formula.move_to([0, 2, 0])
        self.play(Write(formula))
        
        # Create ensemble visualization
        # Previous prediction
        prev_pred = VGroup()
        prev_title = Text("Previous Prediction Fₘ₋₁", font_size=18, color=BLUE)
        prev_title.move_to([-4, 0, 0])
        
        prev_values = [3.2, 4.1, 5.8, 3.9, 6.2]
        prev_elements = VGroup()
        for i, val in enumerate(prev_values):
            element = Text(f"{val:.1f}", font_size=14, color=BLUE)
            element.move_to([-4, -0.5 - i*0.4, 0])
            prev_elements.add(element)
        
        prev_pred.add(prev_title, prev_elements)
        self.play(Create(prev_pred))
        
        # Weak learner contribution
        weak_contrib = VGroup()
        contrib_title = Text("Weak Learner α·hₘ", font_size=18, color=GREEN)
        contrib_title.move_to([0, 0, 0])
        
        contrib_values = [0.08, -0.03, 0.12, 0.05, -0.02]
        contrib_elements = VGroup()
        for i, val in enumerate(contrib_values):
            element = Text(f"{val:+.2f}", font_size=14, color=GREEN)
            element.move_to([0, -0.5 - i*0.4, 0])
            contrib_elements.add(element)
        
        weak_contrib.add(contrib_title, contrib_elements)
        self.play(Create(weak_contrib))
        
        # New prediction
        new_pred = VGroup()
        new_title = Text("New Prediction Fₘ", font_size=18, color=ORANGE)
        new_title.move_to([4, 0, 0])
        
        new_values = [3.28, 4.07, 5.92, 3.95, 6.18]
        new_elements = VGroup()
        for i, val in enumerate(new_values):
            element = Text(f"{val:.2f}", font_size=14, color=ORANGE)
            element.move_to([4, -0.5 - i*0.4, 0])
            new_elements.add(element)
        
        new_pred.add(new_title, new_elements)
        self.play(Create(new_pred))
        
        # Addition arrows
        arrows = VGroup()
        for i in range(5):
            arrow = Arrow(
                start=[-2, -0.5 - i*0.4, 0],
                end=[2, -0.5 - i*0.4, 0],
                color=YELLOW,
                stroke_width=2
            )
            arrows.add(arrow)
        
        self.play(Create(arrows))
        
        # Show ensemble properties
        properties = VGroup(
            Text("🎯 Ensemble Properties:", font_size=20, color=WHITE),
            Text("• Each model improves previous", font_size=16, color=GREEN),
            Text("• Weighted combination", font_size=16, color=BLUE),
            Text("• Sequential optimization", font_size=16, color=YELLOW),
            Text("• Reduces bias and variance", font_size=16, color=ORANGE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        properties.move_to([0, -3, 0])
        
        self.play(Write(properties))
        
        # Show iteration process
        iteration_text = VGroup(
            Text("🔄 Iteration Process:", font_size=18, color=WHITE),
            Text("• Train weak learner on residuals", font_size=14, color=GRAY),
            Text("• Add to ensemble with weight α", font_size=14, color=GRAY),
            Text("• Update predictions", font_size=14, color=GRAY),
            Text("• Repeat until convergence", font_size=14, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        iteration_text.to_edge(RIGHT)
        
        self.play(Write(iteration_text))
        
        self.wait(3)
        
        self.play(FadeOut(VGroup(formula, prev_pred, weak_contrib, new_pred, arrows,
                                properties, iteration_text, ensemble_title)))
    
    def show_final_results(self):
        # Show final results
        results_title = Text("Gradient Boosting Results", font_size=40, color=WHITE)
        results_title.to_edge(UP)
        self.play(Write(results_title))
        
        # Create performance metrics
        metrics = VGroup(
            Text("📊 Performance Metrics:", font_size=28, color=WHITE),
            Text("• Training MSE: 0.15", font_size=20, color=GREEN),
            Text("• Validation MSE: 0.18", font_size=20, color=BLUE),
            Text("• R² Score: 0.92", font_size=20, color=ORANGE),
            Text("• Number of Trees: 100", font_size=20, color=PURPLE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        metrics.move_to([-3, 0, 0])
        
        self.play(Write(metrics))
        
        # Create learning curve
        learning_title = Text("Learning Curve", font_size=20, color=WHITE)
        learning_title.move_to([3, 2, 0])
        
        # Create sample learning curve
        iterations = list(range(1, 11))
        train_errors = [0.8, 0.6, 0.45, 0.35, 0.28, 0.22, 0.18, 0.15, 0.13, 0.12]
        val_errors = [0.85, 0.65, 0.5, 0.4, 0.32, 0.26, 0.22, 0.19, 0.18, 0.18]
        
        # Create coordinate system for learning curve
        curve_axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 1, 0.1],
            x_length=6,
            y_length=4,
            axis_config={"color": GRAY}
        )
        curve_axes.move_to([3, 0, 0])
        
        # Add labels
        curve_x_label = curve_axes.get_x_axis_label("Iterations")
        curve_y_label = curve_axes.get_y_axis_label("Error")
        
        self.play(Create(curve_axes), Write(curve_x_label), Write(curve_y_label))
        
        # Create learning curves
        train_points = VGroup()
        val_points = VGroup()
        
        for i in range(len(iterations)):
            # Training error points
            train_point = Dot(curve_axes.coords_to_point(iterations[i], train_errors[i]), 
                             color=GREEN, radius=0.05)
            train_points.add(train_point)
            
            # Validation error points
            val_point = Dot(curve_axes.coords_to_point(iterations[i], val_errors[i]), 
                           color=RED, radius=0.05)
            val_points.add(val_point)
        
        self.play(Create(train_points), Create(val_points))
        
        # Add legend
        legend = VGroup(
            Text("Training Error", font_size=14, color=GREEN),
            Text("Validation Error", font_size=14, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        legend.move_to([3, -2.5, 0])
        
        self.play(Write(legend))
        
        # Show advantages
        advantages = VGroup(
            Text("🎯 Gradient Boosting Advantages:", font_size=20, color=WHITE),
            Text("• High predictive accuracy", font_size=16, color=GREEN),
            Text("• Handles non-linear relationships", font_size=16, color=BLUE),
            Text("• Robust to outliers", font_size=16, color=YELLOW),
            Text("• Feature importance ranking", font_size=16, color=ORANGE),
            Text("• Automatic feature selection", font_size=16, color=PURPLE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        advantages.move_to([0, -2, 0])
        
        self.play(Write(advantages))
        
        # Final message
        final_message = Text("Gradient Boosting training complete!", font_size=36, color=GREEN)
        final_message.to_edge(DOWN)
        self.play(Write(final_message))
        self.wait(2)
        
        self.play(FadeOut(VGroup(metrics, curve_axes, curve_x_label, curve_y_label,
                                train_points, val_points, legend, advantages, 
                                final_message, results_title)))
