from manim import *
import numpy as np

# Render:
# manim -pqh choose_M_pca.py ChooseMPCA

class ChooseMPCA(Scene):
    def construct(self):
        title = Text("Choosing the Number of Principal Components (M)", weight=BOLD)
        subtitle = Text("Scree/Elbow • Cumulative PVE • Cross-Validation", font_size=28)
        subtitle.next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(title, shift=UP*0.5), FadeIn(subtitle, shift=UP*0.5))
        self.wait(0.5)

        # --- Trade-off panel ---
        trade_title = Text("Trade-off as M increases", font_size=30)
        bullets = VGroup(
            Tex(r"As $M \uparrow$: Cumulative PVE $\uparrow$"),
            Tex(r"As $M \uparrow$: Dimensionality $\uparrow$"),
            Tex(r"If supervised: Model complexity $\uparrow$"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).scale(0.95)
        trade = VGroup(trade_title, bullets).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        trade.to_edge(LEFT, buff=0.6).shift(DOWN*0.3)
        self.play(FadeIn(trade, shift=RIGHT))
        self.wait(0.4)

        # --- Scree plot (eigenvalues) + cumulative PVE ---
        right_group = self.scree_and_cumplot(k=12)   # returns dict with axes, bars, cumline, elbow, etc.
        right_group["group"].to_edge(RIGHT, buff=0.6).shift(DOWN*0.1)

        self.play(Create(right_group["axes"]))
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in right_group["bars"]], lag_ratio=0.12, run_time=1.2))
        self.play(Create(right_group["cum_curve"]), *[FadeIn(d) for d in right_group["cum_dots"]], run_time=0.8)
        self.wait(0.3)

        # Elbow marker and M*
        self.play(Create(right_group["elbow_vline"]), FadeIn(right_group["elbow_dot"]), FadeIn(right_group["elbow_label"]))
        self.wait(0.4)

        # --- Guidance panel for scree choice ---
        guide = VGroup(
            RoundedRectangle(corner_radius=0.15, width=6.9, height=1.2).set_stroke(YELLOW).set_fill(YELLOW, 0.10),
            Tex(r"Scree: choose $M^*$ near the elbow where added PCs give little extra variance.", color=YELLOW).scale(0.9)
        )
        guide[1].move_to(guide[0].get_center())
        guide.next_to(right_group["group"], DOWN, buff=0.3)
        self.play(FadeIn(guide, shift=UP*0.2))
        self.wait(0.5)

        # --- Cross-validation panel (if supervised) ---
        cv_title = Text("If supervised: tune M via Cross-Validation", font_size=30)
        cv_title.to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(trade_title.copy(), cv_title))
        cv_plot = self.cv_curve_plot(M_max=12)
        cv_plot["group"].next_to(guide, DOWN, buff=0.5)
        self.play(Create(cv_plot["axes"]))
        self.play(Create(cv_plot["curve"]), *[FadeIn(d) for d in cv_plot["dots"]])
        self.play(Create(cv_plot["best_vline"]), FadeIn(cv_plot["best_dot"]), FadeIn(cv_plot["best_label"]))
        self.wait(0.4)

        # --- Takeaway card ---
        takeaway = VGroup(
            RoundedRectangle(width=13.0, height=1.7, corner_radius=0.2).set_stroke(WHITE,2).set_fill(DARK_GREY,0.08),
            Tex(
                r"\textbf{Takeaway:} Unsupervised $\Rightarrow$ elbow (or target PVE, e.g., $\geq 90\%$). ",
                r"Supervised $\Rightarrow$ pick $M$ that maximizes CV score. Sanity-check with domain needs.",
                tex_environment="flushleft"
            ).scale(0.9)
        )
        takeaway[1].move_to(takeaway[0].get_center())
        takeaway.to_edge(DOWN, buff=0.25)
        self.play(Create(takeaway[0]), Write(takeaway[1]))
        self.wait(1.0)

    # ---------- helpers ----------
    def scree_and_cumplot(self, k=12):
        """
        Build a scree plot with k eigenvalues (descending) and cumulative PVE curve.
        Includes a simple 'elbow' heuristic: first index where marginal gain < threshold.
        """
        # Fake eigenvalues that decay (typical PCA spectrum shape)
        lam = np.array([3.8, 2.5, 1.9, 1.4, 1.0, 0.75, 0.55, 0.42, 0.31, 0.24, 0.18, 0.14])[:k]
        pv  = lam / lam.sum()
        cum = pv.cumsum()

        # axes
        axes = Axes(
            x_range=[0, k+1, 1],
            y_range=[0, 1.05, 0.2],
            x_length=6.4,
            y_length=3.8,
            tips=False,
            axis_config={"stroke_color": GREY_B, "stroke_width": 2},
            x_axis_config={"numbers_to_include": np.arange(1, k+1)},
        )
        x_label = Text("Principal Component index", font_size=22).next_to(axes, DOWN, buff=0.25)
        y_label = Text("PVE / Cum. PVE", font_size=22).rotate(PI/2).next_to(axes, LEFT, buff=0.25)
        group = VGroup(axes, x_label, y_label)

        # bars = PVE (scree)
        bars = []
        for i, p in enumerate(pv, start=1):
            h = p * axes.y_axis.get_length()
            bar = Rectangle(width=0.35, height=p, stroke_width=0, fill_color=BLUE, fill_opacity=0.8)
            bar.move_to(axes.c2p(i, p/2))
            bars.append(bar)

        # cumulative curve
        cum_dots = []
        cum_points = [axes.c2p(i, c) for i, c in enumerate(cum, start=1)]
        cum_curve = VMobject(color=GREEN, stroke_width=3)
        cum_curve.set_points_as_corners([axes.c2p(1, cum[0]), *cum_points])

        for i, c in enumerate(cum, start=1):
            dot = Dot(axes.c2p(i, c), radius=0.05, color=GREEN)
            cum_dots.append(dot)

        # elbow heuristic: first i where marginal gain < 0.03 (3%) or cum>=0.9
        diffs = np.diff(cum, prepend=0.0)
        elbow_idx = int(np.argmax((diffs < 0.03) | (cum >= 0.90))) + 0  # +0 for clarity
        elbow_idx = max(2, elbow_idx) if elbow_idx > 0 else 3  # keep elbow >= 2

        elbow_vline = DashedLine(
            start=axes.c2p(elbow_idx, 0),
            end=axes.c2p(elbow_idx, 1.02),
            dash_length=0.07,
            color=YELLOW
        )
        elbow_dot = Dot(axes.c2p(elbow_idx, cum[elbow_idx-1]), color=YELLOW, radius=0.06)
        elbow_label = Tex(r"$M^*=\ {}$".format(elbow_idx), color=YELLOW).scale(0.9)
        elbow_label.next_to(elbow_dot, UP, buff=0.15)

        return {
            "group": group, "axes": VGroup(axes, x_label, y_label),
            "bars": bars, "cum_curve": cum_curve, "cum_dots": cum_dots,
            "elbow_vline": elbow_vline, "elbow_dot": elbow_dot, "elbow_label": elbow_label
        }

    def cv_curve_plot(self, M_max=12):
        """
        Simple synthetic CV-mean score vs. M curve with a single-peaked shape.
        """
        Ms = np.arange(1, M_max+1)
        # Build a smooth "best at M≈6–7" curve (just illustrative)
        cv_mean = 0.58 + 0.18*np.exp(-0.5*((Ms-6.7)/2.2)**2) - 0.02*(Ms/12.0)

        axes = Axes(
            x_range=[0, M_max+1, 1],
            y_range=[0.5, 0.9, 0.1],
            x_length=6.4,
            y_length=3.0,
            tips=False,
            axis_config={"stroke_color": GREY_B, "stroke_width": 2},
            x_axis_config={"numbers_to_include": Ms},
        )
        x_label = Text("M (number of PCs kept)", font_size=22).next_to(axes, DOWN, buff=0.25)
        y_label = Text("CV score (e.g., accuracy/AUC)", font_size=22).rotate(PI/2).next_to(axes, LEFT, buff=0.25)
        group = VGroup(axes, x_label, y_label)

        points = [axes.c2p(m, s) for m, s in zip(Ms, cv_mean)]
        curve = VMobject(color=ORANGE, stroke_width=3).set_points_smoothly(points)
        dots = [Dot(p, radius=0.04, color=ORANGE) for p in points]

        best_idx = int(np.argmax(cv_mean))
        best_M = Ms[best_idx]
        best_vline = DashedLine(
            start=axes.c2p(best_M, axes.y_range[0]),
            end=axes.c2p(best_M, axes.y_range[1]),
            dash_length=0.07,
            color=ORANGE
        )
        best_dot = Dot(points[best_idx], radius=0.06, color=ORANGE)
        best_label = Tex(r"Best $M={}$".format(best_M), color=ORANGE).scale(0.9).next_to(best_dot, UP, buff=0.15)

        return {"group": group, "axes": group, "curve": curve, "dots": dots,
                "best_vline": best_vline, "best_dot": best_dot, "best_label": best_label}
