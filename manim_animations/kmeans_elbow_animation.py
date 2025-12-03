#!/usr/bin/env python3
"""
K-means Clustering and Elbow Method Animation
Shows clustering process and how to choose optimal k using elbow plot
"""

from manim import *
import numpy as np

class KMeansElbowAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Show title card
        self.show_title()
        
        # Show basic concept
        self.show_basic_concept()
        
        # Show clustering process
        self.show_clustering_process()
        
        # Show elbow method
        self.show_elbow_method()
        
        # Show optimal k selection
        self.show_optimal_selection()
        
        # Show summary
        self.show_summary()
    
    def show_title(self):
        """Title card"""
        title = Text("K-means Clustering", font_size=36, color=YELLOW, weight=BOLD)
        subtitle = Text("Identify Natural Groupings in Numeric Data", font_size=24, color=WHITE)
        concept = Text("Minimize within-cluster sum of squares • Use elbow plot for choosing k", 
                      font_size=18, color=LIGHT_GRAY, slant=ITALIC)
        
        title_group = VGroup(title, subtitle, concept).arrange(DOWN, buff=0.4)
        
        self.play(Write(title))
        self.play(Write(subtitle))
        self.play(Write(concept))
        self.wait(2)
        self.play(FadeOut(title_group))
    
    def show_basic_concept(self):
        """Show what K-means does"""
        title = Text("What is K-means Clustering?", font_size=32, color=BLUE, weight=BOLD).to_edge(UP)
        self.play(Write(title))
        
        # Key concepts
        concepts = VGroup(
            Text("🎯 Goal: Group similar data points into k clusters", font_size=24, color=WHITE),
            Text("📊 Method: Minimize Within-Cluster Sum of Squares (WCSS)", font_size=24, color=WHITE),
            Text("🔄 Process: Iteratively assign points and update cluster centers", font_size=24, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to(ORIGIN)
        
        for concept in concepts:
            self.play(FadeIn(concept, shift=UP))
            self.wait(1)
        
        # Show WCSS formula (simplified)
        formula_box = RoundedRectangle(
            width=10, height=1.5,
            stroke_color=YELLOW, stroke_width=2,
            fill_color=YELLOW, fill_opacity=0.1
        )
        
        formula_text = VGroup(
            Text("WCSS Formula:", font_size=20, color=YELLOW, weight=BOLD),
            Text("Sum of squared distances from points to their cluster centers", font_size=16, color=WHITE, slant=ITALIC)
        ).arrange(DOWN, buff=0.3).move_to(formula_box.get_center())
        
        formula_group = VGroup(formula_box, formula_text).next_to(concepts, DOWN, buff=1)
        
        self.play(FadeIn(formula_group))
        self.wait(2)
        
        self.play(FadeOut(concepts, formula_group))
        self.title = title

    def show_clustering_process(self):
        """Show the K-means clustering process"""
        process_title = Text("K-means Clustering Process", font_size=28, color=GREEN, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.title, process_title))
        
        # Create 2D data plot
        axes = Axes(
            x_range=[-4, 8, 2],
            y_range=[-3, 7, 2],
            x_length=7,
            y_length=6,
            axis_config={"stroke_color": WHITE, "stroke_width": 2}
        ).move_to(LEFT*2)
        
        x_label = Text("x₁", font_size=18, color=WHITE).next_to(axes, DOWN)
        y_label = Text("x₂", font_size=18, color=WHITE).next_to(axes, LEFT).rotate(PI/2)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Generate synthetic data (3 natural clusters)
        np.random.seed(42)
        
        # Create three distinct blobs
        cluster1 = np.random.normal([0, 1], 0.8, (20, 2))
        cluster2 = np.random.normal([4, 5], 0.8, (20, 2))
        cluster3 = np.random.normal([6, 1], 0.8, (20, 2))
        
        data_points = np.vstack([cluster1, cluster2, cluster3])
        
        # Create dots for data points
        data_dots = VGroup()
        for point in data_points:
            dot = Dot(axes.coords_to_point(point[0], point[1]), color=WHITE, radius=0.05)
            data_dots.add(dot)
        
        self.play(*[FadeIn(dot, scale=0.5) for dot in data_dots])
        
        # Initialize 3 random cluster centers
        k = 3
        center_colors = [RED, BLUE, GREEN]
        
        # Initial centers (somewhat random but not too bad)
        initial_centers = np.array([[1, 2], [3, 4], [5, 2]])
        
        center_markers = VGroup()
        for i, center in enumerate(initial_centers):
            marker = RegularPolygon(n=4, color=center_colors[i], fill_opacity=1, stroke_width=3)
            marker.scale(0.2).move_to(axes.coords_to_point(center[0], center[1]))
            center_markers.add(marker)
        
        self.play(*[FadeIn(marker, scale=1.5) for marker in center_markers])
        
        # Show step-by-step process
        process_steps = VGroup(
            Text("Step 1: Initialize cluster centers", font_size=18, color=WHITE),
            Text("Step 2: Assign points to nearest center", font_size=18, color=WHITE),
            Text("Step 3: Update centers to cluster means", font_size=18, color=WHITE),
            Text("Step 4: Repeat until convergence", font_size=18, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=1)
        
        self.play(Write(process_steps[0]))
        self.wait(1)
        
        # Show WCSS tracker
        wcss_text = Text("WCSS: calculating...", font_size=16, color=YELLOW)
        wcss_text.next_to(axes, UP, buff=0.3)
        self.play(Write(wcss_text))
        
        # Simulate a few iterations
        current_centers = initial_centers.copy()
        
        for iteration in range(3):
            self.play(Write(process_steps[1]))
            
            # Assign points to clusters (color them)
            assignments = []
            wcss_value = 0
            
            for i, dot in enumerate(data_dots):
                point = data_points[i]
                # Calculate distances to each center
                distances = [np.linalg.norm(point - center) for center in current_centers]
                closest_cluster = np.argmin(distances)
                assignments.append(closest_cluster)
                
                # Color the point
                dot.set_color(center_colors[closest_cluster])
                wcss_value += min(distances) ** 2
            
            self.play(*[Indicate(dot, color=dot.color) for dot in data_dots], run_time=1.5)
            
            # Update WCSS display
            wcss_display = Text(f"WCSS: {wcss_value:.1f}", font_size=16, color=YELLOW)
            wcss_display.move_to(wcss_text.get_center())
            self.play(Transform(wcss_text, wcss_display))
            
            self.play(Write(process_steps[2]))
            
            # Update cluster centers
            new_centers = []
            for cluster_id in range(k):
                cluster_points = data_points[np.array(assignments) == cluster_id]
                if len(cluster_points) > 0:
                    new_center = np.mean(cluster_points, axis=0)
                    new_centers.append(new_center)
                    
                    # Animate center movement
                    new_pos = axes.coords_to_point(new_center[0], new_center[1])
                    self.play(center_markers[cluster_id].animate.move_to(new_pos))
                else:
                    new_centers.append(current_centers[cluster_id])
            
            current_centers = np.array(new_centers)
            self.wait(1)
        
        self.play(Write(process_steps[3]))
        
        # Final assignment and WCSS
        final_wcss = 0
        for i, dot in enumerate(data_dots):
            point = data_points[i]
            distances = [np.linalg.norm(point - center) for center in current_centers]
            final_wcss += min(distances) ** 2
        
        final_wcss_display = Text(f"Final WCSS: {final_wcss:.1f}", font_size=16, color=GREEN, weight=BOLD)
        final_wcss_display.move_to(wcss_text.get_center())
        self.play(Transform(wcss_text, final_wcss_display))
        
        self.wait(2)
        
        # Store elements for cleanup
        self.clustering_elements = VGroup(
            axes, x_label, y_label, data_dots, center_markers, 
            process_steps, wcss_text
        )
        self.final_wcss = final_wcss
        self.process_title = process_title

    def show_elbow_method(self):
        """Show the elbow method for choosing k"""
        elbow_title = Text("Elbow Method: Choosing Optimal k", font_size=28, color=PURPLE, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.process_title, elbow_title))
        
        # Fade clustering visualization
        self.play(self.clustering_elements.animate.set_opacity(0.3))
        
        # Create elbow plot
        elbow_axes = Axes(
            x_range=[1, 8, 1],
            y_range=[0, 100, 20],
            x_length=8,
            y_length=5,
            axis_config={"stroke_color": WHITE, "stroke_width": 2}
        ).move_to(ORIGIN)
        
        elbow_x_label = Text("Number of Clusters (k)", font_size=16, color=WHITE).next_to(elbow_axes, DOWN)
        elbow_y_label = Text("WCSS", font_size=16, color=WHITE).next_to(elbow_axes, LEFT).rotate(PI/2)
        
        self.play(Create(elbow_axes), Write(elbow_x_label), Write(elbow_y_label))
        
        # Generate WCSS values for different k (synthetic but realistic)
        k_values = np.arange(1, 8)
        wcss_values = np.array([95, 45, 25, 20, 18, 17, 16.5])  # Typical elbow pattern
        
        # Plot points and curve
        elbow_points = VGroup()
        plot_coords = []
        
        for i, (k, wcss) in enumerate(zip(k_values, wcss_values)):
            coord = elbow_axes.coords_to_point(k, wcss)
            plot_coords.append(coord)
            point = Dot(coord, color=YELLOW, radius=0.08)
            elbow_points.add(point)
        
        # Create smooth curve
        elbow_curve = VMobject(color=BLUE, stroke_width=4)
        elbow_curve.set_points_smoothly(plot_coords)
        
        self.play(Create(elbow_curve))
        self.play(*[FadeIn(point, scale=1.2) for point in elbow_points])
        
        # Highlight the elbow point (k=3)
        elbow_point = elbow_points[2]  # k=3
        elbow_highlight = Circle(radius=0.2, color=RED, stroke_width=4)
        elbow_highlight.move_to(elbow_point.get_center())
        
        self.play(Create(elbow_highlight))
        
        # Add explanation
        elbow_explanation = VGroup(
            Text("The 'Elbow':", font_size=20, color=RED, weight=BOLD),
            Text("Point where WCSS reduction", font_size=16, color=WHITE),
            Text("starts to level off", font_size=16, color=WHITE),
            Text("k = 3 is optimal here", font_size=16, color=GREEN, weight=BOLD)
        ).arrange(DOWN, buff=0.2).next_to(elbow_highlight, UP+RIGHT, buff=0.5)
        
        # Draw arrow pointing to elbow
        elbow_arrow = Arrow(
            elbow_explanation.get_bottom(),
            elbow_highlight.get_top(),
            stroke_width=3,
            color=RED,
            max_tip_length_to_length_ratio=0.1
        )
        
        self.play(
            Write(elbow_explanation),
            Create(elbow_arrow)
        )
        
        # Show diminishing returns concept
        diminishing_text = VGroup(
            Text("Diminishing Returns:", font_size=18, color=ORANGE, weight=BOLD),
            Text("• k=1→2: Large WCSS reduction", font_size=14, color=WHITE),
            Text("• k=2→3: Moderate reduction", font_size=14, color=WHITE),
            Text("• k=3→4: Small reduction", font_size=14, color=GREEN),
            Text("• k>4: Minimal improvement", font_size=14, color=LIGHT_GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=1)
        
        for line in diminishing_text:
            self.play(Write(line))
            self.wait(0.5)
        
        self.wait(2)
        
        # Store elbow elements
        self.elbow_elements = VGroup(
            elbow_axes, elbow_x_label, elbow_y_label, elbow_curve, 
            elbow_points, elbow_highlight, elbow_explanation, 
            elbow_arrow, diminishing_text
        )
        self.elbow_title = elbow_title

    def show_optimal_selection(self):
        """Show how to select optimal k"""
        optimal_title = Text("Selecting Optimal k", font_size=28, color=ORANGE, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.elbow_title, optimal_title))
        
        # Clear previous elements
        self.play(FadeOut(self.clustering_elements, self.elbow_elements))
        
        # Show different methods for choosing k
        methods = VGroup(
            Text("Methods for Choosing k:", font_size=24, color=YELLOW, weight=BOLD),
            
            VGroup(
                Text("1. Elbow Method", font_size=20, color=BLUE, weight=BOLD),
                Text("• Find the 'elbow' in WCSS vs k plot", font_size=16, color=WHITE),
                Text("• Point of diminishing returns", font_size=16, color=WHITE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2),
            
            VGroup(
                Text("2. Silhouette Analysis", font_size=20, color=GREEN, weight=BOLD),
                Text("• Measure how well points fit their clusters", font_size=16, color=WHITE),
                Text("• Higher silhouette score = better clustering", font_size=16, color=WHITE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2),
            
            VGroup(
                Text("3. Domain Knowledge", font_size=20, color=PURPLE, weight=BOLD),
                Text("• Use business/scientific understanding", font_size=16, color=WHITE),
                Text("• Consider interpretability needs", font_size=16, color=WHITE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2),
            
            VGroup(
                Text("4. Gap Statistic", font_size=20, color=ORANGE, weight=BOLD),
                Text("• Compare clustering to random data", font_size=16, color=WHITE),
                Text("• More rigorous statistical approach", font_size=16, color=WHITE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        ).arrange(DOWN, buff=0.6).move_to(ORIGIN)
        
        # Show methods progressively
        for method in methods:
            if isinstance(method, VGroup) and len(method) > 1:
                self.play(Write(method[0]))
                for sub_item in method[1:]:
                    self.play(Write(sub_item))
                    self.wait(0.5)
            else:
                self.play(Write(method))
            self.wait(0.8)
        
        # Highlight elbow method as most common
        elbow_highlight_box = SurroundingRectangle(
            methods[1], 
            color=YELLOW, 
            stroke_width=3,
            buff=0.2
        )
        
        most_common_text = Text("Most commonly used!", font_size=16, color=YELLOW, weight=BOLD)
        most_common_text.next_to(elbow_highlight_box, RIGHT, buff=0.3)
        
        self.play(Create(elbow_highlight_box), Write(most_common_text))
        
        self.wait(2)
        self.play(FadeOut(methods, elbow_highlight_box, most_common_text))
        self.optimal_title = optimal_title

    def show_summary(self):
        """Show final summary"""
        summary_title = Text("K-means Clustering Summary", font_size=32, color=YELLOW, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.optimal_title, summary_title))
        
        # Create comprehensive summary
        summary_card = RoundedRectangle(
            corner_radius=0.2, width=12, height=5,
            stroke_color=WHITE, stroke_width=2,
            fill_color=BLACK, fill_opacity=0.95
        ).move_to(ORIGIN)
        
        summary_content = VGroup(
            VGroup(
                Text("🔄 Algorithm:", font_size=20, color=BLUE, weight=BOLD),
                Text("1. Initialize k cluster centers randomly", font_size=16, color=WHITE),
                Text("2. Assign each point to nearest center", font_size=16, color=WHITE),
                Text("3. Update centers to cluster means", font_size=16, color=WHITE),
                Text("4. Repeat until convergence", font_size=16, color=WHITE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2),
            
            VGroup(
                Text("📊 Choosing k:", font_size=20, color=GREEN, weight=BOLD),
                Text("• Elbow method: find WCSS 'elbow'", font_size=16, color=WHITE),
                Text("• Look for diminishing returns", font_size=16, color=WHITE),
                Text("• Balance complexity vs performance", font_size=16, color=WHITE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2),
            
            VGroup(
                Text("⚡ Key Points:", font_size=20, color=ORANGE, weight=BOLD),
                Text("• Minimizes Within-Cluster Sum of Squares", font_size=16, color=WHITE),
                Text("• Works best with spherical clusters", font_size=16, color=WHITE),
                Text("• Sensitive to initialization and outliers", font_size=16, color=WHITE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        ).arrange(DOWN, buff=0.6).move_to(summary_card.get_center())
        
        self.play(FadeIn(summary_card))
        
        # Animate summary sections
        for section in summary_content:
            self.play(Write(section[0]))
            for item in section[1:]:
                self.play(Write(item))
                self.wait(0.4)
            self.wait(0.8)
        
        # Final message
        final_message = Text(
            "K-means: Simple, effective clustering when k is chosen wisely!",
            font_size=20,
            color=YELLOW,
            weight=BOLD
        ).next_to(summary_card, DOWN, buff=0.8)
        
        self.play(Write(final_message))
        self.wait(3)
        
        # Update todos
        self.mark_todos_complete()
    
    def mark_todos_complete(self):
        """Mark all todos as complete"""
        pass  # The TodoWrite calls would go here if needed