from manim import *
import numpy as np

class PCABiplotInterpretation(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = "#1E1E2A"
        
        # Title
        title = Text("Interpreting PCA Biplot", font_size=48, color=WHITE, weight=BOLD)
        title.to_edge(UP)
        subtitle = Text("PC Scores vs Loadings", font_size=32, color=YELLOW)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(Write(subtitle))
        self.wait(2)
        
        # Fade out title
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # Introduction
        self.show_introduction()
        
        # Create biplot
        self.create_biplot()
        
        # Show interpretation
        self.show_interpretation()
        
        # Summary
        self.show_summary()

    def show_introduction(self):
        # Introduction section
        intro_title = Text("What is a PCA Biplot?", font_size=36, color=WHITE, weight=BOLD)
        intro_title.to_edge(UP)
        
        intro_text = VGroup(
            Text("• Combines PC scores and loadings in one plot", color=WHITE, font_size=24),
            Text("• PC Loadings: Show variable contributions to PCs", color=BLUE, font_size=24),
            Text("• PC Scores: Show observation positions in PC space", color=RED, font_size=24),
            Text("• Together: Reveal relationships between variables and observations", color=GREEN, font_size=24),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        intro_text.next_to(intro_title, DOWN, buff=0.5)
        
        self.play(Write(intro_title))
        self.play(FadeIn(intro_text, shift=LEFT*0.3))
        self.wait(3)
        
        # Store for later
        self.intro_title = intro_title
        self.intro_text = intro_text

    def create_biplot(self):
        # Fade out introduction
        self.play(FadeOut(self.intro_text))
        
        # Biplot title
        biplot_title = Text("PCA Biplot Components", font_size=36, color=WHITE, weight=BOLD)
        biplot_title.to_edge(UP)
        self.play(Transform(self.intro_title, biplot_title))
        
        # Create coordinate system
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": WHITE, "stroke_width": 2},
            x_axis_config={"numbers_to_include": np.arange(-4, 5, 1)},
            y_axis_config={"numbers_to_include": np.arange(-3, 4, 1)},
        )
        
        # Add axis labels
        x_label = Text("PC1", font_size=24, color=WHITE).next_to(axes.x_axis, DOWN)
        y_label = Text("PC2", font_size=24, color=WHITE).next_to(axes.y_axis, LEFT).rotate(90*DEGREES)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Create sample data points (PC scores)
        np.random.seed(42)
        n_points = 30
        
        # Generate clustered data
        cluster1_scores = np.random.multivariate_normal([-1.5, 0.5], [[0.3, 0.1], [0.1, 0.3]], n_points//3)
        cluster2_scores = np.random.multivariate_normal([1.5, -0.5], [[0.3, 0.1], [0.1, 0.3]], n_points//3)
        cluster3_scores = np.random.multivariate_normal([0, 1.5], [[0.3, 0.1], [0.1, 0.3]], n_points//3)
        
        all_scores = np.vstack([cluster1_scores, cluster2_scores, cluster3_scores])
        
        # Create score points
        score_dots = VGroup()
        for i, (x, y) in enumerate(all_scores):
            dot = Dot(axes.coords_to_point(x, y), color=RED, radius=0.05)
            score_dots.add(dot)
        
        # Animate score points appearing
        self.play(LaggedStart(*[FadeIn(dot, scale=0.5) for dot in score_dots], lag_ratio=0.02))
        
        # Add score label
        scores_label = Text("PC Scores (Observations)", font_size=20, color=RED, weight=BOLD)
        scores_label.next_to(axes, DOWN, buff=0.3)
        self.play(Write(scores_label))
        
        # Create variable loadings (arrows from origin)
        loadings_data = np.array([
            [2.5, 0.8],   # Variable 1
            [-1.8, 1.2],  # Variable 2
            [0.5, 2.0],   # Variable 3
            [-2.0, -0.5], # Variable 4
            [1.2, -1.5],  # Variable 5
        ])
        
        variable_names = ["Age", "Income", "Education", "Location", "Occupation"]
        
        # Create loading arrows
        loading_arrows = VGroup()
        loading_labels = VGroup()
        
        for i, (x, y) in enumerate(loadings_data):
            # Arrow from origin to loading point
            arrow = Arrow(
                start=axes.coords_to_point(0, 0),
                end=axes.coords_to_point(x, y),
                color=BLUE,
                stroke_width=3,
                buff=0
            )
            loading_arrows.add(arrow)
            
            # Variable label
            label = Text(variable_names[i], font_size=16, color=BLUE, weight=BOLD)
            label.next_to(arrow.get_end(), direction=arrow.get_unit_vector(), buff=0.1)
            loading_labels.add(label)
        
        # Animate loading arrows
        self.play(LaggedStart(*[Create(arrow) for arrow in loading_arrows], lag_ratio=0.3))
        self.play(LaggedStart(*[Write(label) for label in loading_labels], lag_ratio=0.2))
        
        # Add loadings label
        loadings_label = Text("PC Loadings (Variables)", font_size=20, color=BLUE, weight=BOLD)
        loadings_label.next_to(scores_label, DOWN, buff=0.2)
        self.play(Write(loadings_label))
        
        self.wait(2)
        
        # Store for later
        self.axes = axes
        self.x_label = x_label
        self.y_label = y_label
        self.score_dots = score_dots
        self.scores_label = scores_label
        self.loading_arrows = loading_arrows
        self.loading_labels = loading_labels
        self.loadings_label = loadings_label
        self.loadings_data = loadings_data
        self.all_scores = all_scores

    def show_interpretation(self):
        # Fade out labels
        self.play(FadeOut(self.scores_label), FadeOut(self.loadings_label))
        
        # Interpretation title
        interpret_title = Text("How to Interpret the Biplot", font_size=36, color=WHITE, weight=BOLD)
        interpret_title.to_edge(UP)
        self.play(Transform(self.intro_title, interpret_title))
        
        # Create interpretation panels
        self.create_interpretation_panels()
        
        # Show specific examples
        self.show_specific_examples()

    def create_interpretation_panels(self):
        # Left panel: Loadings interpretation
        left_panel = VGroup()
        
        loadings_title = Text("PC Loadings (Top/Right)", font_size=24, color=BLUE, weight=BOLD)
        loadings_title.to_edge(LEFT).shift(UP*2)
        
        loadings_rules = VGroup(
            Text("• Arrow length = Variable importance", color=WHITE, font_size=18),
            Text("• Arrow direction = Variable contribution", color=WHITE, font_size=18),
            Text("• Similar directions = Correlated variables", color=WHITE, font_size=18),
            Text("• Opposite directions = Anti-correlated", color=WHITE, font_size=18),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        loadings_rules.next_to(loadings_title, DOWN, buff=0.3)
        
        left_panel.add(loadings_title, loadings_rules)
        left_panel.to_edge(LEFT, buff=0.5)
        
        # Right panel: Scores interpretation
        right_panel = VGroup()
        
        scores_title = Text("PC Scores (Bottom/Left)", font_size=24, color=RED, weight=BOLD)
        scores_title.to_edge(RIGHT).shift(UP*2)
        
        scores_rules = VGroup(
            Text("• Point position = Observation location", color=WHITE, font_size=18),
            Text("• Distance from origin = Overall magnitude", color=WHITE, font_size=18),
            Text("• Clustering = Similar observations", color=WHITE, font_size=18),
            Text("• Direction = Dominant characteristics", color=WHITE, font_size=18),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        scores_rules.next_to(scores_title, DOWN, buff=0.3)
        
        right_panel.add(scores_title, scores_rules)
        right_panel.to_edge(RIGHT, buff=0.5)
        
        # Animate panels
        self.play(FadeIn(left_panel, shift=LEFT*0.3))
        self.play(FadeIn(right_panel, shift=RIGHT*0.3))
        self.wait(3)
        
        # Store for later
        self.left_panel = left_panel
        self.right_panel = right_panel

    def show_specific_examples(self):
        # Fade out panels
        self.play(FadeOut(self.left_panel), FadeOut(self.right_panel))
        
        # Example 1: High Education, Low Income
        example1_title = Text("Example 1: High Education, Low Income", font_size=28, color=GREEN, weight=BOLD)
        example1_title.to_edge(UP)
        self.play(Transform(self.intro_title, example1_title))
        
        # Highlight relevant loading and score
        education_arrow = self.loading_arrows[2]  # Education
        income_arrow = self.loading_arrows[1]     # Income
        
        # Find a point with high education, low income characteristics
        high_edu_low_income_point = self.score_dots[0]  # Example point
        
        # Highlight elements
        self.play(
            education_arrow.animate.set_color(YELLOW).set_stroke_width(5),
            income_arrow.animate.set_color(YELLOW).set_stroke_width(5),
            high_edu_low_income_point.animate.set_color(YELLOW).scale(2)
        )
        
        # Add explanation
        explanation1 = Text(
            "This observation has high Education loading\nbut low Income loading",
            font_size=20, color=YELLOW
        )
        explanation1.next_to(self.axes, DOWN, buff=0.5)
        self.play(Write(explanation1))
        self.wait(2)
        
        # Reset colors
        self.play(
            education_arrow.animate.set_color(BLUE).set_stroke_width(3),
            income_arrow.animate.set_color(BLUE).set_stroke_width(3),
            high_edu_low_income_point.animate.set_color(RED).scale(0.5),
            FadeOut(explanation1)
        )
        
        # Example 2: Age and Location correlation
        example2_title = Text("Example 2: Age and Location Correlation", font_size=28, color=GREEN, weight=BOLD)
        example2_title.to_edge(UP)
        self.play(Transform(self.intro_title, example2_title))
        
        age_arrow = self.loading_arrows[0]      # Age
        location_arrow = self.loading_arrows[3] # Location
        
        # Highlight arrows pointing in similar direction
        self.play(
            age_arrow.animate.set_color(YELLOW).set_stroke_width(5),
            location_arrow.animate.set_color(YELLOW).set_stroke_width(5)
        )
        
        # Add correlation explanation
        explanation2 = Text(
            "Age and Location arrows point in similar direction\n→ These variables are correlated",
            font_size=20, color=YELLOW
        )
        explanation2.next_to(self.axes, DOWN, buff=0.5)
        self.play(Write(explanation2))
        self.wait(2)
        
        # Reset colors
        self.play(
            age_arrow.animate.set_color(BLUE).set_stroke_width(3),
            location_arrow.animate.set_color(BLUE).set_stroke_width(3),
            FadeOut(explanation2)
        )
        
        # Store for later
        self.example1_title = example1_title
        self.example2_title = example2_title

    def show_summary(self):
        # Fade out biplot
        self.play(
            FadeOut(self.axes), FadeOut(self.x_label), FadeOut(self.y_label),
            FadeOut(self.score_dots), FadeOut(self.loading_arrows), FadeOut(self.loading_labels)
        )
        
        # Summary title
        summary_title = Text("Key Takeaways", font_size=36, color=WHITE, weight=BOLD)
        summary_title.to_edge(UP)
        self.play(Transform(self.intro_title, summary_title))
        
        # Summary points
        summary_points = VGroup(
            Text("• Loadings (arrows) show variable contributions to PCs", color=BLUE, font_size=24),
            Text("• Scores (points) show observation positions in PC space", color=RED, font_size=24),
            Text("• Arrow length = Variable importance", color=WHITE, font_size=24),
            Text("• Arrow direction = Variable relationships", color=WHITE, font_size=24),
            Text("• Point clustering = Similar observations", color=WHITE, font_size=24),
            Text("• Distance from origin = Overall magnitude", color=WHITE, font_size=24),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        summary_points.next_to(summary_title, DOWN, buff=0.5)
        
        self.play(FadeIn(summary_points, shift=LEFT*0.3))
        self.wait(3)
        
        # Final message
        final_message = Text(
            "Biplots reveal the relationship between\nvariables and observations in PCA space",
            font_size=28, color=GREEN, weight=BOLD
        )
        final_message.move_to(ORIGIN)
        
        self.play(
            FadeOut(self.intro_title),
            FadeOut(summary_points)
        )
        self.play(Write(final_message))
        self.wait(3)
