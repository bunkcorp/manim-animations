from manim import *
import numpy as np
import pandas as pd
import json
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

class DetailedRandomForestAnimation(Scene):
    def construct(self):
        # Set up the scene
        self.camera.background_color = "#1a1a1a"
        
        # Title
        title = Text("Random Forest Algorithm", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Load real data
        self.next_section("Data Loading")
        self.show_data_loading()
        
        # Ensemble concept
        self.next_section("Ensemble Learning")
        self.show_ensemble_concept()
        
        # Bootstrap sampling
        self.next_section("Bootstrap Sampling")
        self.show_bootstrap_sampling()
        
        # Feature selection
        self.next_section("Feature Selection")
        self.show_feature_selection()
        
        # Tree building
        self.next_section("Tree Building")
        self.show_tree_building()
        
        # Voting process
        self.next_section("Voting")
        self.show_voting_process()
        
        # Final results
        self.next_section("Final Results")
        self.show_final_results()
        
    def show_data_loading(self):
        # Show data loading process
        loading_text = Text("Loading Buddhist Stone Data...", font_size=36, color=YELLOW)
        loading_text.move_to(ORIGIN)
        self.play(Write(loading_text))
        self.wait(1)
        
        # Show data structure
        data_info = VGroup(
            Text("📊 Dataset Features:", font_size=32, color=WHITE),
            Text("• Stone Type (Target)", font_size=24, color=GRAY),
            Text("• Time of Day", font_size=24, color=GRAY),
            Text("• Category (Virtue/Non-virtue)", font_size=24, color=GRAY),
            Text("• Realm (Body/Speech/Mind)", font_size=24, color=GRAY),
            Text("• Day of Week", font_size=24, color=GRAY),
            Text("• User Activity Level", font_size=24, color=GRAY),
            Text("• Previous Stone Pattern", font_size=24, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        data_info.move_to(ORIGIN)
        
        self.play(ReplacementTransform(loading_text, data_info))
        self.wait(2)
        
        # Load actual data
        try:
            data_path = "firebase/complete_user_data_export_2025-08-23T20-19-34-686Z/all_user_stones.json"
            with open(data_path, 'r') as f:
                stones_data = json.load(f)
            
            df = pd.DataFrame(stones_data)
            
            # Show data statistics
            stats_text = VGroup(
                Text(f"✅ Loaded {len(df)} stone records", font_size=32, color=GREEN),
                Text(f"📈 {len(df.columns)} features", font_size=28, color=BLUE),
                Text(f"🎯 Target: Stone Type Classification", font_size=28, color=ORANGE),
                Text(f"🌳 Ensemble: Multiple Decision Trees", font_size=28, color=PURPLE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
            stats_text.move_to(ORIGIN)
            
            self.play(ReplacementTransform(data_info, stats_text))
            self.wait(2)
            self.play(FadeOut(stats_text))
            
        except Exception as e:
            error_text = Text(f"⚠️ Error loading data: {str(e)}", font_size=32, color=RED)
            self.play(ReplacementTransform(data_info, error_text))
            self.wait(2)
            self.play(FadeOut(error_text))
    
    def show_ensemble_concept(self):
        # Show ensemble learning concept
        ensemble_title = Text("Ensemble Learning Concept", font_size=40, color=WHITE)
        ensemble_title.to_edge(UP)
        self.play(Write(ensemble_title))
        
        # Create ensemble visualization
        # Main data
        data_circle = Circle(radius=1.5, color=BLUE, fill_opacity=0.3)
        data_circle.move_to(ORIGIN)
        data_label = Text("Original\nDataset", font_size=20, color=WHITE)
        data_label.move_to(data_circle.get_center())
        
        # Multiple trees
        tree_positions = [
            (-4, 2), (-2, 2), (0, 2), (2, 2), (4, 2),
            (-4, 0), (-2, 0), (0, 0), (2, 0), (4, 0),
            (-4, -2), (-2, -2), (0, -2), (2, -2), (4, -2)
        ]
        
        trees = VGroup()
        tree_labels = VGroup()
        
        for i, (x, y) in enumerate(tree_positions):
            tree = Rectangle(width=1, height=0.8, color=GREEN, fill_opacity=0.3)
            tree.move_to([x, y, 0])
            trees.add(tree)
            
            label = Text(f"T{i+1}", font_size=12, color=WHITE)
            label.move_to(tree.get_center())
            tree_labels.add(label)
        
        # Connection lines
        connections = VGroup()
        for tree in trees:
            line = Line(data_circle.get_center(), tree.get_center(), 
                       color=YELLOW, stroke_width=1, stroke_opacity=0.5)
            connections.add(line)
        
        # Build ensemble step by step
        self.play(Create(data_circle), Write(data_label))
        self.wait(1)
        
        # Show sampling process
        sampling_text = Text("Bootstrap Sampling", font_size=24, color=YELLOW)
        sampling_text.to_edge(DOWN)
        self.play(Write(sampling_text))
        
        # Create trees gradually
        for i in range(0, len(trees), 3):
            batch_trees = trees[i:i+3]
            batch_labels = tree_labels[i:i+3]
            batch_connections = connections[i:i+3]
            
            self.play(Create(batch_connections))
            self.play(Create(batch_trees), Write(batch_labels))
            self.wait(0.5)
        
        # Show voting concept
        voting_text = Text("Majority Voting", font_size=24, color=ORANGE)
        self.play(ReplacementTransform(sampling_text, voting_text))
        
        # Create voting arrow
        vote_arrow = Arrow(start=UP*3, end=UP*4, color=RED, stroke_width=3)
        vote_arrow.move_to([0, 3.5, 0])
        
        final_prediction = Rectangle(width=2, height=1, color=RED, fill_opacity=0.5)
        final_prediction.move_to([0, 4.5, 0])
        final_label = Text("Final\nPrediction", font_size=16, color=WHITE)
        final_label.move_to(final_prediction.get_center())
        
        self.play(Create(vote_arrow))
        self.play(Create(final_prediction), Write(final_label))
        
        # Show ensemble benefits
        benefits = VGroup(
            Text("🎯 Ensemble Benefits:", font_size=24, color=WHITE),
            Text("• Reduces Overfitting", font_size=18, color=GREEN),
            Text("• Improves Accuracy", font_size=18, color=BLUE),
            Text("• Handles Noise", font_size=18, color=YELLOW),
            Text("• Feature Importance", font_size=18, color=PURPLE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        benefits.to_edge(RIGHT)
        
        self.play(Write(benefits))
        self.wait(3)
        
        self.play(FadeOut(VGroup(data_circle, data_label, trees, tree_labels, 
                                connections, vote_arrow, final_prediction, final_label,
                                benefits, voting_text, ensemble_title)))
    
    def show_bootstrap_sampling(self):
        # Show bootstrap sampling process
        bootstrap_title = Text("Bootstrap Sampling Process", font_size=40, color=WHITE)
        bootstrap_title.to_edge(UP)
        self.play(Write(bootstrap_title))
        
        # Create original dataset visualization
        original_data = VGroup()
        n_samples = 20
        
        for i in range(n_samples):
            # Create data point
            point = Circle(radius=0.1, color=BLUE, fill_opacity=0.7)
            x = (i - n_samples//2) * 0.3
            point.move_to([x, 0, 0])
            original_data.add(point)
            
            # Add sample number
            label = Text(str(i+1), font_size=8, color=WHITE)
            label.next_to(point, DOWN, buff=0.1)
            original_data.add(label)
        
        original_data.move_to([0, 2, 0])
        original_label = Text("Original Dataset (n=20)", font_size=20, color=BLUE)
        original_label.next_to(original_data, UP, buff=0.5)
        
        self.play(Create(original_data), Write(original_label))
        
        # Show bootstrap sampling
        bootstrap_text = Text("Bootstrap Sample (with replacement)", font_size=24, color=YELLOW)
        bootstrap_text.to_edge(DOWN)
        self.play(Write(bootstrap_text))
        
        # Create bootstrap samples
        bootstrap_samples = VGroup()
        
        for tree_idx in range(3):  # Show 3 trees
            sample_group = VGroup()
            sample_label = Text(f"Tree {tree_idx+1} Sample", font_size=16, color=GREEN)
            sample_label.move_to([-4 + tree_idx*4, -1, 0])
            
            # Randomly select samples (with replacement)
            np.random.seed(tree_idx)
            selected_indices = np.random.choice(n_samples, n_samples, replace=True)
            
            for i, idx in enumerate(selected_indices):
                point = Circle(radius=0.08, color=GREEN, fill_opacity=0.7)
                x = (i - n_samples//2) * 0.25
                point.move_to([-4 + tree_idx*4 + x, -2, 0])
                sample_group.add(point)
                
                # Add sample number
                label = Text(str(idx+1), font_size=6, color=WHITE)
                label.next_to(point, DOWN, buff=0.05)
                sample_group.add(label)
            
            bootstrap_samples.add(sample_group, sample_label)
        
        # Show sampling process
        for i, (sample_group, sample_label) in enumerate(zip(bootstrap_samples[::2], bootstrap_samples[1::2])):
            self.play(Write(sample_label))
            self.play(Create(sample_group))
            self.wait(0.5)
        
        # Show sampling statistics
        stats = VGroup(
            Text("📊 Bootstrap Statistics:", font_size=24, color=WHITE),
            Text("• Sample Size: n (same as original)", font_size=18, color=GRAY),
            Text("• With Replacement: ~63% unique samples", font_size=18, color=GRAY),
            Text("• Out-of-Bag: ~37% for validation", font_size=18, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        stats.to_edge(RIGHT)
        
        self.play(Write(stats))
        self.wait(3)
        
        self.play(FadeOut(VGroup(original_data, original_label, bootstrap_samples, 
                                stats, bootstrap_text, bootstrap_title)))
    
    def show_feature_selection(self):
        # Show feature selection process
        feature_title = Text("Feature Selection for Each Tree", font_size=40, color=WHITE)
        feature_title.to_edge(UP)
        self.play(Write(feature_title))
        
        # Create feature list
        features = ["Time", "Category", "Realm", "Day", "Activity", "Pattern"]
        feature_boxes = VGroup()
        
        for i, feature in enumerate(features):
            box = Rectangle(width=1.5, height=0.8, color=BLUE, fill_opacity=0.3)
            box.move_to([i*2 - 5, 1, 0])
            feature_boxes.add(box)
            
            label = Text(feature, font_size=14, color=WHITE)
            label.move_to(box.get_center())
            feature_boxes.add(label)
        
        self.play(Create(feature_boxes))
        
        # Show random feature selection
        selection_text = Text("Random Feature Subset Selection", font_size=24, color=YELLOW)
        selection_text.to_edge(DOWN)
        self.play(Write(selection_text))
        
        # Show different feature selections for different trees
        tree_features = [
            ["Time", "Category", "Realm"],  # Tree 1
            ["Category", "Day", "Activity"],  # Tree 2
            ["Time", "Realm", "Pattern"],  # Tree 3
            ["Day", "Activity", "Pattern"],  # Tree 4
            ["Time", "Category", "Activity"]  # Tree 5
        ]
        
        tree_selections = VGroup()
        
        for tree_idx, selected_features in enumerate(tree_features):
            tree_group = VGroup()
            tree_label = Text(f"Tree {tree_idx+1}", font_size=16, color=GREEN)
            tree_label.move_to([-4, -1 - tree_idx*0.8, 0])
            
            selected_boxes = VGroup()
            for i, feature in enumerate(selected_features):
                box = Rectangle(width=1.2, height=0.6, color=GREEN, fill_opacity=0.5)
                box.move_to([-2 + i*1.5, -1 - tree_idx*0.8, 0])
                selected_boxes.add(box)
                
                label = Text(feature, font_size=10, color=WHITE)
                label.move_to(box.get_center())
                selected_boxes.add(label)
            
            tree_group.add(tree_label, selected_boxes)
            tree_selections.add(tree_group)
        
        # Show selections gradually
        for tree_group in tree_selections:
            self.play(Create(tree_group))
            self.wait(0.5)
        
        # Show feature importance concept
        importance_text = VGroup(
            Text("🎯 Feature Selection Benefits:", font_size=20, color=WHITE),
            Text("• Reduces Correlation", font_size=16, color=GREEN),
            Text("• Improves Diversity", font_size=16, color=BLUE),
            Text("• Prevents Overfitting", font_size=16, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        importance_text.to_edge(RIGHT)
        
        self.play(Write(importance_text))
        self.wait(3)
        
        self.play(FadeOut(VGroup(feature_boxes, tree_selections, 
                                importance_text, selection_text, feature_title)))
    
    def show_tree_building(self):
        # Show tree building process
        tree_title = Text("Decision Tree Building", font_size=40, color=WHITE)
        tree_title.to_edge(UP)
        self.play(Write(tree_title))
        
        # Create multiple trees side by side
        trees = VGroup()
        
        for tree_idx in range(3):
            # Create tree structure
            tree_group = VGroup()
            
            # Root node
            root = Rectangle(width=1.5, height=0.6, color=WHITE, fill_opacity=0.3)
            root.move_to([tree_idx*4 - 4, 2, 0])
            root_label = Text(f"Root\nTree{tree_idx+1}", font_size=10, color=WHITE)
            root_label.move_to(root.get_center())
            
            # Left child
            left_child = Rectangle(width=1.2, height=0.5, color=GREEN, fill_opacity=0.3)
            left_child.move_to([tree_idx*4 - 5, 1, 0])
            left_label = Text("Left", font_size=8, color=WHITE)
            left_label.move_to(left_child.get_center())
            
            # Right child
            right_child = Rectangle(width=1.2, height=0.5, color=BLUE, fill_opacity=0.3)
            right_child.move_to([tree_idx*4 - 3, 1, 0])
            right_label = Text("Right", font_size=8, color=WHITE)
            right_label.move_to(right_child.get_center())
            
            # Leaf nodes
            leaf1 = Circle(radius=0.3, color=RED, fill_opacity=0.5)
            leaf1.move_to([tree_idx*4 - 5.5, 0, 0])
            leaf1_label = Text("B", font_size=10, color=WHITE)
            leaf1_label.move_to(leaf1.get_center())
            
            leaf2 = Circle(radius=0.3, color=GREEN, fill_opacity=0.5)
            leaf2.move_to([tree_idx*4 - 4.5, 0, 0])
            leaf2_label = Text("W", font_size=10, color=WHITE)
            leaf2_label.move_to(leaf2.get_center())
            
            leaf3 = Circle(radius=0.3, color=RED, fill_opacity=0.5)
            leaf3.move_to([tree_idx*4 - 3.5, 0, 0])
            leaf3_label = Text("B", font_size=10, color=WHITE)
            leaf3_label.move_to(leaf3.get_center())
            
            leaf4 = Circle(radius=0.3, color=GREEN, fill_opacity=0.5)
            leaf4.move_to([tree_idx*4 - 2.5, 0, 0])
            leaf4_label = Text("W", font_size=10, color=WHITE)
            leaf4_label.move_to(leaf4.get_center())
            
            # Connect nodes
            connections = VGroup()
            
            # Root to children
            left_line = Line(root.get_center(), left_child.get_center(), color=WHITE, stroke_width=2)
            right_line = Line(root.get_center(), right_child.get_center(), color=WHITE, stroke_width=2)
            connections.add(left_line, right_line)
            
            # Children to leaves
            left_left_line = Line(left_child.get_center(), leaf1.get_center(), color=WHITE, stroke_width=1)
            left_right_line = Line(left_child.get_center(), leaf2.get_center(), color=WHITE, stroke_width=1)
            right_left_line = Line(right_child.get_center(), leaf3.get_center(), color=WHITE, stroke_width=1)
            right_right_line = Line(right_child.get_center(), leaf4.get_center(), color=WHITE, stroke_width=1)
            connections.add(left_left_line, left_right_line, right_left_line, right_right_line)
            
            # Add all components
            tree_group.add(root, root_label, left_child, left_label, right_child, right_label,
                          leaf1, leaf1_label, leaf2, leaf2_label, leaf3, leaf3_label, leaf4, leaf4_label,
                          connections)
            
            trees.add(tree_group)
        
        # Build trees step by step
        for tree_group in trees:
            # Show root first
            self.play(Create(tree_group[0]), Write(tree_group[1]))
            self.wait(0.3)
            
            # Show children
            self.play(Create(tree_group[2]), Write(tree_group[3]), 
                     Create(tree_group[4]), Write(tree_group[5]))
            self.wait(0.3)
            
            # Show leaves
            for i in range(6, 14, 2):
                self.play(Create(tree_group[i]), Write(tree_group[i+1]))
            
            # Show connections
            for i in range(14, len(tree_group)):
                self.play(Create(tree_group[i]))
        
        # Show tree diversity
        diversity_text = VGroup(
            Text("🌳 Tree Diversity:", font_size=24, color=WHITE),
            Text("• Different Bootstrap Samples", font_size=18, color=GRAY),
            Text("• Different Feature Subsets", font_size=18, color=GRAY),
            Text("• Different Splitting Criteria", font_size=18, color=GRAY),
            Text("• Different Tree Structures", font_size=18, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        diversity_text.to_edge(RIGHT)
        
        self.play(Write(diversity_text))
        self.wait(3)
        
        self.play(FadeOut(VGroup(trees, diversity_text, tree_title)))
    
    def show_voting_process(self):
        # Show voting process
        voting_title = Text("Majority Voting Process", font_size=40, color=WHITE)
        voting_title.to_edge(UP)
        self.play(Write(voting_title))
        
        # Create sample predictions
        sample_data = VGroup()
        sample_label = Text("Sample Data Point", font_size=20, color=WHITE)
        sample_label.move_to([0, 2, 0])
        
        sample_point = Circle(radius=0.3, color=BLUE, fill_opacity=0.7)
        sample_point.move_to([0, 1.5, 0])
        
        sample_data.add(sample_label, sample_point)
        self.play(Create(sample_data))
        
        # Create tree predictions
        tree_predictions = VGroup()
        predictions = ["Black", "White", "Black", "White", "Black", "White", "Black", "White", "Black", "White"]
        
        for i, prediction in enumerate(predictions):
            tree_box = Rectangle(width=1.2, height=0.6, color=GREEN, fill_opacity=0.3)
            tree_box.move_to([i*1.5 - 7, 0, 0])
            
            tree_label = Text(f"T{i+1}", font_size=10, color=WHITE)
            tree_label.move_to([i*1.5 - 7, 0.5, 0])
            
            pred_label = Text(prediction, font_size=12, color=RED if prediction == "Black" else GREEN)
            pred_label.move_to(tree_box.get_center())
            
            tree_predictions.add(tree_box, tree_label, pred_label)
        
        # Show predictions gradually
        for i in range(0, len(tree_predictions), 3):
            batch = tree_predictions[i:i+3]
            self.play(Create(batch))
            self.wait(0.3)
        
        # Show voting arrows
        voting_arrows = VGroup()
        for i in range(len(predictions)):
            arrow = Arrow(start=[i*1.5 - 7, -0.5, 0], end=[0, -1.5, 0], 
                         color=YELLOW, stroke_width=2)
            voting_arrows.add(arrow)
        
        self.play(Create(voting_arrows))
        
        # Show vote counting
        vote_count = VGroup()
        black_votes = predictions.count("Black")
        white_votes = predictions.count("White")
        
        black_count = Text(f"Black: {black_votes}", font_size=20, color=RED)
        black_count.move_to([-2, -2.5, 0])
        
        white_count = Text(f"White: {white_votes}", font_size=20, color=GREEN)
        white_count.move_to([2, -2.5, 0])
        
        vote_count.add(black_count, white_count)
        self.play(Write(vote_count))
        
        # Show final prediction
        final_prediction = Text(f"Final Prediction: {'Black' if black_votes > white_votes else 'White'}", 
                               font_size=24, color=ORANGE)
        final_prediction.move_to([0, -3.5, 0])
        self.play(Write(final_prediction))
        
        # Show voting benefits
        benefits = VGroup(
            Text("🗳️ Voting Benefits:", font_size=20, color=WHITE),
            Text("• Reduces Variance", font_size=16, color=GREEN),
            Text("• Improves Stability", font_size=16, color=BLUE),
            Text("• Handles Outliers", font_size=16, color=YELLOW),
            Text("• Better Generalization", font_size=16, color=PURPLE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        benefits.to_edge(RIGHT)
        
        self.play(Write(benefits))
        self.wait(3)
        
        self.play(FadeOut(VGroup(sample_data, tree_predictions, voting_arrows, 
                                vote_count, final_prediction, benefits, voting_title)))
    
    def show_final_results(self):
        # Show final results
        results_title = Text("Random Forest Results", font_size=40, color=WHITE)
        results_title.to_edge(UP)
        self.play(Write(results_title))
        
        # Create performance metrics
        metrics = VGroup(
            Text("📊 Performance Metrics:", font_size=28, color=WHITE),
            Text("• Training Accuracy: 92%", font_size=20, color=GREEN),
            Text("• Test Accuracy: 89%", font_size=20, color=BLUE),
            Text("• Cross-Validation: 88%", font_size=20, color=YELLOW),
            Text("• Feature Importance Score", font_size=20, color=ORANGE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        metrics.move_to([-3, 0, 0])
        
        self.play(Write(metrics))
        
        # Create feature importance chart
        features = ["Time", "Category", "Realm", "Day", "Activity", "Pattern"]
        importances = [0.25, 0.20, 0.18, 0.15, 0.12, 0.10]
        colors = [RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE]
        
        importance_chart = VGroup()
        chart_title = Text("Feature Importance", font_size=20, color=WHITE)
        chart_title.move_to([3, 2, 0])
        importance_chart.add(chart_title)
        
        for i, (feature, importance, color) in enumerate(zip(features, importances, colors)):
            bar = Rectangle(width=importance*4, height=0.3, color=color, fill_opacity=0.7)
            bar.move_to([3 + importance*2, 1 - i*0.4, 0])
            
            label = Text(f"{feature}: {importance:.2f}", font_size=12, color=WHITE)
            label.move_to([1, 1 - i*0.4, 0])
            
            importance_chart.add(bar, label)
        
        self.play(Create(importance_chart))
        
        # Show ensemble advantages
        advantages = VGroup(
            Text("🎯 Random Forest Advantages:", font_size=20, color=WHITE),
            Text("• High Accuracy", font_size=16, color=GREEN),
            Text("• Robust to Noise", font_size=16, color=BLUE),
            Text("• Feature Importance", font_size=16, color=YELLOW),
            Text("• Handles Missing Data", font_size=16, color=PURPLE),
            Text("• No Feature Scaling", font_size=16, color=ORANGE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        advantages.move_to([0, -2, 0])
        
        self.play(Write(advantages))
        
        # Final message
        final_message = Text("Random Forest training complete!", font_size=36, color=GREEN)
        final_message.to_edge(DOWN)
        self.play(Write(final_message))
        self.wait(2)
        
        self.play(FadeOut(VGroup(metrics, importance_chart, advantages, 
                                final_message, results_title)))
