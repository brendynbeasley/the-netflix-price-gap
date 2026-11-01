# Schmalensee (1981) on streaming prices: findings

## In plain English

Richard Schmalensee showed in 1981 that when a seller charges different groups different prices, the world as a
whole can come out ahead only if more people end up buying. This study applies his test to the regional prices
Netflix and Disney report in their annual 10-K filings.

- **Netflix's regional prices do not add subscribers on the textbook assumption.** If demand in each region is a
  straight line, a single worldwide Netflix price of $10.49 a month in 2024 would keep every region subscribing
  and leave the total of 277.7 million average memberships unchanged. The price gap then moves about 38 million
  memberships from the US-Canada and European regions to Latin America and Asia-Pacific and costs the world
  $2.02 billion a year, 5.2% of Netflix's streaming revenue. American and Canadian subscribers lose $8.13 billion.
- **The cost has grown with the gap.** Netflix's highest regional average was 1.23 times its lowest in 2017 and
  2.36 times in 2024, and the straight-line loss rose from 0.3% to 5.2% of revenue.
- **Disney+ Hotstar is the opposite case.** Disney+ Hotstar subscribers in India and parts of Southeast Asia paid
  96 cents a month in fiscal 2024, against $7.89 in the United States and Canada. At Disney's best single price of
  $7.10 the Hotstar market would close, so pricing by market keeps 36.75 million subscribers and raises welfare,
  with Varian's lower bound positive at $118 million a year.
- **For Netflix, the answer turns on the shape of demand.** Following Aguirre, Cowan and Vickers (2010), when
  regional demand is about as convex as an exponential curve or more, Netflix's price gap adds subscribers and
  raises welfare. The break-even is at a pass-through of 0.96.

A friendlier tour is in the [README](../README.md); method details are in [TECHNICAL.md](../TECHNICAL.md).

## Key to the labels

- *price_actual*, *p*: reported average monthly revenue per paying member (Netflix ARM, Disney ARPU), US dollars.
- *subs_actual_m*, *members_avg_m*: average paying members during the year, millions (Netflix reports it; for
  Disney, the mean of the two fiscal-year-end counts).
- *price_uniform*, *uniform_price*: the single price that maximizes total profit across all markets.
- *subs_uniform_m*: members each market would have at that single price. *served_at_uniform* is False when the
  market's demand reaches zero below the single price.
- *subs_change_m*: members under discrimination minus members at the single price.
- *consumer_surplus_change_musd*, *profit_change_musd*, *welfare_change_musd*: discrimination minus single price, in
  millions of dollars a year. Welfare is consumer surplus plus profit.
- *varian_lower_musd*, *varian_upper_musd*: Varian's (1985) bounds on the welfare change.
- *choke_price*: price at which the fitted straight-line demand reaches zero (2p − c).
- *triangle_musd*: half the price gap times the change in members, per year; with straight lines these sum to the
  welfare loss.
- *d*: curvature parameter of inverse demand p = A − B q^d (1 is a straight line, 0 exponential, negative more
  convex). *curvature* is 1 − d; *pass_through* is 1/(1 + d).
- Netflix regions: UCAN (US and Canada), EMEA (Europe, Middle East and Africa), LATAM (Latin America), APAC
  (Asia-Pacific). Disney segments: Domestic (US and Canada), International (excluding Hotstar), Hotstar.
- All runs use a marginal cost of $0.50 a month per member except in cost_sensitivity.csv.

## Every table

### netflix_2024_linear.csv

| market | price_actual | subs_actual_m | price_uniform | subs_uniform_m | served_at_uniform | subs_change_m | consumer_surplus_change_musd | profit_change_musd | welfare_change_musd | choke_price | price_gap | triangle_musd |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| US and Canada | 17.20 | 84.11 | 10.49 | 117.91 | True | -33.79 | -8,132.60 | 2,720.83 | -5,411.77 | 33.90 | 6.71 | 1,360.42 |
| Europe, Middle East and Africa | 10.96 | 94.20 | 10.49 | 98.43 | True | -4.23 | -542.63 | 23.82 | -518.80 | 21.42 | 0.47 | 11.91 |
| Latin America | 8.24 | 48.95 | 10.49 | 34.72 | True | 14.23 | 1,129.85 | 384.41 | 1,514.26 | 15.98 | -2.25 | 192.20 |
| Asia-Pacific | 7.29 | 50.47 | 10.49 | 26.68 | True | 23.79 | 1,481.41 | 913.58 | 2,394.99 | 14.08 | -3.20 | 456.79 |

