from manim import *
import numpy as np

class MagneticMaterials(ThreeDScene):
    def construct(self):
        # Vue 2D stricte (caméra à pic, par-dessus la scène)
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)

        # ─────────────────────────────────────────────
        # 1. Décor : fond, étiquettes des trois colonnes, séparateurs
        # ─────────────────────────────────────────────
        bg = Rectangle(width=20, height=12).set_fill(color=["#000000", "#1a1a24"], opacity=1).set_z_index(-100)
        
        t_tracker = ValueTracker(20) 
        bg_heat = Rectangle(width=20, height=12).set_fill(color=["#3a0000", "#1a0000"], opacity=1).set_z_index(-99)
        bg_heat.add_updater(lambda m: m.set_opacity(
            np.clip(interpolate(0.0, 0.6, (t_tracker.get_value() - 20) / 750), 0, 0.6)
        ))

        labels = VGroup(
            Text("Diamagnétisme", color=BLUE_B).scale(0.5),
            Text("Paramagnétisme", color=YELLOW).scale(0.5),
            Text("Ferromagnétisme", color=RED).scale(0.5)
        ).arrange(RIGHT, buff=2.2).shift(UP * 2.8)
        
        dividers = VGroup(
            Line(UP*2.4, DOWN*3).shift(LEFT*2.4),
            Line(UP*2.4, DOWN*3).shift(RIGHT*2.4)
        )
        
        self.add_fixed_in_frame_mobjects(bg, bg_heat, *labels)
        self.add(*dividers)

        # ─────────────────────────────────────────────
        # 2. Les deux trackers (champ B0 et température) et l'UI associée
        # ─────────────────────────────────────────────
        b0_tracker = ValueTracker(0) 
        self.b0_peaked = False 
        
        b0_arrow = Arrow(DOWN*1.5, UP*1.5, color=GREEN, stroke_width=8, buff=0)
        b0_arrow.add_updater(lambda m: m.put_start_and_end_on(
            [-6.6, -1.5, 0],
            [-6.6, -1.5 + 3 * max(b0_tracker.get_value(), 0.01), 0]
        ))
        
        b0_text = MathTex(r"\vec{B}_0", color=GREEN)
        b0_text.add_updater(lambda m: m.next_to(b0_arrow, UP))

        # Affichage de la température arrondi au palier de 10°C : ça évite de re-rendre
        # un Text à chaque frame (plus fluide) et ça donne un effet "compteur" plus lisible.
        t_display = ValueTracker(20)
        t_text = Text("Température : 20°C", color=ORANGE).scale(0.6).to_corner(UR)
        def update_t_text(m):
            rounded = int(round(t_display.get_value() / 10) * 10)
            new = Text(f"Température : {rounded}°C", color=ORANGE).scale(0.6).to_corner(UR)
            m.become(new)
        t_text.add_updater(update_t_text)
        
        self.add_fixed_in_frame_mobjects(b0_arrow, b0_text, t_text)

        # ── Sous-titres : remplacement instantané, sans self.play() ──
        # Galère vécue : les self.play(run_time=0.2) forçaient un flush complet
        # de tous les updaters et bloquaient l'animation pendant plusieurs frames.
        # En plus, .become() sur un objet "fixed in frame" ne propage pas le flag
        # aux nouveaux sous-objets — résultat, une partie du texte se mettait à
        # bouger avec la caméra pendant le zoom.
        # Solution propre : retirer l'ancien sous-titre, créer le nouveau, et
        # le ré-ajouter via add_fixed_in_frame_mobjects.
        self.current_caption = Tex(r"1. État initial ($\vec{B}_0 = 0$)", color=WHITE).scale(0.8).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(self.current_caption)

        def switch_caption(new_text_str, text_color=WHITE):
            new_cap = Tex(new_text_str, color=text_color).scale(0.8).to_edge(DOWN)
            # Une opération atomique : on retire l'ancien et on ajoute le nouveau
            # en fixed-in-frame, sans self.play() — donc pas de freeze.
            self.remove(self.current_caption)
            self.add_fixed_in_frame_mobjects(new_cap)
            self.current_caption = new_cap

        # ─────────────────────────────────────────────
        # 3. Colonnes diamagnétisme + paramagnétisme
        # ─────────────────────────────────────────────
        dia_atoms = VGroup()
        for x in np.linspace(-5.4, -3.2, 3):
            for y in np.linspace(-1.5, 1.5, 3):
                atom = Dot(point=[x, y, 0], radius=0.4, color=BLUE_E, fill_opacity=0.3)
                m_ind = always_redraw(lambda a=atom: Arrow(
                    a.get_center(), a.get_center() + DOWN * 0.6 * b0_tracker.get_value(),
                    color=BLUE_B, buff=0, stroke_width=3, tip_length=0.1
                ) if b0_tracker.get_value() > 0.05 else Vector([0,0,0]))
                dia_atoms.add(atom, m_ind)

        para_spins = VGroup()
        np.random.seed(42)
        for x in np.linspace(-2.0, 2.0, 7):
            for y in np.linspace(-1.8, 1.8, 7):
                init_angle = np.random.uniform(0, 2*PI)
                # On parle bien de "moment dipolaire magnétique" et pas de "spin" — termes plus rigoureux pour des L1
                moment = Arrow(ORIGIN, RIGHT*0.2, color=YELLOW, buff=0, tip_length=0.08, stroke_width=2)
                moment.move_to([x, y, 0])
                moment.add_updater(lambda s, ia=init_angle: s.set_angle(
                    interpolate(ia, PI/2, max(0, b0_tracker.get_value() * (1 - t_tracker.get_value()/200))) + 
                    np.sin(self.time * 15 + ia) * (0.1 + 0.9 * (t_tracker.get_value()/100)) * (1 - b0_tracker.get_value()*0.5)
                ))
                para_spins.add(moment)

        # ─────────────────────────────────────────────
        # 4. Colonne ferromagnétisme : domaines de Weiss
        # ─────────────────────────────────────────────
        fx = 4.8
        pts = {
            'A': [fx-1.5, 1.8], 'B': [fx-0.2, 2.0], 'C': [fx+1.5, 1.8],
            'D': [fx-1.6, 0.2], 'E': [fx-0.4, 0.4], 'F': [fx+0.8, 0.5], 'G': [fx+1.6, 0.1],
            'H': [fx-1.5,-1.2], 'I': [fx-0.1,-1.0], 'J': [fx+1.5,-1.2],
            'K': [fx-1.4,-1.9], 'L': [fx+0.2,-1.9], 'M': [fx+1.5,-1.8]
        }
        def to_3d(pt2d): return np.array([pt2d[0], pt2d[1], 0])
        
        palettes = ["#F4EEDD", "#EBE2CD", "#E6DDC3", "#DFD4B7"]
        domain_pts_list = [
            [to_3d(pts['A']), to_3d(pts['B']), to_3d(pts['E']), to_3d(pts['D'])],
            [to_3d(pts['B']), to_3d(pts['C']), to_3d(pts['F']), to_3d(pts['E'])],
            [to_3d(pts['C']), to_3d(pts['G']), to_3d(pts['F'])],
            [to_3d(pts['D']), to_3d(pts['E']), to_3d(pts['I']), to_3d(pts['H'])],
            [to_3d(pts['E']), to_3d(pts['F']), to_3d(pts['J']), to_3d(pts['I'])],
            [to_3d(pts['H']), to_3d(pts['I']), to_3d(pts['L']), to_3d(pts['K'])],
            [to_3d(pts['I']), to_3d(pts['J']), to_3d(pts['M']), to_3d(pts['L'])]
        ]
        
        domains = VGroup(*[
            Polygon(*d_pts, color=WHITE, stroke_width=1, fill_color=palettes[i%4], fill_opacity=0.8)
            for i, d_pts in enumerate(domain_pts_list)
        ])
        
        visual_centers = [
            [fx - 0.9, 1.0, 0], [fx + 0.35, 1.1, 0], [fx + 1.25, 0.75, 0],
            [fx - 0.9, -0.5, 0], [fx + 0.35, -0.4, 0], [fx - 0.7, -1.5, 0], [fx + 0.8, -1.4, 0]
        ]
        domain_angles = [np.random.uniform(0, 2*PI) for _ in domains]
        
        # Température de Curie du fer : ~770°C — c'est la valeur qu'on utilisera comme référence visuelle
        T_CURIE = 770

        def get_ferro_opacity(): return np.clip((T_CURIE * 0.9 - t_tracker.get_value()) / (T_CURIE * 0.1), 0, 1)
        def get_para_opacity(): return np.clip((t_tracker.get_value() - T_CURIE * 0.85) / (T_CURIE * 0.1), 0, 1)

        def create_arrow_updater(idx):
            return always_redraw(lambda: Arrow(
                np.array(visual_centers[idx]) - np.array([
                    np.cos(interpolate(domain_angles[idx], PI/2, max(b0_tracker.get_value(), 0.9 if self.b0_peaked else b0_tracker.get_value()))),
                    np.sin(interpolate(domain_angles[idx], PI/2, max(b0_tracker.get_value(), 0.9 if self.b0_peaked else b0_tracker.get_value()))),
                    0
                ]) * 0.2,
                np.array(visual_centers[idx]) + np.array([
                    np.cos(interpolate(domain_angles[idx], PI/2, max(b0_tracker.get_value(), 0.9 if self.b0_peaked else b0_tracker.get_value()))),
                    np.sin(interpolate(domain_angles[idx], PI/2, max(b0_tracker.get_value(), 0.9 if self.b0_peaked else b0_tracker.get_value()))),
                    0
                ]) * 0.2,
                color=RED, buff=0, stroke_width=4, tip_length=0.1
            ).set_opacity(get_ferro_opacity()))

        ferro_arrows = VGroup(*[create_arrow_updater(i) for i in range(len(domains))])
        domains.add_updater(lambda d: d.set_opacity(get_ferro_opacity() * 0.8))

        ferro_broken_spins = VGroup()
        for x in np.linspace(fx-1.4, fx+1.4, 6):
            for y in np.linspace(-1.8, 1.8, 6):
                ia = np.random.uniform(0, 2*PI)
                # Encore une fois : moments dipolaires magnétiques, pas de "spins" ici
                m_moment = always_redraw(lambda ia=ia, x=x, y=y: Arrow(
                    ORIGIN, RIGHT*0.2, color=RED, buff=0, tip_length=0.08, stroke_width=2
                ).move_to([x, y, 0]).set_angle(
                    interpolate(ia, PI/2, max(0, b0_tracker.get_value() * (1 - t_tracker.get_value()/200))) + 
                    np.sin(self.time * 20 + ia) * 0.8
                ).set_opacity(get_para_opacity()))
                ferro_broken_spins.add(m_moment)

        # ─────────────────────────────────────────────
        # 5. Petits moments visibles uniquement quand on zoome dans un domaine
        # ─────────────────────────────────────────────
        c4 = visual_centers[4]
        micro_spins = VGroup()
        for dx in np.linspace(-0.35, 0.35, 5):
            for dy in np.linspace(-0.35, 0.35, 5):
                if dx**2 + dy**2 < 0.15:
                    # Rouge foncé (#8B0000) : contraste bien avec les fonds beiges des
                    # domaines (#F4EEDD, #EBE2CD, #E6DDC3, #DFD4B7) — testé à l'œil.
                    m_spin = Arrow(ORIGIN, RIGHT*0.15, color="#8B0000", buff=0, stroke_width=3, tip_length=0.05)
                    m_spin.move_to(np.array(c4) + np.array([dx, dy, 0]))
                    m_spin.set_angle(domain_angles[4])
                    micro_spins.add(m_spin)

        micro_spins.set_opacity(0) 

        # ─────────────────────────────────────────────
        # 6. Le scénario complet, étape par étape
        # ─────────────────────────────────────────────
        self.add(ferro_broken_spins, dia_atoms, para_spins, domains, ferro_arrows, micro_spins)
        self.wait(1)

        # --- Zoom d'introduction : on entre dans un domaine pour voir ce qu'il y a dedans ---
        switch_caption(r"Zoom : Un domaine est un groupe d'atomes aux moments dipolaires magnétiques déjà alignés", YELLOW)
        
        self.play(
            ferro_arrows[4].animate.set_opacity(0), 
            micro_spins.animate.set_opacity(1),
            run_time=0.5
        )
        self.move_camera(frame_center=c4, zoom=3.33, run_time=2)
        self.wait(2)
        
        # Dézoom : on revient sur la vue d'ensemble
        switch_caption(r"1. État initial ($\vec{B}_0 = 0$)")
        self.move_camera(frame_center=ORIGIN, zoom=1, run_time=2)
        self.play(
            ferro_arrows[4].animate.set_opacity(1),
            micro_spins.animate.set_opacity(0),
            run_time=0.5
        )
        self.wait(1)

        # --- On allume le champ B0 et on regarde les trois colonnes réagir ---
        switch_caption(r"2. Application du Champ $\vec{B}_0$ (Alignement des moments dipolaires)", GREEN)
        self.play(b0_tracker.animate.set_value(1), run_time=3)
        self.b0_peaked = True 
        self.wait(1)

        # --- On coupe B0 : seul le ferro garde une mémoire (rémanence) ---
        switch_caption(r"3. Rémanence ($\vec{B}_0 = 0$) : Le Ferro mémorise fortement", RED)
        self.play(b0_tracker.animate.set_value(0), run_time=3)
        self.wait(1)

        # --- Chauffage progressif vers la température de Curie ---
        # Astuce : t_tracker pilote la physique de façon continue, t_display pilote
        # uniquement l'affichage (par paliers de 10°C). Les deux trackers évitent
        # de devoir reconstruire le Text à chaque frame.
        switch_caption(r"4. Effet de la Température (Agitation thermique)", ORANGE)
        self.play(
            t_tracker.animate.set_value(T_CURIE * 0.85),
            t_display.animate.set_value(T_CURIE * 0.85),
            run_time=3,
            rate_func=linear
        )
        
        # --- Point de Curie : on franchit T_c et les domaines disparaissent ---
        switch_caption(r"5. Température de Curie ($T_c = 770$°C) : Les parois des domaines s'estompent !", RED_B)
        self.play(
            t_tracker.animate.set_value(T_CURIE),
            t_display.animate.set_value(T_CURIE),
            run_time=4,
            rate_func=linear
        )
        self.wait(1)
        
        switch_caption(r"Le matériau Ferromagnétique est devenu Paramagnétique.", YELLOW)
        self.wait(3)