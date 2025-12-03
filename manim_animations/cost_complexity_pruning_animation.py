#!/usr/bin/env python3
"""
Cost-Complexity Pruning Animation
Demonstrates pruning process in decision trees using cost-complexity parameter
Following detailed specifications for educational visualization
"""

from manim import *
import numpy as np

class CostComplexityPruningAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Show initial overfitted tree (3 seconds)
        self.show_initial_tree()
        
        # Show cost-complexity formula (2 seconds)
        self.show_formula()
        
        # Animate pruning sequence (4 seconds)
        self.animate_pruning_sequence()
        
        # Show optimal cp and performance comparison (4 seconds)
        self.show_optimal_result()
    
    def create_tree_structure(self, depth=6, position=ORIGIN, scale=1.0, pruned_levels=None):
        """Create a tree structure with given depth"""
        if pruned_levels is None:
            pruned_levels = []
        
        tree_group = VGroup()
        node_radius = 0.06 * scale
        level_spacing = 0.5 * scale
        
        # Create nodes level by level
        nodes_by_level = {}
        
        for level in range(depth + 1):
            nodes_by_level[level] = []
            
            num_nodes = 2**level
            if level > 0:
                y_pos = position[1] - level * level_spacing
            else:
                y_pos = position[1]
            
            for i in range(num_nodes):
                # Skip nodes in pruned levels
                if level in pruned_levels:
                    continue
                
                if num_nodes == 1:
                    x_pos = position[0]
                else:
                    x_pos = position[0] + (i - (num_nodes-1)/2) * (3*scale/(num_nodes*0.3))
                
                # Terminal nodes are green, internal nodes are blue
                if level == depth and level not in pruned_levels:
                    node_color = GREEN
                    fill_opacity = 0.7
                else:
                    node_color = BLUE
                    fill_opacity = 0.5
                
                node = Circle(
                    radius=node_radius,
                    color=node_color,
                    fill_opacity=fill_opacity,
                    stroke_width=2
                ).move_to([x_pos, y_pos, 0])
                
                nodes_by_level[level].append(node)
                tree_group.add(node)
                
                # Create lines to parent
                if level > 0 and level-1 not in pruned_levels:
                    parent_idx = i // 2
                    if parent_idx < len(nodes_by_level[level-1]):
                        parent = nodes_by_level[level-1][parent_idx]
                        line = Line(
                            parent.get_center(),
                            node.get_center(),
                            stroke_color=WHITE,
                            stroke_width=1.5 * scale
                        )
                        tree_group.add(line)
        
        return tree_group, nodes_by_level
    
    def create_decision_boundaries(self, complexity="high", position=RIGHT*4):
        """Create 2D plot showing decision boundaries"""
        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=3,
            y_length=3,
            axis_config={"stroke_width": 1, "stroke_color": GRAY}
        ).move_to(position)
        
        # Create data points
        np.random.seed(42)
        n_points = 25
        class_1_x = np.random.normal(-0.5, 0.6, n_points//2)
        class_1_y = np.random.normal(-0.5, 0.6, n_points//2)
        class_2_x = np.random.normal(0.5, 0.6, n_points//2)
        class_2_y = np.random.normal(0.5, 0.6, n_points//2)
        
        data_points = VGroup()
        for x, y in zip(class_1_x, class_1_y):
            if -2 <= x <= 2 and -2 <= y <= 2:
                point = Dot(axes.coords_to_point(x, y), color=RED, radius=0.04)
                data_points.add(point)
        
        for x, y in zip(class_2_x, class_2_y):
            if -2 <= x <= 2 and -2 <= y <= 2:
                point = Dot(axes.coords_to_point(x, y), color=BLUE, radius=0.04)
                data_points.add(point)
        
        # Create decision boundary based on complexity
        boundary_lines = VGroup()
        
        if complexity == "high":
            # Complex, jagged boundaries (overfitted)
            boundary_points = []
            for i in range(25):
                x = -1.8 + i * 0.14
                y = 0.3 * np.sin(12*x) + 0.15 * np.sin(30*x) + 0.1 * np.cos(50*x)
                boundary_points.append(axes.coords_to_point(x, y))
            
            for i in range(len(boundary_points)-1):
                line = Line(boundary_points[i], boundary_points[i+1], 
                          color=YELLOW, stroke_width=3)
                boundary_lines.add(line)
                
        elif complexity == "medium":
            # Moderately complex boundaries
            boundary_points = []
            for i in range(12):
                x = -1.5 + i * 0.25
                y = 0.4 * np.sin(5*x) + 0.1 * np.cos(15*x)
                boundary_points.append(axes.coords_to_point(x, y))
            
            for i in range(len(boundary_points)-1):
                line = Line(boundary_points[i], boundary_points[i+1], 
                          color=YELLOW, stroke_width=3)
                boundary_lines.add(line)
                
        else:  # "low"
            # Simple, smooth boundary
            line = Line(
                axes.coords_to_point(-1.5, -0.3),
                axes.coords_to_point(1.5, 0.3),
                color=YELLOW, stroke_width=4
            )
            boundary_lines.add(line)
        
        return VGroup(axes, data_points, boundary_lines)
    
    def show_initial_tree(self):
        """Show initial overfitted tree T₀"""
        title = Text("Cost-Complexity Pruning", font_size=32, color=YELLOW, weight=BOLD).to_edge(UP)
        self.play(Write(title))
        
        # Create initial large tree T₀
        initial_tree, nodes_by_level = self.create_tree_structure(
            depth=6, position=LEFT*4 + UP*0.3, scale=0.9
        )
        
        # Label the tree with subscript
        tree_label = VGroup(
            Text("T", font_size=18, color=YELLOW, weight=BOLD),
            Text("0", font_size=12, color=YELLOW, weight=BOLD).shift(RIGHT*0.15 + DOWN*0.15),
            Text(" - Initial Large Tree", font_size=14, color=WHITE)
        ).arrange(RIGHT, buff=0.02)
        tree_label.next_to(initial_tree, DOWN, buff=0.4)
        
        # Show overfitted decision boundaries
        boundaries_plot = self.create_decision_boundaries("high", RIGHT*3.5)
        boundaries_label = Text("Overfitted Boundaries", font_size=14, color=RED, weight=BOLD)
        boundaries_label.next_to(boundaries_plot, DOWN, buff=0.3)
        
        # Animate everything appearing (3 seconds total)
        self.play(
            Create(initial_tree),
            Write(tree_label),
            run_time=2
        )
        
        self.play(
            Create(boundaries_plot),
            Write(boundaries_label),
            run_time=1
        )
        
        # Add problem indicators
        problem_text = Text("Problems: Complex, Overfitted!", font_size=16, color=RED, weight=BOLD)
        problem_text.move_to(DOWN*2.8)
        self.play(Write(problem_text))
        
        self.wait(1)
        
        # Store elements
        self.initial_tree = initial_tree
        self.tree_label = tree_label
        self.boundaries_plot = boundaries_plot
        self.boundaries_label = boundaries_label
        self.problem_text = problem_text
        self.title = title
    
    def show_formula(self):
        """Show cost-complexity formula (2 seconds)"""
        formula_title = Text("Cost-Complexity Formula", font_size=24, color=GREEN, weight=BOLD)
        formula_title.move_to(UP*1.2)
        
        # Main formula using MathTex for proper mathematical notation
        formula = VGroup(
            Text("Cost = Training Error + ", font_size=18, color=WHITE),
            Text("cp", font_size=18, color=ORANGE, weight=BOLD, slant=ITALIC),
            Text(" × |Terminal Nodes|", font_size=18, color=WHITE)
        ).arrange(RIGHT)
        formula.next_to(formula_title, DOWN, buff=0.5)
        
        # Example calculation
        example = VGroup(
            Text("Cost = 0.15 + 0.01 × 12 = ", font_size=16, color=WHITE),
            Text("0.27", font_size=16, color=GREEN, weight=BOLD)
        ).arrange(RIGHT)
        example.next_to(formula, DOWN, buff=0.4)
        
        # Objective
        objective = Text("Find cp that minimizes total cost", font_size=14, color=ORANGE, slant=ITALIC)
        objective.next_to(example, DOWN, buff=0.4)
        
        # Clear previous problem text and show formula
        self.play(
            FadeOut(self.problem_text),
            Write(formula_title),
            Write(formula),
            Write(example),
            Write(objective),
            run_time=2
        )
        
        # Store formula elements
        self.formula_group = VGroup(formula_title, formula, example, objective)
    
    def animate_pruning_sequence(self):
        """Animate the pruning sequence T₀ → T₁ → T₂ → T₃ (4 seconds)"""
        # Move formula to top-right to make room
        self.play(
            self.formula_group.animate.scale(0.65).to_corner(UR),
            run_time=0.5
        )
        
        # Create cp parameter display
        cp_display = VGroup(
            Text("cp = ", font_size=16, color=WHITE),
            Text("0.00", font_size=16, color=ORANGE, weight=BOLD)
        ).arrange(RIGHT)
        cp_display.move_to(DOWN*2.5)
        
        self.play(Write(cp_display), run_time=0.5)
        
        # Pruning sequence with realistic numbers
        pruning_steps = [
            {"cp": 0.01, "pruned_levels": [6], "label": "T₁", "nodes": 32, "error": 0.18, "cost": 0.50},
            {"cp": 0.03, "pruned_levels": [5, 6], "label": "T₂", "nodes": 16, "error": 0.25, "cost": 0.73},
            {"cp": 0.05, "pruned_levels": [4, 5, 6], "label": "T₃", "nodes": 8, "error": 0.35, "cost": 0.75},
        ]
        
        current_tree = self.initial_tree
        current_label = self.tree_label
        
        for i, step in enumerate(pruning_steps):
            # Update cp display
            new_cp_display = VGroup(
                Text("cp = ", font_size=16, color=WHITE),
                Text(f"{step['cp']:.2f}", font_size=16, color=ORANGE, weight=BOLD)
            ).arrange(RIGHT)
            new_cp_display.move_to(cp_display.get_center())
            
            # Create new pruned tree
            new_tree, _ = self.create_tree_structure(
                depth=6, position=LEFT*4 + UP*0.3, scale=0.9, 
                pruned_levels=step["pruned_levels"]
            )
            
            # New tree label with cost information
            tree_info = VGroup(
                VGroup(
                    Text("T", font_size=18, color=YELLOW, weight=BOLD),
                    Text(str(i+1), font_size=12, color=YELLOW, weight=BOLD).shift(RIGHT*0.15 + DOWN*0.15)
                ).arrange(RIGHT, buff=0.02),
                Text(f"Nodes: {step['nodes']}", font_size=12, color=WHITE),
                Text(f"RSS: {step['error']:.2f}", font_size=12, color=WHITE),
                Text(f"Cost: {step['cost']:.2f}", font_size=12, color=GREEN, weight=BOLD)
            ).arrange(DOWN, buff=0.08)
            tree_info.next_to(new_tree, DOWN, buff=0.4)
            
            # Update decision boundaries
            if i == 0:
                new_boundaries = self.create_decision_boundaries("medium", RIGHT*3.5)
                boundary_text = "Moderately Complex"
            elif i == 1:
                new_boundaries = self.create_decision_boundaries("low", RIGHT*3.5)
                boundary_text = "Smoother Boundaries"
            else:
                new_boundaries = self.create_decision_boundaries("low", RIGHT*3.5)
                boundary_text = "Simple Boundaries"
            
            new_boundaries_label = Text(boundary_text, font_size=12, color=GREEN, weight=BOLD)
            new_boundaries_label.next_to(new_boundaries, DOWN, buff=0.3)
            
            # Show pruning action with red dashed lines for first step
            if i == 0:
                pruning_text = Text("Bottom-up pruning", font_size=14, color=RED, weight=BOLD)
                pruning_text.move_to(ORIGIN + DOWN*1.5)
                
                # Create red dashed lines for branches being pruned
                prune_lines = VGroup()
                base_pos = LEFT*4 + UP*0.3 + DOWN*3
                for j in range(6):
                    line = DashedLine(
                        base_pos + RIGHT*(j-2.5)*0.3,
                        base_pos + RIGHT*(j-2.5)*0.3 + DOWN*0.4,
                        color=RED, stroke_width=4
                    )
                    prune_lines.add(line)
                
                self.play(Write(pruning_text), run_time=0.3)
                self.play(Create(prune_lines), run_time=0.5)
                
                # Animate shrinking and fading out
                self.play(
                    Transform(cp_display, new_cp_display),
                    Transform(current_tree, new_tree, rate_func=smooth),
                    Transform(current_label, tree_info),
                    Transform(self.boundaries_plot, new_boundaries),
                    Transform(self.boundaries_label, new_boundaries_label),
                    Shrink(prune_lines),
                    FadeOut(prune_lines),
                    FadeOut(pruning_text),
                    run_time=1.2
                )
                
                # Educational overlay
                edu_text = Text("Pruning reduces overfitting", font_size=12, color=GREEN)
                edu_text.move_to(ORIGIN + DOWN*1.8)
                self.play(Write(edu_text), run_time=0.3)
                self.wait(0.2)
                self.play(FadeOut(edu_text), run_time=0.3)
                
            else:
                # Regular pruning steps
                self.play(
                    Transform(cp_display, new_cp_display),
                    Transform(current_tree, new_tree, rate_func=smooth),
                    Transform(current_label, tree_info),
                    Transform(self.boundaries_plot, new_boundaries),
                    Transform(self.boundaries_label, new_boundaries_label),
                    run_time=1.0
                )
                
                if i == 1:
                    edu_text = Text("Bottom-up approach preserves important splits", font_size=11, color=BLUE)
                    edu_text.move_to(ORIGIN + DOWN*1.8)
                    self.play(Write(edu_text), run_time=0.3)
                    self.wait(0.2)
                    self.play(FadeOut(edu_text), run_time=0.3)
        
        # Store final elements
        self.final_tree = current_tree
        self.final_label = current_label
        self.cp_display = cp_display
    
    def show_optimal_result(self):
        """Show optimal cp and performance comparison (4 seconds)"""
        # Create cost vs cp graph
        cost_axes = Axes(
            x_range=[0, 0.06, 0.02],
            y_range=[0.2, 0.8, 0.2],
            x_length=3.5,
            y_length=2.5,
            axis_config={"stroke_width": 2, "stroke_color": WHITE}
        ).to_corner(UL, buff=0.3)
        
        cost_x_label = Text("cp", font_size=12, color=WHITE).next_to(cost_axes, DOWN, buff=0.1)
        cost_y_label = Text("Cost", font_size=12, color=WHITE).next_to(cost_axes, LEFT, buff=0.1).rotate(PI/2)
        
        # Cost curve (U-shaped) - realistic values
        cp_vals = np.linspace(0.005, 0.055, 30)
        cost_vals = 0.2 + 2*cp_vals + 50*(cp_vals - 0.02)**2
        cost_points = [cost_axes.coords_to_point(cp, cost) for cp, cost in zip(cp_vals, cost_vals)]
        
        cost_curve = VMobject(color=PURPLE, stroke_width=4)
        cost_curve.set_points_smoothly(cost_points)
        
        # Mark optimal point
        optimal_cp = 0.02
        optimal_cost = 0.2 + 2*optimal_cp + 50*(optimal_cp - 0.02)**2
        optimal_point = Dot(cost_axes.coords_to_point(optimal_cp, optimal_cost), 
                          color=YELLOW, radius=0.08)
        
        optimal_label = Text("Optimal cp", font_size=11, color=YELLOW, weight=BOLD)
        optimal_label.next_to(optimal_point, UP, buff=0.08)
        
        self.play(
            Create(cost_axes),
            Write(cost_x_label),
            Write(cost_y_label),
            run_time=1.0
        )
        
        self.play(Create(cost_curve), run_time=1.0)
        
        self.play(
            FadeIn(optimal_point, scale=1.5),
            Write(optimal_label),
            run_time=1.0
        )
        
        # Side-by-side comparison
        comparison_title = Text("Overfitted vs Pruned", font_size=16, color=CYAN, weight=BOLD)
        comparison_title.move_to(RIGHT*3.5 + UP*2.2)
        
        # Performance metrics with arrows showing direction
        metrics_display = VGroup(
            VGroup(
                Text("Training Error", font_size=12, color=WHITE),
                Text("↑", font_size=16, color=RED, weight=BOLD),
                Text("0.15 → 0.35", font_size=11, color=ORANGE)
            ).arrange(DOWN, buff=0.05),
            
            VGroup(
                Text("Complexity", font_size=12, color=WHITE),
                Text("↓", font_size=16, color=GREEN, weight=BOLD),
                Text("High → Low", font_size=11, color=GREEN)
            ).arrange(DOWN, buff=0.05),
            
            VGroup(
                Text("Generalization", font_size=12, color=WHITE),
                Text("✓", font_size=16, color=GREEN, weight=BOLD),
                Text("Poor → Good", font_size=11, color=GREEN)
            ).arrange(DOWN, buff=0.05)
        ).arrange(RIGHT, buff=1.2)
        
        metrics_display.next_to(comparison_title, DOWN, buff=0.3)
        
        self.play(Write(comparison_title), run_time=0.3)
        
        for metric in metrics_display:
            self.play(Write(metric), run_time=0.3)
        
        # Final insight with arrow pointing to optimal tree
        final_insight = Text("Best bias-variance tradeoff!", font_size=14, color=YELLOW, weight=BOLD)
        final_insight.to_edge(DOWN, buff=0.5)
        
        insight_arrow = Arrow(
            final_insight.get_top() + UP*0.1,
            self.final_tree.get_bottom() + DOWN*0.3,
            color=YELLOW,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.15
        )
        
        self.play(
            Write(final_insight),
            GrowArrow(insight_arrow),
            run_time=1.0
        )
        
        self.wait(3)