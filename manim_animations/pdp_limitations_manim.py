#!/usr/bin/env python3
"""
Partial Dependence Plot Limitations Animation
Shows the key limitations of PDPs and why they can be misleading
"""

from manim import *
import numpy as np

class PDPLimitationsAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Show intro
        self.show_intro()
        
        # Show what PDPs do
        self.show_pdp_concept()
        
        # Show independence assumption limitation
        self.show_independence_limitation()
        
        # Show unrealistic combinations limitation
        self.show_unrealistic_combinations()
        
        # Show alternatives and recommendations
        self.show_alternatives()
        
        # Final summary
        self.show_summary()
    
    def show_intro(self):
        """Introduction to PDP limitations"""
        title = Text("Partial Dependence Plot Limitations", font_size=36, color=YELLOW, weight=BOLD).to_edge(UP)
        subtitle = Text("Why PDPs can be misleading in practice", font_size=24, color=WHITE).next_to(title, DOWN, buff=0.4)
        
        self.play(Write(title), Write(subtitle))
        self.wait(2)
        
        # Key questions
        questions = VGroup(
            Text("• What do PDPs assume about feature relationships?", font_size=20, color=LIGHT_GRAY),
            Text("• Why can some plotted combinations be unrealistic?", font_size=20, color=LIGHT_GRAY),
            Text("• How can this lead to wrong conclusions?", font_size=20, color=LIGHT_GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(subtitle, DOWN, buff=1)
        
        for q in questions:
            self.play(FadeIn(q, shift=UP))
            self.wait(0.8)
        
        self.wait(2)
        self.play(FadeOut(title, subtitle, questions))
    
    def show_pdp_concept(self):
        """Show what PDPs do conceptually"""
        title = Text("What PDPs Do", font_size=32, color=BLUE).to_edge(UP)
        self.play(Write(title))
        
        # PDP concept
        concept = VGroup(
            Text("Partial Dependence Plot Process:", font_size=24, color=ORANGE, weight=BOLD),
            Text("1. Fix target variable (e.g., Age = 30)", font_size=20, color=WHITE),
            Text("2. Let all other variables vary naturally", font_size=20, color=WHITE),
            Text("3. Average predictions across all combinations", font_size=20, color=WHITE),
            Text("4. Show effect of Age on predictions", font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(ORIGIN)
        
        for item in concept:
            self.play(Write(item))
            self.wait(0.8)
        
        # Add formula
        formula = VGroup(
            Text("Formula:", font_size=20, color=YELLOW, weight=BOLD),
            Text("PD(x_s) = E[f(x_s, X_c)] = (1/n) Σ f(x_s, x_c^(i))", font_size=18, color=WHITE)
        ).arrange(DOWN, buff=0.3).next_to(concept, DOWN, buff=1)
        
        self.play(Write(formula))
        self.wait(2)
        
        self.play(FadeOut(concept, formula))
        self.title = title
    
    def show_independence_limitation(self):
        """Show the independence assumption limitation"""
        limitation_title = Text("Limitation 1: Independence Assumption", font_size=28, color=RED).to_edge(UP)
        self.play(ReplacementTransform(self.title, limitation_title))
        
        # Problem explanation
        problem = VGroup(
            Text("🚨 Critical Assumption:", font_size=24, color=YELLOW, weight=BOLD),
            Text("PDPs assume features are independent", font_size=20, color=WHITE),
            Text("Reality: Features are often correlated!", font_size=20, color=RED, weight=BOLD)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(UP*1.5)
        
        for item in problem:
            self.play(Write(item))
            self.wait(0.8)
        
        # Example with correlated features
        example = VGroup(
            Text("Example: House Price Prediction", font_size=22, color=ORANGE, weight=BOLD),
            Text("• Size and Bedrooms are highly correlated", font_size=18, color=WHITE),
            Text("• Small house (800 sq ft) rarely has 5 bedrooms", font_size=18, color=WHITE),
            Text("• But PDP will average over ALL combinations!", font_size=18, color=RED, weight=BOLD)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(problem, DOWN, buff=1)
        
        for item in example:
            self.play(Write(item))
            self.wait(0.8)
        
        # Visual representation
        correlation_warning = VGroup(
            Text("⚠️ PDP Problem:", font_size=20, color=YELLOW, weight=BOLD),
            Text("Includes impossible combinations like:", font_size=18, color=WHITE),
            Text("Size=800sqft + Bedrooms=5 + Location=Downtown", font_size=16, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(example, DOWN, buff=0.8)
        
        for item in correlation_warning:
            self.play(Write(item))
            self.wait(0.8)
        
        self.wait(2)
        self.play(FadeOut(problem, example, correlation_warning))
        self.limitation_title = limitation_title
    
    def show_unrealistic_combinations(self):
        """Show unrealistic combinations limitation"""
        unrealistic_title = Text("Limitation 2: Unrealistic Feature Combinations", font_size=26, color=RED).to_edge(UP)
        self.play(ReplacementTransform(self.limitation_title, unrealistic_title))
        
        # Create visual example
        realistic_box = VGroup(
            Text("Realistic Data Region", font_size=20, color=GREEN, weight=BOLD),
            Rectangle(width=3, height=2, stroke_color=GREEN, stroke_width=3, fill_opacity=0.1, fill_color=GREEN)
        ).arrange(DOWN, buff=0.3).move_to(LEFT*3 + UP*0.5)
        
        unrealistic_box = VGroup(
            Text("PDP Extrapolation", font_size=20, color=RED, weight=BOLD),
            Rectangle(width=3, height=2, stroke_color=RED, stroke_width=3, fill_opacity=0.1, fill_color=RED)
        ).arrange(DOWN, buff=0.3).move_to(RIGHT*3 + UP*0.5)
        
        self.play(FadeIn(realistic_box), FadeIn(unrealistic_box))
        
        # Examples in each region
        realistic_examples = VGroup(
            Text("Real combinations:", font_size=16, color=WHITE, weight=BOLD),
            Text("Age=25, Income=$40k", font_size=14, color=WHITE),
            Text("Age=50, Income=$80k", font_size=14, color=WHITE),
            Text("Age=65, Income=$30k", font_size=14, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(realistic_box[1].get_center())
        
        unrealistic_examples = VGroup(
            Text("PDP includes:", font_size=16, color=WHITE, weight=BOLD),
            Text("Age=25, Income=$200k", font_size=14, color=RED),
            Text("Age=70, Income=$5k", font_size=14, color=RED),
            Text("Age=18, Income=$150k", font_size=14, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(unrealistic_box[1].get_center())
        
        self.play(Write(realistic_examples), Write(unrealistic_examples))
        
        # Problem explanation
        problem_explanation = VGroup(
            Text("The Problem:", font_size=22, color=YELLOW, weight=BOLD),
            Text("• Model was never trained on these combinations", font_size=18, color=WHITE),
            Text("• Predictions in unrealistic regions are unreliable", font_size=18, color=WHITE),
            Text("• PDP averages over both realistic AND unrealistic data", font_size=18, color=RED, weight=BOLD)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(DOWN*2)
        
        for item in problem_explanation:
            self.play(Write(item))
            self.wait(0.8)
        
        self.wait(2)
        self.play(FadeOut(realistic_box, unrealistic_box, realistic_examples, unrealistic_examples, problem_explanation))
        self.unrealistic_title = unrealistic_title
    
    def show_alternatives(self):
        """Show alternatives to PDPs"""
        alternatives_title = Text("Better Alternatives", font_size=32, color=GREEN).to_edge(UP)
        self.play(ReplacementTransform(self.unrealistic_title, alternatives_title))
        
        # Alternative methods
        alternatives = VGroup(
            VGroup(
                Text("1. Accumulated Local Effects (ALE)", font_size=24, color=BLUE, weight=BOLD),
                Text("• Respects feature correlations", font_size=20, color=WHITE),
                Text("• Only uses realistic feature combinations", font_size=20, color=WHITE),
                Text("• Better for correlated features", font_size=20, color=WHITE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2),
            
            VGroup(
                Text("2. Individual Conditional Expectation (ICE)", font_size=24, color=ORANGE, weight=BOLD),
                Text("• Shows individual prediction curves", font_size=20, color=WHITE),
                Text("• Reveals heterogeneity hidden by averaging", font_size=20, color=WHITE),
                Text("• Complements PDPs nicely", font_size=20, color=WHITE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2),
            
            VGroup(
                Text("3. SHAP Values", font_size=24, color=PURPLE, weight=BOLD),
                Text("• Feature importance for individual predictions", font_size=20, color=WHITE),
                Text("• Considers feature interactions", font_size=20, color=WHITE),
                Text("• Model-agnostic explanations", font_size=20, color=WHITE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.8)
        
        for alt in alternatives:
            self.play(Write(alt[0]))
            for item in alt[1:]:
                self.play(Write(item))
                self.wait(0.5)
            self.wait(0.8)
        
        self.wait(2)
        self.alternatives = alternatives
        self.alternatives_title = alternatives_title
    
    def show_summary(self):
        """Show final summary and recommendations"""
        summary_title = Text("Summary & Best Practices", font_size=32, color=YELLOW).to_edge(UP)
        self.play(ReplacementTransform(self.alternatives_title, summary_title))
        
        # Clear alternatives
        self.play(FadeOut(self.alternatives))
        
        # Summary points
        pdp_limitations = VGroup(
            Text("📊 PDP Limitations:", font_size=24, color=RED, weight=BOLD),
            Text("• Assumes feature independence (rarely true)", font_size=20, color=WHITE),
            Text("• Includes unrealistic feature combinations", font_size=20, color=WHITE),
            Text("• Can give misleading average effects", font_size=20, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(UP*1.8)
        
        recommendations = VGroup(
            Text("💡 Recommendations:", font_size=24, color=GREEN, weight=BOLD),
            Text("• Check feature correlations before using PDPs", font_size=20, color=WHITE),
            Text("• Use ALE plots for correlated features", font_size=20, color=WHITE),
            Text("• Combine PDPs with ICE plots for full picture", font_size=20, color=WHITE),
            Text("• Consider SHAP for individual explanations", font_size=20, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(DOWN*0.5)
        
        warning_box = VGroup(
            Text("⚠️ Key Takeaway:", font_size=24, color=YELLOW, weight=BOLD),
            Text("PDPs can be misleading when features are correlated!", font_size=20, color=WHITE),
            Text("Always validate your interpretations with domain knowledge", font_size=18, color=LIGHT_GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(DOWN*2.8)
        
        # Animate summary
        sections = [pdp_limitations, recommendations, warning_box]
        for section in sections:
            self.play(Write(section[0]))
            for item in section[1:]:
                self.play(Write(item))
                self.wait(0.6)
            self.wait(1)
        
        # Final message
        final_message = Text(
            "Choose the right interpretability method for your data structure!",
            font_size=22,
            color=YELLOW,
            weight=BOLD
        ).to_edge(DOWN, buff=0.5)
        
        self.play(Write(final_message))
        self.wait(4)