#!/usr/bin/env python3
"""
Single Linkage Distance Matrix Update Animation
Shows how to update distance matrix when merging clusters in hierarchical clustering
"""

from manim import *
import numpy as np

class SingleLinkageAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Show intro
        self.show_intro()
        
        # Show initial setup
        self.show_initial_setup()
        
        # Demonstrate distance matrix
        self.show_distance_matrix()
        
        # Show merging process
        self.show_merging_process()
        
        # Show matrix update
        self.show_matrix_update()
        
        # Show final result
        self.show_final_result()
    
    def show_intro(self):
        """Introduction to single linkage clustering"""
        title = Text("Single Linkage Clustering", font_size=48, color=YELLOW).to_edge(UP)
        subtitle = Text("Distance Matrix Updates", font_size=28, color=WHITE).next_to(title, DOWN)
        
        self.play(Write(title), Write(subtitle))
        self.wait(2)
        
        # Key question
        question = VGroup(
            Text("How do you update the distance matrix", font_size=24, color=LIGHT_GRAY),
            Text("when merging two clusters?", font_size=24, color=LIGHT_GRAY)
        ).arrange(DOWN).next_to(subtitle, DOWN, buff=1)
        
        self.play(FadeIn(question, shift=UP))
        self.wait(2)
        
        # Formula
        formula_text = Text("Formula:", font_size=24, color=YELLOW).next_to(question, DOWN, buff=1)
        formula = Text("d(A, {B, C}) = min(d(A, B), d(A, C))", font_size=28, color=GREEN).next_to(formula_text, DOWN, buff=0.5)
        
        self.play(Write(formula_text), Write(formula))
        self.wait(3)
        self.play(FadeOut(title, subtitle, question, formula_text, formula))
    
    def show_initial_setup(self):
        """Show initial clusters and setup"""
        title = Text("Initial Setup: 5 Clusters", font_size=36, color=YELLOW).to_edge(UP)
        self.play(Write(title))
        
        # Create 5 clusters as points
        cluster_positions = [
            [-3, 1.5, 0],    # A
            [-1, 2, 0],      # B  
            [1, 1, 0],       # C
            [2.5, -1, 0],    # D
            [-2, -1.5, 0]    # E
        ]
        
        cluster_colors = [RED, BLUE, GREEN, ORANGE, PURPLE]
        cluster_labels = ['A', 'B', 'C', 'D', 'E']
        
        self.clusters = {}
        self.cluster_dots = {}
        
        for i, (pos, color, label) in enumerate(zip(cluster_positions, cluster_colors, cluster_labels)):
            # Create cluster dot
            dot = Dot(pos, color=color, radius=0.15)
            label_text = Text(label, font_size=20, color=WHITE).next_to(dot, UP, buff=0.1)
            
            cluster_group = VGroup(dot, label_text)
            self.clusters[label] = cluster_group
            self.cluster_dots[label] = dot
            
            self.play(FadeIn(cluster_group), run_time=0.5)
        
        self.wait(1)
        
        # Show that these are the closest clusters
        explanation = Text("Let's say clusters B and C are the closest", font_size=20, color=LIGHT_GRAY).next_to(title, DOWN, buff=0.5)
        self.play(Write(explanation))
        
        # Highlight B and C
        b_highlight = Circle(radius=0.3, color=YELLOW, stroke_width=4).move_to(self.cluster_dots['B'].get_center())
        c_highlight = Circle(radius=0.3, color=YELLOW, stroke_width=4).move_to(self.cluster_dots['C'].get_center())
        
        self.play(Create(b_highlight), Create(c_highlight))
        self.wait(2)
        
        self.play(FadeOut(explanation, b_highlight, c_highlight))
        self.explanation = explanation  # Store for cleanup
        
        self.title = title
    
    def show_distance_matrix(self):
        """Show the initial distance matrix"""
        matrix_title = Text("Distance Matrix", font_size=24, color=YELLOW).next_to(self.title, DOWN, buff=0.5)
        self.play(Write(matrix_title))
        
        # Create distance matrix (symmetric)
        distances = {
            ('A', 'A'): 0,   ('A', 'B'): 2.2, ('A', 'C'): 4.1, ('A', 'D'): 6.4, ('A', 'E'): 3.2,
            ('B', 'A'): 2.2, ('B', 'B'): 0,   ('B', 'C'): 2.0, ('B', 'D'): 4.6, ('B', 'E'): 3.9,
            ('C', 'A'): 4.1, ('C', 'B'): 2.0, ('C', 'C'): 0,   ('C', 'D'): 2.1, ('C', 'E'): 4.2,
            ('D', 'A'): 6.4, ('D', 'B'): 4.6, ('D', 'C'): 2.1, ('D', 'D'): 0,   ('D', 'E'): 5.1,
            ('E', 'A'): 3.2, ('E', 'B'): 3.9, ('E', 'C'): 4.2, ('E', 'D'): 5.1, ('E', 'E'): 0
        }
        
        # Create matrix table
        matrix_size = 0.6
        matrix_group = VGroup()
        
        labels = ['A', 'B', 'C', 'D', 'E']
        
        # Add row and column headers
        for i, label in enumerate(labels):
            # Row header
            row_header = Text(label, font_size=16, color=WHITE).move_to([-3.5, 1 - i * matrix_size, 0])
            matrix_group.add(row_header)
            
            # Column header  
            col_header = Text(label, font_size=16, color=WHITE).move_to([-3 + i * matrix_size, 1.3, 0])
            matrix_group.add(col_header)
        
        # Add matrix cells
        self.matrix_cells = {}
        for i, row_label in enumerate(labels):
            for j, col_label in enumerate(labels):
                value = distances[(row_label, col_label)]
                if row_label == col_label:
                    cell_text = Text("-", font_size=14, color=GRAY)
                else:
                    cell_text = Text(f"{value:.1f}", font_size=14, color=WHITE)
                
                cell_pos = [-3 + j * matrix_size, 1 - i * matrix_size, 0]
                cell_text.move_to(cell_pos)
                
                # Highlight B-C distance (smallest)
                if (row_label == 'B' and col_label == 'C') or (row_label == 'C' and col_label == 'B'):
                    cell_text.set_color(YELLOW)
                    highlight_box = Rectangle(width=matrix_size-0.1, height=matrix_size-0.1, 
                                            color=YELLOW, stroke_width=2, fill_opacity=0.2).move_to(cell_pos)
                    matrix_group.add(highlight_box)
                
                matrix_group.add(cell_text)
                self.matrix_cells[(row_label, col_label)] = cell_text
        
        matrix_group.move_to(RIGHT * 2 + DOWN * 0.5)
        self.play(FadeIn(matrix_group, lag_ratio=0.1))
        self.matrix_group = matrix_group
        self.matrix_title = matrix_title
        self.distances = distances
        
        self.wait(2)
    
    def show_merging_process(self):
        """Show the process of merging B and C"""
        merge_title = Text("Step 1: Merge Clusters B and C", font_size=24, color=GREEN).next_to(self.matrix_title, DOWN, buff=0.8)
        self.play(Write(merge_title))
        
        # Animate merging B and C
        b_pos = self.cluster_dots['B'].get_center()
        c_pos = self.cluster_dots['C'].get_center()
        midpoint = (b_pos + c_pos) / 2
        
        # Create new merged cluster
        new_cluster_dot = Dot(midpoint, color=TEAL, radius=0.2)
        new_cluster_label = Text("{B,C}", font_size=18, color=WHITE).next_to(new_cluster_dot, UP, buff=0.1)
        merged_cluster = VGroup(new_cluster_dot, new_cluster_label)
        
        # Draw connection between B and C
        connection = Line(b_pos, c_pos, color=YELLOW, stroke_width=3)
        self.play(Create(connection))
        
        # Move B and C to merge point
        self.play(
            self.clusters['B'].animate.move_to(midpoint + LEFT * 0.3),
            self.clusters['C'].animate.move_to(midpoint + RIGHT * 0.3),
            run_time=2
        )
        
        # Replace with new merged cluster
        self.play(
            FadeOut(self.clusters['B'], self.clusters['C'], connection),
            FadeIn(merged_cluster)
        )
        
        self.merged_cluster = merged_cluster
        self.merge_title = merge_title
        self.wait(2)
    
    def show_matrix_update(self):
        """Show how to update the distance matrix"""
        update_title = Text("Step 2: Update Distance Matrix", font_size=24, color=ORANGE).next_to(self.merge_title, DOWN, buff=0.5)
        self.play(Write(update_title))
        
        # Show the formula again
        formula_reminder = Text("d(A, {B,C}) = min(d(A,B), d(A,C))", font_size=18, color=GREEN).next_to(update_title, DOWN, buff=0.3)
        self.play(Write(formula_reminder))
        
        # Calculate and show updates for each cluster
        updates = [
            ('A', 'B', 'C', 2.2, 4.1, 2.2),  # min(2.2, 4.1) = 2.2
            ('D', 'B', 'C', 4.6, 2.1, 2.1),  # min(4.6, 2.1) = 2.1  
            ('E', 'B', 'C', 3.9, 4.2, 3.9),  # min(3.9, 4.2) = 3.9
        ]
        
        calculation_group = VGroup()
        y_offset = 0
        
        for cluster, b_dist, c_dist, old_b, old_c, result in updates:
            calc_text = Text(f"d({cluster}, {{B,C}}) = min({old_b:.1f}, {old_c:.1f}) = {result:.1f}", 
                           font_size=16, color=WHITE)
            calc_text.next_to(formula_reminder, DOWN, buff=0.5 + y_offset)
            calculation_group.add(calc_text)
            y_offset += 0.4
            
            self.play(Write(calc_text))
            self.wait(1)
        
        self.wait(2)
        
        # Create new matrix
        self.show_updated_matrix()
        
        self.update_title = update_title
        self.formula_reminder = formula_reminder
        self.calculation_group = calculation_group
    
    def show_updated_matrix(self):
        """Show the updated distance matrix"""
        new_matrix_title = Text("Updated Distance Matrix", font_size=20, color=GREEN).move_to(self.matrix_title.get_center())
        
        # New distances after merging
        new_distances = {
            ('A', 'A'): 0,     ('A', '{B,C}'): 2.2, ('A', 'D'): 6.4, ('A', 'E'): 3.2,
            ('{B,C}', 'A'): 2.2, ('{B,C}', '{B,C}'): 0, ('{B,C}', 'D'): 2.1, ('{B,C}', 'E'): 3.9,
            ('D', 'A'): 6.4,   ('D', '{B,C}'): 2.1, ('D', 'D'): 0,   ('D', 'E'): 5.1,
            ('E', 'A'): 3.2,   ('E', '{B,C}'): 3.9, ('E', 'D'): 5.1, ('E', 'E'): 0
        }
        
        # Create new matrix
        new_matrix_group = VGroup()
        labels = ['A', '{B,C}', 'D', 'E']
        matrix_size = 0.7
        
        # Add headers
        for i, label in enumerate(labels):
            row_header = Text(label, font_size=14, color=WHITE).move_to([-3.8, 1 - i * matrix_size, 0])
            new_matrix_group.add(row_header)
            
            col_header = Text(label, font_size=14, color=WHITE).move_to([-3 + i * matrix_size, 1.4, 0])
            new_matrix_group.add(col_header)
        
        # Add matrix cells
        for i, row_label in enumerate(labels):
            for j, col_label in enumerate(labels):
                if (row_label, col_label) in new_distances:
                    value = new_distances[(row_label, col_label)]
                    if row_label == col_label:
                        cell_text = Text("-", font_size=12, color=GRAY)
                    else:
                        cell_text = Text(f"{value:.1f}", font_size=12, color=WHITE)
                        
                        # Highlight updated values
                        if '{B,C}' in row_label or '{B,C}' in col_label:
                            cell_text.set_color(GREEN)
                else:
                    cell_text = Text("-", font_size=12, color=GRAY)
                
                cell_pos = [-3 + j * matrix_size, 1 - i * matrix_size, 0]
                cell_text.move_to(cell_pos)
                new_matrix_group.add(cell_text)
        
        new_matrix_group.move_to(RIGHT * 2.5 + DOWN * 0.5)
        
        # Transform old matrix to new matrix
        self.play(
            ReplacementTransform(self.matrix_group, new_matrix_group),
            ReplacementTransform(self.matrix_title, new_matrix_title)
        )
        
        self.new_matrix_group = new_matrix_group
        self.new_matrix_title = new_matrix_title
        self.wait(2)
    
    def show_final_result(self):
        """Show the final result and key insights"""
        final_title = Text("Key Insights", font_size=36, color=YELLOW).to_edge(UP)
        
        self.play(
            ReplacementTransform(self.title, final_title),
            FadeOut(self.update_title, self.formula_reminder, self.calculation_group)
        )
        
        insights = VGroup(
            VGroup(
                Text("🔗", font_size=32),
                Text("Single Linkage:", font_size=24, color=WHITE),
                Text("Uses minimum distance", font_size=20, color=LIGHT_GRAY)
            ).arrange(RIGHT, buff=0.3),
            
            VGroup(
                Text("📊", font_size=32),
                Text("Matrix Update:", font_size=24, color=WHITE),
                Text("d(A, {B,C}) = min(d(A,B), d(A,C))", font_size=20, color=GREEN)
            ).arrange(RIGHT, buff=0.3),
            
            VGroup(
                Text("🔄", font_size=32),
                Text("Process:", font_size=24, color=WHITE),
                Text("1. Find closest clusters 2. Merge 3. Update matrix", font_size=18, color=LIGHT_GRAY)
            ).arrange(RIGHT, buff=0.3),
            
            VGroup(
                Text("⚡", font_size=32),
                Text("Efficiency:", font_size=24, color=WHITE),
                Text("Matrix size reduces from n×n to (n-1)×(n-1)", font_size=18, color=LIGHT_GRAY)
            ).arrange(RIGHT, buff=0.3)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).shift(LEFT * 2 + DOWN * 0.5)
        
        for insight in insights:
            self.play(FadeIn(insight, shift=UP))
            self.wait(0.8)
        
        # Algorithm steps summary
        steps_title = Text("Algorithm Steps:", font_size=24, color=ORANGE).next_to(insights, DOWN, buff=0.8)
        steps = VGroup(
            Text("1. Start with distance matrix", font_size=18, color=WHITE),
            Text("2. Find minimum distance pair", font_size=18, color=WHITE),
            Text("3. Merge clusters using single linkage", font_size=18, color=WHITE),
            Text("4. Update matrix: min rule for all other clusters", font_size=18, color=WHITE),
            Text("5. Repeat until one cluster remains", font_size=18, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(steps_title, DOWN, buff=0.3)
        
        self.play(Write(steps_title))
        for step in steps:
            self.play(FadeIn(step))
            self.wait(0.5)
        
        # Final emphasis
        self.wait(2)
        final_message = Text(
            "Single Linkage: Always take the MINIMUM distance!",
            font_size=24,
            color=YELLOW
        ).next_to(steps, DOWN, buff=1)
        
        self.play(Write(final_message))
        self.wait(3)