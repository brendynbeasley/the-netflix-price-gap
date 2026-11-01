# Methods review: Schmalensee (1981)

- **Paper:** Schmalensee, Richard. 1981. "Output and Welfare Implications of Monopolistic Third-Degree Price
  Discrimination." *American Economic Review* 71(1): 242–247. Circulated earlier as MIT Sloan School of
  Management Working Paper 1095-80, January 1980.
- **Statistical focus:** the two formal results the paper is cited for. First, that an increase in total output is
  a necessary condition for third-degree discrimination by a monopolist to raise welfare (consumer surplus plus
  profit). Second, the decomposition of the welfare change into a misallocation term and an output term, which
  delivers the classic straight-line case (output unchanged, welfare lower) and shows how the curvature of demand
  sets the sign of the output effect.
- **Review standard:** internal consistency of the formal results, explicitness of assumptions, and the
  testability of the predictions, judged against how theory papers in industrial organization are expected to
  state scope conditions today.
- **What was read:** I could not read the paper's full text. The AER version is behind the JSTOR and AEA paywalls,
  and the free working-paper PDF on MIT's DSpace repository returned repeated HTTP 429 (rate-limit) errors on
  November 1, 2026. I read the IDEAS/RePEc and DSpace catalog records (citation, working-paper number and date) and
  three later papers in full that describe the paper's method and results: Aguirre, Cowan and Vickers (2010),
  *AER* 100(4): 1601–1615 (author-posted copy); Cowan (2007), Oxford Department of Economics Discussion Paper 364;
  and Cowan (2013), Oxford Discussion Paper 652. Everything below about the paper's content is extracted from those
  secondary accounts and is marked as such. I did not read Varian (1985) directly either; its bounds are taken from
  Cowan (2013, equation 1).

## Methods summary

**Research design.** A theoretical comparative-statics analysis of a single-product monopolist that sells in
several separated markets at constant marginal cost. According to Aguirre, Cowan and Vickers (2010, p. 1604), the
method "used by Schmalensee (1981)" starts from the uniform price and relaxes a constraint on the firm's freedom to
discriminate a little at a time, tracking how welfare and total output change along the way. Their equation (3),
written "following Schmalensee (1981)," splits the marginal welfare effect into two misallocation terms, each
non-positive, and an output term, the margin at the uniform price times the marginal change in total output. For
more than two markets the constraint is placed on a weighted sum of price differences, with weights equal to each
market's marginal profitability at the uniform price (ACV 2010, p. 1608, describing "the technique of
Schmalensee (1981)").

**Sampling strategy, sample size, inclusion and exclusion criteria.** Not applicable. The paper has no data. Its
analogue of inclusion criteria is its scope. From the secondary accounts the results apply to a monopolist (no
rivals), independent demands across markets (no cross-price effects), constant marginal cost, no arbitrage
between markets, and, for the straight-line result, every market served at the uniform price.

**Independent and dependent variables.** In theoretical terms, the degree of discrimination allowed (the bound on
price differences) is the variable moved; the outcomes are each market's price and quantity, total output, and
welfare.

**Statistical methods.** None in the empirical sense. The tools are calculus and the envelope and first-order
conditions of the constrained profit problem.

**Reported effect sizes.** None in numerical form. The results are sign conditions. The one exact quantitative
statement is the straight-line case, in which the change in total output is zero.

**Confidence intervals and p-values.** Not applicable; nothing is estimated.

**Missing data treatment.** Not applicable.

**Stated limitations.** I cannot report the limitations as the paper states them, because I did not read its text.
The secondary accounts make clear that the analysis concerns a pure monopolist and markets that are all served;
Cowan (2007, p. 3) notes that the case in which discrimination opens a new market was treated separately by
Hausman and MacKie-Mason (1988).

## Statistics extraction table

| Statistic | Value and unit | Source location | What it measures | What it does not establish |
|---|---|---|---|---|
| Output condition | Welfare can rise only if total output rises (sign condition, no unit) | Schmalensee (1981), pp. 242–247, exact location not verified; credited to Schmalensee's analysis by Cowan (2007, p. 3), and proved "very generally" by Varian (1985) per ACV (2010, p. 1601) | The link between the sign of the output change and the possible sign of the welfare change | That output rising is sufficient for welfare to rise; the size of any welfare change; whether output rises in any real market |
| Welfare decomposition | W′(r) = (p_w − p̄)q′_w p′_w + (p_s − p̄)q′_s p′_s + (p̄ − c)Q′(r), money per unit change in allowed price gap | ACV (2010), eq. (3), p. 1604, "following Schmalensee (1981)" | Marginal welfare effect of allowing a little more discrimination, split into misallocation and output effects | The global (non-marginal) welfare change unless the sign of W′ is constant along the path |
| Straight-line case | Change in total output = 0 exactly; welfare change < 0 | Original proof by Pigou (1920), per ACV (2010, p. 1601) and Cowan (2013, pp. 1–2); restated within Schmalensee's framework | What discrimination does when every demand curve is linear and every market is served | That real demand curves are linear; anything when a market would be shut out at the uniform price |
| Curvature and output | Sign of the output change depends on the relative curvature of demand in the weak and strong markets | ACV (2010, p. 1601): Robinson's analysis "taken forward by Richard Schmalensee (1981)" | Which demand shapes make discrimination raise or lower output | Which shapes real markets have; ACV (2010) later derived the welfare counterpart |
| Varian's bounds (companion result) | (p̄ − c)ΣΔq_i ≥ ΔW ≥ Σ(p_i − c)Δq_i, money per period | Varian (1985); restated as eq. (1) in Cowan (2013, p. 5) | Upper and lower bounds on the welfare change from observable prices and quantities | The quantities under the regime not observed, which must come from a model or an experiment |

## Interpretation notes

- The paper is a theory paper, so its "statistics" are theorems. Their reliability rests on the assumptions, not on
  sampling, and the secondary literature treats them as correct. I found no published correction or comment that
  identifies an error, and I did not look for one beyond the papers listed above.
- Attribution in the literature is layered. Pigou is credited with the straight-line result, Robinson with the
  curvature intuition, Schmalensee with the method and the output-welfare link in this setting, and Varian with
  the fully general necessary condition and the bounds. Readers citing "Schmalensee's result" should be clear which
  of these they mean.
- The output condition is a screening test. It can rule welfare gains out, but a positive output effect only makes
  a gain possible. ACV (2010) and Cowan (2013) are the papers that turn it into conditions under which welfare
  actually rises.
- The modern rerun in this repository uses the companion bounds and the straight-line case on Netflix and Disney
  regional prices. Because those inputs are company-reported averages and the counterfactual quantities come from
  fitted demand curves, it is an application of the theory, not a test of the theorems.

## Unanswered questions

- How does the published version state its assumptions about cost, independence of demands and markets served,
  and does it discuss the market-opening case at all? This requires reading the full text.
- Does the paper give a numerical example? None is mentioned in the secondary accounts I read.
- How sensitive are the results to non-constant marginal cost, which the later literature treats as an extension?
- What do the results imply under oligopoly, where Holmes (1989) extended the output analysis?

## Items requiring expert verification

- The exact statement, page and equation number of the output condition in the 1981 article, and whether the
  article itself or only Varian (1985) proves it for an arbitrary number of markets.
- Whether the working paper (January 1980) and the published article differ in scope or results.
- Whether the welfare decomposition in ACV (2010) equation (3) appears in Schmalensee's article in that form or is
  ACV's restatement of his method.
- Whether any published comment or correction concerns the paper.
