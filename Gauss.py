from manim import *
import numpy as np

class GaussAdvanced(ThreeDScene):
    def construct(self):
        # ─────────────────────────────────────────────
        # 1. Mise en place de la scène 3D et des formules
        # ─────────────────────────────────────────────
        # On commence en vue 3D, ça donne tout de suite l'impression de volume
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        self.add(NumberPlane(background_line_style={"stroke_opacity": 0.1}))
        
        gauss_formula = MathTex(
            r"\oint \vec{E} \cdot d\vec{A} = \frac{Q_{\text{int}}}{\varepsilon_0}",
            color=WHITE
        ).to_corner(UL).scale(0.8)
        
        flux_def = MathTex(
            r"\Phi_E \propto \text{Sorties} - \text{Entrées}", 
            color=YELLOW
        ).next_to(gauss_formula, DOWN, aligned_edge=LEFT).scale(0.6)
        
        self.add_fixed_in_frame_mobjects(gauss_formula, flux_def)

        # ─────────────────────────────────────────────
        # 2. Phase 1 : on dessine un champ radial 3D, puis on bascule en 2D
        # ─────────────────────────────────────────────
        q_pos_ref = Dot(point=ORIGIN, fill_opacity=0) 
        self.add(q_pos_ref)

        charge = always_redraw(lambda: Dot(q_pos_ref.get_center(), color=RED).scale(2.5))
        q_label = always_redraw(lambda: MathTex("+Q", color=RED).scale(0.6).next_to(charge, UP, buff=0.1))
        
        # Vecteurs du champ en 3D, volontairement fins pour un rendu propre
        e_field_3d = VGroup()
        for theta in np.linspace(0, 2 * PI, 8, endpoint=False):
            for phi in [PI/4, PI/2, 3*PI/4]:
                direction = np.array([np.sin(phi)*np.cos(theta), np.sin(phi)*np.sin(theta), np.cos(phi)])
                start_pt = direction * 0.2
                end_pt = direction * 1.7
                # Arrow plutôt qu'Arrow3D : plus fin, plus contrôlable visuellement
                vec = Arrow(start_pt, end_pt, color=RED, stroke_width=2, tip_length=0.15, buff=0)
                e_field_3d.add(vec)

        self.play(FadeIn(charge), Write(q_label))
        self.play(Create(e_field_3d))
        self.wait(1)

        # Bascule vers la vue 2D (caméra à la verticale au-dessus de la scène)
        self.move_camera(phi=0, theta=-90 * DEGREES, run_time=2)
        self.play(FadeOut(e_field_3d))

        # ─────────────────────────────────────────────
        # 3. Les deux surfaces de Gauss : un cercle, puis une "patate" déformée
        # ─────────────────────────────────────────────
        # Le cercle est représenté par 100 points, pour pouvoir morpher proprement vers la patate plus tard
        circle_temp = Circle(radius=2.2)
        circle_pts = np.array([circle_temp.point_from_proportion(a) for a in np.linspace(0, 1, 100, endpoint=False)])

        # Même nombre de points pour la patate, sinon le morphing devient laid
        potato_points = [
            [2.5, 0, 0], [1.5, 2, 0], [-1.5, 1.5, 0], 
            [-2.5, -0.5, 0], [-1, -2.5, 0], [1.5, -1.5, 0]
        ]
        potato_temp = Polygon(*potato_points).round_corners(radius=1)
        potato_pts = np.array([potato_temp.point_from_proportion(a) for a in np.linspace(0, 1, 100, endpoint=False)])

        # Au démarrage, la surface est un cercle ; elle deviendra une patate par Transform()
        surface = Polygon(*circle_pts, color=BLUE_B, fill_opacity=0.1)
        self.play(Create(surface))

        # ─────────────────────────────────────────────
        # 4. Calcul des intersections rayon ↔ surface (vectorisé en NumPy)
        # ─────────────────────────────────────────────
        def get_math_intersections(ray_origin, ray_direction):
            # get_vertices() rend les 100 points actuels de la forme (suit le morphing)
            cached_pts = surface.get_vertices()
            p1_array = cached_pts
            p2_array = np.roll(cached_pts, -1, axis=0)
            v2_array = p2_array - p1_array
            
            v1_array = ray_origin - p1_array
            denom = ray_direction[0] * v2_array[:, 1] - ray_direction[1] * v2_array[:, 0]
            valid = np.abs(denom) > 1e-6
            
            t = np.zeros(len(cached_pts))
            u = np.zeros(len(cached_pts))
            t[valid] = (v2_array[valid, 0] * v1_array[valid, 1] - v2_array[valid, 1] * v1_array[valid, 0]) / denom[valid]
            u[valid] = (ray_direction[0] * v1_array[valid, 1] - ray_direction[1] * v1_array[valid, 0]) / denom[valid]
            
            intersect_mask = valid & (t >= 0) & (u >= 0.0) & (u < 1.0)
            valid_t = t[intersect_mask]
            
            # On trie par distance : la première intersection est l'entrée, la dernière la sortie
            valid_t.sort()
            return [ray_origin + t_val * ray_direction for t_val in valid_t]

        # ─────────────────────────────────────────────
        # 5. Lignes de champ dynamiques + logique pédagogique entrée/sortie
        # ─────────────────────────────────────────────
        num_lines = 16 
        
        field_lines = always_redraw(lambda: VGroup(*[
            Line(q_pos_ref.get_center(), q_pos_ref.get_center() + rotate_vector(RIGHT*10, a), 
                 color=RED, stroke_width=1.5, stroke_opacity=0.6)
            for a in np.linspace(0, 2*PI, num_lines, endpoint=False)
        ]))

        def get_intersection_dots():
            dots = VGroup()
            origin = q_pos_ref.get_center()
            for a in np.linspace(0, 2*PI, num_lines, endpoint=False):
                direction = np.array([np.cos(a), np.sin(a), 0])
                inters = get_math_intersections(origin, direction)
                
                # Code couleur : rouge pour une entrée, vert pour une sortie
                if len(inters) == 1:
                    dots.add(Dot(inters[0], color=GREEN).scale(1.2))
                elif len(inters) >= 2:
                    dots.add(Dot(inters[0], color=RED).scale(1.2))   
                    dots.add(Dot(inters[-1], color=GREEN).scale(1.2)) 
            return dots

        intersection_dots = always_redraw(get_intersection_dots)

        def is_charge_inside():
            origin = q_pos_ref.get_center()
            inters = get_math_intersections(origin, np.array([1.0, 0.0, 0.0]))
            return len(inters) % 2 != 0

        counter = always_redraw(lambda: Text(
            f"Flux Net : {num_lines if is_charge_inside() else 0}", 
            color=YELLOW
        ).scale(0.5).to_corner(UR))

        self.add_fixed_in_frame_mobjects(counter)
        self.play(Create(field_lines), FadeIn(intersection_dots))
        self.wait(1)

        # ─────────────────────────────────────────────
        # 6. Enchaînement des séquences pédagogiques
        # ─────────────────────────────────────────────

        # --- Séquence 1 : la forme se déforme, mais le flux ne bouge pas ---
        note_shape = Text("Le flux est indépendant de la forme de la surface", color=WHITE).scale(0.4).to_edge(DOWN)
        target_surface = Polygon(*potato_pts, color=BLUE_B, fill_opacity=0.1)
        
        self.play(Write(note_shape))
        # Comme tout est branché à get_vertices(), les points d'intersection suivent le morphing en direct
        self.play(Transform(surface, target_surface), run_time=3)
        self.wait(1)
        self.play(FadeOut(note_shape))

        # --- Séquence 2 : la charge reste à l'intérieur, on la promène un peu ---
        note_inside1 = Text("À l'intérieur : Chaque ligne sort exactement 1 fois", color=WHITE).scale(0.4).to_edge(DOWN)
        note_inside2 = Text("Toutes les intersections sont Vertes (+)", color=GREEN).scale(0.4).next_to(note_inside1, UP)
        
        self.add_fixed_in_frame_mobjects(note_inside1, note_inside2)
        
        # On ajoute le glow seulement maintenant : si on le fait avant le Transform,
        # les updaters entrent en conflit et la forme cligne bizarrement.
        surface.add_updater(lambda m: m.set_stroke(width=8 if is_charge_inside() else 4, color=BLUE_A if is_charge_inside() else BLUE_B))
        
        self.play(q_pos_ref.animate.move_to(RIGHT*1.5 + UP*0.5), run_time=2)
        self.play(q_pos_ref.animate.move_to(LEFT*1.2 + DOWN*0.8), run_time=2)
        self.play(q_pos_ref.animate.move_to(ORIGIN), run_time=1)
        self.wait(1)

        # --- Séquence 3 : la charge sort de la surface, le flux net tombe à zéro ---
        note_outside1 = Text("À l'extérieur : Chaque ligne qui entre, ressort", color=WHITE).scale(0.4).to_edge(DOWN)
        note_outside2 = Text("Entrée (Rouge) + Sortie (Vert) = Flux Nul", color=YELLOW).scale(0.4).next_to(note_outside1, UP)
        
        self.play(
            FadeOut(note_inside1), FadeOut(note_inside2),
            FadeIn(note_outside1), FadeIn(note_outside2),
            q_pos_ref.animate.move_to(RIGHT * 4), 
            run_time=3
        )
        self.wait(1)
        
        self.play(Indicate(intersection_dots, scale_factor=1.5))
        self.wait(2)

        self.play(
            FadeOut(note_outside1), FadeOut(note_outside2),
            q_pos_ref.animate.move_to(ORIGIN), 
            run_time=2
        )
        self.wait(2)