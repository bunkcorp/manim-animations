#!/usr/bin/env python3
"""
Boosting Hyperparameters Animation
Visual demonstration of eta (learning rate) and nrounds effects in boosting
"""

from manim import *
import numpy as np

class BoostingHyperparametersAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Show boosting overview
        self.show_boosting_overview()
        
        # Demonstrate eta effects
        self.show_eta_effects()
        
        # Show nrounds impact
        self.show_nrounds_impact()
        
        # Display hyperparameter interaction
        self.show_hyperparameter_interaction()
        
        # Show practical guidelines
        self.show_practical_guidelines()
    
    def show_boosting_overview(self):
        """Introduce boosting concept with sequential tree building"""
        title = Text("Boosting Hyperparameters: η (eta) & nrounds", 
                    font_size=32, color=YELLOW, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Show initial weak learner
        concept_text = Text("Sequential Tree Building", 
                          font_size=24, color=WHITE, weight=BOLD)
        concept_text.move_to(UP*2)
        self.play(Write(concept_text))
        
        # Create simple data visualization
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 6, 2],
            x_length=8,
            y_length=4,
            axis_config={"stroke_color": WHITE, "stroke_width": 2}
        ).move_to(DOWN*0.5)
        
        # Generate synthetic data points
        np.random.seed(42)
        x_data = np.random.uniform(1, 9, 20)
        y_data = 2 + 0.5*x_data + np.random.normal(0, 0.8, 20)
        
        # Plot data points
        data_points = VGroup()
        for x, y in zip(x_data, y_data):
            point = Dot(axes.coords_to_point(x, y), color=BLUE, radius=0.06)
            data_points.add(point)
        
        self.play(Create(axes))
        self.play(*[FadeIn(point, scale=0.5) for point in data_points])
        
        # Show weak learner (decision stump)
        stump_line = Line(
            axes.coords_to_point(1, 3),
            axes.coords_to_point(9, 3),
            color=RED, stroke_width=3
        )
        
        weak_learner_text = Text("Tree₁: Weak Learner", font_size=16, color=RED, weight=BOLD)
        weak_learner_text.next_to(stump_line, UP, buff=0.2)
        
        self.play(Create(stump_line), Write(weak_learner_text))
        
        # Show residuals as error bars
        residual_arrows = VGroup()
        for x, y in zip(x_data[:8], y_data[:8]):  # Show subset for clarity
            predicted_y = 3  # Constant prediction from stump
            if y != predicted_y:
                arrow = Arrow(
                    axes.coords_to_point(x, predicted_y),
                    axes.coords_to_point(x, y),
                    color=RED, stroke_width=2,
                    max_tip_length_to_length_ratio=0.3
                )
                residual_arrows.add(arrow)
        
        residual_text = Text("Residuals (Errors)", font_size=14, color=RED, weight=BOLD)
        residual_text.move_to(RIGHT*4 + UP*1)
        
        self.play(Create(residual_arrows), Write(residual_text))
        
        # Show sequential addition
        tree2_line = Line(
            axes.coords_to_point(1, 2.5),
            axes.coords_to_point(5, 3.5),
            color=ORANGE, stroke_width=3
        )
        tree2_line.add(Line(
            axes.coords_to_point(5, 3.5),
            axes.coords_to_point(9, 2.5),
            color=ORANGE, stroke_width=3
        ))
        
        tree2_text = Text("+ Tree₂", font_size=16, color=ORANGE, weight=BOLD)
        tree2_text.next_to(weak_learner_text, RIGHT, buff=0.5)
        
        self.play(Create(tree2_line), Write(tree2_text))
        
        # Final ensemble line (more complex)
        final_points = []
        for x in np.linspace(1, 9, 50):
            # Simulate ensemble prediction
            y_pred = 2.8 + 0.4*x + 0.3*np.sin(x) + 0.1*np.random.normal()
            final_points.append(axes.coords_to_point(x, y_pred))
        
        ensemble_curve = VMobject()
        ensemble_curve.set_points_smoothly(final_points)
        ensemble_curve.set_stroke(GREEN, width=4)
        
        tree3_text = Text("+ Tree₃ + ...", font_size=16, color=GREEN, weight=BOLD)
        tree3_text.next_to(tree2_text, RIGHT, buff=0.5)
        
        self.play(Create(ensemble_curve), Write(tree3_text))
        
        # Show boosting formula
        formula = Text("Final = η×Tree₁ + η×Tree₂ + η×Tree₃ + ...", 
                      font_size=18, color=YELLOW, weight=BOLD)
        formula.move_to(DOWN*3)
        
        learning_text = Text("Each tree learns from previous mistakes", 
                           font_size=16, color=WHITE)
        learning_text.next_to(formula, DOWN, buff=0.3)
        
        self.play(Write(formula), Write(learning_text))
        
        self.wait(2)
        
        # Store elements
        self.overview_elements = VGroup(
            axes, data_points, stump_line, weak_learner_text, 
            residual_arrows, residual_text, tree2_line, tree2_text,
            ensemble_curve, tree3_text, formula, learning_text, concept_text
        )
        self.title = title
    
    def show_eta_effects(self):
        """Demonstrate eta (learning rate) effects with visual examples"""
        eta_title = Text("η (Learning Rate) Effects", 
                        font_size=28, color=BLUE, weight=BOLD)
        eta_title.to_edge(UP, buff=0.5)
        self.play(ReplacementTransform(self.title, eta_title))
        
        # Clear previous elements
        self.play(FadeOut(self.overview_elements))
        
        # Create three parallel scenarios
        panel_width = 3.5
        panel_positions = [LEFT*4, ORIGIN, RIGHT*4]
        eta_values = [1.0, 0.3, 0.1]
        eta_labels = ["High η = 1.0\nAggressive", "Medium η = 0.3\nModerate", "Low η = 0.1\nConservative"]
        panel_colors = [RED, ORANGE, GREEN]
        
        panels = []
        for i, (pos, eta, label, color) in enumerate(zip(panel_positions, eta_values, eta_labels, panel_colors)):
            # Panel background
            panel_box = Rectangle(
                width=panel_width, height=5,
                fill_color=BLACK, fill_opacity=0.8,
                stroke_color=color, stroke_width=2
            ).move_to(pos + DOWN*0.3)
            
            # Panel title
            panel_title = Text(label, font_size=14, color=color, weight=BOLD)
            panel_title.move_to(pos + UP*2.3)
            
            # Mini axes for each panel
            mini_axes = Axes(
                x_range=[0, 20, 5],
                y_range=[0, 5, 1],
                x_length=2.8,
                y_length=2.5,
                axis_config={"stroke_color": WHITE, "stroke_width": 1}
            ).move_to(pos + UP*0.2)
            
            panels.append((panel_box, panel_title, mini_axes, pos, color, eta))
            
            self.play(Create(panel_box), Write(panel_title), Create(mini_axes))
        
        # Show learning curves for each eta
        iterations = np.arange(0, 20, 0.5)
        
        for panel_box, panel_title, mini_axes, pos, color, eta in panels:
            # Generate learning curves based on eta
            if eta == 1.0:  # High eta - rapid then oscillating
                train_error = 4 * np.exp(-iterations * 0.3) + 0.5 * np.sin(iterations * 0.8) + 0.2
                val_error = 4 * np.exp(-iterations * 0.25) + 0.8 * np.sin(iterations * 0.8) + 0.5
            elif eta == 0.3:  # Medium eta - steady improvement
                train_error = 4 * np.exp(-iterations * 0.2) + 0.1
                val_error = 4 * np.exp(-iterations * 0.18) + 0.3
            else:  # Low eta - slow but smooth
                train_error = 4 * np.exp(-iterations * 0.1) + 0.05
                val_error = 4 * np.exp(-iterations * 0.09) + 0.15
            
            # Create curves
            train_points = [mini_axes.coords_to_point(i, e) for i, e in zip(iterations, train_error)]
            val_points = [mini_axes.coords_to_point(i, e) for i, e in zip(iterations, val_error)]
            
            train_curve = VMobject()
            train_curve.set_points_smoothly(train_points)
            train_curve.set_stroke(BLUE, width=2)
            
            val_curve = VMobject()
            val_curve.set_points_smoothly(val_points)
            val_curve.set_stroke(color, width=2)
            
            # Animate curve drawing
            self.play(Create(train_curve), Create(val_curve), run_time=1.5)
            
            # Add labels
            train_label = Text("Train", font_size=10, color=BLUE)
            train_label.move_to(pos + DOWN*1.2 + LEFT*0.8)
            
            val_label = Text("Valid", font_size=10, color=color)
            val_label.move_to(pos + DOWN*1.2 + RIGHT*0.8)
            
            self.play(Write(train_label), Write(val_label))
        
        # Add behavioral annotations
        high_eta_warning = Text("Oscillation!", font_size=12, color=RED, weight=BOLD)
        high_eta_warning.move_to(LEFT*4 + DOWN*2.5)
        
        medium_eta_good = Text("Stable!", font_size=12, color=ORANGE, weight=BOLD)
        medium_eta_good.move_to(ORIGIN + DOWN*2.5)
        
        low_eta_slow = Text("Too Slow!", font_size=12, color=GREEN, weight=BOLD)
        low_eta_slow.move_to(RIGHT*4 + DOWN*2.5)
        
        self.play(Write(high_eta_warning), Write(medium_eta_good), Write(low_eta_slow))
        
        # Key insight
        insight = Text("η controls step size in function space", 
                      font_size=18, color=YELLOW, weight=BOLD)
        insight.move_to(DOWN*3.5)
        self.play(Write(insight))
        
        self.wait(3)
        
        # Store elements
        self.eta_elements = VGroup(*[elem for panel in panels for elem in panel[:3]], 
                                 high_eta_warning, medium_eta_good, low_eta_slow, insight)
        self.eta_title = eta_title
    
    def show_nrounds_impact(self):
        """Show nrounds (number of rounds) impact on model performance"""
        nrounds_title = Text("nrounds (Number of Rounds) Impact", 
                           font_size=28, color=PURPLE, weight=BOLD)
        nrounds_title.to_edge(UP, buff=0.5)
        self.play(ReplacementTransform(self.eta_title, nrounds_title))
        
        # Clear previous elements
        self.play(FadeOut(self.eta_elements))
        
        # Fix eta = 0.3, show progression of nrounds
        fixed_eta_text = Text("Fixed: η = 0.3", font_size=20, color=WHITE, weight=BOLD)
        fixed_eta_text.move_to(UP*2.5)
        self.play(Write(fixed_eta_text))
        
        # Create main learning curve plot
        axes = Axes(
            x_range=[0, 500, 100],
            y_range=[0, 4, 1],
            x_length=10,
            y_length=5,
            axis_config={"stroke_color": WHITE, "stroke_width": 2}
        ).move_to(DOWN*0.5)
        
        x_label = Text("Number of Rounds", font_size=16, color=WHITE)
        x_label.next_to(axes.x_axis, DOWN, buff=0.3)
        
        y_label = Text("Error", font_size=16, color=WHITE)
        y_label.next_to(axes.y_axis, LEFT, buff=0.3)
        y_label.rotate(PI/2)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Generate overfitting curves
        rounds = np.arange(0, 500, 10)
        train_error = 3.5 * np.exp(-rounds * 0.01) + 0.1  # Keeps decreasing
        val_error = 3.5 * np.exp(-rounds * 0.008) + 0.002 * rounds + 0.2  # U-shape
        
        # Create curves progressively
        train_points = [axes.coords_to_point(r, e) for r, e in zip(rounds, train_error)]
        val_points = [axes.coords_to_point(r, e) for r, e in zip(rounds, val_error)]
        
        train_curve = VMobject()
        train_curve.set_points_smoothly(train_points)
        train_curve.set_stroke(BLUE, width=4)
        
        val_curve = VMobject()
        val_curve.set_points_smoothly(val_points)
        val_curve.set_stroke(RED, width=4)
        
        # Animate curves appearing
        self.play(Create(train_curve), run_time=2)
        self.play(Create(val_curve), run_time=2)
        
        # Add curve labels
        train_label = Text("Training Error", font_size=14, color=BLUE, weight=BOLD)
        train_label.move_to(axes.coords_to_point(400, 0.5))
        
        val_label = Text("Validation Error", font_size=14, color=RED, weight=BOLD)
        val_label.move_to(axes.coords_to_point(350, 2.5))
        
        self.play(Write(train_label), Write(val_label))
        
        # Show optimal stopping point
        optimal_round = 150
        optimal_error = 3.5 * np.exp(-optimal_round * 0.008) + 0.002 * optimal_round + 0.2
        
        optimal_dot = Dot(axes.coords_to_point(optimal_round, optimal_error), 
                         color=GREEN, radius=0.1)
        
        optimal_line = DashedLine(
            axes.coords_to_point(optimal_round, 0),
            axes.coords_to_point(optimal_round, 4),
            color=GREEN, stroke_width=3
        )
        
        optimal_text = Text("Optimal\nStopping", font_size=14, color=GREEN, weight=BOLD)
        optimal_text.move_to(axes.coords_to_point(optimal_round, 3.5))
        
        self.play(Create(optimal_dot), Create(optimal_line), Write(optimal_text))
        
        # Show overfitting region
        overfitting_box = Rectangle(
            width=3, height=1.5,
            fill_color=RED, fill_opacity=0.2,
            stroke_color=RED, stroke_width=2
        ).move_to(axes.coords_to_point(400, 3))
        
        overfitting_text = Text("Overfitting\nRegion", font_size=14, color=RED, weight=BOLD)
        overfitting_text.move_to(axes.coords_to_point(400, 3))
        
        self.play(Create(overfitting_box), Write(overfitting_text))
        
        # Show early stopping concept
        early_stopping_arrow = CurvedArrow(
            axes.coords_to_point(250, 3.5),
            axes.coords_to_point(optimal_round + 20, optimal_error + 0.3),
            angle=-PI/3, color=YELLOW
        )
        
        early_stopping_text = Text("Early Stopping", font_size=16, color=YELLOW, weight=BOLD)
        early_stopping_text.move_to(axes.coords_to_point(280, 3.7))
        
        self.play(GrowArrow(early_stopping_arrow), Write(early_stopping_text))
        
        self.wait(2)
        
        # Store elements
        self.nrounds_elements = VGroup(
            fixed_eta_text, axes, x_label, y_label, train_curve, val_curve,
            train_label, val_label, optimal_dot, optimal_line, optimal_text,
            overfitting_box, overfitting_text, early_stopping_arrow, early_stopping_text
        )
        self.nrounds_title = nrounds_title
    
    def show_hyperparameter_interaction(self):
        """Display hyperparameter interaction heatmap"""
        interaction_title = Text("Hyperparameter Interaction", 
                                font_size=28, color=GREEN, weight=BOLD)
        interaction_title.to_edge(UP, buff=0.5)
        self.play(ReplacementTransform(self.nrounds_title, interaction_title))
        
        # Clear previous elements
        self.play(FadeOut(self.nrounds_elements))
        
        # Create 2D heatmap representation
        heatmap_title = Text("Validation Error Heatmap", font_size=20, color=WHITE, weight=BOLD)
        heatmap_title.move_to(UP*2.5)
        self.play(Write(heatmap_title))
        
        # Create simplified grid for heatmap
        grid_size = 4
        cell_size = 1.2
        
        # Create simplified heatmap grid
        heatmap_grid = VGroup()
        
        # Predefined colors for simplicity
        colors = [
            [RED, RED, ORANGE, YELLOW],      # High eta
            [RED, ORANGE, YELLOW, GREEN],    # Med-high eta  
            [ORANGE, YELLOW, GREEN, BLUE],   # Med-low eta
            [YELLOW, GREEN, BLUE, BLUE]      # Low eta
        ]
        
        for i in range(grid_size):
            for j in range(grid_size):
                cell = Square(
                    side_length=cell_size,
                    fill_color=colors[i][j], fill_opacity=0.7,
                    stroke_color=WHITE, stroke_width=1
                )
                
                x_pos = (j - grid_size/2 + 0.5) * cell_size
                y_pos = (i - grid_size/2 + 0.5) * cell_size + 0.5
                cell.move_to([x_pos, y_pos, 0])
                
                heatmap_grid.add(cell)
        
        self.play(*[FadeIn(cell, scale=0.8) for cell in heatmap_grid], run_time=1.5)
        
        # Add axes labels
        eta_axis_label = Text("η (eta)", font_size=16, color=WHITE, weight=BOLD)
        eta_axis_label.move_to(LEFT*3.5)
        eta_axis_label.rotate(PI/2)
        
        nrounds_axis_label = Text("nrounds", font_size=16, color=WHITE, weight=BOLD)
        nrounds_axis_label.move_to(DOWN*2.5)
        
        self.play(Write(eta_axis_label), Write(nrounds_axis_label))
        
        # Add value labels
        low_eta_label = Text("0.01", font_size=12, color=WHITE)
        low_eta_label.move_to(LEFT*4 + DOWN*2)
        
        high_eta_label = Text("1.0", font_size=12, color=WHITE)
        high_eta_label.move_to(LEFT*4 + UP*2)
        
        low_rounds_label = Text("50", font_size=12, color=WHITE)
        low_rounds_label.move_to(LEFT*2.5 + DOWN*3)
        
        high_rounds_label = Text("500", font_size=12, color=WHITE)
        high_rounds_label.move_to(RIGHT*2.5 + DOWN*3)
        
        self.play(Write(low_eta_label), Write(high_eta_label), 
                 Write(low_rounds_label), Write(high_rounds_label))
        
        # Highlight optimal region
        optimal_region = Rectangle(
            width=2.4, height=1.6,
            fill_color=TRANSPARENT, fill_opacity=0,
            stroke_color=YELLOW, stroke_width=4
        ).move_to([1.2, -1.2, 0])
        
        optimal_text = Text("Optimal Region:\nLow η + High nrounds", 
                          font_size=14, color=YELLOW, weight=BOLD)
        optimal_text.move_to(RIGHT*4 + UP*1)
        
        self.play(Create(optimal_region), Write(optimal_text))
        
        # Show specific combinations
        combinations = [
            ([1.2, -1.2, 0], "η=0.01, rounds=1000\nSlow but stable", GREEN),
            ([-1.2, 1.2, 0], "η=0.5, rounds=50\nFast but risky", RED),
            ([0.0, 0.0, 0], "η=0.1, rounds=300\nGood balance", BLUE)
        ]
        
        for pos, text, color in combinations:
            dot = Dot(pos, color=color, radius=0.08)
            label = Text(text, font_size=10, color=color, weight=BOLD)
            label.next_to(dot, RIGHT, buff=0.2)
            
            self.play(FadeIn(dot, scale=2), Write(label))
        
        self.wait(2)
        
        # Store elements
        self.interaction_elements = VGroup(
            heatmap_title, heatmap_grid, eta_axis_label, nrounds_axis_label,
            low_eta_label, high_eta_label, low_rounds_label, high_rounds_label,
            optimal_region, optimal_text
        )
        self.interaction_title = interaction_title
    
    def show_practical_guidelines(self):
        """Show practical guidelines summary"""
        guidelines_title = Text("Practical Guidelines", 
                              font_size=32, color=YELLOW, weight=BOLD)
        guidelines_title.to_edge(UP)
        self.play(ReplacementTransform(self.interaction_title, guidelines_title))
        
        # Clear previous elements
        self.play(FadeOut(self.interaction_elements))
        
        # Rule of thumb boxes
        eta_box = Rectangle(
            width=8, height=1.5,
            fill_color=BLUE, fill_opacity=0.2,
            stroke_color=BLUE, stroke_width=2
        ).move_to(UP*1.5)
        
        eta_rule = VGroup(
            Text("η (Learning Rate):", font_size=18, color=BLUE, weight=BOLD),
            Text("Use small values (0.01 - 0.3)", font_size=16, color=WHITE),
            Text("Smaller η = More stable learning", font_size=14, color=GRAY)
        ).arrange(DOWN, buff=0.1)
        eta_rule.move_to(eta_box.get_center())
        
        nrounds_box = Rectangle(
            width=8, height=1.5,
            fill_color=PURPLE, fill_opacity=0.2,
            stroke_color=PURPLE, stroke_width=2
        ).move_to(ORIGIN)
        
        nrounds_rule = VGroup(
            Text("nrounds:", font_size=18, color=PURPLE, weight=BOLD),
            Text("Use large values (100 - 1000+)", font_size=16, color=WHITE),
            Text("More rounds compensates for smaller η", font_size=14, color=GRAY)
        ).arrange(DOWN, buff=0.1)
        nrounds_rule.move_to(nrounds_box.get_center())
        
        self.play(Create(eta_box), Write(eta_rule))
        self.play(Create(nrounds_box), Write(nrounds_rule))
        
        # Key insight
        key_insight = Text("Key Insight: Small η + Many rounds = Better Generalization", 
                          font_size=20, color=YELLOW, weight=BOLD)
        key_insight.move_to(DOWN*2)
        
        # Warning
        warning = Text("⚠️ High η + High rounds = Guaranteed Overfitting!", 
                      font_size=16, color=RED, weight=BOLD)
        warning.move_to(DOWN*2.8)
        
        self.play(Write(key_insight))
        self.play(Write(warning))
        
        # Mathematical formula
        formula = Text("f(x) = Σᵢ₌₁ᵀ η × hᵢ(x)", 
                      font_size=18, color=WHITE)
        formula.move_to(DOWN*3.8)
        
        formula_explanation = Text("T = nrounds, η = learning rate, hᵢ = tree i", 
                                 font_size=12, color=GRAY)
        formula_explanation.next_to(formula, DOWN, buff=0.2)
        
        self.play(Write(formula), Write(formula_explanation))
        
        # Final recommendations
        recommendations = VGroup(
            Text("Recommendations:", font_size=16, color=GREEN, weight=BOLD),
            Text("• Start with η = 0.1, nrounds = 100", font_size=14, color=WHITE),
            Text("• Use early stopping with validation set", font_size=14, color=WHITE),
            Text("• Lower η if overfitting, increase nrounds", font_size=14, color=WHITE),
            Text("• Cross-validation for optimal hyperparameters", font_size=14, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        
        recommendations.move_to(RIGHT*4 + DOWN*1)
        
        for rec in recommendations:
            self.play(Write(rec), run_time=0.8)
        
        self.wait(3)

if __name__ == "__main__":
    # For testing
    pass