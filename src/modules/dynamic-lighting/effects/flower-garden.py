"""
Flower Garden Effect — blooming flowers sway in a gentle breeze
with butterflies drifting across the keyboard.
"""

import math, random
from _runner import EffectRunner, lerp, hex_color

runner = EffectRunner("Flower Garden")

# === PALETTE ===
GRASS_DARK  = (34, 90, 30)
GRASS_LIGHT = (72, 140, 50)
SOIL        = (60, 40, 20)

# Flower species: (petal color, center color)
FLOWERS = [
    ((220, 50, 80),   (255, 200, 60)),   # red rose / gold center
    ((180, 80, 200),  (255, 255, 180)),   # purple lavender / cream
    ((255, 160, 50),  (180, 60, 20)),     # orange marigold / brown
    ((255, 220, 100), (200, 140, 40)),    # yellow daisy / amber
    ((255, 130, 170), (255, 240, 200)),   # pink peony / cream
    ((100, 160, 255), (255, 255, 200)),   # blue hydrangea / pale
    ((255, 255, 255), (255, 220, 80)),    # white daisy / gold
]

# Scatter flower centers across the keyboard
random.seed(42)
flower_beds = []
for _ in range(14):
    fx = random.uniform(0.05, 0.95)
    fy = random.uniform(0.05, 0.95)
    species = random.choice(FLOWERS)
    bloom_phase = random.uniform(0, math.pi * 2)
    size = random.uniform(0.06, 0.12)
    flower_beds.append((fx, fy, species, bloom_phase, size))

# Butterfly paths
butterflies = []
for _ in range(3):
    bx_off = random.uniform(0.0, 1.0)
    by_off = random.uniform(0.2, 0.8)
    speed = random.uniform(0.3, 0.6)
    color = random.choice([(255, 180, 40), (100, 200, 255), (255, 100, 200)])
    butterflies.append((bx_off, by_off, speed, color))


def render_frame(device, t):
    colors = {}
    for lamp in device.lamps:
        lx, ly = lamp['x'], lamp['y']

        # Grass base with wind sway
        wind = math.sin(lx * 5 + t * 0.8) * 0.15 + math.sin(lx * 11 + t * 1.3) * 0.08
        grass_blend = (math.sin(lx * 7 + ly * 5 + t * 0.4) * 0.5 + 0.5) + wind
        grass_blend = max(0, min(1, grass_blend))
        color = lerp(GRASS_DARK, GRASS_LIGHT, grass_blend)

        # Bottom row = soil
        if ly > 0.85:
            soil_blend = (ly - 0.85) / 0.15
            color = lerp(color, SOIL, soil_blend * 0.6)

        # Flowers
        for fx, fy, (petal, center), bloom_phase, size in flower_beds:
            dx = lx - fx
            dy = ly - fy
            dist = math.sqrt(dx * dx + dy * dy)

            # Bloom animation: flowers open and close gently
            bloom = (math.sin(t * 0.5 + bloom_phase) * 0.3 + 0.7)
            effective_size = size * bloom

            if dist < effective_size:
                # Center of flower
                if dist < effective_size * 0.3:
                    color = center
                else:
                    # Petals with slight radial gradient
                    petal_fade = (dist - effective_size * 0.3) / (effective_size * 0.7)
                    color = lerp(petal, color, petal_fade * 0.4)

        # Butterflies
        for bx_off, by_off, speed, bcolor in butterflies:
            bx = (bx_off + t * speed * 0.15) % 1.2 - 0.1
            by = by_off + math.sin(t * speed * 2 + bx_off * 5) * 0.12
            # Wing flutter
            flutter = abs(math.sin(t * 8 + bx_off * 3))
            bw = 0.04 * (0.5 + flutter * 0.5)
            bh = 0.06 * flutter

            dx = abs(lx - bx)
            dy = abs(ly - by)
            if dx < bw and dy < bh:
                intensity = 1.0 - max(dx / bw, dy / bh)
                color = lerp(color, bcolor, intensity * 0.9)

        # Sunlight dapple across the top
        if ly < 0.25:
            sun = math.sin(lx * 9 + t * 0.7) * math.cos(ly * 6 - t * 0.5) * 0.5 + 0.5
            sunlight = (255, 250, 200)
            color = lerp(color, sunlight, sun * 0.2 * (1 - ly / 0.25))

        colors[str(lamp['idx'])] = hex_color(*color)
    return colors

runner.run(render_frame, fps=8)
