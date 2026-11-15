"""Sideways load-cell mount + drop-in portafilter cradle for smart-grind-by-weight (Eureka Mignon Specialita).
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
PF_R                   = 36.5               # seat pocket radius: fits heads up to 72-73 mm OD
BASKET_GAP             = 61.5               # throat of the funnel (basket / bowl / spouts pass through)
LEDGE_Z                = -105.0             # cradle top is 1 mm above this; raise or lower the whole seat here
HEAD_H                 = 23.0               # reference portafilter only (not used by the printed parts)
M3_CLEAR, M3_CBORE     = 3.4, 6.5
CORNER_R               = 6.0                # plan-view corner radius of the load cell box
FOOT_CHAMFER           = 0.6                # bed-side edge break

# derived layout of the sideways cell
TRAY_Z0   = SEAT_Z0                 # tray bottom flush with stub bottom (prints flat)
FLOOR_T   = 4.0
PAD_T     = 1.0                     # fixed end sits on a 1 mm pad -> 1 mm overload gap under the free end
CELL_Z0   = TRAY_Z0 + FLOOR_T + PAD_T          # -185
CELL_Z1   = CELL_Z0 + CELL_H                   # -163
TRAY_Y1   = -92.5                   # rear face of tray (1.5 mm in front of the stock cover)
WALL      = 2.5
SIDE_GAP  = 1.5
CELL_Y1   = TRAY_Y1 - WALL - SIDE_GAP          # -97
CELL_Y0   = CELL_Y1 - CELL_W                   # -112
CELL_YC   = (CELL_Y0 + CELL_Y1) / 2            # -104.5
TRAY_Y0   = CELL_Y0 - SIDE_GAP - WALL          # -116.5
TRAY_XI, TRAY_XO = 38.0, 40.5
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

# ---- shared outline ---------------------------------------------------------------------------
BAR_T    = 6.0
BAR_Z0, BAR_Z1 = CELL_Z1, CELL_Z1 + BAR_T        # lid: -163 .. -153
OUT_R    = TRAY_XO                                # 43: cradle is as wide as the load cell box
SHELL_T  = 3.0                                    # wall thickness
SEAT_R   = PF_R                                   # 36.5: pocket radius (heads up to 72-73 mm)
THROAT_R = BASKET_GAP / 2                         # 30.75: basket / bowl / spouts pass through
TOP_Z    = LEDGE_Z + 1.0                          # top face of the cradle
POCKET_D = 3.0                                    # straight wall above the funnel
ROOF_Z   = TOP_Z - 22.0                           # underside starts closing in here, at 45 degrees
FRONT_Y  = PF_Y - 32.0                            # cradle is cut flat here (front support line)
NECK_W, WINDOW_W = 26.0, 56.0                     # handle slot at the top, open front below it
NECK_D   = 14.0                                   # depth of the handle slot

def disc(r, z0, z1):
    return cq.Workplane("XY").circle(r).extrude(z1 - z0).translate((0, PF_Y, z0))

def cradle_outline(z0, z1, r, y_rear):
    """Plan shape: straight sides at the back, round at the front (a U), as a solid from z0 to z1."""
    back = box(-r, r, PF_Y, y_rear, z0, z1)
    front = disc(r, z0, z1).intersect(box(-r-1, r+1, PF_Y-r-1, PF_Y+0.01, z0-1, z1+1))
    return front.union(back)


# ---- part A: cross mount (stub that takes the cell's place in the stock seat + tray) -------------
def cross_mount():
    stub = box(-CELL_W/2, CELL_W/2, TRAY_Y1-0.5, SEAT_Y0, SEAT_Z0, SEAT_Z0+CELL_H)
    # same U-shaped footprint as the cradle above it, so the two read as one body with a 2 mm shadow line
    tray = cradle_outline(TRAY_Z0, TRAY_Z1, OUT_R, TRAY_Y1)
    tray = tray.edges(cq.selectors.BoxSelector((-OUT_R-1, TRAY_Y1-0.5, TRAY_Z0-1), (OUT_R+1, TRAY_Y1+0.5, TRAY_Z1+1))).edges('|Z').fillet(CORNER_R)
    tray = tray.cut(box(-OUT_R-1, OUT_R+1, PF_Y-OUT_R-1, FRONT_Y, TRAY_Z0-1, TRAY_Z1+1))
    # the part in front of the load cell is only a shell: open top and bottom
    front = cradle_outline(TRAY_Z0-1, TRAY_Z1+1, OUT_R-WALL, TRAY_Y0).cut(box(-OUT_R, OUT_R, PF_Y-OUT_R-1, FRONT_Y+WALL, TRAY_Z0-2, TRAY_Z1+2))
    tray = tray.cut(front).faces('<Z').edges().chamfer(FOOT_CHAMFER)
    cav  = box(-TRAY_XI, TRAY_XI, TRAY_Y0+WALL, TRAY_Y1-WALL, TRAY_Z0+FLOOR_T, TRAY_Z1+1).edges('|Z').fillet(CORNER_R-WALL)
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

# ---- part B: cradle (lid bolted to the free end + two curved walls + funnel seat) -----------------
# The portafilter drops in from above and rests on a 45-degree funnel, so it self-centres at whatever
# height its body is 61.5-73 mm wide. Nothing touches the rim, so head height does not matter, and
# the ears sit above the cradle at any angle.
def cradle():
    yr = TRAY_Y1
    body = cradle_outline(BAR_Z0, TOP_Z, OUT_R, yr)
    body = body.edges(cq.selectors.BoxSelector((-OUT_R-1, yr-0.5, BAR_Z0-1), (OUT_R+1, yr+0.5, TOP_Z+1))).edges("|Z").fillet(CORNER_R)
    # hollow inside the walls, open to the rear, closing in at 45 degrees under the seat
    ri = OUT_R - SHELL_T
    hollow = cradle_outline(BAR_Z1, ROOF_Z, ri, yr + 20)
    cone = cq.Workplane("XZ").polyline([(0, ROOF_Z), (ri, ROOF_Z), (0, ROOF_Z + ri)]).close().revolve(360, (0, 0, 0), (0, 1, 0)).translate((0, PF_Y, 0))
    ridge = prism_xz([(-ri, ROOF_Z), (ri, ROOF_Z), (0, ROOF_Z + ri)], PF_Y, yr + 20)
    body = body.cut(hollow).cut(cone).cut(ridge)
    # funnel seat: throat, 45-degree cone, short straight pocket
    cz = TOP_Z - POCKET_D
    seat = [(0, BAR_Z1), (THROAT_R, BAR_Z1), (THROAT_R, cz - (SEAT_R - THROAT_R)), (SEAT_R, cz), (SEAT_R, TOP_Z + 1), (0, TOP_Z + 1)]
    body = body.cut(cq.Workplane("XZ").polyline(seat).close().revolve(360, (0, 0, 0), (0, 1, 0)).translate((0, PF_Y, 0)))
    # flat front, handle slot, and an open front that narrows at 45 degrees up to the slot
    body = body.cut(box(-OUT_R-1, OUT_R+1, PF_Y - OUT_R - 1, FRONT_Y, BAR_Z0 - 1, TOP_Z + 1))
    zs = TOP_Z - NECK_D
    za = zs - (WINDOW_W - NECK_W) / 2
    opening = [(-WINDOW_W/2, BAR_Z1), (WINDOW_W/2, BAR_Z1), (WINDOW_W/2, za), (NECK_W/2, zs), (NECK_W/2, TOP_Z + 1),
               (-NECK_W/2, TOP_Z + 1), (-NECK_W/2, zs), (-WINDOW_W/2, za)]
    body = body.cut(prism_xz(opening, PF_Y - OUT_R - 1, PF_Y))
    # the floor is one closed plate: lid over the load cell at the back, catch tray for stray grounds in front
    body = body.faces("<Z").edges().chamfer(FOOT_CHAMFER)
    # relief: the lid only touches the cell over the free end
    body = body.cut(box(-TRAY_XI-1, FREE_X-7, TRAY_Y0+WALL, TRAY_Y1-WALL, BAR_Z0-1, BAR_Z0+1.5))
    for dy in (-HOLE_PITCH/2, HOLE_PITCH/2):
        body = body.cut(vcyl(FREE_X, CELL_YC+dy, BAR_Z0-1, BAR_Z1+1, M3_CLEAR))
        body = body.cut(vcyl(FREE_X, CELL_YC+dy, BAR_Z1-(BAR_T-3.0), BAR_Z1+1, M3_CBORE))
    return body

def load_cell():      # reference only
    c = box(-CELL_L/2, CELL_L/2, CELL_Y0, CELL_Y1, CELL_Z0, CELL_Z1)
    for sx in (FIX_X, FREE_X):
        for dy in (-HOLE_PITCH/2, HOLE_PITCH/2):
            c = c.cut(vcyl(sx, CELL_YC+dy, CELL_Z0-1, CELL_Z1+1, 2.5))
    return c

EAR_ANGLE = 0.0
def portafilter():    # reference only: 72 mm head, 23 mm tall, basket below, 2 ears, handle stub
    REST_Z = TOP_Z - POCKET_D - (SEAT_R - 36.0)
    h = cq.Workplane("XY").circle(36).extrude(HEAD_H).translate((0, PF_Y, REST_Z))
    b = cq.Workplane("XY").circle(30).extrude(14).translate((0, PF_Y, REST_Z-14))
    ears = box(-41, 41, PF_Y-9, PF_Y+9, REST_Z+14, REST_Z+20).rotate((0, PF_Y, 0), (0, PF_Y, 1), EAR_ANGLE)
    handle = box(-11, 11, PF_Y-90, PF_Y-30, REST_Z+2, REST_Z+20)
    return h.union(b).union(ears).union(handle)

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"); os.makedirs(out, exist_ok=True)
    parts = {"cross_mount": cross_mount(), "cradle": cradle(), "ref_load_cell": load_cell(), "ref_portafilter": portafilter()}
    for n, p in parts.items():
        cq.exporters.export(p, f"{out}/{n}.step")
        cq.exporters.export(p, f"{out}/{n}.stl", tolerance=0.02, angularTolerance=0.1)
        bb = p.val().BoundingBox(); print(n, "vol cm3 %.1f" % (p.val().Volume()/1000), "solids", len(p.solids().vals()),
              "bbox x %.1f..%.1f y %.1f..%.1f z %.1f..%.1f" % (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax))
