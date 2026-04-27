from manim import *

class AmpereLenz3D(ThreeDScene):
    def construct(self):
        # ─────────────────────────────────────────────
        # 1. Mise en place de la scène 3D (sans axes affichés)
        # ─────────────────────────────────────────────
        self.set_camera_orientation(phi=75 * DEGREES, theta=-60 * DEGREES)

        # Fil horizontal, courant orienté vers la GAUCHE (−X)
        wire_y_pos = -2
        wire = Line(LEFT * 5, RIGHT * 5, color=GRAY_B, stroke_width=6).shift(UP * wire_y_pos)

        # Flèche du courant I dirigée vers la gauche
        i_arrow = Arrow(RIGHT * 1.5, LEFT * 1.5, color=RED).next_to(wire, DOWN, buff=0.2)
        i_label = MathTex("I", color=RED).next_to(i_arrow, DOWN)

        # Boucle rectangulaire posée au-dessus du fil
        loop = Rectangle(height=2, width=3, color=WHITE).shift(UP * -0.5)

        # Petit rappel de la règle de la main droite
        rhr_hint = Text("Pouce vers la gauche (Main Droite)", color=RED_A).scale(0.4)
        rhr_hint.to_corner(DL)
        self.add_fixed_in_frame_mobjects(rhr_hint)

        # ─────────────────────────────────────────────
        # 2. Anneaux de champ magnétique autour du fil
        # ─────────────────────────────────────────────
        def get_field_ring(x_pos):
            ring_group = VGroup()
            radii     = [0.5, 0.9, 1.4, 2.0]
            opacities = [1.0, 0.75, 0.45, 0.20]
            for r, op in zip(radii, opacities):
                circ = Circle(radius=r, color=BLUE_B, stroke_width=2.5)
                circ.set_stroke(opacity=op) 
                circ.rotate(90 * DEGREES, axis=UP)
                circ.move_to(wire.get_center() + RIGHT * x_pos)
                circ.reverse_points()

                # Pointes de flèche bien grosses pour qu'on voie le sens à l'écran
                tip_len = 0.45 + r * 0.2
                arrow = Arrow(
                    circ.point_at_angle(85 * DEGREES),
                    circ.point_at_angle(95 * DEGREES),
                    color=YELLOW_B,
                    tip_length=tip_len,
                    stroke_width=8 + r, 
                    buff=0
                )
                arrow.set_stroke(opacity=op)
                ring_group.add(circ, arrow)
            
            # On garde en mémoire le centre exact, qui resservira pour l'animation
            # d'écrasement (sinon les anneaux glissent au lieu de s'écraser sur place).
            ring_group.center_on_wire = wire.get_center() + RIGHT * x_pos
            return ring_group

        rings = [get_field_ring(x) for x in [-3.0, -1.0, 1.0, 3.0]]
        field_system = VGroup(*rings)

        # ─────────────────────────────────────────────
        # 3. Les deux formules empilées, avec le signe "–" mis en avant
        # ─────────────────────────────────────────────
        ampere_formula = MathTex(
            r"\oint \vec{B} \cdot d\vec{l} = \mu_0 I",
            color=BLUE_B
        ).to_corner(UR).shift(LEFT * 0.5)
        
        # Formule de Lenz éclatée en morceaux pour pouvoir souligner le signe "–"
        lenz_formula = MathTex(
            r"\mathcal{E}", r"=", r"-", r"\frac{d\Phi_B}{dt}",
            color=GREEN_B
        ).next_to(ampere_formula, DOWN, aligned_edge=RIGHT)
        # Le signe "–" en rouge pour bien insister sur l'idée d'opposition
        lenz_formula[2].set_color(RED)

        ampere_formula.set_opacity(0)
        lenz_formula.set_opacity(0)
        self.add_fixed_in_frame_mobjects(ampere_formula, lenz_formula)

        # ─────────────────────────────────────────────
        # 4. Lancement de l'animation 3D
        # ─────────────────────────────────────────────
        self.add(wire, i_arrow, i_label, loop)
        self.play(ampere_formula.animate.set_opacity(1), Write(rhr_hint))

        def create_ring_at(ring_group):
            pairs = [(ring_group[i], ring_group[i+1]) for i in range(0, len(ring_group), 2)]
            return LaggedStart(
                *[AnimationGroup(Create(c), GrowArrow(a)) for c, a in pairs],
                lag_ratio=0.35
            )

        self.play(
            LaggedStart(*[create_ring_at(ring) for ring in field_system], lag_ratio=0.5),
            run_time=4
        )
        self.wait(2)

        # ─────────────────────────────────────────────
        # 5. Passage en vue 2D — chaque anneau s'écrase sur son propre centre
        # ─────────────────────────────────────────────
        self.move_camera(phi=0, theta=-90 * DEGREES, run_time=2)

        # Sans about_point, les anneaux glissent vers le centre commun pendant
        # le scale ; c'est moche. On les écrase chacun sur son propre centre.
        squish_animations = [
            ring.animate.scale(0.1, about_point=ring.center_on_wire).set_opacity(0)
            for ring in field_system
        ]

        self.play(
            *squish_animations,
            ampere_formula.animate.scale(0.8).to_edge(UP).shift(RIGHT),
            FadeOut(rhr_hint)
        )

        # Symboles ⊗ (champ entrant) en vue 2D, avec un dégradé de taille
        def make_cross(x, y):
            y_vals = np.arange(-0.5, 0.6, 0.5)
            y_min, y_max = y_vals[0], y_vals[-1]
            t = (y - y_min) / (y_max - y_min) if y_max != y_min else 0
            sc = 1.1 - 0.6 * t
            return MathTex(r"\otimes", color=BLUE_D).scale(sc).move_to(
                loop.get_center() + np.array([x, y, 0])
            )
            
        crosses = VGroup(*[
            make_cross(x, y)
            for x in np.arange(-1.0, 1.5, 1.0)
            for y in np.arange(-0.5, 0.6, 0.5)
        ])
        self.play(FadeIn(crosses))
        self.wait(1)

        # ─────────────────────────────────────────────
        # 6. Application de la loi de Lenz
        # ─────────────────────────────────────────────
        stage_text = MathTex(
            r"I \downarrow \implies \Phi_{\otimes} \downarrow",
            color=RED
        ).to_corner(UL)
        self.add_fixed_in_frame_mobjects(stage_text)

        self.play(
            i_arrow.animate.scale(0.3).set_color(RED_E),
            crosses.animate.set_opacity(0.2),
            Write(stage_text)
        )
        self.wait(0.5)
        self.play(lenz_formula.animate.set_opacity(1))

        b_ind = MathTex(
            r"\vec{B}_{\text{ind}} = \otimes",
            color=GREEN
        ).next_to(loop, RIGHT)
        self.add_fixed_in_frame_mobjects(b_ind)

        crosses_ind = VGroup(*[
            MathTex(r"\otimes", color=GREEN).scale(0.8).move_to(
                loop.get_center() + np.array([x, y, 0])
            )
            for x in np.arange(-1.0, 1.5, 1.0)
            for y in np.arange(-0.5, 0.6, 0.5)
        ])
        self.play(FadeIn(crosses_ind), Write(b_ind))
        self.wait(0.5)

        # Le courant induit, qui apparaît dans le sens qui s'oppose à la diminution du flux
        current_path = VGroup(
            Arrow(loop.get_corner(UL), loop.get_corner(UR), color=GOLD, buff=0),
            Arrow(loop.get_corner(UR), loop.get_corner(DR), color=GOLD, buff=0),
            Arrow(loop.get_corner(DR), loop.get_corner(DL), color=GOLD, buff=0),
            Arrow(loop.get_corner(DL), loop.get_corner(UL), color=GOLD, buff=0),
        )
        
        # Étiquette du courant induit, posée au-dessus de la boucle
        i_ind_label = MathTex(r"I_{\text{ind}}", color=GOLD).scale(0.8).next_to(loop, UP)
        self.add_fixed_in_frame_mobjects(i_ind_label)

        # On synchronise toutes les indications visuelles : la boucle, le signe "–"
        # de la formule, le courant induit. Ça marque bien le lien causal.
        self.play(
            Indicate(loop, color=GOLD),
            Indicate(lenz_formula[2], color=RED, scale_factor=2), # zoom sur le signe "–"
            Indicate(lenz_formula, color=GOLD),
            Create(current_path), 
            Write(i_ind_label)
        )
        self.wait(3)