from manim import *
import numpy as np

class LM_GLM_ComparisonScene(Scene):
    def construct(self):
        self.camera.background_color = "#333333"  # Dark background to match the image

        # --- Title and Headers ---
        title = Text("LM vs. GLM: Property Comparison", font_size=48, color=WHITE).to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Table Headers
        prop_header = Text("Property", font_size=36, color=WHITE)
        lm_header = Text("LMs", font_size=36, color=BLUE)
        glm_header = Text("GLMs", font_size=36, color=RED)

        table_headers = VGroup(prop_header, lm_header, glm_header).arrange(RIGHT, buff=2.0)
        table_headers.next_to(title, DOWN, buff=0.8)
        
        self.play(FadeIn(table_headers, shift=UP))
        self.wait(0.5)

        # --- Properties List ---
        properties_list_text = [
            "Independence",
            "Target distribution",
            "Mean",
            "Variance"
        ]
        
        properties_mobjects = VGroup(*[
            Text(prop, font_size=32, color=WHITE)
            for prop in properties_list_text
        ]).arrange(DOWN, buff=0.7, aligned_edge=LEFT)
        properties_mobjects.next_to(prop_header, DOWN, buff=0.5).align_to(prop_header, LEFT)

        self.play(FadeIn(properties_mobjects, shift=LEFT))
        self.wait(1)

        # --- Explanations (Row by Row) ---
        explanations = {
            "Independence": {
                "LM": "Given the predictor values, the observations of the target variable are independent.",
                "GLM": "Same as LMs"
            },
            "Target distribution": {
                "LM": "Target follows a normal distribution",
                "GLM": "Target is from the linear exponential family"
            },
            "Mean": {
                "LM": r"$\mu = \beta_0 + \beta_1 X_1 + \dots + \beta_p X_p$",
                "GLM": r"$g(\mu) = \eta$" + "\n (link function)"
            },
            "Variance": {
                "LM": "Constant across predictor values",
                "GLM": "Varies with $\mu$ and predictor values"
            }
        }
        
        # Positions for explanations
        lm_pos = lm_header.get_center() + DOWN*0.5
        glm_pos = glm_header.get_center() + DOWN*0.5

        for i, prop_name in enumerate(properties_list_text):
            prop_mobj = properties_mobjects[i]
            
            # Highlight property
            self.play(prop_mobj.animate.set_color(YELLOW))
            self.wait(0.5)

            # LM explanation
            if prop_name == "Mean":
                lm_exp_text = MathTex(r"\mu = \beta_0 + \beta_1 X_1 + \dots + \beta_p X_p", color=WHITE, font_size=28)
            else:
                lm_exp_text = Text(explanations[prop_name]["LM"], font_size=28, color=WHITE)
            lm_exp_text.next_to(lm_header, DOWN, buff=(i+0.5)*0.7).scale(0.8)
            
            # GLM explanation
            if prop_name == "Mean":
                glm_exp_text = VGroup(
                    MathTex(r"g(\mu) = \eta", color=WHITE, font_size=28),
                    Text("(link function)", font_size=24, color=WHITE)
                ).arrange(DOWN, buff=0.1)
            else:
                glm_exp_text = Text(explanations[prop_name]["GLM"], font_size=28, color=WHITE)
            glm_exp_text.next_to(glm_header, DOWN, buff=(i+0.5)*0.7).scale(0.8)

            self.play(Write(lm_exp_text))
            self.play(Write(glm_exp_text))
            self.wait(1)
            
            # Unhighlight property
            self.play(prop_mobj.animate.set_color(WHITE))

        self.wait(1)

        # --- Link Function Note ---
        note_text = Text(
            "Note: The link function in a GLM is applied to the target mean μ, "
            "the target variable itself is not transformed.",
            font_size=28,
            color=GRAY_A
        ).to_edge(DOWN, buff=0.5).scale(0.8)
        
        self.play(FadeIn(note_text, shift=DOWN))
        self.wait(3)

        # --- Additional Visual Examples ---
        self.play(FadeOut(VGroup(title, table_headers, properties_mobjects, note_text)))
        
        # Clear previous explanations
        all_explanations = VGroup()
        for i in range(len(properties_list_text)):
            all_explanations.add(properties_mobjects[i])
        
        # Show visual examples
        examples_title = Text("Visual Examples", font_size=48, color=WHITE).to_edge(UP, buff=0.5)
        self.play(Write(examples_title))
        
        # LM Example
        lm_example_title = Text("Linear Model Example", font_size=32, color=BLUE).move_to(UP * 1.5 + LEFT * 3)
        
        # Create axes for LM
        lm_axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 20, 4],
            x_length=4,
            y_length=3,
            axis_config={"color": WHITE},
            x_axis_config={"numbers_to_include": np.arange(0, 11, 2)},
            y_axis_config={"numbers_to_include": np.arange(0, 21, 4)},
        ).move_to(UP * 0.5 + LEFT * 3)
        
        lm_x_label = lm_axes.get_x_axis_label(Text("X", font_size=24, color=WHITE))
        lm_y_label = lm_axes.get_y_axis_label(Text("Y", font_size=24, color=WHITE))
        
        # LM data points and line
        lm_data = VGroup(*[
            Dot(lm_axes.coords_to_point(x, 2 + 1.5*x + np.random.uniform(-1, 1)), color=BLUE, radius=0.05)
            for x in np.arange(1, 9, 0.5)
        ])
        lm_line = lm_axes.plot(lambda x: 2 + 1.5*x, color=BLUE, stroke_width=3)
        
        self.play(Write(lm_example_title))
        self.play(Create(lm_axes), Write(lm_x_label), Write(lm_y_label))
        self.play(FadeIn(lm_data))
        self.play(Create(lm_line))
        
        # GLM Example
        glm_example_title = Text("GLM Example (Logistic)", font_size=32, color=RED).move_to(UP * 1.5 + RIGHT * 3)
        
        # Create axes for GLM
        glm_axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 1, 0.2],
            x_length=4,
            y_length=3,
            axis_config={"color": WHITE},
            x_axis_config={"numbers_to_include": np.arange(0, 11, 2)},
            y_axis_config={"numbers_to_include": np.arange(0, 1.1, 0.2)},
        ).move_to(UP * 0.5 + RIGHT * 3)
        
        glm_x_label = glm_axes.get_x_axis_label(Text("X", font_size=24, color=WHITE))
        glm_y_label = glm_axes.get_y_axis_label(Text("P(Y=1)", font_size=24, color=WHITE))
        
        # GLM data points and curve
        glm_data = VGroup(*[
            Dot(glm_axes.coords_to_point(x, 1/(1+np.exp(-(x-5))) + np.random.uniform(-0.1, 0.1)), color=RED, radius=0.05)
            for x in np.arange(1, 9, 0.3)
        ])
        glm_curve = glm_axes.plot(lambda x: 1/(1+np.exp(-(x-5))), color=RED, stroke_width=3)
        
        self.play(Write(glm_example_title))
        self.play(Create(glm_axes), Write(glm_x_label), Write(glm_y_label))
        self.play(FadeIn(glm_data))
        self.play(Create(glm_curve))
        
        self.wait(2)
        
        # Key differences summary
        differences_title = Text("Key Differences", font_size=36, color=YELLOW).move_to(DOWN * 1)
        differences = VGroup(
            Text("• LM: Linear relationship, normal errors", font_size=24, color=BLUE),
            Text("• GLM: Non-linear relationship, exponential family", font_size=24, color=RED),
            Text("• LM: Constant variance", font_size=24, color=BLUE),
            Text("• GLM: Variance depends on mean", font_size=24, color=RED)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        differences.move_to(DOWN * 2.5)
        
        self.play(Write(differences_title))
        self.play(Write(differences))
        self.wait(3)
        
        # Final fade out
        self.play(FadeOut(VGroup(
            examples_title, lm_example_title, lm_axes, lm_x_label, lm_y_label, 
            lm_data, lm_line, glm_example_title, glm_axes, glm_x_label, glm_y_label,
            glm_data, glm_curve, differences_title, differences
        )))
        self.wait(1)
