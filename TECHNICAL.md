# Technical notes

This is the technical companion to the [README](README.md). It covers the original study, the data, the method,
the full set of results and how to reproduce them. Every table the scripts write is collected in
[results/FINDINGS.md](results/FINDINGS.md).

## The original study

Richard Schmalensee, "Output and Welfare Implications of Monopolistic Third-Degree Price Discrimination,"
*American Economic Review* 71(1), March 1981, pp. 242–247 (earlier as MIT Sloan School Working Paper 1095-80,
January 1980). The paper is theoretical and has no data. As described by Cowan (2007) and Aguirre, Cowan and
Vickers (2010), it takes Robinson's (1933) analysis forward for a monopolist selling in markets with independent
demands at a constant unit cost, showing how demand curvature sets the sign of the output effect and that a rise
in total output is necessary for third-degree discrimination to raise welfare (consumer surplus plus profit);
Varian (1985) proved the necessary condition in full generality. In Pigou's (1920) straight-line case with every
market served, total output is unchanged and welfare falls, so the headline quantity is a change in output of
exactly zero. I could not read the paper's full text (see METHODS_REVIEW.md).

Varian's bounds, for uniform price $`\bar p`$, discriminatory prices $`p_i`$ and constant marginal cost $`c`$:

```math
(\bar p - c)\sum_i \Delta q_i \;\ge\; \Delta W \;\ge\; \sum_i (p_i - c)\,\Delta q_i
```

## Headline results

| Case | Single price | Change in output from discrimination | Change in welfare | Varian bounds |
|---|---|---|---|---|
| Netflix 2024, straight line | $10.49 | 0 | −$2.02 bn/yr | [−$4.04 bn, $0] |
| Netflix 2024, exponential (pass-through 1) | $11.76 | +16.7 M | +$0.09 bn/yr | [−$1.98 bn, $2.26 bn] |
| Disney+ FY2024, straight line | $7.10 | +36.75 M | +$0.26 bn/yr | [$0.12 bn, $2.91 bn] |

- Under straight lines Netflix's loss rises every year, from 0.3% of streaming revenue in 2017 to 5.2% in 2024,
  as the ratio of its highest to lowest regional price rises from 1.23 to 2.36. No region is ever shut out.
- Netflix's welfare change crosses zero at pass-through $`\rho^* = 0.96`$ ($`\delta^* = 0.04`$).
- Disney+ gains in every fiscal year under straight lines and at every curvature tried for FY2024. Under one
  price the Hotstar market closes whenever pass-through is 0.91 or lower; above that, these demand curves never
  reach zero, and the gain stays positive.

## Data

- **Netflix:** Form 10-K for 2019, 2022 and 2024, PDFs from the annual reports page of ir.netflix.net, saved as
  `data/raw/filings/netflix_10k_{2019,2022,2024}.pdf` (not committed). Item 7, "Streaming Revenues," gives for UCAN,
  EMEA, LATAM and APAC the streaming revenue, paid net additions, paid memberships at year end, average paying
  memberships and average monthly revenue per paying membership (ARM), three years per filing. Extracted to
  `data/raw/netflix_regions.csv` (32 region-years, 2017–2024; later filings win where years overlap).
- **Disney:** fiscal 2023 and 2024 annual reports (Form 10-K) from thewaltdisneycompany.com, saved as
  `data/raw/filings/disney_annual_report_{2023,2024}.pdf`. Item 7, Direct-to-Consumer key metrics, gives Disney+
  paid subscribers at fiscal year end and fiscal-year ARPU for Domestic, International (excluding Hotstar) and
  Hotstar. Extracted to `data/raw/disney_plus.csv` (fiscal 2021–2024; 2021 is used only as a starting count).
- **Checks:** ARM × average paying memberships × 12 reproduces each Netflix region's reported revenue within 0.1%.

## Method

Rules fixed before results were computed:

- Price $`p_i`$ is reported revenue per member per month; quantity $`q_i`$ is Netflix's average paying
  memberships, or the mean of Disney's two year-end counts.
- Marginal cost $`c`$ is $0.50 a month in every market, with $0, $1 and $2 as alternatives (a cost above the
  lowest price is skipped, which rules out $1 and $2 for Disney).
- Each observed regional price is the profit-maximizing price for that market.
- Demand comes from the Bulow-Pfleiderer family. The first-order condition $`p_i - c = -q_i\,p_i'(q_i)`$ calibrates
  each market from one point:

```math
\begin{aligned}
p_i(q) &= A_i - B_i\,q^{\delta}, \qquad \rho = \frac{1}{1+\delta} \\
B_i &= \frac{p_i - c}{\delta\,q_i^{\delta}}, \qquad A_i = p_i + \frac{p_i - c}{\delta}
\end{aligned}
```

  with the exponential limit $`p_i(q) = A_i - B_i \ln q`$ at $`\delta = 0`$. The main test uses $`\delta = 1`$.
