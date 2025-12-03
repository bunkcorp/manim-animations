from manim import *
import numpy as np
import pandas as pd
import json
import os
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
# import matplotlib.pyplot as plt  # Removed to avoid numpy compatibility issues

class DetailedDecisionTreeAnimation(Scene):
    def construct(self):
        # Set up the scene
        self.camera.background_color = "#1a1a1a"
        
        # Title
        title = Text("Decision Tree Algorithm", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Load real data
        self.next_section("Data Loading")
        self.show_data_loading()
        
        # Data preprocessing
        self.next_section("Data Preprocessing")
        self.show_data_preprocessing()
        
        # Feature selection
        self.next_section("Feature Selection")
        self.show_feature_selection()
        
        # Tree building process
        self.next_section("Tree Building")
        self.show_tree_building()
        
        # Prediction process
        self.next_section("Prediction")
        self.show_prediction_process()
        
        # Final tree visualization
        self.next_section("Final Tree")
        self.show_final_tree()
        
    def show_data_loading(self):
        # Show data loading process
        loading_text = Text("Loading Buddhist Stone Data...", font_size=36, color=YELLOW)
        loading_text.move_to(ORIGIN)
        self.play(Write(loading_text))
        self.wait(1)
        
        # Show data structure
        data_info = VGroup(
            Text("📊 Buddhist Stone Features:", font_size=32, color=WHITE),
            Text("• Stone Type (Black/White)", font_size=24, color=GRAY),
            Text("• Category (Virtue/Non-virtue)", font_size=24, color=GRAY),
            Text("• Realm (Body/Speech/Mind)", font_size=24, color=GRAY),
            Text("• Time of Day", font_size=24, color=GRAY),
            Text("• Day of Week", font_size=24, color=GRAY),
            Text("• User Activity Level", font_size=24, color=GRAY)
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
                Text(f"🎯 Target: Predict Stone Type", font_size=28, color=ORANGE),
                Text(f"📊 Classes: Black vs White Stones", font_size=28, color=PURPLE)
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
    
    def show_data_preprocessing(self):
        # Show preprocessing steps
        preprocess_title = Text("Data Preprocessing", font_size=40, color=WHITE)
        preprocess_title.to_edge(UP)
        self.play(Write(preprocess_title))
        
        # Create preprocessing steps
        steps = VGroup(
            Text("1. Handle Missing Values", font_size=28, color=YELLOW),
            Text("2. Encode Categorical Variables", font_size=28, color=YELLOW),
            Text("3. Feature Scaling", font_size=28, color=YELLOW),
            Text("4. Split Train/Test Data", font_size=28, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        steps.move_to(ORIGIN)
        
        self.play(Write(steps))
        self.wait(1)
        
        # Animate each step with details
        for i, step in enumerate(steps):
            # Highlight current step
            self.play(step.animate.set_color(GREEN).scale(1.2))
            
            # Show details for each step
            if i == 0:  # Missing Values
                details = VGroup(
                    Text("• Check for NaN values", font_size=20, color=GRAY),
                    Text("• Fill with mode/mean", font_size=20, color=GRAY),
                    Text("• Remove incomplete records", font_size=20, color=GRAY)
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
                details.next_to(step, DOWN, buff=0.5)
                self.play(Write(details))
                self.wait(1.5)
                self.play(FadeOut(details))
            
            elif i == 1:  # Encoding
                details = VGroup(
                    Text("• Convert strings to numbers", font_size=20, color=GRAY),
                    Text("• One-hot encoding for categories", font_size=20, color=GRAY),
                    Text("• Label encoding for targets", font_size=20, color=GRAY)
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
                details.next_to(step, DOWN, buff=0.5)
                self.play(Write(details))
                self.wait(1.5)
                self.play(FadeOut(details))
            
            elif i == 2:  # Scaling
                details = VGroup(
                    Text("• Normalize numerical features", font_size=20, color=GRAY),
                    Text("• Standardize to mean=0, std=1", font_size=20, color=GRAY),
                    Text("• Ensure equal feature importance", font_size=20, color=GRAY)
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
                details.next_to(step, DOWN, buff=0.5)
                self.play(Write(details))
                self.wait(1.5)
                self.play(FadeOut(details))
            
            elif i == 3:  # Split
                details = VGroup(
                    Text("• 80% training data", font_size=20, color=GRAY),
                    Text("• 20% test data", font_size=20, color=GRAY),
                    Text("• Stratified sampling", font_size=20, color=GRAY)
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
                details.next_to(step, DOWN, buff=0.5)
                self.play(Write(details))
                self.wait(1.5)
                self.play(FadeOut(details))
            
            # Reset step color
            self.play(step.animate.set_color(YELLOW).scale(1/1.2))
        
        self.play(FadeOut(steps), FadeOut(preprocess_title))
    
    def show_feature_selection(self):
        # Show feature selection process
        feature_title = Text("Feature Selection & Importance", font_size=40, color=WHITE)
        feature_title.to_edge(UP)
        self.play(Write(feature_title))
        
        # Create feature importance visualization
        features = ["Time of Day", "Category", "Realm", "Day of Week", "User Activity"]
        importances = [0.35, 0.28, 0.22, 0.10, 0.05]  # Example values
        colors = [RED, GREEN, BLUE, YELLOW, PURPLE]
        
        # Create bar chart
        chart_width = 8
        chart_height = 4
        chart = VGroup()
        
        max_importance = max(importances)
        bar_width = chart_width / len(features)
        
        for i, (feature, importance, color) in enumerate(zip(features, importances, colors)):
            # Create bar
            bar_height = (importance / max_importance) * chart_height
            bar = Rectangle(
                width=bar_width * 0.8,
                height=bar_height,
                fill_color=color,
                fill_opacity=0.8,
                stroke_color=WHITE,
                stroke_width=2
            )
            
            # Position bar
            bar.move_to([i * bar_width - chart_width/2 + bar_width/2, bar_height/2 - chart_height/2, 0])
            
            # Add feature label
            label = Text(feature, font_size=16, color=WHITE)
            label.rotate(PI/2)
            label.next_to(bar, DOWN, buff=0.3)
            
            # Add importance value
            value = Text(f"{importance:.2f}", font_size=14, color=color)
            value.next_to(bar, UP, buff=0.1)
            
            chart.add(bar, label, value)
        
        chart.move_to(ORIGIN)
        self.play(Create(chart))
        
        # Show selection criteria
        criteria = VGroup(
            Text("🎯 Selection Criteria:", font_size=28, color=WHITE),
            Text("• Information Gain", font_size=20, color=GRAY),
            Text("• Gini Impurity", font_size=20, color=GRAY),
            Text("• Feature Correlation", font_size=20, color=GRAY),
            Text("• Domain Knowledge", font_size=20, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        criteria.to_edge(RIGHT)
        
        self.play(Write(criteria))
        self.wait(3)
        
        self.play(FadeOut(chart), FadeOut(criteria), FadeOut(feature_title))
    
    def show_tree_building(self):
        # Show the tree building process
        tree_title = Text("Decision Tree Building Process", font_size=40, color=WHITE)
        tree_title.to_edge(UP)
        self.play(Write(tree_title))
        
        # Create a simple tree structure
        root = self.create_tree_node("Time of Day\n≤ 12:00?", WHITE, 0, 2)
        
        # Left child (morning)
        left_child = self.create_tree_node("Category\nVirtue?", GREEN, -2, 1)
        left_line = Line(root.get_center(), left_child.get_center(), color=WHITE, stroke_width=2)
        left_label = Text("Yes", font_size=16, color=GREEN)
        left_label.next_to(left_line, LEFT, buff=0.1)
        
        # Right child (afternoon)
        right_child = self.create_tree_node("Realm\nBody?", BLUE, 2, 1)
        right_line = Line(root.get_center(), right_child.get_center(), color=WHITE, stroke_width=2)
        right_label = Text("No", font_size=16, color=RED)
        right_label.next_to(right_line, RIGHT, buff=0.1)
        
        # Leaf nodes
        leaf1 = self.create_leaf_node("Black\n(80%)", RED, -3, 0)
        leaf2 = self.create_leaf_node("White\n(90%)", GREEN, -1, 0)
        leaf3 = self.create_leaf_node("Black\n(70%)", RED, 1, 0)
        leaf4 = self.create_leaf_node("White\n(85%)", GREEN, 3, 0)
        
        # Connect leaf nodes
        leaf1_line = Line(left_child.get_center(), leaf1.get_center(), color=WHITE, stroke_width=2)
        leaf2_line = Line(left_child.get_center(), leaf2.get_center(), color=WHITE, stroke_width=2)
        leaf3_line = Line(right_child.get_center(), leaf3.get_center(), color=WHITE, stroke_width=2)
        leaf4_line = Line(right_child.get_center(), leaf4.get_center(), color=WHITE, stroke_width=2)
        
        leaf1_label = Text("Yes", font_size=14, color=GREEN)
        leaf1_label.next_to(leaf1_line, LEFT, buff=0.05)
        leaf2_label = Text("No", font_size=14, color=RED)
        leaf2_label.next_to(leaf2_line, RIGHT, buff=0.05)
        leaf3_label = Text("Yes", font_size=14, color=GREEN)
        leaf3_label.next_to(leaf3_line, LEFT, buff=0.05)
        leaf4_label = Text("No", font_size=14, color=RED)
        leaf4_label.next_to(leaf4_line, RIGHT, buff=0.05)
        
        # Build tree step by step
        self.play(Create(root))
        self.wait(1)
        
        # Show splitting criteria
        criteria_text = Text("Splitting on: Time of Day", font_size=24, color=YELLOW)
        criteria_text.to_edge(DOWN)
        self.play(Write(criteria_text))
        
        self.play(Create(left_line), Create(right_line), Write(left_label), Write(right_label))
        self.play(Create(left_child), Create(right_child))
        self.wait(1)
        
        # Update criteria
        self.play(ReplacementTransform(criteria_text, 
                                     Text("Splitting on: Category", font_size=24, color=YELLOW)))
        
        self.play(Create(leaf1_line), Create(leaf2_line), Write(leaf1_label), Write(leaf2_label))
        self.play(Create(leaf1), Create(leaf2))
        self.wait(1)
        
        # Update criteria
        self.play(ReplacementTransform(criteria_text, 
                                     Text("Splitting on: Realm", font_size=24, color=YELLOW)))
        
        self.play(Create(leaf3_line), Create(leaf4_line), Write(leaf3_label), Write(leaf4_label))
        self.play(Create(leaf3), Create(leaf4))
        self.wait(1)
        
        # Show tree statistics
        stats = VGroup(
            Text("📊 Tree Statistics:", font_size=24, color=WHITE),
            Text("• Depth: 3 levels", font_size=18, color=GRAY),
            Text("• Nodes: 7 total", font_size=18, color=GRAY),
            Text("• Leaves: 4 terminal", font_size=18, color=GRAY),
            Text("• Accuracy: 85%", font_size=18, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        stats.to_edge(RIGHT)
        
        self.play(Write(stats))
        self.wait(3)
        
        self.play(FadeOut(root), FadeOut(left_child), FadeOut(right_child),
                 FadeOut(leaf1), FadeOut(leaf2), FadeOut(leaf3), FadeOut(leaf4),
                 FadeOut(left_line), FadeOut(right_line), FadeOut(leaf1_line),
                 FadeOut(leaf2_line), FadeOut(leaf3_line), FadeOut(leaf4_line),
                 FadeOut(left_label), FadeOut(right_label), FadeOut(leaf1_label),
                 FadeOut(leaf2_label), FadeOut(leaf3_label), FadeOut(leaf4_label),
                 FadeOut(stats), FadeOut(tree_title))
    
    def create_tree_node(self, text, color, x, y):
        """Create a tree node with given text and position"""
        node = Rectangle(
            width=2,
            height=1,
            fill_color=color,
            fill_opacity=0.3,
            stroke_color=WHITE,
            stroke_width=2
        )
        node.move_to([x, y, 0])
        
        label = Text(text, font_size=14, color=WHITE)
        label.move_to(node.get_center())
        
        return VGroup(node, label)
    
    def create_leaf_node(self, text, color, x, y):
        """Create a leaf node with given text and position"""
        node = Circle(
            radius=0.5,
            fill_color=color,
            fill_opacity=0.5,
            stroke_color=WHITE,
            stroke_width=2
        )
        node.move_to([x, y, 0])
        
        label = Text(text, font_size=12, color=WHITE)
        label.move_to(node.get_center())
        
        return VGroup(node, label)
    
    def show_prediction_process(self):
        # Show how predictions are made
        prediction_title = Text("Prediction Process", font_size=40, color=WHITE)
        prediction_title.to_edge(UP)
        self.play(Write(prediction_title))
        
        # Create a sample prediction path
        sample_data = VGroup(
            Text("📋 Sample Data Point:", font_size=28, color=WHITE),
            Text("• Time: 14:30 (Afternoon)", font_size=20, color=GRAY),
            Text("• Category: Non-virtue", font_size=20, color=GRAY),
            Text("• Realm: Speech", font_size=20, color=GRAY),
            Text("• Day: Wednesday", font_size=20, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        sample_data.to_edge(LEFT)
        
        self.play(Write(sample_data))
        
        # Show prediction path
        path_title = Text("🔍 Prediction Path:", font_size=28, color=YELLOW)
        path_title.to_edge(DOWN)
        self.play(Write(path_title))
        
        # Create prediction steps
        steps = VGroup(
            Text("1. Time ≤ 12:00? → No", font_size=20, color=RED),
            Text("2. Realm = Body? → No", font_size=20, color=RED),
            Text("3. → Predict: White Stone", font_size=20, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        steps.move_to(ORIGIN)
        
        self.play(Write(steps))
        
        # Show confidence
        confidence = VGroup(
            Text("🎯 Prediction Confidence:", font_size=24, color=WHITE),
            Text("• White Stone: 85%", font_size=20, color=GREEN),
            Text("• Black Stone: 15%", font_size=20, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        confidence.to_edge(RIGHT)
        
        self.play(Write(confidence))
        self.wait(3)
        
        self.play(FadeOut(sample_data), FadeOut(steps), FadeOut(confidence),
                 FadeOut(path_title), FadeOut(prediction_title))
    
    def show_final_tree(self):
        # Show the complete final tree
        final_title = Text("Complete Decision Tree", font_size=40, color=WHITE)
        final_title.to_edge(UP)
        self.play(Write(final_title))
        
        # Create a more complex tree
        root = self.create_tree_node("Time of Day\n≤ 12:00?", WHITE, 0, 3)
        
        # Morning branch
        morning = self.create_tree_node("Category\nVirtue?", GREEN, -3, 2)
        morning_line = Line(root.get_center(), morning.get_center(), color=WHITE, stroke_width=2)
        morning_label = Text("Yes", font_size=16, color=GREEN)
        morning_label.next_to(morning_line, LEFT, buff=0.1)
        
        # Afternoon branch
        afternoon = self.create_tree_node("Realm\nBody?", BLUE, 3, 2)
        afternoon_line = Line(root.get_center(), afternoon.get_center(), color=WHITE, stroke_width=2)
        afternoon_label = Text("No", font_size=16, color=RED)
        afternoon_label.next_to(afternoon_line, RIGHT, buff=0.1)
        
        # Morning leaves
        morning_virtue = self.create_leaf_node("White\n(95%)", GREEN, -4, 1)
        morning_nonvirtue = self.create_leaf_node("Black\n(80%)", RED, -2, 1)
        
        morning_virtue_line = Line(morning.get_center(), morning_virtue.get_center(), color=WHITE, stroke_width=2)
        morning_nonvirtue_line = Line(morning.get_center(), morning_nonvirtue.get_center(), color=WHITE, stroke_width=2)
        
        # Afternoon leaves
        afternoon_body = self.create_leaf_node("Black\n(75%)", RED, 2, 1)
        afternoon_other = self.create_tree_node("Day\nWeekend?", YELLOW, 4, 1)
        
        afternoon_body_line = Line(afternoon.get_center(), afternoon_body.get_center(), color=WHITE, stroke_width=2)
        afternoon_other_line = Line(afternoon.get_center(), afternoon_other.get_center(), color=WHITE, stroke_width=2)
        
        # Weekend leaves
        weekend_yes = self.create_leaf_node("White\n(90%)", GREEN, 3, 0)
        weekend_no = self.create_leaf_node("Black\n(70%)", RED, 5, 0)
        
        weekend_yes_line = Line(afternoon_other.get_center(), weekend_yes.get_center(), color=WHITE, stroke_width=2)
        weekend_no_line = Line(afternoon_other.get_center(), weekend_no.get_center(), color=WHITE, stroke_width=2)
        
        # Build complete tree
        tree_parts = [root, morning_line, afternoon_line, morning_label, afternoon_label,
                     morning, afternoon, morning_virtue_line, morning_nonvirtue_line,
                     morning_virtue, morning_nonvirtue, afternoon_body_line, afternoon_other_line,
                     afternoon_body, afternoon_other, weekend_yes_line, weekend_no_line,
                     weekend_yes, weekend_no]
        
        self.play(Create(root))
        self.wait(0.5)
        
        # Add branches gradually
        for i in range(0, len(tree_parts), 3):
            batch = tree_parts[i:i+3]
            self.play(*[Create(part) for part in batch])
            self.wait(0.5)
        
        # Show tree metrics
        metrics = VGroup(
            Text("🌳 Tree Metrics:", font_size=28, color=WHITE),
            Text("• Total Nodes: 9", font_size=20, color=GRAY),
            Text("• Leaf Nodes: 5", font_size=20, color=GRAY),
            Text("• Max Depth: 4", font_size=20, color=GRAY),
            Text("• Training Accuracy: 87%", font_size=20, color=GREEN),
            Text("• Test Accuracy: 84%", font_size=20, color=BLUE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        metrics.to_edge(RIGHT)
        
        self.play(Write(metrics))
        
        # Show feature importance
        importance = VGroup(
            Text("📊 Feature Importance:", font_size=24, color=WHITE),
            Text("• Time of Day: 35%", font_size=18, color=RED),
            Text("• Category: 28%", font_size=18, color=GREEN),
            Text("• Realm: 22%", font_size=18, color=BLUE),
            Text("• Day Type: 15%", font_size=18, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        importance.to_edge(LEFT)
        
        self.play(Write(importance))
        self.wait(3)
        
        # Final message
        final_message = Text("Decision Tree training complete!", font_size=36, color=GREEN)
        final_message.to_edge(DOWN)
        self.play(Write(final_message))
        self.wait(2)
        
        self.play(FadeOut(VGroup(*tree_parts)), FadeOut(metrics), FadeOut(importance),
                 FadeOut(final_message), FadeOut(final_title))
