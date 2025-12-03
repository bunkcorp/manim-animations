from manim import *
import numpy as np

# --- Configuration ---
CONFIG = {
    "colors": {
        "background": "#1E1E2A",
        "primary_text": WHITE,
        "secondary_text": LIGHT_GREY,
        "tree_color": GREEN,
        "partial_dep_color": BLUE,
        "variable_color": YELLOW,
        "prediction_color": ORANGE,
        "highlight_color": RED,
        "plot_color": PURPLE,
    },
    "font_sizes": {
        "title": 48,
        "header": 36,
        "text": 28,
        "formula": 32,
        "label": 24,
        "small_text": 20,
    },
}

class PartialDependenceAnimation(Scene):
    def construct(self):
        self.camera.background_color = CONFIG["colors"]["background"]
        self.show_intro()
        self.show_definition()
        self.show_mathematical_formula()
        self.show_visual_example()
        self.show_ensemble_trees()
        self.show_partial_dependence_plot()
        self.show_interpretation()
        self.show_summary()

    def show_intro(self):
        # Title
        title = Text("Partial Dependence in Ensemble Trees", 
                    font_size=CONFIG["font_sizes"]["title"], 
                    color=CONFIG["colors"]["primary_text"])
        title.to_edge(UP, buff=0.5)
        
        # Subtitle
        subtitle = Text("Understanding Marginal Effects of Variables", 
                       font_size=CONFIG["font_sizes"]["text"], 
                       color=CONFIG["colors"]["secondary_text"])
        subtitle.next_to(title, DOWN, buff=0.3)
        
        self.play(Write(title))
        self.play(Write(subtitle))
        self.wait(2)
        
        # Fade out intro
        self.play(FadeOut(VGroup(title, subtitle)))
        self.wait(1)

    def show_definition(self):
        # Section title
        section_title = Text("What is Partial Dependence?", 
                           font_size=CONFIG["font_sizes"]["header"], 
                           color=CONFIG["colors"]["primary_text"])
        section_title.to_edge(UP, buff=0.5)
        
        # Definition text
        definition = VGroup(
            Text("Definition:", font_size=CONFIG["font_sizes"]["text"], 
                color=CONFIG["colors"]["highlight_color"]),
            Text("The prediction averaged over all training observations,", 
                font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["primary_text"]),
            Text("holding the variable of interest fixed.", 
                font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["primary_text"])
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        definition.move_to(UP * 1)
        
        # Key concept
        key_concept = VGroup(
            Text("Key Idea:", font_size=CONFIG["font_sizes"]["text"], 
                color=CONFIG["colors"]["variable_color"]),
            Text("• Isolate the effect of one variable", 
                font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["primary_text"]),
            Text("• Average out the effects of other variables", 
                font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["primary_text"]),
            Text("• Show the marginal relationship", 
                font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["primary_text"])
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        key_concept.move_to(DOWN * 1)
        
        self.play(Write(section_title))
        self.play(Write(definition))
        self.wait(2)
        self.play(Write(key_concept))
        self.wait(3)
        
        # Fade out definition
        self.play(FadeOut(VGroup(section_title, definition, key_concept)))
        self.wait(1)

    def show_mathematical_formula(self):
        # Section title
        section_title = Text("Mathematical Definition", 
                           font_size=CONFIG["font_sizes"]["header"], 
                           color=CONFIG["colors"]["primary_text"])
        section_title.to_edge(UP, buff=0.5)
        
        # Main formula
        main_formula = MathTex(
            r"PD_s(x_s) = \frac{1}{n} \sum_{i=1}^{n} f(x_s, x_c^{(i)})",
            color=CONFIG["colors"]["partial_dep_color"]
        )
        main_formula.move_to(UP * 1)
        
        # Formula explanation
        explanation = VGroup(
            Text("Where:", font_size=CONFIG["font_sizes"]["text"], 
                color=CONFIG["colors"]["highlight_color"]),
            Text("• PD_s(x_s): Partial dependence for variable s", 
                font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["primary_text"]),
            Text("• x_s: Variable of interest (fixed value)", 
                font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["variable_color"]),
            Text("• x_c^{(i)}: Other variables from training data", 
                font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["primary_text"]),
            Text("• f(): Ensemble model prediction", 
                font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["prediction_color"]),
            Text("• n: Number of training observations", 
                font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["primary_text"])
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        explanation.move_to(DOWN * 1)
        
        self.play(Write(section_title))
        self.play(Write(main_formula))
        self.wait(2)
        self.play(Write(explanation))
        self.wait(3)
        
        # Fade out formula
        self.play(FadeOut(VGroup(section_title, main_formula, explanation)))
        self.wait(1)

    def show_visual_example(self):
        # Section title
        section_title = Text("Visual Example", 
                           font_size=CONFIG["font_sizes"]["header"], 
                           color=CONFIG["colors"]["primary_text"])
        section_title.to_edge(UP, buff=0.5)
        
        # Create a simple dataset visualization
        dataset_title = Text("Training Dataset", font_size=CONFIG["font_sizes"]["text"], 
                           color=CONFIG["colors"]["variable_color"])
        dataset_title.move_to(UP * 1.5)
        
        # Sample data points
        data_points = VGroup()
        for i in range(6):
            point = Circle(radius=0.08, color=CONFIG["colors"]["primary_text"], fill_opacity=0.7)
            point.move_to(UP * 0.8 + RIGHT * (i - 2.5) * 0.8 + DOWN * (i % 2) * 0.3)
            data_points.add(point)
        
        # Variable labels
        x1_label = Text("X₁ (variable of interest)", font_size=CONFIG["font_sizes"]["label"], 
                       color=CONFIG["colors"]["variable_color"])
        x1_label.move_to(UP * 0.2)
        
        x2_label = Text("X₂ (other variables)", font_size=CONFIG["font_sizes"]["label"], 
                       color=CONFIG["colors"]["primary_text"])
        x2_label.move_to(UP * -0.2)
        
        self.play(Write(section_title))
        self.play(Write(dataset_title))
        self.play(FadeIn(data_points))
        self.play(Write(x1_label), Write(x2_label))
        self.wait(2)
        
        # Show partial dependence process
        process_title = Text("Partial Dependence Process", font_size=CONFIG["font_sizes"]["text"], 
                           color=CONFIG["colors"]["partial_dep_color"])
        process_title.move_to(DOWN * 1)
        
        process_steps = VGroup(
            Text("1. Fix X₁ at a specific value", font_size=CONFIG["font_sizes"]["label"], 
                color=CONFIG["colors"]["primary_text"]),
            Text("2. Use all X₂ values from training data", font_size=CONFIG["font_sizes"]["label"], 
                color=CONFIG["colors"]["primary_text"]),
            Text("3. Get predictions for each combination", font_size=CONFIG["font_sizes"]["label"], 
                color=CONFIG["colors"]["primary_text"]),
            Text("4. Average the predictions", font_size=CONFIG["font_sizes"]["label"], 
                color=CONFIG["colors"]["primary_text"])
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        process_steps.move_to(DOWN * 2.5)
        
        self.play(Write(process_title))
        self.play(Write(process_steps))
        self.wait(3)
        
        # Fade out visual example
        self.play(FadeOut(VGroup(section_title, dataset_title, data_points, x1_label, x2_label, 
                                process_title, process_steps)))
        self.wait(1)

    def show_ensemble_trees(self):
        # Section title
        section_title = Text("Ensemble Trees Context", 
                           font_size=CONFIG["font_sizes"]["header"], 
                           color=CONFIG["colors"]["primary_text"])
        section_title.to_edge(UP, buff=0.5)
        
        # Create multiple trees
        trees = VGroup()
        for i in range(3):
            tree = self.create_ensemble_tree()
            tree.scale(0.4)
            tree.move_to(UP * 0.5 + RIGHT * (i - 1) * 2.5)
            trees.add(tree)
        
        # Tree labels
        tree_labels = VGroup(
            Text("Tree 1", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["tree_color"]),
            Text("Tree 2", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["tree_color"]),
            Text("Tree 3", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["tree_color"])
        )
        
        for i, label in enumerate(tree_labels):
            label.next_to(trees[i], DOWN, buff=0.3)
        
        # Ensemble prediction
        ensemble_arrow = Arrow(LEFT * 4, RIGHT * 4, color=CONFIG["colors"]["prediction_color"], stroke_width=4)
        ensemble_arrow.move_to(DOWN * 1)
        
        ensemble_prediction = Text("Ensemble Prediction", font_size=CONFIG["font_sizes"]["text"], 
                                 color=CONFIG["colors"]["prediction_color"])
        ensemble_prediction.next_to(ensemble_arrow, DOWN, buff=0.3)
        
        self.play(Write(section_title))
        self.play(FadeIn(trees))
        self.play(Write(tree_labels))
        self.wait(2)
        self.play(Create(ensemble_arrow))
        self.play(Write(ensemble_prediction))
        self.wait(2)
        
        # Fade out ensemble trees
        self.play(FadeOut(VGroup(section_title, trees, tree_labels, ensemble_arrow, ensemble_prediction)))
        self.wait(1)

    def show_partial_dependence_plot(self):
        # Section title
        section_title = Text("Partial Dependence Plot", 
                           font_size=CONFIG["font_sizes"]["header"], 
                           color=CONFIG["colors"]["primary_text"])
        section_title.to_edge(UP, buff=0.5)
        
        # Create axes
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 1, 0.2],
            x_length=6,
            y_length=4,
            axis_config={"color": WHITE},
            x_axis_config={"numbers_to_include": np.arange(0, 11, 2)},
            y_axis_config={"numbers_to_include": np.arange(0, 1.1, 0.2)},
        ).add_coordinates()
        
        x_label = axes.get_x_axis_label(Text("X1 (Variable of Interest)", font_size=24, color=WHITE))
        y_label = axes.get_y_axis_label(Text("Partial Dependence", font_size=24, color=WHITE))
        axes_labels = VGroup(x_label, y_label)
        
        axes.move_to(ORIGIN)
        
        # Create partial dependence curve
        pd_curve = axes.plot(lambda x: 0.3 + 0.4 * np.sin(x * 0.5), color=CONFIG["colors"]["plot_color"], stroke_width=3)
        
        # Add some data points on the curve
        pd_points = VGroup()
        for i in range(8):
            x_val = i * 1.2
            y_val = 0.3 + 0.4 * np.sin(x_val * 0.5)
            point = Dot(axes.coords_to_point(x_val, y_val), color=CONFIG["colors"]["plot_color"], radius=0.05)
            pd_points.add(point)
        
        self.play(Write(section_title))
        self.play(Create(axes), Write(axes_labels))
        self.play(Create(pd_curve))
        self.play(FadeIn(pd_points))
        self.wait(2)
        
        # Add interpretation text
        interpretation = VGroup(
            Text("Interpretation:", font_size=CONFIG["font_sizes"]["text"], 
                color=CONFIG["colors"]["highlight_color"]),
            Text("• Shows how X₁ affects predictions", 
                font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["primary_text"]),
            Text("• Averaged over all other variables", 
                font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["primary_text"]),
            Text("• Non-linear relationship visible", 
                font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["primary_text"])
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        interpretation.move_to(RIGHT * 4)
        
        self.play(Write(interpretation))
        self.wait(3)
        
        # Fade out plot
        self.play(FadeOut(VGroup(section_title, axes, axes_labels, pd_curve, pd_points, interpretation)))
        self.wait(1)

    def show_interpretation(self):
        # Section title
        section_title = Text("Use Cases & Interpretation", 
                           font_size=CONFIG["font_sizes"]["header"], 
                           color=CONFIG["colors"]["primary_text"])
        section_title.to_edge(UP, buff=0.5)
        
        # Use cases
        use_cases = VGroup(
            Text("Use Cases:", font_size=CONFIG["font_sizes"]["text"], 
                color=CONFIG["colors"]["highlight_color"]),
            Text("• Plot PD(x₁) vs x₁ to visualize marginal effects", 
                font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["primary_text"]),
            Text("• Identify important variables", 
                font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["primary_text"]),
            Text("• Understand non-linear relationships", 
                font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["primary_text"]),
            Text("• Model interpretability", 
                font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["primary_text"])
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        use_cases.move_to(LEFT * 3)
        
        # Advantages
        advantages = VGroup(
            Text("Advantages:", font_size=CONFIG["font_sizes"]["text"], 
                color=CONFIG["colors"]["variable_color"]),
            Text("• Captures non-linear effects", 
                font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["primary_text"]),
            Text("• Model-agnostic approach", 
                font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["primary_text"]),
            Text("• Easy to interpret", 
                font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["primary_text"]),
            Text("• Works with any ensemble", 
                font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["primary_text"])
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        advantages.move_to(RIGHT * 3)
        
        self.play(Write(section_title))
        self.play(Write(use_cases))
        self.play(Write(advantages))
        self.wait(3)
        
        # Fade out interpretation
        self.play(FadeOut(VGroup(section_title, use_cases, advantages)))
        self.wait(1)

    def show_summary(self):
        # Summary title
        summary_title = Text("Summary", 
                           font_size=CONFIG["font_sizes"]["header"], 
                           color=CONFIG["colors"]["primary_text"])
        summary_title.to_edge(UP, buff=0.5)
        
        # Key points
        key_points = VGroup(
            Text("🎯 Partial Dependence shows marginal effects", 
                font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["partial_dep_color"]),
            Text("📊 Averages predictions over training data", 
                font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["primary_text"]),
            Text("🔍 Isolates one variable's effect", 
                font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["variable_color"]),
            Text("📈 Visualizes non-linear relationships", 
                font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["plot_color"]),
            Text("🧠 Enhances model interpretability", 
                font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["highlight_color"])
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        key_points.move_to(ORIGIN)
        
        self.play(Write(summary_title))
        self.play(Write(key_points))
        self.wait(4)
        
        # Final message
        final_message = Text("Partial Dependence: A powerful tool for understanding ensemble models!", 
                           font_size=CONFIG["font_sizes"]["text"], 
                           color=CONFIG["colors"]["highlight_color"])
        final_message.move_to(DOWN * 3)
        
        self.play(Write(final_message))
        self.wait(3)
        
        # Fade out everything
        self.play(FadeOut(VGroup(summary_title, key_points, final_message)))
        self.wait(1)

    def create_ensemble_tree(self):
        """Create a simple ensemble tree visualization"""
        # Root node
        root = Circle(radius=0.2, color=CONFIG["colors"]["tree_color"], fill_opacity=0.3)
        root_text = Text("X₁ > 5?", font_size=CONFIG["font_sizes"]["small_text"], color=WHITE)
        root_text.move_to(root)
        
        # Left child
        left_child = Circle(radius=0.15, color=CONFIG["colors"]["tree_color"], fill_opacity=0.3)
        left_child.move_to(root.get_center() + LEFT * 0.8 + DOWN * 0.6)
        left_text = Text("0.3", font_size=CONFIG["font_sizes"]["small_text"], color=WHITE)
        left_text.move_to(left_child)
        
        # Right child
        right_child = Circle(radius=0.15, color=CONFIG["colors"]["tree_color"], fill_opacity=0.3)
        right_child.move_to(root.get_center() + RIGHT * 0.8 + DOWN * 0.6)
        right_text = Text("0.7", font_size=CONFIG["font_sizes"]["small_text"], color=WHITE)
        right_text.move_to(right_child)
        
        # Edges
        left_edge = Line(root.get_center(), left_child.get_center(), color=CONFIG["colors"]["tree_color"])
        right_edge = Line(root.get_center(), right_child.get_center(), color=CONFIG["colors"]["tree_color"])
        
        return VGroup(root, root_text, left_child, left_text, right_child, right_text, left_edge, right_edge)
