#!/usr/bin/env python3
"""
Correlation Heat Map and Multicollinearity - Final Working Version
Shows why multicollinearity affects GLMs more than trees
"""

from manim import *

class CorrelationFinalAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Show intro
        self.show_intro()
        
        # Show the core concept
        self.show_core_concept()
        
        # Show GLM vs Trees
        self.show_model_comparison()
        
        # Show summary
        self.show_final_summary()
    
    def show_intro(self):
        """Simple introduction"""
        title = Text("Correlation & Multicollinearity", font_size=36, color=YELLOW, weight=BOLD).to_edge(UP)
        subtitle = Text("Why GLMs are more sensitive than Trees", font_size=24, color=WHITE).next_to(title, DOWN, buff=0.4)
        
        self.play(Write(title), Write(subtitle))
        self.wait(2)
        
        # Key question
        question = Text(
            "Why do correlation heat maps matter more for GLMs?",
            font_size=22, color=ORANGE
        ).next_to(subtitle, DOWN, buff=1)
        
        self.play(FadeIn(question, shift=UP))
        self.wait(3)
        self.play(FadeOut(title, subtitle, question))
    
    def show_core_concept(self):
        """Show core concept with simple visualization"""
        title = Text("Heat Map Interpretation", font_size=32, color=BLUE).to_edge(UP)
        self.play(Write(title))
        
        # Show correlation examples
        correlation_examples = VGroup(
            VGroup(
                Rectangle(width=1, height=1, fill_color=RED, fill_opacity=0.8, stroke_color=WHITE),
                Text("0.92", font_size=18, color=WHITE, weight=BOLD)
            ).arrange(DOWN, buff=0.2),
            Text("High Correlation\n(Multicollinearity)", font_size=18, color=RED, weight=BOLD)
        ).arrange(RIGHT, buff=1).move_to(LEFT*3 + UP*1)
        
        moderate_examples = VGroup(
            VGroup(
                Rectangle(width=1, height=1, fill_color=ORANGE, fill_opacity=0.8, stroke_color=WHITE),
                Text("0.65", font_size=18, color=WHITE, weight=BOLD)
            ).arrange(DOWN, buff=0.2),
            Text("Moderate\nCorrelation", font_size=18, color=ORANGE, weight=BOLD)
        ).arrange(RIGHT, buff=1).move_to(ORIGIN + UP*1)
        
        low_examples = VGroup(
            VGroup(
                Rectangle(width=1, height=1, fill_color=BLUE, fill_opacity=0.8, stroke_color=WHITE),
                Text("0.25", font_size=18, color=WHITE, weight=BOLD)
            ).arrange(DOWN, buff=0.2),
            Text("Low\nCorrelation", font_size=18, color=BLUE, weight=BOLD)
        ).arrange(RIGHT, buff=1).move_to(RIGHT*3 + UP*1)
        
        self.play(FadeIn(correlation_examples), FadeIn(moderate_examples), FadeIn(low_examples))
        
        # Add interpretation rule
        rule = VGroup(
            Text("🚨 Rule: |r| > 0.8 = Multicollinearity Problem", font_size=22, color=YELLOW, weight=BOLD),
            Text("Example: Income & Salary with r = 0.92", font_size=18, color=WHITE)
        ).arrange(DOWN, buff=0.4).next_to(correlation_examples, DOWN, buff=1.5)
        
        self.play(Write(rule[0]))
        self.play(Write(rule[1]))
        
        self.wait(3)
        self.play(FadeOut(correlation_examples, moderate_examples, low_examples, rule))
        
        self.title = title
    
    def show_model_comparison(self):
        """Show why GLMs vs Trees handle multicollinearity differently"""
        comparison_title = Text("GLMs vs Trees: Multicollinearity Impact", font_size=28, color=RED).to_edge(UP)
        self.play(ReplacementTransform(self.title, comparison_title))
        
        # GLM problems (left side)
        glm_problems = VGroup(
            Text("GLMs (Linear Models)", font_size=24, color=RED, weight=BOLD),
            Rectangle(width=6, height=0.1, fill_color=RED, fill_opacity=0.8),
            Text("❌ Matrix becomes unstable", font_size=18, color=WHITE),
            Text("❌ Coefficients unreliable", font_size=18, color=WHITE),
            Text("❌ Standard errors inflated", font_size=18, color=WHITE),
            Text("❌ Poor interpretation", font_size=18, color=WHITE),
            Text("Math: (XᵀX)⁻¹ fails when X₁ ≈ X₂", font_size=16, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(LEFT*3)
        
        # Tree advantages (right side)
        tree_advantages = VGroup(
            Text("Tree Models", font_size=24, color=GREEN, weight=BOLD),
            Rectangle(width=6, height=0.1, fill_color=GREEN, fill_opacity=0.8),
            Text("✅ Built-in feature selection", font_size=18, color=WHITE),
            Text("✅ One variable per split", font_size=18, color=WHITE),
            Text("✅ Best predictor wins", font_size=18, color=WHITE),
            Text("✅ No matrix inversions", font_size=18, color=WHITE),
            Text("Logic: Choose Income OR Salary (not both)", font_size=16, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT*3)
        
        # Show GLM problems first
        for item in glm_problems:
            self.play(FadeIn(item))
            self.wait(0.6)
        
        # Then show tree advantages
        self.wait(1)
        for item in tree_advantages:
            self.play(FadeIn(item))
            self.wait(0.6)
        
        # Add versus arrow
        vs_arrow = Arrow(LEFT*0.8, RIGHT*0.8, color=WHITE, stroke_width=4)
        vs_text = Text("VS", font_size=24, color=WHITE, weight=BOLD).next_to(vs_arrow, UP)
        
        self.play(GrowArrow(vs_arrow), Write(vs_text))
        
        self.wait(3)
        self.glm_problems = glm_problems
        self.tree_advantages = tree_advantages
        self.comparison_title = comparison_title
        self.vs_arrow = vs_arrow
        self.vs_text = vs_text
    
    def show_final_summary(self):
        """Show final summary and recommendations"""
        summary_title = Text("Summary & Recommendations", font_size=32, color=YELLOW).to_edge(UP)
        self.play(ReplacementTransform(self.comparison_title, summary_title))
        
        # Clear previous content
        self.play(FadeOut(self.glm_problems, self.tree_advantages, self.vs_arrow, self.vs_text))
        
        # Key takeaways
        takeaways = VGroup(
            VGroup(
                Text("📊", font_size=36),
                Text("Heat Map Reading:", font_size=24, color=BLUE, weight=BOLD),
                VGroup(
                    Text("• Red cells = high correlation", font_size=20, color=WHITE),
                    Text("• |r| > 0.8 = multicollinearity", font_size=20, color=WHITE)
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            ).arrange(RIGHT, buff=0.8),
            
            VGroup(
                Text("⚠️", font_size=36),
                Text("GLM Problems:", font_size=24, color=RED, weight=BOLD),
                VGroup(
                    Text("• Unstable coefficient estimates", font_size=20, color=WHITE),
                    Text("• Poor statistical inference", font_size=20, color=WHITE)
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            ).arrange(RIGHT, buff=0.8),
            
            VGroup(
                Text("✅", font_size=36),
                Text("Tree Advantages:", font_size=24, color=GREEN, weight=BOLD),
                VGroup(
                    Text("• Automatic feature selection", font_size=20, color=WHITE),
                    Text("• Handles correlation naturally", font_size=20, color=WHITE)
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            ).arrange(RIGHT, buff=0.8),
            
            VGroup(
                Text("💡", font_size=36),
                Text("Recommendations:", font_size=24, color=ORANGE, weight=BOLD),
                VGroup(
                    Text("• Check correlations before using GLMs", font_size=20, color=WHITE),
                    Text("• Consider trees for correlated predictors", font_size=20, color=WHITE)
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            ).arrange(RIGHT, buff=0.8)
        ).arrange(DOWN, aligned_edge=LEFT, buff=1)
        
        # Animate takeaways
        for takeaway in takeaways:
            self.play(FadeIn(takeaway, shift=UP))
            self.wait(1.5)
        
        # Final insight
        final_insight = Text(
            "Understanding multicollinearity helps you choose the right modeling approach!",
            font_size=22,
            color=YELLOW,
            weight=BOLD
        ).next_to(takeaways, DOWN, buff=1.5)
        
        self.play(Write(final_insight))
        self.wait(4)