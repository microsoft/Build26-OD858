"""
Cyberpunk Rain — neon digital rain columns with electric glitch bursts.

Hot pink and cyan rain streaks fall down the keyboard like a neon city
in the rain. Random glitch flashes pulse across rows in electric purple.
"""

import math, random
from _runner import EffectRunner, lerp, hex_color

runner = EffectRunner("Cyberpunk Rain")

# Neon palette
NEON_PINK = (227, 0, 140)
CYAN = (0, 255, 255)
PURPLE = (68, 0, 255)
MAGENTA = (255, 0, 255)
DARK_BG = (5, 0, 15)
DEEP_PINK = (80, 0, 50)

# Rain columns — each has a position, speed, color, and head position
NUM_COLUMNS = 8
rain_columns = []
for i in range(NUM_COLUMNS):
    rain_columns.append({
        "x": random.random(),
        "head_y": random.uniform(-0.5, 0.0),
        "speed": random.uniform(0.4, 0.9),
        "color": random.choice([NEON_PINK, CYAN, MAGENTA]),
        "width": random.uniform(0.04, 0.08),
        "trail_len": random.uniform(0.3, 0.6),
    })

# Glitch state
glitch_time = 0
glitch_row = -1
glitch_color = PURPLE
glitch_duration = 0.15

def reset_column(col):
    col["x"] = random.random()
    col["head_y"] = random.uniform(-0.3, -0.1)
    col["speed"] = random.uniform(0.4, 0.9)
    col["color"] = random.choice([NEON_PINK, CYAN, MAGENTA])
    col["width"] = random.uniform(0.04, 0.08)
    col["trail_len"] = random.uniform(0.3, 0.6)

def render_frame(device, t):
    global glitch_time, glitch_row, glitch_color, glitch_duration

    colors = {}

    # Update rain columns
    for col in rain_columns:
        col["head_y"] += col["speed"] * 0.125  # per frame at 8fps
        if col["head_y"] > 1.0 + col["trail_len"]:
            reset_column(col)

    # Trigger random glitch
    if random.random() < 0.03:
        glitch_time = t
        glitch_row = random.randint(0, 6)
        glitch_color = random.choice([PURPLE, CYAN, NEON_PINK])
        glitch_duration = random.uniform(0.1, 0.25)

    for lamp in device.lamps:
        lx, ly = lamp["x"], lamp["y"]

        # Base: dark purple-black with subtle shimmer
        shimmer = math.sin(lx * 12 + t * 1.5) * 0.1 + 0.1
        base = lerp(DARK_BG, DEEP_PINK, shimmer)

        # Layer rain columns
        rain_brightness = 0
        rain_color = CYAN
        for col in rain_columns:
            dx = abs(lx - col["x"])
            if dx < col["width"]:
                # How far behind the head?
                dy = col["head_y"] - ly
                if 0 <= dy <= col["trail_len"]:
                    # Brightest at head, fading along trail
                    intensity = 1.0 - (dy / col["trail_len"])
                    # Sharper at center of column
                    center_factor = 1.0 - (dx / col["width"])
                    brightness = intensity * center_factor
                    if brightness > rain_brightness:
                        rain_brightness = brightness
                        rain_color = col["color"]

        if rain_brightness > 0:
            pixel = lerp(base, rain_color, rain_brightness ** 0.7)
        else:
            pixel = base

        # Glitch flash overlay
        lamp_row = int(round(lamp['y'] * 6))
        if (t - glitch_time) < glitch_duration and lamp_row == glitch_row:
            flash_intensity = 1.0 - ((t - glitch_time) / glitch_duration)
            # Glitch flicker
            if random.random() < 0.7:
                pixel = lerp(pixel, glitch_color, flash_intensity * 0.9)

        colors[str(lamp['idx'])] = hex_color(*pixel)

    return colors

runner.run(render_frame, fps=8)
