from manim import *
import numpy as np

# --- Configuration ---
CONFIG = {
    "colors": {
        "background": "#2F2F2F",  # Dark grey background
        "primary_text": WHITE,
        "secondary_text": LIGHT_GREY,
        "random_forest_color": BLUE,
        "boosting_color": RED,
        "highlight_color": YELLOW,
        "table_header_color": WHITE,
    },
    "font_sizes": {
        "title": 48,
        "header": 36,
        "text": 28,
        "table_text": 24,
        "small_text": 20,
    },
}

class RandomForestVsBoostingComparison(Scene):
    def construct(self):
        self.camera.background_color = CONFIG["colors"]["background"]
        self.show_intro()
        self.show_question()
        self.show_blank_table()
        self.show_filled_table()
        self.show_visual_examples()
        self.show_summary()

    def show_intro(self):
        # Title
        title = Text("Random Forest vs Boosting", 
                    font_size=CONFIG["font_sizes"]["title"], 
                    color=CONFIG["colors"]["primary_text"])
        title.to_edge(UP, buff=0.5)
        
        # Subtitle
        subtitle = Text("Ensemble Methods Comparison", 
                       font_size=CONFIG["font_sizes"]["text"], 
                       color=CONFIG["colors"]["secondary_text"])
        subtitle.next_to(title, DOWN, buff=0.3)
        
        self.play(Write(title))
        self.play(Write(subtitle))
        self.wait(2)
        
        # Fade out intro
        self.play(FadeOut(VGroup(title, subtitle)))
        self.wait(1)

    def show_question(self):
        # Question
        question = Text("How do random forests and boosted trees compare across key characteristics?", 
                       font_size=CONFIG["font_sizes"]["header"], 
                       color=CONFIG["colors"]["primary_text"])
        question.move_to(UP * 2)
        question.scale(0.8)
        
        self.play(Write(question))
        self.wait(2)
        
        # Fade out question
        self.play(FadeOut(question))
        self.wait(1)

    def show_blank_table(self):
        # Table title
        table_title = Text("Comparison Table", 
                          font_size=CONFIG["font_sizes"]["header"], 
                          color=CONFIG["colors"]["primary_text"])
        table_title.to_edge(UP, buff=0.5)
        
        # Create table structure
        headers = ["Item", "Random Forest", "Boosting"]
        items = ["Fitting process", "Focus", "Overfitting", "Hyperparameter tuning"]
        
        # Create table
        table = self.create_comparison_table(headers, items, filled=False)
        table.next_to(table_title, DOWN, buff=0.5)
        
        self.play(Write(table_title))
        self.play(Create(table))
        self.wait(2)
        
        # Fade out blank table
        self.play(FadeOut(VGroup(table_title, table)))
        self.wait(1)

    def show_filled_table(self):
        # Table title
        table_title = Text("Comparison Results", 
                          font_size=CONFIG["font_sizes"]["header"], 
                          color=CONFIG["colors"]["primary_text"])
        table_title.to_edge(UP, buff=0.5)
        
        # Create filled table
        headers = ["Item", "Random Forest", "Boosting"]
        items = ["Fitting process", "Focus", "Overfitting", "Hyperparameter tuning"]
        
        # Answers for each item
        answers = {
            "Fitting process": {
                "Random Forest": "In parallel",
                "Boosting": "In series (sequential)"
            },
            "Focus": {
                "Random Forest": "Variance",
                "Boosting": "Bias"
            },
            "Overfitting": {
                "Random Forest": "Less vulnerable",
                "Boosting": "More vulnerable"
            },
            "Hyperparameter tuning": {
                "Random Forest": "Less sensitive",
                "Boosting": "More sensitive"
            }
        }
        
        # Create filled table
        table = self.create_filled_comparison_table(headers, items, answers)
        table.next_to(table_title, DOWN, buff=0.5)
        
        self.play(Write(table_title))
        self.play(Create(table))
        self.wait(3)
        
        # Fade out filled table
        self.play(FadeOut(VGroup(table_title, table)))
        self.wait(1)

    def show_visual_examples(self):
        # Section title
        section_title = Text("Visual Examples", 
                            font_size=CONFIG["font_sizes"]["header"], 
                            color=CONFIG["colors"]["primary_text"])
        section_title.to_edge(UP, buff=0.5)
        
        # Random Forest Example
        rf_title = Text("Random Forest: Parallel Fitting", 
                       font_size=CONFIG["font_sizes"]["text"], 
                       color=CONFIG["colors"]["random_forest_color"])
        rf_title.move_to(UP * 1.5 + LEFT * 3)
        
        # Create multiple trees for RF
        rf_trees = VGroup()
        for i in range(5):
            tree = self.create_simple_tree()
            tree.scale(0.3)
            tree.move_to(UP * 0.5 + LEFT * 3 + RIGHT * (i - 2) * 1.2)
            rf_trees.add(tree)
        
        # Add parallel arrows
        parallel_arrows = VGroup()
        for i in range(4):
            arrow = Arrow(LEFT * 0.5, RIGHT * 0.5, color=CONFIG["colors"]["random_forest_color"])
            arrow.move_to(UP * 0.5 + LEFT * 3 + RIGHT * (i - 1.5) * 1.2)
            parallel_arrows.add(arrow)
        
        # Boosting Example
        boost_title = Text("Boosting: Sequential Fitting", 
                          font_size=CONFIG["font_sizes"]["text"], 
                          color=CONFIG["colors"]["boosting_color"])
        boost_title.move_to(UP * 1.5 + RIGHT * 3)
        
        # Create sequential trees for boosting
        boost_trees = VGroup()
        for i in range(4):
            tree = self.create_simple_tree()
            tree.scale(0.3)
            tree.move_to(UP * 0.5 + RIGHT * 3 + RIGHT * (i - 1.5) * 1.5)
            boost_trees.add(tree)
        
        # Add sequential arrows
        sequential_arrows = VGroup()
        for i in range(3):
            arrow = Arrow(LEFT * 0.5, RIGHT * 0.5, color=CONFIG["colors"]["boosting_color"])
            arrow.move_to(UP * 0.5 + RIGHT * 3 + RIGHT * (i - 1) * 1.5)
            sequential_arrows.add(arrow)
        
        self.play(Write(section_title))
        self.play(Write(rf_title))
        self.play(FadeIn(rf_trees))
        self.play(Create(parallel_arrows))
        
        self.play(Write(boost_title))
        self.play(FadeIn(boost_trees))
        self.play(Create(sequential_arrows))
        
        self.wait(2)
        
        # Show ensemble predictions
        ensemble_title = Text("Ensemble Predictions", 
                             font_size=CONFIG["font_sizes"]["text"], 
                             color=CONFIG["colors"]["highlight_color"])
        ensemble_title.move_to(DOWN * 0.5)
        
        # RF ensemble (average)
        rf_ensemble = VGroup(
            Text("Random Forest:", font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["random_forest_color"]),
            MathTex(r"\text{Prediction} = \frac{1}{n}\sum_{i=1}^{n} T_i", color=CONFIG["colors"]["random_forest_color"])
        ).arrange(DOWN, buff=0.2)
        rf_ensemble.move_to(DOWN * 1.5 + LEFT * 3)
        
        # Boosting ensemble (weighted sum)
        boost_ensemble = VGroup(
            Text("Boosting:", font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["boosting_color"]),
            MathTex(r"\text{Prediction} = \sum_{i=1}^{n} \alpha_i T_i", color=CONFIG["colors"]["boosting_color"])
        ).arrange(DOWN, buff=0.2)
        boost_ensemble.move_to(DOWN * 1.5 + RIGHT * 3)
        
        self.play(Write(ensemble_title))
        self.play(Write(rf_ensemble))
        self.play(Write(boost_ensemble))
        self.wait(3)
        
        # Fade out visual examples
        self.play(FadeOut(VGroup(
            section_title, rf_title, rf_trees, parallel_arrows, boost_title, boost_trees, sequential_arrows,
            ensemble_title, rf_ensemble, boost_ensemble
        )))
        self.wait(1)

    def show_summary(self):
        # Summary title
        summary_title = Text("Key Takeaways", 
                            font_size=CONFIG["font_sizes"]["header"], 
                            color=CONFIG["colors"]["primary_text"])
        summary_title.to_edge(UP, buff=0.5)
        
        # Key points
        key_points = VGroup(
            Text("🎯 Random Forest: Reduces variance through parallel training", 
                font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["random_forest_color"]),
            Text("🚀 Boosting: Reduces bias through sequential training", 
                font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["boosting_color"]),
            Text("🛡️ Random Forest: More robust to overfitting", 
                font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["random_forest_color"]),
            Text("⚙️ Boosting: Requires careful hyperparameter tuning", 
                font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["boosting_color"]),
            Text("📊 Choose based on your data and problem characteristics", 
                font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["highlight_color"])
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        key_points.move_to(ORIGIN)
        
        self.play(Write(summary_title))
        self.play(Write(key_points))
        self.wait(4)
        
        # Final message
        final_message = Text("Both methods are powerful ensemble techniques with different strengths!", 
                           font_size=CONFIG["font_sizes"]["text"], 
                           color=CONFIG["colors"]["highlight_color"])
        final_message.move_to(DOWN * 3)
        
        self.play(Write(final_message))
        self.wait(3)
        
        # Fade out everything
        self.play(FadeOut(VGroup(summary_title, key_points, final_message)))
        self.wait(1)

    def create_comparison_table(self, headers, items, filled=False):
        """Create a comparison table with headers and items"""
        # Create table structure
        table = VGroup()
        
        # Headers
        header_row = VGroup()
        for i, header in enumerate(headers):
            header_text = Text(header, font_size=CONFIG["font_sizes"]["table_text"], 
                             color=CONFIG["colors"]["table_header_color"])
            if i == 0:
                header_text.move_to(LEFT * 4)
            elif i == 1:
                header_text.move_to(ORIGIN)
            else:
                header_text.move_to(RIGHT * 4)
            header_row.add(header_text)
        
        # Underline headers
        for header in header_row:
            underline = Line(header.get_left() + DOWN * 0.1, header.get_right() + DOWN * 0.1, 
                           color=CONFIG["colors"]["table_header_color"])
            header_row.add(underline)
        
        table.add(header_row)
        
        # Items and checkboxes
        for i, item in enumerate(items):
            item_text = Text(item, font_size=CONFIG["font_sizes"]["table_text"], 
                           color=CONFIG["colors"]["primary_text"])
            item_text.move_to(LEFT * 4 + DOWN * (i + 1) * 0.8)
            
            # Checkboxes for Random Forest and Boosting columns
            rf_checkbox = Square(side_length=0.3, color=CONFIG["colors"]["primary_text"])
            rf_checkbox.move_to(ORIGIN + DOWN * (i + 1) * 0.8)
            
            boost_checkbox = Square(side_length=0.3, color=CONFIG["colors"]["primary_text"])
            boost_checkbox.move_to(RIGHT * 4 + DOWN * (i + 1) * 0.8)
            
            row = VGroup(item_text, rf_checkbox, boost_checkbox)
            table.add(row)
        
        return table

    def create_filled_comparison_table(self, headers, items, answers):
        """Create a filled comparison table with answers"""
        # Create table structure
        table = VGroup()
        
        # Headers
        header_row = VGroup()
        for i, header in enumerate(headers):
            header_text = Text(header, font_size=CONFIG["font_sizes"]["table_text"], 
                             color=CONFIG["colors"]["table_header_color"])
            if i == 0:
                header_text.move_to(LEFT * 4)
            elif i == 1:
                header_text.move_to(ORIGIN)
            else:
                header_text.move_to(RIGHT * 4)
            header_row.add(header_text)
        
        # Underline headers
        for header in header_row:
            underline = Line(header.get_left() + DOWN * 0.1, header.get_right() + DOWN * 0.1, 
                           color=CONFIG["colors"]["table_header_color"])
            header_row.add(underline)
        
        table.add(header_row)
        
        # Items and answers
        for i, item in enumerate(items):
            item_text = Text(item, font_size=CONFIG["font_sizes"]["table_text"], 
                           color=CONFIG["colors"]["primary_text"])
            item_text.move_to(LEFT * 4 + DOWN * (i + 1) * 0.8)
            
            # Answers
            rf_answer = Text(answers[item]["Random Forest"], font_size=CONFIG["font_sizes"]["table_text"], 
                           color=CONFIG["colors"]["random_forest_color"])
            rf_answer.move_to(ORIGIN + DOWN * (i + 1) * 0.8)
            
            boost_answer = Text(answers[item]["Boosting"], font_size=CONFIG["font_sizes"]["table_text"], 
                              color=CONFIG["colors"]["boosting_color"])
            boost_answer.move_to(RIGHT * 4 + DOWN * (i + 1) * 0.8)
            
            row = VGroup(item_text, rf_answer, boost_answer)
            table.add(row)
        
        return table

    def create_simple_tree(self):
        """Create a simple decision tree visualization"""
        # Root node
        root = Circle(radius=0.2, color=CONFIG["colors"]["primary_text"], fill_opacity=0.3)
        root_text = Text("?", font_size=CONFIG["font_sizes"]["small_text"], color=WHITE)
        root_text.move_to(root)
        
        # Left child
        left_child = Circle(radius=0.15, color=CONFIG["colors"]["primary_text"], fill_opacity=0.3)
        left_child.move_to(root.get_center() + LEFT * 0.8 + DOWN * 0.6)
        left_text = Text("Yes", font_size=CONFIG["font_sizes"]["small_text"], color=WHITE)
        left_text.move_to(left_child)
        
        # Right child
        right_child = Circle(radius=0.15, color=CONFIG["colors"]["primary_text"], fill_opacity=0.3)
        right_child.move_to(root.get_center() + RIGHT * 0.8 + DOWN * 0.6)
        right_text = Text("No", font_size=CONFIG["font_sizes"]["small_text"], color=WHITE)
        right_text.move_to(right_child)
        
        # Edges
        left_edge = Line(root.get_center(), left_child.get_center(), color=CONFIG["colors"]["primary_text"])
        right_edge = Line(root.get_center(), right_child.get_center(), color=CONFIG["colors"]["primary_text"])
        
        return VGroup(root, root_text, left_child, left_text, right_child, right_text, left_edge, right_edge)
