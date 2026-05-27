import math
import random
from _runner import EffectRunner, lerp, hex_color

runner = EffectRunner("Tornado")

# Storm palette
DARK_SKY = (15, 15, 30)
STORM_GRAY = (60, 65, 80)
WIND_TEAL = (40, 120, 130)
DEBRIS_TAN = (140, 110, 60)
LIGHTNING = (220, 230, 255)
FUNNEL = (80, 75, 65)

# Pre-computed debris particles
NUM_DEBRIS = 12
debris_radius = [random.uniform(0.15, 0.45) for _ in range(NUM_DEBRIS)]
debris_speed = [random.uniform(2.5, 5.5) for _ in range(NUM_DEBRIS)]
debris_phase = [random.uniform(0, math.tau) for _ in range(NUM_DEBRIS)]
debris_y = [random.uniform(0.1, 0.9) for _ in range(NUM_DEBRIS)]

# Lightning timing
lightning_times = [random.uniform(0, 20) for _ in range(6)]
lightning_cycle = 20.0


def render_frame(device, t):
    colors = {}
    cx, cy = 0.5, 0.5  # tornado center

    # Funnel sways slowly
    cx += 0.08 * math.sin(t * 0.6)
    cy += 0.05 * math.cos(t * 0.45)

    # Check for lightning flash this frame
    flash = 0.0
    cycle_t = t % lightning_cycle
    for lt in lightning_times:
        dt = abs(cycle_t - lt)
        if dt < 0.15:
            flash = max(flash, 1.0 - dt / 0.15)

    for lamp in device.lamps:
        lx, ly = lamp["x"], lamp["y"]
        dx, dy = lx - cx, ly - cy
        dist = math.sqrt(dx * dx + dy * dy) + 1e-6
        angle = math.atan2(dy, dx)

        # Swirling rotation — closer to center spins faster
        spin_speed = 3.0 / (dist * 4.0 + 0.3)
        swirl = math.sin(angle + t * spin_speed) * 0.5 + 0.5

        # Base: dark stormy sky, lighter near funnel
        if dist < 0.12:
            # Eye of the tornado — darkest
            base = lerp(DARK_SKY, FUNNEL, 0.3)
        elif dist < 0.35:
            # Funnel wall — swirling grays and teals
            blend = swirl * 0.7 + 0.15
            base = lerp(STORM_GRAY, WIND_TEAL, blend)
            # Add funnel texture
            funnel_band = math.sin(dist * 25.0 - t * 4.0) * 0.5 + 0.5
            base = lerp(base, FUNNEL, funnel_band * 0.4)
        else:
            # Outer storm clouds
            cloud = math.sin(lx * 6.0 + t * 0.8) * math.cos(ly * 4.0 - t * 0.5)
            cloud = cloud * 0.5 + 0.5
            base = lerp(DARK_SKY, STORM_GRAY, cloud * 0.5)

        # Debris particles orbiting the funnel
        for i in range(NUM_DEBRIS):
            d_angle = t * debris_speed[i] + debris_phase[i]
            d_x = cx + debris_radius[i] * math.cos(d_angle)
            d_y = cy + debris_radius[i] * math.sin(d_angle) * 0.6
            d_dist = math.sqrt((lx - d_x) ** 2 + (ly - d_y) ** 2)
            if d_dist < 0.08:
                intensity = 1.0 - d_dist / 0.08
                base = lerp(base, DEBRIS_TAN, intensity * 0.8)
                break  # one debris hit per lamp is enough

        # Lightning flash overlay
        if flash > 0.05:
            # Brighter at top of keyboard (sky)
            sky_factor = max(0.0, 1.0 - ly * 0.8)
            base = lerp(base, LIGHTNING, flash * sky_factor * 0.7)

        colors[str(lamp["idx"])] = hex_color(*base)
    return colors


runner.run(render_frame, fps=8)
