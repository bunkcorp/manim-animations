from manim import *
import numpy as np

# --- Configuration ---
CONFIG = {
    "colors": {
        "background": "#1E1E2A",
        "primary_text": WHITE,
        "secondary_text": LIGHT_GREY,
        "eda_color": BLUE,
        "feature_color": GREEN,
        "pca_color": YELLOW,
        "data_color": PURPLE,
        "highlight_color": RED,
        "plot_color": ORANGE,
    },
    "font_sizes": {
        "title": 48,
        "header": 36,
        "text": 28,
        "subtext": 24,
        "small_text": 20,
    },
}

class PCAApplicationsAnimation(Scene):
    def construct(self):
        self.camera.background_color = CONFIG["colors"]["background"]
        self.show_title()
        self.show_introduction()
        self.show_eda_application()
        self.show_feature_generation()
        self.show_comparison()
        self.show_summary()

    def show_title(self):
        # Main title
        title = Text("Two Common Applications of PCA", 
                    font_size=CONFIG["font_sizes"]["title"], 
                    color=CONFIG["colors"]["primary_text"],
                    weight=BOLD)
        title.scale(0.8)
        
        # Subtitle
        subtitle = Text("Principal Component Analysis", 
                       font_size=CONFIG["font_sizes"]["text"], 
                       color=CONFIG["colors"]["pca_color"])
        subtitle.scale(0.7)
        
        # Arrange elements
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.3)
        
        self.play(FadeIn(title, shift=UP*0.3))
        self.play(FadeIn(subtitle, shift=DOWN*0.3))
        self.wait(2)
        
        # Fade out title
        self.play(FadeOut(title_group))
        self.wait(1)

    def show_introduction(self):
        # Introduction section
        intro_title = Text("What is PCA?", 
                          font_size=CONFIG["font_sizes"]["header"], 
                          color=CONFIG["colors"]["primary_text"],
                          weight=BOLD)
        intro_title.to_edge(UP)
        
        # PCA explanation
        pca_explanation = VGroup(
            Text("• Dimensionality reduction technique", 
                 color=CONFIG["colors"]["primary_text"], 
                 font_size=CONFIG["font_sizes"]["text"]),
            Text("• Transforms correlated variables into uncorrelated components", 
                 color=CONFIG["colors"]["primary_text"], 
                 font_size=CONFIG["font_sizes"]["text"]),
            Text("• Preserves maximum variance in fewer dimensions", 
                 color=CONFIG["colors"]["primary_text"], 
                 font_size=CONFIG["font_sizes"]["text"]),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        pca_explanation.next_to(intro_title, DOWN, buff=0.5)
        
        # Two applications preview
        applications_preview = VGroup(
            Text("Two Main Applications:", 
                 font_size=CONFIG["font_sizes"]["text"], 
                 color=CONFIG["colors"]["highlight_color"],
                 weight=BOLD),
            Text("1. Exploratory Data Analysis (EDA)", 
                 font_size=CONFIG["font_sizes"]["text"], 
                 color=CONFIG["colors"]["eda_color"]),
            Text("2. Feature Generation", 
                 font_size=CONFIG["font_sizes"]["text"], 
                 color=CONFIG["colors"]["feature_color"]),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        applications_preview.next_to(pca_explanation, DOWN, buff=0.8)
        
        self.play(Write(intro_title))
        self.play(FadeIn(pca_explanation, shift=LEFT*0.3))
        self.wait(1)
        self.play(FadeIn(applications_preview, shift=RIGHT*0.3))
        self.wait(2)
        
        # Store for later
        self.intro_title = intro_title
        self.pca_explanation = pca_explanation
        self.applications_preview = applications_preview

    def show_eda_application(self):
        # Fade out introduction
        self.play(FadeOut(self.pca_explanation), FadeOut(self.applications_preview))
        
        # EDA Section Title
        eda_title = Text("1. Exploratory Data Analysis (EDA)", 
                        font_size=CONFIG["font_sizes"]["header"], 
                        color=CONFIG["colors"]["eda_color"],
                        weight=BOLD)
        eda_title.to_edge(UP)
        self.play(Transform(self.intro_title, eda_title))
        
        # EDA explanation
        eda_explanation = VGroup(
            Text("Plot scores of PC1 vs. PC2 in a scatterplot", 
                 color=CONFIG["colors"]["primary_text"], 
                 font_size=CONFIG["font_sizes"]["text"]),
            Text("to visualize 2D structure", 
                 color=CONFIG["colors"]["primary_text"], 
                 font_size=CONFIG["font_sizes"]["text"]),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        eda_explanation.next_to(eda_title, DOWN, buff=0.5)
        
        self.play(FadeIn(eda_explanation, shift=LEFT*0.3))
        self.wait(1)
        
        # Create scatter plot example
        self.create_eda_scatter_plot()
        
        # Store for later
        self.eda_explanation = eda_explanation

    def create_eda_scatter_plot(self):
        # Create axes for scatter plot
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=4,
            axis_config={"color": CONFIG["colors"]["primary_text"]},
            x_axis_config={"numbers_to_include": np.arange(-3, 4, 1)},
            y_axis_config={"numbers_to_include": np.arange(-3, 4, 1)},
        ).to_edge(RIGHT, buff=0.5)
        
        # Add axis labels
        x_label = Text("PC1", font_size=24, color=CONFIG["colors"]["eda_color"]).next_to(axes.x_axis, DOWN)
        y_label = Text("PC2", font_size=24, color=CONFIG["colors"]["eda_color"]).next_to(axes.y_axis, LEFT).rotate(90*DEGREES)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Generate sample data points (clusters)
        np.random.seed(42)
        n_points = 50
        
        # Cluster 1
        cluster1_x = np.random.normal(-1, 0.5, n_points//2)
        cluster1_y = np.random.normal(-1, 0.5, n_points//2)
        
        # Cluster 2
        cluster2_x = np.random.normal(1, 0.5, n_points//2)
        cluster2_y = np.random.normal(1, 0.5, n_points//2)
        
        # Combine data
        all_x = np.concatenate([cluster1_x, cluster2_x])
        all_y = np.concatenate([cluster1_y, cluster2_y])
        
        # Create dots
        dots = VGroup()
        for i in range(len(all_x)):
            dot = Dot(axes.coords_to_point(all_x[i], all_y[i]), 
                     color=CONFIG["colors"]["data_color"], 
                     radius=0.05)
            dots.add(dot)
        
        # Animate dots appearing
        self.play(LaggedStart(*[FadeIn(dot, scale=0.5) for dot in dots], lag_ratio=0.02))
        
        # Add cluster labels
        cluster1_label = Text("Cluster A", font_size=20, color=CONFIG["colors"]["data_color"]).move_to(axes.coords_to_point(-1, -1) + UP*0.5)
        cluster2_label = Text("Cluster B", font_size=20, color=CONFIG["colors"]["data_color"]).move_to(axes.coords_to_point(1, 1) + UP*0.5)
        
        self.play(Write(cluster1_label), Write(cluster2_label))
        
        # Add insight text
        insight = Text("Reveals natural clustering in data", 
                      font_size=CONFIG["font_sizes"]["subtext"], 
                      color=CONFIG["colors"]["highlight_color"],
                      slant=ITALIC)
        insight.next_to(axes, DOWN, buff=0.3)
        
        self.play(Write(insight))
        self.wait(2)
        
        # Store for later
        self.axes = axes
        self.x_label = x_label
        self.y_label = y_label
        self.dots = dots
        self.cluster1_label = cluster1_label
        self.cluster2_label = cluster2_label
        self.insight = insight

    def show_feature_generation(self):
        # Fade out EDA elements
        self.play(FadeOut(self.eda_explanation), FadeOut(self.axes), FadeOut(self.x_label), 
                 FadeOut(self.y_label), FadeOut(self.dots), FadeOut(self.cluster1_label), 
                 FadeOut(self.cluster2_label), FadeOut(self.insight))
        
        # Feature Generation Section Title
        fg_title = Text("2. Feature Generation", 
                       font_size=CONFIG["font_sizes"]["header"], 
                       color=CONFIG["colors"]["feature_color"],
                       weight=BOLD)
        fg_title.to_edge(UP)
        self.play(Transform(self.intro_title, fg_title))
        
        # Feature generation explanation
        fg_explanation = VGroup(
            Text("Replace original variables with PCs", 
                 color=CONFIG["colors"]["primary_text"], 
                 font_size=CONFIG["font_sizes"]["text"]),
            Text("to reduce overfitting and improve prediction", 
                 color=CONFIG["colors"]["primary_text"], 
                 font_size=CONFIG["font_sizes"]["text"]),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        fg_explanation.next_to(fg_title, DOWN, buff=0.5)
        
        self.play(FadeIn(fg_explanation, shift=LEFT*0.3))
        self.wait(1)
        
        # Create feature transformation visualization
        self.create_feature_transformation()
        
        # Store for later
        self.fg_explanation = fg_explanation

    def create_feature_transformation(self):
        # Create transformation diagram
        # Original features
        original_title = Text("Original Features", 
                             font_size=CONFIG["font_sizes"]["subtext"], 
                             color=CONFIG["colors"]["primary_text"],
                             weight=BOLD)
        original_title.to_edge(LEFT).shift(UP*2)
        
        original_features = VGroup(
            Text("X₁ (Age)", color=CONFIG["colors"]["primary_text"], font_size=20),
            Text("X₂ (Income)", color=CONFIG["colors"]["primary_text"], font_size=20),
            Text("X₃ (Education)", color=CONFIG["colors"]["primary_text"], font_size=20),
            Text("X₄ (Location)", color=CONFIG["colors"]["primary_text"], font_size=20),
            Text("X₅ (Occupation)", color=CONFIG["colors"]["primary_text"], font_size=20),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        original_features.next_to(original_title, DOWN, buff=0.3)
        
        # PCA transformation arrow
        arrow = Arrow(LEFT*2, RIGHT*2, color=CONFIG["colors"]["pca_color"], buff=0.5)
        arrow.move_to(ORIGIN)
        
        # PCA label
        pca_label = Text("PCA", font_size=24, color=CONFIG["colors"]["pca_color"], weight=BOLD)
        pca_label.next_to(arrow, UP)
        
        # Principal components
        pc_title = Text("Principal Components", 
                       font_size=CONFIG["font_sizes"]["subtext"], 
                       color=CONFIG["colors"]["feature_color"],
                       weight=BOLD)
        pc_title.to_edge(RIGHT).shift(UP*2)
        
        pc_features = VGroup(
            Text("PC₁ (Main Component)", color=CONFIG["colors"]["feature_color"], font_size=20),
            Text("PC₂ (Secondary)", color=CONFIG["colors"]["feature_color"], font_size=20),
            Text("PC₃ (Tertiary)", color=CONFIG["colors"]["feature_color"], font_size=20),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        pc_features.next_to(pc_title, DOWN, buff=0.3)
        
        # Show original features
        self.play(FadeIn(original_title), FadeIn(original_features, shift=LEFT*0.3))
        self.wait(1)
        
        # Show transformation
        self.play(Create(arrow), Write(pca_label))
        self.wait(1)
        
        # Show principal components
        self.play(FadeIn(pc_title), FadeIn(pc_features, shift=RIGHT*0.3))
        self.wait(1)
        
        # Add benefits
        benefits = VGroup(
            Text("Benefits:", font_size=CONFIG["font_sizes"]["subtext"], 
                 color=CONFIG["colors"]["highlight_color"], weight=BOLD),
            Text("• Reduced dimensionality", color=CONFIG["colors"]["primary_text"], font_size=20),
            Text("• Less overfitting", color=CONFIG["colors"]["primary_text"], font_size=20),
            Text("• Better model performance", color=CONFIG["colors"]["primary_text"], font_size=20),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        benefits.to_edge(DOWN, buff=0.5)
        
        self.play(FadeIn(benefits, shift=UP*0.3))
        self.wait(2)
        
        # Store for later
        self.original_title = original_title
        self.original_features = original_features
        self.arrow = arrow
        self.pca_label = pca_label
        self.pc_title = pc_title
        self.pc_features = pc_features
        self.benefits = benefits

    def show_comparison(self):
        # Fade out feature generation elements
        self.play(FadeOut(self.fg_explanation), FadeOut(self.original_title), 
                 FadeOut(self.original_features), FadeOut(self.arrow), 
                 FadeOut(self.pca_label), FadeOut(self.pc_title), 
                 FadeOut(self.pc_features), FadeOut(self.benefits))
        
        # Comparison section
        comparison_title = Text("Comparison of Applications", 
                               font_size=CONFIG["font_sizes"]["header"], 
                               color=CONFIG["colors"]["primary_text"],
                               weight=BOLD)
        comparison_title.to_edge(UP)
        self.play(Transform(self.intro_title, comparison_title))
        
        # Create comparison table
        self.create_comparison_table()

    def create_comparison_table(self):
        # Create comparison table
        table_width = 10
        table_height = 3
        
        # Table structure
        table = VGroup()
        
        # Horizontal lines
        for i in range(4):
            h_line = Line(LEFT * table_width/2, RIGHT * table_width/2, color=CONFIG["colors"]["primary_text"])
            h_line.move_to(UP * (table_height/2 - i * table_height/3))
            table.add(h_line)
        
        # Vertical lines
        for i in range(3):
            v_line = Line(UP * table_height/2, DOWN * table_height/2, color=CONFIG["colors"]["primary_text"])
            v_line.move_to(LEFT * table_width/2 + i * table_width/2)
            table.add(v_line)
        
        # Headers
        aspect_header = Text("Aspect", font_size=24, color=CONFIG["colors"]["highlight_color"], weight=BOLD)
        aspect_header.move_to(LEFT * table_width/3)
        
        eda_header = Text("EDA", font_size=24, color=CONFIG["colors"]["eda_color"], weight=BOLD)
        eda_header.move_to(RIGHT * 0)
        
        fg_header = Text("Feature Generation", font_size=24, color=CONFIG["colors"]["feature_color"], weight=BOLD)
        fg_header.move_to(RIGHT * table_width/3)
        
        # Row 1: Purpose
        purpose_label = Text("Purpose", font_size=20, color=CONFIG["colors"]["primary_text"], weight=BOLD)
        purpose_label.move_to(LEFT * table_width/3 + UP * table_height/6)
        
        eda_purpose = Text("Data exploration\n& visualization", font_size=18, color=CONFIG["colors"]["primary_text"])
        eda_purpose.move_to(RIGHT * 0 + UP * table_height/6)
        
        fg_purpose = Text("Model improvement\n& prediction", font_size=18, color=CONFIG["colors"]["primary_text"])
        fg_purpose.move_to(RIGHT * table_width/3 + UP * table_height/6)
        
        # Row 2: Output
        output_label = Text("Output", font_size=20, color=CONFIG["colors"]["primary_text"], weight=BOLD)
        output_label.move_to(LEFT * table_width/3 + DOWN * table_height/6)
        
        eda_output = Text("2D scatter plots\n(PC1 vs PC2)", font_size=18, color=CONFIG["colors"]["primary_text"])
        eda_output.move_to(RIGHT * 0 + DOWN * table_height/6)
        
        fg_output = Text("New feature set\n(PC1, PC2, ...)", font_size=18, color=CONFIG["colors"]["primary_text"])
        fg_output.move_to(RIGHT * table_width/3 + DOWN * table_height/6)
        
        # Add all elements to table
        table_elements = VGroup(
            aspect_header, eda_header, fg_header,
            purpose_label, eda_purpose, fg_purpose,
            output_label, eda_output, fg_output
        )
        
        table.scale(0.8).move_to(ORIGIN)
        table_elements.scale(0.8).move_to(ORIGIN)
        
        self.play(Create(table))
        self.play(FadeIn(table_elements, shift=UP*0.2))
        self.wait(2)
        
        # Store for later
        self.comparison_table = table
        self.table_elements = table_elements

    def show_summary(self):
        # Fade out comparison
        self.play(FadeOut(self.comparison_table), FadeOut(self.table_elements))
        
        # Summary section
        summary_title = Text("Summary", 
                            font_size=CONFIG["font_sizes"]["header"], 
                            color=CONFIG["colors"]["primary_text"],
                            weight=BOLD)
        summary_title.to_edge(UP)
        self.play(Transform(self.intro_title, summary_title))
        
        # Summary points
        summary_points = VGroup(
            Text("• EDA: Visualize data structure in 2D", 
                 color=CONFIG["colors"]["primary_text"], 
                 font_size=CONFIG["font_sizes"]["text"]),
            Text("• Feature Generation: Improve model performance", 
                 color=CONFIG["colors"]["primary_text"], 
                 font_size=CONFIG["font_sizes"]["text"]),
            Text("• Both leverage PCA's dimensionality reduction", 
                 color=CONFIG["colors"]["primary_text"], 
                 font_size=CONFIG["font_sizes"]["text"]),
            Text("• Choose based on analysis goals", 
                 color=CONFIG["colors"]["primary_text"], 
                 font_size=CONFIG["font_sizes"]["text"]),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        summary_points.next_to(summary_title, DOWN, buff=0.8)
        
        self.play(FadeIn(summary_points, shift=LEFT*0.3))
        self.wait(2)
        
        # Final fade out
        self.play(FadeOut(VGroup(self.intro_title, summary_points)))
        self.wait(1)
