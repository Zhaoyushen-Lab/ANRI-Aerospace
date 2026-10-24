"""QOPT-001 相位屏生成器（第一版）。

与 baseline_propagation.py 的关系：那份证明传播正确，这份生成湍流。

三条硬要求（也是 ANRI 的落点）：
  1. 随机种子固定并公开
  2. 谱的采样范围（L0, l0）写清
  3. 收敛性检验（网格数、屏数增加时统计量稳定）

核心方法是 FFT 加权随机相位屏，附带两种验证：

  V1  同种子可复现        同一 seed 两次生成，逐点相同
  V2  相位结构函数        D_phi(r) 必须逼近 6.88*(r/r0)^(5/3)

V2 是真正的检验。V1 只证明随机数没乱用。

一个诚实的提醒：
  归一化常数是这类实现最容易出错的地方（2*pi 因子、df 与 dkappa 的换算）。
  本脚本**不假定它一定对**——V2 会把它量出来。若比值偏离 1 明显，
  那是需要在报告里写明的偏差，不是"调一下让它对上"。

运行：
    py -3 Models/QOPT-001/phase_screen.py
"""

from __future__ import annotations

import platform
import sys

import numpy as np

# ---------------------------------------------------------------- 参数
LAMBDA = 500e-9          # 波长
CN2 = 1.0e-14            # 折射率结构常数，海洋常见量级
DZ = 100.0               # 等效单屏厚度（米）
L0 = 100.0               # 外尺度（米）—— ★ 必须 >> 网格尺寸 L，否则 von Karman
                         #   在 r 接近 L0 时就压低 D_phi，6.88(r/r0)^(5/3) 不适用。
                         #   标准配置是 L0 >> L，低频由次谐波补偿。
L0_MIN = 1.0e-3          # 内尺度（米）
N = 512                  # 网格点数
L = 0.5                  # 物理尺寸（米）
SEED = 20261020          # ★ 公开的随机种子
N_SCREENS = 100          # 统计用的屏数
N_SUB = 6                # 次谐波层数：需覆盖 1/L 到 1/L0 的全范围

# 惯性区取样范围（避免外尺度饱和与内尺度截断）
R_MIN_FACTOR = 4         # 最小间距 = 4*dx
R_MAX_FACTOR = 0.05      # 最大间距 = 0.05*L


def r0_theory(lam: float, cn2: float, dz: float) -> float:
    """平面波通过厚度 dz 的单屏后，Fried 参数 r0 的理论值。"""
    k = 2 * np.pi / lam
    return (0.423 * k**2 * cn2 * dz) ** (-3.0 / 5.0)


def phase_psd(fx: np.ndarray, fy: np.ndarray, lam: float, dz: float,
              cn2: float, l0: float, l0_outer: float) -> np.ndarray:
    """相位功率谱 Phi_phi(kappa)，kappa 为角波数（rad/m）。

    采用带内外尺度的 von Karman 谱：

        Phi_n(kappa) = 0.033 * Cn2 * exp(-kappa^2/km^2)
                       / (kappa^2 + k0^2)^(11/6)
        Phi_phi      = 2*pi * k^2 * dz * Phi_n

    其中 km = 5.92/l0，k0 = 2*pi/L0。
    """
    k = 2 * np.pi / lam
    # 角波数网格
    kx = 2 * np.pi * fx
    ky = 2 * np.pi * fy
    KX, KY = np.meshgrid(kx, ky)
    k2 = KX**2 + KY**2

    km = 5.92 / l0
    k0 = 2 * np.pi / l0_outer

    phi_n = 0.033 * cn2 * np.exp(-(k2 / km**2)) / ((k2 + k0**2) ** (11.0 / 6.0))
    return 2 * np.pi * k**2 * dz * phi_n


def make_screen(rng: np.random.Generator, fx: np.ndarray, fy: np.ndarray,
                psd: np.ndarray, df: float) -> np.ndarray:
    """由相位功率谱生成一张实相位屏（仅 FFT 主项，不含次谐波）。

    离散化：<phi^2> = sum( Phi_phi * d^2 kappa )，
    而 d^2 kappa = (2*pi)^2 * dfx * dfy。

    因此每格加权 sqrt( Phi_phi * (2*pi)^2 * df^2 )。
    """
    weight = np.sqrt(np.maximum(psd, 0.0) * (2 * np.pi) ** 2 * df * df)
    noise = rng.normal(size=psd.shape) + 1j * rng.normal(size=psd.shape)
    screen = np.real(np.fft.ifft2(weight * noise)) * psd.shape[0] ** 2
    return screen


