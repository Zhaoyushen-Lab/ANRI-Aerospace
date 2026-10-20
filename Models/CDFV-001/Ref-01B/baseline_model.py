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
    acceleration_m_s2: float = 0.0,
) -> list[dict[str, float | str]]:
    """Simulate one upward water-exit case along a prescribed motion.

    ``acceleration_m_s2`` defaults to 0.0, which reproduces the original
    constant-speed case byte for byte: the time step collapses to
    ``distance / velocity`` and the position stays linear in time.  A non-zero
    value prescribes constant acceleration, so

        z(t) = z_start + v0*t + a*t^2/2
        v(t) = v0 + a*t

    which is what makes the inertial term in the force balance observable at all.
    With a = 0 the recorded ``constraint_force_N`` cannot distinguish "added mass
    was omitted" from "added mass is negligible", because m*a vanishes either way.
    """

    if velocity_m_s <= 0.0:
        raise ValueError("velocity_m_s must be positive")
    if dt_s <= 0.0:
        raise ValueError("dt_s must be positive")

    # The default interval starts and ends a quarter of a body LENGTH beyond the
    # fully submerged (-L/2) and fully emerged (+L/2) centres, i.e. 0.25*L =
    # 0.080750 m, which is 1.79 radii - not "half a radius", as an earlier comment
    # claimed. See Research_Planning/Ref-01B_Initial_Immersion_Decision.md.
    #
    # Within the baseline the exact clearance does not matter: the free-surface term
    # is excluded (L-EXCLUDED-PHYSICS), so any z_start <= -L/2 gives an identical
    # first row of full buoyancy and the only difference is how long that state is
    # held. It stops being arbitrary once P003 adds the free-surface term.
    if z_start_m is None:
        z_start_m = -0.75 * cfg.length_m
    if z_end_m is None:
        z_end_m = 0.75 * cfg.length_m
    if z_end_m <= z_start_m:
        raise ValueError("z_end_m must be greater than z_start_m")

    distance_m = z_end_m - z_start_m

    if acceleration_m_s2 == 0.0:
        duration_s = distance_m / velocity_m_s
    else:
        # Solve (a/2) t^2 + v0 t - distance = 0 for the positive root.
        discriminant = velocity_m_s**2 + 2.0 * acceleration_m_s2 * distance_m
        if discriminant < 0.0:
            raise ValueError(
                "prescribed acceleration cannot cover the requested distance"
            )
        duration_s = (-velocity_m_s + math.sqrt(discriminant)) / acceleration_m_s2
        if duration_s <= 0.0:
            raise ValueError("prescribed acceleration gives a non-positive duration")

    steps = max(1, math.ceil(duration_s / dt_s))

    rows: list[dict[str, float | str]] = []
    for step in range(steps + 1):
        if acceleration_m_s2 == 0.0:
            # Constant-speed path, kept literally identical to the original so
            # existing outputs stay byte-for-byte unchanged.  Computing
            # distance/velocity via the general helpers reorders the floating-point
            # operations and shifts time_s in the last few digits, which is enough
            # to change the recorded CSV and therefore the registered hashes.
            distance_at_step = min(distance_m, step * velocity_m_s * dt_s)
            z_center_m = z_start_m + distance_at_step
            time_s = distance_at_step / velocity_m_s
            speed_at_step = velocity_m_s
        else:
            # Force the final row to land exactly on z_end_m.
            distance_at_step = min(
                distance_m, _distance_at(step * dt_s, velocity_m_s, acceleration_m_s2)
            )
            time_s = _time_for_distance(
                distance_at_step, velocity_m_s, acceleration_m_s2
            )
            z_center_m = z_start_m + distance_at_step
            speed_at_step = velocity_m_s + acceleration_m_s2 * time_s

        rows.append(
            row_for_state(
                cfg,
                case_id=case_id,
                time_s=time_s,
                z_center_m=z_center_m,
                velocity_m_s=speed_at_step,
                acceleration_m_s2=acceleration_m_s2,
            )
        )

    return rows


def _distance_at(
    time_s: float, velocity_m_s: float, acceleration_m_s2: float
) -> float:
    """Distance travelled under constant acceleration from the initial speed."""

    return velocity_m_s * time_s + 0.5 * acceleration_m_s2 * time_s**2


def _time_for_distance(
    distance_m: float, velocity_m_s: float, acceleration_m_s2: float
) -> float:
    """Inverse of ``_distance_at`` for the positive root.

    With zero acceleration this is exactly ``distance / velocity``, which keeps the
    constant-speed cases identical to their previous bytes.
    """

    if acceleration_m_s2 == 0.0:
        return distance_m / velocity_m_s
    discriminant = velocity_m_s**2 + 2.0 * acceleration_m_s2 * distance_m
    return (-velocity_m_s + math.sqrt(discriminant)) / acceleration_m_s2


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
    """Write one case CSV with LF terminators on every platform.

    ``lineterminator="\\n"`` is deliberate: the csv module defaults to CRLF, and
    a platform-dependent terminator would change the SHA-256 of a frozen result
    artifact between Windows and Linux.
    """

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=FIELDNAMES, lineterminator="\n"
        )
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
        writer = csv.DictWriter(
            handle, fieldnames=summary_fields, lineterminator="\n"
        )
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
        "--accelerations",
        nargs="+",
        type=float,
        default=None,
        help=(
            "Prescribed constant accelerations in m/s^2. When omitted the original "
            "constant-speed cases are produced with their original file names, so "
            "existing outputs stay byte-identical. When given, one case is written "
            "per (velocity, acceleration) pair with an 'a<value>mps2' suffix."
        ),
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
        # The constant-speed case for each velocity is always produced, so the
        # default run keeps its original file names and bytes, and an accelerated
        # run still yields a summary that contains both kinds of case.
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

        for acceleration in args.accelerations or ():
            case_id_acc = (
                f"Ref-01B-B-{velocity:.2f}mps-a{acceleration:.2f}mps2"
            ).replace(".", "p")
            rows_acc = simulate_case(
                cfg,
                case_id=case_id_acc,
                velocity_m_s=velocity,
                dt_s=args.dt,
                z_start_m=args.z_start,
                z_end_m=args.z_end,
                acceleration_m_s2=acceleration,
            )
            case_rows.append((case_id_acc, velocity, rows_acc))
            output_path_acc = args.output_dir / f"{case_id_acc}.csv"
            write_csv(output_path_acc, rows_acc)
            print(f"wrote {output_path_acc} ({len(rows_acc)} rows)")

    summary_path = args.output_dir / "summary.csv"
    write_summary(summary_path, case_rows)
    print(f"wrote {summary_path}")
    print(
        "Assumptions: freshwater density=1000 kg/m^3; "
        "free-surface force=0; drag and added mass omitted."
    )


if __name__ == "__main__":
    main()
