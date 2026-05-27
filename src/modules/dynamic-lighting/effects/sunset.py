"""
Sunset Effect
=============
A warm horizon gradient that slowly shifts through golden hour colors.
Bottom rows glow deep orange/red, middle rows are golden amber,
top rows fade into dusky purple — with gentle shimmer throughout.
"""

import math
import random
from _runner import EffectRunner, lerp, hex_color

runner = EffectRunner("Sunset")

# === EFFECT CONFIG ===
FPS = 8

# Sunset palette (bottom to top)
HORIZON = (255, 60, 20)     # deep red-orange at the horizon
GOLDEN = (255, 160, 30)     # golden amber
PEACH = (255, 120, 80)      # warm peach
DUSK = (120, 50, 140)       # dusky purple
NIGHT = (30, 15, 60)        # deep indigo

random.seed(42)
shimmer_offsets = [random.uniform(0, math.pi * 2) for _ in range(512)]


def sunset_gradient(y, t):
    """Map vertical position to a sunset color, with slow time drift."""
    drift = math.sin(t * 0.15) * 0.08
    y_shifted = max(0.0, min(1.0, y + drift))

    if y_shifted < 0.25:
        return lerp(NIGHT, DUSK, y_shifted / 0.25)
    elif y_shifted < 0.5:
        return lerp(DUSK, PEACH, (y_shifted - 0.25) / 0.25)
    elif y_shifted < 0.75:
        return lerp(PEACH, GOLDEN, (y_shifted - 0.5) / 0.25)
    else:
        return lerp(GOLDEN, HORIZON, (y_shifted - 0.75) / 0.25)


def render_frame(device, t):
    colors = {}
    for lamp in device.lamps:
        base = sunset_gradient(lamp['y'], t)

        # Gentle shimmer: slight brightness fluctuation per lamp
        shimmer = math.sin(t * 1.5 + shimmer_offsets[lamp['idx'] % len(shimmer_offsets)]) * 0.08 + 1.0
        r = min(255, int(base[0] * shimmer))
        g = min(255, int(base[1] * shimmer))
        b = min(255, int(base[2] * shimmer))

        colors[str(lamp['idx'])] = hex_color(r, g, b)
    return colors


runner.run(render_frame, fps=FPS)
