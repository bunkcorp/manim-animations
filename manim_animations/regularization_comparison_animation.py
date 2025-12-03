#!/usr/bin/env python3
"""
Regularization Methods Comparison Animation
Visual comparison of Lasso, Ridge, and Elastic Net regularization
"""

from manim import *
import numpy as np

class RegularizationComparisonAnimation(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Show comparison table
        self.show_comparison_table()
        
        # Show 3D constraint visualization
        self.show_3d_constraints()
        
        # Demonstrate coefficient paths
        self.show_coefficient_paths()
        
        # Show feature selection comparison
        self.show_feature_selection()
        
        # Show final summary
        self.show_final_summary()
    
    def show_comparison_table(self):
        """Display comparison table with penalty formulas"""
        title = Text("Regularization Methods Comparison", 
                    font_size=32, color=YELLOW, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create table
        table_box = Rectangle(
            width=12, height=6,
            fill_color=BLACK, fill_opacity=0.9,
            stroke_color=WHITE, stroke_width=2
        ).move_to(DOWN*0.5)
        
        # Headers
        headers = VGroup(
            Text("Method", font_size=20, color=WHITE, weight=BOLD),
            Text("Penalty Term", font_size=20, color=WHITE, weight=BOLD),
            Text("Characteristic", font_size=20, color=WHITE, weight=BOLD)
        )
        
        # Position headers
        headers[0].move_to(table_box.get_left() + RIGHT*2 + UP*2.3)
        headers[1].move_to(table_box.get_center() + UP*2.3)
        headers[2].move_to(table_box.get_right() + LEFT*2 + UP*2.3)
        
        self.play(Create(table_box))
        self.play(*[Write(header) for header in headers])
        
        # Method names
        lasso_name = Text("Lasso (L1)", font_size=18, color=RED, weight=BOLD)
        ridge_name = Text("Ridge (L2)", font_size=18, color=BLUE, weight=BOLD)
        elastic_name = Text("Elastic Net", font_size=18, color=PURPLE, weight=BOLD)
        
        lasso_name.move_to(table_box.get_left() + RIGHT*2 + UP*1.2)
        ridge_name.move_to(table_box.get_left() + RIGHT*2)
        elastic_name.move_to(table_box.get_left() + RIGHT*2 + DOWN*1.2)
        
        # Penalty formulas
        lasso_penalty = Text("λ Σ|βⱼ|", font_size=16, color=WHITE)
        ridge_penalty = Text("λ Σβⱼ²", font_size=16, color=WHITE)
        elastic_penalty = Text("αL + (1-α)R", font_size=16, color=WHITE)
        
        lasso_penalty.move_to(table_box.get_center() + UP*1.2)
        ridge_penalty.move_to(table_box.get_center())
        elastic_penalty.move_to(table_box.get_center() + DOWN*1.2)
        
        # Characteristics
        lasso_char = Text("Zeros coefficients", font_size=16, color=WHITE)
        ridge_char = Text("Shrinks but doesn't zero", font_size=16, color=WHITE)
        elastic_char = Text("Best of both worlds", font_size=16, color=WHITE)
        
        lasso_char.move_to(table_box.get_right() + LEFT*2 + UP*1.2)
        ridge_char.move_to(table_box.get_right() + LEFT*2)
        elastic_char.move_to(table_box.get_right() + LEFT*2 + DOWN*1.2)
        
        # Animate table content
        self.play(Write(lasso_name), Write(lasso_penalty), Write(lasso_char))
        self.play(Write(ridge_name), Write(ridge_penalty), Write(ridge_char))
        self.play(Write(elastic_name), Write(elastic_penalty), Write(elastic_char))
        
        # Add dividing lines
        h_line1 = Line(
            table_box.get_left() + UP*0.6, table_box.get_right() + UP*0.6,
            stroke_color=WHITE, stroke_width=1
        )
        h_line2 = Line(
            table_box.get_left() + DOWN*0.6, table_box.get_right() + DOWN*0.6,
            stroke_color=WHITE, stroke_width=1
        )
        v_line1 = Line(
            table_box.get_top() + LEFT*2, table_box.get_bottom() + LEFT*2,
            stroke_color=WHITE, stroke_width=1
        )
        v_line2 = Line(
            table_box.get_top() + RIGHT*2, table_box.get_bottom() + RIGHT*2,
            stroke_color=WHITE, stroke_width=1
        )
        
        self.play(Create(h_line1), Create(h_line2), Create(v_line1), Create(v_line2))
        
        self.wait(2)
        
        # Store table elements
        self.table_elements = VGroup(
            table_box, headers, lasso_name, ridge_name, elastic_name,
            lasso_penalty, ridge_penalty, elastic_penalty,
            lasso_char, ridge_char, elastic_char,
            h_line1, h_line2, v_line1, v_line2
        )
        self.title = title
    
    def show_3d_constraints(self):
        """Show 3D constraint visualization"""
        constraint_title = Text("3D Constraint Visualization", 
                               font_size=28, color=BLUE, weight=BOLD)
        constraint_title.to_edge(UP, buff=0.5)
        self.play(ReplacementTransform(self.title, constraint_title))
        
        # Clear table
        self.play(FadeOut(self.table_elements))
        
        # Set up 3D scene
        self.set_camera_orientation(phi=60 * DEGREES, theta=30 * DEGREES)
        
        # Create 3D axes
        axes_3d = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
            z_length=4,
            axis_config={"stroke_color": WHITE, "stroke_width": 2}
        )
        
        # Labels for axes
        x_label = Text("β₁", font_size=16, color=WHITE).move_to([2.5, 0, 0])
        y_label = Text("β₂", font_size=16, color=WHITE).move_to([0, 2.5, 0])
        
        self.play(Create(axes_3d))
        self.add_fixed_in_frame_mobjects(x_label, y_label)
        self.play(Write(x_label), Write(y_label))
        
        # Create constraint shapes
        # Lasso (L1) - Diamond/Rhombus
        lasso_constraint = self.create_lasso_constraint()
        lasso_constraint.set_fill(RED, opacity=0.3)
        lasso_constraint.set_stroke(RED, width=3)
        
        # Ridge (L2) - Circle
        ridge_constraint = Circle(radius=1.5, color=BLUE, fill_opacity=0.3, stroke_width=3)
        ridge_constraint.rotate(PI/2, axis=RIGHT)
        
        # Elastic Net - Rounded Diamond
        elastic_constraint = self.create_elastic_constraint()
        elastic_constraint.set_fill(PURPLE, opacity=0.3)
        elastic_constraint.set_stroke(PURPLE, width=3)
        
        # Show constraints one by one
        lasso_text = Text("Lasso (L1): Diamond Shape", font_size=16, color=RED, weight=BOLD)
        self.add_fixed_in_frame_mobjects(lasso_text)
        lasso_text.to_corner(UL, buff=1)
        
        self.play(Create(lasso_constraint), Write(lasso_text))
        self.wait(1)
        
        ridge_text = Text("Ridge (L2): Circle Shape", font_size=16, color=BLUE, weight=BOLD)
        self.add_fixed_in_frame_mobjects(ridge_text)
        ridge_text.next_to(lasso_text, DOWN, buff=0.3)
        
        self.play(FadeOut(lasso_constraint), Create(ridge_constraint), Write(ridge_text))
        self.wait(1)
        
        elastic_text = Text("Elastic Net: Rounded Diamond", font_size=16, color=PURPLE, weight=BOLD)
        self.add_fixed_in_frame_mobjects(elastic_text)
        elastic_text.next_to(ridge_text, DOWN, buff=0.3)
        
        self.play(FadeOut(ridge_constraint), Create(elastic_constraint), Write(elastic_text))
        self.wait(1)
        
        # Show all together
        comparison_text = Text("Shape Determines Sparsity!", font_size=18, color=YELLOW, weight=BOLD)
        self.add_fixed_in_frame_mobjects(comparison_text)
        comparison_text.next_to(elastic_text, DOWN, buff=0.5)
        
        self.play(
            Create(lasso_constraint), Create(ridge_constraint),
            Write(comparison_text)
        )
        
        # Add arrows pointing to corners
        corner_arrow = Arrow(
            start=[1.2, 1.2, 0], end=[1.5, 0, 0],
            color=YELLOW, stroke_width=4
        )
        corner_text = Text("Corners → Sparsity", font_size=14, color=YELLOW, weight=BOLD)
        self.add_fixed_in_frame_mobjects(corner_text)
        corner_text.move_to([2, 1, 0])
        
        self.play(GrowArrow(corner_arrow), Write(corner_text))
        self.wait(2)
        
        # Store 3D elements
        self.constraint_elements = VGroup(
            axes_3d, lasso_constraint, ridge_constraint, elastic_constraint, corner_arrow
        )
        self.constraint_title = constraint_title
    
    def create_lasso_constraint(self):
        """Create diamond shape for Lasso constraint"""
        diamond_points = [
            [1.5, 0, 0],    # right
            [0, 1.5, 0],    # top
            [-1.5, 0, 0],   # left
            [0, -1.5, 0],   # bottom
            [1.5, 0, 0]     # close path
        ]
        return Polygon(*diamond_points, color=RED)
    
    def create_elastic_constraint(self):
        """Create rounded diamond for Elastic Net"""
        # Approximate rounded diamond with more points
        angles = np.linspace(0, 2*PI, 12, endpoint=False)
        points = []
        for angle in angles:
            # Create rounded diamond by modifying radius based on angle
            base_radius = 1.3
            corner_factor = 0.8 + 0.4 * abs(np.cos(2 * angle))  # Rounded corners
            radius = base_radius * corner_factor
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            points.append([x, y, 0])
        points.append(points[0])  # Close the shape
        
        return Polygon(*points, color=PURPLE)
    
    def show_coefficient_paths(self):
        """Demonstrate coefficient regularization paths"""
        paths_title = Text("Coefficient Regularization Paths", 
                         font_size=28, color=GREEN, weight=BOLD)
        paths_title.to_edge(UP, buff=0.5)
        
        # Reset to 2D view
        self.move_camera(phi=0, theta=-PI/2)
        self.play(ReplacementTransform(self.constraint_title, paths_title))
        self.play(FadeOut(self.constraint_elements))
        
        # Create axes for coefficient paths
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[-2, 3, 1],
            x_length=8,
            y_length=6,
            axis_config={"stroke_color": WHITE, "stroke_width": 2}
        ).move_to(DOWN*0.5)
        
        x_label = Text("λ (Lambda)", font_size=16, color=WHITE)
        x_label.next_to(axes.x_axis, DOWN, buff=0.3)
        
        y_label = Text("Coefficient Value", font_size=16, color=WHITE)
        y_label.next_to(axes.y_axis, LEFT, buff=0.3)
        y_label.rotate(PI/2)
        
        self.add_fixed_in_frame_mobjects(axes, x_label, y_label)
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Generate coefficient paths for 5 features
        lambda_vals = np.linspace(0, 10, 50)
        
        # Lasso paths (some go to zero)
        lasso_paths = []
        lasso_colors = [RED, ORANGE, YELLOW, GREEN, PINK]
        
        for i in range(5):
            # Different coefficients zero out at different lambda values
            zero_lambda = 2 + i * 1.5
            path = []
            for lam in lambda_vals:
                if lam < zero_lambda:
                    coeff = (2.5 - i*0.5) * np.exp(-lam * 0.3)  # Exponential decay
                else:
                    coeff = 0  # Zero out
                path.append(axes.coords_to_point(lam, coeff))
            lasso_paths.append(path)
        
        # Show Lasso paths
        lasso_text = Text("Lasso: Coefficients Drop to Zero", 
                         font_size=20, color=RED, weight=BOLD)
        self.add_fixed_in_frame_mobjects(lasso_text)
        lasso_text.move_to(UP*2.5 + LEFT*3)
        
        self.play(Write(lasso_text))
        
        lasso_curves = []
        for i, (path, color) in enumerate(zip(lasso_paths, lasso_colors)):
            curve = VMobject()
            curve.set_points_smoothly(path)
            curve.set_stroke(color, width=3)
            lasso_curves.append(curve)
            
            # Add coefficient label
            label = Text(f"β{i+1}", font_size=12, color=color, weight=BOLD)
            self.add_fixed_in_frame_mobjects(label)
            label.move_to(axes.coords_to_point(0, 2.5 - i*0.5) + LEFT*0.5)
            
            self.play(Create(curve), Write(label), run_time=0.8)
        
        self.wait(2)
        
        # Clear and show Ridge paths
        self.play(FadeOut(VGroup(*lasso_curves, lasso_text)))
        
        ridge_text = Text("Ridge: Coefficients Shrink but Never Zero", 
                         font_size=20, color=BLUE, weight=BOLD)
        self.add_fixed_in_frame_mobjects(ridge_text)
        ridge_text.move_to(UP*2.5 + LEFT*3)
        
        self.play(Write(ridge_text))
        
        # Ridge paths (all shrink toward zero but never reach it)
        ridge_curves = []
        ridge_colors = [BLUE, TEAL, GREEN, ORANGE, PURPLE]
        
        for i, color in enumerate(ridge_colors):
            path = []
            for lam in lambda_vals:
                coeff = (2.5 - i*0.5) * np.exp(-lam * 0.2)  # Slower decay, never zero
                path.append(axes.coords_to_point(lam, coeff))
            
            curve = VMobject()
            curve.set_points_smoothly(path)
            curve.set_stroke(color, width=3)
            ridge_curves.append(curve)
            
            self.play(Create(curve), run_time=0.8)
        
        self.wait(2)
        
        # Store path elements
        self.paths_elements = VGroup(axes, *ridge_curves, ridge_text)
        self.paths_title = paths_title
    
    def show_feature_selection(self):
        """Show feature selection comparison"""
        selection_title = Text("Feature Selection Comparison", 
                             font_size=28, color=ORANGE, weight=BOLD)
        selection_title.to_edge(UP, buff=0.5)
        self.play(ReplacementTransform(self.paths_title, selection_title))
        
        # Clear paths
        self.play(FadeOut(self.paths_elements))
        
        # Create dataset visualization
        dataset_text = Text("Dataset: 10 Features, 3 Truly Important", 
                          font_size=20, color=WHITE, weight=BOLD)
        self.add_fixed_in_frame_mobjects(dataset_text)
        dataset_text.move_to(UP*2.5)
        self.play(Write(dataset_text))
        
        # Show feature importance (true underlying)
        true_importance = [0.8, 0.1, 0.7, 0.05, 0.02, 0.01, 0.6, 0.03, 0.01, 0.04]
        feature_names = [f"β{i+1}" for i in range(10)]
        
        # Create three panels for comparison
        panel_width = 3.5
        panel_positions = [LEFT*4, ORIGIN, RIGHT*4]
        method_names = ["Lasso", "Ridge", "Elastic Net"]
        method_colors = [RED, BLUE, PURPLE]
        
        panels = []
        for i, (pos, method, color) in enumerate(zip(panel_positions, method_names, method_colors)):
            # Panel background
            panel_box = Rectangle(
                width=panel_width, height=5,
                fill_color=BLACK, fill_opacity=0.8,
                stroke_color=color, stroke_width=2
            ).move_to(pos + DOWN*0.5)
            
            # Panel title
            panel_title = Text(method, font_size=18, color=color, weight=BOLD)
            self.add_fixed_in_frame_mobjects(panel_title)
            panel_title.move_to(pos + UP*2)
            
            panels.append((panel_box, panel_title, pos, color))
            self.play(Create(panel_box), Write(panel_title))
        
        # Show feature selection results
        lasso_selected = [0, 2, 6]  # Only important features
        ridge_selected = list(range(10))  # All features
        elastic_selected = [0, 1, 2, 6]  # Mix of important and some correlated
        
        selections = [lasso_selected, ridge_selected, elastic_selected]
        
        for panel_idx, (selected_features, (panel_box, panel_title, pos, color)) in enumerate(zip(selections, panels)):
            y_start = UP*1.5
            
            for feat_idx in range(10):
                # Feature name
                feat_text = Text(f"β{feat_idx+1}", font_size=12, color=WHITE)
                self.add_fixed_in_frame_mobjects(feat_text)
                feat_text.move_to(pos + LEFT*1.2 + y_start + DOWN*feat_idx*0.3)
                
                # Selection indicator
                if feat_idx in selected_features:
                    if panel_idx == 1:  # Ridge - show small coefficient
                        coeff_val = f"{true_importance[feat_idx]*0.3:.2f}"
                        indicator = Text(f"✓ {coeff_val}", font_size=10, color=GREEN)
                    else:
                        indicator = Text("✓", font_size=14, color=GREEN, weight=BOLD)
                else:
                    indicator = Text("✗", font_size=14, color=RED, weight=BOLD)
                
                self.add_fixed_in_frame_mobjects(indicator)
                indicator.move_to(pos + RIGHT*0.8 + y_start + DOWN*feat_idx*0.3)
                
                self.play(Write(feat_text), Write(indicator), run_time=0.2)
        
        # Add summary statistics
        stats_y = DOWN*3
        
        lasso_stats = Text("3 features\nR² = 0.85", font_size=12, color=RED)
        ridge_stats = Text("10 features\nR² = 0.87", font_size=12, color=BLUE)  
        elastic_stats = Text("4 features\nR² = 0.86", font_size=12, color=PURPLE)
        
        stats = [lasso_stats, ridge_stats, elastic_stats]
        
        for stat, (_, _, pos, _) in zip(stats, panels):
            self.add_fixed_in_frame_mobjects(stat)
            stat.move_to(pos + stats_y)
            self.play(Write(stat))
        
        self.wait(2)
        
        # Store selection elements
        self.selection_title = selection_title
    
    def show_final_summary(self):
        """Show final summary with key takeaways"""
        summary_title = Text("Key Takeaways", 
                           font_size=32, color=YELLOW, weight=BOLD)
        summary_title.to_edge(UP)
        self.play(ReplacementTransform(self.selection_title, summary_title))
        
        # Clear previous elements
        self.play(FadeOut(*[mob for mob in self.mobjects if mob != summary_title]))
        
        # Key insights
        insights = VGroup(
            VGroup(
                Text("Lasso (L1):", font_size=20, color=RED, weight=BOLD),
                Text("• Automatic feature selection", font_size=16, color=WHITE),
                Text("• Sets coefficients to exactly zero", font_size=16, color=WHITE),
                Text("• Good for sparse solutions", font_size=16, color=WHITE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2),
            
            VGroup(
                Text("Ridge (L2):", font_size=20, color=BLUE, weight=BOLD),
                Text("• Keeps all features", font_size=16, color=WHITE),
                Text("• Reduces multicollinearity", font_size=16, color=WHITE),
                Text("• Shrinks but doesn't zero", font_size=16, color=WHITE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2),
            
            VGroup(
                Text("Elastic Net:", font_size=20, color=PURPLE, weight=BOLD),
                Text("• Best of both worlds", font_size=16, color=WHITE),
                Text("• Handles correlated features better", font_size=16, color=WHITE),
                Text("• Tunable via α parameter", font_size=16, color=WHITE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        ).arrange(DOWN, buff=0.8)
        
        insights.move_to(UP*0.5)
        
        # Animate insights
        for insight_group in insights:
            self.play(*[Write(text) for text in insight_group], run_time=1.5)
        
        # Practical advice
        advice_box = Rectangle(
            width=10, height=1.5,
            fill_color=YELLOW, fill_opacity=0.2,
            stroke_color=YELLOW, stroke_width=2
        ).move_to(DOWN*3)
        
        advice_text = VGroup(
            Text("Practical Advice:", font_size=18, color=YELLOW, weight=BOLD),
            Text("Start with Elastic Net (α=0.5) as it combines benefits of both methods", 
                 font_size=14, color=WHITE)
        ).arrange(DOWN, buff=0.2)
        advice_text.move_to(advice_box.get_center())
        
        self.play(Create(advice_box))
        self.play(Write(advice_text))
        
        self.wait(3)

if __name__ == "__main__":
    # For testing
    pass