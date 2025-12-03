from manim import *
import numpy as np

# --- Configuration ---
CONFIG = {
    "colors": {
        "background": "#1E1E2A",
        "primary_text": WHITE,
        "secondary_text": LIGHT_GREY,
        "training_color": BLUE,
        "test_color": RED,
        "positive_color": GREEN,
        "negative_color": ORANGE,
        "neutral_color": YELLOW,
        "warning_color": RED,
        "success_color": GREEN,
    },
    "font_sizes": {
        "title": 48,
        "header": 32,
        "text": 24,
        "label": 20,
    },
}

class StratifiedSamplingAnimation(Scene):
    def construct(self):
        self.camera.background_color = CONFIG["colors"]["background"]

        # --- Scene 1: Introduction ---
        self.show_intro()

        # --- Scene 2: The Problem with Random Splitting ---
        self.show_random_splitting_problem()

        # --- Scene 3: Stratified Sampling Solution ---
        self.show_stratified_solution()

        # --- Scene 4: Visual Comparison ---
        self.show_comparison()

        # --- Scene 5: Why It Matters ---
        self.show_why_it_matters()

        # --- Scene 6: Summary ---
        self.show_summary()

    def show_intro(self):
        """Introduces the concept of stratified sampling."""
        title = Text("Stratified Sampling for Train/Test Splits", font_size=CONFIG["font_sizes"]["title"])
        subtitle = Text("Ensuring Representative Data Distribution", font_size=CONFIG["font_sizes"]["header"], color=CONFIG["colors"]["secondary_text"]).next_to(title, DOWN)
        
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(2)
        
        # Key concept
        key_concept = Text(
            "Stratification is based on the TARGET variable, not the predictors",
            font_size=CONFIG["font_sizes"]["text"],
            color=CONFIG["colors"]["success_color"]
        ).next_to(subtitle, DOWN, buff=1)
        
        self.play(Write(key_concept))
        self.wait(2)
        self.play(FadeOut(VGroup(title, subtitle, key_concept)))

    def show_random_splitting_problem(self):
        """Shows the problem with random splitting on imbalanced data."""
        title = Text("The Problem: Random Splitting on Imbalanced Data", font_size=CONFIG["font_sizes"]["header"]).to_edge(UP)
        self.play(Write(title))

        # Show imbalanced dataset
        dataset_title = Text("Imbalanced Dataset", font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["warning_color"])
        dataset_title.move_to([-4, 1, 0])

        # Create imbalanced data points
        data_points = VGroup()
        
        # 80% negative class (orange)
        for i in range(80):
            point = Circle(radius=0.08, fill_color=CONFIG["colors"]["negative_color"], fill_opacity=0.8)
            x = np.random.uniform(-3, -1)
            y = np.random.uniform(-2, 2)
            point.move_to([x, y, 0])
            data_points.add(point)
        
        # 20% positive class (green)
        for i in range(20):
            point = Circle(radius=0.08, fill_color=CONFIG["colors"]["positive_color"], fill_opacity=0.8)
            x = np.random.uniform(1, 3)
            y = np.random.uniform(-2, 2)
            point.move_to([x, y, 0])
            data_points.add(point)

        # Show distribution
        distribution_text = VGroup(
            Text("Distribution:", font_size=CONFIG["font_sizes"]["text"]),
            Text("80% Negative (Orange)", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["negative_color"]),
            Text("20% Positive (Green)", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["positive_color"])
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        distribution_text.move_to([4, 1, 0])

        self.play(Write(dataset_title))
        self.play(FadeIn(data_points))
        self.play(Write(distribution_text))
        self.wait(2)

        # Show random split
        split_title = Text("Random 80/20 Split", font_size=CONFIG["font_sizes"]["text"])
        split_title.move_to([0, -1, 0])
        self.play(Write(split_title))

        # Create training and test sets
        training_points = VGroup()
        test_points = VGroup()
        
        # Randomly assign points (80% training, 20% test)
        all_points = list(data_points)
        np.random.shuffle(all_points)
        
        for i, point in enumerate(all_points):
            if i < 80:  # 80% to training
                new_point = point.copy()
                new_point.set_color(CONFIG["colors"]["training_color"])
                training_points.add(new_point)
            else:  # 20% to test
                new_point = point.copy()
                new_point.set_color(CONFIG["colors"]["test_color"])
                test_points.add(new_point)

        # Position the split sets
        training_points.move_to([-3, -3, 0])
        test_points.move_to([3, -3, 0])

        training_label = Text("Training Set", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["training_color"])
        test_label = Text("Test Set", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["test_color"])
        
        training_label.next_to(training_points, UP)
        test_label.next_to(test_points, UP)

        self.play(
            FadeOut(data_points),
            FadeIn(training_points),
            FadeIn(test_points),
            Write(training_label),
            Write(test_label)
        )
        self.wait(2)

        # Show the problem
        problem_text = Text(
            "Problem: Test set might have very few positive examples!",
            font_size=CONFIG["font_sizes"]["text"],
            color=CONFIG["colors"]["warning_color"]
        ).next_to(split_title, DOWN, buff=1)
        
        self.play(Write(problem_text))
        self.wait(3)
        
        self.play(FadeOut(VGroup(title, dataset_title, distribution_text, split_title, training_points, test_points, training_label, test_label, problem_text)))

    def show_stratified_solution(self):
        """Shows how stratified sampling solves the problem."""
        title = Text("The Solution: Stratified Sampling", font_size=CONFIG["font_sizes"]["header"]).to_edge(UP)
        self.play(Write(title))

        # Show the process
        process_title = Text("Stratified Sampling Process", font_size=CONFIG["font_sizes"]["text"])
        process_title.move_to([0, 1, 0])

        steps = VGroup(
            Text("1. Separate data by target class", font_size=CONFIG["font_sizes"]["text"]),
            Text("2. Split each class independently", font_size=CONFIG["font_sizes"]["text"]),
            Text("3. Combine to form training and test sets", font_size=CONFIG["font_sizes"]["text"])
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        steps.move_to([0, 0, 0])

        self.play(Write(process_title))
        self.play(Write(steps))
        self.wait(3)

        # Show visual example
        self.show_stratified_visual_example()

    def show_stratified_visual_example(self):
        """Shows a visual example of stratified sampling."""
        # Clear previous content
        self.clear()
        
        title = Text("Stratified Sampling Example", font_size=CONFIG["font_sizes"]["header"]).to_edge(UP)
        self.play(Write(title))

        # Step 1: Show original data separated by class
        step1_title = Text("Step 1: Separate by Target Class", font_size=CONFIG["font_sizes"]["text"])
        step1_title.move_to([0, 1, 0])

        # Negative class (left)
        negative_points = VGroup()
        for i in range(80):
            point = Circle(radius=0.06, fill_color=CONFIG["colors"]["negative_color"], fill_opacity=0.8)
            x = np.random.uniform(-4, -1)
            y = np.random.uniform(-1, 1)
            point.move_to([x, y, 0])
            negative_points.add(point)

        # Positive class (right)
        positive_points = VGroup()
        for i in range(20):
            point = Circle(radius=0.06, fill_color=CONFIG["colors"]["positive_color"], fill_opacity=0.8)
            x = np.random.uniform(1, 4)
            y = np.random.uniform(-1, 1)
            point.move_to([x, y, 0])
            positive_points.add(point)

        negative_label = Text("Negative Class (80)", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["negative_color"])
        positive_label = Text("Positive Class (20)", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["positive_color"])
        
        negative_label.next_to(negative_points, UP)
        positive_label.next_to(positive_points, UP)

        self.play(Write(step1_title))
        self.play(FadeIn(negative_points), FadeIn(positive_points))
        self.play(Write(negative_label), Write(positive_label))
        self.wait(2)

        # Step 2: Show splitting within each class
        step2_title = Text("Step 2: Split Each Class 80/20", font_size=CONFIG["font_sizes"]["text"])
        step2_title.move_to([0, 1, 0])

        # Split negative class
        neg_training = VGroup()
        neg_test = VGroup()
        neg_points_list = list(negative_points)
        np.random.shuffle(neg_points_list)
        
        for i, point in enumerate(neg_points_list):
            if i < 64:  # 80% of 80 = 64
                new_point = point.copy().set_color(CONFIG["colors"]["training_color"])
                neg_training.add(new_point)
            else:  # 20% of 80 = 16
                new_point = point.copy().set_color(CONFIG["colors"]["test_color"])
                neg_test.add(new_point)

        # Split positive class
        pos_training = VGroup()
        pos_test = VGroup()
        pos_points_list = list(positive_points)
        np.random.shuffle(pos_points_list)
        
        for i, point in enumerate(pos_points_list):
            if i < 16:  # 80% of 20 = 16
                new_point = point.copy().set_color(CONFIG["colors"]["training_color"])
                pos_training.add(new_point)
            else:  # 20% of 20 = 4
                new_point = point.copy().set_color(CONFIG["colors"]["test_color"])
                pos_test.add(new_point)

        # Position the split sets
        neg_training.move_to([-3, -2, 0])
        neg_test.move_to([-1, -2, 0])
        pos_training.move_to([1, -2, 0])
        pos_test.move_to([3, -2, 0])

        self.play(
            ReplacementTransform(step1_title, step2_title),
            FadeOut(negative_points), FadeOut(positive_points),
            FadeOut(negative_label), FadeOut(positive_label),
            FadeIn(neg_training), FadeIn(neg_test),
            FadeIn(pos_training), FadeIn(pos_test)
        )
        self.wait(2)

        # Step 3: Combine into final sets
        step3_title = Text("Step 3: Combine into Training and Test Sets", font_size=CONFIG["font_sizes"]["text"])
        step3_title.move_to([0, 1, 0])

        # Combine training sets
        final_training = VGroup(neg_training.copy(), pos_training.copy())
        final_training.arrange(RIGHT, buff=0.5)
        final_training.move_to([-2, -3, 0])

        # Combine test sets
        final_test = VGroup(neg_test.copy(), pos_test.copy())
        final_test.arrange(RIGHT, buff=0.5)
        final_test.move_to([2, -3, 0])

        final_train_label = Text("Training Set (80 samples)", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["training_color"])
        final_test_label = Text("Test Set (20 samples)", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["test_color"])
        
        final_train_label.next_to(final_training, UP)
        final_test_label.next_to(final_test, UP)

        self.play(
            ReplacementTransform(step2_title, step3_title),
            FadeOut(neg_training), FadeOut(neg_test),
            FadeOut(pos_training), FadeOut(pos_test),
            FadeIn(final_training), FadeIn(final_test),
            Write(final_train_label), Write(final_test_label)
        )
        self.wait(3)

        # Show the result
        result_text = Text(
            "Result: Both sets maintain the original 80/20 distribution!",
            font_size=CONFIG["font_sizes"]["text"],
            color=CONFIG["colors"]["success_color"]
        ).next_to(step3_title, DOWN, buff=1)
        
        self.play(Write(result_text))
        self.wait(3)
        
        self.play(FadeOut(VGroup(title, step3_title, final_training, final_test, final_train_label, final_test_label, result_text)))

    def show_comparison(self):
        """Shows a side-by-side comparison of random vs stratified splitting."""
        title = Text("Random vs Stratified Splitting", font_size=CONFIG["font_sizes"]["header"]).to_edge(UP)
        self.play(Write(title))

        # Random splitting side
        random_title = Text("Random Splitting", font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["warning_color"])
        random_title.move_to([-3, 1, 0])

        # Show potential bad outcome
        random_training = VGroup()
        random_test = VGroup()
        
        # Create a bad random split (all positives in training, none in test)
        for i in range(80):
            point = Circle(radius=0.05, fill_color=CONFIG["colors"]["training_color"], fill_opacity=0.8)
            x = np.random.uniform(-4, -2)
            y = np.random.uniform(-1, 1)
            point.move_to([x, y, 0])
            random_training.add(point)
        
        for i in range(20):
            point = Circle(radius=0.05, fill_color=CONFIG["colors"]["positive_color"], fill_opacity=0.8)
            x = np.random.uniform(-4, -2)
            y = np.random.uniform(-1, 1)
            point.move_to([x, y, 0])
            random_training.add(point)

        for i in range(20):
            point = Circle(radius=0.05, fill_color=CONFIG["colors"]["test_color"], fill_opacity=0.8)
            x = np.random.uniform(-2, 0)
            y = np.random.uniform(-1, 1)
            point.move_to([x, y, 0])
            random_test.add(point)

        random_train_label = Text("Training: 100 samples", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["training_color"])
        random_test_label = Text("Test: 20 samples (0 positive)", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["test_color"])
        
        random_train_label.next_to(random_training, UP)
        random_test_label.next_to(random_test, UP)

        # Stratified splitting side
        stratified_title = Text("Stratified Splitting", font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["success_color"])
        stratified_title.move_to([3, 1, 0])

        stratified_training = VGroup()
        stratified_test = VGroup()
        
        # Create balanced stratified split
        for i in range(64):
            point = Circle(radius=0.05, fill_color=CONFIG["colors"]["training_color"], fill_opacity=0.8)
            x = np.random.uniform(2, 4)
            y = np.random.uniform(-1, 1)
            point.move_to([x, y, 0])
            stratified_training.add(point)
        
        for i in range(16):
            point = Circle(radius=0.05, fill_color=CONFIG["colors"]["positive_color"], fill_opacity=0.8)
            x = np.random.uniform(2, 4)
            y = np.random.uniform(-1, 1)
            point.move_to([x, y, 0])
            stratified_training.add(point)

        for i in range(16):
            point = Circle(radius=0.05, fill_color=CONFIG["colors"]["test_color"], fill_opacity=0.8)
            x = np.random.uniform(4, 6)
            y = np.random.uniform(-1, 1)
            point.move_to([x, y, 0])
            stratified_test.add(point)
        
        for i in range(4):
            point = Circle(radius=0.05, fill_color=CONFIG["colors"]["positive_color"], fill_opacity=0.8)
            x = np.random.uniform(4, 6)
            y = np.random.uniform(-1, 1)
            point.move_to([x, y, 0])
            stratified_test.add(point)

        stratified_train_label = Text("Training: 80 samples", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["training_color"])
        stratified_test_label = Text("Test: 20 samples (4 positive)", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["test_color"])
        
        stratified_train_label.next_to(stratified_training, UP)
        stratified_test_label.next_to(stratified_test, UP)

        self.play(
            Write(random_title), Write(stratified_title),
            FadeIn(random_training), FadeIn(random_test),
            FadeIn(stratified_training), FadeIn(stratified_test),
            Write(random_train_label), Write(random_test_label),
            Write(stratified_train_label), Write(stratified_test_label)
        )
        self.wait(3)

        # Show the key difference
        difference_text = Text(
            "Key Difference: Stratified ensures test set has positive examples!",
            font_size=CONFIG["font_sizes"]["text"],
            color=CONFIG["colors"]["success_color"]
        ).next_to(title, DOWN, buff=1)
        
        self.play(Write(difference_text))
        self.wait(3)
        
        self.play(FadeOut(VGroup(title, random_title, stratified_title, random_training, random_test, stratified_training, stratified_test, random_train_label, random_test_label, stratified_train_label, stratified_test_label, difference_text)))

    def show_why_it_matters(self):
        """Explains why stratified sampling matters for model evaluation."""
        title = Text("Why Stratified Sampling Matters", font_size=CONFIG["font_sizes"]["header"]).to_edge(UP)
        self.play(Write(title))

        reasons = VGroup(
            Text("1. Model Evaluation", font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["positive_color"]),
            Text("   • Test set must represent real-world data", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["secondary_text"]),
            Text("   • Need examples of all classes to evaluate performance", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["secondary_text"]),
            Text(""),
            Text("2. Performance Metrics", font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["positive_color"]),
            Text("   • Can't calculate precision/recall without positive examples", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["secondary_text"]),
            Text("   • F1-score requires both classes in test set", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["secondary_text"]),
            Text(""),
            Text("3. Model Generalization", font_size=CONFIG["font_sizes"]["text"], color=CONFIG["colors"]["positive_color"]),
            Text("   • Ensures model learns from all classes", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["secondary_text"]),
            Text("   • Prevents bias towards majority class", font_size=CONFIG["font_sizes"]["label"], color=CONFIG["colors"]["secondary_text"])
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        reasons.move_to([0, 0, 0])

        self.play(LaggedStart(*[Write(reason) for reason in reasons], lag_ratio=0.5))
        self.wait(4)
        
        self.play(FadeOut(VGroup(title, reasons)))

    def show_summary(self):
        """Summarizes the key takeaways."""
        title = Text("Summary", font_size=CONFIG["font_sizes"]["title"]).to_edge(UP)
        self.play(Write(title))

        summary_points = VGroup(
            Text("Stratified Sampling Ensures:", font_size=CONFIG["font_sizes"]["text"]),
            VGroup(
                Dot(color=CONFIG["colors"]["success_color"]),
                Text("Representative distribution of target variable", font_size=CONFIG["font_sizes"]["text"])
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Dot(color=CONFIG["colors"]["success_color"]),
                Text("Both training and test sets have all classes", font_size=CONFIG["font_sizes"]["text"])
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Dot(color=CONFIG["colors"]["success_color"]),
                Text("Reliable model evaluation and performance metrics", font_size=CONFIG["font_sizes"]["text"])
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Dot(color=CONFIG["colors"]["success_color"]),
                Text("Better generalization to real-world data", font_size=CONFIG["font_sizes"]["text"])
            ).arrange(RIGHT, buff=0.2)
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT).next_to(title, DOWN, buff=1)

        self.play(LaggedStart(*[FadeIn(point, shift=UP) for point in summary_points], lag_ratio=0.7))
        self.wait(3)

        final_note = Text(
            "Remember: Stratify based on the TARGET variable, not predictors!",
            font_size=CONFIG["font_sizes"]["text"],
            color=CONFIG["colors"]["warning_color"]
        ).next_to(summary_points, DOWN, buff=1)
        self.play(Write(final_note))
        self.wait(4)
        self.play(FadeOut(VGroup(title, summary_points, final_note)))
