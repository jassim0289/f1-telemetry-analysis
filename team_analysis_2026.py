import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── SETUP ────────────────────────────────────────────────────────────────────
fastf1.Cache.enable_cache("cache")

TEAMS = {
    "Mercedes": {"drivers": ["ANT", "RUS"], "color": "#00D2BE"},
    "Ferrari":  {"drivers": ["LEC", "HAM"], "color": "#DC0000"},
    "McLaren":  {"drivers": ["NOR", "PIA"], "color": "#FF8000"},
}

DRIVER_NAMES = {
    "ANT": "Antonelli", "RUS": "Russell",
    "LEC": "Leclerc",   "HAM": "Hamilton",
    "NOR": "Norris",    "PIA": "Piastri",
}

RACES = ["Australian Grand Prix", "Chinese Grand Prix", "Japanese Grand Prix"]
RACE_LABELS = ["Australia", "China", "Japan"]

all_drivers = [d for t in TEAMS.values() for d in t["drivers"]]

# ── LOAD ALL 3 SESSIONS ───────────────────────────────────────────────────────
print("Loading 3 race sessions — this may take a minute...")
sessions = {}
for race in RACES:
    print(f"  Loading {race}...")
    s = fastf1.get_session(2026, race, "R")
    s.load()
    sessions[race] = s
print("All sessions loaded.\n")

# ── CHART 1: AVERAGE RACE PACE PER TEAM PER RACE ────────────────────────────
fig, ax = plt.subplots(figsize=(13, 6))

x = np.arange(len(RACES))
width = 0.25
offsets = [-width, 0, width]

for i, (team, info) in enumerate(TEAMS.items()):
    team_avg = []
    for race in RACES:
        s = sessions[race]
        laps = s.laps.pick_drivers(info["drivers"]).pick_quicklaps()
        avg = laps["LapTime"].dt.total_seconds().mean()
        team_avg.append(avg)
    bars = ax.bar(x + offsets[i], team_avg, width - 0.02,
                  label=team, color=info["color"], edgecolor="black", linewidth=0.5)
    for bar, val in zip(bars, team_avg):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                f"{val:.1f}s", ha="center", va="bottom", fontsize=8)

ax.set_title("2026 F1 Season — Average Race Pace by Team\nAustralia · China · Japan", fontsize=13)
ax.set_ylabel("Average Lap Time (seconds)", fontsize=11)
ax.set_xticks(x)
ax.set_xticklabels(RACE_LABELS, fontsize=11)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig("team_avg_pace_2026.png", dpi=150)
plt.show()
print("Chart 1 saved.")

# ── CHART 2: FASTEST LAP PER DRIVER ACROSS 3 RACES ──────────────────────────
fig, ax = plt.subplots(figsize=(13, 6))

driver_colors = {
    "ANT": "#00D2BE", "RUS": "#00A693",
    "LEC": "#DC0000", "HAM": "#A50000",
    "NOR": "#FF8000", "PIA": "#CC6600",
}

x = np.arange(len(RACES))
width = 1 / (len(all_drivers) + 1)
offsets = np.linspace(-0.4, 0.4, len(all_drivers))

for i, driver in enumerate(all_drivers):
    fastest_times = []
    for race in RACES:
        try:
            fastest = sessions[race].laps.pick_drivers(driver).pick_fastest()
            fastest_times.append(fastest["LapTime"].total_seconds())
        except Exception:
            fastest_times.append(np.nan)
    ax.plot(RACE_LABELS, fastest_times, marker="o", linewidth=2,
            label=DRIVER_NAMES[driver], color=driver_colors[driver], markersize=7)

ax.set_title("2026 F1 Season — Fastest Lap Per Driver\nAustralia · China · Japan", fontsize=13)
ax.set_ylabel("Fastest Lap Time (seconds)", fontsize=11)
ax.legend(fontsize=9, ncol=2)
plt.tight_layout()
plt.savefig("driver_fastest_laps_2026.png", dpi=150)
plt.show()
print("Chart 2 saved.")

# ── CHART 3: TYRE STRATEGY — JAPANESE GP ALL 6 DRIVERS ──────────────────────
compound_colors = {
    "SOFT": "#E8002D", "MEDIUM": "#FFF200",
    "HARD": "#CCCCCC", "INTERMEDIATE": "#39B54A", "WET": "#0067FF"
}

fig, ax = plt.subplots(figsize=(12, 5))
japan = sessions["Japanese Grand Prix"]
laps = japan.laps.pick_drivers(all_drivers)

driver_order = list(reversed(all_drivers))
for driver in driver_order:
    driver_laps = laps.pick_drivers([driver]).reset_index()
    for _, lap in driver_laps.iterrows():
        compound = lap["Compound"]
        color = compound_colors.get(compound, "#AAAAAA")
        ax.barh(DRIVER_NAMES[driver], 1, left=lap["LapNumber"] - 1,
                color=color, edgecolor="none", height=0.6)

patches = [mpatches.Patch(color=v, label=k) for k, v in compound_colors.items()
           if k in ["SOFT", "MEDIUM", "HARD"]]
ax.legend(handles=patches, loc="lower right", fontsize=9)
ax.set_xlabel("Lap Number", fontsize=11)
ax.set_title("2026 Japanese Grand Prix — Tyre Strategy\nMercedes · Ferrari · McLaren", fontsize=13)
plt.tight_layout()
plt.savefig("japan_tyre_strategy_teams_2026.png", dpi=150)
plt.show()
print("Chart 3 saved.")

print("\nAll done — 3 charts saved.")