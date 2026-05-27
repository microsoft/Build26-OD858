"""
Zen Current — slow teal water currents flowing across the keyboard.

Gentle overlapping sine waves in deep teal and soft green drift left to right,
with occasional soft bright ripples that bloom outward like a pebble in still water.
Designed to be calm and meditative.
"""

import math, random
from _runner import EffectRunner, lerp, hex_color

runner = EffectRunner("Zen Current")

# Palette — deep teal water tones
DEEP_TEAL = (8, 60, 65)
MID_TEAL = (12, 118, 123)
SOFT_GREEN = (60, 140, 120)
BRIGHT_TEAL = (80, 200, 200)
DARK_WATER = (4, 30, 35)

# Ripple state — gentle pebble drops
ripples = []
next_ripple = 2.0  # first ripple after 2 seconds

def render_frame(device, t):
    global next_ripple

    # Spawn a new ripple occasionally
    if t >= next_ripple:
        ripples.append({
            "cx": random.uniform(0.2, 0.8),
            "cy": random.uniform(0.2, 0.8),
            "born": t,
            "speed": random.uniform(0.15, 0.25),
            "max_radius": random.uniform(0.4, 0.7),
        })
        next_ripple = t + random.uniform(3.0, 6.0)

    # Remove expired ripples
    active_ripples = [r for r in ripples if (t - r["born"]) * r["speed"] < r["max_radius"]]
    ripples.clear()
    ripples.extend(active_ripples)

    colors = {}
    for lamp in device.lamps:
        lx, ly = lamp["x"], lamp["y"]

        # Base: slow overlapping sine waves drifting right
        wave1 = math.sin(lx * 4.0 - t * 0.3 + ly * 1.5) * 0.5 + 0.5
        wave2 = math.sin(lx * 2.5 + t * 0.2 + ly * 2.0 + 1.0) * 0.5 + 0.5
        wave3 = math.sin(lx * 6.0 - t * 0.15 - ly * 1.0 + 2.5) * 0.5 + 0.5

        # Blend waves
        blend = (wave1 * 0.5 + wave2 * 0.3 + wave3 * 0.2)

        # Map blend to color gradient: dark water → deep teal → mid teal → soft green
        if blend < 0.33:
            base = lerp(DARK_WATER, DEEP_TEAL, blend / 0.33)
        elif blend < 0.66:
            base = lerp(DEEP_TEAL, MID_TEAL, (blend - 0.33) / 0.33)
        else:
            base = lerp(MID_TEAL, SOFT_GREEN, (blend - 0.66) / 0.34)

        # Overlay ripples
        for rip in ripples:
            dist = math.sqrt((lx - rip["cx"])**2 + (ly - rip["cy"])**2)
            radius = (t - rip["born"]) * rip["speed"]
            ring_dist = abs(dist - radius)
            ring_width = 0.06

            if ring_dist < ring_width:
                # Fade ripple as it expands
                age_factor = 1.0 - (radius / rip["max_radius"])
                ring_intensity = (1.0 - ring_dist / ring_width) * age_factor
                base = lerp(base, BRIGHT_TEAL, ring_intensity * 0.6)

        colors[str(lamp['idx'])] = hex_color(*base)

    return colors

runner.run(render_frame, fps=8)
