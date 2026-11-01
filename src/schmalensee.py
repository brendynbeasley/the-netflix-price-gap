"""Schmalensee (1981) on streaming prices: does charging regions different prices raise total output?

Schmalensee showed that a monopolist's third-degree price discrimination can raise welfare only if
it raises total output, and that with straight-line demands and every market served, output does
not change at all, so welfare must fall. This script takes the prices and subscriber counts that
Netflix and Disney report for each region in their 10-K filings, fits straight-line demand curves
through them on the assumption that each regional price is profit-maximizing, and computes what a
single worldwide price would do to subscribers, consumer surplus, profit and total surplus.

Inputs (written by src/build_data.py from the companies' 10-K filings):
    data/raw/netflix_regions.csv   Netflix revenue, memberships and ARM by region, 2017-2024
    data/raw/disney_plus.csv       Disney+ paid subscribers and ARPU by segment, FY2021-FY2024

Outputs: results/netflix_2024_linear.csv, results/netflix_by_year.csv, results/disney_linear.csv,
results/cost_sensitivity.csv, results/headline.csv, results/netflix_demand_2024.png

Run from the repository root:
    python src/schmalensee.py
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import demand  # noqa: E402

RAW = ROOT / "data" / "raw"
OUT = ROOT / "results"

# Marginal cost of one more subscriber, dollars a month, the same in every region (Schmalensee's
# assumption). Content is a fixed cost; what scales with subscribers is streaming delivery, payment
# processing (a few percent of the price) and customer service, which I put at 50 cents. The
# alternatives bracket it; a cost above a market's price cannot be used for that market.
MC_BASE = 0.50
MC_ALTERNATIVES = [0.0, 0.50, 1.0, 2.0]
LINEAR = 1.0                     # d = 1: straight-line demand, the case Schmalensee's theorem covers
LATEST_NETFLIX = 2024            # Netflix stopped reporting memberships after 2024
NETFLIX_ORDER = ["UCAN", "EMEA", "LATAM", "APAC"]
NETFLIX_NAMES = {"UCAN": "US and Canada", "EMEA": "Europe, Middle East and Africa",
                 "LATAM": "Latin America", "APAC": "Asia-Pacific"}
DISNEY_ORDER = ["Domestic", "International", "Hotstar"]
DISNEY_NAMES = {"Domestic": "Disney+ US and Canada", "International": "Disney+ International (excl. Hotstar)",
                "Hotstar": "Disney+ Hotstar"}


def load():
    nf = pd.read_csv(RAW / "netflix_regions.csv")
    ds = pd.read_csv(RAW / "disney_plus.csv")
    print(f"Loaded netflix_regions.csv: {len(nf)} rows, years {nf.fiscal_year.min()}-{nf.fiscal_year.max()}")
    print(f"Loaded disney_plus.csv: {len(ds)} rows, fiscal years {ds.fiscal_year.min()}-{ds.fiscal_year.max()}")

    # Netflix reports average paying memberships for the year, and ARM is revenue divided by that
    # average and by 12, so it is the quantity that goes with the price.
    nf["members_avg_m"] = nf.avg_paying_memberships_m
    implied = nf.arm_usd * nf.members_avg_m * 12
    nf["revenue_check_pct"] = 100 * (implied / nf.revenue_musd - 1)
    print(f"  Netflix check: ARM x average members x 12 matches reported revenue within "
          f"{nf.revenue_check_pct.abs().max():.1f}% in every region-year")

    # Disney reports subscribers at fiscal year end; average over the year = mean of the two ends.
    ds = ds.sort_values(["segment", "fiscal_year"])
    ds["subs_prev_m"] = ds.groupby("segment").paid_subs_end_m.shift(1)
    before = len(ds)
    ds = ds.dropna(subset=["subs_prev_m", "arpu_usd"]).copy()
    ds["subs_avg_m"] = (ds.paid_subs_end_m + ds.subs_prev_m) / 2
    print(f"  Disney: kept {len(ds)} segment-years with a prior year-end count and ARPU, "
          f"dropped {before - len(ds)} (the first year has no prior count)")
    return nf, ds


def market_table(names, order, p, q, r):
    return pd.DataFrame({
        "market": [names[k] for k in order], "code": order,
        "price_actual": p, "subs_actual_m": q,
        "price_uniform": r["uniform"], "subs_uniform_m": r["q_uniform"],
        "served_at_uniform": r["served_uniform"],
        "subs_change_m": r["dq"],
        "consumer_surplus_change_musd": r["dCS"],
        "profit_change_musd": r["dProfit"],
        "welfare_change_musd": r["dW"],
    })


def netflix_latest(nf):
    yr = nf[nf.fiscal_year == LATEST_NETFLIX].set_index("region").loc[NETFLIX_ORDER]
    p, q = yr.arm_usd.values, yr.members_avg_m.values
    r = demand.compare(p, q, MC_BASE, LINEAR)
    tab = market_table(NETFLIX_NAMES, NETFLIX_ORDER, p, q, r)
    tab["choke_price"] = 2 * p - MC_BASE
    # With straight lines and unchanged total output, the loss is a sum of triangles, one per
    # region: half the price gap times the shift in members (dollars a month x 12).
    tab["price_gap"] = p - r["uniform"]
    tab["triangle_musd"] = 0.5 * np.abs(tab.price_gap * tab.subs_change_m) * 12
    tab.to_csv(OUT / "netflix_2024_linear.csv", index=False, float_format="%.6f")
    print(f"\nNetflix {LATEST_NETFLIX}, straight-line demand, marginal cost ${MC_BASE:.2f}:")
    print(tab.round(2).to_string(index=False))
    print(f"  single profit-maximizing price ${r['uniform']:.2f}; total members change "
          f"{r['total_dq']:+.3f}M; total surplus change ${r['total_dW']:,.0f}M a year")
    return yr, r, tab


def netflix_years(nf):
    rows = []
    for year, g in nf.groupby("fiscal_year"):
        g = g.set_index("region").loc[NETFLIX_ORDER]
        p, q = g.arm_usd.values, g.members_avg_m.values
        r = demand.compare(p, q, MC_BASE, LINEAR)
        revenue = float((p * q).sum() * 12)
        rows.append(dict(
            fiscal_year=year, members_avg_m=q.sum(), revenue_musd=revenue,
            price_UCAN=p[0], price_EMEA=p[1], price_LATAM=p[2], price_APAC=p[3],
            ratio_high_to_low=p.max() / p.min(), uniform_price=r["uniform"],
            regions_served_at_uniform=int(r["served_uniform"].sum()),
            members_change_m=r["total_dq"], welfare_change_musd=r["total_dW"],
            welfare_change_pct_revenue=100 * r["total_dW"] / revenue,
            consumer_surplus_change_musd=r["total_dCS"], profit_change_musd=r["total_dProfit"],
            ucan_share_of_members=q[0] / q.sum(),
        ))
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "netflix_by_year.csv", index=False, float_format="%.6f")
    print("\nNetflix by year, straight-line demand:")
    print(out[["fiscal_year", "members_avg_m", "ratio_high_to_low", "uniform_price",
               "regions_served_at_uniform", "members_change_m", "welfare_change_musd",
               "welfare_change_pct_revenue"]].round(3).to_string(index=False))
    return out


def disney(ds):
    tabs, summary = [], []
    for year, g in ds.groupby("fiscal_year"):
        g = g.set_index("segment").loc[DISNEY_ORDER]
        p, q = g.arpu_usd.values, g.subs_avg_m.values
        r = demand.compare(p, q, MC_BASE, LINEAR)
        t = market_table(DISNEY_NAMES, DISNEY_ORDER, p, q, r)
        t["choke_price"] = 2 * p - MC_BASE
        t.insert(0, "fiscal_year", year)
        tabs.append(t)
        summary.append(dict(fiscal_year=year, uniform=r["uniform"], dq=r["total_dq"], dW=r["total_dW"],
                            dCS=r["total_dCS"], dProfit=r["total_dProfit"],
                            lower=r["varian_lower"], upper=r["varian_upper"]))
    pd.DataFrame(summary).rename(columns={
        "uniform": "uniform_price", "dq": "subs_change_m", "dW": "welfare_change_musd",
        "dCS": "consumer_surplus_change_musd", "dProfit": "profit_change_musd",
        "lower": "varian_lower_musd", "upper": "varian_upper_musd"}).to_csv(OUT / "disney_summary.csv", index=False, float_format="%.6f")
    out = pd.concat(tabs)
    out.to_csv(OUT / "disney_linear.csv", index=False, float_format="%.6f")
    print("\nDisney+, straight-line demand:")
    print(out.round(2).to_string(index=False))
    return out, pd.DataFrame(summary)


def cost_sensitivity(yr, ds):
    rows = []
    g = ds[ds.fiscal_year == ds.fiscal_year.max()].set_index("segment").loc[DISNEY_ORDER]
    cases = {f"Netflix {LATEST_NETFLIX}": (yr.arm_usd.values, yr.members_avg_m.values),
             f"Disney+ FY{int(ds.fiscal_year.max())}": (g.arpu_usd.values, g.subs_avg_m.values)}
    for name, (p, q) in cases.items():
        for c in MC_ALTERNATIVES:
            if c >= p.min():
                print(f"  skip {name} at marginal cost ${c:.2f}: above its lowest price")
                continue
            r = demand.compare(p, q, c, LINEAR)
            rows.append(dict(case=name, marginal_cost=c, uniform_price=r["uniform"],
                             markets_served_at_uniform=int(r["served_uniform"].sum()),
                             subs_change_m=r["total_dq"], welfare_change_musd=r["total_dW"],
                             consumer_surplus_change_musd=r["total_dCS"], profit_change_musd=r["total_dProfit"],
                             varian_lower_musd=r["varian_lower"], varian_upper_musd=r["varian_upper"]))
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "cost_sensitivity.csv", index=False, float_format="%.6f")
    print("\nMarginal-cost sensitivity, straight-line demand:")
    print(out.round(2).to_string(index=False))
    return out


def figure(yr, r):
    p, q = yr.arm_usd.values, yr.members_avg_m.values
    A, B = r["A"], r["B"]
    fig, ax = plt.subplots(figsize=(8, 5.2))
    colors = ["#1f4e79", "#2e86c1", "#c0392b", "#e67e22"]
    for i, code in enumerate(NETFLIX_ORDER):
        qs = np.linspace(0, A[i] / B[i], 200)
        ax.plot(qs, A[i] - B[i] * qs, color=colors[i], lw=1.8, label=NETFLIX_NAMES[code])
        ax.plot(q[i], p[i], "o", color=colors[i], ms=8)
        ax.plot(r["q_uniform"][i], r["uniform"], "s", color=colors[i], ms=7, mfc="white", mew=1.8)
    ax.axhline(r["uniform"], color="0.35", ls="--", lw=1)
    ax.text(245, r["uniform"] + 0.4,
            f"one worldwide price ${r['uniform']:.2f}", ha="right", color="0.25", fontsize=9)
    ax.set_xlim(0, 260)
    ax.set_ylim(0, 36)
    ax.set_xlabel("Average paid memberships in 2024 (millions)")
    ax.set_ylabel("Revenue per membership ($ a month)")
    ax.set_title("Netflix 2024: actual regional prices (dots) and one worldwide price (squares)",
                 fontsize=10.5)
    ax.legend(frameon=False, fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "netflix_demand_2024.png", dpi=150)
    plt.close(fig)


def main():
    OUT.mkdir(exist_ok=True)
    nf, ds = load()
    yr, r, tab = netflix_latest(nf)
    years = netflix_years(nf)
    dis, dsum = disney(ds)
    cost_sensitivity(yr, ds)
    figure(yr, r)

    revenue = float((yr.arm_usd * yr.members_avg_m).sum() * 12)
    latest_d = dsum.iloc[-1]
    head = pd.DataFrame([
        dict(item="Netflix 2024 average paid memberships (M)", value=yr.members_avg_m.sum()),
        dict(item="Netflix 2024 streaming revenue implied by ARM ($M)", value=revenue),
        dict(item="Netflix 2024 price ratio, UCAN to APAC", value=yr.arm_usd.max() / yr.arm_usd.min()),
        dict(item="Netflix 2024 single worldwide price, linear ($/month)", value=r["uniform"]),
        dict(item="Netflix 2024 members change from discrimination, linear (M)", value=r["total_dq"]),
        dict(item="Netflix 2024 total surplus change from discrimination, linear ($M/yr)", value=r["total_dW"]),
        dict(item="Netflix 2024 total surplus change as % of revenue", value=100 * r["total_dW"] / revenue),
        dict(item="Netflix 2024 consumer surplus change, linear ($M/yr)", value=r["total_dCS"]),
        dict(item="Netflix 2024 profit change, linear ($M/yr)", value=r["total_dProfit"]),
        dict(item="Netflix 2024 Varian lower bound ($M/yr)", value=r["varian_lower"]),
        dict(item="Netflix 2024 Varian upper bound ($M/yr)", value=r["varian_upper"]),
        dict(item=f"Disney+ FY{int(latest_d.fiscal_year)} single price, linear ($/month)", value=latest_d.uniform),
        dict(item=f"Disney+ FY{int(latest_d.fiscal_year)} subscribers change from discrimination (M)", value=latest_d.dq),
        dict(item=f"Disney+ FY{int(latest_d.fiscal_year)} total surplus change, linear ($M/yr)", value=latest_d.dW),
        dict(item=f"Disney+ FY{int(latest_d.fiscal_year)} Varian lower bound ($M/yr)", value=latest_d.lower),
        dict(item=f"Disney+ FY{int(latest_d.fiscal_year)} Varian upper bound ($M/yr)", value=latest_d.upper),
        dict(item="Netflix 2024 members priced out in UCAN and EMEA by discrimination (M)",
             value=-tab.subs_change_m[tab.subs_change_m < 0].sum()),
        dict(item="Netflix 2024 members priced in in LATAM and APAC by discrimination (M)",
             value=tab.subs_change_m[tab.subs_change_m > 0].sum()),
        dict(item="Netflix 2024 consumer surplus gain in LATAM and APAC, linear ($M/yr)",
             value=tab.consumer_surplus_change_musd[tab.consumer_surplus_change_musd > 0].sum()),
        dict(item="Netflix UCAN price change 2017 to 2024 (%)",
             value=100 * (years.price_UCAN.iloc[-1] / years.price_UCAN.iloc[0] - 1)),
        dict(item="Netflix years in which a single price would drop a region (linear)",
             value=int((years.regions_served_at_uniform < 4).sum())),
    ])
    head.to_csv(OUT / "headline.csv", index=False, float_format="%.6f")
    print("\nHeadline numbers:")
    print(head.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
