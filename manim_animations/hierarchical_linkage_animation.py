from manim import *
import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage

class HierarchicalLinkageAnimation(Scene):
    def construct(self):
        self.next_section("Introduction")
        title = Text("Hierarchical Clustering: Linkage Methods").to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # 1. Display Data Points
        points_coords = np.array([
            [1, 1], [2, 1.5], [1.5, 2.5], # Cluster 1
            [7, 7], [8, 7.5], [7.5, 8.5], # Cluster 2
            [4, 4], [4.5, 4.2]            # Isolated points
        ])
        
        # Scale points for Manim coordinates
        scaled_points = (points_coords - np.mean(points_coords, axis=0)) / np.std(points_coords, axis=0) * 2
        scaled_points += np.array([0, 0]) # Center around origin

        dots = VGroup(*[Dot(np.array([p[0], p[1], 0]), radius=0.1, color=BLUE) for p in scaled_points])
        labels = VGroup(*[Text(str(i+1)).next_to(dots[i], UP*0.5).scale(0.5) for i in range(len(dots))])

        self.play(FadeIn(dots), FadeIn(labels))
        self.wait(1)

        # Explain Clusters and Distances
        self.next_section("Concepts")
        concept_text = Text("Clusters are initially individual points.").to_edge(UP).shift(DOWN*0.5)
        self.play(Transform(title, concept_text))
        self.wait(1)

        dist_concept = Text("Distance between clusters is key.").next_to(concept_text, DOWN)
        self.play(Write(dist_concept))
        self.wait(1)

        # Define Linkage Methods
        linkage_methods = {
            "Single Linkage": {
                "formula": r"D(C_i, C_j) = \min_{x \in C_i, y \in C_j} d(x, y)",
                "description": "(Minimum Distance) - Closest pair of points."
            },
            "Complete Linkage": {
                "formula": r"D(C_i, C_j) = \max_{x \in C_i, y \in C_j} d(x, y)",
                "description": "(Maximum Distance) - Furthest pair of points."
            },
            "Average Linkage": {
                "formula": r"D(C_i, C_j) = \frac{1}{|C_i||C_j|} \sum_{x \in C_i, y \in C_j} d(x, y)",
                "description": "(Average Distance) - Average of all pairwise distances."
            }
        }

        # Iterate through linkage methods
        for method_name, method_info in linkage_methods.items():
            self.next_section(method_name.replace(" ", ""))
            method_title = Text(method_name).to_edge(UP).shift(DOWN*0.5)
            formula_mob = MathTex(method_info["formula"]).next_to(method_title, DOWN)
            desc_mob = Text(method_info["description"]).next_to(formula_mob, DOWN).scale(0.7)

            self.play(Transform(title, method_title), FadeOut(dist_concept) if method_name == "Single Linkage" else FadeOut(prev_desc_mob), Write(formula_mob), Write(desc_mob))
            self.wait(1)

            # Simulate a merge based on this linkage (conceptual for a few points)
            # For simplicity, we'll just show the first merge for a small subset of points
            # This is not a full hierarchical clustering animation, but illustrates the merge criteria
            
            # Reset points for each method for clarity
            if method_name != "Single Linkage":
                self.play(FadeOut(dots), FadeOut(labels))
                dots = VGroup(*[Dot(np.array([p[0], p[1], 0]), radius=0.1, color=BLUE) for p in scaled_points])
                labels = VGroup(*[Text(str(i+1)).next_to(dots[i], UP*0.5).scale(0.5) for i in range(len(dots))])
                self.play(FadeIn(dots), FadeIn(labels))
                self.wait(0.5)

            # Find the closest pair based on the current method
            # This is a simplified illustration, not a full linkage algorithm
            if method_name == "Single Linkage":
                # Closest two points overall
                min_dist = float('inf')
                min_pair = (0, 0)
                for i in range(len(points_coords)):
                    for j in range(i + 1, len(points_coords)):
                        dist = np.linalg.norm(points_coords[i] - points_coords[j])
                        if dist < min_dist:
                            min_dist = dist
                            min_pair = (i, j)
                
                p1_idx, p2_idx = min_pair
                line_to_highlight = Line(dots[p1_idx].get_center(), dots[p2_idx].get_center(), color=YELLOW, stroke_width=3)
                self.play(Create(line_to_highlight), dots[p1_idx].animate.set_color(RED), dots[p2_idx].animate.set_color(RED))
                self.wait(1)
                self.play(FadeOut(line_to_highlight), dots[p1_idx].animate.set_color(BLUE), dots[p2_idx].animate.set_color(BLUE))

            elif method_name == "Complete Linkage":
                # Conceptually, pick two clusters and show their furthest points
                # For simplicity, let's assume points 0,1,2 form one cluster and 3,4,5 form another
                # And we are merging these two clusters
                cluster1_indices = [0, 1, 2]
                cluster2_indices = [3, 4, 5]
                
                max_dist = -float('inf')
                max_pair_in_clusters = (0, 0)
                for i in cluster1_indices:
                    for j in cluster2_indices:
                        dist = np.linalg.norm(points_coords[i] - points_coords[j])
                        if dist > max_dist:
                            max_dist = dist
                            max_pair_in_clusters = (i, j)
                
                p1_idx, p2_idx = max_pair_in_clusters
                line_to_highlight = Line(dots[p1_idx].get_center(), dots[p2_idx].get_center(), color=YELLOW, stroke_width=3)
                self.play(Create(line_to_highlight), dots[p1_idx].animate.set_color(RED), dots[p2_idx].animate.set_color(RED))
                self.wait(1)
                self.play(FadeOut(line_to_highlight), dots[p1_idx].animate.set_color(BLUE), dots[p2_idx].animate.set_color(BLUE))

            elif method_name == "Average Linkage":
                # Conceptually, pick two clusters and show lines for all pairwise distances
                cluster1_indices = [0, 1, 2]
                cluster2_indices = [3, 4, 5]
                
                pairwise_lines = VGroup()
                for i in cluster1_indices:
                    for j in cluster2_indices:
                        line = Line(dots[i].get_center(), dots[j].get_center(), color=GRAY, stroke_width=1)
                        pairwise_lines.add(line)
                
                self.play(Create(pairwise_lines))
                self.wait(1)
                self.play(FadeOut(pairwise_lines))

            # Show a conceptual merge (e.g., by drawing a circle around the merged points)
            # For simplicity, we'll just highlight the points that would merge
            # and then show a conceptual new cluster
            if method_name == "Single Linkage":
                merge_indices = min_pair
            elif method_name == "Complete Linkage" or method_name == "Average Linkage":
                merge_indices = [0, 1, 2, 3, 4, 5] # Conceptual merge of two larger groups
            else:
                merge_indices = []

            if len(merge_indices) > 0:
                # Create a conceptual bounding box or circle around the merged points
                merged_points_mobs = VGroup(*[dots[idx] for idx in merge_indices])
                bounding_box = SurroundingRectangle(merged_points_mobs, color=GREEN, buff=0.5)
                self.play(Create(bounding_box))
                self.wait(1)
                self.play(FadeOut(bounding_box))

            prev_desc_mob = desc_mob
            self.play(FadeOut(formula_mob), FadeOut(desc_mob))

        self.next_section("Conclusion")
        final_text = Text("Different linkages define cluster distances differently.").to_edge(UP)
        self.play(Transform(title, final_text))
        self.wait(2)
