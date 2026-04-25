import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Enable cache to avoid re-downloading data
fastf1.Cache.enable_cache('cache')

# ── Load Session ──────────────────────────────────────────────
# 2024 British Grand Prix - Race
session = fastf1.get_session(2024, 'British Grand Prix', 'R')
session.load()

print("Session loaded:", session.event['EventName'], session.name)

# ── Plot 1: Lap Time Progression (Top 3 Drivers) ─────────────
fastf1.plotting.setup_mpl()

fig, ax = plt.subplots(figsize=(12, 6))

drivers = ['VER', 'HAM', 'NOR']
colors  = ['#3671C6', '#00D2BE', '#FF8000']

for driver, color in zip(drivers, colors):
    laps = session.laps.pick_driver(driver).pick_quicklaps()
    ax.plot(
        laps['LapNumber'],
        laps['LapTime'].dt.total_seconds(),
        label=driver,
        color=color,
        linewidth=2
    )

ax.set_title('Lap Time Progression — 2024 British Grand Prix', fontsize=14, fontweight='bold')
ax.set_xlabel('Lap Number')
ax.set_ylabel('Lap Time (seconds)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('lap_times.png', dpi=150)
plt.show()
print("Plot 1 saved: lap_times.png")

# ── Plot 2: Fastest Lap Speed Trace Comparison ───────────────
fig, ax = plt.subplots(figsize=(12, 6))

for driver, color in zip(drivers, colors):
    fastest = session.laps.pick_driver(driver).pick_fastest()
    telemetry = fastest.get_telemetry()
    ax.plot(
        telemetry['Distance'],
        telemetry['Speed'],
        label=driver,
        color=color,
        linewidth=1.5
    )

ax.set_title('Speed Trace — Fastest Lap Comparison — 2024 British GP', fontsize=14, fontweight='bold')
ax.set_xlabel('Distance (m)')
ax.set_ylabel('Speed (km/h)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('speed_trace.png', dpi=150)
plt.show()
print("Plot 2 saved: speed_trace.png")

# ── Plot 3: Tyre Strategy ─────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 6))

for i, driver in enumerate(drivers):
    laps = session.laps.pick_driver(driver)
    for _, lap in laps.iterlaps():
        compound = lap['Compound']
        color = fastf1.plotting.get_compound_color(compound, session)
        ax.barh(
            driver,
            1,
            left=lap['LapNumber'] - 1,
            color=color,
            edgecolor='none',
            height=0.4
        )

ax.set_title('Tyre Strategy — 2024 British Grand Prix', fontsize=14, fontweight='bold')
ax.set_xlabel('Lap Number')
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('tyre_strategy.png', dpi=150)
plt.show()
print("Plot 3 saved: tyre_strategy.png")

print("\nAll done. Check your folder for the 3 PNG files.")