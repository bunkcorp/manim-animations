#!/usr/bin/env python3
"""
Correlation Heat Map and Multicollinearity - Basic Animation
Shows why multicollinearity affects GLMs more than trees
"""

from manim import *

class CorrelationBasicAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Show intro
        self.show_intro()
        
        # Show heat map concept
        self.show_heatmap_concept()
        
        # Show GLM vs Trees comparison
        self.show_glm_vs_trees()
        
        # Show summary
        self.show_summary()
    
    def show_intro(self):
        """Introduction"""
        title = Text("Correlation Heat Maps & Multicollinearity", font_size=32, color=YELLOW, weight=BOLD).to_edge(UP)
        subtitle = Text("Why it affects GLMs more than Tree models", font_size=22, color=WHITE).next_to(title, DOWN, buff=0.3)
        
        self.play(Write(title), Write(subtitle))
        self.wait(2)
        
        # Key concepts
        concepts = VGroup(
            Text("🎯 Heat maps visualize correlations between variables", font_size=20, color=WHITE),
            Text("⚠️ High correlation (|r| > 0.8) = multicollinearity", font_size=20, color=WHITE),
            Text("🔍 Problem: GLMs struggle, Trees handle it better", font_size=20, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(subtitle, DOWN, buff=1)
        
        for concept in concepts:
            self.play(FadeIn(concept, shift=UP))
            self.wait(1)
        
        self.wait(2)
        self.play(FadeOut(title, subtitle, concepts))
    
    def show_heatmap_concept(self):
        """Show heat map concept with simple visualization"""
        title = Text("Correlation Heat Map Example", font_size=28, color=BLUE).to_edge(UP)
        self.play(Write(title))
        
        # Create simple heat map representation
        # 3x3 grid showing Income, Salary, Age correlations
        variables = ["Income", "Salary", "Age"]
        
        # Create grid
        grid = VGroup()
        cell_size = 1.5
        
        # Add variable labels
        for i, var in enumerate(variables):
            # Row labels
            row_label = Text(var, font_size=18, color=WHITE).move_to([-3, (1-i)*cell_size, 0])
            # Column labels  
            col_label = Text(var, font_size=18, color=WHITE).move_to([(i-1)*cell_size, 2.5, 0])
            grid.add(row_label, col_label)
        
        # Create correlation cells with colors and values
        correlations = [
            [("1.0", GRAY), ("0.92", RED), ("0.3", LIGHT_BLUE)],    # Income row
            [("0.92", RED), ("1.0", GRAY), ("0.25", LIGHT_BLUE)],   # Salary row
            [("0.3", LIGHT_BLUE), ("0.25", LIGHT_BLUE), ("1.0", GRAY)]  # Age row
        ]
        
        for i in range(3):
            for j in range(3):
                corr_val, cell_color = correlations[i][j]
                
                # Create cell
                cell = Rectangle(
                    width=cell_size*0.8,
                    height=cell_size*0.8,
                    fill_color=cell_color,
                    fill_opacity=0.7,
                    stroke_color=WHITE,
                    stroke_width=2
                )
                
                # Position
                x_pos = (j-1)*cell_size
                y_pos = (1-i)*cell_size
                cell.move_to([x_pos, y_pos, 0])
                
                # Add correlation value
                text_color = WHITE if cell_color == RED or cell_color == GRAY else BLACK
                corr_text = Text(corr_val, font_size=16, color=text_color, weight=BOLD)
                corr_text.move_to(cell.get_center())
                
                grid.add(cell, corr_text)
        
        self.play(FadeIn(grid))
        
        # Highlight the problematic correlation
        problem_box = Rectangle(
            width=cell_size*0.9,
            height=cell_size*0.9, 
            stroke_color=YELLOW,
            stroke_width=6,
            fill_opacity=0
        ).move_to([-cell_size, cell_size, 0])  # Income-Salary cell
        
        problem_box2 = Rectangle(
            width=cell_size*0.9,
            height=cell_size*0.9,
            stroke_color=YELLOW, 
            stroke_width=6,
            fill_opacity=0
        ).move_to([0, 0, 0])  # Salary-Income cell
        
        self.play(Create(problem_box), Create(problem_box2))
        
        # Explanation
        explanation = Text("🚨 High Multicollinearity: Income ↔ Salary (r = 0.92)", 
                         font_size=20, color=YELLOW, weight=BOLD).to_edge(DOWN, buff=1)
        self.play(Write(explanation))
        
        self.wait(3)
        self.play(FadeOut(problem_box, problem_box2, explanation))
        
        self.grid = grid
        self.title = title
    
    def show_glm_vs_trees(self):
        """Show why GLMs are more affected than trees"""
        comparison_title = Text("GLMs vs Trees: Impact of Multicollinearity", font_size=28, color=RED).to_edge(UP)
        self.play(ReplacementTransform(self.title, comparison_title))
        
        # Move grid to left
        self.play(self.grid.animate.scale(0.6).to_edge(LEFT, buff=0.8))
        
        # GLM problems (right side, top)
        glm_section = VGroup(
            Text("GLMs (Linear Models)", font_size=22, color=RED, weight=BOLD),
            Text("❌ Matrix inversion problems", font_size=18, color=WHITE),
            Text("❌ Unstable coefficients", font_size=18, color=WHITE),
            Text("❌ High standard errors", font_size=18, color=WHITE),
            Text("❌ Poor interpretability", font_size=18, color=WHITE),
            Text("Math: (XᵀX)⁻¹ becomes unstable", font_size=16, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT*2 + UP*1.5)
        
        # Tree advantages (right side, bottom)
        tree_section = VGroup(
            Text("Tree Models", font_size=22, color=GREEN, weight=BOLD),
            Text("✅ Built-in feature selection", font_size=18, color=WHITE),
            Text("✅ One variable per split", font_size=18, color=WHITE),
            Text("✅ Best feature wins", font_size=18, color=WHITE),
            Text("✅ No matrix inversions", font_size=18, color=WHITE),
            Text("Logic: if Income > X then left else right", font_size=16, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT*2 + DOWN*1.5)
        
        # Show GLM problems
        self.play(Write(glm_section[0]))
        for item in glm_section[1:]:
            self.play(Write(item))
            self.wait(0.6)
        
        # Show tree advantages
        self.wait(1)
        self.play(Write(tree_section[0]))
        for item in tree_section[1:]:
            self.play(Write(item))
            self.wait(0.6)
        
        self.wait(2)
        self.comparison_title = comparison_title
        self.glm_section = glm_section
        self.tree_section = tree_section
    
    def show_summary(self):
        """Show final summary"""
        summary_title = Text("Key Takeaways", font_size=32, color=YELLOW, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.comparison_title, summary_title))
        
        # Clear previous content
        self.play(FadeOut(self.glm_section, self.tree_section, self.grid))
        
        # Main points
        takeaways = VGroup(
            VGroup(
                Text("📊", font_size=32),
                Text("Heat Map Reading:", font_size=24, color=BLUE, weight=BOLD),
                Text("Look for dark red cells (high |r|)", font_size=20, color=WHITE)
            ).arrange(RIGHT, buff=0.5),
            
            VGroup(
                Text("⚠️", font_size=32),
                Text("Multicollinearity Rule:", font_size=24, color=ORANGE, weight=BOLD),
                Text("|r| > 0.8 between predictors = problem", font_size=20, color=WHITE)
            ).arrange(RIGHT, buff=0.5),
            
            VGroup(
                Text("🔴", font_size=32),
                Text("GLM Impact:", font_size=24, color=RED, weight=BOLD), 
                Text("Serious issues with correlated predictors", font_size=20, color=WHITE)
            ).arrange(RIGHT, buff=0.5),
            
            VGroup(
                Text("🟢", font_size=32),
                Text("Tree Advantage:", font_size=24, color=GREEN, weight=BOLD),
                Text("Handles correlation through feature selection", font_size=20, color=WHITE)
            ).arrange(RIGHT, buff=0.5),
            
            VGroup(
                Text("💡", font_size=32),
                Text("Recommendation:", font_size=24, color=YELLOW, weight=BOLD),
                Text("Check correlations before choosing GLMs", font_size=20, color=WHITE)
            ).arrange(RIGHT, buff=0.5)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.8)
        
        # Animate takeaways
        for takeaway in takeaways:
            self.play(FadeIn(takeaway))
            self.wait(1.2)
        
        # Final message
        final_message = Text(
            "Understanding multicollinearity helps you choose the right model!",
            font_size=22,
            color=YELLOW,
            weight=BOLD
        ).next_to(takeaways, DOWN, buff=1.5)
        
        self.play(Write(final_message))
        self.wait(3)