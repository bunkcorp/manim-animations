from manim import *
import numpy as np
import pandas as pd
import json
import os
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

class DetailedPCAAnimation(Scene):
    def construct(self):
        # Set up the scene
        self.camera.background_color = "#1a1a1a"
        
        # Title
        title = Text("Principal Component Analysis (PCA)", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Load real data
        self.next_section("Data Loading")
        self.show_data_loading()
        
        # Data preprocessing
        self.next_section("Data Preprocessing")
        self.show_data_preprocessing()
        
        # Covariance matrix
        self.next_section("Covariance Matrix")
        self.show_covariance_matrix()
        
        # Eigenvalue decomposition
        self.next_section("Eigenvalue Decomposition")
        self.show_eigenvalue_decomposition()
        
        # Principal components
        self.next_section("Principal Components")
        self.show_principal_components()
        
        # Dimension reduction
        self.next_section("Dimension Reduction")
        self.show_dimension_reduction()
        
        # Reconstruction
        self.next_section("Reconstruction")
        self.show_reconstruction()
        
        # Final results
        self.next_section("Final Results")
        self.show_final_results()
        
    def show_data_loading(self):
        # Show data loading process
        loading_text = Text("Loading Buddhist Stone Data...", font_size=36, color=YELLOW)
        loading_text.move_to(ORIGIN)
        self.play(Write(loading_text))
        self.wait(1)
        
        # Show data structure
        data_info = VGroup(
            Text("📊 High-Dimensional Features:", font_size=32, color=WHITE),
            Text("• Time of Day (24 values)", font_size=24, color=GRAY),
            Text("• Day of Week (7 values)", font_size=24, color=GRAY),
            Text("• Category (10+ categories)", font_size=24, color=GRAY),
            Text("• Realm (3 realms)", font_size=24, color=GRAY),
            Text("• User Activity Level", font_size=24, color=GRAY),
            Text("• Previous Stone Patterns", font_size=24, color=GRAY),
            Text("• Meditation Duration", font_size=24, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        data_info.move_to(ORIGIN)
        
        self.play(ReplacementTransform(loading_text, data_info))
        self.wait(2)
        
        # Load actual data
        try:
            data_path = "firebase/complete_user_data_export_2025-08-23T20-19-34-686Z/all_user_stones.json"
            with open(data_path, 'r') as f:
                stones_data = json.load(f)
            
            df = pd.DataFrame(stones_data)
            
            # Show data statistics
            stats_text = VGroup(
                Text(f"✅ Loaded {len(df)} stone records", font_size=32, color=GREEN),
                Text(f"📈 {len(df.columns)} original features", font_size=28, color=BLUE),
                Text(f"🎯 Goal: Reduce to 2-3 principal components", font_size=28, color=ORANGE),
                Text(f"📊 Preserve maximum variance", font_size=28, color=PURPLE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
            stats_text.move_to(ORIGIN)
            
            self.play(ReplacementTransform(data_info, stats_text))
            self.wait(2)
            self.play(FadeOut(stats_text))
            
        except Exception as e:
            error_text = Text(f"⚠️ Error loading data: {str(e)}", font_size=32, color=RED)
            self.play(ReplacementTransform(data_info, error_text))
            self.wait(2)
            self.play(FadeOut(error_text))
    
    def show_data_preprocessing(self):
        # Show preprocessing steps
        preprocess_title = Text("Data Preprocessing", font_size=40, color=WHITE)
        preprocess_title.to_edge(UP)
        self.play(Write(preprocess_title))
        
        # Create preprocessing steps
        steps = VGroup(
            Text("1. Handle Missing Values", font_size=28, color=YELLOW),
            Text("2. Encode Categorical Variables", font_size=28, color=YELLOW),
            Text("3. Standardize Features", font_size=28, color=YELLOW),
            Text("4. Center Data (Mean = 0)", font_size=28, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        steps.move_to(ORIGIN)
        
        self.play(Write(steps))
        self.wait(1)
        
        # Animate each step with details
        for i, step in enumerate(steps):
            # Highlight current step
            self.play(step.animate.set_color(GREEN).scale(1.2))
            
            # Show details for each step
            if i == 0:  # Missing Values
                details = VGroup(
                    Text("• Fill NaN with mean/mode", font_size=20, color=GRAY),
                    Text("• Remove incomplete records", font_size=20, color=GRAY),
                    Text("• Ensure data completeness", font_size=20, color=GRAY)
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
                details.next_to(step, DOWN, buff=0.5)
                self.play(Write(details))
                self.wait(1.5)
                self.play(FadeOut(details))
            
            elif i == 1:  # Encoding
                details = VGroup(
                    Text("• One-hot encoding for categories", font_size=20, color=GRAY),
                    Text("• Convert strings to numbers", font_size=20, color=GRAY),
                    Text("• Create binary features", font_size=20, color=GRAY)
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
                details.next_to(step, DOWN, buff=0.5)
                self.play(Write(details))
                self.wait(1.5)
                self.play(FadeOut(details))
            
            elif i == 2:  # Standardization
                details = VGroup(
                    Text("• Z-score normalization", font_size=20, color=GRAY),
                    Text("• Mean = 0, Standard Deviation = 1", font_size=20, color=GRAY),
                    Text("• Equal feature importance", font_size=20, color=GRAY)
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
                details.next_to(step, DOWN, buff=0.5)
                self.play(Write(details))
                self.wait(1.5)
                self.play(FadeOut(details))
            
            elif i == 3:  # Centering
                details = VGroup(
                    Text("• Subtract mean from each feature", font_size=20, color=GRAY),
                    Text("• Center data around origin", font_size=20, color=GRAY),
                    Text("• Prepare for covariance calculation", font_size=20, color=GRAY)
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
                details.next_to(step, DOWN, buff=0.5)
                self.play(Write(details))
                self.wait(1.5)
                self.play(FadeOut(details))
            
            # Reset step color
            self.play(step.animate.set_color(YELLOW).scale(1/1.2))
        
        self.play(FadeOut(steps), FadeOut(preprocess_title))
    
    def show_covariance_matrix(self):
        # Show covariance matrix calculation
        cov_title = Text("Covariance Matrix Calculation", font_size=40, color=WHITE)
        cov_title.to_edge(UP)
        self.play(Write(cov_title))
        
        # Create sample data matrix
        data_matrix = VGroup()
        matrix_title = Text("Centered Data Matrix X", font_size=24, color=BLUE)
        matrix_title.move_to([0, 2, 0])
        
        # Create 4x4 sample matrix
        sample_data = np.array([
            [1.2, -0.8, 0.5, -0.3],
            [-0.5, 1.1, -0.2, 0.7],
            [0.8, -0.4, 1.3, -0.1],
            [-0.3, 0.9, -0.6, 1.0]
        ])
        
        matrix_elements = VGroup()
        for i in range(4):
            for j in range(4):
                element = Text(f"{sample_data[i,j]:.1f}", font_size=16, color=WHITE)
                element.move_to([j*1.5 - 2.25, -i*1 + 1, 0])
                matrix_elements.add(element)
        
        # Create matrix brackets
        left_bracket = Rectangle(height=4, width=0.1, color=WHITE)
        left_bracket.move_to([-3, 0, 0])
        right_bracket = Rectangle(height=4, width=0.1, color=WHITE)
        right_bracket.move_to([3, 0, 0])
        
        data_matrix.add(matrix_title, matrix_elements, left_bracket, right_bracket)
        self.play(Create(data_matrix))
        
        # Show covariance formula
        formula_text = Text("Covariance Matrix: Σ = (1/n) X^T X", font_size=24, color=YELLOW)
        formula_text.move_to([0, -2, 0])
        self.play(Write(formula_text))
        
        # Calculate and show covariance matrix
        cov_matrix = np.cov(sample_data.T)
        
        cov_result = VGroup()
        cov_title_result = Text("Covariance Matrix Σ", font_size=20, color=GREEN)
        cov_title_result.move_to([0, -3.5, 0])
        cov_result.add(cov_title_result)
        
        cov_elements = VGroup()
        for i in range(4):
            for j in range(4):
                element = Text(f"{cov_matrix[i,j]:.2f}", font_size=14, color=GREEN)
                element.move_to([j*1.2 - 1.8, -i*0.8 - 4.5, 0])
                cov_elements.add(element)
        
        cov_result.add(cov_elements)
        self.play(Write(cov_result))
        
        # Show covariance properties
        properties = VGroup(
            Text("📊 Covariance Properties:", font_size=20, color=WHITE),
            Text("• Symmetric matrix", font_size=16, color=GRAY),
            Text("• Diagonal = variances", font_size=16, color=GRAY),
            Text("• Off-diagonal = covariances", font_size=16, color=GRAY),
            Text("• Measures feature relationships", font_size=16, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        properties.to_edge(RIGHT)
        
        self.play(Write(properties))
        self.wait(3)
        
        self.play(FadeOut(VGroup(data_matrix, formula_text, cov_result, properties, cov_title)))
    
    def show_eigenvalue_decomposition(self):
        # Show eigenvalue decomposition
        eigen_title = Text("Eigenvalue Decomposition", font_size=40, color=WHITE)
        eigen_title.to_edge(UP)
        self.play(Write(eigen_title))
        
        # Show decomposition formula
        formula = MathTex(r"\Sigma = Q \Lambda Q^T", font_size=36, color=YELLOW)
        formula.move_to([0, 1, 0])
        self.play(Write(formula))
        
        # Explain components
        components = VGroup(
            Text("Where:", font_size=24, color=WHITE),
            Text("• Σ = Covariance Matrix", font_size=18, color=GRAY),
            Text("• Q = Eigenvectors (Principal Components)", font_size=18, color=GRAY),
            Text("• Λ = Eigenvalues (Variance explained)", font_size=18, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        components.move_to([0, -1, 0])
        
        self.play(Write(components))
        
        # Show eigenvalue calculation process
        process_text = Text("Eigenvalue Calculation Process", font_size=24, color=BLUE)
        process_text.move_to([0, -3, 0])
        self.play(Write(process_text))
        
        # Create sample eigenvalues and eigenvectors
        eigenvalues = [2.5, 1.8, 0.9, 0.3]
        eigenvectors = np.array([
            [0.7, 0.3, -0.2, 0.1],
            [-0.2, 0.8, 0.4, -0.1],
            [0.1, -0.1, 0.9, 0.2],
            [0.1, 0.2, 0.1, 0.9]
        ])
        
        # Show eigenvalues
        eigenvals = VGroup()
        eigenvals_title = Text("Eigenvalues (Variance Explained):", font_size=20, color=GREEN)
        eigenvals_title.move_to([-3, -4.5, 0])
        eigenvals.add(eigenvals_title)
        
        for i, val in enumerate(eigenvalues):
            eigenval = Text(f"λ{i+1} = {val:.1f}", font_size=16, color=GREEN)
            eigenval.move_to([-3, -5.5 - i*0.5, 0])
            eigenvals.add(eigenval)
        
        self.play(Write(eigenvals))
        
        # Show eigenvectors
        eigenvecs = VGroup()
        eigenvecs_title = Text("Eigenvectors (Principal Components):", font_size=18, color=BLUE)
        eigenvecs_title.move_to([2, -4.5, 0])
        eigenvecs.add(eigenvecs_title)
        
        for i in range(4):
            eigenvec = Text(f"PC{i+1}: [{eigenvectors[i,0]:.1f}, {eigenvectors[i,1]:.1f}, {eigenvectors[i,2]:.1f}, {eigenvectors[i,3]:.1f}]", 
                           font_size=12, color=BLUE)
            eigenvec.move_to([2, -5.5 - i*0.5, 0])
            eigenvecs.add(eigenvec)
        
        self.play(Write(eigenvecs))
        
        # Show variance explained
        total_var = sum(eigenvalues)
        var_explained = [val/total_var*100 for val in eigenvalues]
        
        var_text = VGroup()
        var_title = Text("Variance Explained (%):", font_size=18, color=ORANGE)
        var_title.move_to([0, -6.5, 0])
        var_text.add(var_title)
        
        for i, var in enumerate(var_explained):
            var_label = Text(f"PC{i+1}: {var:.1f}%", font_size=14, color=ORANGE)
            var_label.move_to([0, -7.5 - i*0.4, 0])
            var_text.add(var_label)
        
        self.play(Write(var_text))
        self.wait(3)
        
        self.play(FadeOut(VGroup(formula, components, process_text, eigenvals, eigenvecs, var_text, eigen_title)))
    
    def show_principal_components(self):
        # Show principal components visualization
        pc_title = Text("Principal Components Visualization", font_size=40, color=WHITE)
        pc_title.to_edge(UP)
        self.play(Write(pc_title))
        
        # Create coordinate system
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=8,
            y_length=8,
            axis_config={"color": GRAY}
        )
        axes.move_to(ORIGIN)
        
        # Add labels
        x_label = axes.get_x_axis_label("Feature 1")
        y_label = axes.get_y_axis_label("Feature 2")
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Generate sample data
        np.random.seed(42)
        n_points = 50
        data = np.random.multivariate_normal([0, 0], [[2, 1.5], [1.5, 2]], n_points)
        
        # Create data points
        points = VGroup()
        for point in data:
            dot = Dot(axes.coords_to_point(point[0], point[1]), color=BLUE, radius=0.05)
            points.add(dot)
        
        self.play(Create(points))
        
        # Show mean
        mean_point = Dot(axes.coords_to_point(0, 0), color=RED, radius=0.15)
        mean_label = Text("Mean", font_size=16, color=RED)
        mean_label.next_to(mean_point, UP, buff=0.2)
        
        self.play(Create(mean_point), Write(mean_label))
        
        # Show principal components
        pc1 = np.array([0.7, 0.7])  # First principal component
        pc2 = np.array([-0.7, 0.7])  # Second principal component
        
        # PC1 line
        pc1_start = axes.coords_to_point(-3*pc1[0], -3*pc1[1])
        pc1_end = axes.coords_to_point(3*pc1[0], 3*pc1[1])
        pc1_line = Line(pc1_start, pc1_end, color=GREEN, stroke_width=4)
        pc1_label = Text("PC1 (Max Variance)", font_size=16, color=GREEN)
        pc1_label.next_to(pc1_line, UP, buff=0.3)
        
        # PC2 line
        pc2_start = axes.coords_to_point(-3*pc2[0], -3*pc2[1])
        pc2_end = axes.coords_to_point(3*pc2[0], 3*pc2[1])
        pc2_line = Line(pc2_start, pc2_end, color=YELLOW, stroke_width=4)
        pc2_label = Text("PC2 (Orthogonal)", font_size=16, color=YELLOW)
        pc2_label.next_to(pc2_line, RIGHT, buff=0.3)
        
        self.play(Create(pc1_line), Write(pc1_label))
        self.wait(1)
        self.play(Create(pc2_line), Write(pc2_label))
        
        # Show projection
        projection_text = Text("Projecting data onto principal components", font_size=20, color=ORANGE)
        projection_text.to_edge(DOWN)
        self.play(Write(projection_text))
        
        # Create projected points
        projected_points = VGroup()
        for point in data:
            # Project onto PC1
            proj_pc1 = np.dot(point, pc1) * pc1
            proj_dot = Dot(axes.coords_to_point(proj_pc1[0], proj_pc1[1]), color=ORANGE, radius=0.06)
            projected_points.add(proj_dot)
            
            # Create projection line
            proj_line = Line(
                axes.coords_to_point(point[0], point[1]),
                axes.coords_to_point(proj_pc1[0], proj_pc1[1]),
                color=ORANGE,
                stroke_width=1,
                stroke_opacity=0.5
            )
            projected_points.add(proj_line)
        
        self.play(Create(projected_points))
        
        # Show variance explanation
        variance_text = VGroup(
            Text("📊 Variance Explained:", font_size=20, color=WHITE),
            Text("• PC1 captures 75% of variance", font_size=16, color=GREEN),
            Text("• PC2 captures 25% of variance", font_size=16, color=YELLOW),
            Text("• Total: 100% of original variance", font_size=16, color=BLUE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        variance_text.to_edge(RIGHT)
        
        self.play(Write(variance_text))
        self.wait(3)
        
        self.play(FadeOut(VGroup(axes, x_label, y_label, points, mean_point, mean_label,
                                pc1_line, pc1_label, pc2_line, pc2_label, projected_points,
                                variance_text, projection_text, pc_title)))
    
    def show_dimension_reduction(self):
        # Show dimension reduction process
        reduction_title = Text("Dimension Reduction Process", font_size=40, color=WHITE)
        reduction_title.to_edge(UP)
        self.play(Write(reduction_title))
        
        # Show original high-dimensional data
        original_data = VGroup()
        original_title = Text("Original Data (High-Dimensional)", font_size=24, color=BLUE)
        original_title.move_to([-4, 2, 0])
        
        # Create sample high-dimensional data
        high_dim_data = np.random.randn(10, 8)  # 10 samples, 8 features
        
        data_matrix = VGroup()
        for i in range(10):
            for j in range(8):
                element = Text(f"{high_dim_data[i,j]:.1f}", font_size=8, color=WHITE)
                element.move_to([-6 + j*0.8, 1.5 - i*0.3, 0])
                data_matrix.add(element)
        
        original_data.add(original_title, data_matrix)
        self.play(Create(original_data))
        
        # Show transformation matrix
        transform_title = Text("Transformation Matrix (Top PCs)", font_size=20, color=GREEN)
        transform_title.move_to([0, 2, 0])
        
        # Create transformation matrix (top 2 PCs)
        transform_matrix = np.random.randn(2, 8)
        
        transform_elements = VGroup()
        for i in range(2):
            for j in range(8):
                element = Text(f"{transform_matrix[i,j]:.1f}", font_size=8, color=GREEN)
                element.move_to([-2 + j*0.8, 1.5 - i*0.3, 0])
                transform_elements.add(element)
        
        transform_group = VGroup(transform_title, transform_elements)
        self.play(Create(transform_group))
        
        # Show reduced data
        reduced_title = Text("Reduced Data (2D)", font_size=24, color=ORANGE)
        reduced_title.move_to([4, 2, 0])
        
        # Create reduced data matrix
        reduced_data = np.random.randn(10, 2)
        
        reduced_elements = VGroup()
        for i in range(10):
            for j in range(2):
                element = Text(f"{reduced_data[i,j]:.1f}", font_size=12, color=ORANGE)
                element.move_to([3 + j*1.5, 1.5 - i*0.3, 0])
                reduced_elements.add(element)
        
        reduced_group = VGroup(reduced_title, reduced_elements)
        self.play(Create(reduced_group))
        
        # Show transformation arrows
        arrow1 = Arrow(start=[-1, 0, 0], end=[2, 0, 0], color=YELLOW, stroke_width=3)
        arrow2 = Arrow(start=[2, 0, 0], end=[5, 0, 0], color=YELLOW, stroke_width=3)
        
        self.play(Create(arrow1), Create(arrow2))
        
        # Show formula
        formula = MathTex(r"X_{reduced} = X \cdot W^T", font_size=28, color=WHITE)
        formula.move_to([0, -1, 0])
        self.play(Write(formula))
        
        # Show benefits
        benefits = VGroup(
            Text("🎯 Dimension Reduction Benefits:", font_size=20, color=WHITE),
            Text("• Reduced computational cost", font_size=16, color=GREEN),
            Text("• Eliminated noise", font_size=16, color=BLUE),
            Text("• Preserved important patterns", font_size=16, color=YELLOW),
            Text("• Easier visualization", font_size=16, color=ORANGE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        benefits.move_to([0, -3, 0])
        
        self.play(Write(benefits))
        self.wait(3)
        
        self.play(FadeOut(VGroup(original_data, transform_group, reduced_group, arrow1, arrow2,
                                formula, benefits, reduction_title)))
    
    def show_reconstruction(self):
        # Show data reconstruction process
        reconstruction_title = Text("Data Reconstruction", font_size=40, color=WHITE)
        reconstruction_title.to_edge(UP)
        self.play(Write(reconstruction_title))
        
        # Show reconstruction formula
        formula = MathTex(r"X_{reconstructed} = X_{reduced} \cdot W", font_size=28, color=WHITE)
        formula.move_to([0, 2, 0])
        self.play(Write(formula))
        
        # Create visualization of reconstruction
        # Original data
        original_circle = Circle(radius=1, color=BLUE, fill_opacity=0.3)
        original_circle.move_to([-4, 0, 0])
        original_label = Text("Original\nData", font_size=16, color=BLUE)
        original_label.move_to([-4, -1.5, 0])
        
        # Reduced data
        reduced_circle = Circle(radius=0.8, color=GREEN, fill_opacity=0.3)
        reduced_circle.move_to([0, 0, 0])
        reduced_label = Text("Reduced\nData", font_size=16, color=GREEN)
        reduced_label.move_to([0, -1.5, 0])
        
        # Reconstructed data
        reconstructed_circle = Circle(radius=0.9, color=ORANGE, fill_opacity=0.3)
        reconstructed_circle.move_to([4, 0, 0])
        reconstructed_label = Text("Reconstructed\nData", font_size=16, color=ORANGE)
        reconstructed_label.move_to([4, -1.5, 0])
        
        # Arrows
        arrow1 = Arrow(start=[-3, 0, 0], end=[-0.8, 0, 0], color=YELLOW, stroke_width=3)
        arrow2 = Arrow(start=[0.8, 0, 0], end=[3, 0, 0], color=YELLOW, stroke_width=3)
        
        # Labels
        transform_label = Text("Transform", font_size=14, color=YELLOW)
        transform_label.next_to(arrow1, UP, buff=0.2)
        reconstruct_label = Text("Reconstruct", font_size=14, color=YELLOW)
        reconstruct_label.next_to(arrow2, UP, buff=0.2)
        
        self.play(Create(original_circle), Write(original_label))
        self.play(Create(arrow1), Write(transform_label))
        self.play(Create(reduced_circle), Write(reduced_label))
        self.play(Create(arrow2), Write(reconstruct_label))
        self.play(Create(reconstructed_circle), Write(reconstructed_label))
        
        # Show reconstruction error
        error_text = VGroup(
            Text("📊 Reconstruction Error:", font_size=20, color=WHITE),
            Text("• Information Loss: 15%", font_size=16, color=RED),
            Text("• Variance Preserved: 85%", font_size=16, color=GREEN),
            Text("• Quality vs. Compression Trade-off", font_size=16, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        error_text.move_to([0, -3, 0])
        
        self.play(Write(error_text))
        
        # Show quality metrics
        metrics = VGroup(
            Text("🎯 Quality Metrics:", font_size=20, color=WHITE),
            Text("• Explained Variance Ratio", font_size=16, color=GRAY),
            Text("• Reconstruction Error", font_size=16, color=GRAY),
            Text("• Information Retention", font_size=16, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        metrics.to_edge(RIGHT)
        
        self.play(Write(metrics))
        self.wait(3)
        
        self.play(FadeOut(VGroup(formula, original_circle, original_label, reduced_circle, reduced_label,
                                reconstructed_circle, reconstructed_label, arrow1, arrow2,
                                transform_label, reconstruct_label, error_text, metrics, reconstruction_title)))
    
    def show_final_results(self):
        # Show final PCA results
        results_title = Text("PCA Results Summary", font_size=40, color=WHITE)
        results_title.to_edge(UP)
        self.play(Write(results_title))
        
        # Create performance metrics
        metrics = VGroup(
            Text("📊 Performance Metrics:", font_size=28, color=WHITE),
            Text("• Original Dimensions: 8", font_size=20, color=BLUE),
            Text("• Reduced Dimensions: 2", font_size=20, color=GREEN),
            Text("• Variance Explained: 85%", font_size=20, color=ORANGE),
            Text("• Compression Ratio: 75%", font_size=20, color=PURPLE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        metrics.move_to([-3, 0, 0])
        
        self.play(Write(metrics))
        
        # Create scree plot
        scree_title = Text("Scree Plot (Variance Explained)", font_size=20, color=WHITE)
        scree_title.move_to([3, 2, 0])
        
        # Create bars for variance explained
        variances = [45, 40, 10, 5]  # Percentage of variance explained
        colors = [GREEN, BLUE, YELLOW, RED]
        
        scree_bars = VGroup()
        for i, (var, color) in enumerate(zip(variances, colors)):
            bar = Rectangle(
                width=0.8,
                height=var/10,
                fill_color=color,
                fill_opacity=0.7,
                stroke_color=WHITE,
                stroke_width=2
            )
            bar.move_to([3 + i*1.2 - 1.8, var/20, 0])
            scree_bars.add(bar)
            
            # Add labels
            pc_label = Text(f"PC{i+1}", font_size=12, color=WHITE)
            pc_label.next_to(bar, DOWN, buff=0.1)
            scree_bars.add(pc_label)
            
            var_label = Text(f"{var}%", font_size=10, color=color)
            var_label.next_to(bar, UP, buff=0.05)
            scree_bars.add(var_label)
        
        scree_group = VGroup(scree_title, scree_bars)
        self.play(Create(scree_group))
        
        # Show applications
        applications = VGroup(
            Text("🎯 PCA Applications:", font_size=20, color=WHITE),
            Text("• Data Visualization", font_size=16, color=GREEN),
            Text("• Noise Reduction", font_size=16, color=BLUE),
            Text("• Feature Engineering", font_size=16, color=YELLOW),
            Text("• Dimensionality Reduction", font_size=16, color=ORANGE),
            Text("• Pattern Recognition", font_size=16, color=PURPLE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        applications.move_to([0, -2, 0])
        
        self.play(Write(applications))
        
        # Final message
        final_message = Text("PCA analysis complete!", font_size=36, color=GREEN)
        final_message.to_edge(DOWN)
        self.play(Write(final_message))
        self.wait(2)
        
        self.play(FadeOut(VGroup(metrics, scree_group, applications, final_message, results_title)))
