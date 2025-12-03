from manim import *
import numpy as np

# Render:
# manim -pqh accuracy_limitations.py AccuracyLimitations

class AccuracyLimitations(Scene):
    def construct(self):
        title = Text("Accuracy: What it Measures & Its Limitations", weight=BOLD)
        subtitle = Text("Good for balance • Misleading with imbalance", font_size=28)
        subtitle.next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(title, shift=UP*0.5), FadeIn(subtitle, shift=UP*0.5))
        self.wait(0.5)

        # --- Formula & definition ---
        formula = Tex(r"Accuracy = \dfrac{TP + TN}{TP + TN + FP + FN}", tex_environment="align").scale(1.0)
        defn = Text("Proportion of correctly predicted observations.", font_size=20)
        defn.next_to(formula, DOWN, buff=0.25)
        self.play(Write(formula))
        self.play(FadeIn(defn))
        self.wait(0.5)

        # --- Confusion Matrix (generic) ---
        cm_box = self.draw_confusion_matrix(label="Confusion Matrix", pos=UP*0.2)
        self.play(FadeIn(cm_box["group"]))
        self.wait(0.2)

        # Fill with variables TP, FP, FN, TN
        self.show_symbols_in_cm(cm_box)

        # --- Example 1: Balanced dataset ---
        left_title = Text("Balanced Data", font_size=28).to_edge(LEFT).shift(DOWN*0.8)
        right_title = Text("Imbalanced Data", font_size=28).to_edge(RIGHT).shift(DOWN*0.8)
        self.play(FadeIn(left_title), FadeIn(right_title))

        # Build two CM panels
        left_cm  = self.draw_confusion_matrix(pos=LEFT*3.2 + DOWN*1.2, label=None)
        right_cm = self.draw_confusion_matrix(pos=RIGHT*3.2 + DOWN*1.2, label=None)
        self.play(FadeIn(left_cm["group"]), FadeIn(right_cm["group"]))

        # Fill numbers
        # Balanced: 100 positives, 100 negatives; model: TP=80, FN=20, TN=85, FP=15
        bal_counts = dict(TP=80, FN=20, FP=15, TN=85)
        self.fill_cm_with_counts(left_cm, bal_counts, color=GREEN)
        bal_acc = (bal_counts["TP"] + bal_counts["TN"]) / sum(bal_counts.values())
        bal_text = Tex(f"Accuracy = ({bal_counts['TP']} + {bal_counts['TN']}) / 200 = {bal_acc:.2f}").scale(0.9)
        bal_text.next_to(left_cm["group"], DOWN, buff=0.25)
        self.play(Write(bal_text))

        # Imbalanced: 1000 negatives, 50 positives; naive model predicts all negative:
        # TP=0, FN=50, TN=1000, FP=0 -> Accuracy = 1000/1050 ≈ 0.95 (but Recall for positive = 0)
        imb_counts = dict(TP=0, FN=50, FP=0, TN=1000)
        self.fill_cm_with_counts(right_cm, imb_counts, color=YELLOW)
        imb_acc = (imb_counts["TP"] + imb_counts["TN"]) / sum(imb_counts.values())
        imb_text = Tex(f"Accuracy = ({imb_counts['TP']} + {imb_counts['TN']}) / 1050 = {imb_acc:.2f}").scale(0.9)
        imb_text.next_to(right_cm["group"], DOWN, buff=0.25)
        self.play(Write(imb_text))
        self.wait(0.6)

        # --- Emphasize limitation ---
        warn = VGroup(
            RoundedRectangle(width=11.5, height=1.4, corner_radius=0.15).set_stroke(ORANGE).set_fill(ORANGE, 0.12),
            Tex(r"Limitation: In imbalanced data, Accuracy can be high even if the minority class is ignored.", color=ORANGE).scale(0.9)
        )
        warn[1].move_to(warn[0].get_center())
        warn.next_to(formula, DOWN, buff=0.9)
        self.play(FadeIn(warn, shift=UP*0.2))
        self.wait(0.4)

        # Highlight minority recall = 0 on right CM
        rec0 = Tex(r"Minority Recall $= \dfrac{TP}{TP+FN} = 0/50 = 0$", color=RED).scale(0.9)
        rec0.next_to(right_cm["group"], UP, buff=0.2)
        self.play(Write(rec0))
        self.play(Indicate(right_cm["cells"]["FN"], color=RED), Indicate(right_cm["cells"]["TP"], color=RED))
        self.wait(0.4)

        # --- Alternatives panel ---
        alts = self.bullet_panel(
            "Use additional metrics",
            [
                "Recall / Sensitivity (minority coverage)",
                "Precision & F1 (balance precision/recall)",
                "PR-AUC (robust under imbalance)"
            ],
            color=BLUE
        )
        alts.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(alts, shift=UP*0.2))
        self.wait(0.6)

        # --- Takeaway card ---
        takeaway = VGroup(
            RoundedRectangle(width=13.0, height=1.6, corner_radius=0.2).set_stroke(WHITE,2).set_fill(DARK_GREY,0.08),
            Tex(
                r"\textbf{Takeaway:} Accuracy = share of correct predictions. ",
                r"Always pair it with class-sensitive metrics on imbalanced problems.",
                tex_environment="flushleft"
            ).scale(0.9)
        )
        takeaway[1].move_to(takeaway[0].get_center())
        takeaway.next_to(alts, UP, buff=0.35)
        self.play(Create(takeaway[0]), Write(takeaway[1]))
        self.wait(1.0)

    # ---------- helpers ----------
    def draw_confusion_matrix(self, pos=ORIGIN, label=None):
        # Grid 2x2 with labels
        size = 2.6
        grid = VGroup(*[
            Square(side_length=size/2).set_stroke(WHITE, 2) for _ in range(4)
        ]).arrange_in_grid(rows=2, cols=2, buff=0)
        grid.move_to(pos)

        # Axis labels
        y_true = Text("Actual", font_size=22).rotate(PI/2)
        y_true.next_to(grid, LEFT, buff=0.25)
        y_pred = Text("Predicted", font_size=22)
        y_pred.next_to(grid, UP, buff=0.25)

        tn, fp, fn, tp = grid[0], grid[1], grid[2], grid[3]  # due to row-major order
        # Put corner captions
        cap_TN = Text("TN", font_size=22).move_to(tn.get_center())
        cap_FP = Text("FP", font_size=22).move_to(fp.get_center())
        cap_FN = Text("FN", font_size=22).move_to(fn.get_center())
        cap_TP = Text("TP", font_size=22).move_to(tp.get_center())

        group = VGroup(grid, y_true, y_pred, cap_TN, cap_FP, cap_FN, cap_TP)
        if label:
            head = Text(label, font_size=26, weight=BOLD).next_to(group, UP, buff=0.2)
            group = VGroup(head, group)

        return {"group": group, "grid": grid,
                "cells": {"TN": tn, "FP": fp, "FN": fn, "TP": tp}}

    def show_symbols_in_cm(self, cm):
        # briefly flash TP/TN contributions to the numerator of accuracy
        brace = Brace(VGroup(cm["grid"][0], cm["grid"][3]), direction=RIGHT, color=YELLOW)
        num = Tex(r"Numerator: $TP + TN$", color=YELLOW).scale(0.9).next_to(brace, RIGHT, buff=0.2)
        self.play(Create(brace), Write(num))
        self.wait(0.3)
        self.play(Indicate(cm["cells"]["TP"], color=YELLOW), Indicate(cm["cells"]["TN"], color=YELLOW))
        self.wait(0.2)
        self.play(FadeOut(brace), FadeOut(num))

    def fill_cm_with_counts(self, cm, counts, color=WHITE):
        # Place counts in each cell
        labels = {}
        for k, cell in cm["cells"].items():
            val = counts[k]
            t = Text(str(val), font_size=26, weight=BOLD).set_color(color)
            t.move_to(cell.get_center()).shift(DOWN*0.2)
            self.play(FadeIn(t, scale=0.9), run_time=0.15)
            labels[k] = t
        return labels

    def bullet_panel(self, title, items, color=WHITE):
        header = Text(title, weight=BOLD, font_size=28).set_color(color)
        bullets = VGroup(*[Text("• " + it, font_size=18) for it in items])\
            .arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        panel = VGroup(header, bullets).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        return panel
