"""Sensitivity of the P004 conclusion to its inputs.

P004 concludes that added mass is negligible at the accelerations P002 could test and
comparable to the free-surface suction force at g-level accelerations. That conclusion
rests on numbers, and numbers rest on inputs of unequal reliability. This script asks
the question the coverage probe asked of the verifier: if an input is wrong, does the
conclusion actually change, and by how much must it be wrong?

The break-even used throughout is

    a_be = F_suction / m_a,   m_a = k * rho * R^3

so a_be is linear in the suction fraction and in rho, and inverse-cubic in R.

Two qualitative claims are tested separately, because they have very different
margins:

    C1  at a <= 0.15 m/s^2 (the range P002 could measure) added mass is negligible
        margin = a_be / 0.15
    C2  at a ~ 1 g added mass is comparable to the suction force
        margin = a_be / g

A claim flips when its margin crosses 1.
"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# --- baseline inputs, each with its provenance ------------------------------------
BASE = {
    "D": (0.090, "P002 Table 1, via CDFV-001_Reference_Configuration.md"),
    "L": (0.323, "P002 Table 1"),
    "m_body": (2.030, "P002 Table 1"),
    "g": (9.80665, "A-GRAVITY, defined not measured"),
    "rho": (1000.0, "A-FRESHWATER, an assumption"),
    "suction_fraction": (0.10, "P002 abstract: 'about 10% of gravity'"),
    # Added-mass coefficient expressed on the rho*R^3 basis, so it is comparable
    # across shapes. Disk = 8/3 is the flat-faced upper bound; the spheroid of the
    # same L/D gives 1.429.
    "k_disk": (8.0 / 3.0, "classical potential flow, flat disk"),
    "k_spheroid": (1.4291, "prolate spheroid, L/D = 3.59"),
}

TESTED_ACCELERATION = 0.15  # highest acceleration P002 could actually measure


def a_be(D: float, rho: float, suction_fraction: float, m_body: float, k: float) -> float:
    """Break-even acceleration against the P003 suction force."""

    R = D / 2.0
    m_a = k * rho * R**3
    F_suction = suction_fraction * m_body * BASE["g"][0]
    return F_suction / m_a


def margins(**overrides) -> tuple[float, float, float]:
    vals = {name: BASE[name][0] for name in BASE}
    vals.update(overrides)
    a = a_be(
        D=vals["D"],
        rho=vals["rho"],
        suction_fraction=vals["suction_fraction"],
        m_body=vals["m_body"],
        k=vals["k_disk"],
    )
    return a, a / TESTED_ACCELERATION, a / BASE["g"][0]


print("=" * 78)
print("baseline")
print("=" * 78)
for name, (value, source) in BASE.items():
    print(f"  {name:<18} {value:<12} {source}")

a_disk, c1_disk, c2_disk = margins()
a_sph, c1_sph, c2_sph = margins(k_disk=BASE["k_spheroid"][0])
print()
print(f"  a_be (disk)      = {a_disk:8.2f} m/s^2   C1 margin = {c1_disk:6.1f}x   C2 margin = {c2_disk:.2f}x")
print(f"  a_be (spheroid)  = {a_sph:8.2f} m/s^2   C1 margin = {c1_sph:6.1f}x   C2 margin = {c2_sph:.2f}x")
print()
print("  C1 survives while a_be > 0.15 m/s^2; C2 is 'comparable' while a_be is within")
print("  roughly 0.5-2 g, so C2 is a statement about order of magnitude, not a bound.")
print()

print("=" * 78)
print("how wrong must each input be for each claim to flip?")
print("=" * 78)
print()
print("  C1 flips when a_be falls to the tested acceleration (0.15 m/s^2).")
print("  C2 flips when a_be leaves the band where it is 'comparable' to suction;")
print("  that band is taken as 0.5 g to 2 g, i.e. 4.90 to 19.61 m/s^2.")
print()
print(f"  {'input':<20} {'C1: factor to reach 1':>24} {'C2: factor to leave band':>26}")
print("-" * 78)

# a_be is linear in these three and inverse-linear in k, inverse-cubic in D.
c1_factor = TESTED_ACCELERATION / a_disk          # multiply input by this
c2_low = 0.5 * BASE["g"][0] / a_disk              # to drop a_be to 0.5 g
c2_high = 2.0 * BASE["g"][0] / a_disk             # to raise a_be to 2 g
print(f"  {'suction_fraction':<20} {c1_factor:>24.4f} {c2_high:>18.2f} to {c2_low:.2f}")
print(f"  {'rho':<20} {c1_factor:>24.4f} {c2_high:>18.2f} to {c2_low:.2f}")
print(f"  {'m_body':<20} {c1_factor:>24.4f} {c2_high:>18.2f} to {c2_low:.2f}")
print(f"  {'k (shape factor)':<20} {1.0 / c1_factor:>24.2f} "
      f"{(1.0 / c2_high):>18.2f} to {(1.0 / c2_low):.2f}")
d_c1 = (1.0 / c1_factor) ** (1.0 / 3.0)
d_c2_hi = (1.0 / c2_high) ** (1.0 / 3.0)
d_c2_lo = (1.0 / c2_low) ** (1.0 / 3.0)
print(f"  {'D (inverse-cubic)':<20} {d_c1:>24.2f} {d_c2_hi:>18.2f} to {d_c2_lo:.2f}")
print()
print("  Reading: C1 needs an input wrong by ~55x (or D by 3.8x) to break.")
print("           C2 breaks with the same input wrong by only ~1.7x.")

print()
print("=" * 78)
print("order-of-magnitude stress test")
print("=" * 78)
print(f"  {'perturbation':<34} {'a_be':>9} {'C1':>8} {'C2':>7}  verdict")
print("-" * 78)


def row(label: str, **over) -> None:
    a, c1, c2 = margins(**over)
    c1_ok = c1 > 1.0
    # C2 is treated as holding when a_be stays in 0.5 g .. 2 g.
    c2_ok = 0.5 <= c2 <= 2.0
    verdict = []
    if not c1_ok:
        verdict.append("C1 FLIPS")
    if not c2_ok:
        verdict.append("C2 shifts to %.1f g" % c2)
    print(f"  {label:<34} {a:>9.2f} {c1:>8.1f} {c2:>7.2f}  "
          f"{', '.join(verdict) if verdict else 'both survive'}")


row("baseline (disk)")
row("suction 5% instead of 10%", suction_fraction=0.05)
row("suction 20% instead of 10%", suction_fraction=0.20)
row("D x0.9  (radius -10%)", D=0.090 * 0.9)
row("D x1.1  (radius +10%)", D=0.090 * 1.1)
row("D x0.5  (radius halved)", D=0.045)
row("seawater rho=1025", rho=1025.0)
row("shape: spheroid lower bound", k_disk=BASE["k_spheroid"][0])
row("k x0.1  (added mass 10x smaller)", k_disk=BASE["k_disk"][0] * 0.1)
row("k x10   (added mass 10x larger)", k_disk=BASE["k_disk"][0] * 10.0)
row("m_body x1.5", m_body=2.030 * 1.5)

print()
print("=" * 78)
print("what the conclusion actually claims, and its margin")
print("=" * 78)
print(f"  C1 'negligible at a <= 0.15 m/s^2'   holds by a factor {c1_disk:.0f}x "
      f"(disk) / {c1_sph:.0f}x (spheroid)")
print(f"  C2 'comparable at ~1 g'              a_be is {c2_disk:.2f} g (disk) / "
      f"{c2_sph:.2f} g (spheroid)")
print()
print("  A conclusion needing the input wrong by ~60x to flip is robust to")
print("  plausible input error. A conclusion already sitting at its own boundary is")
print("  not, and should be stated as order-of-magnitude only.")
