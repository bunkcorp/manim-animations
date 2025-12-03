from manim import *
import numpy as np
import pandas as pd
import json
import os
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
# import matplotlib.pyplot as plt  # Removed to avoid numpy compatibility issues

class DetailedKMeansAnimation(Scene):
    def construct(self):
        # Set up the scene
        self.camera.background_color = "#1a1a1a"
        
        # Title
        title = Text("K-Means Clustering Algorithm", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Load real Buddhist stone data
        self.next_section("Data Loading")
        self.show_data_loading()
        
        # Data preprocessing
        self.next_section("Data Preprocessing")
        self.show_data_preprocessing()
        
        # Initialize centroids
        self.next_section("Centroid Initialization")
        self.show_centroid_initialization()
        
        # Main clustering loop
        self.next_section("Clustering Iterations")
        self.show_clustering_iterations()
        
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
            Text("📊 Data Structure:", font_size=32, color=WHITE),
            Text("• Stone Type (Black/White)", font_size=24, color=GRAY),
            Text("• Category (Virtue/Non-virtue)", font_size=24, color=GRAY),
            Text("• Realm (Body/Speech/Mind)", font_size=24, color=GRAY),
            Text("• Timestamp", font_size=24, color=GRAY),
            Text("• User ID", font_size=24, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        data_info.move_to(ORIGIN)
        
        self.play(ReplacementTransform(loading_text, data_info))
        self.wait(2)
        
        # Show data loading animation
        self.play(FadeOut(data_info))
        
        # Load actual data
        try:
            data_path = "firebase/complete_user_data_export_2025-08-23T20-19-34-686Z/all_user_stones.json"
            with open(data_path, 'r') as f:
                stones_data = json.load(f)
            
            df = pd.DataFrame(stones_data)
            
            # Show data statistics
            stats_text = VGroup(
                Text(f"✅ Loaded {len(df)} stone records", font_size=32, color=GREEN),
                Text(f"📈 {len(df.columns)} features", font_size=28, color=BLUE),
                Text(f"🎯 Target: Stone Type Classification", font_size=28, color=ORANGE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
            stats_text.move_to(ORIGIN)
            
            self.play(Write(stats_text))
            self.wait(2)
            self.play(FadeOut(stats_text))
            
        except Exception as e:
            error_text = Text(f"⚠️ Error loading data: {str(e)}", font_size=32, color=RED)
            self.play(Write(error_text))
            self.wait(2)
            self.play(FadeOut(error_text))
    
    def show_data_preprocessing(self):
        # Show preprocessing steps
        preprocess_title = Text("Data Preprocessing", font_size=40, color=WHITE)
        preprocess_title.to_edge(UP)
        self.play(Write(preprocess_title))
        
        # Create a grid to show preprocessing steps
        steps = VGroup(
            Text("1. Feature Engineering", font_size=28, color=YELLOW),
            Text("2. Data Cleaning", font_size=28, color=YELLOW),
            Text("3. Normalization", font_size=28, color=YELLOW),
            Text("4. Dimensionality Selection", font_size=28, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        steps.move_to(ORIGIN)
        
        self.play(Write(steps))
        self.wait(1)
        
        # Animate each step
        for i, step in enumerate(steps):
            # Highlight current step
            self.play(step.animate.set_color(GREEN).scale(1.2))
            
            # Show details for each step
            if i == 0:  # Feature Engineering
                details = VGroup(
                    Text("• Convert categorical to numerical", font_size=20, color=GRAY),
                    Text("• Create time-based features", font_size=20, color=GRAY),
                    Text("• Extract stone patterns", font_size=20, color=GRAY)
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
                details.next_to(step, DOWN, buff=0.5)
                self.play(Write(details))
                self.wait(1.5)
                self.play(FadeOut(details))
            
            elif i == 1:  # Data Cleaning
                details = VGroup(
                    Text("• Remove missing values", font_size=20, color=GRAY),
                    Text("• Handle outliers", font_size=20, color=GRAY),
                    Text("• Validate data integrity", font_size=20, color=GRAY)
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
                details.next_to(step, DOWN, buff=0.5)
                self.play(Write(details))
                self.wait(1.5)
                self.play(FadeOut(details))
            
            elif i == 2:  # Normalization
                details = VGroup(
                    Text("• Standardize features", font_size=20, color=GRAY),
                    Text("• Scale to [0,1] range", font_size=20, color=GRAY),
                    Text("• Ensure equal importance", font_size=20, color=GRAY)
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
                details.next_to(step, DOWN, buff=0.5)
                self.play(Write(details))
                self.wait(1.5)
                self.play(FadeOut(details))
            
            elif i == 3:  # Dimensionality Selection
                details = VGroup(
                    Text("• Select relevant features", font_size=20, color=GRAY),
                    Text("• Reduce noise", font_size=20, color=GRAY),
                    Text("• Optimize for clustering", font_size=20, color=GRAY)
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
                details.next_to(step, DOWN, buff=0.5)
                self.play(Write(details))
                self.wait(1.5)
                self.play(FadeOut(details))
            
            # Reset step color
            self.play(step.animate.set_color(YELLOW).scale(1/1.2))
        
        self.play(FadeOut(steps), FadeOut(preprocess_title))
    
    def show_centroid_initialization(self):
        # Show centroid initialization
        init_title = Text("Centroid Initialization", font_size=40, color=WHITE)
        init_title.to_edge(UP)
        self.play(Write(init_title))
        
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
        
        # Generate sample data points
        np.random.seed(42)
        n_points = 100
        data = np.random.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], n_points)
        
        # Create data points
        points = VGroup()
        for point in data:
            dot = Dot(axes.coords_to_point(point[0], point[1]), color=BLUE, radius=0.05)
            points.add(dot)
        
        self.play(Create(points))
        self.wait(1)
        
        # Show different initialization methods
        methods = ["Random", "K-Means++", "Manual Selection"]
        colors = [RED, GREEN, YELLOW]
        
        for i, (method, color) in enumerate(zip(methods, colors)):
            # Show method name
            method_text = Text(f"Method: {method}", font_size=32, color=color)
            method_text.to_edge(DOWN)
            self.play(Write(method_text))
            
            # Initialize centroids
            if method == "Random":
                centroids = np.random.choice(range(n_points), 3, replace=False)
                centroid_positions = data[centroids]
            elif method == "K-Means++":
                # Simplified K-Means++ initialization
                centroids = [0, n_points//3, 2*n_points//3]
                centroid_positions = data[centroids]
            else:  # Manual
                centroid_positions = np.array([[-2, -2], [0, 2], [2, -2]])
            
            # Create centroid dots
            centroid_dots = VGroup()
            for j, pos in enumerate(centroid_positions):
                centroid_dot = Dot(
                    axes.coords_to_point(pos[0], pos[1]), 
                    color=color, 
                    radius=0.15
                )
                centroid_dots.add(centroid_dot)
                
                # Add centroid label
                label = Text(f"C{j+1}", font_size=20, color=color)
                label.next_to(centroid_dot, UP, buff=0.1)
                centroid_dots.add(label)
            
            self.play(Create(centroid_dots))
            self.wait(2)
            
            # Show assignment lines
            if method != "Manual":
                assignment_lines = VGroup()
                for point_idx, point in enumerate(data):
                    distances = [np.linalg.norm(point - centroid) for centroid in centroid_positions]
                    closest_centroid = np.argmin(distances)
                    
                    line = Line(
                        axes.coords_to_point(point[0], point[1]),
                        axes.coords_to_point(centroid_positions[closest_centroid][0], 
                                           centroid_positions[closest_centroid][1]),
                        color=color,
                        stroke_width=1,
                        stroke_opacity=0.3
                    )
                    assignment_lines.add(line)
                
                self.play(Create(assignment_lines))
                self.wait(1)
                self.play(FadeOut(assignment_lines))
            
            self.play(FadeOut(centroid_dots), FadeOut(method_text))
        
        self.play(FadeOut(axes), FadeOut(x_label), FadeOut(y_label), 
                 FadeOut(points), FadeOut(init_title))
    
    def show_clustering_iterations(self):
        # Show the main clustering loop
        iteration_title = Text("Clustering Iterations", font_size=40, color=WHITE)
        iteration_title.to_edge(UP)
        self.play(Write(iteration_title))
        
        # Create coordinate system
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=8,
            y_length=8,
            axis_config={"color": GRAY}
        )
        axes.move_to(ORIGIN)
        
        # Generate data with clear clusters
        np.random.seed(42)
        cluster1 = np.random.multivariate_normal([-2, -2], [[0.5, 0.2], [0.2, 0.5]], 30)
        cluster2 = np.random.multivariate_normal([2, 2], [[0.5, 0.2], [0.2, 0.5]], 30)
        cluster3 = np.random.multivariate_normal([0, 0], [[0.5, 0.2], [0.2, 0.5]], 40)
        data = np.vstack([cluster1, cluster2, cluster3])
        
        # Create data points
        points = VGroup()
        for point in data:
            dot = Dot(axes.coords_to_point(point[0], point[1]), color=BLUE, radius=0.05)
            points.add(dot)
        
        self.play(Create(axes), Create(points))
        
        # Initialize centroids
        initial_centroids = np.array([[-3, -3], [3, 3], [0, 0]])
        centroid_colors = [RED, GREEN, YELLOW]
        
        # Show iterations
        max_iterations = 5
        current_centroids = initial_centroids.copy()
        
        for iteration in range(max_iterations):
            # Show iteration number
            iter_text = Text(f"Iteration {iteration + 1}", font_size=32, color=ORANGE)
            iter_text.to_edge(DOWN)
            self.play(Write(iter_text))
            
            # Create centroid dots
            centroid_dots = VGroup()
            for j, (pos, color) in enumerate(zip(current_centroids, centroid_colors)):
                centroid_dot = Dot(
                    axes.coords_to_point(pos[0], pos[1]), 
                    color=color, 
                    radius=0.15
                )
                centroid_dots.add(centroid_dot)
                
                label = Text(f"C{j+1}", font_size=20, color=color)
                label.next_to(centroid_dot, UP, buff=0.1)
                centroid_dots.add(label)
            
            self.play(Create(centroid_dots))
            
            # Assignment step
            assignment_text = Text("Step 1: Assign points to nearest centroid", font_size=24, color=WHITE)
            assignment_text.next_to(iter_text, UP, buff=0.3)
            self.play(Write(assignment_text))
            
            # Calculate assignments
            assignments = []
            assignment_lines = VGroup()
            
            for i, point in enumerate(data):
                distances = [np.linalg.norm(point - centroid) for centroid in current_centroids]
                closest_centroid = np.argmin(distances)
                assignments.append(closest_centroid)
                
                # Create assignment line
                line = Line(
                    axes.coords_to_point(point[0], point[1]),
                    axes.coords_to_point(current_centroids[closest_centroid][0], 
                                       current_centroids[closest_centroid][1]),
                    color=centroid_colors[closest_centroid],
                    stroke_width=1,
                    stroke_opacity=0.5
                )
                assignment_lines.add(line)
                
                # Change point color
                points[i].set_color(centroid_colors[closest_centroid])
            
            self.play(Create(assignment_lines))
            self.wait(1)
            
            # Update step
            update_text = Text("Step 2: Update centroids to cluster means", font_size=24, color=WHITE)
            self.play(ReplacementTransform(assignment_text, update_text))
            
            # Calculate new centroids
            new_centroids = []
            for j in range(len(current_centroids)):
                cluster_points = data[np.array(assignments) == j]
                if len(cluster_points) > 0:
                    new_centroid = np.mean(cluster_points, axis=0)
                else:
                    new_centroid = current_centroids[j]
                new_centroids.append(new_centroid)
            
            new_centroids = np.array(new_centroids)
            
            # Animate centroid movement
            centroid_animations = []
            for j, (old_pos, new_pos, color) in enumerate(zip(current_centroids, new_centroids, centroid_colors)):
                old_point = axes.coords_to_point(old_pos[0], old_pos[1])
                new_point = axes.coords_to_point(new_pos[0], new_pos[1])
                
                # Create movement trail
                trail = Line(old_point, new_point, color=color, stroke_width=3, stroke_opacity=0.7)
                self.play(Create(trail))
                
                # Move centroid
                centroid_animations.append(
                    centroid_dots[2*j].animate.move_to(new_point)
                )
                centroid_animations.append(
                    centroid_dots[2*j+1].animate.next_to(new_point, UP, buff=0.1)
                )
                
                self.play(FadeOut(trail))
            
            self.play(*centroid_animations)
            
            # Check convergence
            if np.allclose(current_centroids, new_centroids, atol=0.1):
                convergence_text = Text("✓ Algorithm Converged!", font_size=28, color=GREEN)
                convergence_text.next_to(update_text, UP, buff=0.3)
                self.play(Write(convergence_text))
                self.wait(2)
                self.play(FadeOut(convergence_text))
                break
            
            current_centroids = new_centroids.copy()
            
            # Clean up for next iteration
            self.play(FadeOut(assignment_lines), FadeOut(centroid_dots), 
                     FadeOut(update_text), FadeOut(iter_text))
            
            # Reset point colors
            for point in points:
                point.set_color(BLUE)
        
        self.play(FadeOut(axes), FadeOut(points), FadeOut(iteration_title))
    
    def show_final_results(self):
        # Show final clustering results
        results_title = Text("Final Clustering Results", font_size=40, color=WHITE)
        results_title.to_edge(UP)
        self.play(Write(results_title))
        
        # Create final visualization
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=8,
            y_length=8,
            axis_config={"color": GRAY}
        )
        axes.move_to(ORIGIN)
        
        # Generate final clustered data
        np.random.seed(42)
        cluster1 = np.random.multivariate_normal([-2, -2], [[0.5, 0.2], [0.2, 0.5]], 30)
        cluster2 = np.random.multivariate_normal([2, 2], [[0.5, 0.2], [0.2, 0.5]], 30)
        cluster3 = np.random.multivariate_normal([0, 0], [[0.5, 0.2], [0.2, 0.5]], 40)
        data = np.vstack([cluster1, cluster2, cluster3])
        
        # Final centroids
        final_centroids = np.array([[-2, -2], [2, 2], [0, 0]])
        centroid_colors = [RED, GREEN, YELLOW]
        
        # Create final clusters
        final_clusters = VGroup()
        for j, (centroid, color) in enumerate(zip(final_centroids, centroid_colors)):
            # Create cluster boundary (simplified as circle)
            cluster_boundary = Circle(
                radius=1.5,
                color=color,
                stroke_width=2,
                stroke_opacity=0.3,
                fill_opacity=0.1
            )
            cluster_boundary.move_to(axes.coords_to_point(centroid[0], centroid[1]))
            final_clusters.add(cluster_boundary)
            
            # Create centroid
            centroid_dot = Dot(
                axes.coords_to_point(centroid[0], centroid[1]),
                color=color,
                radius=0.2
            )
            final_clusters.add(centroid_dot)
            
            # Add cluster label
            label = Text(f"Cluster {j+1}", font_size=24, color=color)
            label.next_to(centroid_dot, UP, buff=0.3)
            final_clusters.add(label)
        
        # Create data points with final colors
        points = VGroup()
        for i, point in enumerate(data):
            # Determine cluster assignment
            distances = [np.linalg.norm(point - centroid) for centroid in final_centroids]
            closest_centroid = np.argmin(distances)
            
            dot = Dot(
                axes.coords_to_point(point[0], point[1]),
                color=centroid_colors[closest_centroid],
                radius=0.06
            )
            points.add(dot)
        
        self.play(Create(axes), Create(points), Create(final_clusters))
        
        # Show statistics
        stats = VGroup(
            Text("📊 Clustering Statistics:", font_size=32, color=WHITE),
            Text(f"• 3 clusters identified", font_size=24, color=GRAY),
            Text(f"• 100 data points clustered", font_size=24, color=GRAY),
            Text(f"• Within-cluster variance minimized", font_size=24, color=GRAY),
            Text(f"• Between-cluster separation maximized", font_size=24, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        stats.to_edge(RIGHT)
        
        self.play(Write(stats))
        self.wait(3)
        
        # Show applications
        applications = VGroup(
            Text("🎯 Applications:", font_size=32, color=WHITE),
            Text("• User behavior segmentation", font_size=24, color=GRAY),
            Text("• Meditation pattern analysis", font_size=24, color=GRAY),
            Text("• Stone type prediction", font_size=24, color=GRAY),
            Text("• Personalized recommendations", font_size=24, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        applications.to_edge(LEFT)
        
        self.play(Write(applications))
        self.wait(3)
        
        # Final message
        final_message = Text("K-Means clustering complete!", font_size=36, color=GREEN)
        final_message.to_edge(DOWN)
        self.play(Write(final_message))
        self.wait(2)
        
        self.play(FadeOut(axes), FadeOut(points), FadeOut(final_clusters),
                 FadeOut(stats), FadeOut(applications), FadeOut(final_message),
                 FadeOut(results_title))
