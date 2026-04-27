from manim import *
import numpy as np

class EMWaveLocalLente(ThreeDScene):
    def construct(self):
        # ---------------------------------------------------------
        # 1. CONFIGURATION DE LA SCÈNE ET CAMÉRA
        # ---------------------------------------------------------
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)
        
        axes = ThreeDAxes(
            x_range=[-1, 10, 1],
            y_range=[-2, 2, 1],
            z_range=[-2, 2, 1],
            x_length=10,
            y_length=4,
            z_length=4
        )
        
        COLOR_E = YELLOW
        COLOR_B = BLUE_C
        # Couleurs plus vives pour les vecteurs locaux sur le plan — ils doivent se distinguer
        # des courbes globales de l'onde sans pour autant créer de confusion de sens.
        COLOR_E_LOCAL = GOLD
        COLOR_B_LOCAL = BLUE_A
        COLOR_S = RED

        x_label = axes.get_x_axis_label(Text("x (Propagation)", font_size=24))

        # VGroup Text + MathTex : le Text gère l'accent de "Électrique", MathTex le vecteur
        y_text = Text("y (Champ Électrique ", font_size=24, color=COLOR_E)
        y_math = MathTex("\\vec{E})", color=COLOR_E).scale(0.8)
        y_label_content = VGroup(y_text, y_math).arrange(RIGHT, buff=0.1)
        y_label = axes.get_y_axis_label(y_label_content)
        # y_label.rotate(PI/2, axis=RIGHT)  # ancienne tentative — donnait une orientation bizarre
        y_label.rotate(270 * DEGREES, axis=OUT)

        # Champ Magnétique B
        z_text = Text("z (Champ Magnétique ", font_size=24, color=COLOR_B)
        z_math = MathTex("\\vec{B})", color=COLOR_B).scale(0.8)
        z_label_content = VGroup(z_text, z_math).arrange(RIGHT, buff=0.1)
        z_label = axes.get_z_axis_label(z_label_content)

        labels = VGroup(x_label, y_label, z_label)

        self.play(Create(axes), FadeIn(labels))
        self.wait(1)

        k = 1.0
        w = 1.25  # légèrement augmenté par rapport à 1.0 pour que l'onde semble plus dynamique
        t = ValueTracker(0)

        # ---------------------------------------------------------
        # 2. GÉNÉRATEURS D'OSCILLATION LOCALE
        # ---------------------------------------------------------
        def get_E_wave():
            vgroup = VGroup()
            for x in np.arange(0, 10, 0.4): 
                amp = np.cos(k * x - w * t.get_value())
                if abs(amp) > 0.05:
                    start = axes.c2p(x, 0, 0)
                    end = axes.c2p(x, amp, 0)
                    vec = Arrow(start, end, buff=0, color=COLOR_E, max_tip_length_to_length_ratio=0.15, stroke_width=3)
                    vgroup.add(vec)
            return vgroup

        def get_B_wave():
            vgroup = VGroup()
            for x in np.arange(0, 10, 0.4):
                amp = np.cos(k * x - w * t.get_value())
                if abs(amp) > 0.05:
                    start = axes.c2p(x, 0, 0)
                    end = axes.c2p(x, 0, amp)
                    vec = Arrow(start, end, buff=0, color=COLOR_B, max_tip_length_to_length_ratio=0.15, stroke_width=3)
                    vgroup.add(vec)
            return vgroup

        E_curve = always_redraw(lambda: axes.plot_parametric_curve(
            lambda x: np.array([x, np.cos(k * x - w * t.get_value()), 0]),
            t_range=[0, 10], color=COLOR_E, stroke_width=1
        ))
        B_curve = always_redraw(lambda: axes.plot_parametric_curve(
            lambda x: np.array([x, 0, np.cos(k * x - w * t.get_value())]),
            t_range=[0, 10], color=COLOR_B, stroke_width=1
        ))

        # ---------------------------------------------------------
        # 3. INTRODUCTION DES CHAMPS
        # ---------------------------------------------------------
        E_wave = always_redraw(get_E_wave)
        B_wave = always_redraw(get_B_wave)

        self.play(Create(E_curve), Create(E_wave), run_time=2.5)
        self.play(Create(B_curve), Create(B_wave), run_time=2.5)
        self.wait(1)

        # ---------------------------------------------------------
        # 4. DÉBUT DE LA PROPAGATION
        # ---------------------------------------------------------
        self.play(t.animate.set_value(2 * PI), run_time=6, rate_func=linear)
        
        # ---------------------------------------------------------
        # 5. LE PLAN D'OBSERVATION
        # ---------------------------------------------------------
        plane_x = 6
        plane = Rectangle(width=5, height=5, color=WHITE).set_fill(WHITE, opacity=0.1)
        plane.move_to(axes.c2p(plane_x, 0, 0))
        plane.rotate(PI/2, axis=UP)
        
        self.play(FadeIn(plane))
        self.move_camera(phi=75 * DEGREES, theta=-20 * DEGREES, run_time=2)

        # ---------------------------------------------------------
        # 6. VECTEURS LOCAUX (CONTRASTÉS) ET POYNTING
        # ---------------------------------------------------------
        def get_local_E():
            amp = np.cos(k * plane_x - w * t.get_value())
            if abs(amp) < 0.05: return Dot(axes.c2p(plane_x, 0, 0), radius=0)
            return Arrow(axes.c2p(plane_x, 0, 0), axes.c2p(plane_x, amp, 0), buff=0, color=COLOR_E_LOCAL, stroke_width=8)

        def get_local_B():
            amp = np.cos(k * plane_x - w * t.get_value())
            if abs(amp) < 0.05: return Dot(axes.c2p(plane_x, 0, 0), radius=0)
            return Arrow(axes.c2p(plane_x, 0, 0), axes.c2p(plane_x, 0, amp), buff=0, color=COLOR_B_LOCAL, stroke_width=8)

        def get_poynting_vector():
            amp = np.cos(k * plane_x - w * t.get_value())**2
            if amp < 0.05: return Dot(axes.c2p(plane_x, 0, 0), radius=0)
            return Arrow(
                axes.c2p(plane_x, 0, 0), 
                axes.c2p(plane_x + amp * 2, 0, 0), 
                buff=0, color=COLOR_S, stroke_width=10
            )

        local_E = always_redraw(get_local_E)
        local_B = always_redraw(get_local_B)
        poynting = always_redraw(get_poynting_vector)

        s_label = MathTex("\\vec{S} = \\frac{1}{\\mu_0} (\\vec{E} \\times \\vec{B})", color=COLOR_S).scale(0.8)
        self.add_fixed_in_frame_mobjects(s_label)
        s_label.to_corner(UR)

        self.play(FadeIn(local_E), FadeIn(local_B))
        self.play(FadeIn(poynting), FadeIn(s_label))

        # Propagation continue avec plan visible
        self.play(t.animate.set_value(6 * PI), run_time=12, rate_func=linear)

        # Balayage final pour montrer l'onde depuis un autre angle
        self.move_camera(phi=50 * DEGREES, theta=-75 * DEGREES, run_time=3)
        self.play(t.animate.set_value(8 * PI), run_time=6, rate_func=linear)

        self.wait(1)