### netflix_by_year.csv

| fiscal_year | members_avg_m | revenue_musd | price_UCAN | price_EMEA | price_LATAM | price_APAC | ratio_high_to_low | uniform_price | regions_served_at_uniform | members_change_m | welfare_change_musd | welfare_change_pct_revenue | consumer_surplus_change_musd | profit_change_musd | ucan_share_of_members |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2017 | 99.32 | 11,240.91 | 9.97 | 9.17 | 8.09 | 9.11 | 1.232 | 9.37 | 4 | 0.00 | -35.45 | -0.32 | -106.35 | 70.90 | 0.560 |
| 2018 | 124.66 | 15,428.20 | 11.16 | 10.45 | 8.19 | 9.33 | 1.363 | 10.17 | 4 | 0.00 | -109.30 | -0.71 | -327.90 | 218.60 | 0.496 |
| 2019 | 152.98 | 19,858.97 | 12.57 | 10.33 | 8.21 | 9.24 | 1.531 | 10.52 | 4 | 0.00 | -272.94 | -1.37 | -818.83 | 545.89 | 0.435 |
| 2020 | 189.09 | 24,759.40 | 13.32 | 10.72 | 7.45 | 9.12 | 1.788 | 10.40 | 4 | 0.00 | -579.61 | -2.34 | -1,738.83 | 1,159.22 | 0.379 |
| 2021 | 210.79 | 29,515.17 | 14.56 | 11.63 | 7.73 | 9.56 | 1.884 | 11.04 | 4 | 0.00 | -797.56 | -2.70 | -2,392.67 | 1,595.11 | 0.352 |
| 2022 | 222.92 | 31,472.67 | 15.86 | 10.99 | 8.48 | 8.50 | 1.870 | 10.99 | 4 | 0.00 | -1,037.89 | -3.30 | -3,113.68 | 2,075.79 | 0.332 |
| 2023 | 240.89 | 33,638.11 | 16.28 | 10.87 | 8.66 | 7.64 | 2.131 | 10.70 | 4 | 0.00 | -1,356.45 | -4.03 | -4,069.35 | 2,712.90 | 0.316 |
| 2024 | 277.73 | 39,005.24 | 17.20 | 10.96 | 8.24 | 7.29 | 2.359 | 10.49 | 4 | 0.00 | -2,021.32 | -5.18 | -6,063.97 | 4,042.64 | 0.303 |

### disney_linear.csv

| fiscal_year | market | price_actual | subs_actual_m | price_uniform | subs_uniform_m | served_at_uniform | subs_change_m | consumer_surplus_change_musd | profit_change_musd | welfare_change_musd | choke_price |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2022 | Disney+ US and Canada | 6.34 | 42.60 | 6.21 | 43.53 | True | -0.93 | -65.86 | 1.42 | -64.44 | 12.18 |
| 2022 | Disney+ International (excl. Hotstar) | 6.10 | 46.25 | 6.21 | 45.32 | True | 0.93 | 61.84 | 1.26 | 63.10 | 11.70 |
| 2022 | Disney+ Hotstar | 0.88 | 52.30 | 6.21 | 0.00 | False | 52.30 | 119.24 | 238.49 | 357.73 | 1.26 |
| 2023 | Disney+ US and Canada | 6.97 | 46.45 | 6.33 | 51.01 | True | -4.56 | -371.76 | 34.82 | -336.94 | 13.44 |
| 2023 | Disney+ International (excl. Hotstar) | 5.93 | 61.30 | 6.33 | 56.74 | True | 4.56 | 286.32 | 22.14 | 308.46 | 11.36 |
| 2023 | Disney+ Hotstar | 0.66 | 49.45 | 6.33 | 0.00 | False | 49.45 | 47.47 | 94.94 | 142.42 | 0.82 |
| 2024 | Disney+ US and Canada | 7.89 | 51.25 | 7.10 | 56.71 | True | -5.46 | -510.44 | 51.67 | -458.77 | 15.28 |
| 2024 | Disney+ International (excl. Hotstar) | 6.60 | 66.40 | 7.10 | 60.94 | True | 5.46 | 383.55 | 32.92 | 416.47 | 12.70 |
| 2024 | Disney+ Hotstar | 0.96 | 36.75 | 7.10 | 0.00 | False | 36.75 | 101.43 | 202.86 | 304.29 | 1.42 |

### disney_summary.csv

