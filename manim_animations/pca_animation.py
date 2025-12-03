from manim import *
import numpy as np
from sklearn.decomposition import PCA

# Data generation function (copied from data_generator.py for self-containment)
def generate_pca_data(n_samples=200, random_seed=42):
    np.random.seed(random_seed)
    x = np.random.normal(loc=5, scale=2, size=n_samples)
    y = 0.8 * x + np.random.normal(loc=0, scale=0.5, size=n_samples)
    return np.array([[x[i], y[i]] for i in range(n_samples)])

class PCAAnimation(Scene):
    def construct(self):
        self.next_section("Introduction")
        title = Text("Principal Component Analysis (PCA) Animation").to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Generate data
        data = generate_pca_data(n_samples=100)
        
        # Scale data for Manim coordinates
        scaled_data = (data - np.mean(data, axis=0)) / np.std(data, axis=0) * 2
        scaled_data += np.array([0, 0]) # Center around origin
        
        # Convert to 3D coordinates for Manim
        scaled_data_3d = np.column_stack([scaled_data, np.zeros(len(scaled_data))])

        points_mobjects = VGroup(*[Dot(point, color=BLUE) for point in scaled_data_3d])
        self.play(FadeIn(points_mobjects))
        self.wait(1)

        # Calculate Mean
        self.next_section("Mean")
        mean_text = Text("Calculate Mean").to_edge(UP).shift(DOWN*0.5)
        self.play(FadeOut(title), Write(mean_text))
        
        data_mean = np.mean(scaled_data, axis=0)
        mean_dot_3d = np.append(data_mean, 0)  # Convert to 3D
        mean_dot = Dot(mean_dot_3d, color=RED, radius=0.15)
        self.play(FadeIn(mean_dot))
        self.wait(1)

        # Perform PCA
        self.next_section("PerformPCA")
        pca_text = Text("Perform PCA").next_to(mean_text, DOWN)
        self.play(FadeOut(mean_text), Write(pca_text))

        pca = PCA(n_components=2)
        pca.fit(scaled_data)

        # Display Principal Components (Eigenvectors)
        pc1 = pca.components_[0]
        pc2 = pca.components_[1]

        pc1_start_3d = np.append(data_mean - pc1 * 3, 0)
        pc1_end_3d = np.append(data_mean + pc1 * 3, 0)
        pc2_start_3d = np.append(data_mean - pc2 * 3, 0)
        pc2_end_3d = np.append(data_mean + pc2 * 3, 0)
        
        pc1_line = Line(pc1_start_3d, pc1_end_3d, color=GREEN, stroke_width=5)
        pc2_line = Line(pc2_start_3d, pc2_end_3d, color=YELLOW, stroke_width=5)

        pc1_label = Text("PC1").next_to(pc1_line, UP)
        pc2_label = Text("PC2").next_to(pc2_line, RIGHT)

        self.play(Create(pc1_line), Write(pc1_label))
        self.play(Create(pc2_line), Write(pc2_label))
        self.wait(1)

        # Project data onto PC1
        self.next_section("Projection")
        proj_text = Text("Project Data onto PC1").next_to(pca_text, DOWN)
        self.play(FadeOut(pca_text), Write(proj_text))

        projected_points_pc1 = []
        for point in scaled_data:
            vec = point - data_mean
            proj = np.dot(vec, pc1) * pc1 + data_mean
            proj_3d = np.append(proj, 0)  # Convert to 3D
            projected_points_pc1.append(proj_3d)

        projected_mobjects_pc1 = VGroup(*[Dot(point, color=ORANGE) for point in projected_points_pc1])
        
        animations = []
        for i in range(len(points_mobjects)):
            animations.append(Transform(points_mobjects[i], projected_mobjects_pc1[i]))
        self.play(*animations)
        self.wait(1)

        # Show transformed data (optional, for 2D to 1D reduction)
        self.next_section("TransformedData")
        transformed_text = Text("Transformed Data (1D)").next_to(proj_text, DOWN)
        self.play(FadeOut(proj_text), Write(transformed_text))

        # For 2D to 1D, we can just show them along the PC1 line
        # The points are already projected, just need to recolor and maybe remove PC2
        self.play(FadeOut(pc2_line), FadeOut(pc2_label))
        for point_mobject in points_mobjects:
            point_mobject.set_color(ORANGE)
        self.wait(2)

        self.next_section("Conclusion")
        final_text = Text("PCA Complete").to_edge(UP)
        self.play(FadeOut(transformed_text), FadeOut(pc1_line), FadeOut(pc1_label), FadeOut(mean_dot), FadeOut(points_mobjects), Write(final_text))
        self.wait(2)
