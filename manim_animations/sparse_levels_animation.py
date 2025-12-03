#!/usr/bin/env python3
"""
Sparse Levels Categorical Predictors Animation
Visual demonstration of sparse levels problem and intelligent grouping solutions
"""

from manim import *
import numpy as np

class SparseLevelsAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Show sparse levels problem setup
        self.show_sparse_levels_problem()
        
        # Demonstrate problems
        self.show_problems_demonstration()
        
        # Show target behavior analysis
        self.show_target_behavior_analysis()
        
        # Before/after comparison
        self.show_before_after_comparison()
        
        # Domain knowledge examples
        self.show_domain_knowledge()
        
        # Trade-off management
        self.show_trade_off_management()
    
    def show_sparse_levels_problem(self):
        """Show the sparse levels problem with realistic example"""
        title = Text("Sparse Levels in Categorical Predictors", 
                    font_size=30, color=YELLOW, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Example setup
        example_text = Text('Example: "Hour of Day" (0-23)', 
                          font_size=20, color=WHITE, weight=BOLD)
        example_text.move_to(UP*2.5)
        self.play(Write(example_text))
        
        # Create bar chart showing distribution
        axes = Axes(
            x_range=[0, 24, 6],
            y_range=[0, 6000, 1000],
            x_length=10,
            y_length=4,
            axis_config={"stroke_color": WHITE, "stroke_width": 2}
        ).move_to(DOWN*0.5)
        
        x_label = Text("Hour of Day", font_size=16, color=WHITE)
        x_label.next_to(axes.x_axis, DOWN, buff=0.3)
        
        y_label = Text("Observations", font_size=16, color=WHITE)
        y_label.next_to(axes.y_axis, LEFT, buff=0.3)
        y_label.rotate(PI/2)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Generate realistic hour distribution (business hours high, night low)
        hours = list(range(24))
        # Simulate realistic distribution - high during business hours, low at night
        observations = []
        for hour in hours:
            if 9 <= hour <= 17:  # Business hours
                obs = np.random.normal(4500, 500)
            elif 6 <= hour <= 8 or 18 <= hour <= 21:  # Commute/evening
                obs = np.random.normal(2500, 300)
            elif 22 <= hour <= 23 or 0 <= hour <= 1:  # Late night
                obs = np.random.normal(800, 200)
            else:  # Very early morning 2-5 AM
                obs = np.random.normal(50, 30)
            observations.append(max(10, int(obs)))  # Minimum 10 observations
        
        # Create bars
        bars = VGroup()
        sparse_bars = VGroup()  # Track sparse levels
        
        for hour, obs in zip(hours, observations):
            bar_height = obs / 1000  # Scale for display
            bar = Rectangle(
                width=0.3,
                height=bar_height,
                fill_opacity=0.8,
                stroke_color=WHITE,
                stroke_width=1
            )
            
            # Color based on sparsity
            if obs < 200:
                bar.set_fill(RED)  # Sparse
                sparse_bars.add(bar)
            elif obs < 1000:
                bar.set_fill(ORANGE)  # Moderate
            else:
                bar.set_fill(GREEN)  # Dense
            
            bar.move_to(axes.coords_to_point(hour + 0.5, bar_height/2))
            bars.add(bar)
        
        # Animate bars appearing
        for i in range(0, 24, 4):
            self.play(*[GrowFromEdge(bars[j], DOWN) for j in range(i, min(i+4, 24))], run_time=0.5)
        
        # Show sample counts for examples
        high_count_text = Text(f"Hour 14: {observations[14]:,} obs", 
                             font_size=12, color=GREEN, weight=BOLD)
        high_count_text.move_to(RIGHT*4 + UP*1)
        
        low_count_text = Text(f"Hour 3: {observations[3]} obs", 
                            font_size=12, color=RED, weight=BOLD)
        low_count_text.move_to(RIGHT*4 + UP*0.5)
        
        self.play(Write(high_count_text), Write(low_count_text))
        
        # Highlight sparse levels
        sparse_boxes = VGroup()
        for bar in sparse_bars:
            box = SurroundingRectangle(bar, color=RED, stroke_width=3, buff=0.1)
            sparse_boxes.add(box)
        
        sparse_label = Text("Sparse Levels", font_size=16, color=RED, weight=BOLD)
        sparse_label.move_to(RIGHT*4 + ORIGIN)
        
        self.play(Create(sparse_boxes), Write(sparse_label))
        
        # Show dummy variables expansion
        dummy_text = Text("One-hot encoding: 1 column → 24 columns", 
                         font_size=16, color=ORANGE, weight=BOLD)
        dummy_text.move_to(DOWN*3)
        self.play(Write(dummy_text))
        
        self.wait(2)
        
        # Store elements
        self.sparse_elements = VGroup(
            axes, x_label, y_label, bars, high_count_text, low_count_text,
            sparse_boxes, sparse_label, dummy_text, example_text
        )
        self.title = title
        self.observations = observations  # Store for later use
    
    def show_problems_demonstration(self):
        """Demonstrate high dimensionality and overfitting issues"""
        problems_title = Text("Problems with Sparse Levels", 
                            font_size=28, color=RED, weight=BOLD)
        problems_title.to_edge(UP, buff=0.5)
        self.play(ReplacementTransform(self.title, problems_title))
        
        # Clear previous elements
        self.play(FadeOut(self.sparse_elements))
        
        # Split into two problem areas
        problem1_title = Text("High Dimensionality", font_size=20, color=BLUE, weight=BOLD)
        problem1_title.move_to(LEFT*4 + UP*2)
        
        problem2_title = Text("Overfitting Risk", font_size=20, color=PURPLE, weight=BOLD)
        problem2_title.move_to(RIGHT*4 + UP*2)
        
        self.play(Write(problem1_title), Write(problem2_title))
        
        # Problem 1: High Dimensionality
        dim_box = Rectangle(width=6, height=4, stroke_color=BLUE, stroke_width=2,
                           fill_color=BLACK, fill_opacity=0.8).move_to(LEFT*4 + DOWN*0.5)
        
        # Show feature matrix expanding
        matrix_before = Text("Features: 1", font_size=16, color=WHITE)
        matrix_before.move_to(LEFT*4 + UP*0.5)
        
        arrow = Arrow(LEFT*2.5, LEFT*1.5, color=YELLOW)
        
        matrix_after = Text("Features: 24", font_size=16, color=RED, weight=BOLD)
        matrix_after.move_to(LEFT*4 + UP*0.5)
        
        curse_text = VGroup(
            Text("Curse of", font_size=14, color=RED),
            Text("Dimensionality", font_size=14, color=RED)
        ).arrange(DOWN, buff=0.1)
        curse_text.move_to(LEFT*4 + ORIGIN)
        
        complexity_text = Text("Model complexity ↗", font_size=12, color=ORANGE)
        complexity_text.move_to(LEFT*4 + DOWN*1)
        
        self.play(Create(dim_box))
        self.play(Write(matrix_before))
        self.play(GrowArrow(arrow))
        self.play(ReplacementTransform(matrix_before, matrix_after))
        self.play(Write(curse_text), Write(complexity_text))
        
        # Problem 2: Overfitting Risk
        overfit_box = Rectangle(width=6, height=4, stroke_color=PURPLE, stroke_width=2,
                               fill_color=BLACK, fill_opacity=0.8).move_to(RIGHT*4 + DOWN*0.5)
        
        # Show decision tree split on sparse level
        tree_text = Text("Decision Tree Split:", font_size=14, color=WHITE, weight=BOLD)
        tree_text.move_to(RIGHT*4 + UP*0.7)
        
        split_text = Text("If Hour = 3 → High Risk", font_size=12, color=RED)
        split_text.move_to(RIGHT*4 + UP*0.2)
        
        obs_text = Text("Based on only 47 obs!", font_size=12, color=RED, weight=BOLD)
        obs_text.move_to(RIGHT*4 + DOWN*0.3)
        
        # Confidence intervals visualization
        ci_text = VGroup(
            Text("Confidence Intervals:", font_size=12, color=WHITE),
            Text("Sparse: ± 0.15 (wide)", font_size=10, color=RED),
            Text("Dense: ± 0.02 (narrow)", font_size=10, color=GREEN)
        ).arrange(DOWN, buff=0.1)
        ci_text.move_to(RIGHT*4 + DOWN*1.2)
        
        self.play(Create(overfit_box))
        self.play(Write(tree_text), Write(split_text))
        self.play(Write(obs_text))
        self.play(Write(ci_text))
        
        # Show train vs validation divergence
        divergence_text = Text("Training ≠ Validation Performance", 
                              font_size=14, color=RED, weight=BOLD)
        divergence_text.move_to(DOWN*3)
        self.play(Write(divergence_text))
        
        self.wait(3)
        
        # Store elements
        self.problems_elements = VGroup(
            problem1_title, problem2_title, dim_box, overfit_box,
            matrix_after, arrow, curse_text, complexity_text,
            tree_text, split_text, obs_text, ci_text, divergence_text
        )
        self.problems_title = problems_title
    
    def show_target_behavior_analysis(self):
        """Show target behavior analysis and smart grouping"""
        analysis_title = Text("Target Behavior Analysis", 
                            font_size=28, color=GREEN, weight=BOLD)
        analysis_title.to_edge(UP, buff=0.5)
        self.play(ReplacementTransform(self.problems_title, analysis_title))
        
        # Clear previous elements
        self.play(FadeOut(self.problems_elements))
        
        # Create line plot: Hour vs Target Variable Mean
        axes = Axes(
            x_range=[0, 24, 6],
            y_range=[0.2, 0.8, 0.2],
            x_length=10,
            y_length=5,
            axis_config={"stroke_color": WHITE, "stroke_width": 2}
        ).move_to(DOWN*0.3)
        
        x_label = Text("Hour of Day", font_size=16, color=WHITE)
        x_label.next_to(axes.x_axis, DOWN, buff=0.3)
        
        y_label = Text("Target Variable Mean", font_size=16, color=WHITE)
        y_label.next_to(axes.y_axis, LEFT, buff=0.3)
        y_label.rotate(PI/2)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Generate realistic target behavior pattern
        hours = np.arange(0, 24, 1)
        # Business pattern: higher conversion during business hours
        target_means = []
        for hour in hours:
            if 6 <= hour <= 11:  # Morning
                mean = 0.45 + 0.05 * np.random.normal()
            elif 12 <= hour <= 17:  # Afternoon - highest conversion
                mean = 0.62 + 0.03 * np.random.normal()
            elif 18 <= hour <= 23 or 0 <= hour <= 5:  # Evening/Night
                mean = 0.38 + 0.04 * np.random.normal()
            target_means.append(np.clip(mean, 0.2, 0.8))
        
        # Create line plot
        points = [axes.coords_to_point(h, tm) for h, tm in zip(hours, target_means)]
        target_line = VMobject()
        target_line.set_points_smoothly(points)
        target_line.set_stroke(BLUE, width=3)
        
        self.play(Create(target_line), run_time=2)
        
        # Show pattern discovery
        pattern_text = Text("Pattern Discovery:", font_size=18, color=WHITE, weight=BOLD)
        pattern_text.move_to(UP*2.2)
        self.play(Write(pattern_text))
        
        # Animate grouping discovery
        # Morning group (6-11)
        morning_box = Rectangle(width=2.1, height=0.6, stroke_color=ORANGE, 
                               stroke_width=3, fill_opacity=0.2, fill_color=ORANGE)
        morning_box.move_to(axes.coords_to_point(8.5, 0.45))
        
        morning_label = Text("Morning\n(6-11)", font_size=12, color=ORANGE, weight=BOLD)
        morning_label.move_to(axes.coords_to_point(8.5, 0.7))
        
        # Afternoon group (12-17)
        afternoon_box = Rectangle(width=2.5, height=0.6, stroke_color=GREEN, 
                                 stroke_width=3, fill_opacity=0.2, fill_color=GREEN)
        afternoon_box.move_to(axes.coords_to_point(14.5, 0.62))
        
        afternoon_label = Text("Afternoon\n(12-17)", font_size=12, color=GREEN, weight=BOLD)
        afternoon_label.move_to(axes.coords_to_point(14.5, 0.52))
        
        # Evening/Night group (18-23, 0-5)
        evening_box1 = Rectangle(width=2.5, height=0.6, stroke_color=PURPLE, 
                                stroke_width=3, fill_opacity=0.2, fill_color=PURPLE)
        evening_box1.move_to(axes.coords_to_point(20.5, 0.38))
        
        evening_box2 = Rectangle(width=2.5, height=0.6, stroke_color=PURPLE, 
                                stroke_width=3, fill_opacity=0.2, fill_color=PURPLE)
        evening_box2.move_to(axes.coords_to_point(2.5, 0.38))
        
        evening_label = Text("Evening/Night\n(18-5)", font_size=12, color=PURPLE, weight=BOLD)
        evening_label.move_to(axes.coords_to_point(20.5, 0.28))
        
        # Animate grouping
        self.play(Create(morning_box), Write(morning_label))
        self.play(Create(afternoon_box), Write(afternoon_label))
        self.play(Create(evening_box1), Create(evening_box2), Write(evening_label))
        
        # Show target means
        means_text = VGroup(
            Text("Target Means:", font_size=14, color=WHITE, weight=BOLD),
            Text("Morning: 0.45", font_size=12, color=ORANGE),
            Text("Afternoon: 0.62", font_size=12, color=GREEN),
            Text("Evening: 0.38", font_size=12, color=PURPLE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        means_text.move_to(RIGHT*4 + UP*0.5)
        
        for text in means_text:
            self.play(Write(text), run_time=0.6)
        
        # Key insight
        insight = Text("Smart grouping based on target behavior!", 
                      font_size=16, color=YELLOW, weight=BOLD)
        insight.move_to(DOWN*3.2)
        self.play(Write(insight))
        
        self.wait(3)
        
        # Store elements
        self.analysis_elements = VGroup(
            axes, x_label, y_label, target_line, pattern_text,
            morning_box, morning_label, afternoon_box, afternoon_label,
            evening_box1, evening_box2, evening_label, means_text, insight
        )
        self.analysis_title = analysis_title
    
    def show_before_after_comparison(self):
        """Show before/after comparison"""
        comparison_title = Text("Before vs After Comparison", 
                              font_size=28, color=BLUE, weight=BOLD)
        comparison_title.to_edge(UP, buff=0.5)
        self.play(ReplacementTransform(self.analysis_title, comparison_title))
        
        # Clear previous elements
        self.play(FadeOut(self.analysis_elements))
        
        # Create side-by-side comparison
        before_title = Text("BEFORE (Sparse)", font_size=20, color=RED, weight=BOLD)
        before_title.move_to(LEFT*4 + UP*2.5)
        
        after_title = Text("AFTER (Grouped)", font_size=20, color=GREEN, weight=BOLD)
        after_title.move_to(RIGHT*4 + UP*2.5)
        
        self.play(Write(before_title), Write(after_title))
        
        # Before panel
        before_box = Rectangle(width=6, height=5, stroke_color=RED, stroke_width=2,
                              fill_color=BLACK, fill_opacity=0.8).move_to(LEFT*4 + DOWN*0.2)
        
        before_content = VGroup(
            Text("• 24 categories", font_size=14, color=WHITE),
            Text("• Many with <50 obs", font_size=14, color=RED),
            Text("• High variance estimates", font_size=14, color=RED),
            Text("• Overfitting in trees", font_size=14, color=RED),
            Text("• Poor generalization", font_size=14, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        before_content.move_to(LEFT*4 + DOWN*0.2)
        
        # After panel
        after_box = Rectangle(width=6, height=5, stroke_color=GREEN, stroke_width=2,
                             fill_color=BLACK, fill_opacity=0.8).move_to(RIGHT*4 + DOWN*0.2)
        
        after_content = VGroup(
            Text("• 3 meaningful categories", font_size=14, color=WHITE),
            Text("• 8,000+ obs each", font_size=14, color=GREEN),
            Text("• Stable estimates", font_size=14, color=GREEN),
            Text("• Robust tree splits", font_size=14, color=GREEN),
            Text("• Better generalization", font_size=14, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        after_content.move_to(RIGHT*4 + DOWN*0.2)
        
        self.play(Create(before_box), Create(after_box))
        
        # Animate content appearing
        for before_item, after_item in zip(before_content, after_content):
            self.play(Write(before_item), Write(after_item), run_time=0.8)
        
        # Show transformation arrow
        transform_arrow = Arrow(LEFT*1, RIGHT*1, color=YELLOW, stroke_width=6)
        transform_text = Text("24 → 3", font_size=18, color=YELLOW, weight=BOLD)
        transform_text.next_to(transform_arrow, UP, buff=0.2)
        
        self.play(GrowArrow(transform_arrow), Write(transform_text))
        
        # Performance improvement
        performance_text = Text("Model Accuracy: 73% → 81%", 
                              font_size=16, color=GREEN, weight=BOLD)
        performance_text.move_to(DOWN*3.5)
        self.play(Write(performance_text))
        
        self.wait(3)
        
        # Store elements
        self.comparison_elements = VGroup(
            before_title, after_title, before_box, after_box,
            before_content, after_content, transform_arrow, 
            transform_text, performance_text
        )
        self.comparison_title = comparison_title
    
    def show_domain_knowledge(self):
        """Show domain knowledge examples"""
        domain_title = Text("Domain Knowledge Examples", 
                          font_size=28, color=PURPLE, weight=BOLD)
        domain_title.to_edge(UP, buff=0.5)
        self.play(ReplacementTransform(self.comparison_title, domain_title))
        
        # Clear previous elements
        self.play(FadeOut(self.comparison_elements))
        
        # Show multiple examples of smart grouping
        examples = [
            {
                "title": "Geographic Grouping",
                "before": "50 US States",
                "after": "4 Regions",
                "groups": ["Northeast", "Southeast", "West", "Midwest"],
                "color": BLUE,
                "position": UP*1.5 + LEFT*4
            },
            {
                "title": "Industry Codes",
                "before": "200+ NAICS codes", 
                "after": "4 Sectors",
                "groups": ["Tech", "Finance", "Manufacturing", "Services"],
                "color": GREEN,
                "position": UP*1.5 + RIGHT*4
            },
            {
                "title": "Age Demographics",
                "before": "100 individual ages",
                "after": "3 Life Stages", 
                "groups": ["Young (18-30)", "Middle (31-50)", "Senior (51+)"],
                "color": ORANGE,
                "position": DOWN*1.5 + ORIGIN
            }
        ]
        
        for example in examples:
            # Create example box
            example_box = Rectangle(width=5, height=3, stroke_color=example["color"], 
                                  stroke_width=2, fill_color=BLACK, fill_opacity=0.8)
            example_box.move_to(example["position"])
            
            # Title
            example_title = Text(example["title"], font_size=16, 
                               color=example["color"], weight=BOLD)
            example_title.move_to(example["position"] + UP*1.2)
            
            # Before/After
            before_text = Text(f"Before: {example['before']}", font_size=12, color=RED)
            before_text.move_to(example["position"] + UP*0.6)
            
            after_text = Text(f"After: {example['after']}", font_size=12, color=GREEN)
            after_text.move_to(example["position"] + UP*0.3)
            
            # Groups
            groups_text = VGroup(*[Text(group, font_size=10, color=WHITE) 
                                 for group in example["groups"]])
            groups_text.arrange(DOWN, buff=0.1)
            groups_text.move_to(example["position"] + DOWN*0.3)
            
            self.play(Create(example_box), Write(example_title))
            self.play(Write(before_text), Write(after_text))
            self.play(*[Write(group) for group in groups_text])
        
        # Key principle
        principle = Text("Use business knowledge + statistical evidence", 
                        font_size=18, color=YELLOW, weight=BOLD)
        principle.move_to(DOWN*3.5)
        self.play(Write(principle))
        
        self.wait(3)
        
        # Store elements for cleanup
        self.domain_elements = VGroup(*self.mobjects[-50:])  # Rough estimate of recent objects
        self.domain_title = domain_title
    
    def show_trade_off_management(self):
        """Show trade-off management principles"""
        tradeoff_title = Text("Trade-off Management", 
                            font_size=32, color=YELLOW, weight=BOLD)
        tradeoff_title.to_edge(UP)
        self.play(ReplacementTransform(self.domain_title, tradeoff_title))
        
        # Clear previous elements
        self.play(FadeOut(self.domain_elements))
        
        # Show balance beam
        beam = Line(LEFT*4, RIGHT*4, color=WHITE, stroke_width=4)
        beam.move_to(UP*1)
        
        fulcrum = Triangle(color=WHITE, fill_opacity=1).scale(0.3)
        fulcrum.move_to(UP*0.7)
        
        self.play(Create(beam), Create(fulcrum))
        
        # Left side: Sample size
        left_weight = Circle(radius=0.8, color=BLUE, fill_opacity=0.8)
        left_weight.move_to(LEFT*3 + UP*1.8)
        
        left_text = VGroup(
            Text("Enough", font_size=16, color=BLUE, weight=BOLD),
            Text("Observations", font_size=16, color=BLUE, weight=BOLD),
            Text("Per Group", font_size=16, color=BLUE, weight=BOLD)
        ).arrange(DOWN, buff=0.1)
        left_text.move_to(LEFT*3 + UP*1.8)
        
        # Right side: Meaningful differences
        right_weight = Circle(radius=0.8, color=GREEN, fill_opacity=0.8)
        right_weight.move_to(RIGHT*3 + UP*1.8)
        
        right_text = VGroup(
            Text("Preserve", font_size=16, color=GREEN, weight=BOLD),
            Text("Meaningful", font_size=16, color=GREEN, weight=BOLD),
            Text("Differences", font_size=16, color=GREEN, weight=BOLD)
        ).arrange(DOWN, buff=0.1)
        right_text.move_to(RIGHT*3 + UP*1.8)
        
        self.play(Create(left_weight), Create(right_weight))
        self.play(Write(left_text), Write(right_text))
        
        # Guidelines
        guidelines_title = Text("Guidelines:", font_size=20, color=WHITE, weight=BOLD)
        guidelines_title.move_to(UP*0.2)
        
        guidelines = VGroup(
            Text("• Minimum 100-500 observations per level", font_size=16, color=WHITE),
            Text("• Statistically significant target differences", font_size=16, color=WHITE),
            Text("• Business interpretability maintained", font_size=16, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        guidelines.move_to(DOWN*0.8)
        
        self.play(Write(guidelines_title))
        for guideline in guidelines:
            self.play(Write(guideline), run_time=0.8)
        
        # Mathematical elements
        math_box = Rectangle(width=10, height=1.5, stroke_color=ORANGE, 
                           stroke_width=2, fill_color=BLACK, fill_opacity=0.8)
        math_box.move_to(DOWN*2.8)
        
        math_content = VGroup(
            Text("Statistical Tests:", font_size=14, color=ORANGE, weight=BOLD),
            Text("CI = x̄ ± t×(s/√n)     ANOVA F-test     n ≥ (z×σ/E)²", 
                 font_size=12, color=WHITE)
        ).arrange(DOWN, buff=0.1)
        math_content.move_to(DOWN*2.8)
        
        self.play(Create(math_box), Write(math_content))
        
        # Final key message
        key_message = Text("Group by target behavior, not just frequency!", 
                          font_size=18, color=YELLOW, weight=BOLD)
        key_message.move_to(DOWN*3.8)
        self.play(Write(key_message))
        
        self.wait(4)

if __name__ == "__main__":
    # For testing
    pass