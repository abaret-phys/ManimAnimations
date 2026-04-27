"""
Laplace Force Animation - ManimCE
==================================
Two scenes:
  1) LaplaceForceMicroscopic: 2D zoomed view of a conductor showing electrons
     drifting under v x B force, transferring momentum to the lattice.
  2) LaplaceForceSetup3D: 3D rendered classic "rails-and-rod" experiment.

Run with:
    manim -pqh laplace_force.py LaplaceForceMicroscopic
    manim -pqh laplace_force.py LaplaceForceSetup3D

Physics convention used in scene 1:
    - Conventional current I points to the LEFT
    - Electrons (negative charges) drift to the RIGHT  (v = +x)
    - Magnetic field B points OUT of the page          (B = +z)
    - Force on each electron: F = q v x B  is UPWARD
    - Net Laplace force on the wire: F = I L x B is also UPWARD
"""

from manim import *
import numpy as np


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def make_dot_in_circle(point, radius=0.10, color=BLUE_C):
    """Marqueur (.) signifiant 'vecteur sortant de la page'."""
    outer = Circle(radius=radius, color=color, stroke_width=2,
                   fill_color=color, fill_opacity=0.15)
    inner = Dot(radius=radius * 0.35, color=color)
    g = VGroup(outer, inner)
    g.move_to(point)
    return g


def make_electron(point, radius=0.16):
    """Cercle bleu avec un signe moins — plus grand que les ions pour rester lisible."""
    body = Circle(radius=radius, color=BLUE_B,
                  fill_color=BLUE_D, fill_opacity=1.0, stroke_width=2)
    minus = Line(LEFT * 0.075, RIGHT * 0.075, color=WHITE, stroke_width=3)
    g = VGroup(body, minus)
    g.move_to(point)
    return g


def make_ion(point, radius=0.12):
    """Cercle rouge plus petit avec un signe plus — ion du réseau cristallin."""
    body = Circle(radius=radius, color=RED_E,
                  fill_color=RED_E, fill_opacity=0.95, stroke_width=1.5)
    h = Line(LEFT * 0.06, RIGHT * 0.06, color=WHITE, stroke_width=2)
    v = Line(DOWN * 0.06, UP * 0.06, color=WHITE, stroke_width=2)
    g = VGroup(body, h, v)
    g.move_to(point)
    return g


def safe_shade_in_3d(mobj, value=True):
    """set_shade_in_3d n'existe pas sur le renderer OpenGL (Prism/Cube) — on ignore silencieusement."""
    fn = getattr(mobj, "set_shade_in_3d", None)
    if callable(fn):
        try:
            fn(value)
        except Exception:
            pass


