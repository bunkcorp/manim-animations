from manim import *
import numpy as np

class RandomForestCombination(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = "#1E1E2A"
        
        # Title
        title = Text("How are base predictions combined in random forests?", font_size=40, color=WHITE, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1.5)
        
        # General Averaging
        avg_text = Text("Average the predictions from all trees", font_size=32, color=YELLOW)
        avg_text.next_to(title, DOWN, buff=1)
        self.play(Write(avg_text))
        self.wait(1)
        
        # Formula
        formula = MathTex(
            r"\hat{f}_{rf}(\mathbf{x}) = \frac{1}{B} \sum_{b=1}^{B} \hat{f}^{*b}(\mathbf{x})",
            font_size=48, color=WHITE
        )
        formula.next_to(avg_text, DOWN, buff=0.5)
        self.play(Write(formula))
        self.wait(2)
        
        # Explanation of formula terms
        f_rf_exp = Text(r"$\hat{f}_{rf}(\mathbf{x})$: Random Forest Prediction", font_size=24, color=BLUE).next_to(formula, DOWN, buff=0.5).align_to(formula, LEFT)
        B_exp = Text(r"$B$: Number of trees", font_size=24, color=BLUE).next_to(f_rf_exp, DOWN, buff=0.2).align_to(formula, LEFT)
        f_star_b_exp = Text(r"$\hat{f}^{*b}(\mathbf{x})$: Prediction from tree $b$", font_size=24, color=BLUE).next_to(B_exp, DOWN, buff=0.2).align_to(formula, LEFT)
        
        self.play(FadeIn(f_rf_exp, shift=UP), FadeIn(B_exp, shift=UP), FadeIn(f_star_b_exp, shift=UP))
        self.wait(3)
        
        self.play(FadeOut(avg_text), FadeOut(formula), FadeOut(f_rf_exp), FadeOut(B_exp), FadeOut(f_star_b_exp))
        self.wait(1)
        
        # Classification Trees
        class_title = Text("Classification trees:", font_size=36, color=GREEN)
        class_title.next_to(title, DOWN, buff=1)
        self.play(Write(class_title))
        self.wait(1)
        
        methods_intro = Text("Two common methods:", font_size=32, color=YELLOW)
        methods_intro.next_to(class_title, DOWN, buff=0.5)
        self.play(Write(methods_intro))
        self.wait(1)
        
        # Method 1
        method1_text = Text("1. Average base probabilities → apply cutoff to assign overall class", font_size=28, color=WHITE)
        method1_text.next_to(methods_intro, DOWN, buff=0.7).align_to(methods_intro, LEFT)
        self.play(Write(method1_text))
        self.wait(2)
        
        # Example for Method 1
        prob_ex_title = Text("Example: Average Probabilities", font_size=24, color=BLUE).next_to(method1_text, DOWN, buff=0.5).align_to(method1_text, LEFT)
        self.play(FadeIn(prob_ex_title))
        
        tree_probs = VGroup(
            Text("Tree 1: P(Class A)=0.8", font_size=20, color=WHITE),
            Text("Tree 2: P(Class A)=0.3", font_size=20, color=WHITE),
            Text("Tree 3: P(Class A)=0.9", font_size=20, color=WHITE)
        ).arrange(DOWN, buff=0.2).next_to(prob_ex_title, DOWN, buff=0.2).align_to(prob_ex_title, LEFT)
        self.play(FadeIn(tree_probs))
        self.wait(1)
        
        avg_prob = Text("Avg P(Class A) = (0.8+0.3+0.9)/3 = 0.66", font_size=20, color=YELLOW).next_to(tree_probs, DOWN, buff=0.3).align_to(tree_probs, LEFT)
        self.play(FadeIn(avg_prob))
        self.wait(1)
        
        cutoff_text = Text("Cutoff (e.g., 0.5) → Assign Class A", font_size=20, color=GREEN).next_to(avg_prob, DOWN, buff=0.3).align_to(avg_prob, LEFT)
        self.play(FadeIn(cutoff_text))
        self.wait(2)
        
        self.play(FadeOut(prob_ex_title), FadeOut(tree_probs), FadeOut(avg_prob), FadeOut(cutoff_text))
        
        # Method 2
        method2_text = Text("2. Majority vote from base class predictions (default)", font_size=28, color=WHITE)
        method2_text.next_to(method1_text, DOWN, buff=1).align_to(method1_text, LEFT)
        self.play(Write(method2_text))
        self.wait(2)
        
        # Example for Method 2
        vote_ex_title = Text("Example: Majority Vote", font_size=24, color=BLUE).next_to(method2_text, DOWN, buff=0.5).align_to(method2_text, LEFT)
        self.play(FadeIn(vote_ex_title))
        
        tree_votes = VGroup(
            Text("Tree 1: Predict Class A", font_size=20, color=WHITE),
            Text("Tree 2: Predict Class B", font_size=20, color=WHITE),
            Text("Tree 3: Predict Class A", font_size=20, color=WHITE)
        ).arrange(DOWN, buff=0.2).next_to(vote_ex_title, DOWN, buff=0.2).align_to(vote_ex_title, LEFT)
        self.play(FadeIn(tree_votes))
        self.wait(1)
        
        final_vote = Text("Result: Class A (2 votes vs 1 vote)", font_size=20, color=GREEN).next_to(tree_votes, DOWN, buff=0.3).align_to(tree_votes, LEFT)
        self.play(FadeIn(final_vote))
        self.wait(2)
        
        self.play(FadeOut(class_title), FadeOut(methods_intro), FadeOut(method1_text), FadeOut(method2_text), FadeOut(vote_ex_title), FadeOut(tree_votes), FadeOut(final_vote))
        self.wait(1)
        
        final_summary = Text("Random Forests combine predictions for robust results!", font_size=36, color=YELLOW)
        self.play(Write(final_summary))
        self.wait(2)
        self.play(FadeOut(final_summary), FadeOut(title))
