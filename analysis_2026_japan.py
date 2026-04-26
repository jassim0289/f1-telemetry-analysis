import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── SESSION SETUP ────────────────────────────────────────────────────────────
fastf1.Cache.enable_cache("cache")
session = fastf1.get_session(2026, "Japanese Grand Prix", "R")
session.load()

drivers = ["ANT", "PIA", "LEC"]
colors  = {"ANT": "#00D2BE", "PIA": "#FF8000", "LEC": "#DC0000"}
names   = {"ANT": "Antonelli", "PIA": "Piastri", "LEC": "Leclerc"}

laps = session.laps.pick_drivers(drivers)

# ── CHART 1: LAP TIME PROGRESSION ───────────────────────────────────────────
plt.figure(figsize=(12, 6))

for driver in drivers:
    driver_laps = laps.pick_drivers([driver]).pick_quicklaps().reset_index()
    plt.plot(
        driver_laps["LapNumber"],
        driver_laps["LapTime"].dt.total_seconds(),
        label=names[driver], color=colors[driver], linewidth=2
    )

plt.title("2026 Japanese Grand Prix — Lap Time Progression\nAntonelli vs Piastri vs Leclerc", fontsize=13)
plt.xlabel("Lap Number", fontsize=11)
plt.ylabel("Lap Time (seconds)", fontsize=11)
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig("japan_2026_lap_times.png", dpi=150)
plt.show()
print("Chart 1 saved.")

# ── CHART 2: FASTEST LAP SPEED TRACE ────────────────────────────────────────
plt.figure(figsize=(13, 5))

for driver in drivers:
    fastest = session.laps.pick_drivers(driver).pick_fastest()
    tel = fastest.get_telemetry()
    plt.plot(tel["Distance"], tel["Speed"],
             label=names[driver], color=colors[driver], linewidth=1.8)

plt.title("2026 Japanese Grand Prix — Fastest Lap Speed Trace\nSuzuka", fontsize=13)
plt.xlabel("Distance (m)", fontsize=11)
plt.ylabel("Speed (km/h)", fontsize=11)
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig("japan_2026_speed_trace.png", dpi=150)
plt.show()
print("Chart 2 saved.")

# ── CHART 3: TYRE STRATEGY ───────────────────────────────────────────────────
compound_colors = {
    "SOFT": "#E8002D", "MEDIUM": "#FFF200",
    "HARD": "#CCCCCC", "INTERMEDIATE": "#39B54A", "WET": "#0067FF"
}

fig, ax = plt.subplots(figsize=(10, 4))

for i, driver in enumerate(drivers):
    driver_laps = laps.pick_drivers([driver]).reset_index()
    for _, lap in driver_laps.iterrows():
        compound = lap["Compound"]
        color = compound_colors.get(compound, "#AAAAAA")
        ax.barh(names[driver], 1, left=lap["LapNumber"] - 1,
                color=color, edgecolor="none", height=0.5)

patches = [mpatches.Patch(color=v, label=k) for k, v in compound_colors.items()]
ax.legend(handles=patches, loc="lower right", fontsize=9)
ax.set_xlabel("Lap Number", fontsize=11)
ax.set_title("2026 Japanese Grand Prix — Tyre Strategy", fontsize=13)
plt.tight_layout()
plt.savefig("japan_2026_tyre_strategy.png", dpi=150)
plt.show()
print("Chart 3 saved.")