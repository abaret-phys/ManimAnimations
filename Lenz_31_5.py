from manim import *

class LenzCompleteExercise(ThreeDScene):
    def construct(self):
        # ─────────────────────────────────────────────
        # 1. Mise en place : zone de champ + graphique côté droit
        # ─────────────────────────────────────────────
        field_box = Rectangle(width=4, height=4, color=BLUE_E, fill_opacity=0.1)
        field_box.to_edge(LEFT, buff=0.8)
        
        b_symbols = VGroup(*[
            MathTex(r"\odot", color=BLUE_B).scale(0.8).move_to(field_box.get_center() + np.array([x, y, 0]))
            for x in np.arange(-1.5, 2, 1) for y in np.arange(-1.5, 2, 1)
        ])

        axes = Axes(
            x_range=[0, 5, 1], y_range=[-1, 1.5, 1],
            x_length=5, y_length=4,
            axis_config={"include_tip": False, "color": GRAY}
        ).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.5)
        
        phi_label = MathTex(r"\Phi_B", color=YELLOW).scale(0.8).move_to(axes.c2p(0.5, 1.3))
        deriv_label = MathTex(r"\frac{d\Phi_B}{dt}", color=TEAL).scale(0.8).move_to(axes.c2p(4.5, -0.4))

        # Étiquettes des trois phases, posées en blanc au-dessus du graphique.
        # Elles apparaissent une par une au moment où la phase correspondante démarre.
        phase1_lab = MathTex(r"\Phi_B \text{ constant } (\mathcal{E}=0)", color=WHITE).scale(0.45)
        phase2_lab = MathTex(r"\Phi_B \propto t", color=WHITE).scale(0.45)
        phase3_lab = MathTex(r"\Phi_B = 0", color=WHITE).scale(0.45)
        
        # Positionnement précis au-dessus des axes (y=1.7 dans le repère du graphique)
        phase1_lab.move_to(axes.c2p(0.7, 1.7))
        phase2_lab.move_to(axes.c2p(2.5, 1.7))
        phase3_lab.move_to(axes.c2p(4.0, 1.7))

        # Au démarrage, seule la phase 1 est visible
        phase1_lab.set_opacity(1)
        phase2_lab.set_opacity(0)
        phase3_lab.set_opacity(0)

        self.add_fixed_in_frame_mobjects(axes, phi_label, deriv_label, phase1_lab, phase2_lab, phase3_lab)

        # ─────────────────────────────────────────────
        # 2. La boucle qui se déplace et la formule de Lenz
        # ─────────────────────────────────────────────
        loop = Square(side_length=1.5, color=WHITE, stroke_width=4)
        loop.move_to(field_box.get_center() + LEFT * 0.5) 
        
        v_arrow = Arrow(loop.get_right(), loop.get_right() + RIGHT * 0.8, color=WHITE, buff=0.1)
        v_text = MathTex(r"\vec{v}", color=WHITE).next_to(v_arrow, RIGHT, buff=0.1)
        
        lenz_formula = MathTex(
            r"\mathcal{E}", r"=", r"-", r"\frac{d\Phi_B}{dt}", color=GREEN
        ).to_edge(UP).shift(RIGHT * 2)
        lenz_formula[2].set_color(RED)

        # ─────────────────────────────────────────────
        # 3. Physique du système et synchronisation des phases
        # ─────────────────────────────────────────────
        t_tracker = ValueTracker(0)
        v_const = 1.0
        boundary_x = field_box.get_right()[0]
        t1 = (boundary_x - (field_box.get_center()[0] - 0.5 + 0.75)) / v_const
        t2 = t1 + 1.5 / v_const

        def get_flux(t):
            if t < t1: return 1.0
            elif t < t2: return 1.0 - (t - t1) / (t2 - t1)
            else: return 0.0

        def get_deriv(t):
            if t1 <= t <= t2: return -1.0 / (t2 - t1)
            return 0.0

        def loop_physics_updater(m):
            t = t_tracker.get_value()
            m.set_x(field_box.get_center()[0] - 0.5 + t * v_const)
            v_arrow.next_to(m, RIGHT, buff=0.1)
            v_text.next_to(v_arrow, RIGHT, buff=0.1)
            
            # On rend visibles les étiquettes au fur et à mesure que les phases démarrent
            if t >= 0: phase1_lab.set_opacity(1)
            if t >= t1: phase2_lab.set_opacity(1)
            if t >= t2: phase3_lab.set_opacity(1)

        loop.add_updater(loop_physics_updater)

        # Les flèches qui matérialisent le courant induit pendant la phase de sortie
        i_ind_arrows = VGroup(
            Arrow(loop.get_corner(UR), loop.get_corner(UL), color=GOLD, buff=0),
            Arrow(loop.get_corner(UL), loop.get_corner(DL), color=GOLD, buff=0),
            Arrow(loop.get_corner(DL), loop.get_corner(DR), color=GOLD, buff=0),
            Arrow(loop.get_corner(DR), loop.get_corner(UR), color=GOLD, buff=0),
        )
        i_label = MathTex("I_{ind}", color=GOLD).scale(0.8)
        
        i_ind_arrows.set_opacity(0)
        i_label.set_opacity(0)

        def i_ind_updater(m):
            t = t_tracker.get_value()
            m.move_to(loop.get_center())
            i_label.next_to(loop, UP, buff=0.2)
            if t1 <= t <= t2:
                m.set_opacity(1)
                i_label.set_opacity(1)
                loop.set_color(GOLD)
                loop.set_stroke(width=8) 
            else:
                m.set_opacity(0)
                i_label.set_opacity(0)
                loop.set_color(WHITE)
                loop.set_stroke(width=4)

        i_ind_arrows.add_updater(i_ind_updater)

        # Tracé du flux et de sa dérivée — les deux courbes se construisent en temps réel
        phi_curve = always_redraw(lambda: axes.plot(
            get_flux, 
            x_range=[0, max(0.01, t_tracker.get_value())], 
            color=YELLOW
        ))
        
        deriv_curve = always_redraw(lambda: axes.plot(
            get_deriv, 
            x_range=[0, max(0.01, t_tracker.get_value())], 
            color=TEAL, 
            use_smoothing=False,
            discontinuities=[t1, t2]
        ))
        
        moving_dot = always_redraw(lambda: 
            Dot(color=RED if t1 <= t_tracker.get_value() <= t2 else YELLOW).move_to(
                axes.c2p(t_tracker.get_value(), get_flux(t_tracker.get_value()))
            )
        )

        # ─────────────────────────────────────────────
        # 4. Lancement de l'animation, phase par phase
        # ─────────────────────────────────────────────
        self.add(field_box, b_symbols, axes, phi_label, deriv_label, loop, v_arrow, v_text)
        self.add(phi_curve, deriv_curve, moving_dot, i_ind_arrows, i_label)
        self.wait(1)

        # PHASE 1 : la boucle est entièrement dans le champ → flux constant, pas de fem
        self.play(t_tracker.animate.set_value(t1), run_time=t1, rate_func=linear)

        # PHASE 2 : la boucle commence à sortir → le flux chute, la fem apparaît
        self.play(Write(lenz_formula), run_time=0.5)
        self.play(
            Indicate(lenz_formula[2], color=RED, scale_factor=2),
            Indicate(deriv_label, color=TEAL), 
            Flash(axes.c2p(t1, 1), color=RED),
            run_time=1
        )
        
        # Pendant que la boucle sort, le flux décroît linéairement
        self.play(t_tracker.animate.set_value(t2), run_time=(t2 - t1), rate_func=linear)

        # PHASE 3 : la boucle est complètement hors du champ → flux nul, fem nulle
        self.play(t_tracker.animate.set_value(5), run_time=1.5, rate_func=linear)
        self.wait(2)