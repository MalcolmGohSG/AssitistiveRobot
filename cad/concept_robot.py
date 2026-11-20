"""Concept model of the assistive robot ("Kawan" working name).

Not an engineering model: proportions and layout only, to discuss the design.
Units are metres, Z up, the robot faces -Y.

Run headless:   python concept_robot.py  (with the `bpy` module installed)
Or in Blender:  Scripting tab -> open this file -> Run Script
                (rendering is skipped inside the GUI; the scene is built so you
                 can orbit it, and saved/exported only when run headless)
"""
import math
import os
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "renders")
HEADLESS = bpy.app.background or "bpy" in sys.modules and not hasattr(bpy.context, "window")


# ---------------------------------------------------------------- helpers
def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def mat(name, rgb, rough=0.5, emit=0.0, metal=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit:
        b.inputs["Emission Color"].default_value = (*rgb, 1)
        b.inputs["Emission Strength"].default_value = emit
    return m


def assign(obj, m):
    obj.data.materials.clear()
    obj.data.materials.append(m)
    return obj


def smooth(obj):
    for p in obj.data.polygons:
        p.use_smooth = True
    return obj


def rounded_box(name, size, loc, radius, m):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = size
    bpy.ops.object.transform_apply(scale=True)
    bev = o.modifiers.new("bevel", "BEVEL")
    bev.width = radius
    bev.segments = 8
    bev.limit_method = "NONE"
    return smooth(assign(o, m))


def cyl(name, r, depth, loc, m, rot=(0, 0, 0), verts=64):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc,
                                        rotation=rot, vertices=verts)
    o = bpy.context.object
    o.name = name
    return smooth(assign(o, m))


def sphere(name, r, loc, m):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=48, ring_count=24)
    o = bpy.context.object
    o.name = name
    return smooth(assign(o, m))


def rod(name, p1, p2, r, m):
    p1, p2 = Vector(p1), Vector(p2)
    d = p2 - p1
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d.length,
                                        location=(p1 + p2) / 2, vertices=48)
    o = bpy.context.object
    o.name = name
    o.rotation_mode = "QUATERNION"
    o.rotation_quaternion = d.to_track_quat("Z", "Y")
    return smooth(assign(o, m))


def torus(name, R, r, loc, m):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc,
                                     major_segments=96, minor_segments=24)
    o = bpy.context.object
    o.name = name
    return smooth(assign(o, m))


def arm(side, shoulder, elbow, wrist, M):
    rod(f"upper_{side}", shoulder, elbow, 0.028, M["shell"])
    rod(f"fore_{side}", elbow, wrist, 0.024, M["shell"])
    for n, p, r in (("shoulder", shoulder, 0.042), ("elbow", elbow, 0.034),
                    ("wrist", wrist, 0.030)):
        sphere(f"{n}_{side}", r, p, M["joint"])
    # simple two-finger gripper, soft TPU pads
    w = Vector(wrist)
    fwd = (w - Vector(elbow)).normalized()
    across = fwd.cross(Vector((0, 0, 1))).normalized()
    palm = w + fwd * 0.04
    rod(f"palm_{side}", w, palm, 0.026, M["joint"])
    for s in (-1, 1):
        base = palm + across * 0.018 * s
        rod(f"finger_{side}_{s}", base, base + fwd * 0.07, 0.008, M["skin"])