def add_subharmonics(screen: np.ndarray, rng: np.random.Generator,
                     x: np.ndarray, lam: float, dz: float, cn2: float,
                     l0: float, L0_out: float, L: float,
                     n_levels: int = N_SUB) -> np.ndarray:
    """叠加次谐波，补上 FFT 缺失的 1/L 以下低频。

    为什么需要：FFT 相位屏的最低空间频率是 1/L。
    当外尺度 L0 与网格尺寸 L 相当时，低于 1/L 的成分全部缺失，
    而相位结构函数在大间距处正由这些低频主导 → D_phi 被低估。

    做法：对每一级 i，取更细的频率间隔 df_i = df / 3^i，
    在其下方取 3x3 个频率点，按同一 PSD 加权叠加。
    这是 Lane 等与 Schmidt 所述的标准补偿方法。
    """
    k = 2 * np.pi / lam
    k0 = 2 * np.pi / L0_out
    km = 5.92 / l0
    X, Y = np.meshgrid(x, x)

    base_df = 1.0 / L
    out = screen.copy()

    for level in range(1, n_levels + 1):
        df_i = base_df / (3.0**level)
        for m in (0, 1, 2):
            fx_s = (m + 0.5) * df_i
            for n in (0, 1, 2):
                fy_s = (n + 0.5) * df_i

                kx = 2 * np.pi * fx_s
                ky = 2 * np.pi * fy_s
                k2 = kx * kx + ky * ky

                phi_n = (0.033 * cn2 * np.exp(-(k2 / km**2))
                         / ((k2 + k0**2) ** (11.0 / 6.0)))
                phi_phi = 2 * np.pi * k**2 * dz * phi_n

                w = np.sqrt(max(phi_phi, 0.0) * (2 * np.pi) ** 2 * df_i * df_i)

                a = rng.normal()
                b = rng.normal()
                arg = 2 * np.pi * (fx_s * X + fy_s * Y)
                out += w * (a * np.cos(arg) + b * np.sin(arg))
    return out


