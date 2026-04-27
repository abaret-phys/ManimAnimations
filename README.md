> 🇬🇧 **English below** · 🇫🇷 Français en premier

---

# Animations pédagogiques — Introduction à l'Électromagnétisme

Animations [ManimCE](https://www.manim.community/) pour un cours d'introduction à l'électromagnétisme (PHYS1986).  
Chaque fichier est une scène autonome conçue pour illustrer un concept précis en ~1–2 minutes.

Les vidéos rendues sont hébergées sur Vimeo. GitHub ne peut pas lire les vidéos en ligne.

---

## Contenu

Les animations suivent approximativement la progression d'un cours standard : champ électrique, flux et loi de Gauss, théorème d'Ampère, induction, forces magnétiques, ondes électromagnétiques. Visualisation des symétries spatiales.

### Champ électrique et flux

| Fichier | Scène | Description |
|---|---|---|
| `flux.py` | `FluxIntuition` | **Flux électrique** — deux parties : (1) l'aire projetée et le produit scalaire, avec une surface tournante et son ombre ; (2) pourquoi le flux est invariant par distance grâce à la loi en 1/r^2. |
| `Gauss.py` | `GaussAdvanced` | **Loi de Gauss** — surface de Gauss qui se déforme sans changer le flux ; charge déplacée à l'intérieur puis à l'extérieur ; comptage visuel des intersections entrée/sortie.

### Symétries et invariances

| Fichier | Scène(s) | Description |
|---|---|---|
| `symetriespherique.py` | `SymetrieSpherique2D` | **Symétrie sphérique + plan infini** — version plate (tout dans `construct()`). Partie 1 : argument par rotation pour montrer que E est radial et que ‖E‖ est constant sur la sphère. Partie 2 : simulation d'une vue 3D → coupe 2D, arguments de translation et de miroir pour le plan infini, compensation 1/r² × r². |
| `symetrieplaninfini.py` | `SymetrieSpherique2D` · `SymetrieSpherique` · `PlanInfini` | **Idem, version refactorisée** — mêmes scènes découpées en méthodes `_run_part1()` / `_run_part2()`. Permet de rendre chaque partie séparément. |
| `symetriecylindrique.py` | `ElectricFieldSymmetry` | **Symétrie cylindrique** — cylindre infini en 3D, deux plans de symétrie (vertical XZ et horizontal XY), leur intersection donne la direction radiale de E ; invariances par rotation et translation. |

### Théorème d'Ampère

| Fichier | Scène | Description |
|---|---|---|
| `ampere.py` | `AmpereLaw` | **Théorème d'Ampère** — fil infini en 3D avec anneaux de champ ; transition vers la vue 2D ; contour circulaire puis contour quelconque (patate) ; calcul du flux net et indépendance par rapport à la forme. |

### Induction et loi de Lenz

| Fichier | Scène | Description |
|---|---|---|
| `Lenz_31_3.py` | `AmpereLenz3D` | **Loi de Lenz — approche visuelle** — fil parcouru par un courant décroissant, anneaux de champ magnétique en 3D, passage en vue 2D ; courant induit qui s'oppose à la diminution du flux ; formule E = −dΦ/dt avec le signe « − » mis en évidence. |
| `Lenz_31_5.py` | `LenzCompleteExercise` | **Exercice complet** — boucle rectangulaire qui sort d'une zone de champ à vitesse constante ; graphe de Φ(t) et dΦ/dt tracé en temps réel ; courant induit visible pendant la phase de sortie. |

### Magnétisme de la matière

| Fichier | Scène | Description |
|---|---|---|
| `magnetismMatter.py` | `MagneticMaterials` | **Dia/para/ferromagnétisme** — trois colonnes côte à côte ; zoom dans un domaine de Weiss pour voir les moments dipolaires alignés ; application et coupure du champ B₀ (rémanence) ; chauffage jusqu'à la température de Curie (770 °C) et disparition des domaines. |

### Forces magnétiques

| Fichier | Scène(s) | Description |
|---|---|---|
| `magneticforce.py` | `MagneticForceMotion` | **Force de Lorentz** — particule chargée entrant dans une zone de champ B uniforme ; mouvement circulaire uniforme en 2D (F perpendiculaire à v) ; passage en 3D avec une composante v∥ → trajectoire hélicoïdale. |
| `laplaceforce.py` | `LaplaceForceMicroscopic` | **Force de Laplace — vue microscopique** — zoom sur un conducteur ; électrons dérivant sous F = qv×B, courbant vers le haut et poussant le réseau par collisions ; force macroscopique F = IL×B. |
| `laplaceforce.py` | `LaplaceForceSetup3D` | **Montage expérimental 3D** — aimant en C, deux rails, tige métallique ; vecteurs B, I, F affichés ; rotation ambiante pour percevoir la 3D ; la tige glisse vers la sortie du gap. |

### Ondes électromagnétiques

| Fichier | Scène | Description |
|---|---|---|
| `em_wave.py` | `EMWaveLocalLente` | **Onde EM plane** — champs E et B oscillant en quadrature dans les plans y et z ; plan d'observation mobile ; vecteur de Poynting S = (1/μ₀) E×B tracé en temps réel ; balayage de caméra final. |

---

## Vidéos

> Les vidéos sont hébergées sur Vimeo.

- [Flux électrique et aire projetée](https://vimeo.com/1186660839)
- [Loi de Gauss — surface quelconque](https://vimeo.com/1184928561)
- [Symétrie sphérique et plan infini](https://vimeo.com/1185282780)
- [Symétrie du plan infini](https://vimeo.com/1185282750)
- [Symétrie cylindrique — cylindre infini](https://vimeo.com/1186469601)
- [Théorème d'Ampère](https://vimeo.com/1184928482)
- [Loi de Lenz — courant induit](https://vimeo.com/1184928518)
- [Dia/para/ferromagnétisme, température de Curie](https://vimeo.com/1184928580)
- [Force magnétique — circulaire et hélicoïdale](https://vimeo.com/1186478753)
- [Force de Laplace — vue microscopique](https://vimeo.com/1186651790)
- [Onde électromagnétique et vecteur de Poynting](https://vimeo.com/1186660839)

---

## Dépendances

- Python ≥ 3.9
- [ManimCE](https://www.manim.community/) ≥ 0.18
- LaTeX (pour le rendu des formules — [MiKTeX](https://miktex.org/) ou [TeX Live](https://tug.org/texlive/))

```bash
pip install manim
```

---

## Utilisation

```bash
# Aperçu rapide (basse qualité)
manim -pql flux.py FluxIntuition

# Rendu haute qualité (1080p)
manim -pqh Gauss.py GaussAdvanced

# Scènes autonomes dans symetrieplaninfini.py
manim -pql symetrieplaninfini.py SymetrieSpherique   # symétrie sphérique seulement
manim -pql symetrieplaninfini.py PlanInfini           # plan infini seulement
manim -pql symetrieplaninfini.py SymetrieSpherique2D  # vidéo complète (les deux)
```

Les fichiers rendus se trouvent dans `media/videos/`.

---

## Licence

[MIT](LICENSE) — libre d'utilisation et d'adaptation, avec attribution.

---
---

# Pedagogical Animations — Introduction to Electromagnetism

[ManimCE](https://www.manim.community/) animations for a first-year university electromagnetism course.  
Each file is a self-contained scene designed to illustrate one specific concept in ~1–2 minutes.

Videos are hosted on Vimeo. GitHub cannot play videos inline.

---

## Contents

Animations roughly follow the standard course progression: electric field, flux and Gauss's law, Ampère's theorem, induction, then magnetic forces.

### Electric field and flux

| File | Scene | Description |
|---|---|---|
| `flux.py` | `FluxIntuition` | **Electric flux** — two parts: (1) the projected area and the dot product E·n, using a rotating surface and its shadow; (2) why flux is distance-invariant thanks to the 1/r² law. |
| `Gauss.py` | `GaussAdvanced` | **Gauss's law** — a Gaussian surface that morphs (circle → potato) without changing the flux; charge moved inside then outside; visual counting of entry/exit intersections. |

### Symmetries and invariances

| File | Scene(s) | Description |
|---|---|---|
| `symetriespherique.py` | `SymetrieSpherique2D` | **Spherical symmetry + infinite plane** — flat version (everything in `construct()`). Part 1: rotation argument showing E is radial and ‖E‖ is constant on the sphere. Part 2: simulated 3D → 2D cross-section, translation and mirror arguments for the infinite plane, 1/r² × r² compensation. |
| `symetrieplaninfini.py` | `SymetrieSpherique2D` · `SymetrieSpherique` · `PlanInfini` | **Same, refactored version** — scenes split into `_run_part1()` / `_run_part2()` methods, allowing each part to be rendered independently. |
| `symetriecylindrique.py` | `ElectricFieldSymmetry` | **Cylindrical symmetry** — infinite cylinder in 3D, two symmetry planes (vertical XZ and horizontal XY), their intersection gives the radial direction of E; rotation and translation invariances. |

### Ampère's theorem

| File | Scene | Description |
|---|---|---|
| `ampere.py` | `AmpereLaw` | **Ampère's theorem** — infinite wire in 3D with field rings; transition to 2D view; circular contour then arbitrary contour (potato shape); net flux calculation and shape independence. |

### Induction and Lenz's law

| File | Scene | Description |
|---|---|---|
| `Lenz_31_3.py` | `AmpereLenz3D` | **Lenz's law — visual approach** — wire carrying a decreasing current, magnetic field rings in 3D, switch to 2D view; induced current opposing the flux decrease; formula E = −dΦ/dt with the "−" sign highlighted. |
| `Lenz_31_5.py` | `LenzCompleteExercise` | **Full exercise** — rectangular loop exiting a field region at constant velocity; Φ(t) and dΦ/dt graph drawn in real time; induced current visible during the exit phase. |

### Magnetic properties of matter

| File | Scene | Description |
|---|---|---|
| `magnetismMatter.py` | `MagneticMaterials` | **Dia/para/ferromagnetism** — three columns side by side; zoom into a Weiss domain to see aligned magnetic dipole moments; B₀ field applied and removed (remanence); heating to the Curie temperature (770 °C) and domain wall dissolution. |

### Magnetic forces

| File | Scene(s) | Description |
|---|---|---|
| `magneticforce.py` | `MagneticForceMotion` | **Lorentz force** — charged particle entering a uniform B field region; uniform circular motion in 2D (F perpendicular to v); transition to 3D with a v∥ component → helical trajectory. |
| `laplaceforce.py` | `LaplaceForceMicroscopic` | **Laplace force — microscopic view** — zoom into a conductor; electrons drifting under F = qv×B, curving upward and pushing the lattice through collisions; macroscopic force F = IL×B. |
| `laplaceforce.py` | `LaplaceForceSetup3D` | **3D experimental setup** — C-shaped magnet, two rails, metallic rod; B, I, F vectors displayed; ambient camera rotation to convey 3D depth; rod slides out of the magnet gap. |

### Electromagnetic waves

| File | Scene | Description |
|---|---|---|
| `em_wave.py` | `EMWaveLocalLente` | **Plane EM wave** — E and B fields oscillating in the y and z planes; observation plane; Poynting vector S = (1/μ₀) E×B drawn in real time; final camera sweep. |

---

## Videos

> Videos are hosted on Vimeo.

- [Electric flux and projected area](https://vimeo.com/1186660839)
- [Gauss's law — arbitrary surface](https://vimeo.com/1184928561)
- [Spherical symmetry and infinite plane](https://vimeo.com/1185282780)
- [Infinite plane symmetry](https://vimeo.com/1185282750)
- [Cylindrical symmetry — infinite cylinder](https://vimeo.com/1186469601)
- [Ampère's theorem](https://vimeo.com/1184928482)
- [Lenz's law — induced current](https://vimeo.com/1184928518)
- [Dia/para/ferromagnetism, Curie temperature](https://vimeo.com/1184928580)
- [Magnetic force — circular and helical motion](https://vimeo.com/1186478753)
- [Laplace force — microscopic view](https://vimeo.com/1186651790)
- [Electromagnetic wave and Poynting vector](https://vimeo.com/1186660839)

---

## Dependencies

- Python ≥ 3.9
- [ManimCE](https://www.manim.community/) ≥ 0.18
- LaTeX for formula rendering ([MiKTeX](https://miktex.org/) or [TeX Live](https://tug.org/texlive/))

```bash
pip install manim
```

---

## Usage

```bash
# Quick preview (low quality)
manim -pql flux.py FluxIntuition

# High quality render (1080p)
manim -pqh Gauss.py GaussAdvanced

# Standalone scenes in symetrieplaninfini.py
manim -pql symetrieplaninfini.py SymetrieSpherique   # spherical symmetry only
manim -pql symetrieplaninfini.py PlanInfini           # infinite plane only
manim -pql symetrieplaninfini.py SymetrieSpherique2D  # full video (both parts)
```

Rendered files are saved in `media/videos/`.

---

## License

[MIT](LICENSE) — free to use and adapt, with attribution.