# ---------------------------------------------------------------- build
def build():
    reset()
    M = {
        "shell": mat("shell_PETG_warm_white", (0.92, 0.90, 0.85), 0.45),
        "skin": mat("skin_TPU_soft_teal", (0.35, 0.68, 0.66), 0.85),
        "joint": mat("joint_dark_grey", (0.12, 0.13, 0.15), 0.4),
        "screen": mat("screen_black", (0.01, 0.01, 0.015), 0.15),
        "eye": mat("eye_cyan_emit", (0.35, 0.9, 1.0), 0.3, emit=6.0),
        "ring": mat("calm_light_ring", (0.55, 0.85, 1.0), 0.3, emit=3.0),
        "btn_g": mat("btn_finished_green", (0.20, 0.65, 0.30), 0.35),
        "btn_y": mat("btn_help_yellow", (0.95, 0.75, 0.15), 0.35),
        "btn_b": mat("btn_break_blue", (0.20, 0.45, 0.85), 0.35),
        "estop": mat("estop_red", (0.85, 0.08, 0.06), 0.35),
        "floor": mat("floor", (0.36, 0.35, 0.34), 0.8),
        "wood": mat("table_wood", (0.45, 0.30, 0.18), 0.55),
        "bowl": mat("bowl_ceramic", (0.93, 0.93, 0.95), 0.2),
        "chop": mat("chopsticks", (0.55, 0.36, 0.20), 0.5),
        "lens": mat("lens", (0.02, 0.02, 0.03), 0.05, metal=0.5),
    }

    # floor
    bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 0, 0))
    assign(bpy.context.object, M["floor"])

    # ---- mobile base (differential drive, ~48 cm diameter)
    cyl("base_shell", 0.235, 0.17, (0, 0, 0.145), M["shell"])
    bpy.context.object.modifiers.new("bevel", "BEVEL").width = 0.03
    torus("bumper_TPU", 0.24, 0.035, (0, 0, 0.09), M["skin"])        # soft contact ring
    for s in (-1, 1):
        cyl(f"drive_wheel_{s}", 0.075, 0.04, (0.215 * s, 0, 0.075), M["joint"],
            rot=(0, math.pi / 2, 0))
    # depth camera low on the front for obstacles / stair edges
    rounded_box("depth_cam_low", (0.10, 0.03, 0.03), (0, -0.235, 0.20), 0.008, M["joint"])
    for s in (-1, 1):
        cyl(f"lens_low_{s}", 0.008, 0.01, (0.03 * s, -0.252, 0.20), M["lens"],
            rot=(math.pi / 2, 0, 0))
    # lidar puck
    cyl("lidar", 0.045, 0.04, (0, -0.10, 0.25), M["joint"])

    # ---- lift mast (telescopic: counter height for the kitchen, low for the floor)
    cyl("mast_lower", 0.05, 0.40, (0, 0.02, 0.43), M["joint"])
    cyl("mast_upper", 0.042, 0.20, (0, 0.02, 0.70), M["shell"])

    # ---- torso with AAC buttons
    rounded_box("torso", (0.34, 0.22, 0.32), (0, 0, 0.93), 0.06, M["shell"])
    for x, m, label in ((-0.085, M["btn_y"], "help"), (0.0, M["btn_b"], "break"),
                        (0.085, M["btn_g"], "finished")):
        cyl(f"btn_{label}", 0.032, 0.02, (x, -0.115, 0.88), m, rot=(math.pi / 2, 0, 0))
    # emergency stop on top-back, reachable by staff
    cyl("estop_collar", 0.03, 0.015, (0.12, 0.07, 1.095), M["joint"])
    cyl("estop", 0.024, 0.02, (0.12, 0.07, 1.11), M["estop"])

    # ---- guide handle on the left-rear: rigid, Glide-style, for a person walking beside
    hp0 = Vector((-0.17, 0.06, 0.92))
    hp1 = Vector((-0.30, 0.20, 0.92))
    hp2 = Vector((-0.30, 0.20, 0.90))
    rod("handle_arm", hp0, hp1, 0.018, M["joint"])
    rod("handle_grip", hp2 + Vector((0, -0.07, 0)), hp2 + Vector((0, 0.07, 0)), 0.024, M["skin"])
    sphere("handle_elbow", 0.022, hp1, M["joint"])

    # ---- two light arms (SO-101 class), right one reaching to the table
    arm("R", (0.20, -0.02, 1.00), (0.27, -0.16, 0.86), (0.20, -0.38, 0.80), M)
    arm("L", (-0.20, -0.02, 1.00), (-0.25, -0.06, 0.80), (-0.21, -0.20, 0.66), M)

    # ---- neck, calm light ring, head with screen face
    cyl("neck", 0.035, 0.08, (0, 0, 1.12), M["joint"])
    torus("light_ring", 0.055, 0.010, (0, 0, 1.115), M["ring"])
    rounded_box("head", (0.30, 0.14, 0.20), (0, -0.005, 1.25), 0.05, M["shell"])
    rounded_box("face_screen", (0.24, 0.01, 0.14), (0, -0.077, 1.245), 0.03, M["screen"])
    for s in (-1, 1):
        cyl(f"eye_{s}", 0.022, 0.004, (0.055 * s, -0.084, 1.26), M["eye"],
            rot=(math.pi / 2, 0, 0))
    # soft smile
    bpy.ops.mesh.primitive_torus_add(major_radius=0.04, minor_radius=0.004,
                                     location=(0, -0.084, 1.235), rotation=(math.pi / 2, 0, 0),
                                     major_segments=64, minor_segments=8)
    smile = bpy.context.object
    assign(smile, M["eye"])
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="DESELECT")
    bpy.ops.object.mode_set(mode="OBJECT")
    for v in smile.data.vertices:
        v.select = v.co.y > -0.012           # local Y is world Z here: keep the lower arc
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.delete(type="VERT")
    bpy.ops.object.mode_set(mode="OBJECT")
    # head camera (stereo) above the screen
    rounded_box("head_cam", (0.12, 0.025, 0.025), (0, -0.07, 1.335), 0.008, M["joint"])
    for s in (-1, 1):
        cyl(f"lens_head_{s}", 0.007, 0.01, (0.035 * s, -0.085, 1.335), M["lens"],
            rot=(math.pi / 2, 0, 0))

    # ---- context: a low Singapore-style dining table with bowl and chopsticks
    rounded_box("table_top", (0.9, 0.6, 0.03), (0.15, -0.75, 0.745), 0.01, M["wood"])
    for x in (-0.25, 0.55):
        for y in (-0.5, -1.0):
            cyl("table_leg", 0.02, 0.73, (x, y, 0.365), M["wood"])
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.065, location=(0.12, -0.62, 0.80),
                                         segments=48, ring_count=24)
    bowl = smooth(assign(bpy.context.object, M["bowl"]))
    bowl.scale.z = 0.75
    sol = bowl.modifiers.new("solid", "SOLIDIFY")
    sol.thickness = 0.004
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="DESELECT")
    bpy.ops.object.mode_set(mode="OBJECT")
    for v in bowl.data.vertices:
        v.select = v.co.z > 0.0
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.delete(type="VERT")
    bpy.ops.object.mode_set(mode="OBJECT")
    for dx in (0.0, 0.012):
        rod("chopstick", (0.22 + dx, -0.70, 0.765), (0.25 + dx, -0.48, 0.765), 0.0035, M["chop"])
    # spoon rest
    rounded_box("chopstick_rest", (0.04, 0.012, 0.01), (0.235, -0.67, 0.765), 0.004, M["bowl"])

    return M


