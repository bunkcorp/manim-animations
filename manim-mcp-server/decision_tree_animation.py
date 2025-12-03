from manim import *
import numpy as np
import math
from collections import Counter

# ================= CONFIG =================
CLASS_COLORS = {0: RED, 1: GREEN}
TEXT_COLOR = WHITE
SPLIT_COLOR = YELLOW
LEAF_COLOR = GREEN
NODE_COLOR = TEAL

SHOW_CHIPS = True
CHIP_SIZE = 0.18
CHIPS_PER_ROW = 10
SPEED = 1.0

MAX_DEPTH = 3
MIN_SAMPLES_SPLIT = 2


# ============= DecisionTree with tracing =============
class DecisionTree:
    def __init__(self, max_depth=None, min_samples_split=2, event_callback=None):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.root = None
        self.event_callback = event_callback or (lambda ev: None)

    def emit(self, typ, **payload):
        self.event_callback({"type": typ, "payload": payload})

    def calculate_entropy(self, y):
        self.emit("entropy_start", y=list(y))
        if len(y) == 0:
            return 0
        counts = Counter(y)
        total = len(y)
        ent = 0
        for count in counts.values():
            p = count / total
            if p > 0:
                ent -= p * math.log2(p)
        self.emit("entropy_end", value=ent)
        return ent

    def calculate_information_gain(self, X_column, y, threshold):
        parent_entropy = self.calculate_entropy(y)
        left_mask = X_column <= threshold
        right_mask = ~left_mask
        if sum(left_mask) == 0 or sum(right_mask) == 0:
            return 0
        n = len(y)
        n_left, n_right = sum(left_mask), sum(right_mask)
        left_entropy = self.calculate_entropy(y[left_mask])
        right_entropy = self.calculate_entropy(y[right_mask])
        weighted = (n_left/n)*left_entropy + (n_right/n)*right_entropy
        ig = parent_entropy - weighted
        self.emit("ig_eval", threshold=threshold,
                  ig=ig, n_left=n_left, n_right=n_right,
                  left_entropy=left_entropy, right_entropy=right_entropy,
                  parent_entropy=parent_entropy)
        return ig

    def find_best_split(self, X, y):
        best_gain, best_feature, best_thr = 0, None, None
        n_features = X.shape[1]
        for f in range(n_features):
            self.emit("feature_eval_start", feature=f)
            thresholds = np.unique(X[:, f])
            for thr in thresholds:
                gain = self.calculate_information_gain(X[:, f], y, thr)
                if gain > best_gain:
                    best_gain, best_feature, best_thr = gain, f, thr
            self.emit("feature_eval_end", feature=f, best_gain=best_gain,
                      best_feature=best_feature, best_thr=best_thr)
        return best_feature, best_thr, best_gain

    def build_tree(self, X, y, depth=0):
        self.emit("node_start", depth=depth, n_samples=len(y), labels=list(y))
        if len(np.unique(y)) == 1:
            c = y[0]
            self.emit("node_leaf", leaf_class=c)
            return {"class": c}
        if (self.max_depth and depth >= self.max_depth) or len(y) < self.min_samples_split:
            c = Counter(y).most_common(1)[0][0]
            self.emit("node_leaf", leaf_class=c)
            return {"class": c}
        f, thr, gain = self.find_best_split(X, y)
        if gain == 0:
            c = Counter(y).most_common(1)[0][0]
            self.emit("node_leaf", leaf_class=c)
            return {"class": c}
        self.emit("best_split", feature=f, threshold=thr, gain=gain)
        left_mask = X[:, f] <= thr
        right_mask = ~left_mask
        left = self.build_tree(X[left_mask], y[left_mask], depth+1)
        right = self.build_tree(X[right_mask], y[right_mask], depth+1)
        return {"feature": f, "threshold": thr, "gain": gain,
                "left": left, "right": right}

    def fit(self, X, y):
        self.root = self.build_tree(X, y)
        return self


# ============= Visual Helpers =============
class SampleChips(VGroup):
    def __init__(self, labels, **kwargs):
        super().__init__(**kwargs)
        chips = []
        for v in labels:
            sq = Square(CHIP_SIZE).set_stroke(WHITE, 0.6)
            sq.set_fill(CLASS_COLORS.get(v, GRAY), opacity=0.9)
            chips.append(sq)
        self.chips = VGroup(*chips)
        if chips:
            rows = math.ceil(len(chips)/CHIPS_PER_ROW)
            self.chips.arrange_in_grid(rows=rows, buff=0.04)
            self.add(self.chips)


def class_bar(labels, width=2.2, height=0.22):
    if len(labels) == 0:
        return Rectangle(width=width, height=height).set_stroke(GRAY, 1)
    counts = Counter(labels)
    n = len(labels)
    x = -width/2
    bar_parts = VGroup()
    for cls, col in CLASS_COLORS.items():
        w = (counts.get(cls, 0)/n) * width
        if w > 0:
            r = Rectangle(width=w, height=height).set_fill(col, 0.9).set_stroke(WHITE, 0.5)
            r.move_to([x + w/2, 0, 0])
            bar_parts.add(r)
            x += w
    frame = Rectangle(width=width, height=height).set_stroke(WHITE, 0.8)
    return VGroup(bar_parts, frame)


