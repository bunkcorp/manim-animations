from manim import *
import numpy as np

# --- Configuration ---
CONFIG = {
    "colors": {
        "background": "#2F2F2F",  # Dark grey background
        "primary_text": WHITE,
        "secondary_text": LIGHT_GREY,
        "parameter_color": BLUE,
        "r_name_color": GREEN,
        "meaning_color": YELLOW,
        "effect_color": ORANGE,
        "highlight_color": RED,
        "tree_color": PURPLE,
    },
    "font_sizes": {
        "title": 48,
        "header": 36,
        "text": 28,
        "table_text": 24,
        "small_text": 20,
    },
}

class TreeComplexityParametersAnimation(Scene):
    def construct(self):
        self.camera.background_color = CONFIG["colors"]["background"]
        self.show_intro()
        self.show_question()
        self.show_blank_table()
        self.show_filled_table()
        self.show_parameter_explanations()
        self.show_tree_visualizations()
        self.show_notes()
        self.show_summary()

    def show_intro(self):
        # Title
        title = Text("Tree Complexity Parameters in R", 
                    font_size=CONFIG["font_sizes"]["title"], 
                    color=CONFIG["colors"]["primary_text"])
        title.to_edge(UP, buff=0.5)
        
        # Subtitle
        subtitle = Text("Understanding Decision Tree Hyperparameters", 
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
        question = Text("What are common tree complexity parameters in R, and how do they affect the tree?", 
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
        table_title = Text("Parameters to Learn", 
                          font_size=CONFIG["font_sizes"]["header"], 
                          color=CONFIG["colors"]["primary_text"])
        table_title.to_edge(UP, buff=0.5)
        
        # Create blank table
        headers = ["Parameter", "Name in R", "Meaning", "Effect"]
        parameters = ["Minimum bucket size", "Complexity parameter", "Maximum depth"]
        
        table = self.create_blank_table(headers, parameters)
        table.next_to(table_title, DOWN, buff=0.5)
        
        self.play(Write(table_title))
        self.play(Create(table))
        self.wait(2)
        
        # Fade out blank table
        self.play(FadeOut(VGroup(table_title, table)))
        self.wait(1)

    def show_filled_table(self):
        # Table title
        table_title = Text("Tree Complexity Parameters", 
                          font_size=CONFIG["font_sizes"]["header"], 
                          color=CONFIG["colors"]["primary_text"])
        table_title.to_edge(UP, buff=0.5)
        
        # Create filled table
        headers = ["Parameter", "Name in R", "Meaning", "Effect"]
        parameters = ["Minimum bucket size", "Complexity parameter", "Maximum depth"]
        
        # Answers for each parameter
        answers = {
            "Minimum bucket size": {
                "r_name": "minbucket",
                "meaning": "Minimum # of observations in a terminal node",
                "effect": "Higher ⇒ simpler tree"
            },
            "Complexity parameter": {
                "r_name": "cp",
                "meaning": "Minimum improvement in model fit to allow a split",
                "effect": "Higher ⇒ less complex tree"
            },
            "Maximum depth": {
                "r_name": "maxdepth",
                "meaning": "# edges from root to furthest node",
                "effect": "Higher ⇒ more complex tree"
            }
        }
        
        # Create filled table
        table = self.create_filled_table(headers, parameters, answers)
        table.next_to(table_title, DOWN, buff=0.5)
        
        self.play(Write(table_title))
        self.play(Create(table))
        self.wait(3)
        
        # Fade out filled table
        self.play(FadeOut(VGroup(table_title, table)))
        self.wait(1)

    def show_parameter_explanations(self):
        # Section title
        section_title = Text("Parameter Explanations", 
                           font_size=CONFIG["font_sizes"]["header"], 
                           color=CONFIG["colors"]["primary_text"])
        section_title.to_edge(UP, buff=0.5)
        
        # Parameter 1: minbucket
        minbucket_title = Text("1. minbucket", font_size=CONFIG["font_sizes"]["text"], 
                             color=CONFIG["colors"]["parameter_color"])
        minbucket_title.move_to(UP * 1.5)
        
        minbucket_explanation = VGroup(
            Text("• Controls minimum observations in terminal nodes", 
                font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["primary_text"]),
            Text("• Higher values prevent overfitting", 
                font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["primary_text"]),
            Text("• Must be tuned manually (trial and error)", 
                font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["highlight_color"])
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        minbucket_explanation.move_to(UP * 0.8)
        
        self.play(Write(section_title))
        self.play(Write(minbucket_title))
        self.play(Write(minbucket_explanation))
        self.wait(2)
        
        # Parameter 2: cp
        cp_title = Text("2. cp (Complexity Parameter)", font_size=CONFIG["font_sizes"]["text"], 
                       color=CONFIG["colors"]["parameter_color"])
        cp_title.move_to(UP * 0.2)
        
        cp_explanation = VGroup(
            Text("• Minimum improvement required for a split", 
                font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["primary_text"]),
            Text("• Can be tuned via cross-validation in rpart()", 
                font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["primary_text"]),
            Text("• Higher values create simpler trees", 
                font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["primary_text"])
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        cp_explanation.move_to(DOWN * 0.5)
        
        self.play(Write(cp_title))
        self.play(Write(cp_explanation))
        self.wait(2)
        
        # Parameter 3: maxdepth
        maxdepth_title = Text("3. maxdepth", font_size=CONFIG["font_sizes"]["text"], 
                            color=CONFIG["colors"]["parameter_color"])
        maxdepth_title.move_to(DOWN * 1.2)
        
        maxdepth_explanation = VGroup(
            Text("• Maximum number of edges from root to leaf", 
                font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["primary_text"]),
            Text("• Must be tuned manually (trial and error)", 
                font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["highlight_color"]),
            Text("• Higher values allow more complex trees", 
                font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["primary_text"])
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        maxdepth_explanation.move_to(DOWN * 2)
        
        self.play(Write(maxdepth_title))
        self.play(Write(maxdepth_explanation))
        self.wait(3)
        
        # Fade out parameter explanations
        self.play(FadeOut(VGroup(section_title, minbucket_title, minbucket_explanation, 
                                cp_title, cp_explanation, maxdepth_title, maxdepth_explanation)))
        self.wait(1)

    def show_tree_visualizations(self):
        # Section title
        section_title = Text("Visual Examples", 
                           font_size=CONFIG["font_sizes"]["header"], 
                           color=CONFIG["colors"]["primary_text"])
        section_title.to_edge(UP, buff=0.5)
        
        # Simple tree (high minbucket, high cp, low maxdepth)
        simple_title = Text("Simple Tree", font_size=CONFIG["font_sizes"]["text"], 
                          color=CONFIG["colors"]["effect_color"])
        simple_title.move_to(UP * 1.5 + LEFT * 3)
        
        simple_tree = self.create_simple_tree()
        simple_tree.scale(0.4)
        simple_tree.move_to(UP * 0.5 + LEFT * 3)
        
        simple_params = VGroup(
            Text("minbucket = 50", font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["parameter_color"]),
            Text("cp = 0.1", font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["parameter_color"]),
            Text("maxdepth = 2", font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["parameter_color"])
        ).arrange(DOWN, buff=0.1)
        simple_params.next_to(simple_tree, DOWN, buff=0.3)
        
        # Complex tree (low minbucket, low cp, high maxdepth)
        complex_title = Text("Complex Tree", font_size=CONFIG["font_sizes"]["text"], 
                           color=CONFIG["colors"]["effect_color"])
        complex_title.move_to(UP * 1.5 + RIGHT * 3)
        
        complex_tree = self.create_complex_tree()
        complex_tree.scale(0.4)
        complex_tree.move_to(UP * 0.5 + RIGHT * 3)
        
        complex_params = VGroup(
            Text("minbucket = 5", font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["parameter_color"]),
            Text("cp = 0.01", font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["parameter_color"]),
            Text("maxdepth = 5", font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["parameter_color"])
        ).arrange(DOWN, buff=0.1)
        complex_params.next_to(complex_tree, DOWN, buff=0.3)
        
        self.play(Write(section_title))
        self.play(Write(simple_title))
        self.play(Create(simple_tree))
        self.play(Write(simple_params))
        
        self.play(Write(complex_title))
        self.play(Create(complex_tree))
        self.play(Write(complex_params))
        self.wait(3)
        
        # Fade out visualizations
        self.play(FadeOut(VGroup(section_title, simple_title, simple_tree, simple_params, 
                                complex_title, complex_tree, complex_params)))
        self.wait(1)

    def show_notes(self):
        # Section title
        section_title = Text("Important Notes", 
                           font_size=CONFIG["font_sizes"]["header"], 
                           color=CONFIG["colors"]["primary_text"])
        section_title.to_edge(UP, buff=0.5)
        
        # Notes
        notes = VGroup(
            Text("Notes:", font_size=CONFIG["font_sizes"]["text"], 
                color=CONFIG["colors"]["highlight_color"]),
            Text("• Know how these parameters limit tree complexity", 
                font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["primary_text"]),
            Text("• cp can be tuned via cross-validation in rpart()", 
                font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["primary_text"]),
            Text("• minbucket and maxdepth must be tuned manually (trial and error)", 
                font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["primary_text"]),
            Text("• Balance between model complexity and overfitting", 
                font_size=CONFIG["font_sizes"]["small_text"], color=CONFIG["colors"]["primary_text"])
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        notes.move_to(ORIGIN)
        
        self.play(Write(section_title))
        self.play(Write(notes))
        self.wait(4)
        
        # Fade out notes
        self.play(FadeOut(VGroup(section_title, notes)))
        self.wait(1)

    def show_summary(self):
        # Summary title
        summary_title = Text("Summary", 
                           font_size=CONFIG["font_sizes"]["header"], 
                           color=CONFIG["colors"]["primary_text"])
        summary_title.to_edge(UP, buff=0.5)
        
        # Key points
        key_points = VGroup(
            Text("🌳 minbucket: Controls terminal node size", 
                font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["parameter_color"]),
            Text("⚙️ cp: Controls split improvement threshold", 
                font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["parameter_color"]),
            Text("📏 maxdepth: Controls tree depth limit", 
                font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["parameter_color"]),
            Text("🎯 Higher values generally create simpler trees", 
                font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["effect_color"]),
            Text("🔧 Tune carefully to balance complexity and performance", 
                font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["highlight_color"])
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        key_points.move_to(ORIGIN)
        
        self.play(Write(summary_title))
        self.play(Write(key_points))
        self.wait(4)
        
        # Final message
        final_message = Text("Master these parameters to build better decision trees in R!", 
                           font_size=CONFIG["font_sizes"]["text"], 
                           color=CONFIG["colors"]["highlight_color"])
        final_message.move_to(DOWN * 3)
        
        self.play(Write(final_message))
        self.wait(3)
        
        # Fade out everything
        self.play(FadeOut(VGroup(summary_title, key_points, final_message)))
        self.wait(1)

    def create_blank_table(self, headers, parameters):
        """Create a blank table with checkboxes"""
        table = VGroup()
        
        # Headers
        header_row = VGroup()
        for i, header in enumerate(headers):
            header_text = Text(header, font_size=CONFIG["font_sizes"]["table_text"], 
                             color=CONFIG["colors"]["primary_text"])
            if i == 0:
                header_text.move_to(LEFT * 4)
            elif i == 1:
                header_text.move_to(LEFT * 1.5)
            elif i == 2:
                header_text.move_to(RIGHT * 1)
            else:
                header_text.move_to(RIGHT * 4)
            header_row.add(header_text)
        
        # Underline headers
        for header in header_row:
            underline = Line(header.get_left() + DOWN * 0.1, header.get_right() + DOWN * 0.1, 
                           color=CONFIG["colors"]["primary_text"])
            header_row.add(underline)
        
        table.add(header_row)
        
        # Parameters and checkboxes
        for i, param in enumerate(parameters):
            param_text = Text(param, font_size=CONFIG["font_sizes"]["table_text"], 
                            color=CONFIG["colors"]["primary_text"])
            param_text.move_to(LEFT * 4 + DOWN * (i + 1) * 0.8)
            
            # Checkboxes for other columns
            checkboxes = VGroup()
            for j in range(3):  # 3 columns with checkboxes
                checkbox = Square(side_length=0.3, color=CONFIG["colors"]["primary_text"])
                if j == 0:
                    checkbox.move_to(LEFT * 1.5 + DOWN * (i + 1) * 0.8)
                elif j == 1:
                    checkbox.move_to(RIGHT * 1 + DOWN * (i + 1) * 0.8)
                else:
                    checkbox.move_to(RIGHT * 4 + DOWN * (i + 1) * 0.8)
                checkboxes.add(checkbox)
            
            row = VGroup(param_text, checkboxes)
            table.add(row)
        
        return table

    def create_filled_table(self, headers, parameters, answers):
        """Create a filled table with answers"""
        table = VGroup()
        
        # Headers
        header_row = VGroup()
        for i, header in enumerate(headers):
            header_text = Text(header, font_size=CONFIG["font_sizes"]["table_text"], 
                             color=CONFIG["colors"]["primary_text"])
            if i == 0:
                header_text.move_to(LEFT * 4)
            elif i == 1:
                header_text.move_to(LEFT * 1.5)
            elif i == 2:
                header_text.move_to(RIGHT * 1)
            else:
                header_text.move_to(RIGHT * 4)
            header_row.add(header_text)
        
        # Underline headers
        for header in header_row:
            underline = Line(header.get_left() + DOWN * 0.1, header.get_right() + DOWN * 0.1, 
                           color=CONFIG["colors"]["primary_text"])
            header_row.add(underline)
        
        table.add(header_row)
        
        # Parameters and answers
        for i, param in enumerate(parameters):
            param_text = Text(param, font_size=CONFIG["font_sizes"]["table_text"], 
                            color=CONFIG["colors"]["primary_text"])
            param_text.move_to(LEFT * 4 + DOWN * (i + 1) * 0.8)
            
            # Answers
            r_name = Text(answers[param]["r_name"], font_size=CONFIG["font_sizes"]["table_text"], 
                         color=CONFIG["colors"]["r_name_color"])
            r_name.move_to(LEFT * 1.5 + DOWN * (i + 1) * 0.8)
            
            meaning = Text(answers[param]["meaning"], font_size=CONFIG["font_sizes"]["table_text"], 
                         color=CONFIG["colors"]["meaning_color"])
            meaning.move_to(RIGHT * 1 + DOWN * (i + 1) * 0.8)
            
            effect = Text(answers[param]["effect"], font_size=CONFIG["font_sizes"]["table_text"], 
                        color=CONFIG["colors"]["effect_color"])
            effect.move_to(RIGHT * 4 + DOWN * (i + 1) * 0.8)
            
            row = VGroup(param_text, r_name, meaning, effect)
            table.add(row)
        
        return table

    def create_simple_tree(self):
        """Create a simple decision tree visualization"""
        # Root node
        root = Circle(radius=0.2, color=CONFIG["colors"]["tree_color"], fill_opacity=0.3)
        root_text = Text("X > 5?", font_size=CONFIG["font_sizes"]["small_text"], color=WHITE)
        root_text.move_to(root)
        
        # Left child
        left_child = Circle(radius=0.15, color=CONFIG["colors"]["tree_color"], fill_opacity=0.3)
        left_child.move_to(root.get_center() + LEFT * 0.8 + DOWN * 0.6)
        left_text = Text("Yes", font_size=CONFIG["font_sizes"]["small_text"], color=WHITE)
        left_text.move_to(left_child)
        
        # Right child
        right_child = Circle(radius=0.15, color=CONFIG["colors"]["tree_color"], fill_opacity=0.3)
        right_child.move_to(root.get_center() + RIGHT * 0.8 + DOWN * 0.6)
        right_text = Text("No", font_size=CONFIG["font_sizes"]["small_text"], color=WHITE)
        right_text.move_to(right_child)
        
        # Edges
        left_edge = Line(root.get_center(), left_child.get_center(), color=CONFIG["colors"]["tree_color"])
        right_edge = Line(root.get_center(), right_child.get_center(), color=CONFIG["colors"]["tree_color"])
        
        return VGroup(root, root_text, left_child, left_text, right_child, right_text, left_edge, right_edge)

    def create_complex_tree(self):
        """Create a complex decision tree visualization"""
        # Root node
        root = Circle(radius=0.15, color=CONFIG["colors"]["tree_color"], fill_opacity=0.3)
        root_text = Text("X1 > 3?", font_size=CONFIG["font_sizes"]["small_text"], color=WHITE)
        root_text.move_to(root)
        
        # Level 1 nodes
        left1 = Circle(radius=0.12, color=CONFIG["colors"]["tree_color"], fill_opacity=0.3)
        left1.move_to(root.get_center() + LEFT * 1.2 + DOWN * 0.8)
        left1_text = Text("Yes", font_size=CONFIG["font_sizes"]["small_text"], color=WHITE)
        left1_text.move_to(left1)
        
        right1 = Circle(radius=0.12, color=CONFIG["colors"]["tree_color"], fill_opacity=0.3)
        right1.move_to(root.get_center() + RIGHT * 1.2 + DOWN * 0.8)
        right1_text = Text("No", font_size=CONFIG["font_sizes"]["small_text"], color=WHITE)
        right1_text.move_to(right1)
        
        # Level 2 nodes
        left1_left = Circle(radius=0.1, color=CONFIG["colors"]["tree_color"], fill_opacity=0.3)
        left1_left.move_to(left1.get_center() + LEFT * 0.8 + DOWN * 0.6)
        left1_left_text = Text("X2 > 2?", font_size=CONFIG["font_sizes"]["small_text"], color=WHITE)
        left1_left_text.move_to(left1_left)
        
        left1_right = Circle(radius=0.1, color=CONFIG["colors"]["tree_color"], fill_opacity=0.3)
        left1_right.move_to(left1.get_center() + RIGHT * 0.8 + DOWN * 0.6)
        left1_right_text = Text("Class A", font_size=CONFIG["font_sizes"]["small_text"], color=WHITE)
        left1_right_text.move_to(left1_right)
        
        right1_left = Circle(radius=0.1, color=CONFIG["colors"]["tree_color"], fill_opacity=0.3)
        right1_left.move_to(right1.get_center() + LEFT * 0.8 + DOWN * 0.6)
        right1_left_text = Text("Class B", font_size=CONFIG["font_sizes"]["small_text"], color=WHITE)
        right1_left_text.move_to(right1_left)
        
        right1_right = Circle(radius=0.1, color=CONFIG["colors"]["tree_color"], fill_opacity=0.3)
        right1_right.move_to(right1.get_center() + RIGHT * 0.8 + DOWN * 0.6)
        right1_right_text = Text("Class C", font_size=CONFIG["font_sizes"]["small_text"], color=WHITE)
        right1_right_text.move_to(right1_right)
        
        # Edges
        edges = VGroup(
            Line(root.get_center(), left1.get_center(), color=CONFIG["colors"]["tree_color"]),
            Line(root.get_center(), right1.get_center(), color=CONFIG["colors"]["tree_color"]),
            Line(left1.get_center(), left1_left.get_center(), color=CONFIG["colors"]["tree_color"]),
            Line(left1.get_center(), left1_right.get_center(), color=CONFIG["colors"]["tree_color"]),
            Line(right1.get_center(), right1_left.get_center(), color=CONFIG["colors"]["tree_color"]),
            Line(right1.get_center(), right1_right.get_center(), color=CONFIG["colors"]["tree_color"])
        )
        
        return VGroup(root, root_text, left1, left1_text, right1, right1_text,
                     left1_left, left1_left_text, left1_right, left1_right_text,
                     right1_left, right1_left_text, right1_right, right1_right_text, edges)