# ---------------------------------------------------------------- render
def lights_and_world():
    world = bpy.data.worlds.new("w")
    bpy.context.scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.30, 0.33, 0.37, 1)
    world.node_tree.nodes["Background"].inputs[1].default_value = 0.45
    for name, loc, energy, size in (("key", (-2.0, -2.5, 3.0), 900, 2.0),
                                    ("fill", (2.5, -1.0, 2.0), 350, 3.0),
                                    ("rim", (0.5, 2.5, 2.5), 500, 2.0)):
        bpy.ops.object.light_add(type="AREA", location=loc)
        L = bpy.context.object
        L.name = name
        L.data.energy = energy
        L.data.size = size
        L.rotation_mode = "QUATERNION"
        L.rotation_quaternion = (Vector((0, 0, 0.8)) - Vector(loc)).to_track_quat("-Z", "Y")


def camera(name, loc, target, lens=50):
    bpy.ops.object.camera_add(location=loc)
    c = bpy.context.object
    c.name = name
    c.data.lens = lens
    c.rotation_mode = "QUATERNION"
    c.rotation_quaternion = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y")
    return c


def render_views():
    os.makedirs(OUT, exist_ok=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = int(os.environ.get("SAMPLES", "96"))
    sc.cycles.use_denoising = True
    sc.render.resolution_x = 1400
    sc.render.resolution_y = 1050
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Medium High Contrast"
    sc.view_settings.exposure = -0.6
    lights_and_world()
    views = {
        "front_three_quarter": ((1.55, -2.15, 1.25), (0.05, -0.2, 0.72), 45),
        "side_with_table": ((2.6, -0.45, 1.05), (0.0, -0.35, 0.70), 42),
        "rear_guide_handle": ((-1.75, 1.85, 1.30), (-0.05, 0.0, 0.70), 45),
        "face_closeup": ((0.45, -1.05, 1.30), (0.0, -0.05, 1.08), 55),
    }
    for name, (loc, tgt, lens) in views.items():
        sc.camera = camera(name, loc, tgt, lens)
        sc.render.filepath = os.path.join(OUT, f"{name}.png")
        bpy.ops.render.render(write_still=True)
        print("wrote", sc.render.filepath)


if __name__ == "__main__":
    build()
    if bpy.app.background or not getattr(bpy.context, "window", None):
        render_views()
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "concept_robot.blend"))
