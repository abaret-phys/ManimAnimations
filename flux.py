from manim import *
import numpy as np

class FluxIntuition(Scene):
    def construct(self):
        # ─────────────────────────────────────────────
        # PARTIE 1 — Densité de lignes et aire projetée (le sens du produit scalaire)
        # ─────────────────────────────────────────────
        title1 = Title("1. L'Aire Projetée (Le Produit Scalaire)", color=WHITE)
        self.play(Write(title1))

        # Champ électrique uniforme représenté par un peigne de lignes horizontales
        lines_group = VGroup()
        # linspace plutôt qu'arange : positions y exactes, sans dérive due aux erreurs d'arrondi
        y_vals = np.linspace(-2.4, 2.4, 13) 
        for y in y_vals:
            lines_group.add(Arrow(LEFT*6 + UP*y, RIGHT*1 + UP*y, color=BLUE_D, buff=0, stroke_width=3, tip_length=0.15))
        
        self.play(Create(lines_group, lag_ratio=0.1))

        # La surface, vue ici par la tranche : on la fait tourner autour du point xc
        xc = -2.0
        L = 4.0  # longueur de la surface
        
        theta_tracker = ValueTracker(0)

        # Pour éviter tout glissement parasite, on calcule les extrémités directement
        # à partir de θ — pas de Rotate() empilé sur Rotate(), pas de drift numérique.
        def get_top_pt():
            theta = theta_tracker.get_value()
            return np.array([xc - (L/2)*np.sin(theta), (L/2)*np.cos(theta), 0])
            
        def get_bot_pt():
            theta = theta_tracker.get_value()
            return np.array([xc + (L/2)*np.sin(theta), -(L/2)*np.cos(theta), 0])

        surface = always_redraw(lambda: Line(get_bot_pt(), get_top_pt(), color=WHITE, stroke_width=6))
        
        # Vecteur normal n à la surface
        def get_n_vec():
            theta = theta_tracker.get_value()
            # À θ=0, n est horizontal et aligné avec le champ : flux maximal
            return np.array([np.cos(theta), np.sin(theta), 0])

        normal_vec = always_redraw(lambda: Arrow(
            [xc, 0, 0], [xc, 0, 0] + get_n_vec() * 1.5, 
            color=YELLOW, buff=0
        ))
        # On note "n" plutôt que "dA" : ici on regarde la direction, pas l'élément différentiel
        n_label = always_redraw(lambda: MathTex(r"\vec{n}", color=YELLOW).next_to(normal_vec.get_end(), RIGHT, buff=0.1))

        self.play(Create(surface), Create(normal_vec), Write(n_label))

        # --- L'ombre projetée à droite, calée pile sur les extrémités de la surface ---
        proj_x = 2.0
        proj_line = always_redraw(lambda: Line(
            [proj_x, get_bot_pt()[1], 0], 
            [proj_x, get_top_pt()[1], 0], 
            color=GREEN, stroke_width=8
        ))
        
        # Pointillés qui relient chaque extrémité à son ombre — toujours alignés grâce au calcul direct
        dash_top = always_redraw(lambda: DashedLine(get_top_pt(), [proj_x, get_top_pt()[1], 0], color=GRAY, stroke_width=2))
        dash_bot = always_redraw(lambda: DashedLine(get_bot_pt(), [proj_x, get_bot_pt()[1], 0], color=GRAY, stroke_width=2))
        
        proj_label = always_redraw(lambda: MathTex(r"A_{\perp} = A \cos \theta", color=GREEN).next_to(proj_line, RIGHT))

        self.play(Create(proj_line), Create(dash_top), Create(dash_bot), Write(proj_label))

        # --- Points d'intersection champ ↔ surface, calculés analytiquement ---
        def get_intersections():
            dots = VGroup()
            theta = theta_tracker.get_value()
            # Bornes en y exactes (au lieu d'un test approximatif)
            max_y = (L/2) * np.cos(theta)
            min_y = -(L/2) * np.cos(theta)
            
            for y in y_vals:
                if min_y - 1e-4 <= y <= max_y + 1e-4: # petite tolérance pour les flottants
                    # Formule directe : x = xc - y * tan(theta), pas d'intersection numérique à faire
                    x_intersect = xc - y * np.tan(theta)
                    dots.add(Dot([x_intersect, y, 0], color=GREEN).scale(1.2))
            return dots

        intersections = always_redraw(get_intersections)
        self.play(FadeIn(intersections))

        # --- L'équation qui relie le nombre de lignes capturées au flux ---
        math_box = VGroup(
            MathTex(r"\text{Nombre de lignes capturées } \propto E \times A_{\perp}", color=GREEN),
            MathTex(r"\Rightarrow \Phi_E = \vec{E} \cdot \vec{n} A = E A \cos \theta", color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.7).to_corner(DL)
        
        # Petit fond noir pour garder le texte lisible par-dessus le peigne de lignes bleues
        math_bg = BackgroundRectangle(math_box, color=BLACK, fill_opacity=0.8, buff=0.2)
        self.play(FadeIn(math_bg), Write(math_box))

        # --- Animation : on fait varier l'angle pour voir l'ombre rétrécir ---
        self.wait(1)
        self.play(theta_tracker.animate.set_value(PI/3), run_time=3)
        self.wait(1)
        self.play(theta_tracker.animate.set_value(PI/2.1), run_time=2) # presque parallèle au champ : ombre quasi nulle
        self.wait(1)
        self.play(theta_tracker.animate.set_value(0), run_time=2)
        self.wait(2)

        # Grand nettoyage avant la seconde partie
        self.play(*[FadeOut(m) for m in self.mobjects])

        # ─────────────────────────────────────────────
        # PARTIE 2 — Pourquoi le flux reste constant : la loi en 1/r²
        # ─────────────────────────────────────────────
        title2 = Title("2. L'Invariance par la Distance (Loi en $1/r^2$)", color=WHITE)
        self.play(Write(title2))

        charge = Dot(LEFT*5, color=RED).scale(2)
        q_label = MathTex("+Q", color=RED).next_to(charge, UP)
        self.play(FadeIn(charge), Write(q_label))

        cone_angle = PI/6
        cone_lines = VGroup(
            Line(charge.get_center(), charge.get_center() + rotate_vector(RIGHT*12, cone_angle), color=GRAY_C, stroke_width=1),
            Line(charge.get_center(), charge.get_center() + rotate_vector(RIGHT*12, -cone_angle), color=GRAY_C, stroke_width=1)
        )
        self.play(Create(cone_lines))

        rays = VGroup(*[
            Arrow(charge.get_center(), charge.get_center() + rotate_vector(RIGHT*10, a), color=RED, buff=0.2, stroke_width=2, tip_length=0.15)
            for a in np.linspace(-cone_angle*0.8, cone_angle*0.8, 5)
        ])
        self.play(Create(rays, lag_ratio=0.1))

        # Deux portions de sphère à r et 2r : la seconde a 4× plus de surface
        r1 = 3
        arc1 = Arc(radius=r1, angle=2*cone_angle, start_angle=-cone_angle, arc_center=charge.get_center(), color=BLUE, stroke_width=6)
        label1 = MathTex(r"A \propto r^2", color=BLUE).next_to(arc1, UP)
        
        r2 = 6
        arc2 = Arc(radius=r2, angle=2*cone_angle, start_angle=-cone_angle, arc_center=charge.get_center(), color=GREEN, stroke_width=6)
        label2 = MathTex(r"4A \propto (2r)^2", color=GREEN).next_to(arc2, UP)

        self.play(Create(arc1), Write(label1))
        self.wait(1)
        self.play(Create(arc2), Write(label2))
        self.wait(1)

        # --- Le calcul qui montre que les deux effets (1/r² et r²) se compensent ---
        explanations = VGroup(
            MathTex(r"\text{À distance } 2r :", color=WHITE),
            MathTex(r"\text{Densité du champ } (E) \propto \frac{1}{r^2} \rightarrow \text{Divisée par } 4", color=RED_B),
            MathTex(r"\text{Surface } (A) \propto r^2 \rightarrow \text{Multipliée par } 4", color=GREEN_B),
            MathTex(r"\Phi_E = E \times A \Rightarrow \left(\frac{E}{4}\right) \times (4A) = \text{Constant}", color=YELLOW),
            MathTex(r"\Rightarrow \text{Les } 5 \text{ lignes traversent les deux surfaces !}", color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(DR).scale(0.65)

        expl_bg = BackgroundRectangle(explanations, color=BLACK, fill_opacity=0.8, buff=0.2)
        
        for i, text in enumerate(explanations):
            if i == 0: self.play(FadeIn(expl_bg))
            self.play(Write(text))
            self.wait(1)

        # Points jaunes : la preuve visuelle finale — ce sont exactement les mêmes 5 lignes qui traversent les deux arcs
        intersection_dots2 = VGroup()
        for ray in rays:
            direction = ray.get_end() - ray.get_start()
            direction /= np.linalg.norm(direction)
            intersection_dots2.add(Dot(charge.get_center() + direction * r1, color=YELLOW))
            intersection_dots2.add(Dot(charge.get_center() + direction * r2, color=YELLOW))

        self.play(FadeIn(intersection_dots2))
        self.play(Indicate(intersection_dots2, color=GOLD, scale_factor=1.5))
        self.wait(3)