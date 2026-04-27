from manim import *
import numpy as np

def b_color_from_dot(dp: float):
    """Vert si B pousse avec dl (+), Rouge si opposé (-)."""
    if dp > 0.05:   return GREEN
    if dp < -0.05:  return RED
    return GRAY

class AmpereLaw(ThreeDScene):
    def construct(self):
        self.setup_3d_scene()
        self.transition_to_pure_2d()
        self.phase_moving_wire_and_b_field()
        self.phase_zoomed_sweep()

    # ══════════════════════════════════════════════════════════════
    # PHASE 1 — Vue 3D, champ B anti-horaire
    # ══════════════════════════════════════════════════════════════
    # Mêmes rayons partagés entre la vue 3D et la vue 2D : sans ça, on voit un petit
    # saut visuel au moment de la transition, ce qui casse l'effet de continuité.
    FIELD_RADII = [0.8, 1.6, 2.4, 3.2, 4.0, 4.8]

    def setup_3d_scene(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-55 * DEGREES)

        self.ground = Rectangle(width=12, height=12, color=BLUE_E, fill_opacity=0.15, stroke_width=1)
        self.ground.shift(DOWN * 1.5)

        self.axes = ThreeDAxes(x_range=[-4, 4], y_range=[-4, 4], z_range=[-2, 3], 
                               axis_config={"color": GRAY, "stroke_width": 2})

        self.wire_3d = Line(
            np.array([0, -6, 0]), np.array([0, 6, 0]), 
            color=WHITE, stroke_width=12
        )

        # Flèche du courant placée près du haut du fil — meilleure lisibilité à l'écran
        self.arr_I = Arrow(np.array([0.4, -2.5, 0]), np.array([0.4, -5, 0]), color=RED, stroke_width=6)

        self.b_rings_3d = VGroup()
        for r in self.FIELD_RADII[:3]:   # 3 anneaux suffisent en 3D, au-delà ça surcharge la vue
            op = max(0.1, 0.95 - r * 0.22)
            arc = Arc(radius=r, start_angle=PI/2, angle=TAU * 0.9, color=YELLOW, stroke_opacity=op)
            arc.rotate(PI/2, RIGHT)
            arc.add_tip(tip_length=0.18, tip_width=0.12)
            self.b_rings_3d.add(arc)

        self.play(FadeIn(self.ground), Create(self.axes), FadeIn(self.wire_3d), Create(self.arr_I))
        # Les anneaux apparaissent doucement : on a le temps de comprendre qu'ils tournent autour du fil
        self.play(Create(self.b_rings_3d), run_time=3.0, rate_func=linear)
        self.wait(1.5)

    # ══════════════════════════════════════════════════════════════
    # Transition 3D → 2D : on bascule la caméra pour passer en vue de dessus
    # ══════════════════════════════════════════════════════════════
    def transition_to_pure_2d(self):
        self.move_camera(phi=90 * DEGREES, theta=-90 * DEGREES, run_time=2.5)
        self.wait(0.5)

        self.formula = MathTex(
            r"\oint ", r"\vec{B}", r" \cdot d\vec{l} = \mu_0 I_{\mathrm{in}}"
        ).scale(0.8).to_corner(UL)
        self.formula[1].set_color(YELLOW)
        self.add_fixed_in_frame_mobjects(self.formula)
        self.play(Write(self.formula))

        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)

        self.wire_2d = VGroup(
            Circle(radius=0.18, color=WHITE, stroke_width=2.5),
            Dot(radius=0.06, color=WHITE)
        ).move_to(ORIGIN)

        # Attention au piège classique : avec Arc(TAU*0.9), la bounding-box n'est pas
        # symétrique, et chaque rayon se décale d'un cheveu différent — résultat,
        # les cercles ne sont plus concentriques à l'écran. Un Circle complet, lui,
        # est centré pile sur ORIGIN. La pointe est rajoutée à la main par-dessus.
        def make_field_circle(r):
            op = max(0.05, 0.55 - r * 0.08)
            circ = Circle(radius=r, color=YELLOW, stroke_width=1)
            circ.set_stroke(opacity=op)
            # Le Circle est déjà centré sur ORIGIN, donc rien à faire de ce côté.
            # On colle juste une petite pointe de flèche à PI/4 pour rappeler le sens anti-horaire.
            tip_angle = PI / 4
            tip_pos = np.array([r * np.cos(tip_angle), r * np.sin(tip_angle), 0])
            # Le Triangle par défaut pointe vers le haut, donc il faut le tourner
            # pour qu'il suive la tangente du cercle dans le bon sens.
            tip = Triangle(color=YELLOW, fill_opacity=op, stroke_width=0)
            tip.set_height(0.12)
            tip.rotate(tip_angle)  # ce qui revient à PI/2 + tip_angle au total
            tip.move_to(tip_pos)
            return VGroup(circ, tip)

        self.ghost_field = VGroup(*[make_field_circle(r) for r in self.FIELD_RADII])

        self.remove(self.ground, self.axes, self.wire_3d, self.arr_I, self.b_rings_3d)
        self.add(self.wire_2d, self.ghost_field)
        self.wait(0.5)

    # ══════════════════════════════════════════════════════════════
    # PHASE 2 — On compare B et dl le long du contour
    # ══════════════════════════════════════════════════════════════
    def phase_moving_wire_and_b_field(self):
        LOOP_R = 2.4
        self.loop = Circle(radius=LOOP_R, color=WHITE, stroke_width=2.5, stroke_opacity=0.8)
        self.play(Create(self.loop))

        N = 16
        self.angles = np.linspace(0, TAU, N, endpoint=False)
        self.loop_pts = [np.array([LOOP_R * np.cos(a), LOOP_R * np.sin(a), 0]) for a in self.angles]
        
        dl_group = VGroup(*[
            Arrow(pt, pt + 0.38 * np.array([-np.sin(a), np.cos(a), 0]), color=BLUE, buff=0, tip_length=0.15, stroke_width=3)
            for pt, a in zip(self.loop_pts, self.angles)
        ])
        self.play(FadeIn(dl_group))

        # Une seule étiquette "dl" sur un endroit lisible vaut mieux que 16 étiquettes empilées
        ref_idx = 2   # en haut à droite, là où c'est bien dégagé
        ref_pt  = self.loop_pts[ref_idx]
        ref_a   = self.angles[ref_idx]
        dl_dir_ref = np.array([-np.sin(ref_a), np.cos(ref_a), 0])
        label_dl = MathTex(r"d\vec{l}", color=BLUE, font_size=26).move_to(
            ref_pt + dl_dir_ref * 0.65 + np.array([-0.15, 0.25, 0])
        )
        self.add_fixed_in_frame_mobjects(label_dl)
        self.play(FadeIn(label_dl))

        self.b_vec_group = VGroup(*[Arrow(ORIGIN, RIGHT, buff=0) for _ in range(N)])
        
        def update_b_vectors(grp):
            wc = self.wire_2d.get_center()
            new_grp = VGroup()
            for pt, a in zip(self.loop_pts, self.angles):
                r_vec = pt - wc
                dist = np.linalg.norm(r_vec)
                if dist < 0.1: continue
                
                b_dir = np.array([-r_vec[1], r_vec[0], 0]) / dist
                b_mag = min(0.8, 0.7 / dist)
                dl_dir = np.array([-np.sin(a), np.cos(a), 0])
                dp = float(np.dot(b_dir, dl_dir))
                
                arr = Arrow(pt, pt + b_dir * b_mag, color=b_color_from_dot(dp), buff=0, tip_length=0.15, stroke_width=3)
                new_grp.add(arr)
            grp.become(new_grp)

        update_b_vectors(self.b_vec_group)
        self.add(self.b_vec_group)
        self.b_vec_group.add_updater(update_b_vectors)
        self.wait(1)

        txt_out = Text("Si le fil sort du contour...", font_size=20, color=YELLOW).next_to(self.formula, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(txt_out)
        self.play(Write(txt_out))

        self.play(
            self.wire_2d.animate.move_to(RIGHT * 4.2), self.ghost_field.animate.move_to(RIGHT * 4.2),
            run_time=3, rate_func=smooth
        )

        # Pour la légende : \textcolor demande le package xcolor et fait planter la
        # compilation latex→dvi. Bien plus simple : couper la formule en morceaux et
        # colorer chaque morceau avec set_color() côté Manim.
        line_green = MathTex(r"\bullet\ ", r"\text{Vert}", r" : \vec{B} \cdot d\vec{l} > 0", font_size=22)
        line_green[1].set_color(GREEN)
        line_red   = MathTex(r"\bullet\ ", r"\text{Rouge}", r" : \vec{B} \cdot d\vec{l} < 0", font_size=22)
        line_red[1].set_color(RED)
        txt_forces = VGroup(line_green, line_red).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(txt_out, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(txt_forces)
        self.play(Write(txt_forces))
        self.wait(2)

        txt_cancel = Text("=> Les contributions s'annulent", font_size=20, color=ORANGE).next_to(txt_forces, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(txt_cancel)
        self.play(Write(txt_cancel))
        self.wait(3)

        self.b_vec_group.remove_updater(update_b_vectors)
        self.remove_fixed_in_frame_mobjects(label_dl)
        self.play(
            FadeOut(txt_out, txt_forces, txt_cancel, self.b_vec_group, dl_group, self.loop, label_dl),
            self.wire_2d.animate.move_to(ORIGIN), self.ghost_field.animate.move_to(ORIGIN)
        )

    # ══════════════════════════════════════════════════════════════
    # PHASE 3 — On balaye un contour quelconque, caméra qui suit
    # ══════════════════════════════════════════════════════════════
    def phase_zoomed_sweep(self):
        title = Text("Pourquoi la forme n'importe pas ?", font_size=24, color=YELLOW).next_to(self.formula, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        # On commence par un cercle, c'est rassurant visuellement
        current_shape = Circle(radius=1.8, color=GREEN, stroke_width=3)
        self.play(Create(current_shape))

        ellipse = Ellipse(width=5.2, height=2.4, color=GREEN, stroke_width=3)
        self.play(Transform(current_shape, ellipse), run_time=1.5)

        # Le tracker qui pilote le balayage : il va de 0 (départ) à 1 (tour complet)
        tracker = ValueTracker(0)

        exp_math = MathTex(r"\vec{B} \cdot d\vec{l} = B_{\parallel} \cdot dl", font_size=24, color=YELLOW).next_to(title, DOWN, aligned_edge=LEFT, buff=0.3)
        self.add_fixed_in_frame_mobjects(exp_math)

        # Le "blob" : exprès biscornu, pour bien casser l'idée que la forme doit être régulière
        blob_pts = [
            [-2.4,  0.3, 0], [-2.6, -1.3, 0], [-1.2, -2.6, 0],
            [ 0.1, -1.8, 0], [ 1.6, -2.5, 0], [ 3.1, -1.5, 0],
            [ 2.5, -0.3, 0], [ 3.0,  1.1, 0], [ 2.0,  2.9, 0],
            [ 0.9,  2.3, 0], [-0.8,  2.8, 0], [-2.0,  1.8, 0],
        ]
        blob = VMobject(color=GREEN, stroke_width=3)
        blob.set_points_as_corners([np.array(p) for p in blob_pts + [blob_pts[0]]])
        blob.make_smooth()
        
        self.play(Transform(current_shape, blob), Write(exp_math), run_time=1.5)

        # ── Suivi caméra ──────────────────────────────
        # (le tracker a déjà été créé plus haut)

        # On part de la position correspondant à la proportion 0 sur le blob
        start_pt = blob.point_from_proportion(0.0)

        # Un point invisible qui se balade sur le contour, et que la caméra va suivre
        cam_anchor = Dot(radius=0, fill_opacity=0)
        cam_anchor.move_to(start_pt)
        cam_anchor.add_updater(
            lambda d: d.move_to(blob.point_from_proportion(tracker.get_value() % 1.0))
        )
        self.add(cam_anchor)

        self.camera.frame_center[:] = start_pt
        self.move_camera(focal_point=start_pt, zoom=3.0, run_time=1.5)

        def _follow_camera(dt):
            self.camera.frame_center[:] = cam_anchor.get_center()

        self.add_updater(_follow_camera)

        # Le petit point lumineux qu'on voit glisser sur le contour
        sweep_dot = Dot(radius=0.08, color=WHITE, fill_opacity=0.9)
        sweep_dot.add_updater(
            lambda d: d.move_to(blob.point_from_proportion(tracker.get_value() % 1.0))
        )
        self.add(sweep_dot)

        # ── Tout ce qui s'affiche pendant le balayage ────────────────────────────────────────
        sweep_group = VGroup()

        def update_sweep(grp):
            alpha = tracker.get_value() % 1.0
            pt = blob.point_from_proportion(alpha)

            pt_next = blob.point_from_proportion((alpha + 0.003) % 1.0)
            raw = pt_next - pt
            norm = np.linalg.norm(raw)
            if norm < 1e-6:
                return
            dl_dir = raw / norm

            wc = self.wire_2d.get_center()
            r_vec = pt - wc
            dist = np.linalg.norm(r_vec)
            if dist < 1e-6:
                return
            b_dir = np.array([-r_vec[1], r_vec[0], 0]) / dist

            B_full     = b_dir * 1.6
            B_par_vec  = np.dot(B_full, dl_dir) * dl_dir
            B_perp_vec = B_full - B_par_vec

            radial_line = Line(wc, pt, color=WHITE, stroke_width=1.5).set_stroke(opacity=0.3)
            arr_dl    = Arrow(pt, pt + dl_dir * 1.0, color=BLUE,   buff=0, stroke_width=12, tip_length=0.25)
            arr_bpar  = Arrow(pt, pt + B_par_vec,    color=YELLOW,  buff=0, stroke_width=7,  tip_length=0.2)
            arr_bperp = Arrow(pt, pt + B_perp_vec,   color=RED,     buff=0, stroke_width=7,  tip_length=0.2)
            l_dl    = MathTex(r"d\vec{l}",       color=BLUE,   font_size=32).next_to(arr_dl.get_end(),    dl_dir, buff=0.1)
            l_bp    = MathTex(r"B_{\parallel}",  color=YELLOW, font_size=32).next_to(arr_bpar.get_end(),  dl_dir, buff=0.1)
            l_bperp = MathTex(r"B_{\perp}",      color=RED,    font_size=28).next_to(arr_bperp.get_end(), np.array([-dl_dir[1], dl_dir[0], 0]), buff=0.08)

            grp.become(VGroup(radial_line, arr_dl, arr_bpar, arr_bperp, l_dl, l_bp, l_bperp))

        sweep_group.add_updater(update_sweep)
        self.add(sweep_group)

        # 15 secondes de balayage, vitesse constante : on a le temps de voir B_para se "moyenner"
        self.play(tracker.animate.set_value(1.0), run_time=15, rate_func=linear)

        # ── Nettoyage ───────────────────────────────────────────────
        sweep_group.remove_updater(update_sweep)
        self.remove_updater(_follow_camera)
        cam_anchor.clear_updaters()
        sweep_dot.clear_updaters()

        self.move_camera(focal_point=ORIGIN, zoom=1.0, run_time=2)
        self.play(FadeOut(sweep_group, sweep_dot))

        conclusion = Text(
            "Peu importe la forme, l'angle balayé reste 360°.\nLa loi d'Ampère est universelle.",
            font_size=20, color=GREEN
        ).next_to(exp_math, DOWN, aligned_edge=LEFT, buff=0.5)
        self.add_fixed_in_frame_mobjects(conclusion)
        self.play(Write(conclusion))
        self.wait(3)