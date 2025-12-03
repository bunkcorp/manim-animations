#!/usr/bin/env python3
"""
Correlation Heat Map and Multicollinearity Animation
Shows how to interpret correlation heat maps and why multicollinearity affects GLMs more than trees
"""

from manim import *
import numpy as np

class CorrelationHeatMapAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Show intro
        self.show_intro()
        
        # Create correlation heat map
        self.create_heatmap()
        
        # Identify multicollinearity
        self.identify_multicollinearity()
        
        # Show GLM vs Trees comparison
        self.show_glm_vs_trees()
        
        # Show mathematical explanation
        self.show_mathematical_explanation()
        
        # Final summary
        self.show_summary()
    
    def show_intro(self):
        """Introduction to correlation heat maps"""
        title = Text(
            "Correlation Heat Maps & Multicollinearity",
            font_size=36,
            color=YELLOW,
            weight=BOLD
        ).to_edge(UP)
        
        subtitle = Text(
            "Why multicollinearity affects GLMs more than Tree-based models",
            font_size=24,
            color=WHITE
        ).next_to(title, DOWN, buff=0.3)
        
        self.play(Write(title), Write(subtitle))
        self.wait(2)
        
        # Key question
        question = VGroup(
            Text("How do you interpret a correlation heat map?", font_size=22, color=LIGHT_GRAY),
            Text("How do you identify multicollinearity?", font_size=22, color=LIGHT_GRAY),
            Text("Why does it matter more for GLMs than Trees?", font_size=22, color=LIGHT_GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(subtitle, DOWN, buff=1)
        
        for q in question:
            self.play(FadeIn(q, shift=UP))
            self.wait(0.8)
        
        self.wait(2)
        self.play(FadeOut(title, subtitle, question))
    
    def create_heatmap(self):
        """Create an interactive correlation heat map"""
        title = Text("Correlation Heat Map Example", font_size=32, color=YELLOW).to_edge(UP)
        self.play(Write(title))
        
        # Create sample correlation matrix
        variables = ["Age", "Income", "Salary", "Education", "Experience"]
        
        # Realistic correlation matrix (Income and Salary are highly correlated)
        correlation_matrix = np.array([
            [1.0,  0.3,  0.25, 0.4,  0.6],   # Age
            [0.3,  1.0,  0.92, 0.7,  0.5],   # Income  
            [0.25, 0.92, 1.0,  0.65, 0.48],  # Salary (highly correlated with Income)
            [0.4,  0.7,  0.65, 1.0,  0.8],   # Education
            [0.6,  0.5,  0.48, 0.8,  1.0]    # Experience
        ])
        
        # Create heat map visualization
        heatmap_group = self.create_correlation_heatmap(correlation_matrix, variables)
        heatmap_group.scale(0.8).move_to(ORIGIN)
        
        self.play(FadeIn(heatmap_group))
        self.wait(2)
        
        # Add color scale legend
        legend = self.create_color_legend().to_edge(RIGHT, buff=0.8)
        self.play(FadeIn(legend))
        
        self.heatmap_group = heatmap_group
        self.correlation_matrix = correlation_matrix
        self.variables = variables
        self.legend = legend
        self.title = title
    
    def create_correlation_heatmap(self, matrix, variables):
        """Create the visual heat map"""
        n = len(variables)
        cell_size = 0.8
        
        heatmap_group = VGroup()
        
        # Create cells
        for i in range(n):
            for j in range(n):
                corr_val = matrix[i][j]
                
                # Color mapping: -1 (blue) to +1 (red), 0 (white)
                if corr_val >= 0:
                    color_intensity = corr_val
                    cell_color = interpolate_color(WHITE, RED, color_intensity)
                else:
                    color_intensity = abs(corr_val)
                    cell_color = interpolate_color(WHITE, BLUE, color_intensity)
                
                # Create cell
                cell = Rectangle(
                    width=cell_size,
                    height=cell_size,
                    fill_color=cell_color,
                    fill_opacity=0.8,
                    stroke_color=GRAY,
                    stroke_width=1
                )
                
                # Position cell
                x_pos = (j - n/2 + 0.5) * cell_size
                y_pos = (n/2 - i - 0.5) * cell_size
                cell.move_to([x_pos, y_pos, 0])
                
                # Add correlation value text
                if abs(corr_val) > 0.8 and i != j:  # Highlight high correlations
                    text_color = WHITE
                    font_weight = BOLD
                else:
                    text_color = BLACK if abs(corr_val) < 0.5 else WHITE
                    font_weight = NORMAL
                
                corr_text = Text(
                    f"{corr_val:.2f}",
                    font_size=14,
                    color=text_color,
                    weight=font_weight
                ).move_to(cell.get_center())
                
                heatmap_group.add(cell, corr_text)
        
        # Add variable labels
        for i, var in enumerate(variables):
            # Row labels (left side)
            row_label = Text(var, font_size=16, color=WHITE).move_to([
                -n/2 * cell_size - 0.5,
                (n/2 - i - 0.5) * cell_size,
                0
            ])
            
            # Column labels (top)
            col_label = Text(var, font_size=16, color=WHITE).rotate(PI/4).move_to([
                (i - n/2 + 0.5) * cell_size,
                n/2 * cell_size + 0.5,
                0
            ])
            
            heatmap_group.add(row_label, col_label)
        
        return heatmap_group
    
    def create_color_legend(self):
        """Create color scale legend"""
        legend_group = VGroup()
        
        # Legend title
        legend_title = Text("Correlation", font_size=18, color=WHITE, weight=BOLD)
        
        # Color scale
        scale_height = 3
        scale_width = 0.3
        n_steps = 20
        
        for i in range(n_steps):
            corr_val = -1 + (2 * i / (n_steps - 1))  # From -1 to +1
            
            if corr_val >= 0:
                cell_color = interpolate_color(WHITE, RED, corr_val)
            else:
                cell_color = interpolate_color(WHITE, BLUE, abs(corr_val))
            
            y_pos = (i - n_steps/2 + 0.5) * (scale_height / n_steps)
            
            scale_cell = Rectangle(
                width=scale_width,
                height=scale_height / n_steps,
                fill_color=cell_color,
                fill_opacity=0.8,
                stroke_width=0
            ).move_to([0, y_pos, 0])
            
            legend_group.add(scale_cell)
        
        # Add scale labels
        labels = ["+1", "0", "-1"]
        positions = [scale_height/2, 0, -scale_height/2]
        
        for label, pos in zip(labels, positions):
            scale_label = Text(label, font_size=14, color=WHITE).move_to([scale_width + 0.3, pos, 0])
            legend_group.add(scale_label)
        
        # Arrange legend
        legend_content = VGroup(legend_title, legend_group).arrange(DOWN, buff=0.3)
        
        return legend_content
    
    def identify_multicollinearity(self):
        """Highlight and explain multicollinearity"""
        explanation_title = Text("Identifying Multicollinearity", font_size=28, color=ORANGE, weight=BOLD)
        explanation_title.next_to(self.title, DOWN, buff=0.5)
        self.play(Write(explanation_title))
        
        # Highlight high correlation between Income and Salary
        high_corr_box = Rectangle(
            width=0.8,
            height=0.8,
            stroke_color=YELLOW,
            stroke_width=6,
            fill_opacity=0
        ).move_to(self.heatmap_group.submobjects[7].get_center())  # Income-Salary cell
        
        high_corr_box2 = Rectangle(
            width=0.8,
            height=0.8,
            stroke_color=YELLOW,
            stroke_width=6,
            fill_opacity=0
        ).move_to(self.heatmap_group.submobjects[17].get_center())  # Salary-Income cell
        
        self.play(Create(high_corr_box), Create(high_corr_box2))
        
        # Add explanation
        explanation = VGroup(
            Text("🚨 High Multicollinearity Detected!", font_size=20, color=YELLOW, weight=BOLD),
            Text("Income ↔ Salary: r = 0.92", font_size=18, color=WHITE),
            Text("Rule: |r| > 0.8 indicates strong multicollinearity", font_size=16, color=LIGHT_GRAY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UL, buff=1)
        
        for line in explanation:
            self.play(Write(line))
            self.wait(0.8)
        
        # Show other problematic correlations
        self.wait(2)
        
        # Add interpretation guide
        interpretation = VGroup(
            Text("Interpretation Guide:", font_size=18, color=CYAN, weight=BOLD),
            Text("• |r| > 0.8: Strong multicollinearity", font_size=16, color=RED),
            Text("• 0.5 < |r| < 0.8: Moderate correlation", font_size=16, color=ORANGE),
            Text("• |r| < 0.5: Weak correlation", font_size=16, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=1)
        
        for line in interpretation:
            self.play(Write(line))
            self.wait(0.5)
        
        self.wait(2)
        self.play(
            FadeOut(high_corr_box, high_corr_box2),
            FadeOut(explanation),
            FadeOut(interpretation),
            FadeOut(explanation_title)
        )
    
    def show_glm_vs_trees(self):
        """Show why multicollinearity affects GLMs more than trees"""
        comparison_title = Text("GLMs vs Trees: Multicollinearity Impact", font_size=32, color=RED).to_edge(UP)
        self.play(ReplacementTransform(self.title, comparison_title))
        
        # Move heatmap to side
        self.play(
            self.heatmap_group.animate.scale(0.6).to_edge(LEFT, buff=0.5),
            FadeOut(self.legend)
        )
        
        # GLM side (problematic)
        glm_section = VGroup(
            Text("GLMs (Problematic)", font_size=24, color=RED, weight=BOLD),
            Text("❌ Linear combination issues", font_size=18, color=WHITE),
            Text("❌ Unstable coefficients", font_size=18, color=WHITE), 
            Text("❌ Inflated standard errors", font_size=18, color=WHITE),
            Text("❌ Poor interpretability", font_size=18, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT*2 + UP*1.5)
        
        # Tree section (less problematic)  
        tree_section = VGroup(
            Text("Trees (Less Problematic)", font_size=24, color=GREEN, weight=BOLD),
            Text("✅ Feature selection built-in", font_size=18, color=WHITE),
            Text("✅ Non-linear relationships", font_size=18, color=WHITE),
            Text("✅ Handles correlated features", font_size=18, color=WHITE),
            Text("✅ Automatic variable importance", font_size=18, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT*2 + DOWN*1.5)
        
        # Animate sections
        self.play(Write(glm_section[0]))
        for item in glm_section[1:]:
            self.play(Write(item))
            self.wait(0.6)
        
        self.wait(1)
        
        self.play(Write(tree_section[0]))
        for item in tree_section[1:]:
            self.play(Write(item))
            self.wait(0.6)
        
        self.wait(2)
        self.glm_section = glm_section
        self.tree_section = tree_section
        self.comparison_title = comparison_title
    
    def show_mathematical_explanation(self):
        """Show mathematical explanation of why GLMs are affected"""
        math_title = Text("Mathematical Explanation", font_size=32, color=BLUE).to_edge(UP)
        self.play(ReplacementTransform(self.comparison_title, math_title))
        
        # Clear previous content
        self.play(FadeOut(self.glm_section, self.tree_section, self.heatmap_group))
        
        # GLM mathematical problem
        glm_math = VGroup(
            Text("GLM Problem with Multicollinearity:", font_size=24, color=RED, weight=BOLD),
            Text("Linear model: y = β₀ + β₁x₁ + β₂x₂ + ε", font_size=20, color=WHITE),
            Text("If x₁ and x₂ are highly correlated (r ≈ 0.92):", font_size=18, color=YELLOW),
            Text("• Matrix (XᵀX) becomes near-singular", font_size=18, color=WHITE),
            Text("• Coefficients become unstable", font_size=18, color=WHITE),
            Text("• Small data changes → large coefficient changes", font_size=18, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(UP*1.5)
        
        # Tree advantage
        tree_math = VGroup(
            Text("Tree Advantage:", font_size=24, color=GREEN, weight=BOLD),
            Text("Splits: if x₁ > threshold then left else right", font_size=20, color=WHITE),
            Text("• Only uses ONE variable per split", font_size=18, color=YELLOW),
            Text("• Automatically selects most informative feature", font_size=18, color=WHITE),
            Text("• Correlated features compete, best one wins", font_size=18, color=WHITE),
            Text("• No matrix inversion problems", font_size=18, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(DOWN*1.5)
        
        # Animate mathematical explanation
        for section in [glm_math, tree_math]:
            self.play(Write(section[0]))
            for item in section[1:]:
                self.play(Write(item))
                self.wait(0.7)
            self.wait(1)
        
        self.wait(2)
        self.math_title = math_title
        self.glm_math = glm_math
        self.tree_math = tree_math
    
    def show_summary(self):
        """Show final summary and recommendations"""
        summary_title = Text("Summary & Recommendations", font_size=32, color=YELLOW).to_edge(UP)
        self.play(ReplacementTransform(self.math_title, summary_title))
        
        # Clear previous content
        self.play(FadeOut(self.glm_math, self.tree_math))
        
        # Summary points
        summary_points = VGroup(
            Text("📊 Correlation Heat Map Interpretation:", font_size=24, color=CYAN, weight=BOLD),
            Text("• Look for |r| > 0.8 between predictors", font_size=20, color=WHITE),
            Text("• Dark red/blue cells indicate high correlation", font_size=20, color=WHITE),
            Text("• Diagonal = 1.0 (perfect self-correlation)", font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(UP*1.8)
        
        impact_points = VGroup(
            Text("⚖️ Multicollinearity Impact:", font_size=24, color=ORANGE, weight=BOLD),
            Text("• GLMs: Unstable coefficients, poor interpretation", font_size=20, color=RED),
            Text("• Trees: Less problematic, built-in feature selection", font_size=20, color=GREEN),
            Text("• Ensemble trees: Even more robust", font_size=20, color=BLUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(DOWN*0.2)
        
        recommendations = VGroup(
            Text("💡 Recommendations:", font_size=24, color=GREEN, weight=BOLD),
            Text("• For GLMs: Remove/combine correlated features", font_size=20, color=WHITE),
            Text("• For Trees: Monitor but less critical", font_size=20, color=WHITE),
            Text("• Use VIF (Variance Inflation Factor) for quantification", font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(DOWN*2.2)
        
        # Animate summary
        sections = [summary_points, impact_points, recommendations]
        for section in sections:
            self.play(Write(section[0]))
            for item in section[1:]:
                self.play(Write(item))
                self.wait(0.6)
            self.wait(1)
        
        # Final message
        final_message = Text(
            "Understanding multicollinearity helps you choose the right modeling approach!",
            font_size=22,
            color=YELLOW,
            weight=BOLD
        ).next_to(recommendations, DOWN, buff=1)
        
        self.play(Write(final_message))
        self.wait(3)