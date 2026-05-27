import math
import random
from _runner import EffectRunner, lerp, hex_color

runner = EffectRunner("Aurora Borealis")

# Aurora color palette — greens, teals, purples, and hints of pink
AURORA_COLORS = [
    (0, 200, 80),    # vivid green
    (0, 255, 140),   # bright emerald
    (0, 180, 200),   # teal
    (80, 100, 255),  # blue-violet
    (160, 50, 220),  # purple
    (200, 40, 160),  # magenta-pink
]

# Dark sky base
SKY_DARK = (2, 4, 15)
SKY_MID = (8, 12, 30)

# Pre-generate random offsets for curtain variation per lamp
random.seed(42)
LAMP_SEEDS = [random.random() * 100 for _ in range(256)]


def sample_aurora(t_norm):
    """Sample from the aurora palette at position t_norm (0-1)."""
    t_norm = t_norm % 1.0
    n = len(AURORA_COLORS)
    idx = t_norm * n
    i = int(idx) % n
    j = (i + 1) % n
    frac = idx - int(idx)
    return lerp(AURORA_COLORS[i], AURORA_COLORS[j], frac)


def render_frame(device, t):
    colors = {}
    for lamp in device.lamps:
        x, y = lamp['x'], lamp['y']
        idx = lamp['idx']
        seed = LAMP_SEEDS[idx % len(LAMP_SEEDS)]

        # Aurora curtains — vertical bands that sway horizontally
        # Multiple overlapping sine waves create organic curtain shapes
        curtain1 = math.sin(x * 4.0 + t * 0.3 + seed * 0.5) * 0.5 + 0.5
        curtain2 = math.sin(x * 7.0 - t * 0.5 + seed * 0.3) * 0.5 + 0.5
        curtain3 = math.sin(x * 2.5 + t * 0.15 + 1.5) * 0.5 + 0.5

        # Combine curtains — the aurora is strongest at the top (low y)
        curtain = (curtain1 * 0.5 + curtain2 * 0.3 + curtain3 * 0.2)

        # Aurora fades from top to bottom — strongest at top of keyboard
        vertical_fade = max(0.0, 1.0 - y * 1.3)
        vertical_fade = vertical_fade ** 0.6

        # Shimmer — fast subtle flickering like real aurora
        shimmer = math.sin(t * 5.0 + seed * 20.0 + x * 15.0) * 0.1 + 0.9

        # Color shifts slowly across position and time
        color_phase = (x * 0.4 + t * 0.08 + curtain * 0.3) % 1.0
        aurora_color = sample_aurora(color_phase)

        # Intensity combines curtain shape, vertical position, and shimmer
        intensity = curtain * vertical_fade * shimmer

        # Occasional bright flare — a surge of brightness
        flare = math.sin(t * 0.7 + x * 3.0) * 0.5 + 0.5
        if flare > 0.92:
            intensity = min(1.0, intensity + (flare - 0.92) * 5.0)

        # Blend between dark sky and aurora color
        sky = lerp(SKY_DARK, SKY_MID, y * 0.5)
        r = sky[0] + (aurora_color[0] - sky[0]) * intensity
        g = sky[1] + (aurora_color[1] - sky[1]) * intensity
        b = sky[2] + (aurora_color[2] - sky[2]) * intensity

        # Subtle star twinkle in dark areas
        if intensity < 0.15:
            star = math.sin(t * 3.0 + seed * 50.0) * 0.5 + 0.5
            if star > 0.95:
                sparkle = (star - 0.95) * 20.0 * (1.0 - intensity)
                r = min(255, r + 60 * sparkle)
                g = min(255, g + 60 * sparkle)
                b = min(255, b + 70 * sparkle)

        colors[str(idx)] = hex_color(r, g, b)
    return colors


runner.run(render_frame, fps=8)
