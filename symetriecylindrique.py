from manim import *
import numpy as np

class ElectricFieldSymmetry(ThreeDScene):
    def construct(self):
        # ==========================================
        # PART 1: The Setup (3D View)
        # ==========================================
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        cylinder = Cylinder(radius=1, height=14, color=RED, fill_opacity=0.3)
        z_axis = DashedLine(start=IN*7, end=OUT*7, color=WHITE)
        
        p_pos = np.array([3, 0, 0])
        point_p = Dot3D(point=p_pos, color=WHITE)
        
        title = Tex("Champ électrique d'un\\\\cylindre infini\\\\uniformément chargé", font_size=40)
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)
        self.remove(title)

        self.play(FadeIn(cylinder), Create(z_axis))
        self.play(FadeIn(point_p))
        self.play(Write(title))
        self.wait(1)

        # ==========================================
        # PART 2: Argument 1 - The Direction is Radial
        # ==========================================
        subtitle1 = Tex("1. Plans de symétrie", font_size=36, color=BLUE)
        subtitle1.next_to(title, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(subtitle1)
        self.remove(subtitle1)
        self.play(Write(subtitle1))

        # Plan vertical (XZ) — contient l'axe et le point P : E doit appartenir à ce plan
        vert_plane = Polygon(
            [-4, 0, -7], [4, 0, -7], [4, 0, 7], [-4, 0, 7],
            color=GREEN, fill_opacity=0.3, stroke_width=0
        )
        
        vert_text = Tex("Le cylindre est symétrique\\\\par rapport à ce plan.", font_size=30)
        vert_text.to_corner(DL)
        self.add_fixed_in_frame_mobjects(vert_text)
        self.remove(vert_text)
        
        self.play(FadeIn(vert_plane))
        self.play(Write(vert_text))
        self.wait(3)

        # Plan horizontal (XY) passant par P — second plan de symétrie, perpendiculaire au premier
        horiz_plane = Polygon(
            [-4, -4, 0], [4, -4, 0], [4, 4, 0], [-4, 4, 0],
            color=TEAL, fill_opacity=0.3, stroke_width=0
        )
        
        horiz_text = Tex("Le cylindre infini est aussi\\\\symétrique par rapport au\\\\plan horizontal passant par P.", font_size=30)
        horiz_text.to_corner(DL)
        self.add_fixed_in_frame_mobjects(horiz_text)
        self.remove(horiz_text)
        
        self.play(FadeOut(vert_text))
        self.play(FadeIn(horiz_plane))
        self.play(Write(horiz_text))
        self.wait(3)

        # L'intersection des deux plans de symétrie est la direction radiale — c'est là que E doit pointer
        intersect_line_dashed = DashedLine(start=ORIGIN, end=RIGHT*5, color=WHITE)
        e_vector = Arrow3D(
            start=p_pos, 
            end=p_pos + np.array([1.2, 0, 0]), 
            color=YELLOW,
            base_radius=0.04,
            height=0.25
        )
        
        radial_text = Tex("Le champ $\\vec{E}$ doit appartenir à\\\\chaque plan de symétrie.\\\\Il est donc confondu avec leur\\\\intersection : il est RADIAL.", font_size=30)
        radial_text.to_corner(DL)
        self.add_fixed_in_frame_mobjects(radial_text)
        self.remove(radial_text)

        self.play(FadeOut(horiz_text))
        
        self.play(Create(intersect_line_dashed))
        self.play(Create(e_vector))
        
        self.play(Write(radial_text))
        self.wait(3)

        # On bascule en vue 2D pour montrer la rotation — plus lisible de face
        self.move_camera(phi=0 * DEGREES, theta=0 * DEGREES, zoom=0.75, run_time=2)
        self.wait(2)

        # ==========================================
        # PART 3: Argument 2 - The Magnitude depends only on r
        # ==========================================
        self.play(
            FadeOut(vert_plane),
            FadeOut(horiz_plane),
            FadeOut(intersect_line_dashed),
            FadeOut(radial_text),
            FadeOut(subtitle1)
        )

        subtitle2 = Tex("2. Invariances", font_size=36, color=GREEN)
        subtitle2.next_to(title, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(subtitle2)
        self.remove(subtitle2)
        self.play(Write(subtitle2))

        rot_text = Tex("Invariance par rotation :\\\\la norme $E$ ne dépend pas\\\\de l'angle $\\theta$.", font_size=30)
        rot_text.to_corner(DL)
        self.add_fixed_in_frame_mobjects(rot_text)
        self.remove(rot_text)
        
        self.play(Write(rot_text))
        
        # La ligne d'intersection a disparu, on anime seulement P et son vecteur E
        p_and_v = VGroup(point_p, e_vector)
        self.play(Rotate(p_and_v, angle=PI/2, about_point=ORIGIN, rate_func=smooth), run_time=2)
        self.wait(1)
        self.play(Rotate(p_and_v, angle=-PI/4, about_point=ORIGIN, rate_func=smooth), run_time=1.5)
        self.wait(2)

        # Retour en 3D pour montrer la translation selon z — visible qu'en perspective
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=1.0, run_time=2)
        self.play(FadeOut(rot_text))

        trans_text = Tex("Invariance par translation :\\\\la norme $E$ ne dépend pas\\\\de l'altitude $z$.", font_size=30)
        trans_text.to_corner(DL)
        self.add_fixed_in_frame_mobjects(trans_text)
        self.remove(trans_text)
        
        self.play(Write(trans_text))
        
        self.play(p_and_v.animate.shift(OUT * 2.5), run_time=2)
        self.wait(0.5)
        self.play(p_and_v.animate.shift(IN * 4), run_time=2)
        self.wait(0.5)
        self.play(p_and_v.animate.shift(OUT * 2.5), run_time=1.5)
        self.wait(2)

        self.play(FadeOut(trans_text))
        
        current_p_pos = point_p.get_center()
        axis_point = np.array([0, 0, current_p_pos[2]])
        r_line = DashedLine(start=axis_point, end=current_p_pos, color=WHITE)
        
        conclusion_text = Tex(
            "Le champ électrique $\\vec{E}$ ne dépend\\\\que de la distance $r$ :\\\\", 
            "$\\vec{E} = E(r)\\hat{e}_r$", 
            font_size=36, color=YELLOW
        )
        conclusion_text.to_corner(DL)
        self.add_fixed_in_frame_mobjects(conclusion_text)
        self.remove(conclusion_text)
        
        self.play(Create(r_line))
        self.play(Write(conclusion_text))
        self.wait(4)