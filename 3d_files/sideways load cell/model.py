"""Sideways load-cell mount + portafilter cradle for smart-grind-by-weight (Eureka Mignon Specialita).
Coordinates = the repo's Fusion assembly frame, mm: x across the grinder (0 = centreline),
y front/back (grinder front face at y = -63.25, more negative = toward you), z up.
Stock load cell seat (back plate): cell 70 x 15 x 22, z -190..-168, fixed-end M3 holes at y = -80, x = +-3.5."""
import cadquery as cq, os

# ---- parameters -------------------------------------------------------------
CELL_L, CELL_W, CELL_H = 70.0, 15.0, 22.0   # T70 as modelled in the repo
HOLE_END, HOLE_PITCH   = 6.0, 7.0           # M3 pair: 6 mm from each end, 7 mm apart
SEAT_Y0, SEAT_Z0       = -74.0, -190.0      # stock seat: rear end of cell, underside of cell
SEAT_HOLE_Y            = -80.0
PF_Y                   = -117.0             # basket centre (stock cup centre is -114.5; moved forward so a 72 mm head clears the cover)
PF_R                   = 36.5               # head radius + 0.5 (58 mm portafilter heads are ~70-72 mm OD)
BASKET_GAP             = 61.5               # clear width between prongs (basket / bowl passes through)
LEDGE_Z                = -105.0             # underside of the portafilter head rests here
HEAD_H                 = 23.0               # YOUR portafilter: underside of the head -> top of the rim
LIP_PLAY               = 1.5                # air between the rim and the hold-down bridge
EAR_R                  = 42.5               # nothing may sit inside this radius at ear height (ears reach ~41 mm)
SEAT_D                 = 1.5                # depth of the seat pocket that stops the head sliding forward
M3_CLEAR, M3_CBORE     = 3.4, 6.5
CORNER_R               = 3.0

# derived layout of the sideways cell
TRAY_Z0   = SEAT_Z0                 # tray bottom flush with stub bottom (prints flat)
FLOOR_T   = 4.0
PAD_T     = 1.0                     # fixed end sits on a 1 mm pad -> 1 mm overload gap under the free end
CELL_Z0   = TRAY_Z0 + FLOOR_T + PAD_T          # -185
CELL_Z1   = CELL_Z0 + CELL_H                   # -163
TRAY_Y1   = -92.5                   # rear face of tray (1.5 mm in front of the stock cover)
WALL      = 3.0
SIDE_GAP  = 1.5
CELL_Y1   = TRAY_Y1 - WALL - SIDE_GAP          # -97
CELL_Y0   = CELL_Y1 - CELL_W                   # -112
CELL_YC   = (CELL_Y0 + CELL_Y1) / 2            # -104.5
TRAY_Y0   = CELL_Y0 - SIDE_GAP - WALL          # -116.5
TRAY_XI, TRAY_XO = 40.0, 43.0
TRAY_Z1   = CELL_Z1 - 2.0           # walls stop 2 mm below the yoke (shadow gap, nothing touches)
FIX_X, FREE_X = -(CELL_L/2 - HOLE_END), (CELL_L/2 - HOLE_END)   # -29 / +29

def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1-x0, y1-y0, z1-z0, centered=False).translate((x0, y0, z0))

def vcyl(x, y, z0, z1, d):
    return cq.Workplane("XY").circle(d/2).extrude(z1-z0).translate((x, y, z0))

def prism_xz(pts, y0, y1):          # polygon in (x,z), extruded along y
    return cq.Workplane("XZ").polyline(pts).close().extrude(-(y1-y0)).translate((0, y0, 0))

def prism_yz(pts, x0, x1):          # polygon in (y,z), extruded along x
    return cq.Workplane("YZ").polyline(pts).close().extrude(x1-x0).translate((x0, 0, 0))

