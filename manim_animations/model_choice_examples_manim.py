#!/usr/bin/env python3
"""
Model Choice GLM vs Trees Examples Animation
Shows specific examples of when to choose different modeling approaches
"""

from manim import *
import numpy as np

class ModelChoiceGLMvsTreesExamples(Scene):
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Show intro
        self.show_intro()
        
        # Create axes
        self.create_axes()
        
        # Create model cards with examples
        self.create_model_cards()
        
        # Show guided highlights
        self.show_guided_highlights()
        
        # Show practical examples
        self.show_practical_examples()
        
        # Show closing summary
        self.show_closing_summary()
    
    def show_intro(self):
        """Introduction with enhanced title"""
        title = Text(
            "When to choose GLMs, Regularized GLMs, Single Trees, or Ensemble Trees?",
            font_size=32,
            color=WHITE
        ).to_edge(UP)
        
        subtitle = Text(
            "Real-world examples and decision framework",
            font_size=24,
            color=LIGHT_GRAY
        ).next_to(title, DOWN, buff=0.3)
        
        self.play(FadeIn(title), FadeIn(subtitle))
        self.wait(2)
        
        self.title = title
        self.subtitle = subtitle
    
    def create_axes(self):
        """Create interpretability vs complexity axes"""
        origin = LEFT*5.5 + DOWN*2.5
        
        # Axes
        x_axis = Arrow(origin, origin + RIGHT*11, color=WHITE, stroke_width=4, max_tip_length_to_length_ratio=0.03)
        y_axis = Arrow(origin, origin + UP*5, color=WHITE, stroke_width=4, max_tip_length_to_length_ratio=0.03)
        
        # Labels
        x_label = Text("Predictive Power / Complexity →", font_size=24, color=WHITE).next_to(x_axis, DOWN, buff=0.3)
        y_label = Text("Interpretability ↑", font_size=24, color=WHITE).rotate(PI/2).next_to(y_axis, LEFT, buff=0.3)
        speed_note = Text("(speed ↓ as you move right)", font_size=18, color=GRAY).next_to(x_label, DOWN, buff=0.1)
        
        self.play(Create(x_axis), Create(y_axis))
        self.play(Write(x_label), Write(y_label), FadeIn(speed_note))
        self.wait(1)
        
        self.origin = origin
    
    def create_model_card(self, title_text, bullets, color=WHITE, width=5.0, height=2.8):
        """Create enhanced model cards with examples"""
        # Card background with gradient effect
        box = RoundedRectangle(
            corner_radius=0.2,
            width=width,
            height=height,
            stroke_color=color,
            stroke_width=3,
            fill_color=color,
            fill_opacity=0.1
        )
        
        # Title with emphasis
        title = Text(title_text, font_size=28, color=color, weight=BOLD)
        
        # Bullet points with better formatting
        bullet_lines = VGroup()
        for bullet in bullets:
            bullet_text = Text(f"• {bullet}", font_size=20, color=WHITE)
            bullet_lines.add(bullet_text)
        
        bullet_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        
        # Arrange content with better spacing
        content = VGroup(title, bullet_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        content.move_to(box.get_center())
        
        return VGroup(box, content)
    
    def create_model_cards(self):
        """Create all model cards with specific examples"""
        # GLMs card
        glm_card = self.create_model_card(
            "GLMs",
            [
                "Interpretability & known target distribution",
                "Examples: Linear (Normal), Logistic (Binomial), Poisson",
                "Use case: Medical diagnosis, A/B testing"
            ],
            color=YELLOW
        )
        
        # Regularized GLMs card
        reg_glm_card = self.create_model_card(
            "Regularized GLMs",
            [
                "Automatic variable selection + shrinkage", 
                "Examples: Lasso/L1, Ridge/L2, Elastic Net",
                "Use case: High-dimensional data, genomics"
            ],
            color=GOLD
        )
        
        # Single Trees card
        tree_card = self.create_model_card(
            "Single Trees",
            [
                "Rule paths are easy to explain",
                "Captures nonlinearity & interactions",
                "Use case: Credit scoring, clinical decisions"
            ],
            color=BLUE
        )
        
        # Ensemble Trees card
        ens_card = self.create_model_card(
            "Ensemble Trees",
            [
                "Highest accuracy (usually), less interpretable",
                "Examples: Random Forest, XGBoost, LightGBM",
                "Use case: Kaggle competitions, complex prediction"
            ],
            color=ORANGE
        )
        
        # Position cards on the interpretability-complexity map
        glm_card.move_to(LEFT*2.8 + UP*1.5)        # High interpretability, low complexity
        reg_glm_card.move_to(RIGHT*0.3 + UP*1.1)   # Moderate interpretability, moderate complexity
        tree_card.move_to(LEFT*0.8 + DOWN*0.3)     # Moderate interpretability, moderate complexity
        ens_card.move_to(RIGHT*3.1 + DOWN*1.3)     # Low interpretability, high complexity
        
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
    
    def highlight_model(self, card, description, color):
        """Highlight a specific model with description"""
        # Footer description
        footer = Text(description, font_size=28, color=WHITE).to_edge(DOWN, buff=0.6)
        self.play(Write(footer))
        
        # Highlight effect
        glow = SurroundingRectangle(card, color=color, buff=0.15, stroke_width=8)
        checkmark = Text("✓", font_size=48, color=color).next_to(card, UP, buff=0.3)
        
        self.play(Create(glow), FadeIn(checkmark, scale=0.8))
        self.wait(2)
        self.play(FadeOut(glow), FadeOut(checkmark), FadeOut(footer))
    
    def show_guided_highlights(self):
        """Show guided highlights for each model type"""
        self.highlight_model(
            self.glm_card,
            "Use GLMs when interpretability matters and target distribution is known",
            YELLOW
        )
        
        self.highlight_model(
            self.reg_glm_card,
            "Use regularized GLMs for automatic variable selection and regularization",
            GOLD
        )
        
        self.highlight_model(
            self.tree_card,
            "Use single trees for simple, explainable rules with complex relations",
            BLUE
        )
        
        self.highlight_model(
            self.ens_card,
            "Use ensemble trees for top accuracy (RF/GBM/XGBoost), trading speed & interpretability",
            ORANGE
        )
    
    def show_practical_examples(self):
        """Show specific practical examples"""
        examples_title = Text("Practical Examples", font_size=36, color=YELLOW, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.title, examples_title))
        
        # Create example scenarios
        scenarios = [
            {
                "title": "Medical Diagnosis",
                "description": "Need to explain why a patient has high risk",
                "recommendation": "GLM (Logistic Regression)",
                "reason": "Doctors need interpretable coefficients",
                "color": YELLOW
            },
            {
                "title": "Gene Expression Analysis", 
                "description": "10,000+ features, need feature selection",
                "recommendation": "Regularized GLM (Lasso)",
                "reason": "Automatic feature selection with L1 penalty",
                "color": GOLD
            },
            {
                "title": "Credit Scoring",
                "description": "Need simple rules for loan approval",
                "recommendation": "Single Decision Tree",
                "reason": "Clear if-then rules for decision making",
                "color": BLUE
            },
            {
                "title": "Kaggle Competition",
                "description": "Only care about prediction accuracy",
                "recommendation": "Ensemble Trees (XGBoost)",
                "reason": "Maximum predictive performance",
                "color": ORANGE
            }
        ]
        
        # Show scenarios one by one
        for i, scenario in enumerate(scenarios):
            scenario_box = self.create_scenario_box(scenario)
            scenario_box.move_to(ORIGIN)
            
            self.play(FadeIn(scenario_box))
            self.wait(3)
            self.play(FadeOut(scenario_box))
    
    def create_scenario_box(self, scenario):
        """Create a scenario example box"""
        box = RoundedRectangle(
            corner_radius=0.3,
            width=10,
            height=6,
            stroke_color=scenario["color"],
            stroke_width=3,
            fill_color=scenario["color"],
            fill_opacity=0.1
        )
        
        title = Text(scenario["title"], font_size=32, color=scenario["color"], weight=BOLD)
        description = Text(scenario["description"], font_size=24, color=WHITE)
        recommendation = Text(f"Recommended: {scenario['recommendation']}", font_size=28, color=GREEN, weight=BOLD)
        reason = Text(f"Why: {scenario['reason']}", font_size=22, color=LIGHT_GRAY)
        
        content = VGroup(title, description, recommendation, reason).arrange(DOWN, buff=0.5)
        content.move_to(box.get_center())
        
        return VGroup(box, content)
    
    def show_closing_summary(self):
        """Show closing summary with cheat sheet"""
        # Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        summary_title = Text("Quick Decision Guide", font_size=40, color=YELLOW, weight=BOLD).to_edge(UP)
        self.play(Write(summary_title))
        
        # Create summary points
        summary_points = VGroup(
            Text("GLMs → interpretability, known distribution", font_size=24, color=YELLOW),
            Text("Regularized GLMs → auto selection + shrinkage (L1/L2/EN)", font_size=24, color=GOLD),
            Text("Single Trees → clear rules; nonlinearity & interactions", font_size=24, color=BLUE),
            Text("Ensemble Trees → best accuracy; slower & less interpretable", font_size=24, color=ORANGE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(UP*0.5)
        
        # Animate summary points
        for point in summary_points:
            self.play(Write(point))
            self.wait(0.8)
        
        # Add decision flowchart
        flowchart_title = Text("Decision Flowchart:", font_size=28, color=WHITE, weight=BOLD).next_to(summary_points, DOWN, buff=1)
        
        flowchart_steps = VGroup(
            Text("1. Interpretability required? → GLMs or Single Trees", font_size=20, color=WHITE),
            Text("2. Many features (p > n)? → Regularized GLMs", font_size=20, color=WHITE),
            Text("3. Complex nonlinear patterns? → Trees", font_size=20, color=WHITE), 
            Text("4. Maximum accuracy needed? → Ensemble Trees", font_size=20, color=WHITE),
            Text("5. Fast inference required? → GLMs or Single Trees", font_size=20, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(flowchart_title, DOWN, buff=0.3)
        
        self.play(Write(flowchart_title))
        for step in flowchart_steps:
            self.play(Write(step))
            self.wait(0.5)
        
        # Final message with emphasis
        final_message = Text(
            "Remember: The best model depends on your specific problem constraints!",
            font_size=26,
            color=GREEN,
            weight=BOLD
        ).next_to(flowchart_steps, DOWN, buff=1)
        
        self.play(Write(final_message))
        self.wait(3)
        
        # Add algorithm examples
        self.show_algorithm_examples()
    
    def show_algorithm_examples(self):
        """Show specific algorithm examples"""
        algo_title = Text("Common Algorithm Examples", font_size=32, color=CYAN, weight=BOLD).to_edge(UP)
        self.play(Transform(self.mobjects[0], algo_title))
        
        # Clear other content
        self.play(*[FadeOut(mob) for mob in self.mobjects[1:]])
        
        # Algorithm categories
        categories = [
            {
                "title": "GLMs",
                "algorithms": ["Linear Regression", "Logistic Regression", "Poisson Regression", "Gamma GLM"],
                "color": YELLOW
            },
            {
                "title": "Regularized GLMs", 
                "algorithms": ["Lasso (L1)", "Ridge (L2)", "Elastic Net", "Group Lasso"],
                "color": GOLD
            },
            {
                "title": "Single Trees",
                "algorithms": ["CART", "C4.5", "ID3", "CHAID"],
                "color": BLUE
            },
            {
                "title": "Ensemble Trees",
                "algorithms": ["Random Forest", "XGBoost", "LightGBM", "CatBoost", "AdaBoost"],
                "color": ORANGE
            }
        ]
        
        # Position categories in 2x2 grid
        positions = [UP*1.5 + LEFT*3, UP*1.5 + RIGHT*3, DOWN*1.5 + LEFT*3, DOWN*1.5 + RIGHT*3]
        
        for category, pos in zip(categories, positions):
            category_box = self.create_algorithm_box(category)
            category_box.move_to(pos)
            self.play(FadeIn(category_box))
            self.wait(1)
        
        self.wait(2)
    
    def create_algorithm_box(self, category):
        """Create algorithm category box"""
        box = RoundedRectangle(
            corner_radius=0.2,
            width=4.5,
            height=3,
            stroke_color=category["color"],
            stroke_width=2,
            fill_color=category["color"],
            fill_opacity=0.1
        )
        
        title = Text(category["title"], font_size=24, color=category["color"], weight=BOLD)
        
        algorithms = VGroup()
        for algo in category["algorithms"]:
            algo_text = Text(f"• {algo}", font_size=18, color=WHITE)
            algorithms.add(algo_text)
        
        algorithms.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        
        content = VGroup(title, algorithms).arrange(DOWN, buff=0.3)
        content.move_to(box.get_center())
        
        return VGroup(box, content)