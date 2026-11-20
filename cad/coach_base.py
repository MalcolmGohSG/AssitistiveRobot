"""Workstation coach: electronics base, lid and table clamp (fit-test v0.1).

Code-based CAD with build123d. Every dimension is a named parameter below,
so a change is one edit and a re-run:

    pip install build123d
    python cad/coach_base.py          # writes cad/out/*.stl and *.step

Units are mm. Base frame: origin at the centre of the base's underside,
+Y towards the rear, Z up. The table top is at Z = 0 and the table's edge
lines up with the base's rear face (Y = BASE_W / 2).

Parts
  base   - enclosure holding the Arduino VENTUNO Q by its corners
  lid    - vented lid with a socket for the neck tube that carries the head
  clamp  - C-clamp bolted to the base's rear wall and gripping the table edge
  knob   - hand knob for the M8 clamp bolt (no tools needed in a classroom)
  pad    - soft pressure pad for the end of the clamp bolt (print in TPU)
"""
from pathlib import Path

from build123d import (Axis, Box, Cylinder,
                       Pos, RectangleRounded, RegularPolygon, Rot, export_step,
                       export_stl, extrude, fillet)

OUT = Path(__file__).parent / "out"

# ---------------------------------------------------------------- parameters
# Board: Arduino VENTUNO Q, 160 x 100 x 25.8 mm (height excludes heatsink/fan).
# MEASURE YOUR BOARD and update these before printing the final version.
BOARD_L, BOARD_W = 160.0, 100.0
BOARD_Y = -10.0           # board centre, shifted forward to leave room for the neck socket
BOARD_CLEAR = 0.5         # gap around the board edge
POST_H = 8.0              # air gap under the board
POST = 10.0               # corner support post size
FENCE_H = 5.0             # how far the corner fences rise above the board's underside
FENCE_T = 2.0
FENCE_LEN = 14.0

BASE_L, BASE_W, BASE_H = 240.0, 180.0, 60.0
WALL, FLOOR, CORNER_R = 3.5, 4.0, 18.0

INSERT_D, INSERT_DEPTH = 4.0, 8.0     # M3 heat-set insert
BOSS_D = 10.0

CLAMP_BOLT_X = 25.0       # two M5 bolts, +/- this X
CLAMP_BOLT_Z = 30.0
M5_HOLE, M5_NUT_R, M5_NUT_T = 5.5, 4.75, 4.5

LID_T = 4.0
NECK_D, NECK_Y = 32.0, 62.0           # neck tube outer diameter, socket position
SOCKET_OD, SOCKET_H = 46.0, 20.0

# Clamp: fits tables 15-36 mm thick
CLAMP_W, CLAMP_T = 80.0, 10.0
JAW_REACH, JAW_T, JAW_TOP = 40.0, 12.0, -46.0
INNER_FILLET = 8.0
M8_HOLE, M8_NUT_R, M8_NUT_T = 8.4, 7.7, 7.0
CLAMP_TOP = 48.0

REAR_Y = BASE_W / 2


# ---------------------------------------------------------------- parts
def rounded_slab(l, w, r, h, z0=0.0):
    return Pos(0, 0, z0) * extrude(RectangleRounded(l, w, r), h)


def base():
    shell = rounded_slab(BASE_L, BASE_W, CORNER_R, BASE_H)
    shell -= rounded_slab(BASE_L - 2 * WALL, BASE_W - 2 * WALL, CORNER_R - WALL, BASE_H, FLOOR)

    # board corner posts and L-shaped fences
    hx, y_front, y_rear = BOARD_L / 2, BOARD_Y - BOARD_W / 2, BOARD_Y + BOARD_W / 2
    for sx in (-1, 1):
        for sy, ye in ((-1, y_front), (1, y_rear)):
            shell += Pos(sx * (hx - POST / 2), ye - sy * POST / 2, FLOOR + POST_H / 2) * Box(POST, POST, POST_H)
            fz = FLOOR + (POST_H + FENCE_H) / 2
            off = BOARD_CLEAR + FENCE_T / 2
            shell += Pos(sx * (hx - FENCE_LEN / 2), ye + sy * off, fz) * Box(FENCE_LEN, FENCE_T, POST_H + FENCE_H)
            shell += Pos(sx * (hx + off), ye - sy * FENCE_LEN / 2, fz) * Box(FENCE_T, FENCE_LEN, POST_H + FENCE_H)

    # lid screw bosses with heat-set insert holes
    bx, by = BASE_L / 2 - 14, BASE_W / 2 - 14
    for sx in (-1, 1):
        for sy in (-1, 1):
            h = BASE_H - FLOOR
            shell += Pos(sx * bx, sy * by, FLOOR + h / 2) * Cylinder(BOSS_D / 2, h)
            shell -= Pos(sx * bx, sy * by, BASE_H - INSERT_DEPTH / 2) * Cylinder(INSERT_D / 2, INSERT_DEPTH)

    # rear wall: thickened blocks with captive M5 nuts for the clamp
    inner_rear = REAR_Y - WALL
    for sx in (-1, 1):
        x = sx * CLAMP_BOLT_X
        shell += Pos(x, inner_rear - 5, CLAMP_BOLT_Z) * Box(16, 10, 16)
        shell -= Pos(x, REAR_Y - 7, CLAMP_BOLT_Z) * Rot(90, 0, 0) * Cylinder(M5_HOLE / 2, 16)
        nut_y = inner_rear - 10 + M5_NUT_T / 2
        shell -= Pos(x, nut_y, CLAMP_BOLT_Z) * Rot(90, 0, 0) * Rot(0, 0, 30) * extrude(
            RegularPolygon(M5_NUT_R, 6), M5_NUT_T / 2, both=True)

    # rear power-cable port, left-side service window, front speaker grille
    shell -= Pos(-70, REAR_Y, 40) * Box(24, 3 * WALL, 12)
    shell -= Pos(-BASE_L / 2, BOARD_Y, FLOOR + POST_H + 14) * Box(3 * WALL, 100, 26)
    for i in range(-3, 4):
        for j in range(-3, 4):
            x, z = 60 + i * 6 + (j % 2) * 3, 34 + j * 5.2
            if (x - 60) ** 2 + (z - 34) ** 2 <= 18 ** 2:
                shell -= Pos(x, -BASE_W / 2, z) * Rot(90, 0, 0) * Cylinder(2.0, 3 * WALL)
    return shell