class TreeNodeVisual(VGroup):
    def __init__(self, title, labels, entropy_val, **kwargs):
        super().__init__(**kwargs)
        box = RoundedRectangle(width=3.2, height=2.2, corner_radius=0.2)
        box.set_stroke(NODE_COLOR, 2).set_fill(NODE_COLOR, 0.06)
        title_txt = Text(title, font_size=24, color=TEXT_COLOR)
        title_txt.next_to(box.get_top(), DOWN, buff=0.1)

        bar_title = Text("Class Distribution", font_size=18, color=TEXT_COLOR).next_to(title_txt, DOWN, buff=0.15)
        bar = class_bar(labels).next_to(bar_title, DOWN, buff=0.1)

        info = Text(f"""samples = {len(labels)}
entropy = {entropy_val:.3f}""", font_size=20, color=TEXT_COLOR)
        info.next_to(bar, DOWN, buff=0.1)
        self.add(box, title_txt, bar_title, bar, info)

        if SHOW_CHIPS:
            chips = SampleChips(labels)
            chips.next_to(info, DOWN, buff=0.1)
            self.add(chips)

        self.box = box
        self.title_txt = title_txt
        self.info = info


# ============= Scene =============
class ID3TraceScene(Scene):
    def construct(self):
        # Dataset
        data = {
            'outlook': [0,0,1,2,2,2,1,0,0,2,0,1,1,2],
            'temp':    [85,80,83,70,68,65,64,72,69,75,75,72,81,71],
            'humid':   [85,90,78,96,80,70,65,95,70,80,70,90,75,80],
            'play':    [0,0,1,1,1,0,1,0,1,1,1,1,1,0]
        }
        feature_names = ["outlook", "temp", "humid"]
        X = np.column_stack([data['outlook'], data['temp'], data['humid']])
        y = np.array(data['play'])

        # Collect events
        events = []
        tree = DecisionTree(max_depth=MAX_DEPTH, min_samples_split=MIN_SAMPLES_SPLIT,
                            event_callback=lambda ev: events.append(ev))
        tree.fit(X, y)

        # HUD + IG Panel
        hud = RoundedRectangle(width=5.5, height=2.5, corner_radius=0.2).set_stroke(GRAY, 1).set_fill(BLACK, 0.2)
        hud.to_corner(UR)
        hud_text = Text("", font_size=22, color=TEXT_COLOR).move_to(hud.get_center())
        self.play(FadeIn(hud))

        ig_frame = RoundedRectangle(width=5.5, height=2.5, corner_radius=0.2).set_stroke(GRAY, 1).set_fill(BLACK, 0.15)
        ig_frame.to_corner(DR)
        ig_title = Text("Information Gain (IG)", font_size=22, color=TEXT_COLOR).move_to(ig_frame.get_top()+DOWN*0.3)
        self.play(FadeIn(ig_frame), FadeIn(ig_title))

        ig_bars = {}
        ig_labels = {}
        for i, name in enumerate(feature_names):
            bar = Rectangle(width=0.01, height=0.2).set_fill(YELLOW, 0.8).set_stroke(WHITE, 0.5)
            bar.move_to(ig_frame.get_bottom()+UP*(0.5+i*0.5)+LEFT*2)
            label = Text(name, font_size=20, color=TEXT_COLOR).next_to(bar, LEFT)
            ig_label = Text("0.0", font_size=20, color=TEXT_COLOR).next_to(bar, RIGHT)
            self.play(FadeIn(bar), FadeIn(label), FadeIn(ig_label))
            ig_bars[name] = bar
            ig_labels[name] = ig_label

        # Calculation display
        calc_display = VGroup().to_corner(DL).add_background_rectangle(color=BLACK, opacity=0.5)
        self.play(FadeIn(calc_display))


        # Play events
        y_offset = 3
        x_offset = 0
        node_stack = []
        current_feature_index = -1

        for ev in events:
            t, p = ev["type"], ev["payload"]

            if t == "node_start":
                labels = p["labels"]
                ent = self.calculate_entropy_for_display(labels)
                nv = TreeNodeVisual("Node", labels, ent)
                nv.move_to([x_offset, y_offset, 0])
                self.play(FadeIn(nv))
                node_stack.append(nv)

                hud_text_new = Text(f"Creating new node.\n- {len(labels)} samples\n- Purity (Entropy): {ent:.3f}",
                                    font_size=22, color=TEXT_COLOR).move_to(hud.get_center())
                self.play(FadeOut(hud_text), FadeIn(hud_text_new))
                hud_text = hud_text_new

            elif t == "feature_eval_start":
                current_feature_index = p["feature"]
                fname = feature_names[current_feature_index]
                hud_text_new = Text(f"Scanning feature: {fname}", font_size=22, color=TEXT_COLOR).move_to(hud.get_center())
                self.play(FadeOut(hud_text), FadeIn(hud_text_new))
                hud_text = hud_text_new
                # Reset other IG bars
                for i, name in enumerate(feature_names):
                    if i != current_feature_index:
                        self.play(
                            Transform(ig_bars[name], Rectangle(width=0.01, height=0.2).set_fill(YELLOW, 0.8).set_stroke(WHITE, 0.5).move_to(ig_bars[name].get_center())),
                            Transform(ig_labels[name], Text("0.0", font_size=20, color=TEXT_COLOR).next_to(ig_bars[name], RIGHT))
                        )


            elif t == "ig_eval":
                fname = feature_names[current_feature_index]
                thr = p["threshold"]
                ig = p["ig"]

                # Update HUD
                hud_text_new = Text(f"Evaluating {fname} <= {thr:.2f}", font_size=22, color=TEXT_COLOR).move_to(hud.get_center())
                self.play(FadeOut(hud_text), FadeIn(hud_text_new))
                hud_text = hud_text_new

                # Show calculations
                calc_text = self.get_calculation_text(p)
                calc_text_obj = Text(calc_text, font_size=18, color=WHITE).move_to(calc_display)
                self.play(FadeIn(calc_text_obj))


                # Grow IG bar
                new_bar_width = ig * 4 # Scale factor for visibility
                new_bar = Rectangle(width=new_bar_width if new_bar_width > 0 else 0.01, height=0.2).set_fill(YELLOW, 0.8).set_stroke(WHITE, 0.5)
                new_bar.move_to(ig_bars[fname].get_center())
                new_bar.align_to(ig_bars[fname], LEFT)


                new_label = Text(f"{ig:.3f}", font_size=20, color=TEXT_COLOR).next_to(new_bar, RIGHT)
                self.play(Transform(ig_bars[fname], new_bar), Transform(ig_labels[fname], new_label))
                self.wait(0.2)
                self.play(FadeOut(calc_text_obj))


            elif t == "best_split":
                fname = feature_names[p["feature"]]
                thr = p["threshold"]
                nv = node_stack[-1]
                new_title = Text(f"{fname} <= {thr}", font_size=22, color=SPLIT_COLOR)
                new_title.move_to(nv.title_txt.get_center())
                self.play(Transform(nv.title_txt, new_title))

                hud_text_new = Text(f"Best split found!\nFeature: {fname}\nThreshold: {thr:.2f}\nInfo Gain: {p['gain']:.3f}",
                                    font_size=22, color=SPLIT_COLOR).move_to(hud.get_center())
                self.play(FadeOut(hud_text), FadeIn(hud_text_new))
                hud_text = hud_text_new

                # Prepare for children
                y_offset -= 2.5
                x_offset_left = x_offset - 3
                x_offset_right = x_offset + 3

                # Draw lines to children
                line_left = Line(nv.get_bottom(), [x_offset_left, y_offset, 0], color=WHITE, stroke_width=2)
                line_right = Line(nv.get_bottom(), [x_offset_right, y_offset, 0], color=WHITE, stroke_width=2)
                self.play(Create(line_left), Create(line_right))
                x_offset = x_offset_left # Next node will be the left one


            elif t == "node_leaf":
                c = p["leaf_class"]
                nv = node_stack.pop()
                nv.box.set_stroke(LEAF_COLOR, 3)
                leaf_label = Text(f"LEAF\nClass = {c}", font_size=20, color=LEAF_COLOR).next_to(nv.box, DOWN, buff=0.2)
                self.play(FadeIn(leaf_label))

                hud_text_new = Text(f"Reached a leaf node.\nPredicted class: {c}", font_size=22, color=LEAF_COLOR).move_to(hud.get_center())
                self.play(FadeOut(hud_text), FadeIn(hud_text_new))
                hud_text = hud_text_new

                if node_stack: # If this was a left child, move to the right
                    if x_offset < node_stack[-1].get_x():
                       x_offset = node_stack[-1].get_x() + 6


        self.wait(3)

    def calculate_entropy_for_display(self, labels):
        if not labels:
            return 0
        counts = Counter(labels)
        total = len(labels)
        ent = 0
        for count in counts.values():
            p = count / total
            if p > 0:
                ent -= p * math.log2(p)
        return ent

    def get_calculation_text(self, p):
        parent_ent_str = f"Parent Entropy: {p['parent_entropy']:.3f}"
        left_ent_str = f"Left Entropy: {p['left_entropy']:.3f} (n={p['n_left']})"
        right_ent_str = f"Right Entropy: {p['right_entropy']:.3f} (n={p['n_right']})"
        n = p['n_left'] + p['n_right']
        weighted_avg_str = f"Weighted Avg: ({p['n_left']}/{n})*{p['left_entropy']:.2f} + ({p['n_right']}/{n})*{p['right_entropy']:.2f}"
        ig_str = f"IG = {p['parent_entropy']:.3f} - ({p['left_entropy']:.3f}*{p['n_left']/n:.2f} + {p['right_entropy']:.3f}*{p['n_right']/n:.2f}) = {p['ig']:.3f}"

        return f"{parent_ent_str}\n{left_ent_str}\n{right_ent_str}\n\n{weighted_avg_str}\n\n{ig_str}"
