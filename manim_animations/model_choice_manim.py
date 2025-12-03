#!/usr/bin/env python3
"""
Model Choice: GLMs vs Trees Animation
Shows when to choose GLMs, regularized GLMs, single trees, or ensemble trees
"""

from manim import *
import numpy as np

class ModelChoiceGLMvsTrees(Scene):
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Title
        title = Text(
            "When might you choose GLMs, regularized GLMs, single trees, or ensemble trees?",
            font_size=32,
            color=WHITE
        ).to_edge(UP)
        self.play(FadeIn(title))
        self.wait(1)
        
        # Create axes for trade-off map
        self.create_axes()
        
        # Create model cards
        self.create_model_cards()
        
        # Show scenario highlights
        self.show_scenarios()
        
        # Show final summary
        self.show_summary()
    
    def create_axes(self):
        """Create the interpretability vs complexity axes"""
        # Axes
        x_axis = Arrow(LEFT*5.5 + DOWN*2.5, RIGHT*5.5 + DOWN*2.5, 
                      color=WHITE, stroke_width=4, max_tip_length_to_length_ratio=0.03)
        y_axis = Arrow(LEFT*5.5 + DOWN*2.5, LEFT*5.5 + UP*2.5, 
                      color=WHITE, stroke_width=4, max_tip_length_to_length_ratio=0.03)
        
        # Labels
        x_label = Text("Predictive Power / Complexity →", font_size=24, color=WHITE)\
            .next_to(x_axis, DOWN, buff=0.3)
        y_label = Text("Interpretability ↑", font_size=24, color=WHITE)\
            .rotate(PI/2).next_to(y_axis, LEFT, buff=0.3)
        
        # Speed note
        speed_note = Text("(speed ↓ as you move right)", font_size=20, color=GRAY)\
            .next_to(x_label, DOWN, buff=0.1)
        
        self.play(Create(x_axis), Create(y_axis))
        self.play(Write(x_label), Write(y_label), FadeIn(speed_note))
        self.wait(1)
        
        self.x_axis = x_axis
        self.y_axis = y_axis
    
    def create_model_card(self, title_text, bullets, color=WHITE, width=4.5, height=2.4):
        """Helper function to create model cards"""
        # Card background
        box = RoundedRectangle(
            corner_radius=0.2, 
            width=width, 
            height=height, 
            stroke_color=color,
            stroke_width=3,
            fill_color=color,
            fill_opacity=0.1
        )
        
        # Title
        title = Text(title_text, font_size=26, color=color, weight=BOLD)
        
        # Bullet points
        bullet_lines = VGroup()
        for bullet in bullets:
            bullet_text = Text(f"• {bullet}", font_size=20, color=WHITE)
            bullet_lines.add(bullet_text)
        
        bullet_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        
        # Arrange content
        content = VGroup(title, bullet_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        content.move_to(box.get_center())
        
        return VGroup(box, content)
    
    def create_model_cards(self):
        """Create and position all model cards"""
        # Create cards
        glm_card = self.create_model_card(
            "GLMs",
            ["Interpretability important", "Target distribution known", "Linear relationships"],
            color=YELLOW
        )
        
        reg_glm_card = self.create_model_card(
            "Regularized GLMs", 
            ["Automatic variable selection", "Regularization reduces overfitting", "Feature shrinkage"],
            color=GOLD
        )
        
        tree_card = self.create_model_card(
            "Single Trees",
            ["Easy to interpret paths", "Capture non-linearities", "Handle interactions naturally"],
            color=BLUE
        )
        
        ens_card = self.create_model_card(
            "Ensemble Trees",
            ["Highest accuracy typically", "Less interpretable", "Computationally expensive"],
            color=ORANGE
        )
        
        # Position cards on the interpretability-complexity map
        glm_card.move_to(LEFT*2.8 + UP*1.4)        # High interpretability, low complexity
        reg_glm_card.move_to(RIGHT*0.2 + UP*1.0)   # Still interpretable, moderate complexity
        tree_card.move_to(LEFT*0.8 + DOWN*0.2)     # Moderate interpretability, moderate complexity  
        ens_card.move_to(RIGHT*3.2 + DOWN*1.2)     # Low interpretability, high complexity
        
        # Animate cards appearing
        self.play(
            FadeIn(glm_card, shift=UP*0.5),
            FadeIn(reg_glm_card, shift=UP*0.5),
            FadeIn(tree_card, shift=UP*0.5), 
            FadeIn(ens_card, shift=UP*0.5)
        )
        
        # Add connector arrows to show progression
        arrow1 = Arrow(glm_card.get_right(), reg_glm_card.get_left(), 
                      color=GRAY, stroke_width=2, max_tip_length_to_length_ratio=0.1)
        arrow2 = Arrow(tree_card.get_right(), ens_card.get_left(),
                      color=GRAY, stroke_width=2, max_tip_length_to_length_ratio=0.1)
        
        self.play(GrowArrow(arrow1), GrowArrow(arrow2))
        self.wait(1)
        
        # Store cards for later use
        self.glm_card = glm_card
        self.reg_glm_card = reg_glm_card
        self.tree_card = tree_card
        self.ens_card = ens_card
    
    def highlight_card(self, card, question_text, highlight_color):
        """Highlight a specific card with question"""
        # Show question
        question = Text(question_text, font_size=28, color=WHITE).to_edge(DOWN, buff=0.8)
        self.play(Write(question))
        
        # Highlight card
        glow = SurroundingRectangle(card, color=highlight_color, buff=0.15, stroke_width=6)
        checkmark = Text("✓", font_size=48, color=highlight_color).next_to(card, UP, buff=0.3)
        
        self.play(Create(glow), FadeIn(checkmark, scale=0.7))
        self.wait(2)
        self.play(FadeOut(glow), FadeOut(checkmark), FadeOut(question))
        
    def show_scenarios(self):
        """Show different scenarios and which model to choose"""
        # Scenario 1: GLMs
        self.highlight_card(
            self.glm_card,
            "Use GLMs when interpretability and known distributions are key",
            YELLOW
        )
        
        # Scenario 2: Regularized GLMs  
        self.highlight_card(
            self.reg_glm_card,
            "Use regularized GLMs for automatic selection and overfitting control",
            GOLD
        )
        
        # Scenario 3: Single Trees
        self.highlight_card(
            self.tree_card,
            "Use single trees for interpretable models with complex relationships",
            BLUE
        )
        
        # Scenario 4: Ensemble Trees
        self.highlight_card(
            self.ens_card,
            "Use ensemble trees for maximum accuracy (when interpretability is less important)",
            ORANGE
        )
    
    def show_summary(self):
        """Show final summary of recommendations"""
        summary_title = Text("Quick Decision Guide", font_size=32, color=YELLOW, weight=BOLD).to_corner(UL, buff=0.8)
        
        summary_points = VGroup(
            Text("GLMs → interpretability + known distributions", font_size=22, color=YELLOW),
            Text("Regularized GLMs → variable selection + shrinkage", font_size=22, color=GOLD),
            Text("Single Trees → clear rules + nonlinear patterns", font_size=22, color=BLUE),
            Text("Ensemble Trees → best accuracy (less interpretable)", font_size=22, color=ORANGE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(summary_title, DOWN, buff=0.4)
        
        # Animate summary
        self.play(Write(summary_title))
        for point in summary_points:
            self.play(Write(point))
            self.wait(0.8)
        
        # Add decision flowchart
        flowchart_title = Text("Decision Flowchart:", font_size=24, color=WHITE, weight=BOLD)\
            .next_to(summary_points, DOWN, buff=0.8)
        
        flowchart = VGroup(
            Text("1. Need interpretability? → GLMs or Single Trees", font_size=18, color=WHITE),
            Text("2. Have many features? → Regularized GLMs", font_size=18, color=WHITE), 
            Text("3. Complex patterns? → Trees (single or ensemble)", font_size=18, color=WHITE),
            Text("4. Maximum accuracy? → Ensemble Trees", font_size=18, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(flowchart_title, DOWN, buff=0.3)
        
        self.play(Write(flowchart_title))
        for step in flowchart:
            self.play(Write(step))
            self.wait(0.6)
        
        # Final message
        self.wait(2)
        final_message = Text(
            "Choose the right tool for your specific problem and constraints!",
            font_size=26,
            color=GREEN
        ).next_to(flowchart, DOWN, buff=1)
        
        self.play(Write(final_message))
        self.wait(3)
        
        # Add performance vs interpretability visualization
        self.show_performance_comparison()
    
    def show_performance_comparison(self):
        """Show a simple performance comparison chart"""
        # Clear previous content
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        # New title
        comp_title = Text("Performance vs Interpretability Trade-off", font_size=36, color=YELLOW).to_edge(UP)
        self.play(Write(comp_title))
        
        # Create bar chart
        models = ["GLMs", "Regularized\nGLMs", "Single\nTrees", "Ensemble\nTrees"]
        performance = [0.6, 0.7, 0.75, 0.95]  # Relative performance scores
        interpretability = [0.9, 0.8, 0.7, 0.3]  # Interpretability scores
        colors = [YELLOW, GOLD, BLUE, ORANGE]
        
        # Create axes for bar chart
        chart_axes = Axes(
            x_range=[-0.5, 3.5, 1],
            y_range=[0, 1, 0.2],
            x_length=8,
            y_length=4,
            axis_config={"include_numbers": False}
        ).shift(DOWN*0.5)
        
        y_label = Text("Score", font_size=20, color=WHITE).next_to(chart_axes, LEFT).rotate(PI/2)
        
        self.play(Create(chart_axes), Write(y_label))
        
        # Create bars
        bar_width = 0.3
        bars_performance = VGroup()
        bars_interpretability = VGroup()
        
        for i, (model, perf, interp, color) in enumerate(zip(models, performance, interpretability, colors)):
            # Performance bars
            perf_bar = Rectangle(
                width=bar_width,
                height=perf * 3.5,
                fill_color=color,
                fill_opacity=0.8,
                stroke_color=color
            ).move_to(chart_axes.c2p(i - 0.15, perf/2))
            
            # Interpretability bars  
            interp_bar = Rectangle(
                width=bar_width,
                height=interp * 3.5,
                fill_color=color,
                fill_opacity=0.4,
                stroke_color=color,
                stroke_width=2
            ).move_to(chart_axes.c2p(i + 0.15, interp/2))
            
            bars_performance.add(perf_bar)
            bars_interpretability.add(interp_bar)
            
            # Model labels
            model_label = Text(model, font_size=16, color=WHITE).next_to(chart_axes.c2p(i, 0), DOWN, buff=0.3)
            self.play(Write(model_label), run_time=0.5)
        
        # Add legend
        legend = VGroup(
            VGroup(Rectangle(width=0.3, height=0.2, fill_color=WHITE, fill_opacity=0.8), 
                   Text("Performance", font_size=16, color=WHITE)).arrange(RIGHT, buff=0.2),
            VGroup(Rectangle(width=0.3, height=0.2, fill_color=WHITE, fill_opacity=0.4, stroke_color=WHITE), 
                   Text("Interpretability", font_size=16, color=WHITE)).arrange(RIGHT, buff=0.2)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=1)
        
        self.play(Create(bars_performance), Create(bars_interpretability), FadeIn(legend))
        
        # Key insight
        insight = Text(
            "The eternal trade-off: Performance vs Interpretability",
            font_size=24,
            color=RED
        ).next_to(chart_axes, DOWN, buff=0.8)
        
        self.play(Write(insight))
        self.wait(3)