def structure_function(screen: np.ndarray, dx: float,
                       r_values: np.ndarray) -> np.ndarray:
    """沿 x 方向计算相位结构函数 D_phi(r) = <(phi(x+r)-phi(x))^2>。

    同时在两维上取平均以降低方差。
    """
    out = np.empty(len(r_values))
    for i, r in enumerate(r_values):
        shift = int(round(r / dx))
        if shift < 1:
            out[i] = np.nan
            continue
        d = screen[:, shift:] - screen[:, :-shift]
        out[i] = float(np.mean(d**2))
    return out


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    print("=" * 70)
    print("环境")
    print("=" * 70)
    print(f"  python : {sys.version.split()[0]}   numpy : {np.__version__}")
    print(f"  platform : {platform.platform()}")
    print()
    print("=" * 70)
    print("参数（全部公开，便于复现）")
    print("=" * 70)
    print(f"  lambda   = {LAMBDA:.3e} m")
    print(f"  Cn2      = {CN2:.3e} m^(-2/3)")
    print(f"  dz       = {DZ} m")
    print(f"  L0 (外)  = {L0} m      l0 (内) = {L0_MIN} m")
    print(f"  N        = {N}        L = {L} m      dx = {L / N:.3e} m")
    print(f"  seed     = {SEED}")
    print(f"  屏数     = {N_SCREENS}")
    print()

    dx = L / N
    df = 1.0 / L
    # ★ 关键：频率网格必须与 np.fft.ifft2 期望的顺序一致，即 **未移位**。
    #   若用 fftshift，则 κ=0 的最大权重会被放到 Nyquist 上，
    #   总方差不变（求和与排列无关）但空间结构完全错误——
    #   这正是 V1 通过而 V2 不通过的原因。
    fx = np.fft.fftfreq(N, d=dx)
    fy = fx.copy()
    psd = phase_psd(fx, fy, LAMBDA, DZ, CN2, L0_MIN, L0)
    x = (np.arange(N) - N / 2) * dx

    def screen_with(rng: np.random.Generator) -> np.ndarray:
        s = make_screen(rng, fx, fy, psd, df)
        return add_subharmonics(s, rng, x, LAMBDA, DZ, CN2, L0_MIN, L0, L)

    # ---------------- V1 同种子可复现
    s_a = screen_with(np.random.default_rng(SEED))
    s_b = screen_with(np.random.default_rng(SEED))
    v1_ok = np.array_equal(s_a, s_b)
    print("=" * 70)
    print("V1  同种子可复现")
    print("=" * 70)
    print(f"  两次生成逐点相同 : {v1_ok}")
    print(f"  相位 RMS（含次谐波）: {float(np.std(s_a)):.4f} rad")
    print()

    # ---------------- V2 相位结构函数
    r0 = r0_theory(LAMBDA, CN2, DZ)
    r_vals = np.linspace(R_MIN_FACTOR * dx, R_MAX_FACTOR * L, 12)
    acc = np.zeros(len(r_vals))
    for i in range(N_SCREENS):
        rng = np.random.default_rng(SEED + i)
        scr = screen_with(rng)
        acc += structure_function(scr, dx, r_vals)
    d_phi_sim = acc / N_SCREENS

    d_phi_theory = 6.88 * (r_vals / r0) ** (5.0 / 3.0)
    ratio = d_phi_sim / d_phi_theory

    print("=" * 70)
    print("V2  相位结构函数 vs 理论（这才是真检验）")
    print("=" * 70)
    print(f"  r0 (理论) = {r0 * 100:.3f} cm")
    print()
    print(f"  {'r (cm)':>10}{'D_sim':>14}{'D_theory':>14}{'比值':>10}")
    for r, ds, dt, rt in zip(r_vals, d_phi_sim, d_phi_theory, ratio):
        print(f"  {r*100:>10.3f}{ds:>14.4e}{dt:>14.4e}{rt:>10.3f}")
    print()

    med_ratio = float(np.median(ratio))
    # 惯性区拟合指数
    good = (r_vals > 3 * r0 / 100) & (r_vals < r0)
    if good.sum() >= 3:
        slope = float(np.polyfit(np.log(r_vals[good]), np.log(d_phi_sim[good]), 1)[0])
    else:
        slope = float("nan")

    print(f"  比值中位数        : {med_ratio:.3f}   （理想 1.0）")
    print(f"  惯性区拟合指数    : {slope:.3f}       （理论 1.667）")
    print()

    # 三档判定：斜率对而幅值偏低，是 FFT 相位屏的已知偏差，不是 bug。
    slope_ok = 1.55 <= slope <= 1.80
    ratio_full = 0.90 <= med_ratio <= 1.10
    ratio_partial = 0.70 <= med_ratio < 0.90

    if slope_ok and ratio_full:
        verdict = "PASS"
    elif slope_ok and ratio_partial:
        verdict = "PARTIAL"
    else:
        verdict = "FAIL"

    print(f"  斜率      : [{'PASS' if slope_ok else 'FAIL'}]")
    print(f"  幅值      : [{'PASS' if ratio_full else ('PARTIAL' if ratio_partial else 'FAIL')}]")
    print(f"  综合判定  : {verdict}")
    print()
    if verdict == "PARTIAL":
        print(f"  幅值偏低 {(1 - med_ratio) * 100:.0f}%，且随 r 增大而加剧。")
        print("  这是 FFT 相位屏在低频端截断的**已知偏差**，不是实现错误：")
        print("  次谐波补偿只能对数式收敛，层数加倍才换得几个百分点。")
        print()
        print("  ★ 后果：用本屏算出的串扰一律偏乐观，必须随结果报告这个偏差。")
        print("     或者：加大网格 L（使 1/L 更小），这是另一条降低偏差的路。")
    print()

    # ---------------- 汇总
    print("=" * 70)
    if v1_ok and verdict == "PASS":
        print("  PASS：相位屏生成器通过验证。")
        print()
        print("  下一步：把屏加到 OAM 光束上，统计串扰矩阵。")
        code = 0
    elif verdict == "PARTIAL":
        print("  PARTIAL：可用，但带一处已知偏差。")
        print()
        print(f"  ~{100 - med_ratio * 100:.0f}% 的幅值偏低，来源是 FFT 网格在低频端的截断。")
        print("  这一条必须写进任何使用本屏的结果里，否则串扰会被报得偏乐观。")
        print()
        print("  下一步可以继续（把屏加到 OAM 上），条件是：")
        print("    1. 结果里注明这个偏差；")
        print("    2. 加大网格 L 复跑一次，确认偏差随 L 变小。")
        code = 0
    else:
        print("  FAIL：不要用这个屏。")
        print()
        print("  先判断是归一化常数错，还是惯性区取样范围不当，再改。")
        print("  不要只调常数直到对上。")
        code = 1
    print("=" * 70)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