# ---- part A: cross mount (stub that takes the cell's place in the stock seat + tray) -------------
def cross_mount():
    stub = box(-CELL_W/2, CELL_W/2, TRAY_Y1-0.5, SEAT_Y0, SEAT_Z0, SEAT_Z0+CELL_H)
    tray = box(-TRAY_XO, TRAY_XO, TRAY_Y0, TRAY_Y1, TRAY_Z0, TRAY_Z1).edges('|Z').fillet(CORNER_R)
    cav  = box(-TRAY_XI, TRAY_XI, TRAY_Y0+WALL, TRAY_Y1-WALL, TRAY_Z0+FLOOR_T, TRAY_Z1+1)
    pad  = box(-TRAY_XI, FIX_X+7, TRAY_Y0+WALL, TRAY_Y1-WALL, TRAY_Z0+FLOOR_T, CELL_Z0)
    a = tray.cut(cav).union(pad).union(stub)
    # fixed-end screws, from below into the cell's threaded holes
    for dy in (-HOLE_PITCH/2, HOLE_PITCH/2):
        a = a.cut(vcyl(FIX_X, CELL_YC+dy, TRAY_Z0-1, CELL_Z0+1, M3_CLEAR))
        a = a.cut(vcyl(FIX_X, CELL_YC+dy, TRAY_Z0-1, TRAY_Z0+2.5, M3_CBORE))
    # stub: stock seat screws come up through the back plate shelf into captive M3 nuts
    for dx in (-HOLE_PITCH/2, HOLE_PITCH/2):
        a = a.cut(vcyl(dx, SEAT_HOLE_Y, SEAT_Z0-1, SEAT_Z0+9, M3_CLEAR))
    a = a.cut(box(-6.9, CELL_W/2+1, SEAT_HOLE_Y-2.95, SEAT_HOLE_Y+2.95, SEAT_Z0+3.0, SEAT_Z0+5.8))
    # cable notch at the fixed-end corner, towards the cover opening
    a = a.cut(box(-TRAY_XI, -TRAY_XI+8, TRAY_Y1-WALL-0.5, TRAY_Y1+1, TRAY_Z1-11, TRAY_Z1+1))
    return a

# ---- part B: yoke (lid bar bolted to the free end + two side plates + prongs + hold-downs) -------
BAR_T = 10.0
BAR_Z0, BAR_Z1 = CELL_Z1, CELL_Z1 + BAR_T        # -163 .. -153
PRONG_XI = BASKET_GAP/2                           # 30.75
PLATE_XI, PLATE_XO = 34.0, 43.0
PRONG_T  = 5.0
PRONG_Y0, PRONG_Y1 = PF_Y - 26.0, PF_Y + 32.5           # front tip / rear end
UP_Y0, UP_Y1 = TRAY_Y0, TRAY_Y0 + 16.0            # upright foot on the bar
LIP_Z0 = LEDGE_Z + HEAD_H + LIP_PLAY              # flat underside of the hold-down bridge
BRIDGE_T = 3.5
POST_TOP = LIP_Z0 + BRIDGE_T
STOP_H = 8.0                                      # rear stop pads stay below ear height
POST_Y0, BRIDGE_Y0, BRIDGE_Y1 = PF_Y + 25.5, PF_Y + 26.5, PF_Y + 30.5

def side_plate():
    zt, zb = LEDGE_Z, LEDGE_Z - PRONG_T
    xz = [(PLATE_XO, BAR_Z1-1), (PLATE_XI, BAR_Z1-1), (PLATE_XI, zb-(PLATE_XI-PRONG_XI)),
          (PRONG_XI, zb), (PRONG_XI, zt), (PLATE_XO, zt)]
    yz = [(UP_Y0, BAR_Z1-1), (UP_Y1, BAR_Z1-1), (UP_Y1, zb-(PRONG_Y1-UP_Y1)), (PRONG_Y1, zb),
          (PRONG_Y1, zt), (PRONG_Y0, zt), (PRONG_Y0, zb), (UP_Y0, zb-(UP_Y0-PRONG_Y0))]
    plate = prism_xz(xz, PRONG_Y0, PRONG_Y1).intersect(prism_yz(yz, 0, PLATE_XO+1))
    # seat pocket: the front half of the prong is SEAT_D higher, with a round pocket the head drops into
    rim = box(PRONG_XI, PLATE_XO, PRONG_Y0, PF_Y, zt, zt+SEAT_D)
    plate = plate.union(rim.cut(cq.Workplane('XY').circle(PF_R).extrude(SEAT_D+2).translate((0, PF_Y, zt-1))))
    # rear post: stands outside the ear radius, so ears can sit at any angle
    post = box(PLATE_XI, PLATE_XO, POST_Y0, PRONG_Y1, LEDGE_Z, POST_TOP)
    # low back-stop pad (below ear height), shaped to the head radius
    px0, py0 = 24.0, PF_Y + 20.5
    pad = box(px0, PLATE_XI+1, py0, PRONG_Y1, LEDGE_Z, LEDGE_Z+STOP_H)
    wedge = prism_xz([(PRONG_XI, zt), (px0, zt), (PRONG_XI, zt-(PRONG_XI-px0))], py0, PRONG_Y1)
    head = cq.Workplane("XY").circle(PF_R).extrude(STOP_H+14).translate((0, PF_Y, LEDGE_Z-12))
    post = post.union(pad.union(wedge).cut(head))
    return plate.union(post)

