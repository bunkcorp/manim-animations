from manim import *
import numpy as np
from sklearn.cluster import KMeans

# Data generation function (copied from data_generator.py for self-containment)
def generate_cluster_data(n_samples_per_cluster=100, n_clusters=3, random_seed=42):
    np.random.seed(random_seed)
    data = []
    labels = []

    centers = [
        [2, 2],   # Cluster 1
        [8, 3],   # Cluster 2
        [4, 8]    # Cluster 3
    ]
    stds = [
        [0.8, 0.5],
        [0.5, 0.8],
        [0.7, 0.7]
    ]

    for i in range(n_clusters):
        for _ in range(n_samples_per_cluster):
            x = np.random.normal(loc=centers[i][0], scale=stds[i][0])
            y = np.random.normal(loc=centers[i][1], scale=stds[i][1])
            data.append([x, y])
            labels.append(i)

    return np.array(data), np.array(labels)

class KMeansAnimation(Scene):
    def construct(self):
        self.next_section("Introduction")
        title = Text("K-Means Clustering Animation").to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Generate data
        data, true_labels = generate_cluster_data(n_samples_per_cluster=50, n_clusters=3)
        
        # Scale data for Manim coordinates (adjust as needed)
        # Manim's default coordinate system is roughly -7 to 7 for x, -4 to 4 for y
        # Our data is roughly 0-10 for x, 0-10 for y. Let's scale and center.
        scaled_data = (data - np.mean(data, axis=0)) / np.std(data, axis=0) * 2 # Scale to fit roughly within [-2, 2]
        scaled_data += np.array([0, 0]) # Center around origin

        # Convert to 3D coordinates for Manim
        scaled_data_3d = np.column_stack([scaled_data, np.zeros(len(scaled_data))])
        points_mobjects = VGroup(*[Dot(point) for point in scaled_data_3d])
        self.play(FadeIn(points_mobjects))
        self.wait(1)

        n_clusters = 3
        kmeans = KMeans(n_clusters=n_clusters, init='random', n_init=1, max_iter=1, random_state=0) # One iteration at a time

        # Initial centroids
        self.next_section("Initialization")
        kmeans.fit(data) # Fit once to get initial centroids
        initial_centroids = kmeans.cluster_centers_
        
        # Scale initial centroids as well
        scaled_initial_centroids = (initial_centroids - np.mean(data, axis=0)) / np.std(data, axis=0) * 2
        scaled_initial_centroids += np.array([0, 0])

        # Convert centroids to 3D coordinates
        scaled_initial_centroids_3d = np.column_stack([scaled_initial_centroids, np.zeros(len(scaled_initial_centroids))])
        centroids_mobjects = VGroup(*[Dot(centroid, color=COLOR_MAP[i], radius=0.15) for i, centroid in enumerate(scaled_initial_centroids_3d)])
        self.play(FadeIn(centroids_mobjects))
        self.wait(1)

        # Iterations
        for i in range(3): # Run 3 iterations
            self.next_section(f"Iteration_{i+1}")
            iteration_text = Text(f"Iteration {i+1}").to_edge(UP).shift(DOWN*0.5)
            self.play(FadeOut(title), Write(iteration_text))

            # Assignment Step
            self.next_section(f"Assignment_{i+1}")
            assignment_text = Text("Assignment Step").next_to(iteration_text, DOWN)
            self.play(Write(assignment_text))

            # Predict clusters for current data points
            current_labels = kmeans.predict(data)
            
            # Animate coloring points
            animations = []
            for j, point_mobject in enumerate(points_mobjects):
                animations.append(point_mobject.animate.set_color(COLOR_MAP[current_labels[j]]))
            self.play(*animations)
            self.wait(1)

            # Update Step
            self.next_section(f"Update_{i+1}")
            update_text = Text("Update Step").next_to(assignment_text, DOWN)
            self.play(FadeOut(assignment_text), Write(update_text))

            # Recalculate centroids (Manim doesn't do this, so we simulate by refitting with max_iter=1)
            kmeans = KMeans(n_clusters=n_clusters, init=kmeans.cluster_centers_, n_init=1, max_iter=1, random_state=0) # Use current centroids as init
            kmeans.fit(data)
            new_centroids = kmeans.cluster_centers_
            
            # Scale new centroids
            scaled_new_centroids = (new_centroids - np.mean(data, axis=0)) / np.std(data, axis=0) * 2
            scaled_new_centroids += np.array([0, 0])

            # Convert new centroids to 3D coordinates
            scaled_new_centroids_3d = np.column_stack([scaled_new_centroids, np.zeros(len(scaled_new_centroids))])
            
            # Animate centroid movement
            animations = []
            for j, centroid_mobject in enumerate(centroids_mobjects):
                animations.append(centroid_mobject.animate.move_to(scaled_new_centroids_3d[j]))
            self.play(*animations)
            self.wait(1)
            
            self.play(FadeOut(iteration_text), FadeOut(update_text))

        self.next_section("Conclusion")
        final_text = Text("K-Means Clustering Complete").to_edge(UP)
        self.play(Write(final_text))
        self.wait(2)

COLOR_MAP = {
    0: RED,
    1: BLUE,
    2: GREEN,
    3: YELLOW,
    4: PURPLE,
    5: ORANGE,
    6: TEAL,
    7: PINK,
    8: MAROON,
    9: GOLD
}
