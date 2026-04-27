from manim import *
import numpy as np

class MagneticForceMotion(ThreeDScene):
    def construct(self):
        # ==========================================
        # PART 1: 2D Circular Motion (Perpendicular v)
        # ==========================================
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)

        # Titre
        title = Tex("Force Magnétique et Mouvement", font_size=40)
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)
        self.remove(title)
        self.play(Write(title))

        # Zone du champ B
        field_rect = Rectangle(width=7, height=8, color=BLUE).set_fill(BLUE, opacity=0.1)
        field_rect.move_to(RIGHT * 3.5)
        
        dots = VGroup(*[
            Dot(np.array([x, y, 0]), color=BLUE, radius=0.04) 
            for x in np.arange(0.5, 6.5, 0.75) 
            for y in np.arange(-3.5, 4.0, 0.75)
        ])
        
        b_label = MathTex("\\vec{B} \\text{ (sortant)}", color=BLUE, font_size=32)
        b_label.next_to(field_rect, UP, buff=0.2).shift(LEFT)
        self.add_fixed_in_frame_mobjects(b_label)
        self.remove(b_label)
        
        self.play(FadeIn(field_rect), FadeIn(dots), Write(b_label))

        # Particule
        q = Dot(np.array([-4, 2, 0]), color=RED, radius=0.1)
        
        text_2d = Tex(
            "1. $\\vec{v} \\perp \\vec{B}$\\\\",
            "La force $\\vec{F}_m$ est purement radiale ($\\perp \\vec{v}$).\\\\",
            "La norme de la vitesse est constante,\\\\seule la direction change.\\\\",
            "$\\Rightarrow$ \\textbf{Mouvement Circulaire Uniforme}",
            font_size=32, color=WHITE
        )
        text_2d.to_corner(DL)
        self.add_fixed_in_frame_mobjects(text_2d)
        self.remove(text_2d)
        
        self.play(FadeIn(q), Write(text_2d))

        # On trace la trajectoire en temps réel pour bien voir la courbure
        path_trace = TracedPath(q.get_center, stroke_color=RED, stroke_width=3)
        self.add(path_trace)
        
        v_entry = always_redraw(lambda: Arrow(
            start=q.get_center(), end=q.get_center() + RIGHT * 1.5,
            color=GREEN, buff=0, max_tip_length_to_length_ratio=0.15
        ))
        v_label_entry = always_redraw(lambda: MathTex("\\vec{v}", color=GREEN, font_size=28)
                                      .next_to(v_entry.get_end(), UP, buff=0.1))
        
        self.add(v_entry, v_label_entry)
        self.play(q.animate.move_to(np.array([0, 2, 0])), run_time=2, rate_func=linear)
        self.remove(v_entry, v_label_entry)

        # Mouvement circulaire : F_m = qv×B est centripète, norme de v constante
        radius = 2
        t_tracker = ValueTracker(0)

        def get_pos(t):
            return np.array([radius * np.sin(t), radius * np.cos(t), 0])
        def get_v_dir(t):
            return np.array([np.cos(t), -np.sin(t), 0])
        def get_f_dir(t):
            return np.array([-np.sin(t), -np.cos(t), 0])

        q.add_updater(lambda m: m.move_to(get_pos(t_tracker.get_value())))

        v_vec = always_redraw(lambda: Arrow(
            start=q.get_center(), end=q.get_center() + get_v_dir(t_tracker.get_value()) * 1.5,
            color=GREEN, buff=0, max_tip_length_to_length_ratio=0.15
        ))
        f_vec = always_redraw(lambda: Arrow(
            start=q.get_center(), end=q.get_center() + get_f_dir(t_tracker.get_value()) * 1.5,
            color=YELLOW, buff=0, max_tip_length_to_length_ratio=0.15
        ))

        v_label = always_redraw(lambda: MathTex("\\vec{v}", color=GREEN, font_size=28)
                                .move_to(v_vec.get_end() + get_v_dir(t_tracker.get_value()) * 0.3))
        f_label = always_redraw(lambda: MathTex("\\vec{F}_m", color=YELLOW, font_size=28)
                                .move_to(f_vec.get_end() + get_f_dir(t_tracker.get_value()) * 0.3))

        self.add(v_vec, f_vec, v_label, f_label)
        self.play(t_tracker.animate.set_value(PI), run_time=4, rate_func=linear)
        
        q.clear_updaters()
        self.remove(v_vec, f_vec, v_label, f_label)
        
        # Sortie du champ : plus de force magnétique, la particule repart en ligne droite
        v_exit = always_redraw(lambda: Arrow(
            start=q.get_center(), end=q.get_center() + LEFT * 1.5,
            color=GREEN, buff=0, max_tip_length_to_length_ratio=0.15
        ))
        v_label_exit = always_redraw(lambda: MathTex("\\vec{v}", color=GREEN, font_size=28)
                                     .next_to(v_exit.get_end(), UP, buff=0.1))
        
        self.add(v_exit, v_label_exit)
        self.play(q.animate.move_to(np.array([-4, -2, 0])), run_time=2, rate_func=linear)
        self.remove(v_exit, v_label_exit)
        self.wait(1)

        # ==========================================
        # PART 2: 3D Helical Motion (Along Y-axis)
        # ==========================================
        self.play(
            FadeOut(field_rect), FadeOut(dots), FadeOut(b_label), 
            FadeOut(text_2d), FadeOut(path_trace), FadeOut(q)
        )

        # Vue oblique : on voit à la fois la rotation dans XZ et l'avancement selon Y
        self.move_camera(phi=75 * DEGREES, theta=-45 * DEGREES, run_time=2)

        text_3d = Tex(
            "2. Composante de vitesse $\\parallel \\vec{B}$ (selon l'axe $y$)\\\\",
            "$\\vec{v}_\\parallel$ est insensible à la force magnétique.\\\\",
            "$\\Rightarrow$ \\textbf{Mouvement Hélicoïdal}",
            font_size=32, color=WHITE
        )
        text_3d.to_corner(DL)
        self.add_fixed_in_frame_mobjects(text_3d)
        self.remove(text_3d)
        self.play(Write(text_3d))

        # Légende des vecteurs en 3D
        legend = VGroup(
            MathTex("\\vec{v}_{tot} = \\vec{v}_\\perp + \\vec{v}_\\parallel", font_size=30),
            Tex("$\\bullet$ $\\vec{v}_{tot}$ (Totale)", color=GREEN, font_size=26),
            Tex("$\\bullet$ $\\vec{v}_\\perp$ (Crée la rotation)", color=TEAL, font_size=26),
            Tex("$\\bullet$ $\\vec{v}_\\parallel$ (Crée l'avancement)", color=ORANGE, font_size=26),
            Tex("$\\bullet$ $\\vec{F}_m$ (Force centripète)", color=YELLOW, font_size=26)
        ).arrange(DOWN, aligned_edge=LEFT)
        legend.to_corner(DR)
        self.add_fixed_in_frame_mobjects(legend)
        self.remove(legend)
        self.play(FadeIn(legend))

        axes = ThreeDAxes(x_range=[-3, 3], y_range=[-4, 4], z_range=[-3, 3])
        y_label = MathTex("y").move_to(axes.c2p(0, 4.3, 0))
        self.play(Create(axes), FadeIn(y_label))

        # Lignes de champ B parallèles à l'axe Y
        b_lines = VGroup()
        for x in [-1.5, 1.5]:
            for z in [-1.5, 1.5]:
                line = Arrow3D(
                    start=np.array([x, -3.5, z]), 
                    end=np.array([x, 3.5, z]), 
                    color=BLUE, base_radius=0.03, height=0.2
                )
                b_lines.add(line)
        
        b_label_3d = MathTex("\\vec{B}", color=BLUE, font_size=36)
        b_label_3d.to_corner(UR)
        self.add_fixed_in_frame_mobjects(b_label_3d)
        self.remove(b_label_3d)
        self.play(FadeIn(b_lines), Write(b_label_3d))

        # Paramètres de l'hélice : R_3d = rayon de rotation, v_y = vitesse d'avancement selon B
        t_tracker_3d = ValueTracker(0)
        R_3d = 1.2
        omega = 2.0    # lent pour que l'étudiant ait le temps de lire les vecteurs
        v_y = 0.5      # composante parallèle à B — insensible à la force magnétique
        
        def get_helix_pos(t):
            # Progression selon Y, rotation dans le plan XZ
            return np.array([R_3d * np.cos(omega * t), (v_y * t) - 3.5, R_3d * np.sin(omega * t)])

        def get_v_tot(t):
            return np.array([-R_3d * omega * np.sin(omega * t), v_y, R_3d * omega * np.cos(omega * t)])
            
        def get_v_perp(t):
            return np.array([-R_3d * omega * np.sin(omega * t), 0, R_3d * omega * np.cos(omega * t)])
            
        def get_v_para(t):
            return np.array([0, v_y, 0])
            
        def get_f_dir(t):
            return np.array([-np.cos(omega * t), 0, -np.sin(omega * t)])

        q_3d = Dot3D(point=get_helix_pos(0), color=RED, radius=0.08)
        self.add(q_3d)

        helix_trace = TracedPath(q_3d.get_center, stroke_color=RED, stroke_width=4)
        self.add(helix_trace)

        # Facteurs d'échelle : les vecteurs physiques seraient trop grands à l'écran
        sc_v = 0.4
        sc_f = 1.0

        # Vecteurs dynamiques attachés à la particule
        v_vec_tot = always_redraw(lambda: Arrow3D(
            start=q_3d.get_center(), end=q_3d.get_center() + get_v_tot(t_tracker_3d.get_value()) * sc_v, 
            color=GREEN, base_radius=0.04, height=0.2
        ))
        v_vec_perp = always_redraw(lambda: Arrow3D(
            start=q_3d.get_center(), end=q_3d.get_center() + get_v_perp(t_tracker_3d.get_value()) * sc_v, 
            color=TEAL, base_radius=0.02, height=0.1
        ))
        v_vec_para = always_redraw(lambda: Arrow3D(
            start=q_3d.get_center(), end=q_3d.get_center() + get_v_para(t_tracker_3d.get_value()) * sc_v * 1.5, 
            color=ORANGE, base_radius=0.02, height=0.1
        ))
        f_vec_3d = always_redraw(lambda: Arrow3D(
            start=q_3d.get_center(), end=q_3d.get_center() + get_f_dir(t_tracker_3d.get_value()) * sc_f, 
            color=YELLOW, base_radius=0.04, height=0.2
        ))

        self.add(v_vec_perp, v_vec_para, v_vec_tot, f_vec_3d)

        q_3d.add_updater(lambda m: m.move_to(get_helix_pos(t_tracker_3d.get_value())))

        # 14 secondes : assez long pour que l'étudiant voie bien les trois composantes évoluer
        self.play(t_tracker_3d.animate.set_value(14), run_time=14, rate_func=linear)
        self.wait(3)