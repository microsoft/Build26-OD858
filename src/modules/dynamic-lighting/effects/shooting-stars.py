import math
from _runner import EffectRunner, lerp, hex_color

runner = EffectRunner("Shooting Stars")

# Night sky colors
BASE = (5, 5, 16)
ACCENT = (136, 204, 255)

def render_frame(device, t):
    """Return {lamp_index_str: '#rrggbb'} for each lamp at time t seconds."""
    star_slots = 6
    tail_length = 0.25
    head_glow = 0.04
    colors = {}

    for lamp in device.lamps:
        lx, ly = lamp['x'], lamp['y']
        best_brightness = 0.0

        for i in range(star_slots):
            h1 = ((i * 73856093) ^ 19349663) & 0x7FFFFFFF
            h2 = ((i * 19349663) ^ 83492791) & 0x7FFFFFFF
            h3 = ((i * 83492791) ^ 73856093) & 0x7FFFFFFF

            star_y = (h1 % 1000) / 1000.0
            period = 2.0 + (h2 % 1000) / 250.0
            speed_var = 0.8 + (h3 % 1000) / 1000.0 * 0.6

            cycle_time = t * speed_var / period
            phase = cycle_time - math.floor(cycle_time)
            star_x = 1.0 + tail_length - phase * (1.0 + tail_length + head_glow)

            dx = lx - star_x
            dy = ly - star_y
            y_proximity = math.exp(-dy * dy / 0.01)

            if y_proximity < 0.05:
                continue

            if -head_glow <= dx <= head_glow:
                head_intensity = 1.0 - abs(dx) / head_glow
                best_brightness = max(best_brightness, head_intensity * y_proximity)
            elif 0 < dx < tail_length:
                tail_intensity = 1.0 - dx / tail_length
                tail_intensity *= tail_intensity
                best_brightness = max(best_brightness, tail_intensity * y_proximity * 0.7)

        if best_brightness < 0.01:
            color = BASE
        else:
            star_r = int(ACCENT[0] + (255 - ACCENT[0]) * best_brightness)
            star_g = int(ACCENT[1] + (255 - ACCENT[1]) * best_brightness)
            star_b = int(ACCENT[2] + (255 - ACCENT[2]) * best_brightness)
            blend = min(best_brightness * 1.5, 1.0)
            r = int(BASE[0] + (star_r - BASE[0]) * blend)
            g = int(BASE[1] + (star_g - BASE[1]) * blend)
            b = int(BASE[2] + (star_b - BASE[2]) * blend)
            color = (min(r, 255), min(g, 255), min(b, 255))

        colors[str(lamp['idx'])] = hex_color(*color)
    return colors

runner.run(render_frame, fps=8)
