from manim import *
import numpy as np
from scipy.spatial import ConvexHull

config.background_color = WHITE

class PCA3DAnimation(ThreeDScene):
    def construct(self):
        # Set equal 3D axes — BLACK color, no labels
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            z_length=6,
            axis_config={"include_tip": True, "include_ticks": False, "stroke_width": 2.5}
        ).set_color(BLACK)  # 🖤 BLACK AXES

        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.add(axes)
        self.wait(0.5)

        # Generate 150 points — mostly in XZ plane, tiny Y noise
        np.random.seed(42)
        n_points = 150

        x_vals = np.linspace(-2.5, 2.5, n_points)
        z_vals = np.linspace(-2.5, 2.5, n_points)
        y_vals = np.zeros(n_points)

        noise_x = np.random.normal(scale=0.15, size=n_points)
        noise_y = np.random.normal(scale=0.05, size=n_points)
        noise_z = np.random.normal(scale=0.15, size=n_points)

        x_vals += noise_x
        y_vals += noise_y
        z_vals += noise_z

        data_points = list(zip(x_vals, y_vals, z_vals))

        # Create 3D dots — BLUE_A
        dots = VGroup()
        for x, y, z in data_points:
            dot = Dot3D(point=axes.c2p(x, y, z), radius=0.04, color=BLUE_C)  # 🔵 BLUE_A
            dots.add(dot)

        self.play(
            LaggedStart(*[DrawBorderThenFill(dot) for dot in dots], lag_ratio=0.02),
            run_time=2
        )
        self.wait(1)

        # === 3D CRYSTAL-LIKE CONVEX HULL ===
        raw_points = np.array([[x, y, z] for x, y, z in data_points])
        points_3d_np = np.array([axes.c2p(x, y, z) for x, y, z in data_points])

        try:
            hull = ConvexHull(raw_points)
            hull_faces = []
            for simplex in hull.simplices:
                face_points = [points_3d_np[i] for i in simplex]
                # Create filled face with stroke — crystal effect
                face = Polygon(*face_points)\
                    .set_fill(PURE_RED, opacity=0.15)\
                    .set_stroke(PURE_RED, width=0, opacity=0.4)
                hull_faces.append(face)
            hull_group = VGroup(*hull_faces).scale(1.1)

            self.play(FadeIn(hull_group), run_time=1.5)
            self.wait(0.5)

            # Rotate around hull — show from many angles
            angles = [
                (75 * DEGREES, 30 * DEGREES),
                (60 * DEGREES, -45 * DEGREES),
                (45 * DEGREES, 120 * DEGREES),
                (80 * DEGREES, 180 * DEGREES),
                (50 * DEGREES, 60 * DEGREES),
                (75 * DEGREES, 30 * DEGREES),
            ]

            for phi, theta in angles:
                self.move_camera(phi=phi, theta=theta, run_time=2)
                self.wait(0.3)

            self.play(FadeOut(hull_group), run_time=1.5)
            self.remove(hull_group)  # Clean up to reduce submobjects

        except Exception as e:
            print("ConvexHull failed, using XZ fallback:", e)
            points_xz = np.array([[x, z] for x, y, z in data_points])
            hull_2d = ConvexHull(points_xz)
            hull_vertices_2d = [points_xz[i] for i in hull_2d.vertices]
            hull_vertices_3d = [axes.c2p(x, 0, z) for x, z in hull_vertices_2d]
            hull_poly = Polygon(*hull_vertices_3d)\
                .set_fill(WHITE, opacity=0.2)\
                .set_stroke(WHITE, width=2, opacity=0.5)
            self.play(FadeIn(hull_poly), run_time=1)
            self.wait(1)
            self.play(FadeOut(hull_poly))
            self.remove(hull_poly)

        self.wait(1)

        # === PCA CALCULATION ===
        centered_coords = np.array([[x, y, z] for x, y, z in data_points])
        data_matrix = centered_coords.T
        cov_matrix = np.cov(data_matrix)
        eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

        sorted_indices = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[sorted_indices]
        eigenvectors = eigenvectors[:, sorted_indices]

        PC_COLORS = [PURE_GREEN, PURE_RED, PURE_BLUE]
        vector_length = 2.5

        pc_arrows = VGroup()
        pc_lines = VGroup()
        pc_projections = [VGroup() for _ in range(3)]

        for i in range(3):
            pc_vector = eigenvectors[:, i]
            color = PC_COLORS[i]

            arrow = Arrow3D(
                start=axes.c2p(0, 0, 0),
                end=axes.c2p(
                    pc_vector[0] * vector_length,
                    pc_vector[1] * vector_length,
                    pc_vector[2] * vector_length
                ),
                color=color,
                thickness=0.02,
                resolution=8
            )
            pc_arrows.add(arrow)

            dotted_line = DashedLine(
                axes.c2p(-pc_vector[0] * 3.5, -pc_vector[1] * 3.5, -pc_vector[2] * 3.5),
                axes.c2p(pc_vector[0] * 3.5, pc_vector[1] * 3.5, pc_vector[2] * 3.5),
                color=color,
                stroke_width=2,
                dash_length=0.1
            )
            pc_lines.add(dotted_line)

            for x, y, z in data_points:
                point = np.array([x, y, z])
                proj_length = np.dot(point, pc_vector)
                proj_point = proj_length * pc_vector
                proj_dot = Dot3D(
                    point=axes.c2p(*proj_point),
                    radius=0.03,
                    color=color
                )
                pc_projections[i].add(proj_dot)

        # Animate PCs
        for i in range(3):
            self.play(Create(pc_lines[i]), run_time=1)
            self.play(DrawBorderThenFill(pc_arrows[i]), run_time=1.5)
            self.wait(0.3)

        self.wait(1)

        # Animate projections
        for i in range(3):
            self.play(ReplacementTransform(dots.copy(), pc_projections[i]), run_time=1.5)
            self.wait(0.5)

        # Clean up: keep only PC1 (GREEN)
        self.play(
            FadeOut(pc_arrows[1]),      # RED
            FadeOut(pc_arrows[2]),      # BLUE
            FadeOut(pc_lines[1]),
            FadeOut(pc_lines[2]),
            FadeOut(pc_projections[1]),
            FadeOut(pc_projections[2]),
            FadeOut(dots),
            run_time=2
        )

        self.wait(1)

        # Focus camera on PC1
        self.move_camera(phi=60 * DEGREES, theta=45 * DEGREES, zoom=0.9, run_time=2)

        # 💬 FIXED SCREEN TEXT — NOT 3D, NOT ROTATING
        var_percent = 100 * eigenvalues / np.sum(eigenvalues)
        pc1_text = Text(
            f"PC1 captures {var_percent[0]:.1f}% of variance",
            font_size=36,
            color=GREEN,
            weight=BOLD
        ).to_edge(UP, buff=0.5)  # Fixed to top of SCREEN, not 3D space

        self.add_fixed_in_frame_mobjects(pc1_text)  # 🔒 LOCK TO CAMERA
        self.play(Create(pc1_text))

        self.wait(4)