| fiscal_year | uniform_price | subs_change_m | welfare_change_musd | consumer_surplus_change_musd | profit_change_musd | varian_lower_musd | varian_upper_musd |
|---|---|---|---|---|---|---|---|
| 2022 | 6.21 | 52.30 | 356.39 | 115.23 | 241.17 | 235.81 | 3,585.20 |
| 2023 | 6.33 | 49.45 | 113.94 | -37.97 | 151.90 | 37.99 | 3,462.06 |
| 2024 | 7.10 | 36.75 | 261.99 | -25.46 | 287.45 | 118.27 | 2,911.49 |

### cost_sensitivity.csv

| case | marginal_cost | uniform_price | markets_served_at_uniform | subs_change_m | welfare_change_musd | consumer_surplus_change_musd | profit_change_musd | varian_lower_musd | varian_upper_musd |
|---|---|---|---|---|---|---|---|---|---|
| Netflix 2024 | 0.00 | 10.54 | 4 | 0.00 | -1,937.84 | -5,813.53 | 3,875.68 | -3,875.68 | 0.00 |
| Netflix 2024 | 0.50 | 10.49 | 4 | 0.00 | -2,021.32 | -6,063.97 | 4,042.64 | -4,042.64 | 0.00 |
| Netflix 2024 | 1.00 | 10.44 | 4 | 0.00 | -2,112.96 | -6,338.88 | 4,225.92 | -4,225.92 | 0.00 |
| Netflix 2024 | 2.00 | 10.31 | 4 | 0.00 | -2,326.56 | -6,979.69 | 4,653.13 | -4,653.13 | 0.00 |
| Disney+ FY2024 | 0.00 | 7.11 | 2 | 36.75 | 595.63 | 93.45 | 502.18 | 344.54 | 3,133.80 |
| Disney+ FY2024 | 0.50 | 7.10 | 2 | 36.75 | 261.99 | -25.46 | 287.45 | 118.27 | 2,911.49 |

### headline.csv

| item | value |
|---|---|
| Netflix 2024 average paid memberships (M) | 277.732 |
| Netflix 2024 streaming revenue implied by ARM ($M) | 39,005.238 |
| Netflix 2024 price ratio, UCAN to APAC | 2.359 |
| Netflix 2024 single worldwide price, linear ($/month) | 10.491 |
| Netflix 2024 members change from discrimination, linear (M) | 0.000 |
| Netflix 2024 total surplus change from discrimination, linear ($M/yr) | -2,021.322 |
| Netflix 2024 total surplus change as % of revenue | -5.182 |
| Netflix 2024 consumer surplus change, linear ($M/yr) | -6,063.965 |
| Netflix 2024 profit change, linear ($M/yr) | 4,042.644 |
| Netflix 2024 Varian lower bound ($M/yr) | -4,042.644 |
| Netflix 2024 Varian upper bound ($M/yr) | 0.000 |
| Disney+ FY2024 single price, linear ($/month) | 7.102 |
| Disney+ FY2024 subscribers change from discrimination (M) | 36.750 |
| Disney+ FY2024 total surplus change, linear ($M/yr) | 261.994 |
| Disney+ FY2024 Varian lower bound ($M/yr) | 118.267 |
| Disney+ FY2024 Varian upper bound ($M/yr) | 2,911.492 |
| Netflix 2024 members priced out in UCAN and EMEA by discrimination (M) | 38.021 |
| Netflix 2024 members priced in in LATAM and APAC by discrimination (M) | 38.021 |
| Netflix 2024 consumer surplus gain in LATAM and APAC, linear ($M/yr) | 2,611.263 |
| Netflix UCAN price change 2017 to 2024 (%) | 72.518 |
| Netflix years in which a single price would drop a region (linear) | 0.000 |

### curvature_breakeven.csv

| case | d_breakeven | curvature_breakeven | pass_through_breakeven | note |
|---|---|---|---|---|
| Netflix 2024 | 0.043 | 0.957 | 0.958 | discrimination raises total surplus when demand is more convex than this |
| Disney+ FY2024 |  |  |  | total surplus change has the same sign across the whole grid |

### curvature_mixed.csv

