from manim import *


def make_arrow(start, end, color=WHITE, stroke_width=4, tip_size=0.15):
    # Arrow et add_tip de Manim ont des boîtes englobantes asymétriques et des
    # comportements de scaling qui cassent les animations fines. On construit
    # à la main : une Line + un Polygon triangulaire, c'est plus prévisible.
    start = np.array(start, dtype=float)
    end = np.array(end, dtype=float)
    direction = end - start
    length = np.linalg.norm(direction)
    if length == 0:
        return VGroup()
    unit = direction / length
    # Perpendiculaire dans le plan xy, utilisée pour les deux coins de la pointe
    perp = np.array([-unit[1], unit[0], 0.0])

    # La ligne s'arrête avant la pointe pour qu'il n'y ait pas de chevauchement
    line_end = end - unit * tip_size
    line = Line(start=start, end=line_end, stroke_width=stroke_width)
    line.set_color(color)

    # Triangle (pointe)
    tip_base_left = end - unit * tip_size + perp * tip_size * 0.5
    tip_base_right = end - unit * tip_size - perp * tip_size * 0.5
    tip_tri = Polygon(
        end, tip_base_left, tip_base_right,
        fill_opacity=1,
        stroke_width=0,
    )
    tip_tri.set_fill(color)

    arrow = VGroup(line, tip_tri)
    return arrow


