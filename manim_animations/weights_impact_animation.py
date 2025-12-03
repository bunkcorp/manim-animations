#!/usr/bin/env python3
"""
Weights Impact on Model Metrics Animation
Shows how weights affect AIC vs AUC differently
"""

from manim import *
import numpy as np

class WeightsImpactAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Show title card
        self.show_title()
        
        # Show basic concepts
        self.show_basic_concepts()
        
        # Show log-likelihood and AIC relationship
        self.show_aic_relationship()
        
        # Demonstrate weight effects on AIC
        self.show_aic_weight_effects()
        
        # Show AUC robustness
        self.show_auc_robustness()
        
        # Compare sensitivities
        self.show_sensitivity_comparison()
        
        # Show summary
        self.show_summary()
    
    def show_title(self):
        """Title card"""
        title = Text("Weights Impact on Model Metrics", font_size=36, color=YELLOW, weight=BOLD)
        subtitle = Text("AIC vs AUC Sensitivity", font_size=28, color=WHITE)
        concept = Text("How weighting schemes affect different evaluation metrics", 
                      font_size=20, color=LIGHT_GRAY, slant=ITALIC)
        
        title_group = VGroup(title, subtitle, concept).arrange(DOWN, buff=0.4)
        
        self.play(Write(title))
        self.play(Write(subtitle))
        self.play(Write(concept))
        self.wait(2)
        self.play(FadeOut(title_group))
    
    def show_basic_concepts(self):
        """Explain weighting and metrics"""
        title = Text("Sample Weights in Machine Learning", font_size=32, color=BLUE, weight=BOLD).to_edge(UP)
        self.play(Write(title))
        
        # Key concepts
        concepts = VGroup(
            Text("🎯 Sample weights: Assign different importance to data points", font_size=22, color=WHITE),
            Text("📊 Higher weight = more influence on model training", font_size=22, color=WHITE),
            Text("⚖️ Used for: imbalanced data, importance weighting, cost-sensitive learning", font_size=22, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to(UP*0.5)
        
        for concept in concepts:
            self.play(FadeIn(concept, shift=UP))
            self.wait(1)
        
        # Show example data points with weights
        data_title = Text("Example: Weighted Data Points", font_size=20, color=ORANGE, weight=BOLD)
        data_title.next_to(concepts, DOWN, buff=0.8)
        
        # Create visual representation of weighted points
        points_group = VGroup()
        weights_demo = [1.0, 0.5, 2.0, 0.1, 1.5]
        colors_demo = [RED, RED, BLUE, BLUE, RED]
        labels = ["Point 1", "Point 2", "Point 3", "Point 4", "Point 5"]
        
        for i, (weight, color, label) in enumerate(zip(weights_demo, colors_demo, labels)):
            # Create circle with size proportional to weight
            circle = Circle(radius=0.2 + 0.3*weight, color=color, fill_opacity=0.3)
            circle.move_to(LEFT*4 + RIGHT*i*2 + DOWN*2)
            
            # Add weight label
            weight_text = Text(f"w={weight}", font_size=14, color=WHITE)
            weight_text.next_to(circle, DOWN, buff=0.1)
            
            point_group = VGroup(circle, weight_text)
            points_group.add(point_group)
        
        self.play(Write(data_title))
        for point_group in points_group:
            self.play(FadeIn(point_group))
            self.wait(0.3)
        
        # Add legend
        legend = VGroup(
            Text("Circle size ∝ weight", font_size=16, color=WHITE),
            VGroup(
                Circle(radius=0.1, color=RED, fill_opacity=0.3),
                Text("Class A", font_size=14, color=WHITE)
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Circle(radius=0.1, color=BLUE, fill_opacity=0.3),
                Text("Class B", font_size=14, color=WHITE)
            ).arrange(RIGHT, buff=0.2)
        ).arrange(DOWN, buff=0.2).to_corner(UR)
        
        self.play(FadeIn(legend))
        self.wait(2)
        self.play(FadeOut(concepts, data_title, points_group, legend))
        self.title = title
    
    def show_aic_relationship(self):
        """Show AIC and log-likelihood relationship"""
        aic_title = Text("AIC and Log-Likelihood Relationship", font_size=28, color=GREEN, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.title, aic_title))
        
        # Show AIC formula
        formula_card = RoundedRectangle(
            corner_radius=0.2, width=10, height=3,
            stroke_color=WHITE, stroke_width=2,
            fill_color=BLACK, fill_opacity=0.9
        ).move_to(UP*1)
        
        formula_content = VGroup(
            Text("AIC Formula:", font_size=24, color=YELLOW, weight=BOLD),
            Text("AIC = -2 × log-likelihood + 2p", font_size=20, color=WHITE),
            Text("where p = number of parameters", font_size=16, color=LIGHT_GRAY, slant=ITALIC)
        ).arrange(DOWN, buff=0.3).move_to(formula_card.get_center())
        
        self.play(FadeIn(formula_card), Write(formula_content))
        
        # Show how weights affect log-likelihood
        weight_effects = VGroup(
            Text("How Weights Affect Log-Likelihood:", font_size=20, color=ORANGE, weight=BOLD),
            VGroup(
                Text("• Weighted log-likelihood = Σ wᵢ × log(P(yᵢ|xᵢ))", font_size=18, color=WHITE),
                Text("• Higher weights amplify contribution of those points", font_size=18, color=WHITE),
                Text("• Noisy points with high weights can hurt log-likelihood", font_size=18, color=WHITE),
                Text("• This directly impacts AIC calculation", font_size=18, color=WHITE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        ).arrange(DOWN, buff=0.4).next_to(formula_card, DOWN, buff=0.8)
        
        for item in weight_effects:
            self.play(Write(item))
            self.wait(1)
        
        self.wait(2)
        self.play(FadeOut(formula_card, formula_content, weight_effects))
        self.aic_title = aic_title
    
    def show_aic_weight_effects(self):
        """Demonstrate weight effects on AIC"""
        effects_title = Text("Weight Effects on AIC", font_size=28, color=PURPLE, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.aic_title, effects_title))
        
        # Create scenarios
        scenarios = [
            ("Equal Weights", [1, 1, 1, 1, 1], BLUE),
            ("Amplify Good Data", [2, 2, 0.5, 0.5, 0.5], GREEN),
            ("Amplify Noise", [0.5, 0.5, 2, 2, 2], RED)
        ]
        
        scenario_results = VGroup()
        
        for i, (scenario_name, weights, color) in enumerate(scenarios):
            # Create scenario visualization
            scenario_group = VGroup()
            
            # Title
            scenario_title = Text(scenario_name, font_size=18, color=color, weight=BOLD)
            scenario_title.move_to(LEFT*4 + RIGHT*i*4 + UP*2)
            
            # Weight bars
            bars = VGroup()
            for j, weight in enumerate(weights):
                bar = Rectangle(
                    width=0.3,
                    height=weight * 0.8,
                    fill_color=color,
                    fill_opacity=0.7,
                    stroke_color=WHITE
                ).move_to(LEFT*4 + RIGHT*i*4 + LEFT*1 + RIGHT*j*0.5 + UP*0.5)
                bars.add(bar)
            
            # Simulated AIC values (lower is better)
            if i == 0:  # Equal weights - baseline
                aic_value = 150.2
            elif i == 1:  # Amplify good data - better AIC
                aic_value = 142.8
            else:  # Amplify noise - worse AIC
                aic_value = 168.5
            
            aic_text = Text(f"AIC = {aic_value:.1f}", font_size=16, color=color, weight=BOLD)
            aic_text.next_to(bars, DOWN, buff=0.3)
            
            scenario_group = VGroup(scenario_title, bars, aic_text)
            scenario_results.add(scenario_group)
        
        # Show scenarios sequentially
        for scenario in scenario_results:
            self.play(FadeIn(scenario))
            self.wait(1)
        
        # Add explanation
        explanation = VGroup(
            Text("Key Insights:", font_size=20, color=YELLOW, weight=BOLD),
            VGroup(
                Text("✓ Weighting informative data improves AIC (lower values)", font_size=16, color=GREEN),
                Text("✗ Weighting noisy data worsens AIC (higher values)", font_size=16, color=RED),
                Text("⚠️ AIC is sensitive to weight distribution", font_size=16, color=ORANGE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        ).arrange(DOWN, buff=0.4).next_to(scenario_results, DOWN, buff=0.8)
        
        for item in explanation:
            self.play(Write(item))
            self.wait(1)
        
        self.wait(2)
        self.play(FadeOut(scenario_results, explanation))
        self.effects_title = effects_title
    
    def show_auc_robustness(self):
        """Show AUC robustness to weights"""
        auc_title = Text("AUC Robustness to Weights", font_size=28, color=ORANGE, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.effects_title, auc_title))
        
        # Explain AUC concept
        auc_concept = VGroup(
            Text("AUC (Area Under ROC Curve):", font_size=22, color=YELLOW, weight=BOLD),
            VGroup(
                Text("• Measures ability to distinguish between classes", font_size=18, color=WHITE),
                Text("• Based on ranking/ordering of predictions", font_size=18, color=WHITE),
                Text("• Less sensitive to individual point weights", font_size=18, color=WHITE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        ).arrange(DOWN, buff=0.4).move_to(UP*1.5)
        
        for item in auc_concept:
            self.play(Write(item))
            self.wait(1)
        
        # Create ROC curves for different weighting schemes
        axes = Axes(
            x_range=[0, 1, 0.2],
            y_range=[0, 1, 0.2],
            x_length=6,
            y_length=6,
            axis_config={"stroke_color": WHITE, "stroke_width": 2}
        ).move_to(DOWN*0.5)
        
        x_label = Text("False Positive Rate", font_size=16, color=WHITE).next_to(axes, DOWN)
        y_label = Text("True Positive Rate", font_size=16, color=WHITE).next_to(axes, LEFT).rotate(PI/2)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Create ROC curves (simulated)
        fpr = np.linspace(0, 1, 20)
        
        # All curves are very similar despite different weighting
        curves_data = [
            ("Equal Weights", 0.82, BLUE),
            ("Amplify Good", 0.83, GREEN), 
            ("Amplify Noise", 0.81, RED)
        ]
        
        curves = VGroup()
        legend_items = VGroup()
        
        for i, (name, auc_val, color) in enumerate(curves_data):
            # Generate slightly different but similar curves
            tpr = fpr**(0.7 + 0.1*np.sin(i)) + 0.1*np.random.normal(0, 0.02, len(fpr))
            tpr = np.clip(tpr, fpr, 1)  # Ensure TPR >= FPR for valid ROC
            
            points = [axes.coords_to_point(x, y) for x, y in zip(fpr, tpr)]
            curve = VMobject(color=color, stroke_width=3)
            curve.set_points_smoothly(points)
            curves.add(curve)
            
            # Legend
            legend_item = VGroup(
                Line(ORIGIN, RIGHT*0.5, color=color, stroke_width=3),
                Text(f"{name}: AUC = {auc_val:.2f}", font_size=14, color=WHITE)
            ).arrange(RIGHT, buff=0.2)
            legend_items.add(legend_item)
        
        # Position legend
        legend_items.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(axes, RIGHT, buff=0.5)
        
        # Draw diagonal reference line
        diagonal = Line(
            axes.coords_to_point(0, 0),
            axes.coords_to_point(1, 1),
            color=GRAY,
            stroke_width=2,
            stroke_opacity=0.5
        )
        
        self.play(Create(diagonal))
        
        # Show curves
        for curve, legend_item in zip(curves, legend_items):
            self.play(Create(curve), Write(legend_item))
            self.wait(0.8)
        
        # Add insight
        insight = Text("AUC values remain similar despite different weighting!", 
                      font_size=18, color=YELLOW, weight=BOLD)
        insight.next_to(axes, DOWN, buff=1)
        
        self.play(Write(insight))
        self.wait(2)
        
        self.play(FadeOut(auc_concept, axes, x_label, y_label, curves, legend_items, diagonal, insight))
        self.auc_title = auc_title
    
    def show_sensitivity_comparison(self):
        """Compare metric sensitivities side by side"""
        comparison_title = Text("Metric Sensitivity Comparison", font_size=28, color=TEAL, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.auc_title, comparison_title))
        
        # Create comparison table
        table_data = [
            ["Metric", "Weight Sensitivity", "Why?"],
            ["AIC", "HIGH", "Direct impact on log-likelihood"],
            ["AUC", "LOW", "Based on ranking, not absolute values"],
            ["Accuracy", "MEDIUM", "Depends on weight distribution"],
            ["Log-Loss", "HIGH", "Directly weighted in calculation"],
            ["F1-Score", "MEDIUM", "Threshold-dependent effects"]
        ]
        
        # Create table
        table = VGroup()
        colors = [YELLOW, RED, BLUE, ORANGE, RED, ORANGE]  # Header + data rows
        
        for i, (row, color) in enumerate(zip(table_data, colors)):
            row_group = VGroup()
            for j, cell in enumerate(row):
                if i == 0:  # Header
                    cell_text = Text(cell, font_size=18, color=YELLOW, weight=BOLD)
                else:
                    if j == 1:  # Sensitivity column
                        if cell == "HIGH":
                            cell_color = RED
                        elif cell == "MEDIUM":
                            cell_color = ORANGE
                        else:  # LOW
                            cell_color = GREEN
                        cell_text = Text(cell, font_size=16, color=cell_color, weight=BOLD)
                    else:
                        cell_text = Text(cell, font_size=16, color=WHITE)
                
                # Position cells
                cell_text.move_to(LEFT*4 + RIGHT*j*3)
                row_group.add(cell_text)
            
            row_group.move_to(UP*2 - DOWN*i*0.6)
            table.add(row_group)
        
        # Add table border
        table_border = Rectangle(
            width=10, height=4,
            stroke_color=WHITE, stroke_width=2,
            fill_opacity=0
        ).move_to(table.get_center())
        
        self.play(Create(table_border))
        for row in table:
            self.play(*[Write(cell) for cell in row])
            self.wait(0.5)
        
        # Add key insights
        insights = VGroup(
            Text("Key Insights:", font_size=20, color=YELLOW, weight=BOLD),
            VGroup(
                Text("🔴 Likelihood-based metrics (AIC, Log-Loss) are highly sensitive", font_size=16, color=RED),
                Text("🟢 Ranking-based metrics (AUC) are more robust", font_size=16, color=GREEN),
                Text("🟡 Classification metrics vary based on decision thresholds", font_size=16, color=ORANGE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        ).arrange(DOWN, buff=0.4).next_to(table_border, DOWN, buff=0.8)
        
        for item in insights:
            self.play(Write(item))
            self.wait(1)
        
        self.wait(2)
        self.play(FadeOut(table, table_border, insights))
        self.comparison_title = comparison_title
    
    def show_summary(self):
        """Show final summary"""
        summary_title = Text("Weights Impact Summary", font_size=32, color=YELLOW, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.comparison_title, summary_title))
        
        # Create summary card
        summary_card = RoundedRectangle(
            corner_radius=0.2, width=12, height=5.5,
            stroke_color=WHITE, stroke_width=2,
            fill_color=BLACK, fill_opacity=0.95
        ).move_to(ORIGIN)
        
        # Summary content
        summary_content = VGroup(
            Text("Impact of Sample Weights on Metrics:", font_size=24, color=YELLOW, weight=BOLD),
            VGroup(
                Text("🎯 AIC (Highly Sensitive):", font_size=18, color=RED, weight=BOLD),
                Text("   • Direct impact through weighted log-likelihood", font_size=16, color=WHITE),
                Text("   • Amplifying noise increases AIC", font_size=16, color=WHITE),
                Text("   • Weighting informative data improves AIC", font_size=16, color=WHITE),
                Text("", font_size=4),  # Spacer
                Text("🎯 AUC (Low Sensitivity):", font_size=18, color=GREEN, weight=BOLD),
                Text("   • Based on ranking/ordering of predictions", font_size=16, color=WHITE),
                Text("   • Weights don't change relative order much", font_size=16, color=WHITE),
                Text("   • More robust to weighting schemes", font_size=16, color=WHITE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2),
            
            Text("Best Practice:", font_size=20, color=ORANGE, weight=BOLD),
            Text("Consider metric sensitivity when choosing evaluation approach for weighted models", 
                 font_size=16, color=WHITE, slant=ITALIC)
        ).arrange(DOWN, buff=0.4).move_to(summary_card.get_center())
        
        self.play(FadeIn(summary_card), *[Write(item) for item in summary_content])
        
        # Final message
        final_message = Text(
            "Understand how weights affect different metrics to make informed model choices!",
            font_size=20,
            color=YELLOW,
            weight=BOLD
        ).next_to(summary_card, DOWN, buff=0.8)
        
        self.play(Write(final_message))
        self.wait(3)