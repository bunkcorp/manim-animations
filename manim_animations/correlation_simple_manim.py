#!/usr/bin/env python3
"""
Correlation Heat Map and Multicollinearity - Simplified Animation
Shows why multicollinearity affects GLMs more than trees
"""

from manim import *
import numpy as np

class CorrelationSimpleAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Show intro
        self.show_intro()
        
        # Show heat map example
        self.show_heatmap_example()
        
        # Show multicollinearity identification
        self.show_multicollinearity()
        
        # Show GLM vs Trees impact
        self.show_glm_vs_trees_impact()
        
        # Show summary
        self.show_summary()
    
    def show_intro(self):
        """Introduction"""
        title = Text("Correlation Heat Maps & Multicollinearity", font_size=32, color=YELLOW, weight=BOLD).to_edge(UP)
        subtitle = Text("Why it affects GLMs more than Tree-based models", font_size=22, color=WHITE).next_to(title, DOWN, buff=0.3)
        
        self.play(Write(title), Write(subtitle))
        self.wait(2)
        
        # Key questions
        questions = VGroup(
            Text("• How to interpret correlation heat maps?", font_size=20, color=LIGHT_GRAY),
            Text("• How to identify multicollinearity?", font_size=20, color=LIGHT_GRAY),
            Text("• Why does it matter more for GLMs?", font_size=20, color=LIGHT_GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(subtitle, DOWN, buff=1)
        
        for q in questions:
            self.play(FadeIn(q, shift=UP))
            self.wait(0.8)
        
        self.wait(2)
        self.play(FadeOut(title, subtitle, questions))
    
    def show_heatmap_example(self):
        """Show a simplified heat map example"""
        title = Text("Correlation Heat Map Example", font_size=28, color=CYAN).to_edge(UP)
        self.play(Write(title))
        
        # Create a simple 3x3 correlation matrix visualization
        variables = ["Income", "Salary", "Age"]
        
        # Create heat map cells
        heatmap_group = VGroup()
        
        # Correlation values
        correlations = [
            [1.0, 0.92, 0.3],   # Income row
            [0.92, 1.0, 0.25],  # Salary row  
            [0.3, 0.25, 1.0]    # Age row
        ]
        
        cell_size = 1.2
        
        for i in range(3):
            for j in range(3):
                corr_val = correlations[i][j]
                
                # Color based on correlation strength
                if abs(corr_val) > 0.8 and i != j:
                    cell_color = RED
                    text_color = WHITE
                elif abs(corr_val) > 0.5:
                    cell_color = ORANGE
                    text_color = BLACK
                elif i == j:
                    cell_color = GRAY
                    text_color = WHITE
                else:
                    cell_color = LIGHT_BLUE
                    text_color = BLACK
                
                # Create cell
                cell = Rectangle(
                    width=cell_size,
                    height=cell_size,
                    fill_color=cell_color,
                    fill_opacity=0.8,
                    stroke_color=WHITE,
                    stroke_width=2
                )
                
                # Position
                x_pos = (j - 1) * cell_size
                y_pos = (1 - i) * cell_size
                cell.move_to([x_pos, y_pos, 0])
                
                # Add text
                corr_text = Text(f"{corr_val:.2f}", font_size=16, color=text_color, weight=BOLD)
                corr_text.move_to(cell.get_center())
                
                heatmap_group.add(cell, corr_text)
        
        # Add labels
        for i, var in enumerate(variables):
            # Row labels
            row_label = Text(var, font_size=18, color=WHITE).move_to([-2.5, (1-i)*cell_size, 0])
            # Column labels
            col_label = Text(var, font_size=18, color=WHITE).move_to([(i-1)*cell_size, 2, 0])
            heatmap_group.add(row_label, col_label)
        
        heatmap_group.move_to(ORIGIN)
        self.play(FadeIn(heatmap_group))
        
        # Add legend
        legend = VGroup(
            Text("Color Guide:", font_size=18, color=WHITE, weight=BOLD),
            VGroup(Rectangle(width=0.3, height=0.3, fill_color=RED, fill_opacity=0.8),
                   Text("|r| > 0.8 (High)", font_size=14, color=WHITE)).arrange(RIGHT, buff=0.2),
            VGroup(Rectangle(width=0.3, height=0.3, fill_color=ORANGE, fill_opacity=0.8),
                   Text("0.5 < |r| < 0.8", font_size=14, color=WHITE)).arrange(RIGHT, buff=0.2),
            VGroup(Rectangle(width=0.3, height=0.3, fill_color=LIGHT_BLUE, fill_opacity=0.8),
                   Text("|r| < 0.5 (Low)", font_size=14, color=WHITE)).arrange(RIGHT, buff=0.2)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_corner(UR, buff=1)
        
        self.play(FadeIn(legend))
        
        self.heatmap_group = heatmap_group
        self.legend = legend
        self.title = title
    
    def show_multicollinearity(self):
        """Identify multicollinearity in the heat map"""
        multicollinearity_title = Text("Identifying Multicollinearity", font_size=24, color=ORANGE, weight=BOLD)
        multicollinearity_title.next_to(self.title, DOWN, buff=0.5)
        self.play(Write(multicollinearity_title))
        
        # Highlight the high correlation
        highlight_box1 = Rectangle(width=1.3, height=1.3, stroke_color=YELLOW, stroke_width=6, fill_opacity=0)
        highlight_box1.move_to([-1.2, 0, 0])  # Income-Salary
        
        highlight_box2 = Rectangle(width=1.3, height=1.3, stroke_color=YELLOW, stroke_width=6, fill_opacity=0)
        highlight_box2.move_to([0, 1.2, 0])   # Salary-Income
        
        self.play(Create(highlight_box1), Create(highlight_box2))
        
        # Explanation
        explanation = VGroup(
            Text("🚨 Multicollinearity Detected!", font_size=20, color=YELLOW, weight=BOLD),
            Text("Income ↔ Salary: r = 0.92", font_size=18, color=WHITE),
            Text("Rule: |r| > 0.8 indicates problems", font_size=16, color=LIGHT_GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_corner(UL, buff=1)
        
        for line in explanation:
            self.play(Write(line))
            self.wait(0.8)
        
        self.wait(2)
        self.play(FadeOut(highlight_box1, highlight_box2, explanation, multicollinearity_title))
    
    def show_glm_vs_trees_impact(self):
        """Show why GLMs are more affected than trees"""
        impact_title = Text("Impact: GLMs vs Tree Models", font_size=28, color=RED).to_edge(UP)
        self.play(ReplacementTransform(self.title, impact_title))
        
        # Move heatmap to left
        self.play(
            self.heatmap_group.animate.scale(0.7).to_edge(LEFT, buff=1),
            FadeOut(self.legend)
        )
        
        # GLMs problems
        glm_problems = VGroup(
            Text("GLMs (Generalized Linear Models)", font_size=22, color=RED, weight=BOLD),
            Text("❌ Matrix inversion problems", font_size=18, color=WHITE),
            Text("❌ Unstable coefficients", font_size=18, color=WHITE),
            Text("❌ Inflated standard errors", font_size=18, color=WHITE),
            Text("❌ Poor interpretability", font_size=18, color=WHITE),
            Text("Example: β₁ and β₂ highly correlated", font_size=16, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT*2.5 + UP*1.5)
        
        # Tree advantages
        tree_advantages = VGroup(
            Text("Tree Models", font_size=22, color=GREEN, weight=BOLD),
            Text("✅ Built-in feature selection", font_size=18, color=WHITE),
            Text("✅ Uses only one variable per split", font_size=18, color=WHITE),
            Text("✅ Automatically picks best feature", font_size=18, color=WHITE),
            Text("✅ Correlated features compete", font_size=18, color=WHITE),
            Text("Example: Tree picks Income OR Salary", font_size=16, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT*2.5 + DOWN*1.5)
        
        # Show GLM problems
        self.play(Write(glm_problems[0]))
        for item in glm_problems[1:]:
            self.play(Write(item))
            self.wait(0.6)
        
        # Show tree advantages
        self.wait(1)
        self.play(Write(tree_advantages[0]))
        for item in tree_advantages[1:]:
            self.play(Write(item))
            self.wait(0.6)
        
        self.wait(2)
        self.impact_title = impact_title
        self.glm_problems = glm_problems
        self.tree_advantages = tree_advantages
    
    def show_summary(self):
        """Show final summary"""
        summary_title = Text("Summary & Key Takeaways", font_size=28, color=YELLOW).to_edge(UP)
        self.play(ReplacementTransform(self.impact_title, summary_title))
        
        # Clear previous content
        self.play(FadeOut(self.glm_problems, self.tree_advantages, self.heatmap_group))
        
        # Summary points
        summary = VGroup(
            Text("📊 Heat Map Interpretation:", font_size=24, color=CYAN, weight=BOLD),
            Text("• Dark red cells = high positive correlation", font_size=20, color=WHITE),
            Text("• Look for |r| > 0.8 between predictors", font_size=20, color=WHITE),
            Text("• Diagonal always = 1.0 (self-correlation)", font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(UP*1.5)
        
        impact = VGroup(
            Text("⚖️ Model Impact:", font_size=24, color=ORANGE, weight=BOLD),
            Text("• GLMs: Serious problems with multicollinearity", font_size=20, color=RED),
            Text("• Trees: Less problematic due to feature selection", font_size=20, color=GREEN),
            Text("• Ensembles: Even more robust to correlation", font_size=20, color=BLUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(DOWN*0.5)
        
        recommendations = VGroup(
            Text("💡 Recommendations:", font_size=24, color=GREEN, weight=BOLD),
            Text("• For GLMs: Remove correlated variables first", font_size=20, color=WHITE),
            Text("• For Trees: Monitor but less critical", font_size=20, color=WHITE),
            Text("• Use domain knowledge to decide which to keep", font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(DOWN*2.5)
        
        # Animate summary
        sections = [summary, impact, recommendations]
        for section in sections:
            self.play(Write(section[0]))
            for item in section[1:]:
                self.play(Write(item))
                self.wait(0.6)
            self.wait(0.8)
        
        # Final message
        final_message = Text(
            "Choose your modeling approach based on multicollinearity sensitivity!",
            font_size=20,
            color=YELLOW,
            weight=BOLD
        ).next_to(recommendations, DOWN, buff=1)
        
        self.play(Write(final_message))
        self.wait(3)