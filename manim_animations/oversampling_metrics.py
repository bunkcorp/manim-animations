from manim import *
import numpy as np
rng = np.random.default_rng(2)

class OversamplingMetricsScene(Scene):
    def construct(self):
        title = Text("Oversampling • Metrics & Proper Usage", weight=BOLD)
        subtitle = Text("Precision • Recall • F1 • PR-AUC • No Leakage", font_size=28)
        subtitle.next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(title, shift=UP*0.5), FadeIn(subtitle, shift=UP*0.5))
        self.wait(0.6)

        # ==== 1) Imbalanced dataset (left) vs After oversampling (right) ====
        left_title  = Text("Before (Imbalanced)", font_size=26)
        right_title = Text("After (Oversampled Train)", font_size=26)
        left_axes   = self.make_axes().to_edge(LEFT, buff=0.7).shift(DOWN*0.2)
        right_axes  = self.make_axes().to_edge(RIGHT, buff=0.7).shift(DOWN*0.2)
        left_title.next_to(left_axes, UP, buff=0.2)
        right_title.next_to(right_axes, UP, buff=0.2)

        self.play(FadeIn(left_axes), FadeIn(right_axes))
        self.play(FadeIn(left_title), FadeIn(right_title))

        # Majority/minority points
        maj = rng.normal(loc=[0,0], scale=[1.0,0.7], size=(220,2))
        mino= rng.normal(loc=[2.2,1.6], scale=[0.5,0.4], size=(20,2))

        all_pts = np.vstack([maj, mino])
        m, s = all_pts.mean(0), all_pts.std(0)
        maj_n  = (maj - m)/s
        mino_n = (mino - m)/s

        # Scatter before
        left_maj = self.scatter_points(left_axes, maj_n, color=BLUE, radius=0.03)
        left_min = self.scatter_points(left_axes, mino_n, color=RED, radius=0.035)
        self.play(FadeIn(left_maj, lag_ratio=0.01, run_time=0.8))
        self.play(FadeIn(left_min, lag_ratio=0.05, run_time=0.6))

        # Simple oversampling with jitter (train only conceptually)
        reps = int(np.ceil(200/len(mino_n)))
        mino_dup = np.vstack([mino_n for _ in range(reps)])[:200]
        jitter = rng.normal(0, 0.06, size=mino_dup.shape)
        mino_syn = mino_dup + jitter

        right_maj = self.scatter_points(right_axes, maj_n, color=BLUE, radius=0.03, alpha=0.9)
        right_min = self.scatter_points(right_axes, mino_syn, color=RED, radius=0.035, alpha=0.9)
        self.play(FadeIn(right_maj, lag_ratio=0.01, run_time=0.6))
        for chunk in np.array_split(np.arange(len(mino_syn)), 5):
            self.play(FadeIn(VGroup(*[right_min[i] for i in chunk])), run_time=0.4)

        # Decorative decision boundaries (intuition only)
        self.play(Create(self.curvy_boundary(left_axes, shift=0.0, color=GREY_B)))
        self.play(Create(self.curvy_boundary(right_axes, shift=0.2, color=GREY_B)))

        self.wait(0.4)

        # ==== 2) Metrics bars: Before vs After ====
        # We'll animate hypothetical metrics to illustrate improvement in minority coverage.
        # Before (imbalanced): high precision ~0.80, low recall ~0.35, F1 ~0.49, PR-AUC ~0.41
        # After (oversampled train, evaluated properly): precision ~0.72, recall ~0.70, F1 ~0.71, PR-AUC ~0.62
        metrics_before = {"Precision":0.80, "Recall":0.35, "F1":0.49, "PR-AUC":0.41}
        metrics_after  = {"Precision":0.72, "Recall":0.70, "F1":0.71, "PR-AUC":0.62}

        bars_title = Text("Minority-focused Metrics", font_size=28)
        bars_title.to_edge(UP, buff=0.2)
        self.play(FadeIn(bars_title))

        bars_before = self.metric_bars(metrics_before, label="Before", color=BLUE)
        bars_after  = self.metric_bars(metrics_after,  label="After",  color=GREEN)

        group_bars = VGroup(bars_before["group"], bars_after["group"]).arrange(RIGHT, buff=0.8).scale(0.9)
        group_bars.next_to(bars_title, DOWN, buff=0.2)
        self.play(FadeIn(group_bars))

        # Animate the fill to target heights
        self.animate_bar_fill(bars_before, metrics_before)
        self.animate_bar_fill(bars_after,  metrics_after)
        self.wait(0.6)

        # Highlight recall and PR-AUC emphasis
        callout = VGroup(
            RoundedRectangle(width=6.8, height=1.2, corner_radius=0.15).set_stroke(YELLOW).set_fill(YELLOW, 0.12),
            Tex(r"Evaluate with Recall / F1 / PR-AUC (not Accuracy only)", color=YELLOW).scale(0.9)
        )
        callout[1].move_to(callout[0].get_center())
        callout.next_to(group_bars, DOWN, buff=0.3)
        self.play(FadeIn(callout, shift=UP*0.2))
        self.wait(0.6)

        # ==== 3) Train/Test split: Oversample only in Train ====
        split_title = Text("Data Split: Avoid Leakage", font_size=28)
        split = self.train_test_split_panel()
        split["group"].next_to(callout, DOWN, buff=0.5)
        split_title.next_to(split["group"], UP, buff=0.25).align_to(split["group"], LEFT)

        self.play(FadeIn(split_title), FadeIn(split["group"]))
        self.wait(0.3)

        # Emphasize: oversample only train
        train_box, test_box, train_tag, test_tag, oversample_tag = split["boxes"]
        self.play(Indicate(train_box, color=GREEN, scale_factor=1.03))
        self.play(Flash(oversample_tag, color=RED))
        self.wait(0.2)
        self.play(Indicate(test_box, color=RED, scale_factor=1.03))
        leak = Tex(r"Never oversample Test/Validation", color=RED).scale(0.9)
        leak.next_to(test_box, DOWN, buff=0.15)
        self.play(Write(leak))
        self.wait(0.6)

        # ==== 4) K-fold CV visualization ====
        cv_title = Text("K-fold CV: Oversample Inside Each Train Fold", font_size=28)
        cv = self.kfold_panel(k=5)
        cv["group"].next_to(split["group"], DOWN, buff=0.6)
        cv_title.next_to(cv["group"], UP, buff=0.25).align_to(cv["group"], LEFT)
        self.play(FadeIn(cv_title), FadeIn(cv["group"]))
        self.wait(0.3)

        # Animate through folds (highlight train vs val each step)
        for i in range(5):
            trains, val = cv["folds"]
            # reset opacities
            for box in trains:
                box.set_opacity(0.12)
            val.set_opacity(0.12)

            # mark train region
            for j, box in enumerate(trains):
                if j != i:
                    box.set_opacity(0.45).set_color(GREEN)
            # mark validation region
            trains[i].set_opacity(0.12)
            val.set_opacity(0.85).set_color(BLUE)

            # place "oversample" tag over the combined green areas (approximate)
            self.play(
                *[box.animate.set_stroke(GREEN, 2) for j, box in enumerate(trains) if j != i],
                val.animate.set_stroke(BLUE, 2),
                run_time=0.6
            )
            tag = self.small_tag("oversample", color=RED).next_to(trains[0], UP, buff=0.1).shift(RIGHT*1.8)
            self.play(FadeIn(tag), run_time=0.2)
            self.play(FadeOut(tag), run_time=0.2)

        self.wait(0.5)

        # ==== 5) Takeaway ====
        takeaway = VGroup(
            RoundedRectangle(width=13.0, height=1.7, corner_radius=0.2).set_stroke(WHITE, 2).set_fill(DARK_GREY, 0.08),
            Tex(
                r"\textbf{Takeaway:} Oversample only in training folds to avoid leakage. ",
                r"Track Recall/F1/PR-AUC for the minority class; decision thresholds matter.",
                tex_environment="flushleft"
            ).scale(0.9)
        )
        takeaway[1].move_to(takeaway[0].get_center())
        takeaway.to_edge(DOWN, buff=0.3)
        self.play(Create(takeaway[0]), Write(takeaway[1]))
        self.wait(1.0)

    # ---------- helpers ----------
    def make_axes(self):
        return Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=5.0,
            y_length=4.3,
            tips=False,
            axis_config={"stroke_color": GREY_B, "stroke_width": 2},
        )

    def scatter_points(self, axes, pts, color=WHITE, radius=0.04, alpha=1.0):
        dots = VGroup()
        for x, y in pts:
            d = Dot(axes.coords_to_point(x, y), radius=radius, color=color)
            d.set_opacity(alpha)
            dots.add(d)
        return dots

    def curvy_boundary(self, axes, shift=0.0, color=GREY_B):
        xs = np.linspace(-2.5, 2.5, 80)
        ys = 0.6*np.sin(1.2*xs) + shift
        points = [axes.coords_to_point(x, y) for x, y in zip(xs, ys)]
        curve = VMobject(color=color, stroke_width=3)
        curve.set_points_smoothly(points)
        return curve

    def metric_bars(self, metric_dict, label="Before", color=WHITE):
        # returns a VGroup with: title, frame, bars (dict of name->(rect, fill_rect, value_label))
        names = list(metric_dict.keys())
        max_h = 2.5
        width = 0.5
        gap = 0.5

        group = VGroup()
        caption = Text(label, font_size=26, weight=BOLD).set_color(color)
        bars = {}
        x0 = 0
        for i, name in enumerate(names):
            x = x0 + i*(width+gap)
            frame = Rectangle(width=width, height=max_h, stroke_color=GREY_B)
            frame.move_to(np.array([x, 0, 0]))
            fill = Rectangle(width=width*0.9, height=0.001, fill_color=color, fill_opacity=0.8, stroke_width=0)
            fill.move_to(frame.get_bottom() + np.array([0, fill.height/2, 0]))
            label_name = Text(name, font_size=22).next_to(frame, DOWN, buff=0.15)
            val_label = DecimalNumber(0.0, num_decimal_places=2, include_sign=False).scale(0.6)
            val_label.next_to(frame, UP, buff=0.05)
            bars[name] = (frame, fill, val_label, label_name)
            group.add(frame, fill, val_label, label_name)
        caption.next_to(VGroup(*[b[0] for b in bars.values()]), UP, buff=0.25).align_to(group, LEFT)
        group.add(caption)
        return {"group":group, "bars":bars}

    def animate_bar_fill(self, bars_obj, target_values):
        group = bars_obj["group"]
        bars = bars_obj["bars"]
        # Position the group nicely
        self.play(FadeIn(group))
        max_h = 2.5
        for name, val in target_values.items():
            frame, fill, val_label, _ = bars[name]
            target_h = max_h * float(val)
            # Animate height and value label
            self.play(
                fill.animate.set(height=target_h).move_to(
                    frame.get_bottom() + np.array([0, target_h/2, 0])
                ),
                val_label.animate.set_value(val),
                run_time=0.5
            )

    def small_tag(self, text, color=WHITE):
        tag = VGroup(
            RoundedRectangle(width=1.6, height=0.45, corner_radius=0.12).set_stroke(color).set_fill(color, 0.15),
            Text(text, font_size=18, weight=BOLD).set_color(color)
        )
        tag[1].move_to(tag[0].get_center())
        return tag

    def train_test_split_panel(self):
        # A long bar split into Train and Test; an "oversample" tag on Train only
        base = RoundedRectangle(width=10.0, height=1.1, corner_radius=0.1).set_stroke(WHITE,2).set_fill(WHITE,0.06)
        train = Rectangle(width=6.6, height=0.9).set_fill(GREEN, 0.12).set_stroke(GREEN,2)
        test  = Rectangle(width=3.0, height=0.9).set_fill(BLUE, 0.12).set_stroke(BLUE,2)
        train.move_to(base.get_left() + np.array([train.width/2 + 0.2, 0, 0]))
        test.move_to(base.get_right() - np.array([test.width/2 + 0.2, 0, 0]))
        train_tag = Text("Train", font_size=24, weight=BOLD).next_to(train, UP, buff=0.1)
        test_tag  = Text("Test",  font_size=24, weight=BOLD).next_to(test,  UP, buff=0.1)
        oversample_tag = self.small_tag("oversample", color=RED).next_to(train, DOWN, buff=0.1)
        group = VGroup(base, train, test, train_tag, test_tag, oversample_tag)
        return {"group": group, "boxes": (train, test, train_tag, test_tag, oversample_tag)}

    def kfold_panel(self, k=5):
        # One long bar divided into k equal boxes; green = train (oversample), blue = validation
        total_w = 10.0
        h = 0.9
        base = RoundedRectangle(width=total_w+0.4, height=1.2, corner_radius=0.1).set_stroke(WHITE,2).set_fill(WHITE,0.06)
        boxes = []
        w = total_w / k
        for i in range(k):
            r = Rectangle(width=w-0.1, height=h).set_stroke(WHITE, 1).set_fill(WHITE, 0.12)
            boxes.append(r)
        strip = VGroup(*boxes).arrange(RIGHT, buff=0.08)
        strip.move_to(base.get_center())
        # create "train" (all except one) and "validation" (one) overlays
        trains = [b.copy().set_fill(GREEN,0.12).set_stroke(GREEN,1) for b in boxes]
        val = boxes[0].copy().set_fill(BLUE,0.12).set_stroke(BLUE,1)
        cv_group = VGroup(base, strip, *trains, val)
        return {"group": cv_group, "folds": (trains, val)}