# ============================================================================
# SCENE 1 - Microscopic / zoomed view of the conductor
# ============================================================================
class LaplaceForceMicroscopic(Scene):
    def construct(self):
        # ---------- Title ----------
        title = Text("Force de Laplace — Vue microscopique", font_size=34)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(0.3)

        # ---------- The conductor (a horizontal "wire slice") ----------
        wire_left, wire_right = -6.2, 6.2
        wire_top, wire_bot = 1.2, -1.2
        conductor = Rectangle(
            width=wire_right - wire_left,
            height=wire_top - wire_bot,
            color=GREY_B,
            fill_color=GREY_E,
            fill_opacity=0.35,
            stroke_width=2,
        )
        conductor.move_to(ORIGIN)

        wire_label = Text("Conducteur (zoom)", font_size=20, color=GREY_A)
        wire_label.next_to(conductor, DOWN, buff=0.15).shift(LEFT * 4.2)

        scale_note = Text("(non à l'échelle)", font_size=16, color=GREY_B,
                          slant=ITALIC)
        scale_note.next_to(wire_label, DOWN, buff=0.05)

        self.play(Create(conductor))
        self.wait(0.2)

        # Zone de champ B (sortant de la page) — les électrons vont y ressentir la force
        b_region_left = -1.0
        b_region_right = wire_right - 0.1

        b_overlay = Rectangle(
            width=b_region_right - b_region_left,
            height=wire_top - wire_bot,
            stroke_width=0,
            fill_color=BLUE_E,
            fill_opacity=0.10,
        ).move_to([(b_region_left + b_region_right) / 2, 0, 0])

        b_field_marks = VGroup()
        cols = np.arange(b_region_left + 0.5, b_region_right - 0.1, 0.75)
        rows = np.arange(wire_bot + 0.4, wire_top - 0.1, 0.6)
        for x in cols:
            for y in rows:
                b_field_marks.add(make_dot_in_circle([x, y, 0],
                                                    radius=0.08, color=BLUE_C))

        b_label = MathTex(r"\vec{B}", color=BLUE_C, font_size=42)
        b_label.next_to(conductor, UP, buff=0.15).shift(RIGHT * 3.0)
        b_sub = Text("(sortant de la page)", font_size=18, color=BLUE_C)
        b_sub.next_to(b_label, RIGHT, buff=0.15)

        self.play(FadeIn(b_overlay), LaggedStart(
            *[FadeIn(m, scale=0.5) for m in b_field_marks],
            lag_ratio=0.01, run_time=1.0))
        self.play(Write(b_label), FadeIn(b_sub))
        self.wait(0.3)

        # Courant conventionnel I vers la gauche (electrons driftent vers la droite)
        I_arrow = Arrow(
            start=[2.2, wire_top + 0.85, 0],
            end=[-2.2, wire_top + 0.85, 0],
            color=YELLOW, buff=0, stroke_width=6,
            max_tip_length_to_length_ratio=0.07,
        )
        I_label = MathTex(r"I", color=YELLOW, font_size=42)
        I_label.next_to(I_arrow, UP, buff=0.05)
        self.play(GrowArrow(I_arrow), Write(I_label))
        self.wait(0.2)

        # Ions du réseau (fixes) — c'est eux qui transmettront la force aux élèves
        lattice = VGroup()
        lat_xs = np.linspace(wire_left + 0.6, wire_right - 0.6, 14)
        lat_ys = np.linspace(wire_bot + 0.5, wire_top - 0.5, 3)
        for x in lat_xs:
            for y in lat_ys:
                lattice.add(make_ion([x, y, 0]))
        lattice.set_z_index(1)

        lattice_label = Text("Ions du réseau (+)", font_size=18, color=RED_B)
        lattice_label.next_to(conductor, DOWN, buff=0.15).shift(RIGHT * 3.5)

        self.play(FadeIn(lattice, shift=0.08 * UP), FadeIn(lattice_label),
                  FadeIn(wire_label), FadeIn(scale_note))
        self.wait(0.2)

        # ---------- Electrons ----------
        n_electrons = 6
        electron_y_levels = [-0.55, 0.55]
        electrons = VGroup()
        e_start_xs = np.linspace(wire_left + 0.5, b_region_left - 0.4, n_electrons)
        for i, x in enumerate(e_start_xs):
            y = electron_y_levels[i % 2]
            electrons.add(make_electron([x, y, 0]))
        for e in electrons:
            e.set_z_index(2)

        e_label = Text("Électrons (–)", font_size=18, color=BLUE_B)
        e_label.next_to(lattice_label, DOWN, buff=0.1)

        self.play(FadeIn(electrons), FadeIn(e_label))
        self.wait(0.2)

        # ---------- Electron velocity arrow ----------
        v_arrow = Arrow(
            start=[wire_left + 0.4, wire_bot - 0.7, 0],
            end=[wire_left + 2.0, wire_bot - 0.7, 0],
            color=BLUE_B, buff=0, stroke_width=5,
            max_tip_length_to_length_ratio=0.18,
        )
        v_label = MathTex(r"\vec{v}", color=BLUE_B, font_size=40)
        v_label.next_to(v_arrow, DOWN, buff=0.1)
        self.play(GrowArrow(v_arrow), Write(v_label))
        self.wait(0.3)

        # Dérive initiale : on ajuste la distance pour que les 3 électrons les plus à droite
        # se retrouvent dans (ou au bord de) la zone de champ après ce déplacement.
        drift_dx = 2.2
        self.play(
            *[e.animate.shift(RIGHT * drift_dx) for e in electrons],
            run_time=1.5, rate_func=linear,
        )
        self.wait(0.2)

        # ---------- Step B: magnetic-force formula ----------
        formula = MathTex(
            r"\vec{F}_{\text{mag}} = q\,\vec{v}\times\vec{B}",
            font_size=36, color=GREEN,
        )
        formula.to_edge(DOWN, buff=0.4).shift(LEFT * 3.4)

        sign_note = MathTex(
            r"q=-e<0 \;\Rightarrow\; \vec{F}\ \text{vers le haut}",
            font_size=32, color=GREEN,
        )
        sign_note.next_to(formula, RIGHT, buff=0.5)

        self.play(Write(formula))
        self.play(FadeIn(sign_note, shift=0.2 * UP))
        self.wait(0.4)

        # Force vers le haut sur les 3 électrons dans le champ — on les trie par x
        # pour être sûr de prendre les bons même si l'ordre a changé pendant la dérive.
        sorted_e = sorted(electrons, key=lambda e: e.get_center()[0])
        in_field_electrons = sorted_e[-3:]
        out_field_electrons = sorted_e[:-3]

        force_arrows = VGroup()
        for e in in_field_electrons:
            c = e.get_center()
            f = Arrow(
                start=c + 0.05 * UP,
                end=c + 0.55 * UP,
                color=GREEN, buff=0, stroke_width=5,
                max_tip_length_to_length_ratio=0.32,
            )
            force_arrows.add(f)

        if len(force_arrows) > 0:
            f_tag = MathTex(r"\vec{F}", color=GREEN, font_size=32)
            f_tag.next_to(force_arrows[-1], UP, buff=0.05)
        else:
            f_tag = VGroup()

        self.play(LaggedStart(*[GrowArrow(a) for a in force_arrows],
                              lag_ratio=0.12, run_time=1.2))
        if len(force_arrows) > 0:
            self.play(Write(f_tag))
        self.wait(0.4)

        # Les flèches de force suivent leurs électrons via updaters — on les attache avant l'animation
        def make_force_updater(electron_ref):
            def upd(m):
                c = electron_ref.get_center()
                m.put_start_and_end_on(c + 0.05 * UP, c + 0.55 * UP)
            return upd

        for e, f in zip(in_field_electrons, force_arrows):
            f.add_updater(make_force_updater(e))

        if len(force_arrows) > 0:
            def label_upd(m):
                m.next_to(force_arrows[-1], UP, buff=0.05)
            f_tag.add_updater(label_upd)

        anims = []
        for e in in_field_electrons:
            start = e.get_center()
            dx = 1.2
            ceiling = wire_top - 0.25  # plafond : l'électron ne sort pas du conducteur
            dy = min(0.55, max(0.0, ceiling - start[1]))
            mid = start + RIGHT * (dx * 0.5) + UP * (dy * 0.2)
            end = start + RIGHT * dx + UP * dy
            path = VMobject()
            path.set_points_smoothly([start, mid, end])
            anims.append(MoveAlongPath(e, path, rate_func=smooth))

        for e in out_field_electrons:
            anims.append(e.animate.shift(RIGHT * 1.4))

        self.play(*anims, run_time=2.2)
        self.wait(0.3)

        for f in force_arrows:
            f.clear_updaters()
        if len(force_arrows) > 0:
            f_tag.clear_updaters()

        # Collisions : les électrons poussent les ions du réseau — c'est le mécanisme microscopique
        # de la force de Laplace. Un petit tremblement du réseau pour le rendre visible.
        collide_text = Text("Les électrons poussent le réseau vers le haut par collisions",
                            font_size=24, color=YELLOW)
        collide_text.to_edge(DOWN, buff=0.05)

        self.play(FadeOut(formula), FadeOut(sign_note))
        self.play(FadeIn(collide_text, shift=0.2 * UP))
        self.wait(0.2)

        # Petit pulse de secousse
        self.play(lattice.animate.shift(UP * 0.05), run_time=0.12)
        self.play(lattice.animate.shift(DOWN * 0.05), run_time=0.12)
        self.play(lattice.animate.shift(UP * 0.04), run_time=0.10)
        self.play(lattice.animate.shift(DOWN * 0.04), run_time=0.10)
        self.wait(0.2)

        # Force de Laplace nette vers le haut, ancrée au bord supérieur du conducteur
        net_force_arrow = Arrow(
            start=[-3.5, wire_top + 0.15, 0],
            end=[-3.5, wire_top + 1.6, 0],
            color=GREEN, buff=0, stroke_width=10,
            max_tip_length_to_length_ratio=0.25,
        )
        net_force_label = MathTex(
            r"\vec{F}_{\text{Laplace}} = I\,\vec{\ell}\times\vec{B}",
            color=GREEN, font_size=32,
        )
        net_force_label.next_to(net_force_arrow, RIGHT, buff=0.25)
        # Léger décalage vers le haut pour ne pas se superposer à la flèche de courant I
        net_force_label.shift(UP * 0.4)

        self.play(FadeOut(force_arrows), FadeOut(f_tag))
        self.play(GrowArrow(net_force_arrow), Write(net_force_label))
        self.wait(0.4)

        # On pousse tout le système vers le haut pour illustrer la force macroscopique
        wire_system = VGroup(
            conductor, b_overlay, b_field_marks, lattice, electrons,
            I_arrow, I_label, b_label, b_sub,
            net_force_arrow, net_force_label,
            wire_label, scale_note, lattice_label, e_label,
        )
        self.play(wire_system.animate.shift(UP * 0.3),
                  run_time=1.6, rate_func=smooth)
        self.wait(0.5)

        summary = Text(
            "Cette force nette vers le haut sur le conducteur est la force de Laplace",
            font_size=24, color=GREEN,
        )
        summary.to_edge(DOWN, buff=0.05)
        self.play(FadeOut(collide_text), FadeIn(summary, shift=0.2 * UP))
        self.wait(2.5)