- The single price maximizes pooled profit over a fine grid and is then refined, so a market can drop out:

```math
\bar p = \arg\max_{P > c}\; (P - c)\sum_i q_i(P), \qquad q_i(P) = \max\Bigl\{\Bigl(\frac{A_i - P}{B_i}\Bigr)^{1/\delta},\, 0\Bigr\}
```

- Welfare in market $`i`$ is $`W_i(q) = \int_0^{q} \bigl(p_i(x) - c\bigr)\,dx`$; consumer surplus is
  $`\int_0^{q} p_i(x)\,dx - p_i(q)\,q`$; all money figures are monthly × 12.
- The curvature grid runs over $`\delta`$ from −0.80 to 3.0 (pass-through 0.25 to 5). The mixed-curvature check
  sets $`\delta`$ separately for high-price markets (Netflix UCAN and EMEA; Disney Domestic and International) and
  low-price markets, each in {0.5, 1, 2}.
- There is no sampling error, since the inputs are company totals. Uncertainty is reported by varying cost and
  curvature.

## Full results

Straight-line demand, marginal cost $0.50, Netflix 2024:

| Region | p | q (M) | q at single price | ΔCS ($M/yr) | Δπ ($M/yr) | ΔW ($M/yr) | Choke price |
|---|---|---|---|---|---|---|---|
| UCAN | 17.20 | 84.11 | 117.91 | −8,133 | +2,721 | −5,412 | 33.90 |
| EMEA | 10.96 | 94.20 | 98.43 | −543 | +24 | −519 | 21.42 |
| LATAM | 8.24 | 48.95 | 34.72 | +1,130 | +384 | +1,514 | 15.98 |
| APAC | 7.29 | 50.47 | 26.68 | +1,481 | +914 | +2,395 | 14.08 |

Marginal-cost sensitivity, Netflix 2024 (single price, ΔW): $0 gives $10.54 and −$1,938M; $0.50 gives $10.49 and
−$2,021M; $1 gives $10.44 and −$2,113M; $2 gives $10.31 and −$2,327M. Disney+ FY2024 at $0 gives $7.11 and
+$596M; at $0.50, $7.10 and +$262M.

Disney+ by year (straight line): FY2022 single price $6.21, +52.3M, ΔW +$356M, bounds [$236M, $3,585M]; FY2023
$6.33, +49.45M, +$114M, [$38M, $3,462M]; FY2024 $7.10, +36.75M, +$262M, [$118M, $2,911M].

Mixed curvature, Netflix 2024 (δ high-price, δ low-price → Δq, ΔW): (2, 0.5) → +22.1M, +$927M; (1, 0.5) →
+15.2M, −$60M; (0.5, 2) → −33.3M, −$5,949M. The full grid and the curvature scan are in
`results/curvature_mixed.csv` and `results/curvature_scan.csv`.

## Reproducing the results

```bash
pip install -r requirements.txt
python src/build_data.py      # downloads the five 10-K PDFs, rewrites data/raw/*.csv
python src/schmalensee.py     # straight-line test, years, Disney+, cost checks, figure 1
python src/curvature.py       # curvature extension, figure 2
```

The first step is optional because the extracted CSVs are committed. Python 3.12 or later.

## Repository layout

| Path | What it is |
|---|---|
| `src/build_data.py` | Downloads the filings and extracts regional prices and subscribers |
| `src/demand.py` | Demand calibration, single-price search, welfare accounting |
| `src/schmalensee.py` | Straight-line test, years, Disney+, cost sensitivity |
| `src/curvature.py` | Aguirre-Cowan-Vickers extension |
| `data/raw/*.csv` | Extracted 10-K figures with source URLs |
| `results/` | Every table and figure |

## References

- Aguirre, I., Cowan, S. & Vickers, J. (2010). Monopoly price discrimination and demand curvature. *AER* 100(4).
- Bulow, J. & Pfleiderer, P. (1983). A note on the effect of cost changes on prices. *JPE* 91(1).
- Cowan, S. (2007). The welfare effects of third-degree price discrimination with non-linear demand functions.
  Oxford Economics Discussion Paper 364.
- Cowan, S. (2013). Welfare-increasing third-degree price discrimination. Oxford Economics Discussion Paper 652.
- Hausman, J. & MacKie-Mason, J. (1988). Price discrimination and patent policy. *RAND Journal of Economics* 19, 253–265.
- Pigou, A. C. (1920). *The Economics of Welfare*. Macmillan.
- Robinson, J. (1933). *The Economics of Imperfect Competition*. Macmillan.
- Schmalensee, R. (1981). Output and welfare implications of monopolistic third-degree price discrimination.
  *AER* 71(1), 242–247.
- Varian, H. R. (1985). Price discrimination and social welfare. *AER* 75(4), 870–875.
