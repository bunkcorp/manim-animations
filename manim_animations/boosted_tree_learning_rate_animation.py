from manim import *
import numpy as np

class BoostedTreeLearningRate(Scene):
    def construct(self):
        # Title
        title = Text("Effect of Learning Rate on Boosted Tree Performance", font_size=36, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))

        # Create axes
        axes = Axes(
            x_range=[0, 100, 20],
            y_range=[0, 1, 0.2],
            x_length=6,
            y_length=4,
            axis_config={"color": BLUE},
            x_axis_config={"numbers_to_include": np.arange(0, 101, 20)},
            y_axis_config={"numbers_to_include": np.arange(0, 1.1, 0.2)},
        ).add_coordinates()

        axes_labels = axes.get_axis_labels(
            x_label="Number of Trees", y_label="RMSE"
        )

        # High Learning Rate
        high_lr_text = Text("High Learning Rate (Overfitting)", font_size=24, color=RED).next_to(axes, UP, buff=0.2)
        high_lr_train_curve = axes.plot(lambda x: 0.1 + 0.6 * np.exp(-0.1 * x), color=GREEN)
        high_lr_test_curve = axes.plot(lambda x: 0.4 + 0.0001 * x**2, color=RED)
        high_lr_train_label = axes.get_graph_label(high_lr_train_curve, "Train RMSE", x_val=60)
        high_lr_test_label = axes.get_graph_label(high_lr_test_curve, "Test RMSE", x_val=60)

        # Low Learning Rate
        low_lr_text = Text("Low Learning Rate (Good Fit)", font_size=24, color=GREEN).next_to(axes, UP, buff=0.2)
        low_lr_train_curve = axes.plot(lambda x: 0.3 + 0.4 * np.exp(-0.05 * x), color=GREEN)
        low_lr_test_curve = axes.plot(lambda x: 0.4 + 0.1 * np.exp(-0.05 * x), color=RED)
        low_lr_train_label = axes.get_graph_label(low_lr_train_curve, "Train RMSE", x_val=60, direction=UP)
        low_lr_test_label = axes.get_graph_label(low_lr_test_curve, "Test RMSE", x_val=60, direction=DOWN)

        # Animation
        self.play(Create(axes), Write(axes_labels))
        self.wait(1)

        # High Learning Rate Animation
        self.play(Write(high_lr_text))
        self.play(Create(high_lr_train_curve), Write(high_lr_train_label))
        self.play(Create(high_lr_test_curve), Write(high_lr_test_label))
        self.wait(2)

        # Show the problem with high learning rate
        problem_text = Text(
            "Problem: Large gap between train and test performance",
            font_size=20, color=RED
        ).next_to(axes, DOWN, buff=0.5)
        self.play(Write(problem_text))
        self.wait(2)
        self.play(FadeOut(problem_text))

        # Transform to Low Learning Rate
        self.play(
            Transform(high_lr_text, low_lr_text),
            Transform(high_lr_train_curve, low_lr_train_curve),
            Transform(high_lr_test_curve, low_lr_test_curve),
            Transform(high_lr_train_label, low_lr_train_label),
            Transform(high_lr_test_label, low_lr_test_label)
        )
        self.wait(2)

        # Show the benefit of low learning rate
        benefit_text = Text(
            "Benefit: Train and test performance converge",
            font_size=20, color=GREEN
        ).next_to(axes, DOWN, buff=0.5)
        self.play(Write(benefit_text))
        self.wait(2)
        self.play(FadeOut(benefit_text))

        # Add learning rate values
        lr_values = VGroup(
            Text("High Learning Rate: η = 0.3", font_size=18, color=RED),
            Text("Low Learning Rate: η = 0.1", font_size=18, color=GREEN)
        ).arrange(DOWN, buff=0.3)
        lr_values.move_to([-4, -2, 0])
        self.play(Write(lr_values))
        self.wait(2)

        # Summary
        summary = VGroup(
            Text("Learning Rate Effects:", font_size=24, color=BLUE),
            Text("• High LR: Fast learning, risk of overfitting", font_size=18, color=RED),
            Text("• Low LR: Slow learning, better generalization", font_size=18, color=GREEN),
            Text("• Choose LR based on validation performance", font_size=18, color=YELLOW)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        summary.move_to([4, -2, 0])
        self.play(Write(summary))
        self.wait(3)

        # Final fade out
        self.play(FadeOut(VGroup(title, axes, axes_labels, low_lr_text, low_lr_train_curve, low_lr_test_curve, low_lr_train_label, low_lr_test_label, lr_values, summary)))
        self.wait(1)
