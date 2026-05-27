import math
import random
from _runner import EffectRunner, lerp, hex_color

runner = EffectRunner("Zen Coding")

# Calm teal palette inspired by Quiet Current theme
DEEP = (8, 28, 32)
TEAL = (12, 118, 123)
SOFT_TEAL = (30, 90, 95)
MIST = (60, 140, 145)
DARK = (4, 14, 18)

# Slow ripple seeds
NUM_RIPPLES = 5
ripple_cx = [random.uniform(0.1, 0.9) for _ in range(NUM_RIPPLES)]
ripple_cy = [random.uniform(0.2, 0.8) for _ in range(NUM_RIPPLES)]
ripple_phase = [random.uniform(0, math.tau) for _ in range(NUM_RIPPLES)]
ripple_period = [random.uniform(6.0, 12.0) for _ in range(NUM_RIPPLES)]


def render_frame(device, t):
    colors = {}
    for lamp in device.lamps:
        lx, ly = lamp["x"], lamp["y"]

        # Base: gentle horizontal current flowing left to right
        flow = math.sin(lx * 3.0 - t * 0.3 + ly * 1.5) * 0.5 + 0.5
        base = lerp(DEEP, SOFT_TEAL, flow * 0.45)

        # Slow breathing brightness (inhale / exhale)
        breath = math.sin(t * 0.4) * 0.5 + 0.5
        base = lerp(base, TEAL, breath * 0.15)

        # Gentle ripples that fade in and out
        for i in range(NUM_RIPPLES):
            # Each ripple appears, expands, and fades on its own cycle
            cycle = (t + ripple_phase[i]) / ripple_period[i]
            life = (cycle % 1.0)  # 0 to 1 within each cycle
            if life < 0.6:
                radius = life * 0.5
                fade = 1.0 - (life / 0.6)  # fades as it expands
                dx = lx - ripple_cx[i]
                dy = ly - ripple_cy[i]
                dist = math.sqrt(dx * dx + dy * dy)
                ring = abs(dist - radius)
                if ring < 0.06:
                    ring_intensity = (1.0 - ring / 0.06) * fade * 0.35
                    base = lerp(base, MIST, ring_intensity)

        # Subtle darkening at edges for vignette / focus effect
        edge_x = 1.0 - 2.0 * abs(lx - 0.5)
        edge_y = 1.0 - 2.0 * abs(ly - 0.5)
        vignette = edge_x * edge_y
        vignette = max(0.0, min(1.0, vignette))
        base = lerp(DARK, base, 0.5 + vignette * 0.5)

        colors[str(lamp["idx"])] = hex_color(*base)
    return colors


runner.run(render_frame, fps=8)
