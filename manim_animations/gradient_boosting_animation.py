from manim import *
import numpy as np
from sklearn.tree import DecisionTreeRegressor

class GradientBoostingAnimation(Scene):
    def construct(self):
        self.next_section("Introduction")
        title = Text("Gradient Boosting Animation").to_edge(UP)
        subtitle = Text("Focus: Sequential Error Correction").next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        self.wait(1)

        # Create Axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            x_length=8,
            y_length=6,
            axis_config={
                "color": GRAY,
                "include_numbers": True,
                "font_size": 24,
            },
        ).to_edge(DOWN).shift(UP*0.5)

        x_label = axes.get_x_axis_label("Feature (X)")
        y_label = axes.get_y_axis_label("Target (Y)")

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(0.5)

        # Generate Data Points
        np.random.seed(0)
        X = np.linspace(0.5, 9.5, 20).reshape(-1, 1)
        y = np.sin(X).flatten() * 2 + X.flatten() * 0.5 + np.random.normal(0, 0.5, X.shape[0]) + 3

        points_group = VGroup()
        for i in range(len(X)):
            x_coord = float(X[i, 0])
            y_coord = float(y[i])
            dot = Dot(axes.coords_to_point(x_coord, y_coord), color=BLUE)
            points_group.add(dot)
        
        self.play(FadeIn(points_group))
        self.wait(1)

        # Initial Prediction (F0) - Mean of Y
        self.next_section("InitialPrediction")
        initial_pred_text = Text("1. Initial Prediction (F₀)").to_edge(UP).shift(DOWN*0.5)
        self.play(FadeOut(title), FadeOut(subtitle), Write(initial_pred_text))

        F0 = np.mean(y)
        F0_graph = axes.plot(lambda x: F0, color=YELLOW)
        F0_label = Text(f"F₀ = {F0:.2f}").next_to(F0_graph, UP).scale(0.6)
        self.play(Create(F0_graph), Write(F0_label))
        self.wait(1)

        current_prediction = np.full_like(y, F0)
        learning_rate = 0.5
        n_iterations = 3

        for i in range(n_iterations):
            self.next_section(f"Iteration_{i+1}")
            iteration_text = Text(f"Iteration {i+1}").to_edge(UP).shift(DOWN*0.5)
            self.play(FadeOut(initial_pred_text) if i == 0 else FadeOut(prev_iteration_text), 
                      FadeOut(F0_label) if i == 0 else FadeOut(prev_tree_label), 
                      Write(iteration_text))
            prev_iteration_text = iteration_text

            # Calculate Residuals
            residuals = y - current_prediction
            residuals_text = Text("2. Calculate Residuals").next_to(iteration_text, DOWN)
            self.play(Write(residuals_text))

            residual_lines = VGroup()
            for j in range(len(X)):
                x_coord = float(X[j, 0])
                y_coord = float(y[j])
                pred_coord = float(current_prediction[j])
                line = Line(axes.coords_to_point(x_coord, y_coord), 
                            axes.coords_to_point(x_coord, pred_coord), 
                            color=RED, stroke_width=2)
                residual_lines.add(line)
            self.play(Create(residual_lines))
            self.wait(1)

            # Fit Weak Learner (Tree) to Residuals
            fit_tree_text = Text("3. Fit Weak Learner (f_b) to Residuals").next_to(residuals_text, DOWN)
            self.play(FadeOut(residuals_text), Write(fit_tree_text))

            tree_model = DecisionTreeRegressor(max_depth=1, random_state=i) # Simple stump
            tree_model.fit(X, residuals)
            tree_pred = tree_model.predict(X)

            tree_graph = axes.plot(lambda x_val: tree_model.predict(np.array([[x_val]]))[0] + current_prediction[0] - residuals[0], color=GREEN)
            tree_label = Text(f"f_{i+1}(X)").next_to(tree_graph, UP).scale(0.6)
            self.play(Create(tree_graph), Write(tree_label))
            self.wait(1)

            # Update Prediction
            update_pred_text = Text("4. Update Prediction (F_b = F_{b-1} + λ * f_b)").next_to(fit_tree_text, DOWN)
            self.play(FadeOut(fit_tree_text), FadeOut(residual_lines), Write(update_pred_text))

            new_prediction = current_prediction + learning_rate * tree_pred
            new_prediction_graph = axes.plot(lambda x_val: new_prediction[np.argmin(np.abs(X.flatten() - x_val))], color=ORANGE)
            
            self.play(Transform(F0_graph, new_prediction_graph))
            current_prediction = new_prediction
            self.wait(1)
            prev_tree_label = tree_label
            
            self.play(FadeOut(update_pred_text))

        self.next_section("Conclusion")
        final_text = Text("Gradient Boosting Complete").to_edge(UP)
        self.play(FadeOut(prev_iteration_text), FadeOut(F0_graph), FadeOut(prev_tree_label), 
                  FadeOut(points_group), FadeOut(axes), FadeOut(x_label), FadeOut(y_label), 
                  Write(final_text))
        self.wait(2)