| case | d_high_price_markets | d_low_price_markets | uniform_price | markets_served_at_uniform | subs_change_m | welfare_change_musd | varian_lower_musd | varian_upper_musd |
|---|---|---|---|---|---|---|---|---|
| Netflix 2024 | 0.5 | 0.5 | 11.10 | 4 | 8.45 | -997.33 | -3,058.21 | 1,074.59 |
| Netflix 2024 | 0.5 | 1.0 | 10.32 | 4 | -8.26 | -3,098.22 | -5,320.61 | -974.07 |
| Netflix 2024 | 0.5 | 2.0 | 9.34 | 4 | -33.27 | -5,949.06 | -8,557.86 | -3,527.99 |
| Netflix 2024 | 1.0 | 0.5 | 11.26 | 4 | 15.25 | -60.45 | -1,998.68 | 1,968.87 |
| Netflix 2024 | 1.0 | 1.0 | 10.49 | 4 | 0.00 | -2,021.32 | -4,042.64 | 0.00 |
| Netflix 2024 | 1.0 | 2.0 | 9.43 | 4 | -24.86 | -4,904.82 | -7,190.51 | -2,664.14 |
| Netflix 2024 | 2.0 | 0.5 | 11.38 | 4 | 22.10 | 927.48 | -852.47 | 2,885.45 |
| Netflix 2024 | 2.0 | 1.0 | 10.68 | 4 | 9.98 | -676.71 | -2,467.15 | 1,218.95 |
| Netflix 2024 | 2.0 | 2.0 | 9.55 | 4 | -13.93 | -3,511.57 | -5,403.06 | -1,512.54 |
| Disney+ FY2024 | 0.5 | 0.5 | 7.13 | 2 | 37.01 | 316.34 | 138.42 | 2,945.18 |
| Disney+ FY2024 | 0.5 | 1.0 | 7.13 | 2 | 37.01 | 282.53 | 138.42 | 2,945.18 |
| Disney+ FY2024 | 0.5 | 2.0 | 7.13 | 2 | 37.01 | 248.72 | 138.42 | 2,945.18 |
| Disney+ FY2024 | 1.0 | 0.5 | 7.10 | 2 | 36.75 | 295.80 | 118.27 | 2,911.49 |
| Disney+ FY2024 | 1.0 | 1.0 | 7.10 | 2 | 36.75 | 261.99 | 118.27 | 2,911.49 |
| Disney+ FY2024 | 1.0 | 2.0 | 7.10 | 2 | 36.75 | 228.18 | 118.27 | 2,911.49 |
| Disney+ FY2024 | 2.0 | 0.5 | 7.05 | 2 | 36.27 | 258.50 | 81.95 | 2,849.75 |
| Disney+ FY2024 | 2.0 | 1.0 | 7.05 | 2 | 36.27 | 224.69 | 81.95 | 2,849.75 |
| Disney+ FY2024 | 2.0 | 2.0 | 7.05 | 2 | 36.27 | 190.88 | 81.95 | 2,849.75 |

### curvature_scan.csv (main columns; the file also has percentages, consumer surplus and profit)

