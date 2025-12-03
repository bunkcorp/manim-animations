from manim import *
import numpy as np

class InteractionEffectScene(Scene):
    def construct(self):
        # 1. Setup the scene and axes
        self.camera.background_color = "#f0f0f0"  # Light gray background
        ax = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 12, 2],
            x_length=7,
            y_length=5,
            axis_config={"color": BLACK, "include_tip": False},
            x_axis_config={"numbers_to_include": np.arange(2, 11, 2)},
            y_axis_config={"numbers_to_include": np.arange(2, 13, 2)},
        ).to_edge(DL, buff=1)

        x_label = ax.get_x_axis_label(
            Text("Predictor (e.g., KWH_TOTAL_SQFT)", color=BLACK, font_size=32),
            edge=DOWN,
            direction=DOWN,
            buff=0.4
        )
        y_label = ax.get_y_axis_label(
            Text("Outcome", color=BLACK, font_size=32).rotate(90 * DEGREES),
            edge=LEFT,
            direction=LEFT,
            buff=0.4
        )
        title = Title("Interpreting an Interaction Effect", color=BLACK, font_size=40)
        self.add(title)

        # 2. Define regression parameters
        main_effect_slope = 0.5
        interaction_effect_slope = 0.6
        intercept = 2.0
        
        # 3. Create data points for two groups
        group1_dots = VGroup(*[
            Dot(ax.coords_to_point(x, main_effect_slope * x + intercept + np.random.uniform(-0.5, 0.5)), color=BLUE)
            for x in np.arange(1, 9, 0.5)
        ])
        
        group2_dots = VGroup(*[
            Dot(ax.coords_to_point(x, (main_effect_slope + interaction_effect_slope) * x + intercept + np.random.uniform(-0.5, 0.5)), color=RED)
            for x in np.arange(1, 9, 0.5)
        ])
        
        # 4. ANIMATION SEQUENCE STARTS HERE
        self.play(Create(ax), Write(x_label), Write(y_label))
        self.wait(0.5)

        # Show baseline group and its regression line
        legend_group1 = VGroup(Dot(color=BLUE), Text("Baseline Group", color=BLACK, font_size=28)).arrange(RIGHT).to_edge(UR)
        self.play(FadeIn(group1_dots, shift=UP), Write(legend_group1))
        
        # Line for the main effect
        main_effect_line = ax.plot(lambda x: main_effect_slope * x + intercept, x_range=[0, 9], color=BLUE)
        line_label_main = MathTex(r"\text{Slope} = \beta_1", color=BLUE, font_size=36).next_to(main_effect_line, UR, buff=-1.5)
        
        self.play(Create(main_effect_line), Write(line_label_main))
        self.wait(1)

        # Introduce the second group
        legend_group2 = VGroup(Dot(color=RED), Text("Group B", color=BLACK, font_size=28)).arrange(RIGHT).next_to(legend_group1, DOWN)
        self.play(FadeIn(group2_dots, shift=UP), Write(legend_group2))
        self.wait(1)

        # Line for the interaction effect
        interaction_line = ax.plot(lambda x: (main_effect_slope + interaction_effect_slope) * x + intercept, x_range=[0, 9], color=RED)
        
        self.play(Create(interaction_line))
        self.wait(1)
        
        # Use a brace to show the interaction effect
        # We create two lines to form a visual wedge for the brace
        brace_line1 = DashedLine(
            ax.coords_to_point(7, main_effect_slope * 7 + intercept),
            ax.coords_to_point(9, main_effect_slope * 9 + intercept),
            color=BLUE
        )
        brace_line2 = DashedLine(
            ax.coords_to_point(7, main_effect_slope * 7 + intercept),
            ax.coords_to_point(9, (main_effect_slope + interaction_effect_slope) * 9 + intercept),
            color=RED
        )
        brace = Brace(brace_line2, direction=brace_line2.get_unit_vector() + 0.9*UP + 0.5*RIGHT, color=BLACK)
        
        interaction_label = MathTex(r"\beta_2 (\text{Interaction})", color=DARK_GRAY, font_size=36)
        interaction_label.next_to(brace, UP)
        
        self.play(
            FadeOut(line_label_main),
            Create(brace_line1),
            Create(brace_line2)
        )
        self.play(GrowFromCenter(brace), Write(interaction_label))
        self.wait(1)
        
        # Final descriptive text
        final_text_group_1 = MathTex(r"\text{Baseline Slope} = \beta_1 (\text{Main Effect})", color=BLUE).next_to(ax, DOWN, buff=1.2, aligned_edge=LEFT)
        final_text_group_2 = MathTex(r"\text{Group B Slope} = \beta_1 + \beta_2", color=RED).next_to(final_text_group_1, DOWN, buff=0.2, aligned_edge=LEFT)

        self.play(Write(final_text_group_1))
        self.wait(0.5)
        self.play(Write(final_text_group_2))
        self.wait(3)

        # Add explanation of what interaction means
        explanation_title = Text("What This Means:", color=BLACK, font_size=32).next_to(final_text_group_2, DOWN, buff=0.5, aligned_edge=LEFT)
        explanation_text = VGroup(
            Text("• The effect of the predictor differs between groups", color=BLACK, font_size=24),
            Text("• Group B has a stronger relationship with the outcome", color=BLACK, font_size=24),
            Text("• The interaction term (β₂) captures this difference", color=BLACK, font_size=24)
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        explanation_text.next_to(explanation_title, DOWN, buff=0.3, aligned_edge=LEFT)
        
        self.play(Write(explanation_title))
        self.play(Write(explanation_text))
        self.wait(3)

        # Show the mathematical model
        model_title = Text("Mathematical Model:", color=BLACK, font_size=32).move_to(UP * 2 + RIGHT * 3)
        model_equation = MathTex(
            r"Y = \beta_0 + \beta_1 X + \beta_2 (X \times \text{Group}) + \epsilon",
            color=BLACK, font_size=28
        ).next_to(model_title, DOWN, buff=0.3)
        
        self.play(Write(model_title))
        self.play(Write(model_equation))
        self.wait(2)

        # Final summary
        summary_text = Text(
            "Interaction effects show how the relationship between variables changes across different groups or conditions",
            color=BLACK, font_size=24, line_spacing=1.2
        ).move_to(DOWN * 3.5)
        
        self.play(Write(summary_text))
        self.wait(3)

        # Fade out everything
        self.play(FadeOut(VGroup(
            title, ax, x_label, y_label, group1_dots, group2_dots, 
            legend_group1, legend_group2, main_effect_line, interaction_line,
            brace_line1, brace_line2, brace, interaction_label,
            final_text_group_1, final_text_group_2, explanation_title, explanation_text,
            model_title, model_equation, summary_text
        )))
        self.wait(1)
