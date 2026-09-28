#!/usr/bin/env python3
"""Minimal CDFV-001 Ref-01B vertical water-exit baseline model.

This is a prescribed-motion hydrostatic benchmark.  It is deliberately
small: it contains gravity, partially submerged buoyancy, and the algebraic
constraint force required to maintain a chosen constant upward velocity.

It does *not* contain a free-surface suction term, drag, added mass, vehicle
propulsion, controller dynamics, or experimental calibration.  Therefore the
reported constraint force is a model residual for the prescribed motion; it
must not be called a measured thrust or a validated CDFV load.

P002 source values used here:
    diameter = 0.090 m
    length   = 0.323 m
    mass     = 2.030 kg

The water density (1000 kg/m^3) and gravitational acceleration are explicit
modelling assumptions.  Replace them when the Ref-01B configuration records
another study environment.

Coordinate convention:
    z = cylinder centre height relative to the still-water free surface
    positive z is upward
    the cylinder axis is vertical

Run from the repository root, for example:

    python Models/CDFV-001/Ref-01B/baseline_model.py

The default run writes three case files and one summary file under
Models/CDFV-001/Ref-01B/results/.
"""

from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional


@dataclass(frozen=True)
class Ref01BConfig:
    """Frozen v0.1 benchmark parameters.

    The geometry and mass are taken from P002's cylindrical experimental
    model.  They are being reused as a computational reference body, not
    claimed as measured CDFV-001 hardware parameters.
    """

    diameter_m: float = 0.090
    length_m: float = 0.323
    mass_kg: float = 2.030
    water_density_kg_m3: float = 1000.0  # explicit freshwater assumption
    gravity_m_s2: float = 9.80665

    @property
    def radius_m(self) -> float:
        return self.diameter_m / 2.0

    @property
    def cross_section_area_m2(self) -> float:
        return math.pi * self.radius_m**2

    @property
    def full_volume_m3(self) -> float:
        return self.cross_section_area_m2 * self.length_m

    @property
    def weight_n(self) -> float:
        return self.mass_kg * self.gravity_m_s2


def clipped(value: float, lower: float, upper: float) -> float:
    return max(lower, min(value, upper))


def submerged_length(z_center_m: float, length_m: float) -> float:
    """Return the vertical cylinder length below z=0.

    The cylinder extends from z_center - length/2 to z_center + length/2.
    The still-water surface is z=0.  End-cap and meniscus details are outside
    this first benchmark.
    """

    return clipped(length_m / 2.0 - z_center_m, 0.0, length_m)


def row_for_state(
    cfg: Ref01BConfig,
    *,
    case_id: str,
    time_s: float,
    z_center_m: float,
    velocity_m_s: float,
    acceleration_m_s2: float = 0.0,
) -> dict[str, float | str]:
    """Calculate one output row using the baseline force balance.

    Positive force is upward.  With prescribed acceleration a:

        m*a = F_constraint + F_buoyancy - F_weight

    so:

        F_constraint = m*a - F_buoyancy + F_weight

    The baseline sets F_free_surface = 0 by definition.
    """

    h_sub = submerged_length(z_center_m, cfg.length_m)
    volume_sub = cfg.cross_section_area_m2 * h_sub
    buoyancy_n = cfg.water_density_kg_m3 * cfg.gravity_m_s2 * volume_sub
    net_hydrostatic_n = buoyancy_n - cfg.weight_n
    constraint_n = (
        cfg.mass_kg * acceleration_m_s2 - buoyancy_n + cfg.weight_n
    )

    return {
        "case_id": case_id,
        "time_s": time_s,
        "z_center_m": z_center_m,
        "velocity_m_s": velocity_m_s,
        "acceleration_m_s2": acceleration_m_s2,
        "submerged_length_m": h_sub,
        "immersion_fraction": h_sub / cfg.length_m,
        "submerged_volume_m3": volume_sub,
        "buoyancy_N": buoyancy_n,
        "weight_N": cfg.weight_n,
        "net_hydrostatic_force_N": net_hydrostatic_n,
        "free_surface_force_N": 0.0,
        "constraint_force_N": constraint_n,
        "constraint_force_abs_N": abs(constraint_n),
    }


