"""Render previews of the coach base parts (assembled on a table, and exploded).

    python cad/coach_base.py           # make the STLs first
    python cad/render_coach_base.py    # needs the `bpy` module (pip install bpy)
"""
import math
import os

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
STL = os.path.join(HERE, "out")
OUT = os.path.join(HERE, "..", "renders")
MM = 0.001

BASE_H, REAR_Y, JAW_Y, JAW_BOTTOM, NECK_Y = 60, 90, 68, -58, 62
TABLE_T = 25


def mat(name, rgb, rough=0.5, alpha=1.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Roughness"].default_value = rough
    if alpha < 1:
        b.inputs["Alpha"].default_value = alpha
    return m


def load(name, m, loc=(0, 0, 0), rot=(0, 0, 0)):
    bpy.ops.wm.stl_import(filepath=os.path.join(STL, f"{name}.stl"))
    o = bpy.context.selected_objects[0]
    o.scale = (MM, MM, MM)
    o.location = Vector(loc) * MM
    o.rotation_euler = [math.radians(a) for a in rot]
    o.data.materials.append(m)
    bpy.ops.object.shade_auto_smooth()
    return o


def box(size, loc, m):
    bpy.ops.mesh.primitive_cube_add(size=1, location=Vector(loc) * MM)
    o = bpy.context.object
    o.scale = Vector(size) * MM
    o.data.materials.append(m)
    return o


def cyl(r, h, loc, m):
    bpy.ops.mesh.primitive_cylinder_add(radius=r * MM, depth=h * MM, location=Vector(loc) * MM, vertices=64)
    o = bpy.context.object
    o.data.materials.append(m)
    bpy.ops.object.shade_smooth()
    return o


def scene(exploded):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    shell = mat("PETG warm white", (0.90, 0.88, 0.83), 0.45)
    clamp_m = mat("PC dark grey", (0.18, 0.19, 0.21), 0.4)
    tpu = mat("TPU teal", (0.30, 0.62, 0.60), 0.85)
    board = mat("board placeholder", (0.10, 0.35, 0.25), 0.4)
    wood = mat("table", (0.50, 0.36, 0.24), 0.6)
    tube = mat("neck tube", (0.6, 0.62, 0.65), 0.3)

    e = 1 if exploded else 0
    load("base", shell)
    box((160, 100, 26), (0, -10, 4 + 8 + 13 + e * 25), board)
    load("lid", shell, (0, 0, BASE_H + e * 90))
    cyl(16, 120, (0, NECK_Y, BASE_H + 4 + 60 + e * 150), tube)
    load("clamp", clamp_m, (0, e * 60, 0))
    load("knob", clamp_m, (0, JAW_Y + e * 60, JAW_BOTTOM - 7 - 18 - e * 40))
    load("pad_TPU", tpu, (0, JAW_Y + e * 60, -TABLE_T - 3 - e * 15))
    if not exploded:
        box((700, 500, TABLE_T), (0, REAR_Y - 250, -TABLE_T / 2), wood)

    world = bpy.data.worlds.new("w")
    bpy.context.scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.30, 0.33, 0.37, 1)
    world.node_tree.nodes["Background"].inputs[1].default_value = 0.5
    for loc, energy in (((-0.6, -0.8, 0.9), 45), ((0.8, 0.6, 0.6), 25), ((0.2, 0.9, -0.5), 20)):
        bpy.ops.object.light_add(type="AREA", location=loc)
        L = bpy.context.object
        L.data.energy = energy
        L.data.size = 0.6
        L.rotation_mode = "QUATERNION"
        L.rotation_quaternion = (Vector((0, 0, 0)) - Vector(loc)).to_track_quat("-Z", "Y")


def render(name, cam_loc, target, lens=40):
    bpy.ops.object.camera_add(location=cam_loc)
    c = bpy.context.object
    c.data.lens = lens
    c.rotation_mode = "QUATERNION"
    c.rotation_quaternion = (Vector(target) - Vector(cam_loc)).to_track_quat("-Z", "Y")
    sc = bpy.context.scene
    sc.camera = c
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = int(os.environ.get("SAMPLES", "64"))
    sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = 1400, 1050
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Medium High Contrast"
    sc.view_settings.exposure = -0.4
    sc.render.filepath = os.path.join(OUT, f"{name}.png")
    bpy.ops.render.render(write_still=True)
    print("wrote", sc.render.filepath)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    scene(exploded=False)
    render("coach_base_on_table", (0.42, 0.55, 0.26), (0, 0.03, 0.0))
    scene(exploded=True)
    render("coach_base_exploded", (0.60, 0.62, 0.30), (0, 0.04, 0.05), lens=32)
