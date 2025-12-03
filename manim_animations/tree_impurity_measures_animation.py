from manim import *
import numpy as np

# --- Configuration ---
CONFIG = {
    "colors": {
        "background": "#1E1E2A",
        "primary_text": WHITE,
        "secondary_text": LIGHT_GREY,
        "regression_color": BLUE,
        "classification_color": GREEN,
        "formula_color": YELLOW,
        "highlight_color": RED,
        "bar_color": PURPLE,
    },
    "font_sizes": {
        "title": 48,
        "header": 36,
        "text": 28,
        "table_text": 24,
        "small_text": 20,
    },
}

def gini(p):
    p = np.array(p, dtype=float)
    return np.sum(p * (1 - p))  # = 1 - sum(p^2)

def entropy2(p):
    p = np.array(p, dtype=float)
    p = np.clip(p, 1e-12, 1.0)  # safe for log
    return -np.sum(p * np.log2(p))

def misclass_error(p):
    p = np.array(p, dtype=float)
    return 1 - np.max(p)

class TreeImpurityMeasuresAnimation(Scene):
    def construct(self):
        self.camera.background_color = CONFIG["colors"]["background"]
        self.show_title_card()
        self.show_main_table()
        self.show_live_demo()
        self.show_regression_note()
        self.show_summary()

    def show_title_card(self):
        # Title
        title = Text("Node Impurity Measures", 
                    font_size=CONFIG["font_sizes"]["title"], 
                    color=CONFIG["colors"]["primary_text"],
                    weight=BOLD)
        title.scale(0.9)
        
        # Subtitle
        subtitle = Text("Regression & Classification Trees", 
                       font_size=CONFIG["font_sizes"]["text"], 
                       color=CONFIG["colors"]["formula_color"],
                       weight=BOLD)
        subtitle.scale(0.9)
        
        # Measures list
        measures = Text("RSS • Misclassification Error • Gini • Entropy", 
                       font_size=CONFIG["font_sizes"]["small_text"], 
                       color=CONFIG["colors"]["secondary_text"],
                       slant=ITALIC)
        measures.scale(0.5)
        
        # Arrange elements
        title_group = VGroup(title, subtitle, measures).arrange(DOWN, buff=0.3)
        
        self.play(FadeIn(title, shift=UP*0.2))
        self.play(FadeIn(subtitle, shift=DOWN*0.2))
        self.play(FadeIn(measures, shift=DOWN*0.2))
        self.wait(1.2)
        
        # Fade out title card
        self.play(FadeOut(title_group))
        self.wait(1)

    def show_main_table(self):
        # Main title
        title = Text("Common Node Impurity Measures", 
                    font_size=CONFIG["font_sizes"]["header"], 
                    color=CONFIG["colors"]["primary_text"],
                    weight=BOLD)
        title.scale(0.75).to_edge(UP)
        self.play(Write(title))

        # Table headers
        headers = [
            Text("Tree Type", weight=BOLD, color=CONFIG["colors"]["primary_text"]).scale(0.45),
            Text("Impurity Measure", weight=BOLD, color=CONFIG["colors"]["primary_text"]).scale(0.45),
            Text("Formula", weight=BOLD, color=CONFIG["colors"]["primary_text"]).scale(0.45),
        ]
        
        # Table data
        data = [
            [
                Text("Regression", color=CONFIG["colors"]["regression_color"]).scale(0.45),
                Text("Residual Sum of Squares (RSS)", color=CONFIG["colors"]["primary_text"]).scale(0.45),
                MathTex(r"\sum_{i\in R_m}\,\bigl(y_i-\hat y_{R_m}\bigr)^2", color=CONFIG["colors"]["formula_color"]).scale(0.6),
            ],
            [
                Text("Classification", color=CONFIG["colors"]["classification_color"]).scale(0.45),
                Text("Classification Error Rate", color=CONFIG["colors"]["primary_text"]).scale(0.45),
                MathTex(r"1-\max_{1\le k\le K}\,\hat p_{mk}", color=CONFIG["colors"]["formula_color"]).scale(0.6),
            ],
            [
                Text("Classification", color=CONFIG["colors"]["classification_color"]).scale(0.45),
                Text("Gini Index", color=CONFIG["colors"]["primary_text"]).scale(0.45),
                MathTex(r"\sum_{k=1}^{K}\hat p_{mk}\,(1-\hat p_{mk})", color=CONFIG["colors"]["formula_color"]).scale(0.6),
            ],
            [
                Text("Classification", color=CONFIG["colors"]["classification_color"]).scale(0.45),
                Text("Entropy", color=CONFIG["colors"]["primary_text"]).scale(0.45),
                MathTex(r"-\sum_{k=1}^{K}\hat p_{mk}\,\log_{2}\hat p_{mk}", color=CONFIG["colors"]["formula_color"]).scale(0.6),
            ],
        ]

        # Create table manually
        table = VGroup()
        
        # Create table structure
        table_width = 8
        table_height = 2.5
        cell_width = table_width / 3
        cell_height = table_height / 5
        
        # Create grid lines
        for i in range(4):  # 4 rows
            h_line = Line(LEFT * table_width/2, RIGHT * table_width/2, color=CONFIG["colors"]["primary_text"])
            h_line.move_to(UP * (table_height/2 - i * cell_height))
            table.add(h_line)
        
        for i in range(4):  # 4 columns
            v_line = Line(UP * table_height/2, DOWN * table_height/2, color=CONFIG["colors"]["primary_text"])
            v_line.move_to(LEFT * table_width/2 + i * cell_width)
            table.add(v_line)
        
        # Add headers
        for i, header in enumerate(headers):
            header.move_to(UP * (table_height/2 - cell_height/2) + RIGHT * (i * cell_width - table_width/2 + cell_width/2))
            table.add(header)
        
        # Add data
        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                cell_data.move_to(UP * (table_height/2 - (row_idx + 2) * cell_height + cell_height/2) + 
                                RIGHT * (col_idx * cell_width - table_width/2 + cell_width/2))
                table.add(cell_data)
        
        table.scale(0.9).to_edge(LEFT, buff=0.5).shift(DOWN*0.1)
        self.play(Create(table))
        
        # Draw divider after regression row
        divider = Line(
            table.get_center() + UP * (table_height/2 - 2 * cell_height) + LEFT * table_width/2,
            table.get_center() + UP * (table_height/2 - 2 * cell_height) + RIGHT * table_width/2,
            stroke_width=2,
            color=CONFIG["colors"]["secondary_text"]
        )
        self.play(Create(divider))

        # Add labels
        reg_label = Text("Regression", weight=BOLD, color=CONFIG["colors"]["regression_color"]).scale(0.45)
        reg_label.next_to(table, LEFT, buff=0.2).align_to(table.get_center() + UP * (table_height/2 - 1.5 * cell_height), UP)
        
        cls_label = Text("Classification", weight=BOLD, color=CONFIG["colors"]["classification_color"]).scale(0.45)
        cls_label.next_to(table, LEFT, buff=0.2).align_to(table.get_center() + UP * (table_height/2 - 2.5 * cell_height), UP)
        
        self.play(FadeIn(reg_label), FadeIn(cls_label))
        
        self.wait(2)
        
        # Store table for later use
        self.table = table
        self.reg_label = reg_label
        self.cls_label = cls_label

    def show_live_demo(self):
        # Create panel
        panel = RoundedRectangle(
            corner_radius=0.2, 
            width=6.0, 
            height=4.2
        ).set_stroke(CONFIG["colors"]["primary_text"], 2).to_edge(RIGHT, buff=0.6)
        self.play(Create(panel))

        # Demo title
        demo_title = Text("Classification node: class probabilities", 
                         weight=BOLD, 
                         color=CONFIG["colors"]["primary_text"]).scale(0.5).next_to(panel, UP, buff=0.2)
        self.play(FadeIn(demo_title))

        # Create bars for 3 classes
        K = 3
        bar_w = 0.6
        base_y = panel.get_bottom()[1] + 0.5
        base_x = panel.get_left()[0] + 0.8
        xgap = 1.3
        
        bar_axes = VGroup()
        bars = VGroup()
        class_labels = VGroup()
        
        for k in range(K):
            # Y-axis for each bar
            y_axis = NumberLine(
                x_range=[0, 1, 0.2],
                length=2.6,
                rotation=90*DEGREES,
                include_numbers=True,
                decimal_number_config={"num_decimal_places": 1, "color": CONFIG["colors"]["primary_text"]},
                color=CONFIG["colors"]["primary_text"]
            ).move_to([base_x + k*xgap, base_y + 1.3, 0])
            
            # Bar rectangle
            bar_rect = Rectangle(
                width=bar_w, 
                height=0.001
            ).set_fill(CONFIG["colors"]["bar_color"], opacity=0.8).set_stroke(CONFIG["colors"]["bar_color"], 0)
            bar_rect.move_to([base_x + k*xgap, base_y, 0], aligned_edge=DOWN)
            
            # Class label
            label = Text(f"Class {k+1}", color=CONFIG["colors"]["primary_text"]).scale(0.4).next_to(y_axis, DOWN, buff=0.2)
            
            bar_axes.add(y_axis)
            bars.add(bar_rect)
            class_labels.add(label)

        self.play(LaggedStart(*[Create(ax) for ax in bar_axes], lag_ratio=0.05))
        self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.05))
        self.play(LaggedStart(*[FadeIn(t) for t in class_labels], lag_ratio=0.05))

        # Live formulas with numeric values
        f_gini = MathTex(r"\text{Gini}=1-\sum_k \hat p_k^2 \;=\; ", color=CONFIG["colors"]["formula_color"]).scale(0.6).to_edge(RIGHT).shift(UP*0.6+LEFT*0.5)
        f_ent = MathTex(r"H=-\sum_k \hat p_k\log_2\hat p_k \;=\; ", color=CONFIG["colors"]["formula_color"]).next_to(f_gini, DOWN, aligned_edge=LEFT, buff=0.25)
        f_err = MathTex(r"\text{Error}=1-\max_k \hat p_k \;=\; ", color=CONFIG["colors"]["formula_color"]).next_to(f_ent, DOWN, aligned_edge=LEFT, buff=0.25)
        
        self.play(Write(f_gini), Write(f_ent), Write(f_err))

        value_gini = DecimalNumber(0, num_decimal_places=3, color=CONFIG["colors"]["highlight_color"]).scale(0.6).next_to(f_gini, RIGHT, buff=0.1)
        value_ent = DecimalNumber(0, num_decimal_places=3, color=CONFIG["colors"]["highlight_color"]).scale(0.6).next_to(f_ent, RIGHT, buff=0.1)
        value_err = DecimalNumber(0, num_decimal_places=3, color=CONFIG["colors"]["highlight_color"]).scale(0.6).next_to(f_err, RIGHT, buff=0.1)
        
        self.add(value_gini, value_ent, value_err)

        # Helper function to animate probabilities
        def animate_probs(p, run_time=1.0):
            p = np.array(p, dtype=float)
            p = p / p.sum()  # normalize
            
            # Animate bar heights
            anims = []
            for j in range(K):
                target_h = 2.6 * p[j]
                # Scale the bar to the target height
                scale_factor = target_h / bars[j].height if bars[j].height > 0 else 1
                anims.append(bars[j].animate.scale(scale_factor, about_point=bars[j].get_bottom()))
            
            # Calculate new values
            g, h, e = gini(p), entropy2(p), misclass_error(p)
            
            return Succession(
                AnimationGroup(*anims, lag_ratio=0.02, run_time=run_time),
                AnimationGroup(
                    value_gini.animate.set_value(g),
                    value_ent.animate.set_value(h),
                    value_err.animate.set_value(e),
                    run_time=0.8
                )
            )

        # Scenario 1: Uniform (1/3, 1/3, 1/3)
        self.play(animate_probs([1/3, 1/3, 1/3], run_time=1.0))
        callout1 = Text("Max impurity when classes are uniform", 
                       slant=ITALIC, 
                       color=CONFIG["colors"]["secondary_text"]).scale(0.45).next_to(panel, DOWN, buff=0.2)
        self.play(FadeIn(callout1, shift=DOWN*0.1))
        self.wait(0.5)

        # Scenario 2: Skewed (0.8, 0.1, 0.1)
        self.play(FadeOut(callout1, shift=DOWN*0.1))
        self.play(animate_probs([0.8, 0.1, 0.1], run_time=1.0))
        callout2 = Text("Impurity drops as one class dominates", 
                       slant=ITALIC, 
                       color=CONFIG["colors"]["secondary_text"]).scale(0.45).next_to(panel, DOWN, buff=0.2)
        self.play(FadeIn(callout2, shift=DOWN*0.1))
        self.wait(0.5)

        # Scenario 3: Pure (1, 0, 0)
        self.play(FadeOut(callout2, shift=DOWN*0.1))
        self.play(animate_probs([1.0, 0.0, 0.0], run_time=1.0))
        callout3 = Text("Pure node ⇒ impurity = 0 (Gini/Entropy), error = 0", 
                       slant=ITALIC, 
                       color=CONFIG["colors"]["secondary_text"]).scale(0.45).next_to(panel, DOWN, buff=0.2)
        self.play(FadeIn(callout3, shift=DOWN*0.1))
        self.wait(0.6)
        
        # Store elements for summary
        self.panel = panel
        self.demo_title = demo_title
        self.bars = bars
        self.value_gini = value_gini
        self.value_ent = value_ent
        self.value_err = value_err

    def show_regression_note(self):
        # Regression note box
        rss_box = RoundedRectangle(
            corner_radius=0.15, 
            width=12.2, 
            height=1.4
        ).set_fill(BLACK, 0.9).set_stroke(CONFIG["colors"]["primary_text"], 2)
        
        rss_text = VGroup(
            Text("Regression nodes:", weight=BOLD, color=CONFIG["colors"]["formula_color"]).scale(0.5),
            Text("Use RSS: predict the leaf mean; splitting aims to reduce RSS.", 
                 slant=ITALIC, 
                 color=CONFIG["colors"]["primary_text"]).scale(0.48),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        
        rss_panel = VGroup(rss_box, rss_text).to_edge(DOWN, buff=0.25)
        rss_text.move_to(rss_box.get_center())
        
        self.play(FadeIn(rss_box, shift=UP*0.1), FadeIn(rss_text, shift=UP*0.1))
        self.wait(1.2)
        
        # Store for summary
        self.rss_panel = rss_panel

    def show_summary(self):
        # Summary card
        card = RoundedRectangle(
            corner_radius=0.2, 
            width=12.2, 
            height=3.0
        ).set_fill(BLACK, 0.95).set_stroke(CONFIG["colors"]["primary_text"], 2)
        
        h = Text("Cheat Sheet", weight=BOLD, color=CONFIG["colors"]["formula_color"]).scale(0.6)
        
        bullets = VGroup(
            Text("Regression: RSS = ∑(y − leaf mean)²", 
                 slant=ITALIC, 
                 color=CONFIG["colors"]["primary_text"]).scale(0.48),
            Text("Classification: Error = 1 − max p̂; Gini = 1 − ∑ p̂²; Entropy = −∑ p̂ log₂ p̂", 
                 slant=ITALIC, 
                 color=CONFIG["colors"]["primary_text"]).scale(0.48),
            Text("All decrease as a node becomes more pure; zero at a pure node.", 
                 slant=ITALIC, 
                 color=CONFIG["colors"]["primary_text"]).scale(0.48),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        
        summary = VGroup(h, bullets).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        summary_group = VGroup(card, summary).to_edge(DOWN, buff=0.25)
        summary.move_to(card.get_center())

        # Fade out previous elements
        self.play(FadeOut(self.rss_panel))
        
        self.play(FadeIn(card, shift=UP*0.15), FadeIn(summary, shift=UP*0.15))
        self.play(Wiggle(self.value_gini), Wiggle(self.value_ent), Wiggle(self.value_err))
        self.wait(1.4)
        
        # Final fade out
        self.play(FadeOut(VGroup(
            self.table, self.reg_label, self.cls_label,
            self.panel, self.demo_title, self.bars,
            self.value_gini, self.value_ent, self.value_err,
            card, summary
        )))
        self.wait(1)