def simulate_case(
    cfg: Ref01BConfig,
    *,
    case_id: str,
    velocity_m_s: float,
    dt_s: float,
    z_start_m: Optional[float] = None,
    z_end_m: Optional[float] = None,
) -> list[dict[str, float | str]]:
    """Simulate one constant-speed upward water-exit case."""

    if velocity_m_s <= 0.0:
        raise ValueError("velocity_m_s must be positive")
    if dt_s <= 0.0:
        raise ValueError("dt_s must be positive")

    # The default interval starts and ends half a radius beyond the fully
    # submerged/fully emerged positions, while remaining relative to L.
    if z_start_m is None:
        z_start_m = -0.75 * cfg.length_m
    if z_end_m is None:
        z_end_m = 0.75 * cfg.length_m
    if z_end_m <= z_start_m:
        raise ValueError("z_end_m must be greater than z_start_m")

    distance_m = z_end_m - z_start_m
    duration_s = distance_m / velocity_m_s
    steps = max(1, math.ceil(duration_s / dt_s))

    rows: list[dict[str, float | str]] = []
    for step in range(steps + 1):
        # Force the final row to land exactly on z_end_m.
        distance_at_step = min(distance_m, step * velocity_m_s * dt_s)
        z_center_m = z_start_m + distance_at_step
        time_s = distance_at_step / velocity_m_s
        rows.append(
            row_for_state(
                cfg,
                case_id=case_id,
                time_s=time_s,
                z_center_m=z_center_m,
                velocity_m_s=velocity_m_s,
            )
        )

    return rows


FIELDNAMES = [
    "case_id",
    "time_s",
    "z_center_m",
    "velocity_m_s",
    "acceleration_m_s2",
    "submerged_length_m",
    "immersion_fraction",
    "submerged_volume_m3",
    "buoyancy_N",
    "weight_N",
    "net_hydrostatic_force_N",
    "free_surface_force_N",
    "constraint_force_N",
    "constraint_force_abs_N",
]


def write_csv(path: Path, rows: Iterable[dict[str, float | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_summary(
    path: Path, case_rows: list[tuple[str, float, list[dict[str, float | str]]]]
) -> None:
    summary_fields = [
        "case_id",
        "velocity_m_s",
        "rows",
        "z_start_m",
        "z_end_m",
        "duration_s",
        "min_constraint_force_N",
        "max_constraint_force_N",
        "max_abs_constraint_force_N",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fields)
        writer.writeheader()
        for case_id, velocity, rows in case_rows:
            constraints = [float(row["constraint_force_N"]) for row in rows]
            writer.writerow(
                {
                    "case_id": case_id,
                    "velocity_m_s": velocity,
                    "rows": len(rows),
                    "z_start_m": rows[0]["z_center_m"],
                    "z_end_m": rows[-1]["z_center_m"],
                    "duration_s": rows[-1]["time_s"],
                    "min_constraint_force_N": min(constraints),
                    "max_constraint_force_N": max(constraints),
                    "max_abs_constraint_force_N": max(
                        abs(value) for value in constraints
                    ),
                }
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the CDFV-001 Ref-01B hydrostatic baseline benchmark."
    )
    parser.add_argument(
        "--velocities",
        nargs="+",
        type=float,
        default=[0.10, 0.25, 0.50],
        help="Upward prescribed velocities in m/s (default: 0.10 0.25 0.50).",
    )
    parser.add_argument(
        "--dt",
        type=float,
        default=0.001,
        help="Output time step in seconds (default: 0.001).",
    )
    parser.add_argument(
        "--z-start",
        type=float,
        default=None,
        help="Initial cylinder-centre height in m; default is -0.75 L.",
    )
    parser.add_argument(
        "--z-end",
        type=float,
        default=None,
        help="Final cylinder-centre height in m; default is +0.75 L.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "results",
        help="Directory for CSV outputs.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = Ref01BConfig()

    case_rows: list[tuple[str, float, list[dict[str, float | str]]]] = []
    for velocity in args.velocities:
        case_id = f"Ref-01B-B-{velocity:.2f}mps".replace(".", "p")
        rows = simulate_case(
            cfg,
            case_id=case_id,
            velocity_m_s=velocity,
            dt_s=args.dt,
            z_start_m=args.z_start,
            z_end_m=args.z_end,
        )
        case_rows.append((case_id, velocity, rows))
        output_path = args.output_dir / f"{case_id}.csv"
        write_csv(output_path, rows)
        print(f"wrote {output_path} ({len(rows)} rows)")

    summary_path = args.output_dir / "summary.csv"
    write_summary(summary_path, case_rows)
    print(f"wrote {summary_path}")
    print(
        "Assumptions: freshwater density=1000 kg/m^3; "
        "free-surface force=0; drag and added mass omitted."
    )


if __name__ == "__main__":
    main()
