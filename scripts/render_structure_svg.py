#!/usr/bin/env python3
"""Render the homepage SrTiO3 supercell as a static SVG.

The interactive 3Dmol viewer in layouts/index.html builds its model from
data/structures/srtio3.yaml. This script builds the same atoms from the same
file, applies the same initial view (rotation and perspective camera distance),
and draws a ball model with depth-sorted spheres and cell edges. Output is
deterministic.

Usage: python scripts/render_structure_svg.py   (or: make structure)
"""
import math
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "structures" / "srtio3.yaml"
OUT = ROOT / "static" / "images" / "structures" / "srtio3-supercell.svg"

SCALE = 34.0      # SVG units per Å
PADDING = 16.0    # SVG units around the model
EDGE_SEGMENTS = 12


def build_atoms(a, cells):
    """Same construction as the JavaScript in layouts/index.html."""
    atoms, seen = [], set()

    def add(element, x, y, z):
        key = f"{element}:{x:.3f}:{y:.3f}:{z:.3f}"
        if key not in seen:
            seen.add(key)
            atoms.append((element, x, y, z))

    for i in range(cells + 1):
        for j in range(cells + 1):
            for k in range(cells + 1):
                add("Sr", i * a, j * a, k * a)
    for i in range(cells):
        for j in range(cells):
            for k in range(cells):
                add("Ti", (i + 0.5) * a, (j + 0.5) * a, (k + 0.5) * a)
                add("O", (i + 0.5) * a, (j + 0.5) * a, k * a)
                add("O", (i + 0.5) * a, j * a, (k + 0.5) * a)
                add("O", i * a, (j + 0.5) * a, (k + 0.5) * a)
    return atoms


def rot_x(deg):
    t = math.radians(deg)
    c, s = math.cos(t), math.sin(t)
    return ((1, 0, 0), (0, c, -s), (0, s, c))


def rot_y(deg):
    t = math.radians(deg)
    c, s = math.cos(t), math.sin(t)
    return ((c, 0, s), (0, 1, 0), (-s, 0, c))


def matmul(m, n):
    return tuple(tuple(sum(m[i][k] * n[k][j] for k in range(3)) for j in range(3)) for i in range(3))


def apply(m, v):
    return tuple(sum(m[i][k] * v[k] for k in range(3)) for i in range(3))


def shade(hex_color, factor):
    """Mix with white (factor > 0) or black (factor < 0)."""
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    if factor >= 0:
        r, g, b = (round(c + (255 - c) * factor) for c in (r, g, b))
    else:
        r, g, b = (round(c * (1 + factor)) for c in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


def main():
    d = yaml.safe_load(DATA.read_text())
    a, cells = float(d["lattice_a"]), int(d["cells"])
    elements = d["elements"]
    length = a * cells
    centre = (length / 2,) * 3

    # 3Dmol: rotate(x) then rotate(y) gives R = Rx * Ry acting on the model.
    view = matmul(rot_x(d["view"]["rotate_x"]), rot_y(d["view"]["rotate_y"]))
    distance = float(d["view"]["camera_distance"])

    def project(p):
        """Perspective projection; returns screen x, y, depth (> 0 towards viewer), scale."""
        x, y, z = apply(view, tuple(p[i] - centre[i] for i in range(3)))
        f = distance / (distance - z)
        return x * f, y * f, z, f

    items = []  # (depth, order, svg)
    atoms = build_atoms(a, cells)
    projected = [(el, *project((x, y, z))) for el, x, y, z in atoms]  # el, x, y, z, f

    corners = [(0, 0, 0), (length, 0, 0), (0, length, 0), (0, 0, length),
               (length, length, 0), (length, 0, length), (0, length, length),
               (length, length, length)]
    edges = [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (2, 4),
             (2, 6), (3, 5), (3, 6), (4, 7), (5, 7), (6, 7)]

    xs, ys = [], []
    for el, x, y, z, f in projected:
        r = elements[el]["radius"] * f
        xs += [x - r, x + r]
        ys += [y - r, y + r]
    for c in corners:
        x, y, _, _ = project(c)
        xs.append(x)
        ys.append(y)
    min_x, max_x, min_y, max_y = min(xs), max(xs), min(ys), max(ys)
    width = (max_x - min_x) * SCALE + 2 * PADDING
    height = (max_y - min_y) * SCALE + 2 * PADDING

    def to_svg(x, y):
        return (x - min_x) * SCALE + PADDING, (max_y - y) * SCALE + PADDING

    order = 0
    for s, e in edges:
        p0, p1 = corners[s], corners[e]
        for n in range(EDGE_SEGMENTS):
            t0, t1 = n / EDGE_SEGMENTS, (n + 1) / EDGE_SEGMENTS
            q0 = project(tuple(p0[i] + (p1[i] - p0[i]) * t0 for i in range(3)))
            q1 = project(tuple(p0[i] + (p1[i] - p0[i]) * t1 for i in range(3)))
            (x0, y0), (x1, y1) = to_svg(q0[0], q0[1]), to_svg(q1[0], q1[1])
            items.append(((q0[2] + q1[2]) / 2, order,
                          f'<line x1="{x0:.2f}" y1="{y0:.2f}" x2="{x1:.2f}" y2="{y1:.2f}"/>'))
            order += 1

    for el, x, y, z, f in projected:
        cx, cy = to_svg(x, y)
        r = elements[el]["radius"] * f * SCALE
        items.append((z, order, f'<circle class="{el}" cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}"/>'))
        order += 1

    items.sort(key=lambda it: (round(it[0], 6), it[1]))

    grads = []
    for el, spec in elements.items():
        c = spec["color"]
        grads.append(
            f'<radialGradient id="g-{el}" cx="0.36" cy="0.32" r="0.72">'
            f'<stop offset="0" stop-color="{shade(c, 0.55)}"/>'
            f'<stop offset="0.45" stop-color="{c}"/>'
            f'<stop offset="1" stop-color="{shade(c, -0.35)}"/></radialGradient>')
    styles = "".join(f".{el}{{fill:url(#g-{el})}}" for el in elements)
    styles += f"line{{stroke:{d['edge_color']};stroke-width:2;stroke-linecap:round}}"

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.0f} {height:.0f}" '
        f'width="{width:.0f}" height="{height:.0f}">',
        f"<!-- {d['name']}: {cells}x{cells}x{cells} cells, a = {a} Å, {len(atoms)} atoms. "
        "Generated by scripts/render_structure_svg.py from data/structures/srtio3.yaml. -->",
        f"<defs>{''.join(grads)}<style>{styles}</style></defs>",
        *[it[2] for it in items],
        "</svg>",
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n")
    counts = {el: sum(1 for p in atoms if p[0] == el) for el in elements}
    print(f"wrote {OUT.relative_to(ROOT)}: {counts}, {width:.0f}x{height:.0f}")


if __name__ == "__main__":
    main()
