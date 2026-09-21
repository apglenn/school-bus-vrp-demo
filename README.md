# School Bus Vehicle Routing Model

A Python-based optimization project using Google OR-Tools to model and solve
Capacitated Vehicle Routing Problems (CVRP) for multi-district school
transportation planning. Compares an **independent baseline** (each district
routes its own fleet in isolation) against a **collaborative model** (districts
share vehicle capacity for overlapping destinations) to quantify potential
savings in distance and vehicle usage.

## Problem

School districts often transport students to the same out-of-district
destinations independently, resulting in duplicated routes and underused
buses. This project models both the status-quo (independent) and a
coordinated (collaborative) approach, and measures the difference.

## Features
- Multi-depot CVRP with per-district garages and vehicle fleets
- Time window and vehicle capacity constraints
- District-restricted routing (independent baseline) vs. unrestricted
  routing (collaborative), via `SetAllowedVehiclesForIndex`
- Automated comparison script (`comparison.py`) reporting total distance
  savings and vehicle usage between scenarios
- Interactive map visualization per scenario using Folium

## How to Run

**Requires Python 3.12** (see Known Issues below).

1. Clone this repository.
2. Create and activate a virtual environment using Python 3.12:
   - macOS/Linux/WSL:
     python3.12 -m venv myenv
     source myenv/bin/activate
   - Windows (PowerShell):
     py -3.12 -m venv myenv
     myenv\Scripts\Activate.p
4. Install Dependencies: pip install "ortools==9.11.4210" pandas numpy folium requests
5. Run a single scenario: python main.py  (toggle the `collaborative` flag at the bottom of `main.py`)
6. Run the full comparison (both scenarios, generates both maps and `output.txt` with savings summary): python comparison.py



## Known Issues / Environment Notes

- **Python version:** OR-Tools 9.11.4210 (pinned below) does not currently
  publish wheels for Python 3.13+. If your system's default `python3` has
  moved past 3.12, install 3.12 explicitly and build the virtual environment
  with that interpreter specifically (`python3.12 -m venv myenv`).
- **OR-Tools version pin:** This project requires `ortools==9.11.4210`.
  OR-Tools >=9.15 has a confirmed regression in the Python bindings for
  `SetAllowedVehiclesForIndex` (raises a `TypeError` on `absl::Span<const int>`
  conversion even with correctly-typed native Python int lists — verified via
  isolated reproduction across multiple OR-Tools versions).
- **Virtual environment activation (WSL specifically):** If developing on
  WSL with your project on a Windows-mounted drive (`/mnt/c/...`), always
  `cd` into the project directory *before* activating `myenv` — activating
  from another location can silently pick up an unrelated environment of
  the same name. Verify with `which python3` and `pip show ortools` before
  running anything. This is a WSL/DrvFs-specific quirk and shouldn't affect
  native Linux, macOS, or Windows-only setups.
- **Road-network distances (OSRM):** An initial integration using OSRM for
  real driving-distance/time matrices was implemented and validated correctly
  in isolated testing, but exhibited an intermittent failure in the full
  pipeline that wasn't resolved before this version was finalized. The
  current version uses a Euclidean-distance approximation instead. See the
  `osrm-attempt` branch for the in-progress implementation.

## Planned Extensions
- Real road-network distances via OSRM (see Known Issues)
- Drop-off destinations (schools) distinct from garages
- Per-district demand splitting at shared destinations
- Disjunctions (allow dropping an unservable stop with a penalty, rather
  than failing the entire solve)
- Vehicle fixed-cost in the objective (optimize for fleet size, not just
  distance)
- Synthetic data generator for testing at multiple district counts/scales


