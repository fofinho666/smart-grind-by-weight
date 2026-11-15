# Sideways Load Cell + Portafilter Yoke (Eureka Mignon Specialità)

⚠️ **Experimental: modelled and checked in CAD, not yet test-printed.** ⚠️

[<img src="preview.png" alt="Sideways load cell mount with portafilter yoke" width="70%">](preview.png)

## Overview

An alternative to the cup holder for grinding straight into a 58mm portafilter. The load cell is turned 90° so it lies across the grinder, hidden in a closed box under the portafilter, instead of pointing forward out of the front.

- The box ends 53 mm in front of the grinder face (the stock load cell reaches 83 mm) and stays inside the portafilter's footprint.
- The stock **back plate, cover and screen adapter are unchanged**. Nothing is reprinted and the mod is reversible.
- The stock cup holder and its hole cover are not used.

## Parts

| Part | Files | Description |
|------|-------|-------------|
| **Cross mount** | [STL](Cross%20mount.stl) / [STEP](Cross%20mount.step) | Stub that bolts into the stock load cell seat, plus a tray that holds the load cell sideways |
| **Portafilter yoke** | [STL](Portafilter%20yoke.stl) / [STEP](Portafilter%20yoke.step) | Lid over the load cell, two side plates, prongs the portafilter slides onto, and two rear hold-down lips that stop the handle weight tipping it |

`model.py` is the parametric [CadQuery](https://github.com/CadQuery/cadquery) source for both parts. All dimensions are parameters at the top of the file.

## Hardware

- T70 load cell, 1 kg (70 × 15 × 22 mm, M3 hole pairs 7 mm apart, 6 mm from each end)
- 4× M3 × 10 mm screws (2 fixed end, 2 free end)
- 2× M3 nuts (captive in the stub)
- The 2 stock seat screws

## Printing

- Print both parts in the STL orientation, flat side down, **no supports**
- 0.2 mm layers, 4 perimeters
- PETG preferred, PLA works

## Assembly

1. Slide two M3 nuts into the slot in the side of the stub.
2. Drop the load cell into the tray with its cable end at the notched corner. Fix it with two M3 × 10 screws from underneath.
3. Push the stub into the stock load cell seat through the cover opening. Fasten it with the two stock seat screws from below into the nuts.
4. Run the cable through the notch into the cover opening to the HX711.
5. Set the yoke on top and fix it with two M3 × 10 screws into the free end of the load cell.
6. Check that the yoke touches nothing but the load cell (2 mm gap all round), then recalibrate (Menu → Calibrate).

## Fit and Limits

- **Portafilter:** heads up to 72 mm wide and 20–26.5 mm tall, with ears at the sides. Shorter heads tilt a few degrees before the lips catch them. A portafilter with an ear opposite the handle does not fit.
- **Weight:** the yoke weighs about 75 g in PETG, so a portafilter over roughly 650 g gets close to the 1 kg load cell limit.
- **Overload:** the tray floor sits 1 mm under the free end of the load cell as a downward stop. There is no upward stop.
- **Dimensions source:** load cell and grinder geometry are taken from the Fusion 360 design in `3d_files/smart-grind-by-weight. Eureka Mignon.f3z`, not measured on hardware. Real clearances may differ by a millimetre or two.

## Adjusting

Edit the parameters in `model.py` and regenerate:

```bash
pip3 install cadquery
python3 model.py   # writes STL and STEP files to ./out
```

Most likely to need tuning for a specific portafilter:

- `LEDGE_Z`: height the portafilter head rests at
- `HEAD_MAX`: height of the hold-down lips above the ledge
- `PF_R`: head radius plus clearance
