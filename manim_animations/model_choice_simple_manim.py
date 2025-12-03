#!/usr/bin/env python3
"""
Model Choice GLM vs Trees Examples - Simplified Animation
Shows when to choose different modeling approaches with examples
"""

from manim import *

class ModelChoiceSimple(Scene):
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Title
        title = Text(
            "When to choose GLMs, Regularized GLMs, Single Trees, or Ensemble Trees?",
            font_size=28,
            color=WHITE
        ).to_edge(UP)
        self.play(FadeIn(title))
        self.wait(1)
        
        # Create interpretability vs complexity axes
        self.create_axes()
        
        # Create and position model cards
        self.create_model_cards()
        
        # Show scenario examples
        self.show_examples()
        
        # Final summary
        self.show_summary()
    
    def create_axes(self):
        """Create the trade-off axes"""
        # Axes
        x_axis = Arrow(LEFT*5.5 + DOWN*2.5, RIGHT*5.5 + DOWN*2.5, 
                      color=WHITE, stroke_width=3, max_tip_length_to_length_ratio=0.03)
        y_axis = Arrow(LEFT*5.5 + DOWN*2.5, LEFT*5.5 + UP*2.5, 
                      color=WHITE, stroke_width=3, max_tip_length_to_length_ratio=0.03)
        
        # Labels
        x_label = Text("Predictive Power / Complexity →", font_size=20, color=WHITE)\
            .next_to(x_axis, DOWN, buff=0.3)
        y_label = Text("Interpretability ↑", font_size=20, color=WHITE)\
            .rotate(PI/2).next_to(y_axis, LEFT, buff=0.3)
        
        self.play(Create(x_axis), Create(y_axis))
        self.play(Write(x_label), Write(y_label))
        self.wait(1)
    
    def create_model_cards(self):
        """Create model cards with examples"""
        # GLMs
        glm_card = self.create_card(
            "GLMs",
            ["Interpretable coefficients", "Linear/Logistic regression", "Medical diagnosis"],
            YELLOW
        ).move_to(LEFT*3 + UP*1.5)
        
        # Regularized GLMs  
        reg_glm_card = self.create_card(
            "Regularized GLMs",
            ["Feature selection", "Lasso/Ridge/Elastic Net", "High-dimensional data"],
            GOLD
        ).move_to(RIGHT*0.5 + UP*1)
        
        # Single Trees
        tree_card = self.create_card(
            "Single Trees",
            ["Simple rules", "CART/C4.5", "Credit scoring"],
            BLUE
        ).move_to(LEFT*1 + DOWN*0.5)
        
        # Ensemble Trees
        ens_card = self.create_card(
            "Ensemble Trees", 
            ["High accuracy", "Random Forest/XGBoost", "Competitions"],
            ORANGE
        ).move_to(RIGHT*3 + DOWN*1.5)
        
        # Show cards
        cards = [glm_card, reg_glm_card, tree_card, ens_card]
        self.play(*[FadeIn(card, shift=UP*0.5) for card in cards])
        
        # Add connecting arrows
        arrow1 = Arrow(glm_card.get_right(), reg_glm_card.get_left(), 
                      color=GRAY, stroke_width=2, max_tip_length_to_length_ratio=0.1)
        arrow2 = Arrow(tree_card.get_right(), ens_card.get_left(),
                      color=GRAY, stroke_width=2, max_tip_length_to_length_ratio=0.1)
        
        self.play(GrowArrow(arrow1), GrowArrow(arrow2))
        self.wait(2)
        
        self.cards = cards
    
    def create_card(self, title, bullets, color):
        """Create a model card"""
        # Background
        box = RoundedRectangle(
            corner_radius=0.2,
            width=4,
            height=2.5,
            stroke_color=color,
            stroke_width=2,
            fill_color=color,
            fill_opacity=0.1
        )
        
        # Title
        title_text = Text(title, font_size=22, color=color, weight=BOLD)
        
        # Bullet points
        bullet_group = VGroup()
        for bullet in bullets:
            bullet_text = Text(f"• {bullet}", font_size=16, color=WHITE)
            bullet_group.add(bullet_text)
        
        bullet_group.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        
        # Arrange content
        content = VGroup(title_text, bullet_group).arrange(DOWN, buff=0.2)
        content.move_to(box.get_center())
        
        return VGroup(box, content)
    
    def show_examples(self):
        """Show practical examples"""
        examples = [
            {
                "title": "Medical Diagnosis",
                "description": "Doctor needs to explain risk factors",
                "choice": "GLM (Logistic Regression)",
                "color": YELLOW
            },
            {
                "title": "Gene Analysis",
                "description": "10,000+ genes, need feature selection", 
                "choice": "Regularized GLM (Lasso)",
                "color": GOLD
            },
            {
                "title": "Loan Approval",
                "description": "Simple rules for decisions",
                "choice": "Single Decision Tree",
                "color": BLUE
            },
            {
                "title": "Kaggle Contest",
                "description": "Only accuracy matters",
                "choice": "Ensemble (XGBoost)",
                "color": ORANGE
            }
        ]
        
        for i, example in enumerate(examples):
            # Highlight corresponding card
            card = self.cards[i]
            glow = SurroundingRectangle(card, color=example["color"], buff=0.1, stroke_width=6)
            
            # Show example
            example_text = VGroup(
                Text(f"Example: {example['title']}", font_size=24, color=example["color"], weight=BOLD),
                Text(example["description"], font_size=20, color=WHITE),
                Text(f"→ {example['choice']}", font_size=22, color=GREEN, weight=BOLD)
            ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=1)
            
            self.play(Create(glow), FadeIn(example_text))
            self.wait(3)
            self.play(FadeOut(glow), FadeOut(example_text))
    
    def show_summary(self):
        """Show final summary"""
        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        # Summary title
        summary_title = Text("Quick Decision Guide", font_size=36, color=YELLOW, weight=BOLD).to_edge(UP)
        self.play(Write(summary_title))
        
        # Summary points
        points = [
            ("GLMs", "interpretability + known distributions", YELLOW),
            ("Regularized GLMs", "feature selection + regularization", GOLD),
            ("Single Trees", "simple rules + nonlinear patterns", BLUE),
            ("Ensemble Trees", "maximum accuracy (less interpretable)", ORANGE)
        ]
        
        summary_group = VGroup()
        for model, description, color in points:
            point_text = Text(f"{model} → {description}", font_size=24, color=color)
            summary_group.add(point_text)
        
        summary_group.arrange(DOWN, aligned_edge=LEFT, buff=0.5).shift(UP*0.5)
        
        for point in summary_group:
            self.play(Write(point))
            self.wait(0.8)
        
        # Final message
        final_msg = Text(
            "Choose based on your priorities: interpretability vs accuracy!",
            font_size=24,
            color=GREEN,
            weight=BOLD
        ).next_to(summary_group, DOWN, buff=1)
        
        self.play(Write(final_msg))
        self.wait(3)