"""Extension: Aguirre, Cowan and Vickers (2010) on the same data. How does the answer depend on the
shape of demand?

Schmalensee's output-neutral result is special to straight-line demand. Aguirre, Cowan and
Vickers showed that whether discrimination raises output, and welfare, turns on the curvature of
demand in each market. Prices and subscriber counts pin down the slope of each region's demand at
the observed point, but not its curvature. This script therefore re-fits the Netflix and Disney+
demand curves for a range of curvatures (the Bulow-Pfleiderer family in src/demand.py) and records,
for each one, the single worldwide price, the change in subscribers and the change in total
surplus, together with Varian's (1985) upper and lower bounds. It then lets the high-price and
low-price regions have different curvatures, which is the comparison at the heart of ACV.

Inputs: data/raw/netflix_regions.csv, data/raw/disney_plus.csv
Outputs: results/curvature_scan.csv, results/curvature_mixed.csv, results/curvature_breakeven.csv,
results/curvature_scan.png

Run from the repository root (after src/schmalensee.py, which it does not depend on):
    python src/curvature.py
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np
import pandas as pd
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import demand  # noqa: E402
from schmalensee import (MC_BASE, LATEST_NETFLIX, NETFLIX_ORDER, DISNEY_ORDER,  # noqa: E402
                         load)

OUT = ROOT / "results"

# Curvature parameter d of inverse demand p = A - B q^d. d = 1 is linear; d = 2 is concave like a
# dome; d = 0 is exponential demand; d near -1 is very convex, close to constant elasticity.
# Pass-through of a cost change is 1/(1+d), so the grid covers pass-through from 0.25 to 5.
D_GRID = np.round(np.concatenate([np.arange(-0.80, 1.0, 0.05), np.arange(1.0, 3.01, 0.10)]), 2)
MIXED = [0.5, 1.0, 2.0]          # curvatures tried separately for high-price and low-price markets


def cases():
    nf, ds = load()
    yr = nf[nf.fiscal_year == LATEST_NETFLIX].set_index("region").loc[NETFLIX_ORDER]
    g = ds[ds.fiscal_year == ds.fiscal_year.max()].set_index("segment").loc[DISNEY_ORDER]
    return {
        f"Netflix {LATEST_NETFLIX}": (yr.arm_usd.values, yr.members_avg_m.values, [True, True, False, False]),
        f"Disney+ FY{int(ds.fiscal_year.max())}": (g.arpu_usd.values, g.subs_avg_m.values, [True, True, False]),
    }


def scan(all_cases):
    rows = []
    for name, (p, q, _) in all_cases.items():
        revenue = float((p * q).sum() * 12)
        for d in D_GRID:
            r = demand.compare(p, q, MC_BASE, float(d))
            rows.append(dict(case=name, d=float(d), curvature=1 - float(d), pass_through=1 / (1 + float(d)),
                             uniform_price=r["uniform"], markets_served_at_uniform=int(r["served_uniform"].sum()),
                             subs_change_m=r["total_dq"], subs_change_pct=100 * r["total_dq"] / q.sum(),
                             welfare_change_musd=r["total_dW"], welfare_change_pct_revenue=100 * r["total_dW"] / revenue,
                             consumer_surplus_change_musd=r["total_dCS"], profit_change_musd=r["total_dProfit"],
                             varian_lower_musd=r["varian_lower"], varian_upper_musd=r["varian_upper"]))
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "curvature_scan.csv", index=False, float_format="%.6f")
    print(f"\nCurvature scan: {len(D_GRID)} curvatures x {len(all_cases)} cases, marginal cost ${MC_BASE:.2f}")
    show = out[out.d.isin([-0.8, -0.5, 0.0, 0.5, 1.0, 2.0, 3.0])]
    print(show[["case", "d", "pass_through", "uniform_price", "markets_served_at_uniform", "subs_change_m",
                "welfare_change_musd", "varian_lower_musd", "varian_upper_musd"]].round(2).to_string(index=False))
    return out


def breakeven(all_cases):
    """Curvature at which discrimination stops lowering total surplus (Netflix only; Disney+ never crosses)."""
    rows = []
    for name, (p, q, _) in all_cases.items():
        f = lambda d: demand.compare(p, q, MC_BASE, d)["total_dW"]
        lo, hi = -0.8, 3.0
        if np.sign(f(lo)) == np.sign(f(hi)):
            rows.append(dict(case=name, d_breakeven=np.nan, curvature_breakeven=np.nan, pass_through_breakeven=np.nan,
                             note="total surplus change has the same sign across the whole grid"))
            continue
        d0 = brentq(f, lo, hi, xtol=1e-6)
        rows.append(dict(case=name, d_breakeven=d0, curvature_breakeven=1 - d0, pass_through_breakeven=1 / (1 + d0),
                         note="discrimination raises total surplus when demand is more convex than this"))
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "curvature_breakeven.csv", index=False, float_format="%.6f")
    print("\nBreak-even curvature:")
    print(out.round(3).to_string(index=False))
    return out


def mixed(all_cases):
    rows = []
    for name, (p, q, strong) in all_cases.items():
        strong = np.array(strong)
        for ds_ in MIXED:
            for dw in MIXED:
                d = np.where(strong, ds_, dw)
                r = demand.compare(p, q, MC_BASE, d)
                rows.append(dict(case=name, d_high_price_markets=ds_, d_low_price_markets=dw,
                                 uniform_price=r["uniform"], markets_served_at_uniform=int(r["served_uniform"].sum()),
                                 subs_change_m=r["total_dq"], welfare_change_musd=r["total_dW"],
                                 varian_lower_musd=r["varian_lower"], varian_upper_musd=r["varian_upper"]))
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "curvature_mixed.csv", index=False, float_format="%.6f")
    print("\nDifferent curvature in high-price and low-price markets:")
    print(out.round(2).to_string(index=False))
    return out


def figure(sc):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
    colors = {sc.case.unique()[0]: "#c0392b", sc.case.unique()[1]: "#1f4e79"}
    for name, g in sc.groupby("case"):
        axes[0].plot(g.pass_through, g.subs_change_pct, color=colors[name], lw=2, label=name)
        axes[1].plot(g.pass_through, g.welfare_change_musd / 1000, color=colors[name], lw=2, label=name)
    for ax in axes:
        ax.axhline(0, color="0.4", lw=0.8)
        ax.axvline(0.5, color="0.6", lw=0.8, ls=":")
        ax.set_xscale("log")
        ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
        ax.set_xticks([0.25, 0.5, 1, 2, 5])
        ax.set_xticklabels(["0.25", "0.5\n(straight line)", "1", "2", "5"])
        ax.set_xlabel("Pass-through of a cost change to price (curvature of demand)")
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("Change in subscribers from discrimination (%)")
    axes[1].set_ylabel("Change in total surplus ($ billion a year)")
    axes[0].legend(frameon=False, fontsize=9)
    axes[0].set_title("Output", fontsize=10.5)
    axes[1].set_title("Consumer surplus plus profit", fontsize=10.5)
    fig.tight_layout()
    fig.savefig(OUT / "curvature_scan.png", dpi=150)
    plt.close(fig)


def main():
    OUT.mkdir(exist_ok=True)
    all_cases = cases()
    sc = scan(all_cases)
    breakeven(all_cases)
    mixed(all_cases)
    figure(sc)


if __name__ == "__main__":
    main()