# ============================================================================
# SCENE 2 - 3D experimental setup
# ============================================================================
class LaplaceForceSetup3D(ThreeDScene):
    def construct(self):
        # Vue en perspective à 45° face à l'ouverture du C — le C ouvre vers -X,
        # on se place du côté -X/-Y pour voir l'intérieur du gap.
        self.set_camera_orientation(phi=80 * DEGREES, theta=-135 * DEGREES)

        # ---------- Color palette ----------
        BASE_BLACK = "#3A3A42"  # dark slate grey (no longer pure black)
        ACRYLIC = "#BFE7FF"
        SILVER = "#C8C8D0"
        ROD_METAL = "#D8D8E0"
        WHEEL_BLACK = "#0A0A0A"
        MAGNET_RED = "#C81E1E"
        MAGNET_SILVER = "#B8B8C0"
        WIRE_RED = "#E03030"
        WIRE_BLACK = "#202020"

        # Support acrylique à gauche uniquement — à droite, c'est le C-aimant qui supporte les rails
        acrylic_dims = [0.6, 3.4, 0.7]
        acrylic_left = Prism(dimensions=acrylic_dims)
        acrylic_left.set_fill(ACRYLIC, opacity=0.35)
        acrylic_left.set_stroke(WHITE, width=1, opacity=0.6)
        safe_shade_in_3d(acrylic_left)
        acrylic_left.move_to([-3.5, 0, 0.35])

        self.add(acrylic_left)
        self.wait(0.50)

        # Deux rails parallèles argentés — de l'acrylique gauche jusqu'à l'intérieur du C
        rail_y = 1.1
        rail_dims = [7.0, 0.12, 0.12]
        rail_z = 0.7 + 0.06

        rail_front = Prism(dimensions=rail_dims)
        rail_front.set_fill(SILVER, opacity=1.0)
        rail_front.set_stroke(GREY_A, width=1)
        safe_shade_in_3d(rail_front)

        rail_back = rail_front.copy()
        # Centered so rails go from x=-3.5 (left support) to x=+3.5 (inside magnet)
        rail_front.move_to([0, +rail_y, rail_z])
        rail_back.move_to([0, -rail_y, rail_z])

        self.add(rail_front, rail_back)
        self.wait(0.50)

        # Tige métallique posée sur les rails — c'est elle qui va être poussée
        rod_length = 2 * rail_y + 0.3
        rod = Cylinder(
            radius=0.07, height=rod_length,
            direction=np.array([0.0, 1.0, 0.0]),
            resolution=(12, 24),
            fill_color=ROD_METAL, fill_opacity=1.0,
            stroke_color=GREY_A, stroke_width=1,
        )
        # Start the rod inside the magnet gap, near its right opening.
        rod.move_to([2.8, 0, rail_z + 0.13])

        rod_assembly = VGroup(rod)
        self.add(rod_assembly)
        self.wait(0.50)

        # Aimant en C à droite — les bras couvrent toute la longueur des rails
        # pour que la tige reste dans le champ quelle que soit sa position.
        gap_z_center = rail_z + 0.13
        gap_height = 1.6
        arm_thickness = 0.45
        arm_depth = 6.6                 # arms span the whole rail length
        arm_width = 3.0
        spine_x = 3.4                   # spine sits at the right end
        back_thickness_x = 0.36
        # Center of the arms in X: arms extend from x = spine - arm_depth to x = spine
        arm_center_x = spine_x - arm_depth / 2

        # Top arm (RED)
        top_arm = Prism(dimensions=[arm_depth, arm_width, arm_thickness])
        top_arm.set_fill(MAGNET_RED, opacity=1.0)
        top_arm.set_stroke(BLACK, width=1.5)
        safe_shade_in_3d(top_arm)
        top_arm.move_to([arm_center_x, 0,
                         gap_z_center + gap_height / 2 + arm_thickness / 2])

        # Bottom arm (SILVER)
        bot_arm = Prism(dimensions=[arm_depth, arm_width, arm_thickness])
        bot_arm.set_fill(MAGNET_SILVER, opacity=1.0)
        bot_arm.set_stroke(BLACK, width=1.5)
        safe_shade_in_3d(bot_arm)
        bot_arm.move_to([arm_center_x, 0,
                         gap_z_center - gap_height / 2 - arm_thickness / 2])

        # Dos du C, en deux demi-blocs pour garder la même convention de couleur N/S
        back_x = spine_x + back_thickness_x / 2
        full_back_height = gap_height + 2 * arm_thickness

        back_top = Prism(
            dimensions=[back_thickness_x, arm_width, full_back_height / 2])
        back_top.set_fill(MAGNET_RED, opacity=1.0)
        back_top.set_stroke(BLACK, width=1.5)
        safe_shade_in_3d(back_top)
        back_top.move_to([back_x, 0, gap_z_center + full_back_height / 4])

        back_bot = Prism(
            dimensions=[back_thickness_x, arm_width, full_back_height / 2])
        back_bot.set_fill(MAGNET_SILVER, opacity=1.0)
        back_bot.set_stroke(BLACK, width=1.5)
        safe_shade_in_3d(back_bot)
        back_bot.move_to([back_x, 0, gap_z_center - full_back_height / 4])

        magnet = VGroup(top_arm, bot_arm, back_top, back_bot)
        self.add(magnet)
        self.wait(0.50)

        # Labels N/S sur la face intérieure visible depuis la caméra — sur les bras, pas le dos
        label_x = arm_center_x         # roughly center of the arms
        N_label = Text("N", font_size=36, color=WHITE, weight=BOLD)
        S_label = Text("S", font_size=36, color="#7A0000", weight=BOLD)
        N_label.move_to([label_x, -arm_width / 2 - 0.05,
                         gap_z_center + gap_height / 2 + arm_thickness / 2])
        S_label.move_to([label_x, -arm_width / 2 - 0.05,
                         gap_z_center - gap_height / 2 - arm_thickness / 2])
        self.add_fixed_orientation_mobjects(N_label, S_label)
        self.play(FadeIn(N_label), FadeIn(S_label), run_time=0.5)
        self.wait(0.50)

        # Fils électriques : rouge = +, noir = −.
        # Chemin du courant : rouge → rail arrière (y=−) → tige (+y) → rail avant (y=+) → noir.
        # Ce sens donne I·L = +y dans la tige. Avec B = −z (N en haut → S en bas) :
        # F = I L × B = (+y) × (−z) = −x → tige poussée vers la GAUCHE, cohérent avec l'animation.
        rail_end_x = -3.5

        def make_wire(y_offset, color):
            sign = 1.0 if y_offset > 0 else -1.0
            start = np.array([rail_end_x - 0.05, y_offset, rail_z])
            mid = np.array([rail_end_x - 1.0, y_offset + 0.6 * sign, rail_z - 0.4])
            end = np.array([rail_end_x - 1.8, y_offset + 1.0 * sign, -0.6])

            def f(t):
                return ((1 - t) ** 2) * start + 2 * (1 - t) * t * mid + (t ** 2) * end

            return ParametricFunction(f, t_range=[0, 1, 0.02],
                                      color=color, stroke_width=8)

        wire_red = make_wire(-rail_y, WIRE_RED)   # red on the back rail (-y)
        wire_blk = make_wire(+rail_y, WIRE_BLACK) # black on the front rail (+y)

        plug_red = Sphere(radius=0.10, resolution=(10, 16))
        plug_red.set_color(WIRE_RED)
        plug_red.move_to([rail_end_x - 0.05, -rail_y, rail_z])
        plug_blk = Sphere(radius=0.10, resolution=(10, 16))
        plug_blk.set_color(WIRE_BLACK)
        plug_blk.move_to([rail_end_x - 0.05, +rail_y, rail_z])

        self.play(Create(wire_red), Create(wire_blk),
                  FadeIn(plug_red), FadeIn(plug_blk), run_time=0.8)
        self.wait(0.75)

        # Vecteurs physiques B, I, F — Arrow3D pour qu'ils s'intègrent naturellement en 3D
        rod_x0 = 2.8
        # B du pôle N (bras rouge, en haut) vers S (bras argenté, en bas) → direction −z
        B_arrow = Arrow3D(
            start=np.array([rod_x0, 0,
                            gap_z_center + gap_height / 2 - 0.05]),
            end=np.array([rod_x0, 0,
                          gap_z_center - gap_height / 2 + 0.05]),
            color=BLUE_C, thickness=0.03, height=0.18, base_radius=0.09,
        )
        B_label = MathTex(r"\vec{B}", color=BLUE_C, font_size=36)
        B_label.next_to(B_arrow, RIGHT, buff=0.1)
        self.add_fixed_orientation_mobjects(B_label)

        # I dans la tige : du rail arrière (−y) vers le rail avant (+y) → direction +y
        I_arrow = Arrow3D(
            start=np.array([rod_x0, -rail_y + 0.05, rail_z + 0.13]),
            end=np.array([rod_x0,  rail_y - 0.05, rail_z + 0.13]),
            color=YELLOW, thickness=0.025, height=0.16, base_radius=0.07,
        )
        I_label = MathTex(r"I", color=YELLOW, font_size=36)
        I_label.next_to(I_arrow, UP, buff=0.05)
        self.add_fixed_orientation_mobjects(I_label)

        # F = IL×B : L = +y, B = −z → F = +y × (−z) = −x → pointe vers la GAUCHE
        F_arrow = Arrow3D(
            start=np.array([rod_x0, 0, rail_z + 0.13]),
            end=np.array([rod_x0 - 1.4, 0, rail_z + 0.13]),
            color=GREEN, thickness=0.04, height=0.22, base_radius=0.11,
        )
        F_label = MathTex(r"\vec{F}", color=GREEN, font_size=36)
        F_label.next_to(F_arrow, UP, buff=0.1)
        self.add_fixed_orientation_mobjects(F_label)

        self.play(Create(B_arrow), FadeIn(B_label), run_time=0.7)
        self.wait(0.50)
        self.play(Create(I_arrow), FadeIn(I_label), run_time=0.7)
        self.wait(0.50)
        self.play(Create(F_arrow), FadeIn(F_label), run_time=0.7)
        self.wait(0.75)

        # Sens du courant dans les rails — cohérent avec I dans la tige (+y) :
        # rail arrière (y=−) : de x=−3.5 vers la tige (+x) ; rail avant (y=+) : l'inverse.
        rail_I_z = rail_z + 0.20  # slightly above the rail to stay visible
        I_back_arrow = Arrow3D(
            start=np.array([-1.5, -rail_y, rail_I_z]),
            end=np.array([0.5, -rail_y, rail_I_z]),
            color=YELLOW, thickness=0.02, height=0.14, base_radius=0.06,
        )
        I_front_arrow = Arrow3D(
            start=np.array([0.5, +rail_y, rail_I_z]),
            end=np.array([-1.5, +rail_y, rail_I_z]),
            color=YELLOW, thickness=0.02, height=0.14, base_radius=0.06,
        )
        I_back_label = MathTex(r"I", color=YELLOW, font_size=28)
        I_back_label.next_to(I_back_arrow, DOWN, buff=0.05)
        I_front_label = MathTex(r"I", color=YELLOW, font_size=28)
        I_front_label.next_to(I_front_arrow, UP, buff=0.05)
        self.add_fixed_orientation_mobjects(I_back_label, I_front_label)

        self.play(Create(I_back_arrow), Create(I_front_arrow),
                  FadeIn(I_back_label), FadeIn(I_front_label), run_time=0.7)
        self.wait(0.75)

        # ---------- Title and caption (fixed in frame, 2D overlay) ----------
        title3d = Text("Force de Laplace — Montage expérimental", font_size=32)
        title3d.to_edge(UP, buff=0.3)
        self.add_fixed_in_frame_mobjects(title3d)
        self.play(FadeIn(title3d), run_time=0.6)

        caption = MathTex(
            r"\vec{F} = I \vec{L} \times \vec{B}\text{: la tige est poussée hors de l'aimant}",
            font_size=22, color=YELLOW,
        )
        caption.to_edge(DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(caption)
        self.play(FadeIn(caption), run_time=0.6)
        self.wait(0.75)

        # Rotation lente pour que l'étudiant perçoive bien la 3D — on reste sur la position finale
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(6.25)
        self.stop_ambient_camera_rotation()

        # La tige glisse vers la gauche — B, I, F et leurs labels suivent via shift
        moving_group = VGroup(
            rod_assembly,
            B_arrow, B_label,
            I_arrow, I_label,
            F_arrow, F_label,
        )
        self.play(moving_group.animate.shift(LEFT * 3.5),
                  run_time=4.40, rate_func=smooth)
        self.wait(2.50)

        self.wait(3.75)