| case | d | curvature | pass_through | uniform_price | markets_served_at_uniform | subs_change_m | welfare_change_musd | varian_lower_musd | varian_upper_musd |
|---|---|---|---|---|---|---|---|---|---|
| Netflix 2024 | -0.80 | 1.80 | 5.00 | 12.80 | 4 | 27.58 | 1,702.77 | -350.28 | 4,072.26 |
| Netflix 2024 | -0.75 | 1.75 | 4.00 | 12.74 | 4 | 27.03 | 1,614.05 | -442.51 | 3,969.96 |
| Netflix 2024 | -0.70 | 1.70 | 3.33 | 12.68 | 4 | 26.45 | 1,523.34 | -536.48 | 3,865.62 |
| Netflix 2024 | -0.65 | 1.65 | 2.86 | 12.61 | 4 | 25.86 | 1,430.71 | -632.13 | 3,759.36 |
| Netflix 2024 | -0.60 | 1.60 | 2.50 | 12.55 | 4 | 25.25 | 1,336.24 | -729.36 | 3,651.27 |
| Netflix 2024 | -0.55 | 1.55 | 2.22 | 12.49 | 4 | 24.62 | 1,240.02 | -828.09 | 3,541.47 |
| Netflix 2024 | -0.50 | 1.50 | 2.00 | 12.42 | 4 | 23.98 | 1,142.12 | -928.23 | 3,430.07 |
| Netflix 2024 | -0.45 | 1.45 | 1.82 | 12.36 | 4 | 23.31 | 1,042.66 | -1,029.68 | 3,317.21 |
| Netflix 2024 | -0.40 | 1.40 | 1.67 | 12.29 | 4 | 22.64 | 941.72 | -1,132.33 | 3,203.02 |
| Netflix 2024 | -0.35 | 1.35 | 1.54 | 12.23 | 4 | 21.94 | 839.43 | -1,236.07 | 3,087.64 |
| Netflix 2024 | -0.30 | 1.30 | 1.43 | 12.16 | 4 | 21.24 | 735.89 | -1,340.80 | 2,971.19 |
| Netflix 2024 | -0.25 | 1.25 | 1.33 | 12.09 | 4 | 20.52 | 631.20 | -1,446.40 | 2,853.82 |
| Netflix 2024 | -0.20 | 1.20 | 1.25 | 12.03 | 4 | 19.78 | 525.49 | -1,552.76 | 2,735.67 |
| Netflix 2024 | -0.15 | 1.15 | 1.18 | 11.96 | 4 | 19.03 | 418.88 | -1,659.77 | 2,616.87 |
| Netflix 2024 | -0.10 | 1.10 | 1.11 | 11.89 | 4 | 18.27 | 311.47 | -1,767.31 | 2,497.58 |
| Netflix 2024 | -0.05 | 1.05 | 1.05 | 11.82 | 4 | 17.50 | 203.38 | -1,875.26 | 2,377.92 |
| Netflix 2024 | 0.00 | 1.00 | 1.00 | 11.76 | 4 | 16.72 | 94.74 | -1,983.51 | 2,258.03 |
| Netflix 2024 | 0.05 | 0.95 | 0.95 | 11.69 | 4 | 15.92 | -14.35 | -2,091.96 | 2,138.05 |
| Netflix 2024 | 0.10 | 0.90 | 0.91 | 11.62 | 4 | 15.12 | -123.76 | -2,200.47 | 2,018.10 |
| Netflix 2024 | 0.15 | 0.85 | 0.87 | 11.56 | 4 | 14.31 | -233.39 | -2,308.96 | 1,898.31 |
| Netflix 2024 | 0.20 | 0.80 | 0.83 | 11.49 | 4 | 13.49 | -343.12 | -2,417.30 | 1,778.81 |
| Netflix 2024 | 0.25 | 0.75 | 0.80 | 11.42 | 4 | 12.66 | -452.84 | -2,525.39 | 1,659.72 |
| Netflix 2024 | 0.30 | 0.70 | 0.77 | 11.36 | 4 | 11.83 | -562.43 | -2,633.11 | 1,541.17 |
| Netflix 2024 | 0.35 | 0.65 | 0.74 | 11.29 | 4 | 10.99 | -671.79 | -2,740.36 | 1,423.26 |
| Netflix 2024 | 0.40 | 0.60 | 0.71 | 11.23 | 4 | 10.15 | -780.80 | -2,847.04 | 1,306.12 |
| Netflix 2024 | 0.45 | 0.55 | 0.69 | 11.16 | 4 | 9.30 | -889.35 | -2,953.02 | 1,189.86 |
| Netflix 2024 | 0.50 | 0.50 | 0.67 | 11.10 | 4 | 8.45 | -997.33 | -3,058.21 | 1,074.59 |
| Netflix 2024 | 0.55 | 0.45 | 0.65 | 11.03 | 4 | 7.60 | -1,104.63 | -3,162.50 | 960.43 |
| Netflix 2024 | 0.60 | 0.40 | 0.62 | 10.97 | 4 | 6.74 | -1,211.13 | -3,265.76 | 847.48 |
| Netflix 2024 | 0.65 | 0.35 | 0.61 | 10.91 | 4 | 5.89 | -1,316.72 | -3,367.91 | 735.86 |
| Netflix 2024 | 0.70 | 0.30 | 0.59 | 10.85 | 4 | 5.04 | -1,421.29 | -3,468.83 | 625.66 |
| Netflix 2024 | 0.75 | 0.25 | 0.57 | 10.79 | 4 | 4.19 | -1,524.74 | -3,568.41 | 517.00 |
| Netflix 2024 | 0.80 | 0.20 | 0.56 | 10.72 | 4 | 3.34 | -1,626.95 | -3,666.54 | 409.97 |
| Netflix 2024 | 0.85 | 0.15 | 0.54 | 10.67 | 4 | 2.50 | -1,727.81 | -3,763.13 | 304.66 |
| Netflix 2024 | 0.90 | 0.10 | 0.53 | 10.61 | 4 | 1.66 | -1,827.23 | -3,858.08 | 201.17 |
| Netflix 2024 | 0.95 | 0.05 | 0.51 | 10.55 | 4 | 0.83 | -1,925.10 | -3,951.28 | 99.59 |
| Netflix 2024 | 1.00 | 0.00 | 0.50 | 10.49 | 4 | 0.00 | -2,021.32 | -4,042.64 | 0.00 |
| Netflix 2024 | 1.10 | -0.10 | 0.48 | 10.38 | 4 | -1.63 | -2,208.48 | -4,219.53 | -192.93 |
| Netflix 2024 | 1.20 | -0.20 | 0.45 | 10.27 | 4 | -3.22 | -2,388.06 | -4,388.11 | -377.09 |
| Netflix 2024 | 1.30 | -0.30 | 0.43 | 10.17 | 4 | -4.76 | -2,559.50 | -4,547.88 | -552.09 |
| Netflix 2024 | 1.40 | -0.40 | 0.42 | 10.07 | 4 | -6.25 | -2,722.37 | -4,698.46 | -717.65 |
| Netflix 2024 | 1.50 | -0.50 | 0.40 | 9.97 | 4 | -7.69 | -2,876.39 | -4,839.58 | -873.63 |
| Netflix 2024 | 1.60 | -0.60 | 0.38 | 9.88 | 4 | -9.07 | -3,021.38 | -4,971.13 | -1,020.00 |
| Netflix 2024 | 1.70 | -0.70 | 0.37 | 9.79 | 4 | -10.38 | -3,157.29 | -5,093.09 | -1,156.84 |
| Netflix 2024 | 1.80 | -0.80 | 0.36 | 9.70 | 4 | -11.63 | -3,284.18 | -5,205.59 | -1,284.36 |
| Netflix 2024 | 1.90 | -0.90 | 0.34 | 9.62 | 4 | -12.81 | -3,402.19 | -5,308.82 | -1,402.82 |
| Netflix 2024 | 2.00 | -1.00 | 0.33 | 9.55 | 4 | -13.93 | -3,511.57 | -5,403.06 | -1,512.54 |
| Netflix 2024 | 2.10 | -1.10 | 0.32 | 9.47 | 4 | -14.99 | -3,612.61 | -5,488.66 | -1,613.92 |
| Netflix 2024 | 2.20 | -1.20 | 0.31 | 9.40 | 4 | -15.98 | -3,705.65 | -5,566.00 | -1,707.38 |
| Netflix 2024 | 2.30 | -1.30 | 0.30 | 9.34 | 4 | -16.91 | -3,791.06 | -5,635.51 | -1,793.34 |
| Netflix 2024 | 2.40 | -1.40 | 0.29 | 9.28 | 4 | -17.78 | -3,869.25 | -5,697.63 | -1,872.26 |
| Netflix 2024 | 2.50 | -1.50 | 0.29 | 9.22 | 4 | -18.59 | -3,940.62 | -5,752.79 | -1,944.58 |
| Netflix 2024 | 2.60 | -1.60 | 0.28 | 9.16 | 4 | -19.35 | -4,005.59 | -5,801.46 | -2,010.74 |
| Netflix 2024 | 2.70 | -1.70 | 0.27 | 9.11 | 4 | -20.05 | -4,064.55 | -5,844.07 | -2,071.16 |
| Netflix 2024 | 2.80 | -1.80 | 0.26 | 9.06 | 4 | -20.71 | -4,117.90 | -5,881.04 | -2,126.25 |
| Netflix 2024 | 2.90 | -1.90 | 0.26 | 9.01 | 4 | -21.32 | -4,166.03 | -5,912.79 | -2,176.41 |
| Netflix 2024 | 3.00 | -2.00 | 0.25 | 8.96 | 4 | -21.89 | -4,209.30 | -5,939.71 | -2,222.00 |
| Disney+ FY2024 | -0.80 | 1.80 | 5.00 | 7.10 | 3 | 34.09 | 414.65 | 29.94 | 2,700.92 |
| Disney+ FY2024 | -0.75 | 1.75 | 4.00 | 7.11 | 3 | 34.39 | 419.47 | 38.87 | 2,726.20 |
| Disney+ FY2024 | -0.70 | 1.70 | 3.33 | 7.11 | 3 | 34.69 | 424.31 | 48.38 | 2,751.73 |
| Disney+ FY2024 | -0.65 | 1.65 | 2.86 | 7.11 | 3 | 34.99 | 429.10 | 58.43 | 2,777.39 |
| Disney+ FY2024 | -0.60 | 1.60 | 2.50 | 7.12 | 3 | 35.29 | 433.74 | 68.99 | 2,803.03 |
| Disney+ FY2024 | -0.55 | 1.55 | 2.22 | 7.13 | 3 | 35.58 | 438.12 | 79.97 | 2,828.45 |
| Disney+ FY2024 | -0.50 | 1.50 | 2.00 | 7.13 | 3 | 35.86 | 442.08 | 91.26 | 2,853.39 |
| Disney+ FY2024 | -0.45 | 1.45 | 1.82 | 7.14 | 3 | 36.13 | 445.44 | 102.71 | 2,877.52 |
| Disney+ FY2024 | -0.40 | 1.40 | 1.67 | 7.14 | 3 | 36.38 | 447.96 | 114.09 | 2,900.45 |
| Disney+ FY2024 | -0.35 | 1.35 | 1.54 | 7.15 | 3 | 36.62 | 449.36 | 125.13 | 2,921.71 |
| Disney+ FY2024 | -0.30 | 1.30 | 1.43 | 7.15 | 3 | 36.83 | 449.31 | 135.46 | 2,940.72 |
| Disney+ FY2024 | -0.25 | 1.25 | 1.33 | 7.16 | 3 | 37.00 | 447.47 | 144.64 | 2,956.87 |
| Disney+ FY2024 | -0.20 | 1.20 | 1.25 | 7.16 | 3 | 37.14 | 443.48 | 152.17 | 2,969.50 |
| Disney+ FY2024 | -0.15 | 1.15 | 1.18 | 7.16 | 3 | 37.24 | 437.08 | 157.55 | 2,978.07 |
| Disney+ FY2024 | -0.10 | 1.10 | 1.11 | 7.17 | 3 | 37.29 | 428.21 | 160.44 | 2,982.30 |
| Disney+ FY2024 | -0.05 | 1.05 | 1.05 | 7.16 | 3 | 37.30 | 417.28 | 160.86 | 2,982.57 |
| Disney+ FY2024 | 0.00 | 1.00 | 1.00 | 7.16 | 3 | 37.28 | 405.28 | 159.46 | 2,980.09 |
| Disney+ FY2024 | 0.05 | 0.95 | 0.95 | 7.16 | 3 | 37.25 | 393.51 | 157.38 | 2,976.62 |
| Disney+ FY2024 | 0.10 | 0.90 | 0.91 | 7.16 | 2 | 37.23 | 382.57 | 155.24 | 2,973.09 |
| Disney+ FY2024 | 0.15 | 0.85 | 0.87 | 7.15 | 2 | 37.20 | 372.40 | 153.11 | 2,969.56 |
| Disney+ FY2024 | 0.20 | 0.80 | 0.83 | 7.15 | 2 | 37.17 | 362.90 | 150.99 | 2,966.05 |
| Disney+ FY2024 | 0.25 | 0.75 | 0.80 | 7.15 | 2 | 37.15 | 353.99 | 148.88 | 2,962.54 |
| Disney+ FY2024 | 0.30 | 0.70 | 0.77 | 7.14 | 2 | 37.12 | 345.62 | 146.77 | 2,959.05 |
| Disney+ FY2024 | 0.35 | 0.65 | 0.74 | 7.14 | 2 | 37.09 | 337.71 | 144.67 | 2,955.56 |
| Disney+ FY2024 | 0.40 | 0.60 | 0.71 | 7.14 | 2 | 37.06 | 330.22 | 142.58 | 2,952.09 |
| Disney+ FY2024 | 0.45 | 0.55 | 0.69 | 7.13 | 2 | 37.04 | 323.11 | 140.50 | 2,948.63 |
| Disney+ FY2024 | 0.50 | 0.50 | 0.67 | 7.13 | 2 | 37.01 | 316.34 | 138.42 | 2,945.18 |
| Disney+ FY2024 | 0.55 | 0.45 | 0.65 | 7.13 | 2 | 36.98 | 309.88 | 136.36 | 2,941.74 |
| Disney+ FY2024 | 0.60 | 0.40 | 0.62 | 7.13 | 2 | 36.96 | 303.70 | 134.31 | 2,938.32 |
| Disney+ FY2024 | 0.65 | 0.35 | 0.61 | 7.12 | 2 | 36.93 | 297.78 | 132.26 | 2,934.91 |
| Disney+ FY2024 | 0.70 | 0.30 | 0.59 | 7.12 | 2 | 36.91 | 292.09 | 130.23 | 2,931.52 |
| Disney+ FY2024 | 0.75 | 0.25 | 0.57 | 7.12 | 2 | 36.88 | 286.62 | 128.21 | 2,928.14 |
| Disney+ FY2024 | 0.80 | 0.20 | 0.56 | 7.11 | 2 | 36.85 | 281.35 | 126.20 | 2,924.78 |
| Disney+ FY2024 | 0.85 | 0.15 | 0.54 | 7.11 | 2 | 36.83 | 276.27 | 124.20 | 2,921.43 |
| Disney+ FY2024 | 0.90 | 0.10 | 0.53 | 7.11 | 2 | 36.80 | 271.35 | 122.21 | 2,918.10 |
| Disney+ FY2024 | 0.95 | 0.05 | 0.51 | 7.10 | 2 | 36.78 | 266.60 | 120.23 | 2,914.79 |
| Disney+ FY2024 | 1.00 | 0.00 | 0.50 | 7.10 | 2 | 36.75 | 261.99 | 118.27 | 2,911.49 |
| Disney+ FY2024 | 1.10 | -0.10 | 0.48 | 7.10 | 2 | 36.70 | 253.19 | 114.38 | 2,904.96 |
| Disney+ FY2024 | 1.20 | -0.20 | 0.45 | 7.09 | 2 | 36.65 | 244.87 | 110.54 | 2,898.49 |
| Disney+ FY2024 | 1.30 | -0.30 | 0.43 | 7.09 | 2 | 36.60 | 236.99 | 106.76 | 2,892.11 |
| Disney+ FY2024 | 1.40 | -0.40 | 0.42 | 7.08 | 2 | 36.55 | 229.50 | 103.03 | 2,885.80 |
| Disney+ FY2024 | 1.50 | -0.50 | 0.40 | 7.07 | 2 | 36.50 | 222.35 | 99.37 | 2,879.57 |
| Disney+ FY2024 | 1.60 | -0.60 | 0.38 | 7.07 | 2 | 36.45 | 215.52 | 95.76 | 2,873.43 |
| Disney+ FY2024 | 1.70 | -0.70 | 0.37 | 7.06 | 2 | 36.41 | 208.98 | 92.21 | 2,867.38 |
| Disney+ FY2024 | 1.80 | -0.80 | 0.36 | 7.06 | 2 | 36.36 | 202.71 | 88.73 | 2,861.41 |
| Disney+ FY2024 | 1.90 | -0.90 | 0.34 | 7.05 | 2 | 36.32 | 196.68 | 85.30 | 2,855.54 |
| Disney+ FY2024 | 2.00 | -1.00 | 0.33 | 7.05 | 2 | 36.27 | 190.88 | 81.95 | 2,849.75 |
| Disney+ FY2024 | 2.10 | -1.10 | 0.32 | 7.04 | 2 | 36.23 | 185.30 | 78.65 | 2,844.05 |
| Disney+ FY2024 | 2.20 | -1.20 | 0.31 | 7.04 | 2 | 36.18 | 179.91 | 75.42 | 2,838.45 |
| Disney+ FY2024 | 2.30 | -1.30 | 0.30 | 7.03 | 2 | 36.14 | 174.71 | 72.26 | 2,832.94 |
| Disney+ FY2024 | 2.40 | -1.40 | 0.29 | 7.03 | 2 | 36.10 | 169.69 | 69.17 | 2,827.53 |
| Disney+ FY2024 | 2.50 | -1.50 | 0.29 | 7.02 | 2 | 36.06 | 164.83 | 66.13 | 2,822.21 |
| Disney+ FY2024 | 2.60 | -1.60 | 0.28 | 7.02 | 2 | 36.02 | 160.14 | 63.17 | 2,816.98 |
| Disney+ FY2024 | 2.70 | -1.70 | 0.27 | 7.01 | 2 | 35.98 | 155.59 | 60.27 | 2,811.85 |
| Disney+ FY2024 | 2.80 | -1.80 | 0.26 | 7.01 | 2 | 35.94 | 151.19 | 57.44 | 2,806.81 |
| Disney+ FY2024 | 2.90 | -1.90 | 0.26 | 7.00 | 2 | 35.90 | 146.93 | 54.67 | 2,801.86 |
| Disney+ FY2024 | 3.00 | -2.00 | 0.25 | 7.00 | 2 | 35.86 | 142.80 | 51.97 | 2,797.01 |

## Figures

- `netflix_demand_2024.png`: the four fitted straight-line demand curves for Netflix 2024, the observed regional
  prices (dots) and the quantities at the single price (squares).
- `curvature_scan.png`: change in subscribers (percent) and in welfare ($ billion a year) from discrimination
  against pass-through, Netflix 2024 and Disney+ FY2024.
