from manim import *
import numpy as np

# --- Configuration ---
CONFIG = {
    "colors": {
        "background": "#1E1E2A",
        "primary_text": WHITE,
        "secondary_text": LIGHT_GREY,
        "original_color": BLUE,
        "pc_color": GREEN,
        "feature1_color": YELLOW,
        "feature2_color": ORANGE,
        "feature3_color": PURPLE,
        "warning_color": RED,
        "success_color": GREEN,
    },
    "font_sizes": {
        "title": 48,
        "header": 32,
        "text": 24,
        "label": 20,
    },
}

class PCAInterpretabilityAnimation(Scene):
    def construct(self):
        self.camera.background_color = CONFIG["colors"]["background"]

        # --- Scene 1: Introduction ---
        self.show_intro()

        # --- Scene 2: Original Features vs Principal Components ---
        self.show_original_vs_pc()

        # --- Scene 3: How PCA Creates Composite Variables ---
        self.show_composite_creation()

        # --- Scene 4: Loss of Interpretability ---
        self.show_interpretability_loss()

        # --- Scene 5: Visual Example ---
        self.show_visual_example()

        # --- Scene 6: Summary ---
        self.show_summary()

    def show_intro(self):
        """Introduces the concept of PCA interpretability loss."""
        title = Text("PCA and Loss of Interpretability", font_size=CONFIG["font_sizes"]["title"])
        subtitle = Text("Why Principal Components Are Hard to Interpret", font_size=CONFIG["font_sizes"]["header"], color=CONFIG["colors"]["secondary_text"]).next_to(title, DOWN)
        
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(2)
        
        # Key concept
        key_concept = Text(
            "Principal Components = Composite Variables",
            font_size=CONFIG["font_sizes"]["text"],
            color=CONFIG["colors"]["warning_color"]
        ).next_to(subtitle, DOWN, buff=1)
        
        self.play(Write(key_concept))
        self.wait(2)
        self.play(FadeOut(VGroup(title, subtitle, key_concept)))

    def show_original_vs_pc(self):
        """Shows the difference between original features and principal components."""
        title = Text("Original Features vs Principal Components", font_size=CONFIG["font_sizes"]["header"]).to_edge(UP)
        self.play(Write(title))

        # Original features side
        original_title = Text("Original Features", font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["original_color"])
        original_title.move_to([-3, 1, 0])

        original_features = VGroup(
            Text("• Age", font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["feature1_color"]),
            Text("• Height", font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["feature2_color"]),
            Text("• Weight", font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["feature3_color"]),
            Text("• Income", font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["feature1_color"]),
            Text("• Education", font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["feature2_color"])
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        original_features.move_to([-3, 0, 0])

        original_interpretation = Text(
            "Easy to interpret:\nEach feature has clear meaning",
            font_size=CONFIG["font_sizes"]["label"],
            color=CONFIG["colors"]["success_color"]
        ).next_to(original_features, DOWN, buff=0.5)

        # Principal components side
        pc_title = Text("Principal Components", font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["pc_color"])
        pc_title.move_to([3, 1, 0])

        pc_components = VGroup(
            Text("• PC1 = 0.3×Age + 0.2×Height + 0.4×Weight + 0.1×Income + 0.0×Education", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["pc_color"]),
            Text("• PC2 = 0.1×Age + 0.5×Height + 0.1×Weight + 0.2×Income + 0.1×Education", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["pc_color"]),
            Text("• PC3 = 0.2×Age + 0.1×Height + 0.1×Weight + 0.1×Income + 0.5×Education", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["pc_color"])
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        pc_components.move_to([3, 0, 0])

        pc_interpretation = Text(
            "Hard to interpret:\nWhat does PC1 actually represent?",
            font_size=CONFIG["font_sizes"]["label"],
            color=CONFIG["colors"]["warning_color"]
        ).next_to(pc_components, DOWN, buff=0.5)

        self.play(
            Write(original_title), Write(pc_title),
            Write(original_features), Write(pc_components),
            Write(original_interpretation), Write(pc_interpretation)
        )
        self.wait(3)
        
        self.play(FadeOut(VGroup(title, original_title, pc_title, original_features, pc_components, original_interpretation, pc_interpretation)))

    def show_composite_creation(self):
        """Shows how PCA creates composite variables from original features."""
        title = Text("How PCA Creates Composite Variables", font_size=CONFIG["font_sizes"]["header"]).to_edge(UP)
        self.play(Write(title))

        # Show the transformation process
        process_title = Text("PCA Transformation Process", font_size=CONFIG["font_sizes"]["text"])
        process_title.move_to([0, 1, 0])

        steps = VGroup(
            Text("1. Original features (interpretable)", font_size=CONFIG["font_sizes"]["text"]),
            Text("2. Linear combinations (mathematical)", font_size=CONFIG["font_sizes"]["text"]),
            Text("3. Principal components (composite)", font_size=CONFIG["font_sizes"]["text"])
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        steps.move_to([0, 0, 0])

        self.play(Write(process_title))
        self.play(Write(steps))
        self.wait(2)

        # Show mathematical transformation
        math_title = Text("Mathematical Transformation", font_size=CONFIG["font_sizes"]["text"])
        math_title.move_to([0, -1, 0])

        transformation = MathTex(
            r"\text{PC}_1 = w_1 \times \text{Age} + w_2 \times \text{Height} + w_3 \times \text{Weight} + \ldots",
            font_size=CONFIG["font_sizes"]["text"]
        ).next_to(math_title, DOWN, buff=0.5)

        self.play(Write(math_title))
        self.play(Write(transformation))
        self.wait(3)
        
        self.play(FadeOut(VGroup(title, process_title, steps, math_title, transformation)))

    def show_interpretability_loss(self):
        """Demonstrates the specific ways interpretability is lost."""
        title = Text("Loss of Interpretability", font_size=CONFIG["font_sizes"]["header"]).to_edge(UP)
        self.play(Write(title))

        # Show specific problems
        problems = VGroup(
            Text("Problems with PCA Interpretability:", font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["warning_color"]),
            VGroup(
                Dot(color=CONFIG["colors"]["warning_color"]),
                Text("No clear meaning: What is 'PC1' in real-world terms?", font_size=CONFIG["font_sizes"]["text"])
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Dot(color=CONFIG["colors"]["warning_color"]),
                Text("Mixed features: PC1 combines age, height, weight, etc.", font_size=CONFIG["font_sizes"]["text"])
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Dot(color=CONFIG["colors"]["warning_color"]),
                Text("Arbitrary weights: Why 0.3×Age + 0.2×Height + 0.4×Weight?", font_size=CONFIG["font_sizes"]["text"])
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Dot(color=CONFIG["colors"]["warning_color"]),
                Text("No domain expertise: Weights come from math, not knowledge", font_size=CONFIG["font_sizes"]["text"])
            ).arrange(RIGHT, buff=0.2)
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        problems.move_to([0, 0, 0])

        self.play(LaggedStart(*[Write(problem) for problem in problems], lag_ratio=0.7))
        self.wait(4)
        
        self.play(FadeOut(VGroup(title, problems)))

    def show_visual_example(self):
        """Shows a visual example of the interpretability problem."""
        title = Text("Visual Example: Customer Data", font_size=CONFIG["font_sizes"]["header"]).to_edge(UP)
        self.play(Write(title))

        # Original features
        original_title = Text("Original Features (Interpretable)", font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["success_color"])
        original_title.move_to([-3, 1, 0])

        original_data = VGroup(
            Text("Customer 1:", font_size=CONFIG["font_sizes"]["label"]),
            Text("Age: 25 years", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["feature1_color"]),
            Text("Income: $50,000", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["feature2_color"]),
            Text("Education: Bachelor's", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["feature3_color"]),
            Text(""),
            Text("Customer 2:", font_size=CONFIG["font_sizes"]["label"]),
            Text("Age: 45 years", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["feature1_color"]),
            Text("Income: $80,000", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["feature2_color"]),
            Text("Education: Master's", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["feature3_color"])
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        original_data.move_to([-3, 0, 0])

        # After PCA
        pca_title = Text("After PCA (Hard to Interpret)", font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["warning_color"])
        pca_title.move_to([3, 1, 0])

        pca_data = VGroup(
            Text("Customer 1:", font_size=CONFIG["font_sizes"]["label"]),
            Text("PC1: 0.73", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["pc_color"]),
            Text("PC2: -0.42", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["pc_color"]),
            Text("PC3: 0.15", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["pc_color"]),
            Text(""),
            Text("Customer 2:", font_size=CONFIG["font_sizes"]["label"]),
            Text("PC1: 1.24", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["pc_color"]),
            Text("PC2: 0.18", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["pc_color"]),
            Text("PC3: -0.33", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["pc_color"])
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        pca_data.move_to([3, 0, 0])

        self.play(
            Write(original_title), Write(pca_title),
            Write(original_data), Write(pca_data)
        )
        self.wait(3)

        # Show the interpretation problem
        question = Text(
            "What does PC1 = 0.73 mean?\nIs this good or bad?",
            font_size=CONFIG["font_sizes"]["text"],
            color=CONFIG["colors"]["warning_color"]
        ).next_to(title, DOWN, buff=1)
        
        self.play(Write(question))
        self.wait(2)

        # Show the transformation
        transformation_arrow = Arrow(start=[-1, 0, 0], end=[1, 0, 0], color=YELLOW, buff=0.5)
        transformation_label = Text("PCA Transformation", font_size=CONFIG["font_sizes"]["label"], color=YELLOW)
        transformation_label.next_to(transformation_arrow, UP)
        
        self.play(Create(transformation_arrow), Write(transformation_label))
        self.wait(3)
        
        self.play(FadeOut(VGroup(title, original_title, pca_title, original_data, pca_data, question, transformation_arrow, transformation_label)))

    def show_summary(self):
        """Summarizes the key points about PCA interpretability loss."""
        title = Text("Summary: PCA Interpretability Loss", font_size=CONFIG["font_sizes"]["title"]).to_edge(UP)
        self.play(Write(title))

        summary_points = VGroup(
            Text("Why PCA Loses Interpretability:", font_size=CONFIG["font_sizes"]["text"]),
            VGroup(
                Dot(color=CONFIG["colors"]["warning_color"]),
                Text("Principal components are composite variables", font_size=CONFIG["font_sizes"]["text"])
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Dot(color=CONFIG["colors"]["warning_color"]),
                Text("Built from linear combinations of all original features", font_size=CONFIG["font_sizes"]["text"])
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Dot(color=CONFIG["colors"]["warning_color"]),
                Text("Weights determined by mathematics, not domain knowledge", font_size=CONFIG["font_sizes"]["text"])
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Dot(color=CONFIG["colors"]["warning_color"]),
                Text("No clear real-world meaning for individual components", font_size=CONFIG["font_sizes"]["text"])
            ).arrange(RIGHT, buff=0.2)
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT).next_to(title, DOWN, buff=1)

        self.play(LaggedStart(*[FadeIn(point, shift=UP) for point in summary_points], lag_ratio=0.7))
        self.wait(3)

        # Trade-off explanation
        tradeoff = VGroup(
            Text("The Trade-off:", font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["success_color"]),
            Text("• PCA reduces dimensionality and removes redundancy", font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["success_color"]),
            Text("• But sacrifices interpretability for mathematical efficiency", font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["warning_color"])
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        tradeoff.next_to(summary_points, DOWN, buff=1)

        self.play(Write(tradeoff))
        self.wait(4)
        self.play(FadeOut(VGroup(title, summary_points, tradeoff)))