class SymetrieSpherique2D(Scene):
    """Scène combinée : partie 1 (symétrie sphérique) + partie 2 (plan infini)."""

    def construct(self):
        self._run_setup_legend()
        self._run_part1()
        self._run_part2()

    # ==============================================================
    # SETUP COMMUN : rectangle de légende + fonction make_legend
    # ==============================================================
    def _run_setup_legend(self):
        bg_rect = Rectangle(
            width=config.frame_width,
            height=1.2,
            fill_color=BLACK,
            fill_opacity=0.85,
            stroke_width=0,
        ).to_edge(DOWN, buff=0)
        self.add(bg_rect)
        self._bg_rect = bg_rect

    def _make_legend(self, tex_str):
        leg = Tex(tex_str, font_size=36)
        leg.move_to(self._bg_rect.get_center())
        return leg

    # ==============================================================
    # PARTIE 1 : SYMÉTRIE SPHÉRIQUE
    # ==============================================================
    def _run_part1(self):
        # ==========================================================
        # CONFIGURATION
        # ==========================================================
        R_charge = 1.2
        R_gauss = 2.6
        n_arrows = 12

        make_legend = self._make_legend

        # ==========================================================
        # OBJETS PHYSIQUES
        # ==========================================================
        charge = Circle(radius=R_charge, fill_opacity=0.7, stroke_width=3)
        charge.set_fill(BLUE_D)
        charge.set_stroke(BLUE_B)
        plus_sign = Tex("+", font_size=60)
        plus_sign.set_color(WHITE)
        plus_sign.move_to(charge.get_center())

        # Vecteurs champ radiaux — 12 directions
        radial_vectors = VGroup()
        for k in range(n_arrows):
            angle = k * TAU / n_arrows
            d = np.array([np.cos(angle), np.sin(angle), 0])
            radial_vectors.add(
                make_arrow(d * R_charge, d * (R_charge + 0.6),
                           color=WHITE, stroke_width=3, tip_size=0.12)
            )

        # Vecteur d'étude (rouge) — initialement radial, au pôle "nord"
        P_start = np.array([0.0, R_charge, 0.0])
        P_end_radial = np.array([0.0, R_charge + 1.2, 0.0])
        red_vector = make_arrow(
            P_start, P_end_radial, color=RED, stroke_width=6, tip_size=0.2
        )

        # Point visuel en P
        P_dot = Dot(point=P_start, radius=0.07, color=RED)

        # Label P (à droite du vecteur, hors du disque)
        P_label = Tex("$P$", font_size=36)
        P_label.set_color(RED)
        P_label.next_to(P_start, UR, buff=0.15)

        # ==========================================================
        # TITRE PARTIE 1
        # ==========================================================
        title_part1 = Tex("Symétrie sphérique (vue en coupe)", font_size=40)
        title_part1.set_color(BLUE_A)
        title_part1.to_edge(UP, buff=0.3)
        self.play(FadeIn(title_part1), run_time=0.8)
        self.wait(0.3)

        # ==========================================================
        # SCÈNE 1 : INTRODUCTION
        # ==========================================================
        legend = make_legend(
            "Distribution sphérique de charge : on cherche la direction de $\\vec{E}$."
        )

        self.play(Create(charge), Write(plus_sign), FadeIn(legend), run_time=1.6)
        self.play(
            LaggedStart(*[FadeIn(v) for v in radial_vectors], lag_ratio=0.06),
            run_time=1.6,
        )
        self.play(FadeIn(red_vector), FadeIn(P_dot), Write(P_label), run_time=1.1)
        self.wait(1.0)

        # ==========================================================
        # ACTION 1 : L'HYPOTHÈSE ABSURDE
        # ==========================================================
        leg_1 = make_legend(
            "Hypothèse : supposons que $\\vec{E}(P)$ n'est pas radial."
        )

        self.play(
            FadeOut(radial_vectors),
            FadeOut(legend),
            FadeIn(leg_1),
            run_time=1.1,
        )
        self.wait(0.6)

        tilt_angle = 40 * DEGREES
        self.play(
            Rotate(red_vector, angle=tilt_angle, about_point=P_start),
            run_time=1.6,
        )
        self.wait(1.2)

        # ==========================================================
        # ACTION 2 : LA ROTATION (LE PARADOXE)
        # ==========================================================
        leg_2 = make_legend(
            "Rotation : la charge est inchangée, mais $\\vec{E}$ a tourné. Absurde !"
        )

        system = VGroup(charge, plus_sign, red_vector, P_dot, P_label)

        self.play(FadeOut(leg_1), FadeIn(leg_2), run_time=0.6)
        self.wait(0.4)
        self.play(
            Rotate(system, angle=120 * DEGREES, about_point=ORIGIN),
            run_time=2.0,
        )
        self.wait(0.6)
        self.play(
            Rotate(system, angle=-120 * DEGREES, about_point=ORIGIN),
            run_time=2.0,
        )
        self.wait(0.8)

        # ==========================================================
        # RÉSOLUTION : le vecteur doit être radial
        # ==========================================================
        leg_3 = make_legend(
            "Seule solution invariante par rotation : $\\vec{E}$ est radial."
        )

        self.play(FadeOut(leg_2), FadeIn(leg_3), run_time=0.6)
        self.wait(0.4)
        self.play(
            Rotate(red_vector, angle=-tilt_angle, about_point=P_start),
            run_time=1.6,
        )
        self.wait(0.8)

        self.play(
            LaggedStart(*[FadeIn(v) for v in radial_vectors], lag_ratio=0.06),
            run_time=1.6,
        )
        self.wait(0.8)

        # ==========================================================
        # CONCLUSION : surface de Gauss + norme constante
        # ==========================================================
        # D'abord on transforme le vecteur rouge en l'un des vecteurs blancs
        # (même direction radiale, même norme) pour montrer visuellement que
        # E(P) est désormais "comme les autres".
        # On cible le vecteur blanc qui correspond à la direction de P (angle = PI/2)
        target_white_vec = make_arrow(
            P_start, P_start + np.array([0, 0.6, 0]),  # même style/longueur que radial_vectors
            color=WHITE, stroke_width=3, tip_size=0.12,
        )
        self.play(Transform(red_vector, target_white_vec), FadeOut(P_dot), FadeOut(P_label), run_time=1.2)
        self.wait(0.6)

        # Introduction de la sphère de Gauss (sans encore parler de norme constante)
        leg_4 = make_legend(
            "Traçons une sphère imaginaire de rayon $r$ centrée sur la charge."
        )

        gauss = DashedVMobject(
            Circle(radius=R_gauss, stroke_width=3).set_color(YELLOW),
            num_dashes=40,
        )
        r_line = Line(
            ORIGIN,
            R_gauss * np.array([np.cos(-PI / 4), np.sin(-PI / 4), 0]),
            stroke_width=2,
        )
        r_line.set_color(YELLOW)
        r_label = Tex("$r$", font_size=36)
        r_label.set_color(YELLOW)
        # Position : vers l'extérieur du rayon (70% de la longueur), décalé perpendiculairement
        r_point_along = np.array(
            [0.75 * R_gauss * np.cos(-PI / 4), 0.75 * R_gauss * np.sin(-PI / 4), 0]
        )
        r_label.move_to(r_point_along + 0.3 * np.array([-np.sin(-PI / 4), np.cos(-PI / 4), 0]))

        self.play(FadeOut(leg_3), FadeIn(leg_4), run_time=0.6)
        self.wait(0.3)
        self.play(Create(gauss), Create(r_line), Write(r_label), run_time=1.8)
        self.wait(0.8)

        # -------- ARGUMENT : pourquoi ||E|| est-il constant sur le cercle ? --------
        # Argument : prenons deux points P1, P2 à la même distance R. Une rotation
        # autour du centre les échange, et laisse la charge invariante.
        # Donc ||E(P1)|| = ||E(P2)||.
        leg_4b = make_legend(
            "Une rotation autour du centre échange deux points \\emph{à la même distance}."
        )
        self.play(FadeOut(leg_4), FadeIn(leg_4b), run_time=0.6)
        self.wait(0.6)

        # Deux points test sur le cercle de Gauss
        angle1 = 70 * DEGREES
        angle2 = -20 * DEGREES
        P1_pos = R_gauss * np.array([np.cos(angle1), np.sin(angle1), 0])
        P2_pos = R_gauss * np.array([np.cos(angle2), np.sin(angle2), 0])

        P1_dot = Dot(P1_pos, radius=0.09, color=GREEN)
        P2_dot = Dot(P2_pos, radius=0.09, color=GREEN)
        P1_label = Tex("$P_1$", font_size=34).set_color(GREEN).next_to(P1_dot, UR, buff=0.12)
        P2_label = Tex("$P_2$", font_size=34).set_color(GREEN).next_to(P2_dot, DR, buff=0.12)

        # Flèches E aux deux points (mêmes longueurs : on veut montrer l'égalité)
        E1 = make_arrow(P1_pos, P1_pos + 0.8 * np.array([np.cos(angle1), np.sin(angle1), 0]),
                        color=GREEN, stroke_width=5, tip_size=0.18)
        E2 = make_arrow(P2_pos, P2_pos + 0.8 * np.array([np.cos(angle2), np.sin(angle2), 0]),
                        color=GREEN, stroke_width=5, tip_size=0.18)

        self.play(
            FadeIn(P1_dot), Write(P1_label), FadeIn(E1),
            FadeIn(P2_dot), Write(P2_label), FadeIn(E2),
            run_time=1.2,
        )
        self.wait(0.8)

        # Arc de rotation pour visualiser l'opération qui amène P1 sur P2
        rot_arc = Arc(
            radius=R_gauss,
            start_angle=angle1,
            angle=angle2 - angle1,  # négatif ⇒ sens horaire
            color=GREEN_A,
            stroke_width=3,
        )

        leg_4c = make_legend(
            "Cette rotation amène $P_1 \\to P_2$ et laisse la charge invariante."
        )
        self.play(FadeOut(leg_4b), FadeIn(leg_4c), Create(rot_arc), run_time=1.0)
        self.wait(0.4)

        # On fait pivoter (P1, E1, P1_label) pour qu'il aille se superposer sur P2
        moving_group = VGroup(P1_dot, P1_label, E1)
        self.play(
            Rotate(moving_group, angle=angle2 - angle1, about_point=ORIGIN),
            run_time=2.0,
        )
        self.wait(1.0)

        # MAINTENANT on conclut : ||E(P1)|| = ||E(P2)||
        leg_4d = make_legend(
            "Donc $\\|\\vec{E}(P_1)\\| = \\|\\vec{E}(P_2)\\|$ : la norme est la même partout à distance $r$."
        )
        self.play(FadeOut(leg_4c), FadeIn(leg_4d), run_time=0.6)
        self.wait(2.0)

        # On nettoie avant de poser la conclusion finale
        self.play(
            FadeOut(moving_group), FadeOut(rot_arc),
            FadeOut(P2_dot), FadeOut(P2_label), FadeOut(E2),
            run_time=0.8,
        )

        # Conclusion finale
        leg_4_final = make_legend(
            "Conséquence : $\\|\\vec{E}\\|$ est constant sur toute sphère de rayon $r$."
        )
        self.play(FadeOut(leg_4d), FadeIn(leg_4_final), run_time=0.6)
        self.wait(0.4)
        # ---------------------------------------------------------------------------

        # Flèches E sur la surface de Gauss
        gauss_vectors = VGroup()
        for k in range(n_arrows):
            angle = k * TAU / n_arrows + PI / n_arrows
            d = np.array([np.cos(angle), np.sin(angle), 0])
            gauss_vectors.add(
                make_arrow(d * R_gauss, d * (R_gauss + 0.5),
                           color=YELLOW, stroke_width=3, tip_size=0.12)
            )

        self.play(
            LaggedStart(*[FadeIn(v) for v in gauss_vectors], lag_ratio=0.05),
            run_time=1.5,
        )
        self.wait(2.5)

    # ==============================================================
    # PARTIE 2 : PLAN INFINI
    # ==============================================================
    def _run_part2(self):
        make_legend = self._make_legend

        # Group (pas VGroup) : self.mobjects peut contenir des Mobject non-VMobject
        # issus de transformations précédentes — VGroup lèverait une exception.
        to_clear = [m for m in self.mobjects if m is not self._bg_rect]
        if to_clear:
            self.play(FadeOut(Group(*to_clear)), run_time=1.0)

        # ----- Titre partie 2 -----
        title_part2 = Tex("Plan infini chargé", font_size=40)
        title_part2.set_color(BLUE_A)
        title_part2.to_edge(UP, buff=0.3)
        self.play(FadeIn(title_part2), run_time=0.8)
        self.wait(0.4)

        # Vue en perspective simulée : un parallélogramme + vecteurs inclinés.
        # Pas de vraie 3D (ThreeDScene + move_camera serait trop lourd pour ce bout),
        # juste de la fausse perspective par interpolation 2D.
        depth_vec = np.array([0.6, 0.35, 0])  # compression + inclinaison

        plane_center_3d = np.array([0.0, -0.5, 0.0])
        half_w = 3.2  # demi-largeur du plan en perspective
        half_d = 1.6  # demi-profondeur

        # Les 4 coins du parallélogramme
        corner_fl = plane_center_3d + np.array([-half_w, 0, 0]) - half_d * depth_vec  # front-left
        corner_fr = plane_center_3d + np.array([+half_w, 0, 0]) - half_d * depth_vec  # front-right
        corner_br = plane_center_3d + np.array([+half_w, 0, 0]) + half_d * depth_vec  # back-right
        corner_bl = plane_center_3d + np.array([-half_w, 0, 0]) + half_d * depth_vec  # back-left

        plane_3d = Polygon(
            corner_fl, corner_fr, corner_br, corner_bl,
            stroke_width=3, fill_opacity=0.35,
        )
        plane_3d.set_stroke(BLUE_B)
        plane_3d.set_fill(BLUE_D)

        # Quelques "+" sur le plan 3D (répartis sur une grille en perspective)
        plane_3d_pluses = VGroup()
        for u in np.linspace(-0.8, 0.8, 4):
            for v in np.linspace(-0.8, 0.8, 3):
                pos = plane_center_3d + u * half_w * RIGHT + v * half_d * depth_vec
                p = Tex("+", font_size=22).set_color(BLUE_A)
                p.move_to(pos)
                plane_3d_pluses.add(p)

        # Vecteurs E perpendiculaires au plan (verticaux dans notre vue perspective)
        # On en place quelques-uns répartis sur le plan (au-dessus et en-dessous)
        field_arrows_3d = VGroup()
        for u in [-0.6, 0.0, 0.6]:
            for v in [-0.5, 0.5]:
                base = plane_center_3d + u * half_w * RIGHT + v * half_d * depth_vec
                # Vecteur vers le haut
                field_arrows_3d.add(make_arrow(
                    base, base + np.array([0, 1.0, 0]),
                    color=RED, stroke_width=4, tip_size=0.15,
                ))
                # Vecteur vers le bas
                field_arrows_3d.add(make_arrow(
                    base, base + np.array([0, -1.0, 0]),
                    color=RED, stroke_width=4, tip_size=0.15,
                ))

        intro_3d_legend = make_legend(
            "Plan infini uniformément chargé, vu en perspective."
        )

        self.play(FadeIn(plane_3d), FadeIn(intro_3d_legend), run_time=1.2)
        self.play(FadeIn(plane_3d_pluses), run_time=0.8)
        self.play(
            LaggedStart(*[FadeIn(a) for a in field_arrows_3d], lag_ratio=0.08),
            run_time=1.8,
        )
        self.wait(2.0)

        # Transition 3D → vue en coupe : on simule la caméra qui descend au niveau du plan.
        # Techniquement on interpole la composante Y du vecteur de profondeur de 0.35 à 0,
        # ce qui aplatit progressivement le parallélogramme en une ligne droite.
        transition_legend = make_legend(
            "Changement de point de vue : la caméra descend au niveau du plan."
        )

        # Nouveau titre avec "(vue en coupe)"
        new_title = Tex("Plan infini chargé (vue en coupe)", font_size=40)
        new_title.set_color(BLUE_A)
        new_title.to_edge(UP, buff=0.3)

        # On stocke les coordonnées (u, v) de chaque élément et on les re-projette
        # à chaque frame via un depth_vec qui interpole entre perspective et coupe.

        # (u, v) des "+" sur le plan
        plus_uvs = []
        for u in np.linspace(-0.8, 0.8, 4):
            for v in np.linspace(-0.8, 0.8, 3):
                plus_uvs.append((u, v))

        # (u, v) et direction (haut/bas) des flèches E
        arrow_specs = []
        for u in [-0.6, 0.0, 0.6]:
            for v in [-0.5, 0.5]:
                for sign in [+1, -1]:
                    arrow_specs.append((u, v, sign))

        depth_init = np.array([0.6, 0.35, 0.0])  # perspective initiale
        depth_final = np.array([0.6, 0.0, 0.0])  # plan vu parfaitement de côté

        def project(u, v, depth):
            """Projette un point (u, v) du plan abstrait dans la vue 2D."""
            return plane_center_3d + u * half_w * RIGHT + v * half_d * depth

        def update_scene(mob, alpha):
            """Met à jour plane_3d, les '+' et les flèches en fonction de alpha."""
            depth = depth_init + alpha * (depth_final - depth_init)

            # Nouveaux coins du parallélogramme
            c_fl = plane_center_3d + np.array([-half_w, 0, 0]) - half_d * depth
            c_fr = plane_center_3d + np.array([+half_w, 0, 0]) - half_d * depth
            c_br = plane_center_3d + np.array([+half_w, 0, 0]) + half_d * depth
            c_bl = plane_center_3d + np.array([-half_w, 0, 0]) + half_d * depth
            new_plane = Polygon(c_fl, c_fr, c_br, c_bl,
                                stroke_width=3, fill_opacity=0.35)
            new_plane.set_stroke(BLUE_B)
            new_plane.set_fill(BLUE_D)
            plane_3d.become(new_plane)

            # Nouveaux "+"
            for idx, (u, v) in enumerate(plus_uvs):
                plane_3d_pluses[idx].move_to(project(u, v, depth))

            # Nouvelles flèches : on reconstruit chaque flèche in-place
            for idx, (u, v, sign) in enumerate(arrow_specs):
                base = project(u, v, depth)
                tip_end = base + np.array([0, sign * 1.0, 0])
                new_arrow = make_arrow(
                    base, tip_end,
                    color=RED, stroke_width=4, tip_size=0.15,
                )
                field_arrows_3d[idx].become(new_arrow)

        self.play(
            FadeOut(intro_3d_legend),
            FadeIn(transition_legend),
            Transform(title_part2, new_title),
            UpdateFromAlphaFunc(plane_3d, update_scene),
            run_time=2.5,
        )
        self.wait(1.2)

        # Le parallélogramme est maintenant une ligne — on le remplace par une vraie Line
        # et on retire les éléments 3D pour passer à la représentation de coupe propre.
        plane_flat_y = plane_center_3d[1]
        plane_line_full = Line(
            [-6.5, plane_flat_y, 0],
            [+6.5, plane_flat_y, 0],
            stroke_width=6,
        )
        plane_line_full.set_color(BLUE_D)

        plane_y = plane_flat_y

        # Hachures (petits "+" pour indiquer la charge surfacique positive)
        plane_pluses = VGroup()
        for x in np.linspace(-5.5, 5.5, 12):
            p = Tex("+", font_size=28)
            p.set_color(BLUE_B)
            p.move_to([x, plane_y - 0.25, 0])
            plane_pluses.add(p)

        # Flèches en pointillés aux bords pour suggérer l'infini
        inf_left = make_arrow([-5.8, plane_y, 0], [-6.5, plane_y, 0],
                              color=BLUE_D, stroke_width=4, tip_size=0.2)
        inf_right = make_arrow([5.8, plane_y, 0], [6.5, plane_y, 0],
                               color=BLUE_D, stroke_width=4, tip_size=0.2)

        legend_p2 = make_legend(
            "Plan infini uniformément chargé : on cherche la direction de $\\vec{E}$."
        )

        self.play(
            FadeOut(plane_3d),  # parallélogramme aplati (redondant avec la future ligne)
            FadeOut(plane_3d_pluses),
            FadeOut(field_arrows_3d),
            FadeIn(plane_line_full),
            FadeIn(plane_pluses),
            FadeIn(inf_left), FadeIn(inf_right),
            FadeOut(transition_legend),
            FadeIn(legend_p2),
            run_time=1.5,
        )
        plane_line = plane_line_full
        self.wait(1.5)

        # ==========================================================
        # ARGUMENT 1 : INVARIANCE PAR TRANSLATION
        # ==========================================================
        # Point d'étude M au-dessus du plan
        M_start = np.array([0.0, plane_y + 1.6, 0.0])
        M_dot = Dot(point=M_start, radius=0.08, color=RED)
        M_label = Tex("$M$", font_size=34)
        M_label.set_color(RED)
        M_label.next_to(M_dot, RIGHT, buff=0.15)

        # Vecteur rouge initialement incliné (hypothèse : E a une composante parallèle au plan)
        E_tilt = make_arrow(
            M_start,
            M_start + np.array([0.9, 0.9, 0]),
            color=RED, stroke_width=6, tip_size=0.22,
        )

        leg_p2_1 = make_legend(
            "Hypothèse : $\\vec{E}(M)$ a une composante parallèle au plan."
        )
        self.play(
            FadeOut(legend_p2),
            FadeIn(leg_p2_1),
            FadeIn(M_dot), Write(M_label), FadeIn(E_tilt),
            run_time=1.2,
        )
        self.wait(1.8)

        # Translation horizontale du système (M + E) : le plan est inchangé, mais E a "bougé"
        leg_p2_2 = make_legend(
            "Translation le long du plan : plan inchangé, mais le point est déplacé."
        )
        self.play(FadeOut(leg_p2_1), FadeIn(leg_p2_2), run_time=0.7)
        self.wait(1.2)

        moving_system = VGroup(M_dot, M_label, E_tilt)
        self.play(
            moving_system.animate.shift(2.5 * RIGHT),
            run_time=1.8,
        )
        self.wait(0.6)
        self.play(
            moving_system.animate.shift(5.0 * LEFT),
            run_time=2.2,
        )
        self.wait(0.6)
        self.play(
            moving_system.animate.shift(2.5 * RIGHT),
            run_time=1.8,
        )
        self.wait(0.8)

        # Conclusion argument 1 : E ne dépend pas de la position le long du plan
        leg_p2_3 = make_legend(
            "Par invariance : $\\vec{E}$ ne dépend pas de la position \\emph{le long} du plan."
        )
        self.play(FadeOut(leg_p2_2), FadeIn(leg_p2_3), run_time=0.7)
        self.wait(2.0)

        # ==========================================================
        # ARGUMENT 2 : SYMÉTRIE MIROIR (plan miroir contenant la normale)
        # ==========================================================
        leg_p2_4 = make_legend(
            "On applique une symétrie miroir verticale passant par $M$."
        )
        self.play(FadeOut(leg_p2_3), FadeIn(leg_p2_4), run_time=0.7)
        self.wait(1.5)

        # Axe miroir vertical passant par M (pointillés)
        mirror_axis = DashedLine(
            M_start + np.array([0, 2.2, 0]),
            M_start + np.array([0, -2.2, 0]),
            stroke_width=2,
            dash_length=0.15,
        )
        mirror_axis.set_color(GREY_B)
        self.play(Create(mirror_axis), run_time=1.0)
        self.wait(0.5)

        # Symétrie par rapport à la verticale passant par M (x = M_start[0])
        def mirror(p):
            return np.array([2 * M_start[0] - p[0], p[1], p[2]])

        # Le plan est symétrique par rapport à cet axe, donc il ressort inchangé.
        # Seul E, incliné, bascule — c'est le paradoxe qu'on veut montrer.
        leg_p2_4b = make_legend(
            "Le plan est invariant par ce miroir (il reste identique)..."
        )
        full_scene = VGroup(plane_line, plane_pluses, inf_left, inf_right, M_dot, E_tilt)

        # Petit flash lumineux sur le plan pour signaler qu'on l'inclut dans la transformation
        plane_highlight = plane_line.copy().set_color(YELLOW).set_stroke(width=8)

        self.play(
            FadeOut(leg_p2_4),
            FadeIn(leg_p2_4b),
            Flash(M_dot, color=WHITE, flash_radius=0.3, num_lines=8, run_time=0.8),
            run_time=0.8,
        )
        self.wait(0.8)
        # Flash du plan pour montrer qu'on lui applique bien la transformation
        self.play(
            Create(plane_highlight),
            rate_func=there_and_back,
            run_time=1.4,
        )
        self.remove(plane_highlight)
        self.wait(0.6)

        # apply_function(mirror) : le plan et les "+" restent en place, E bascule
        leg_p2_4c = make_legend(
            "...mais $\\vec{E}$, lui, bascule. Absurde !"
        )
        self.play(
            FadeOut(leg_p2_4b),
            FadeIn(leg_p2_4c),
            full_scene.animate.apply_function(mirror),
            run_time=2.2,
        )
        self.wait(1.8)

        # Conclusion argument 2 : E doit être sur l'axe miroir ⇒ perpendiculaire au plan
        leg_p2_5 = make_legend(
            "$\\vec{E}$ doit donc être porté par l'axe miroir : perpendiculaire au plan."
        )
        self.play(FadeOut(leg_p2_4c), FadeIn(leg_p2_5), run_time=0.7)
        self.wait(1.5)

        # On redresse E vers le haut (perpendiculaire au plan)
        E_perp = make_arrow(
            M_start,
            M_start + np.array([0, 1.2, 0]),
            color=RED, stroke_width=6, tip_size=0.22,
        )
        self.play(
            FadeOut(E_tilt),
            FadeIn(E_perp),
            FadeOut(mirror_axis),
            run_time=1.2,
        )
        self.wait(1.0)

        # Argument 3 : pourquoi E est indépendant de la distance z au plan ?
        # Quand M s'éloigne, chaque dE diminue en 1/r² — mais simultanément, les dE
        # deviennent plus verticaux (leurs composantes horizontales s'annulent par symétrie).
        # Pour un plan infini ces deux effets se compensent exactement : E reste constant.
        leg_p2_6 = make_legend(
            "Regardons les contributions $d\\vec{E}$ de chaque élément d'aire $dA$ du plan."
        )
        self.play(FadeOut(leg_p2_5), FadeIn(leg_p2_6), run_time=0.7)
        self.wait(1.2)

        # Positions des éléments dl sur le plan (symétriques par rapport à x=0)
        dl_positions_x = np.array([-2.8, -1.6, -0.8, 0.0, 0.8, 1.6, 2.8])
        dl_dots = VGroup()
        for xdl in dl_positions_x:
            d = Dot([xdl, plane_y, 0], radius=0.06, color=BLUE_A)
            dl_dots.add(d)
        dl_label = Tex("$dA$", font_size=26).set_color(BLUE_A)
        dl_label.next_to(dl_dots[-1], DOWN, buff=0.15)

        self.play(FadeIn(dl_dots), Write(dl_label), run_time=1.2)
        self.wait(0.8)

        # E_perp va être remplacé par un vecteur "somme" reconstruit via UpdateFromAlphaFunc.
        z_initial = M_start[1] - plane_y  # ~1.6
        # On a un nombre FINI d'éléments dA, donc la somme n'est qu'approximative.
        # On impose une norme fixe à la flèche résultante — c'est ce que la physique prédit.
        E_total_norm = 1.2  # longueur de la flèche résultante

        def build_dE_arrows(z, alpha_global=1.0):
            """Construit les flèches dE ancrées en M(0, plane_y + z), pointant dans
            la direction dl→M (prolongation de la ligne dl-M). Chaque dE est
            accompagnée d'une ligne pointillée semi-transparente reliant dl à M.
            Retourne (VGroup dE, VGroup lignes pointillées, flèche somme E)."""
            M_pos = np.array([0.0, plane_y + z, 0.0])
            dE_group = VGroup()
            dash_group = VGroup()
            # Constante calibrée pour que la flèche la plus proche reste de taille raisonnable
            k = 0.8 * z_initial ** 2
            for xdl in dl_positions_x:
                dl_pos = np.array([xdl, plane_y, 0])
                r_vec = M_pos - dl_pos  # direction dl -> M
                r = np.linalg.norm(r_vec)
                if r < 0.01:
                    continue
                r_hat = r_vec / r
                dE_length = k / (r ** 2)
                dE_length = min(dE_length, 1.4)  # plafond de sécurité

                # Flèche dE : ancrée EN M, pointant dans la direction r_hat (prolongation)
                dE_start = M_pos
                dE_end = M_pos + r_hat * dE_length
                arrow = make_arrow(
                    dE_start, dE_end,
                    color=ORANGE, stroke_width=3, tip_size=0.10,
                )
                arrow.set_opacity(alpha_global)
                dE_group.add(arrow)

                # Ligne pointillée semi-transparente de dl à M
                dash = DashedLine(
                    dl_pos, M_pos,
                    stroke_width=1.5,
                    dash_length=0.08,
                )
                dash.set_color(GREY_B)
                dash.set_stroke(opacity=0.4)
                dash_group.add(dash)

            # Flèche somme E (verticale, norme fixe = E_total_norm)
            E_sum = make_arrow(
                M_pos,
                M_pos + np.array([0, E_total_norm, 0]),
                color=RED, stroke_width=6, tip_size=0.22,
            )
            return dE_group, dash_group, E_sum

        dE_arrows, dash_lines, _ = build_dE_arrows(z_initial)
        # E_perp reprendra l'apparence cible via Transform — on le garde sous le nom
        # E_perp_current pour pouvoir continuer à le passer au conteneur d'animation.
        E_perp_target = make_arrow(
            M_start, M_start + np.array([0, E_total_norm, 0]),
            color=RED, stroke_width=6, tip_size=0.22,
        )
        self.play(
            Transform(E_perp, E_perp_target),
            FadeIn(dash_lines),
            LaggedStart(*[FadeIn(a) for a in dE_arrows], lag_ratio=0.08),
            run_time=1.8,
        )
        E_perp_current = E_perp
        self.wait(1.5)

        # ---- Éloignement de M : on voit les dE devenir plus verticaux ----
        leg_p2_7 = make_legend(
            "Éloignons $M$ : chaque $d\\vec{E}$ diminue, mais devient plus vertical."
        )
        self.play(FadeOut(leg_p2_6), FadeIn(leg_p2_7), run_time=0.7)
        self.wait(1.0)

        # UpdateFromAlphaFunc permet de tout faire bouger ensemble (M, dE, E) en un seul play
        container = VGroup(dE_arrows, dash_lines, E_perp_current, M_dot, M_label)

        z_initial_val = z_initial
        z_final_val = 3.2  # M monte à ~3.2 au-dessus du plan

        def update_container(mob, alpha):
            z = z_initial_val + alpha * (z_final_val - z_initial_val)
            M_pos = np.array([0.0, plane_y + z, 0.0])
            # Met à jour M_dot
            M_dot.move_to(M_pos)
            M_label.next_to(M_dot, RIGHT, buff=0.15)
            # Met à jour E_perp_current (toujours de norme E_total_norm)
            new_E = make_arrow(
                M_pos, M_pos + np.array([0, E_total_norm, 0]),
                color=RED, stroke_width=6, tip_size=0.22,
            )
            E_perp_current.become(new_E)
            # Met à jour dE et lignes pointillées
            new_dEs, new_dashes, _ = build_dE_arrows(z)
            for i, new_arrow in enumerate(new_dEs):
                if i < len(dE_arrows):
                    dE_arrows[i].become(new_arrow)
            for i, new_dash in enumerate(new_dashes):
                if i < len(dash_lines):
                    dash_lines[i].become(new_dash)

        self.play(
            UpdateFromAlphaFunc(container, update_container),
            run_time=3.5,
            rate_func=smooth,
        )
        self.wait(1.5)

        # Retour vers le plan — on montre que les dE grossissent mais s'inclinent, bilan identique
        leg_p2_8 = make_legend(
            "Rapprochons $M$ : les $d\\vec{E}$ grandissent, mais s'inclinent davantage."
        )
        self.play(FadeOut(leg_p2_7), FadeIn(leg_p2_8), run_time=0.7)
        self.wait(0.8)

        def update_container_back(mob, alpha):
            z = z_final_val + alpha * (z_initial_val - z_final_val)
            M_pos = np.array([0.0, plane_y + z, 0.0])
            M_dot.move_to(M_pos)
            M_label.next_to(M_dot, RIGHT, buff=0.15)
            new_E = make_arrow(
                M_pos, M_pos + np.array([0, E_total_norm, 0]),
                color=RED, stroke_width=6, tip_size=0.22,
            )
            E_perp_current.become(new_E)
            new_dEs, new_dashes, _ = build_dE_arrows(z)
            for i, new_arrow in enumerate(new_dEs):
                if i < len(dE_arrows):
                    dE_arrows[i].become(new_arrow)
            for i, new_dash in enumerate(new_dashes):
                if i < len(dash_lines):
                    dash_lines[i].become(new_dash)

        self.play(
            UpdateFromAlphaFunc(container, update_container_back),
            run_time=3.0,
            rate_func=smooth,
        )
        self.wait(1.2)

        # ---- Conclusion : les deux effets se compensent → E uniforme ----
        leg_p2_9 = make_legend(
            "Les deux effets se compensent exactement : $\\vec{E}$ ne dépend pas de la distance !"
        )
        self.play(FadeOut(leg_p2_8), FadeIn(leg_p2_9), run_time=0.7)
        self.wait(2.5)

        # Nettoyage : on enlève les dE pour laisser parler le champ résultant seul
        self.play(
            FadeOut(dE_arrows),
            FadeOut(dash_lines),
            FadeOut(dl_dots),
            FadeOut(dl_label),
            run_time=1.2,
        )
        self.wait(0.5)

        # ==========================================================
        # CONCLUSION FINALE : champ uniforme sur tout l'espace
        # ==========================================================
        leg_p2_10 = make_legend(
            "Conclusion : $\\vec{E}$ est perpendiculaire au plan et \\emph{uniforme}."
        )
        self.play(FadeOut(leg_p2_9), FadeIn(leg_p2_10), run_time=0.7)
        self.wait(1.2)

        # Toutes les flèches ont la même longueur — c'est exactement le résultat qu'on vient de démontrer
        E_field = VGroup()
        for x in np.linspace(-4.5, 4.5, 5):
            if abs(x) < 0.1:  # on saute celle au centre (où est M)
                continue
            # Au-dessus
            E_field.add(make_arrow(
                [x, plane_y + 0.1, 0], [x, plane_y + 1.3, 0],
                color=RED, stroke_width=5, tip_size=0.18,
            ))
            # En-dessous (symétrique)
            E_field.add(make_arrow(
                [x, plane_y - 0.4, 0], [x, plane_y - 1.6, 0],
                color=RED, stroke_width=5, tip_size=0.18,
            ))

        # M a pu bouger pendant l'animation — on récupère sa position actuelle
        M_current = M_dot.get_center()
        E_below_M = make_arrow(
            [M_current[0], plane_y - 0.4, 0],
            [M_current[0], plane_y - 1.6, 0],
            color=RED, stroke_width=6, tip_size=0.22,
        )

        self.play(FadeIn(E_field), FadeIn(E_below_M), run_time=1.8)
        self.wait(3.5)


# Scènes autonomes — pratique pour rendre une partie sans attendre l'autre :
#   manim -pql symetrieplaninfini.py SymetrieSpherique   (partie 1 seule)
#   manim -pql symetrieplaninfini.py PlanInfini          (partie 2 seule)
#   manim -pql symetrieplaninfini.py SymetrieSpherique2D (vidéo complète)


class SymetrieSpherique(SymetrieSpherique2D):
    """Vidéo autonome : seulement la symétrie sphérique (partie 1)."""

    def construct(self):
        self._run_setup_legend()
        self._run_part1()


class PlanInfini(SymetrieSpherique2D):
    """Vidéo autonome : seulement le plan infini (partie 2)."""

    def construct(self):
        self._run_setup_legend()
        self._run_part2()