"""
Cozy Campfire Effect
====================
Warm flickering flames rising from the bottom, glowing embers drifting up,
and a soft ambient warmth radiating outward. Evokes sitting by a fire on
a cool evening.
"""

import math
import random
from _runner import EffectRunner, lerp, hex_color

FPS = 8
EFFECT_NAME = "Cozy Campfire"

# Palette: deep ember → orange flame → golden tip
EMBER = (80, 10, 0)
FLAME_CORE = (255, 80, 0)
FLAME_MID = (255, 140, 20)
FLAME_TIP = (255, 200, 50)
WARM_GLOW = (60, 15, 2)

runner = EffectRunner(EFFECT_NAME)

# Pre-generate flicker offsets for organic randomness
_flicker_seeds = [random.uniform(0, 100) for _ in range(200)]


def _noise(seed, t, speed=1.0):
    """Simple pseudo-noise using layered sine waves."""
    v = math.sin(seed * 12.9898 + t * speed * 1.7)
    v += 0.5 * math.sin(seed * 7.233 + t * speed * 3.1)
    v += 0.25 * math.sin(seed * 4.118 + t * speed * 5.3)
    return (v / 1.75) * 0.5 + 0.5  # normalize to 0-1


def render_frame(device, t):
    """Render campfire: flames rise from bottom, embers drift, warm ambient glow."""
    # Lamp/strip devices get a warm flickering glow (simpler spatial layout)
    if getattr(device, 'kind', 'Keyboard') != 'Keyboard':
        colors = {}
        for i, lamp in enumerate(device.lamps):
            seed = _flicker_seeds[i % len(_flicker_seeds)]
            flicker = _noise(seed, t, speed=2.0)
            pulse = _noise(seed + 20, t, speed=1.0)
            # Blend between ember and flame based on flicker
            color = lerp(EMBER, FLAME_CORE, flicker)
            color = lerp(color, FLAME_TIP, pulse * 0.3)
            colors[str(lamp['idx'])] = hex_color(
                int(min(255, color[0])),
                int(min(255, color[1])),
                int(min(255, color[2]))
            )
        return colors

    # Keyboard gets the full spatial campfire effect
    colors = {}

    for i, lamp in enumerate(device.lamps):
        x, y = lamp['x'], lamp['y']
        seed = _flicker_seeds[i % len(_flicker_seeds)]

        # Fire height: flames are strongest at the bottom (y=1) and fade toward top (y=0)
        # Invert y so bottom of device = fire base
        fire_y = 1.0 - y

        # Flickering intensity — varies per lamp over time
        flicker = _noise(seed, t, speed=2.5)
        flicker2 = _noise(seed + 50, t, speed=1.8)

        # Horizontal proximity to center (fire is centered)
        center_dist = abs(x - 0.5) * 2.0  # 0 at center, 1 at edges

        # Flame shape: tall and narrow, tapering upward
        flame_width = 0.3 + 0.7 * fire_y  # wider at base
        flame_intensity = max(0, 1.0 - center_dist / flame_width)
        flame_intensity *= fire_y  # stronger at base
        flame_intensity *= (0.6 + 0.4 * flicker)  # flicker modulation

        # Ember sparks: occasional bright spots that drift upward
        ember_phase = _noise(seed * 3.7, t * 0.5 + y * 2.0, speed=1.2)
        ember_spark = max(0, ember_phase - 0.7) * 3.3  # sparse bright sparks
        ember_spark *= (1.0 - fire_y) * 0.6  # embers mostly in upper area

        # Color blending based on flame height
        if flame_intensity > 0.7:
            # Hot core — bright orange/yellow
            blend = (flame_intensity - 0.7) / 0.3
            color = lerp(FLAME_MID, FLAME_TIP, blend * flicker2)
        elif flame_intensity > 0.3:
            # Mid flame — orange
            blend = (flame_intensity - 0.3) / 0.4
            color = lerp(FLAME_CORE, FLAME_MID, blend)
        elif flame_intensity > 0.05:
            # Outer flame — deep red/ember
            blend = flame_intensity / 0.3
            color = lerp(EMBER, FLAME_CORE, blend)
        else:
            # Ambient warm glow
            glow_strength = max(0, 0.3 - center_dist * 0.3) * (0.5 + 0.5 * fire_y)
            glow_strength *= (0.7 + 0.3 * flicker2)
            color = lerp((0, 0, 0), WARM_GLOW, min(1, glow_strength))

        # Add ember sparks on top
        if ember_spark > 0:
            color = lerp(color, FLAME_TIP, min(1, ember_spark))

        colors[str(lamp['idx'])] = hex_color(
            int(min(255, color[0])),
            int(min(255, color[1])),
            int(min(255, color[2]))
        )

    return colors


def render_frame_lamp_only(device, t):
    """Only render on the lamp/scene device, leave keyboard dark."""
    if device.kind != "Scene":
        return {str(lamp['idx']): '#000000' for lamp in device.lamps}
    return render_frame(device, t)


if __name__ == '__main__':
    import sys
    lamp_only = '--lamp' in sys.argv
    runner.run(render_frame_lamp_only if lamp_only else render_frame, fps=FPS)
