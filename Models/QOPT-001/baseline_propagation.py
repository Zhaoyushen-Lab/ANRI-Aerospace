"""QOPT-001 地基：角谱法传播的最小验证。

目的不是"算出什么"，是"证明传播代码没写错"。

在此之前，任何相位屏结果都不可信。

五项检验，按强度递增：

  T1  z = 0 恒等        传播 0 距离必须原样返回
  T2  能量守恒          角谱法用酉变换，总能量必须不变
  T3  全零相位屏         全零屏不能改变场（这正是用户点名要的那一项）
  T4  平面波不变         自由空间中平面波传播后强度仍均匀
  T5  高斯光束 vs 解析解  ★ 唯一强检验：与 w(z) 的闭式解对比

T1–T4 都可能因为代码什么都不做而"通过"。只有 T5 真正检验了传播。

运行：
    py -3 Models/QOPT-001/baseline_propagation.py
"""

from __future__ import annotations

import platform
import sys

import numpy as np

# ---------------------------------------------------------------- 参数
LAMBDA = 500e-9          # 波长，蓝绿窗口
N = 1024                 # 网格点数（每边）
L = 0.05                 # 物理尺寸（米）
W0 = 0.5e-3              # 高斯光束腰半径
Z_TEST = 5.0             # 传播距离（米）
SEED = 20261020          # 固定种子，写进任何报告


def make_grid(n: int, size: float) -> tuple[np.ndarray, np.ndarray,
                                             np.ndarray, np.ndarray]:
    """返回 (x, y, fx, fy)。坐标以 0 为中心，频率以 0 为中心。"""
    dx = size / n
    x = (np.arange(n) - n / 2) * dx
    fx = np.fft.fftshift(np.fft.fftfreq(n, d=dx))
    return x, x.copy(), fx, fx.copy()


def angular_spectrum(U: np.ndarray, z: float, lam: float,
                     fx: np.ndarray, fy: np.ndarray) -> np.ndarray:
    """角谱法传播。

    A(fx,fy,z) = A(fx,fy,0) * exp(i * kz * z)，
    kz = 2*pi*sqrt(1/lam^2 - fx^2 - fy^2)。

    倏逝波（fx^2+fy^2 > 1/lam^2）置零——本组参数下不会触发。
    """
    FX, FY = np.meshgrid(fx, fy)
    arg = 1.0 / lam**2 - FX**2 - FY**2
    kz = 2 * np.pi * np.sqrt(np.maximum(arg, 0.0))
    kz = np.where(arg >= 0.0, kz, 0.0)

    A = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(U)))
    A = A * np.exp(1j * kz * z)
    return np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(A)))


def gaussian(x: np.ndarray, y: np.ndarray, w0: float) -> np.ndarray:
    X, Y = np.meshgrid(x, y)
    return np.exp(-(X**2 + Y**2) / w0**2).astype(complex)


def apply_phase_screen(U: np.ndarray, phase: np.ndarray) -> np.ndarray:
    """把相位屏加到场上。"""
    return U * np.exp(1j * phase)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    print("=" * 68)
    print("环境")
    print("=" * 68)
    print(f"  python     : {sys.version.split()[0]}")
    print(f"  numpy      : {np.__version__}")
    print(f"  platform   : {platform.platform()}")
    print()
    print("=" * 68)
    print("参数")
    print("=" * 68)
    print(f"  lambda = {LAMBDA:.3e} m   N = {N}   L = {L} m")
    print(f"  w0     = {W0:.3e} m   z = {Z_TEST} m   seed = {SEED}")
    dx = L / N
    print(f"  dx = {dx:.3e} m   Nyquist fx = {1 / (2 * dx):.3e} /m   "
          f"1/lambda = {1 / LAMBDA:.3e} /m")
    print()

    x, y, fx, fy = make_grid(N, L)
    results: list[tuple[str, bool, str]] = []

    # ---------------- T1: z = 0 恒等
    U0 = gaussian(x, y, W0)
    U_id = angular_spectrum(U0, 0.0, LAMBDA, fx, fy)
    err = float(np.max(np.abs(U_id - U0)))
    ok = err < 1e-10
    results.append(("T1  z=0 恒等", ok, f"max|Δ| = {err:.3e}"))

    # ---------------- T2: 能量守恒
    Uz = angular_spectrum(U0, Z_TEST, LAMBDA, fx, fy)
    e0 = float(np.sum(np.abs(U0) ** 2))
    ez = float(np.sum(np.abs(Uz) ** 2))
    rel = abs(ez - e0) / e0
    ok = rel < 1e-10
    results.append(("T2  能量守恒", ok, f"相对偏差 = {rel:.3e}"))

    # ---------------- T3: 全零相位屏
    zero_screen = np.zeros((N, N), dtype=float)
    U_with = apply_phase_screen(U0, zero_screen)
    err = float(np.max(np.abs(U_with - U0)))
    ok = err == 0.0
    results.append(("T3  全零相位屏不改变场", ok, f"max|Δ| = {err:.3e}"))

    # ---------------- T4: 平面波不变
    U_plane = np.ones((N, N), dtype=complex)
    U_plane_z = angular_spectrum(U_plane, Z_TEST, LAMBDA, fx, fy)
    amp = np.abs(U_plane_z)
    spread = float(np.max(amp) - np.min(amp))
    ok = spread < 1e-6
    results.append(("T4  平面波强度不变", ok, f"强度极差 = {spread:.3e}"))

    # ---------------- T5: 高斯光束 vs 解析解（强检验）
    zR = np.pi * W0**2 / LAMBDA
    w_analytic = W0 * np.sqrt(1 + (Z_TEST / zR) ** 2)
    I = np.abs(Uz) ** 2
    I0_peak = float(np.max(np.abs(U0) ** 2))
    peak_sim = float(np.max(I))
    peak_analytic = I0_peak * (W0 / w_analytic) ** 2
    peak_rel = abs(peak_sim - peak_analytic) / peak_analytic

    # 由模拟场反推束宽：二阶矩定义
    X, Y = np.meshgrid(x, y)
    r2 = X**2 + Y**2
    w_sim = float(np.sqrt(2 * np.sum(I * r2) / np.sum(I)))
    w_rel = abs(w_sim - w_analytic) / w_analytic

    ok = (peak_rel < 0.02) and (w_rel < 0.02)
    results.append(
        ("T5  高斯光束 vs 解析解", ok,
         f"束宽 {w_sim*1e3:.4f} vs {w_analytic*1e3:.4f} mm ({w_rel*100:.2f}%)；"
         f"峰值偏差 {peak_rel*100:.2f}%")
    )

    # ---------------- 汇总
    print("=" * 68)
    print("检验结果")
    print("=" * 68)
    for name, passed, detail in results:
        mark = "PASS" if passed else "FAIL"
        print(f"  [{mark}] {name}")
        print(f"         {detail}")
    print()

    n_pass = sum(1 for _, p, _ in results if p)
    print(f"  通过 {n_pass}/{len(results)}")
    print()

    if n_pass == len(results):
        print("  地基成立：传播代码可信，可以开始加湍流。")
        print()
        print("  ⚠️ 但记住：T1–T4 都可能因为'代码什么都不做'而通过。")
        print("     真正证明传播正确性的只有 T5。")
        return 0
    print("  地基不成立：先修传播代码，任何相位屏结果都不可信。")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
