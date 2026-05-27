"""
Dynamic Lighting Effect Template
=================================
Copy this file to create a new per-lamp lighting effect.

How it works:
1. EffectRunner launches the driver and discovers ALL connected devices
   (keyboards, mice, lamps, mousepads, headsets, light strips)
2. Your `render_frame(device, t)` is called once per device per frame
3. Return a dict of {lamp_index_str: "#rrggbb"} for each lamp on that device
4. Alert flash coordination is handled automatically by the runner

Quick start:
    1. Copy this file: cp _template.py my-effect.py
    2. Edit the EFFECT CONFIG section and render_frame()
    3. Run: python my-effect.py

Each device has:
    device.lamps — list of lamps, each with 'idx', 'x' (0–1), 'y' (0–1)
    device.kind  — 'Keyboard', 'Mouse', 'LampStrip', etc.
    device.is_keyboard, device.is_mouse, device.is_strip, etc.
"""

import math
from _runner import EffectRunner, lerp, hex_color

# =============================================
# === EFFECT CONFIG — edit these values! ===
# =============================================
FPS = 8
EFFECT_NAME = "My Effect"

# Your color palette
COLOR_A = (0, 120, 255)   # primary color
COLOR_B = (255, 255, 255) # accent color

runner = EffectRunner(EFFECT_NAME)


def render_frame(device, t):
    """
    Return a dict of {lamp_index_str: "#rrggbb"} for the current time t (seconds).

    This is where your effect logic goes! Use lamp['x'] and lamp['y']
    for spatial effects, and `t` for animation over time.

    Called once per device per frame — works on keyboards, lamps, mice, etc.
    """
    colors = {}
    for lamp in device.lamps:
        # Example: a simple wave that moves left to right
        wave = math.sin(lamp['x'] * math.pi * 2 - t * 2.0) * 0.5 + 0.5
        color = lerp(COLOR_A, COLOR_B, wave)
        colors[str(lamp['idx'])] = hex_color(*color)
    return colors


runner.run(render_frame, fps=FPS)
