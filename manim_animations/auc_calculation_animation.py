from manim import *
import numpy as np

class AUCCalculation(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = "#1E1E2A"
        
        # Title
        title = Text("Calculating AUC from Confusion Matrix", font_size=40, color=WHITE, weight=BOLD)
        title.to_edge(UP)
        subtitle = Text("Using TPR, FPR, and Trapezoid Rule", font_size=28, color=YELLOW)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(Write(subtitle))
        self.wait(2)
        
        # Fade out title
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # Show confusion matrix
        self.show_confusion_matrix()
        
        # Calculate TPR and FPR
        self.calculate_rates()
        
        # Show ROC curve
        self.show_roc_curve()
        
        # Calculate AUC using trapezoid rule
        self.calculate_auc()
        
        # Summary
        self.show_summary()

    def show_confusion_matrix(self):
        # Confusion matrix title
        cm_title = Text("Confusion Matrix", font_size=32, color=WHITE, weight=BOLD)
        cm_title.to_edge(UP)
        
        # Create confusion matrix
        # Example values: TP=80, FP=20, FN=10, TN=90
        tp, fp, fn, tn = 80, 20, 10, 90
        
        # Matrix structure
        matrix = VGroup()
        
        # Headers
        header_row = VGroup(
            Text("", font_size=20, color=WHITE),  # Empty corner
            Text("Predicted", font_size=20, color=YELLOW, weight=BOLD),
            Text("", font_size=20, color=WHITE),  # Empty space
            Text("Negative", font_size=20, color=YELLOW, weight=BOLD),
        ).arrange(RIGHT, buff=0.5)
        
        # Row 1: Actual Positive
        row1 = VGroup(
            Text("Actual", font_size=20, color=YELLOW, weight=BOLD),
            Text("Positive", font_size=20, color=YELLOW, weight=BOLD),
            Text("", font_size=20, color=WHITE),  # Empty space
            Text("", font_size=20, color=WHITE),  # Empty space
        ).arrange(RIGHT, buff=0.5)
        
        # Row 2: Actual Negative
        row2 = VGroup(
            Text("", font_size=20, color=WHITE),  # Empty space
            Text("Negative", font_size=20, color=YELLOW, weight=BOLD),
            Text("", font_size=20, color=WHITE),  # Empty space
            Text("", font_size=20, color=WHITE),  # Empty space
        ).arrange(RIGHT, buff=0.5)
        
        # Values
        values = VGroup(
            VGroup(
                Text("", font_size=20, color=WHITE),  # Empty corner
                Text("Positive", font_size=20, color=YELLOW, weight=BOLD),
                Text("", font_size=20, color=WHITE),  # Empty space
                Text("Negative", font_size=20, color=YELLOW, weight=BOLD),
            ).arrange(RIGHT, buff=0.5),
            VGroup(
                Text("Positive", font_size=20, color=YELLOW, weight=BOLD),
                Text(str(tp), font_size=24, color=GREEN, weight=BOLD),  # TP
                Text("", font_size=20, color=WHITE),  # Empty space
                Text(str(fp), font_size=24, color=RED, weight=BOLD),   # FP
            ).arrange(RIGHT, buff=0.5),
            VGroup(
                Text("", font_size=20, color=WHITE),  # Empty space
                Text("", font_size=20, color=WHITE),  # Empty space
                Text("", font_size=20, color=WHITE),  # Empty space
                Text("", font_size=20, color=WHITE),  # Empty space
            ).arrange(RIGHT, buff=0.5),
            VGroup(
                Text("Negative", font_size=20, color=YELLOW, weight=BOLD),
                Text(str(fn), font_size=24, color=RED, weight=BOLD),   # FN
                Text("", font_size=20, color=WHITE),  # Empty space
                Text(str(tn), font_size=24, color=GREEN, weight=BOLD), # TN
            ).arrange(RIGHT, buff=0.5),
        ).arrange(DOWN, buff=0.3)
        
        # Create matrix with borders
        matrix_group = VGroup(header_row, values[0], values[1], values[3])
        matrix_group.arrange(DOWN, buff=0.3)
        
        # Add borders
        border = Rectangle(
            width=matrix_group.width + 0.5,
            height=matrix_group.height + 0.5,
            color=WHITE,
            stroke_width=2
        )
        border.move_to(matrix_group.get_center())
        
        # Labels for TP, FP, FN, TN
        labels = VGroup(
            Text("TP (True Positive)", font_size=16, color=GREEN),
            Text("FP (False Positive)", font_size=16, color=RED),
            Text("FN (False Negative)", font_size=16, color=RED),
            Text("TN (True Negative)", font_size=16, color=GREEN),
        ).arrange(DOWN, buff=0.2)
        labels.to_edge(RIGHT).shift(UP * 1)
        
        self.play(Write(cm_title))
        self.play(Create(border))
        self.play(FadeIn(matrix_group, shift=UP*0.3))
        self.play(FadeIn(labels, shift=LEFT*0.3))
        
        self.wait(2)
        
        # Store for later
        self.cm_title = cm_title
        self.matrix_group = matrix_group
        self.border = border
        self.labels = labels
        self.tp, self.fp, self.fn, self.tn = tp, fp, fn, tn

    def calculate_rates(self):
        # Fade out confusion matrix
        self.play(FadeOut(self.matrix_group), FadeOut(self.border), FadeOut(self.labels))
        
        # Rates title
        rates_title = Text("Calculate TPR and FPR", font_size=32, color=WHITE, weight=BOLD)
        rates_title.to_edge(UP)
        self.play(Transform(self.cm_title, rates_title))
        
        # Formulas
        formulas = VGroup(
            MathTex(r"\text{TPR} = \frac{\text{TP}}{\text{TP} + \text{FN}}", font_size=28, color=GREEN),
            MathTex(r"\text{FPR} = \frac{\text{FP}}{\text{FP} + \text{TN}}", font_size=28, color=RED),
        ).arrange(DOWN, buff=0.5)
        formulas.next_to(rates_title, DOWN, buff=0.5)
        
        self.play(Write(formulas))
        
        # Calculate values
        tpr = self.tp / (self.tp + self.fn)
        fpr = self.fp / (self.fp + self.tn)
        
        calculations = VGroup(
            MathTex(fr"\text{{TPR}} = \frac{{{self.tp}}}{{{self.tp} + {self.fn}}} = \frac{{{self.tp}}}{{{self.tp + self.fn}}} = {tpr:.3f}", font_size=24, color=GREEN),
            MathTex(fr"\text{{FPR}} = \frac{{{self.fp}}}{{{self.fp} + {self.tn}}} = \frac{{{self.fp}}}{{{self.fp + self.tn}}} = {fpr:.3f}", font_size=24, color=RED),
        ).arrange(DOWN, buff=0.4)
        calculations.next_to(formulas, DOWN, buff=0.5)
        
        self.play(Write(calculations))
        
        # Summary of points
        points_summary = VGroup(
            Text("ROC Curve Points:", font_size=20, color=YELLOW, weight=BOLD),
            Text(f"• (0, 0): Perfect negative prediction", font_size=18, color=WHITE),
            Text(f"• ({fpr:.3f}, {tpr:.3f}): Our model's performance", font_size=18, color=GREEN),
            Text(f"• (1, 1): Perfect positive prediction", font_size=18, color=WHITE),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        points_summary.to_edge(RIGHT).shift(UP * 1)
        
        self.play(FadeIn(points_summary, shift=LEFT*0.3))
        
        self.wait(2)
        
        # Store for later
        self.formulas = formulas
        self.calculations = calculations
        self.points_summary = points_summary
        self.tpr, self.fpr = tpr, fpr

    def show_roc_curve(self):
        # Fade out calculations
        self.play(FadeOut(self.formulas), FadeOut(self.calculations), FadeOut(self.points_summary))
        
        # ROC curve title
        roc_title = Text("ROC Curve", font_size=32, color=WHITE, weight=BOLD)
        roc_title.to_edge(UP)
        self.play(Transform(self.cm_title, roc_title))
        
        # Create coordinate system for ROC curve
        axes = Axes(
            x_range=[0, 1, 0.2],
            y_range=[0, 1, 0.2],
            x_length=6,
            y_length=6,
            axis_config={"color": WHITE, "stroke_width": 2},
            x_axis_config={"numbers_to_include": np.arange(0, 1.2, 0.2)},
            y_axis_config={"numbers_to_include": np.arange(0, 1.2, 0.2)},
        )
        
        # Add axis labels
        x_label = Text("False Positive Rate (FPR)", font_size=20, color=WHITE).next_to(axes.x_axis, DOWN)
        y_label = Text("True Positive Rate (TPR)", font_size=20, color=WHITE).next_to(axes.y_axis, LEFT).rotate(90*DEGREES)
        
        # Add diagonal line (random classifier)
        diagonal = Line(
            start=axes.coords_to_point(0, 0),
            end=axes.coords_to_point(1, 1),
            color=GRAY,
            stroke_width=2
        )
        
        # Add ROC curve points
        points = VGroup()
        
        # Point (0, 0)
        point1 = Dot(axes.coords_to_point(0, 0), color=BLUE, radius=0.08)
        label1 = Text("(0, 0)", font_size=16, color=BLUE).next_to(point1, DOWN, buff=0.1)
        points.add(point1, label1)
        
        # Point (FPR, TPR)
        point2 = Dot(axes.coords_to_point(self.fpr, self.tpr), color=GREEN, radius=0.08)
        label2 = Text(f"({self.fpr:.3f}, {self.tpr:.3f})", font_size=16, color=GREEN).next_to(point2, UP, buff=0.1)
        points.add(point2, label2)
        
        # Point (1, 1)
        point3 = Dot(axes.coords_to_point(1, 1), color=RED, radius=0.08)
        label3 = Text("(1, 1)", font_size=16, color=RED).next_to(point3, UP, buff=0.1)
        points.add(point3, label3)
        
        # Create ROC curve (simplified as straight lines)
        roc_line1 = Line(
            start=axes.coords_to_point(0, 0),
            end=axes.coords_to_point(self.fpr, self.tpr),
            color=GREEN,
            stroke_width=3
        )
        
        roc_line2 = Line(
            start=axes.coords_to_point(self.fpr, self.tpr),
            end=axes.coords_to_point(1, 1),
            color=GREEN,
            stroke_width=3
        )
        
        # Animate ROC curve creation
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(Create(diagonal))
        self.play(Create(point1), Write(label1))
        self.play(Create(point2), Write(label2))
        self.play(Create(point3), Write(label3))
        self.play(Create(roc_line1), Create(roc_line2))
        
        # Add legend
        legend = VGroup(
            Text("Random Classifier", font_size=16, color=GRAY),
            Text("Our Model", font_size=16, color=GREEN),
        ).arrange(DOWN, buff=0.2)
        legend.to_edge(RIGHT).shift(UP * 1)
        
        self.play(FadeIn(legend, shift=LEFT*0.3))
        
        self.wait(2)
        
        # Store for later
        self.axes = axes
        self.x_label = x_label
        self.y_label = y_label
        self.diagonal = diagonal
        self.points = points
        self.roc_line1 = roc_line1
        self.roc_line2 = roc_line2
        self.legend = legend

    def calculate_auc(self):
        # AUC calculation title
        auc_title = Text("Calculate AUC using Trapezoid Rule", font_size=28, color=WHITE, weight=BOLD)
        auc_title.to_edge(UP)
        self.play(Transform(self.cm_title, auc_title))
        
        # Highlight the area under the curve
        # Create polygon for AUC calculation
        auc_polygon = Polygon(
            self.axes.coords_to_point(0, 0),
            self.axes.coords_to_point(self.fpr, 0),
            self.axes.coords_to_point(self.fpr, self.tpr),
            self.axes.coords_to_point(1, 1),
            color=YELLOW,
            fill_opacity=0.3,
            stroke_width=2
        )
        
        self.play(FadeIn(auc_polygon))
        
        # Show trapezoid rule
        trapezoid_text = VGroup(
            Text("Trapezoid Rule:", font_size=20, color=YELLOW, weight=BOLD),
            Text("AUC = Area of trapezoids", font_size=18, color=WHITE),
            Text("= (1/2) × base × (height1 + height2)", font_size=18, color=WHITE),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        trapezoid_text.to_edge(RIGHT).shift(UP * 1)
        
        self.play(FadeIn(trapezoid_text, shift=LEFT*0.3))
        
        # Calculate AUC
        # Area = (1/2) * FPR * TPR + (1/2) * (1 - FPR) * (TPR + 1)
        area1 = 0.5 * self.fpr * self.tpr  # Triangle from (0,0) to (FPR, TPR)
        area2 = 0.5 * (1 - self.fpr) * (self.tpr + 1)  # Trapezoid from (FPR, TPR) to (1, 1)
        auc = area1 + area2
        
        # Show calculation
        calculation_text = VGroup(
            Text("AUC Calculation:", font_size=20, color=GREEN, weight=BOLD),
            MathTex(fr"A_1 = \frac{{1}}{{2}} \times {self.fpr:.3f} \times {self.tpr:.3f} = {area1:.3f}", font_size=16, color=WHITE),
            MathTex(fr"A_2 = \frac{{1}}{{2}} \times (1 - {self.fpr:.3f}) \times ({self.tpr:.3f} + 1) = {area2:.3f}", font_size=16, color=WHITE),
            MathTex(fr"AUC = A_1 + A_2 = {area1:.3f} + {area2:.3f} = {auc:.3f}", font_size=18, color=GREEN),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        calculation_text.next_to(trapezoid_text, DOWN, buff=0.5)
        
        self.play(FadeIn(calculation_text, shift=LEFT*0.3))
        
        # Interpretation
        interpretation = Text(
            f"AUC = {auc:.3f}\nGood performance (> 0.7)",
            font_size=20, color=GREEN, weight=BOLD
        )
        interpretation.next_to(calculation_text, DOWN, buff=0.5)
        
        self.play(Write(interpretation))
        
        self.wait(3)
        
        # Store for later
        self.auc_polygon = auc_polygon
        self.trapezoid_text = trapezoid_text
        self.calculation_text = calculation_text
        self.interpretation = interpretation
        self.auc = auc

    def show_summary(self):
        # Fade out ROC curve elements
        self.play(
            FadeOut(self.axes), FadeOut(self.x_label), FadeOut(self.y_label),
            FadeOut(self.diagonal), FadeOut(self.points), FadeOut(self.roc_line1),
            FadeOut(self.roc_line2), FadeOut(self.legend), FadeOut(self.auc_polygon),
            FadeOut(self.trapezoid_text), FadeOut(self.calculation_text), FadeOut(self.interpretation)
        )
        
        # Summary title
        summary_title = Text("Summary: AUC from Confusion Matrix", font_size=32, color=WHITE, weight=BOLD)
        summary_title.to_edge(UP)
        self.play(Transform(self.cm_title, summary_title))
        
        # Summary steps
        summary_steps = VGroup(
            Text("1. Extract TP, FP, FN, TN from confusion matrix", color=WHITE, font_size=24),
            Text("2. Calculate TPR = TP / (TP + FN)", color=GREEN, font_size=24),
            Text("3. Calculate FPR = FP / (FP + TN)", color=RED, font_size=24),
            Text("4. Plot points (0,0), (FPR, TPR), (1,1) on ROC curve", color=BLUE, font_size=24),
            Text("5. Use trapezoid rule to calculate AUC", color=YELLOW, font_size=24),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        summary_steps.next_to(summary_title, DOWN, buff=0.5)
        
        self.play(FadeIn(summary_steps, shift=LEFT*0.3))
        
        # Final AUC value
        final_auc = Text(
            f"Final AUC = {self.auc:.3f}",
            font_size=28, color=GREEN, weight=BOLD
        )
        final_auc.next_to(summary_steps, DOWN, buff=0.5)
        
        self.play(Write(final_auc))
        
        self.wait(3)
        
        # Final message
        final_message = Text(
            "AUC measures the model's ability\nto distinguish between classes",
            font_size=24, color=YELLOW, weight=BOLD
        )
        final_message.move_to(ORIGIN)
        
        self.play(
            FadeOut(self.cm_title),
            FadeOut(summary_steps),
            FadeOut(final_auc)
        )
        self.play(Write(final_message))
        self.wait(3)
