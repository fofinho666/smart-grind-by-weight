# Sideways Load Cell + Portafilter Cradle (Eureka Mignon Specialità)

⚠️ **Experimental: modelled and checked in CAD, not yet test-printed.** ⚠️

[<img src="preview.png" alt="Sideways load cell mount with portafilter cradle" width="70%">](preview.png)

## Overview

An alternative to the cup holder for grinding straight into a 58mm portafilter. The load cell is turned 90° so it lies across the grinder, hidden in a closed box under the portafilter, instead of pointing forward out of the front. The portafilter drops into a round cradle on top.

- The cross mount and the cradle share the same footprint, so they read as one body with a 2 mm shadow line between them.
- The whole assembly reaches 86 mm in front of the grinder face, about the same as the portafilter head it holds (the stock load cell reaches 83 mm).
- The stock **back plate, cover and screen adapter are unchanged**. Nothing is reprinted and the mod is reversible.
- The stock cup holder and its hole cover are not used.

## Parts

| Part | Files | Description |
|------|-------|-------------|
| **Cross mount** | [STL](Cross%20mount.stl) / [STEP](Cross%20mount.step) | Stub that bolts into the stock load cell seat, plus a tray that holds the load cell sideways. Its front is an open shell that continues the cradle's shape downward |
| **Portafilter cradle** | [STL](Portafilter%20cradle.stl) / [STEP](Portafilter%20cradle.step) | Lid over the load cell with two curved walls and a funnel-shaped seat the portafilter drops into |

`model.py` is the parametric [CadQuery](https://github.com/CadQuery/cadquery) source for both parts. All dimensions are parameters at the top of the file.

## Hardware

- T70 load cell, 1 kg (70 × 15 × 22 mm, M3 hole pairs 7 mm apart, 6 mm from each end)
- 4× M3 × 10 mm screws (2 fixed end, 2 free end)
- 2× M3 nuts (captive in the stub)
- The 2 stock seat screws

## Printing

- Print both parts in the STL orientation, flat side down, **no supports**
- 0.2 mm layers, 4 perimeters, 15–20% infill
- PETG preferred, PLA works

## Assembly

1. Slide two M3 nuts into the slot in the side of the stub.
2. Drop the load cell into the tray with its cable end at the notched corner. Fix it with two M3 × 10 screws from underneath.
3. Push the stub into the stock load cell seat through the cover opening. Fasten it with the two stock seat screws from below into the nuts.
4. Run the cable through the notch into the cover opening to the HX711.
5. Set the cradle on top and fix it with two M3 × 10 screws into the free end of the load cell. The screws sit under the seat, so reach them with an L-shaped hex key through the open front.
6. Check that the cradle touches nothing but the load cell (2 mm gap all round), then recalibrate (Menu → Calibrate).

## How the Portafilter Is Held

- **Funnel seat:** the seat is a 45° funnel with a short straight wall above it. The portafilter drops in from above and centres itself, resting wherever its body is between 61.5 and 73 mm wide. A flat-bottomed head sits near the top of the funnel; a bowl-shaped one sits a little lower.
- **Nothing touches the rim,** so the height of the head does not matter and there is nothing to adjust.
- **Ears sit above the cradle** and can be at any angle.
- **Open front:** the handle passes through a slot at the top, and the front below it is open so spouts are visible and drips fall through.
- **To use:** lower the portafilter in, handle to the front. Lift it out the same way.

## Fit and Limits

- **Portafilter:** any 58mm portafilter with a head up to 72–73 mm wide: spouted or bottomless, any ear layout, any head height.
- **Rear ear:** an ear pointing directly opposite the handle ends up about 1 mm from the stock cover and may touch it.
- **Heavy handles:** the cradle supports the head up to 32 mm in front of the basket centre. A portafilter whose balance point is further forward than that (a very heavy handle on a light head) can tip forward.
- **Weight:** the cradle weighs roughly 50–60 g at 15–20% infill, so a portafilter over roughly 650 g gets close to the 1 kg load cell limit.
- **Basket position:** the basket centre is 2.5 mm further forward than the stock cup holder, so a 72 mm head clears the cover by about 4 mm.
- **Overload:** the tray floor sits 1 mm under the free end of the load cell as a downward stop. There is no upward stop.
- **Dimensions source:** load cell and grinder geometry are taken from the Fusion 360 design in `3d_files/smart-grind-by-weight. Eureka Mignon.f3z`, not measured on hardware. Real clearances may differ by a millimetre or two.

## Adjusting

Edit the parameters in `model.py` and regenerate:

```bash
pip3 install cadquery
python3 model.py   # writes STL and STEP files to ./out
```

Most useful parameters:

- `PF_R`: seat pocket radius (largest head that fits)
- `BASKET_GAP`: funnel throat (what has to pass through below the head)
- `LEDGE_Z`: height of the seat
- `PF_Y`: basket centre, front to back
- `FRONT_Y`: how far forward the cradle supports the head
