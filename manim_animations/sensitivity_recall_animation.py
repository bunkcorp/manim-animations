#!/usr/bin/env python3
"""
Sensitivity (Recall) Animation
Visual demonstration of what sensitivity measures
Focus on movement and practical examples
"""

from manim import *
import numpy as np

class SensitivityRecallAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#1E1E1E"
        
        # Show what sensitivity measures
        self.show_sensitivity_concept()
        
        # Show confusion matrix breakdown
        self.show_confusion_matrix()
        
        # Show formula demonstration
        self.show_formula_demo()
        
        # Show practical examples
        self.show_practical_examples()
        
        # Show sensitivity comparison
        self.show_sensitivity_comparison()
    
    def show_sensitivity_concept(self):
        """Show the basic concept of sensitivity"""
        title = Text("Sensitivity (Recall)", font_size=36, color=YELLOW, weight=BOLD).to_edge(UP)
        subtitle = Text("How well does the model catch positives?", font_size=24, color=WHITE)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        self.play(Write(title), Write(subtitle))
        
        # Create visual representation with moving elements
        # Show actual positives and what model catches
        actual_positives = VGroup()
        for i in range(10):
            dot = Circle(radius=0.2, color=GREEN, fill_opacity=0.8)
            dot.move_to(LEFT*4 + RIGHT*i*0.8 + UP*1)
            actual_positives.add(dot)
        
        actual_label = Text("Actual Positives (10)", font_size=16, color=GREEN, weight=BOLD)
        actual_label.next_to(actual_positives, UP, buff=0.3)
        
        self.play(*[FadeIn(dot, scale=1.5) for dot in actual_positives], Write(actual_label))
        
        # Show what model catches (7 out of 10)
        caught_indices = [0, 1, 2, 4, 5, 7, 9]  # Model catches 7
        missed_indices = [3, 6, 8]  # Model misses 3
        
        # Animate catching process
        catching_text = Text("Model trying to catch positives...", font_size=18, color=WHITE)
        catching_text.move_to(DOWN*0.5)
        self.play(Write(catching_text))
        
        # Show net catching positives
        net = Arc(radius=1.5, angle=PI, color=BLUE, stroke_width=5)
        net.move_to(DOWN*1.5)
        net.rotate(-PI/2)
        
        self.play(Create(net))
        
        # Move caught positives into net
        for idx in caught_indices:
            self.play(
                actual_positives[idx].animate.move_to(net.get_center() + 
                    0.3*np.array([np.cos(idx*0.5), np.sin(idx*0.5), 0])),
                run_time=0.3
            )
        
        # Highlight missed ones
        for idx in missed_indices:
            self.play(actual_positives[idx].animate.set_fill(RED), run_time=0.3)
        
        # Show result
        result_text = Text("Caught 7 out of 10 positives", font_size=18, color=BLUE, weight=BOLD)
        result_text.next_to(net, DOWN, buff=0.3)
        
        sensitivity_calc = Text("Sensitivity = 7/10 = 70%", font_size=20, color=YELLOW, weight=BOLD)
        sensitivity_calc.next_to(result_text, DOWN, buff=0.3)
        
        self.play(
            ReplacementTransform(catching_text, result_text),
            Write(sensitivity_calc)
        )
        
        self.wait(2)
        self.play(FadeOut(VGroup(
            actual_positives, actual_label, net, result_text, sensitivity_calc
        )))
        self.title = title
        self.subtitle = subtitle
    
    def show_confusion_matrix(self):
        """Show confusion matrix with animated breakdown"""
        matrix_title = Text("Confusion Matrix Breakdown", font_size=28, color=PURPLE, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(VGroup(self.title, self.subtitle), matrix_title))
        
        # Create confusion matrix
        matrix_size = 3
        matrix_pos = ORIGIN
        
        # Create grid
        grid = VGroup()
        for i in range(3):
            for j in range(3):
                if i == 0 or j == 0:  # Headers
                    cell = Rectangle(width=matrix_size*0.8, height=matrix_size*0.8, 
                                   stroke_color=WHITE, fill_color=GRAY, fill_opacity=0.3)
                else:
                    cell = Rectangle(width=matrix_size*0.8, height=matrix_size*0.8, 
                                   stroke_color=WHITE, fill_color=BLACK, fill_opacity=0.1)
                
                cell.move_to(matrix_pos + RIGHT*(j-1)*matrix_size*0.8 + DOWN*(i-1)*matrix_size*0.8)
                grid.add(cell)
        
        self.play(Create(grid))
        
        # Add labels
        labels = [
            ("", 0, 0), ("Predicted", 1, 0), ("", 2, 0),
            ("Actual", 0, 1), ("Negative", 1, 1), ("Positive", 2, 1),
            ("", 0, 2), ("TN", 1, 2), ("FP", 2, 2),
            ("", 0, 3), ("FN", 1, 3), ("TP", 2, 3)
        ]
        
        label_objects = VGroup()
        for text, col, row in labels[:6]:  # First 6 are headers
            if text:
                label = Text(text, font_size=16, color=WHITE, weight=BOLD)
                label.move_to(matrix_pos + RIGHT*(col-1)*matrix_size*0.8 + DOWN*(row-1)*matrix_size*0.8)
                label_objects.add(label)
        
        self.play(*[Write(label) for label in label_objects])
        
        # Add matrix values with animation
        values = [
            ("850", 1, 2, WHITE),  # TN
            ("50", 2, 2, RED),     # FP  
            ("30", 1, 3, RED),     # FN
            ("70", 2, 3, GREEN)    # TP
        ]
        
        value_objects = VGroup()
        for text, col, row, color in values:
            value = Text(text, font_size=20, color=color, weight=BOLD)
            value.move_to(matrix_pos + RIGHT*(col-1)*matrix_size*0.8 + DOWN*(row-1)*matrix_size*0.8)
            value_objects.add(value)
        
        # Animate values appearing
        for i, value in enumerate(value_objects):
            self.play(FadeIn(value, scale=1.5), run_time=0.5)
        
        # Highlight sensitivity calculation
        tp_highlight = Rectangle(width=matrix_size*0.8, height=matrix_size*0.8,
                               stroke_color=YELLOW, stroke_width=4, fill_opacity=0)
        tp_highlight.move_to(matrix_pos + RIGHT*matrix_size*0.8 + DOWN*matrix_size*0.8)
        
        fn_highlight = Rectangle(width=matrix_size*0.8, height=matrix_size*0.8,
                               stroke_color=YELLOW, stroke_width=4, fill_opacity=0)
        fn_highlight.move_to(matrix_pos + DOWN*matrix_size*0.8)
        
        self.play(Create(tp_highlight), Create(fn_highlight))
        
        # Show formula
        formula = Text("Sensitivity = TP / (TP + FN)", font_size=24, color=YELLOW, weight=BOLD)
        formula.move_to(DOWN*3)
        
        calculation = Text("= 70 / (70 + 30) = 70%", font_size=20, color=WHITE)
        calculation.next_to(formula, DOWN, buff=0.3)
        
        self.play(Write(formula), Write(calculation))
        
        self.wait(2)
        self.play(FadeOut(VGroup(
            grid, label_objects, value_objects, tp_highlight, fn_highlight, formula, calculation
        )))
        self.matrix_title = matrix_title
    
    def show_formula_demo(self):
        """Show formula with visual demonstration"""
        demo_title = Text("Visual Formula Demo", font_size=28, color=ORANGE, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.matrix_title, demo_title))
        
        # Create visual buckets
        tp_bucket = Rectangle(width=3, height=2, stroke_color=GREEN, fill_color=GREEN, fill_opacity=0.2)
        tp_bucket.move_to(LEFT*3 + UP*1)
        tp_label = Text("True Positives\n(TP)", font_size=16, color=GREEN, weight=BOLD)
        tp_label.next_to(tp_bucket, UP, buff=0.2)
        
        fn_bucket = Rectangle(width=3, height=2, stroke_color=RED, fill_color=RED, fill_opacity=0.2)
        fn_bucket.move_to(RIGHT*3 + UP*1)
        fn_label = Text("False Negatives\n(FN)", font_size=16, color=RED, weight=BOLD)
        fn_label.next_to(fn_bucket, UP, buff=0.2)
        
        self.play(Create(tp_bucket), Create(fn_bucket), Write(tp_label), Write(fn_label))
        
        # Fill buckets with dots
        tp_dots = VGroup()
        for i in range(7):
            dot = Circle(radius=0.1, color=GREEN, fill_opacity=1)
            dot.move_to(tp_bucket.get_center() + 
                       0.6*np.array([np.cos(i*0.9), np.sin(i*0.9), 0]))
            tp_dots.add(dot)
        
        fn_dots = VGroup()
        for i in range(3):
            dot = Circle(radius=0.1, color=RED, fill_opacity=1)
            dot.move_to(fn_bucket.get_center() + 
                       0.6*np.array([np.cos(i*2), np.sin(i*2), 0]))
            fn_dots.add(dot)
        
        # Animate dots falling into buckets
        for dot in tp_dots:
            start_pos = dot.get_center() + UP*3
            dot.move_to(start_pos)
            self.play(dot.animate.move_to(dot.get_center() + DOWN*3), run_time=0.3)
        
        for dot in fn_dots:
            start_pos = dot.get_center() + UP*3
            dot.move_to(start_pos)
            self.play(dot.animate.move_to(dot.get_center() + DOWN*3), run_time=0.3)
        
        # Show counting
        tp_count = Text("7", font_size=24, color=GREEN, weight=BOLD)
        tp_count.next_to(tp_bucket, DOWN, buff=0.3)
        
        fn_count = Text("3", font_size=24, color=RED, weight=BOLD)
        fn_count.next_to(fn_bucket, DOWN, buff=0.3)
        
        self.play(Write(tp_count), Write(fn_count))
        
        # Show formula calculation
        formula_parts = VGroup(
            Text("Sensitivity", font_size=20, color=YELLOW, weight=BOLD),
            Text("=", font_size=20, color=WHITE),
            Text("7", font_size=20, color=GREEN, weight=BOLD),
            Text("÷", font_size=20, color=WHITE),
            Text("(7 + 3)", font_size=20, color=WHITE),
            Text("=", font_size=20, color=WHITE),
            Text("70%", font_size=24, color=YELLOW, weight=BOLD)
        ).arrange(RIGHT, buff=0.3)
        
        formula_parts.move_to(DOWN*2.5)
        
        # Animate formula parts
        for part in formula_parts:
            self.play(Write(part), run_time=0.3)
        
        # Highlight the result
        result_highlight = Rectangle(width=1.5, height=0.8, stroke_color=YELLOW, 
                                   stroke_width=4, fill_opacity=0)
        result_highlight.move_to(formula_parts[-1].get_center())
        
        self.play(Create(result_highlight))
        self.play(result_highlight.animate.scale(1.2), run_time=0.5)
        self.play(result_highlight.animate.scale(1/1.2), run_time=0.5)
        
        self.wait(2)
        self.play(FadeOut(VGroup(
            tp_bucket, fn_bucket, tp_label, fn_label, tp_dots, fn_dots,
            tp_count, fn_count, formula_parts, result_highlight
        )))
        self.demo_title = demo_title
    
    def show_practical_examples(self):
        """Show practical examples where sensitivity matters"""
        examples_title = Text("When Sensitivity Matters", font_size=28, color=TEAL, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.demo_title, examples_title))
        
        # Create three scenarios
        scenarios = [
            ("Fraud Detection", "🏦", "Missing fraud is costly!", GREEN),
            ("Medical Diagnosis", "🏥", "Missing disease is dangerous!", RED),  
            ("Energy Usage", "⚡", "Missing high usage blocks!", BLUE)
        ]
        
        positions = [LEFT*4, ORIGIN, RIGHT*4]
        
        for i, ((title, icon, description, color), pos) in enumerate(zip(scenarios, positions)):
            # Scenario setup
            scenario_group = VGroup()
            
            # Title with icon
            scenario_title = VGroup(
                Text(icon, font_size=32),
                Text(title, font_size=16, color=color, weight=BOLD)
            ).arrange(DOWN, buff=0.2)
            scenario_title.move_to(pos + UP*2.5)
            
            # Create population of cases
            total_cases = 20
            positive_cases = 6
            
            cases = VGroup()
            for j in range(total_cases):
                if j < positive_cases:
                    case = Rectangle(width=0.2, height=0.2, fill_color=color, fill_opacity=0.8)
                else:
                    case = Rectangle(width=0.2, height=0.2, fill_color=GRAY, fill_opacity=0.3)
                
                row = j // 5
                col = j % 5
                case.move_to(pos + LEFT*0.5 + RIGHT*col*0.25 + UP*0.5 + DOWN*row*0.25)
                cases.add(case)
            
            # Show detection results
            if i == 0:  # Fraud - high sensitivity needed
                detected = [0, 1, 2, 3, 4]  # Catches 5/6 frauds
                sensitivity_val = "83%"
            elif i == 1:  # Medical - very high sensitivity needed
                detected = [0, 1, 2, 3, 4, 5]  # Catches all 6 diseases  
                sensitivity_val = "100%"
            else:  # Energy - moderate sensitivity
                detected = [0, 1, 3]  # Catches 3/6 high usage
                sensitivity_val = "50%"
            
            # Animate detection
            for idx in detected:
                self.play(cases[idx].animate.set_stroke(YELLOW, width=3), run_time=0.1)
            
            # Add sensitivity score
            score = Text(f"Sensitivity: {sensitivity_val}", font_size=14, color=color, weight=BOLD)
            score.move_to(pos + DOWN*1.5)
            
            # Add description
            desc = Text(description, font_size=12, color=WHITE)
            desc.next_to(score, DOWN, buff=0.2)
            
            scenario_group = VGroup(scenario_title, cases, score, desc)
            
            self.play(FadeIn(scenario_group))
            self.wait(1)
        
        # Add key insight
        insight = Text("High sensitivity = Few missed positives!", 
                      font_size=18, color=YELLOW, weight=BOLD)
        insight.to_edge(DOWN)
        self.play(Write(insight))
        
        self.wait(3)
        self.play(FadeOut(*self.mobjects[1:]))  # Keep title
        self.examples_title = examples_title
    
    def show_sensitivity_comparison(self):
        """Show comparison of different sensitivity levels"""
        comparison_title = Text("Sensitivity Levels Comparison", font_size=28, color=PINK, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(self.examples_title, comparison_title))
        
        # Create three sensitivity scenarios
        sensitivities = [30, 70, 95]
        labels = ["Low (30%)", "Medium (70%)", "High (95%)"]
        colors = [RED, ORANGE, GREEN]
        positions = [LEFT*4, ORIGIN, RIGHT*4]
        
        for sens, label, color, pos in zip(sensitivities, labels, colors, positions):
            # Title
            sens_title = Text(label, font_size=16, color=color, weight=BOLD)
            sens_title.move_to(pos + UP*2.5)
            
            # Create visualization
            total_positives = 20
            caught = int(total_positives * sens / 100)
            missed = total_positives - caught
            
            # Show caught positives (green dots)
            caught_dots = VGroup()
            for i in range(caught):
                dot = Circle(radius=0.08, color=GREEN, fill_opacity=1)
                row = i // 5
                col = i % 5
                dot.move_to(pos + LEFT*0.4 + RIGHT*col*0.2 + UP*1 + DOWN*row*0.2)
                caught_dots.add(dot)
            
            # Show missed positives (red X's)  
            missed_dots = VGroup()
            for i in range(missed):
                x_mark = Text("✗", font_size=16, color=RED, weight=BOLD)
                row = (caught + i) // 5
                col = (caught + i) % 5
                x_mark.move_to(pos + LEFT*0.4 + RIGHT*col*0.2 + UP*1 + DOWN*row*0.2)
                missed_dots.add(x_mark)
            
            # Labels
            caught_label = Text(f"Caught: {caught}", font_size=12, color=GREEN)
            caught_label.move_to(pos + DOWN*0.5)
            
            missed_label = Text(f"Missed: {missed}", font_size=12, color=RED)
            missed_label.next_to(caught_label, DOWN, buff=0.1)
            
            # Cost indicator
            if sens < 50:
                cost_text = Text("High Cost!", font_size=12, color=RED, weight=BOLD)
            elif sens < 80:
                cost_text = Text("Medium Cost", font_size=12, color=ORANGE)
            else:
                cost_text = Text("Low Cost", font_size=12, color=GREEN)
            
            cost_text.next_to(missed_label, DOWN, buff=0.2)
            
            # Animate everything appearing
            group = VGroup(sens_title, caught_dots, missed_dots, caught_label, missed_label, cost_text)
            self.play(FadeIn(group))
            self.wait(0.5)
        
        # Final message
        final_message = Text("Choose sensitivity based on cost of missing positives!", 
                           font_size=16, color=YELLOW, weight=BOLD)
        final_message.to_edge(DOWN)
        
        self.play(Write(final_message))
        self.wait(3)