def lid():
    # Flat plate, printed as modelled (plate on the bed, socket up) so it needs
    # no supports. The four screws locate it on the base.
    part = rounded_slab(BASE_L, BASE_W, CORNER_R, LID_T)

    # screw holes, countersunk from the top (M3)
    bx, by = BASE_L / 2 - 14, BASE_W / 2 - 14
    for sx in (-1, 1):
        for sy in (-1, 1):
            part -= Pos(sx * bx, sy * by, LID_T / 2) * Cylinder(1.7, LID_T)
            part -= Pos(sx * bx, sy * by, LID_T - 0.9) * Cylinder(3.1, 1.8)

    # vent slots over the board
    for i in range(-6, 7):
        part -= Pos(i * 9, BOARD_Y, LID_T / 2) * Box(4, 60, LID_T)

    # neck socket with a side set-screw hole (M4)
    part += Pos(0, NECK_Y, LID_T + SOCKET_H / 2) * Cylinder(SOCKET_OD / 2, SOCKET_H)
    part -= Pos(0, NECK_Y, (LID_T + SOCKET_H) / 2) * Cylinder(NECK_D / 2 + 0.2, LID_T + SOCKET_H)
    part -= Pos(SOCKET_OD / 4, NECK_Y, LID_T + SOCKET_H / 2) * Rot(0, 90, 0) * Cylinder(1.7, SOCKET_OD / 2)
    return part


def clamp():
    y0, y1 = REAR_Y, REAR_Y + CLAMP_T
    z_bot = JAW_TOP - JAW_T
    # L-shaped profile in the YZ plane: plate behind the table edge + jaw under the table
    plate = Pos(0, (y0 + y1) / 2, (CLAMP_TOP + z_bot) / 2) * Box(CLAMP_W, CLAMP_T, CLAMP_TOP - z_bot)
    jaw = Pos(0, (y0 - JAW_REACH + y1) / 2, z_bot + JAW_T / 2) * Box(CLAMP_W, JAW_REACH + CLAMP_T, JAW_T)
    part = plate + jaw

    def x_edges_at(y, z):
        return [e for e in part.edges().filter_by(Axis.X)
                if abs(e.center().Y - y) < 1e-3 and abs(e.center().Z - z) < 1e-3]

    part = fillet(x_edges_at(y0, JAW_TOP), radius=INNER_FILLET)      # inside corner: strength
    part = fillet(x_edges_at(y1, z_bot) + x_edges_at(y0 - JAW_REACH, z_bot)
                  + x_edges_at(y0 - JAW_REACH, JAW_TOP) + x_edges_at(y1, CLAMP_TOP)
                  + x_edges_at(y0, CLAMP_TOP), radius=3)

    for sx in (-1, 1):   # M5 bolt holes with head counterbores on the outside
        x = sx * CLAMP_BOLT_X
        part -= Pos(x, y0 + CLAMP_T / 2, CLAMP_BOLT_Z) * Rot(90, 0, 0) * Cylinder(M5_HOLE / 2, CLAMP_T)
        part -= Pos(x, y1 - 2, CLAMP_BOLT_Z) * Rot(90, 0, 0) * Cylinder(5.2, 4)

    jaw_y = y0 - JAW_REACH / 2 - 2
    part -= Pos(0, jaw_y, z_bot + JAW_T / 2) * Cylinder(M8_HOLE / 2, JAW_T)
    part -= Pos(0, jaw_y, z_bot + M8_NUT_T / 2) * Rot(0, 0, 30) * extrude(
        RegularPolygon(M8_NUT_R, 6), M8_NUT_T / 2, both=True)
    return part


def knob():
    k = Cylinder(20, 14)
    for i in range(8):                     # finger scallops
        k -= Rot(0, 0, i * 45) * Pos(21, 0, 0) * Cylinder(4.5, 14)
    k -= Cylinder(M8_HOLE / 2, 14)
    k -= Pos(0, 0, -7 + 2.8) * Rot(0, 0, 30) * extrude(RegularPolygon(7.6, 6), 2.8, both=True)  # M8 bolt head
    return k


def pad():
    p = Cylinder(12, 6)
    p -= Pos(0, 0, -3 + 2) * Cylinder(4.2, 4)   # bolt tip socket
    return p


PARTS = {"base": base, "lid": lid, "clamp": clamp, "knob": knob, "pad_TPU": pad}


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name, make in PARTS.items():
        solid = make()
        bb = solid.bounding_box()
        export_stl(solid, str(OUT / f"{name}.stl"))
        export_step(solid, str(OUT / f"{name}.step"))
        print(f"{name:8s} {bb.size.X:6.1f} x {bb.size.Y:6.1f} x {bb.size.Z:6.1f} mm  "
              f"volume {solid.volume / 1000:6.1f} cm3  valid={solid.is_valid}")