def yoke():
    bar = box(-TRAY_XO, TRAY_XO, TRAY_Y0, TRAY_Y1, BAR_Z0, BAR_Z1).edges('|Z').fillet(CORNER_R)
    # relief: the bar only touches the cell over the free end
    bar = bar.cut(box(-TRAY_XI-1, FREE_X-7, TRAY_Y0+WALL, TRAY_Y1-WALL, BAR_Z0-1, BAR_Z0+1.5))
    for dy in (-HOLE_PITCH/2, HOLE_PITCH/2):
        bar = bar.cut(vcyl(FREE_X, CELL_YC+dy, BAR_Z0-1, BAR_Z1+1, M3_CLEAR))
        bar = bar.cut(vcyl(FREE_X, CELL_YC+dy, BAR_Z1-5.5, BAR_Z1+1, M3_CBORE))
    sp = side_plate()
    # hold-down bridge: a flat beam above the rear of the rim, joining the two posts
    bridge = box(-PLATE_XO, PLATE_XO, BRIDGE_Y0, BRIDGE_Y1, LIP_Z0, POST_TOP)
    return bar.union(sp).union(sp.mirror("YZ")).union(bridge)

def load_cell():      # reference only
    c = box(-CELL_L/2, CELL_L/2, CELL_Y0, CELL_Y1, CELL_Z0, CELL_Z1)
    for sx in (FIX_X, FREE_X):
        for dy in (-HOLE_PITCH/2, HOLE_PITCH/2):
            c = c.cut(vcyl(sx, CELL_YC+dy, CELL_Z0-1, CELL_Z1+1, 2.5))
    return c

EAR_ANGLE = 0.0
def portafilter():    # reference only: 72 mm head, 23 mm tall, basket below, 2 ears, handle stub
    h = cq.Workplane("XY").circle(36).extrude(HEAD_H).translate((0, PF_Y, LEDGE_Z))
    b = cq.Workplane("XY").circle(30).extrude(14).translate((0, PF_Y, LEDGE_Z-14))
    ears = box(-41, 41, PF_Y-9, PF_Y+9, LEDGE_Z+14, LEDGE_Z+20).rotate((0, PF_Y, 0), (0, PF_Y, 1), EAR_ANGLE)
    handle = box(-11, 11, PF_Y-90, PF_Y-30, LEDGE_Z+2, LEDGE_Z+20)
    return h.union(b).union(ears).union(handle)

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"); os.makedirs(out, exist_ok=True)
    parts = {"cross_mount": cross_mount(), "yoke": yoke(), "ref_load_cell": load_cell(), "ref_portafilter": portafilter()}
    for n, p in parts.items():
        cq.exporters.export(p, f"{out}/{n}.step")
        cq.exporters.export(p, f"{out}/{n}.stl", tolerance=0.02, angularTolerance=0.1)
        bb = p.val().BoundingBox(); print(n, "vol cm3 %.1f" % (p.val().Volume()/1000), "solids", len(p.solids().vals()),
              "bbox x %.1f..%.1f y %.1f..%.1f z %.1f..%.1f" % (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax))
