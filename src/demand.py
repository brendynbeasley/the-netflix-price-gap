"""Demand curves calibrated to one observed price and quantity, and the monopoly pricing they imply.

Shared by schmalensee.py and curvature.py; it is not meant to be run on its own.

Each market i has inverse demand from the Bulow-Pfleiderer family,

    p = A_i - B_i * q**d_i          (d_i != 0)
    p = A_i - B_i * ln(q)           (d_i == 0, exponential demand)

d = 1 is a straight line (Schmalensee's and Pigou's case). d > 1 is concave demand, d < 1 is
convex demand, and d must exceed -1. The curvature of inverse demand, -q p''/p', is 1 - d, and
the pass-through of a cost change to the monopoly price is 1/(1+d): one half for a straight line.

Calibration assumes the observed price is the seller's profit-maximizing price in that market,
given a constant marginal cost c common to all markets (Schmalensee's setting). The first-order
condition p - c = -q p'(q) then pins down B_i and A_i from the observed (p_i, q_i):

    d != 0:  B_i = (p_i - c) / (d * q_i**d),   A_i = p_i + (p_i - c) / d
    d == 0:  B_i = p_i - c,                     A_i = p_i + B_i * ln(q_i)

All functions take arrays with one entry per market; `d` may be a scalar or one value per market.
"""

import numpy as np
from scipy.optimize import minimize_scalar


def _arr(x, n=None):
    a = np.atleast_1d(np.asarray(x, dtype=float))
    if n is not None and a.size == 1:
        a = np.full(n, a[0])
    return a


def calibrate(p, q, c, d):
    """Return arrays (A, B) so that each market's monopoly price at cost c is exactly p."""
    p, q = _arr(p), _arr(q)
    d = _arr(d, len(p))
    if np.any(p <= c):
        raise ValueError("every observed price must exceed marginal cost")
    if np.any(d <= -1):
        raise ValueError("curvature parameter d must be greater than -1")
    A = np.empty_like(p)
    B = np.empty_like(p)
    for i in range(len(p)):
        if d[i] == 0:
            B[i] = p[i] - c
            A[i] = p[i] + B[i] * np.log(q[i])
        else:
            B[i] = (p[i] - c) / (d[i] * q[i] ** d[i])
            A[i] = p[i] + (p[i] - c) / d[i]
    return A, B


def quantity(P, A, B, d):
    """Quantity each market buys at one common price P (zero above a choke price)."""
    d = _arr(d, len(A))
    out = np.zeros(len(A))
    for i in range(len(A)):
        if d[i] == 0:
            out[i] = np.exp((A[i] - P) / B[i])
        else:
            ratio = (A[i] - P) / B[i]
            out[i] = ratio ** (1.0 / d[i]) if ratio > 0 else 0.0
    return out


def welfare(q, A, B, c, d):
    """Consumer surplus plus profit in each market: the integral of (p(x) - c) from 0 to q."""
    q = _arr(q)
    d = _arr(d, len(q))
    w = np.zeros(len(q))
    for i in range(len(q)):
        if q[i] <= 0:
            continue
        if d[i] == 0:
            w[i] = (A[i] - c) * q[i] - B[i] * (q[i] * np.log(q[i]) - q[i])
        else:
            w[i] = (A[i] - c) * q[i] - B[i] * q[i] ** (d[i] + 1) / (d[i] + 1)
    return w


def consumer_surplus(q, A, B, d):
    """Area under inverse demand and above the price actually paid, in each market."""
    q = _arr(q)
    d = _arr(d, len(q))
    cs = np.zeros(len(q))
    for i in range(len(q)):
        if q[i] <= 0:
            continue
        cs[i] = B[i] * q[i] if d[i] == 0 else B[i] * d[i] * q[i] ** (d[i] + 1) / (d[i] + 1)
    return cs


def uniform_price(A, B, c, d, p_obs):
    """The single price that maximizes total profit across all markets.

    Total profit can have more than one peak when a market drops out, so a fine grid is searched
    first and the best grid point is refined.
    """
    hi = 4.0 * float(np.max(p_obs)) + c
    grid = np.linspace(c + 1e-6, hi, 20001)
    profit = np.array([(P - c) * quantity(P, A, B, d).sum() for P in grid])
    k = int(np.argmax(profit))
    lo_b, hi_b = grid[max(k - 1, 0)], grid[min(k + 1, len(grid) - 1)]
    res = minimize_scalar(lambda P: -(P - c) * quantity(P, A, B, d).sum(),
                          bounds=(lo_b, hi_b), method="bounded", options={"xatol": 1e-10})
    return float(res.x)


def compare(p, q, c, d, months=12.0):
    """Uniform pricing against the observed (discriminatory) prices, market by market.

    Quantities are millions of subscribers and prices are dollars a month, so money comes out in
    millions of dollars a month and is multiplied by `months` to give annual figures. Every change
    is discrimination minus uniform pricing.
    """
    p, q = _arr(p), _arr(q)
    A, B = calibrate(p, q, c, d)
    P = uniform_price(A, B, c, d, p)
    q_u = quantity(P, A, B, d)
    dq = q - q_u
    w_d, w_u = welfare(q, A, B, c, d), welfare(q_u, A, B, c, d)
    cs_d, cs_u = consumer_surplus(q, A, B, d), consumer_surplus(q_u, A, B, d)
    pr_d, pr_u = (p - c) * q, (P - c) * q_u
    return dict(
        A=A, B=B, uniform=P, q_uniform=q_u, dq=dq,
        dW=(w_d - w_u) * months, dCS=(cs_d - cs_u) * months, dProfit=(pr_d - pr_u) * months,
        served_uniform=q_u > 1e-9,
        total_dq=float(dq.sum()),
        total_dW=float((w_d - w_u).sum() * months),
        total_dCS=float((cs_d - cs_u).sum() * months),
        total_dProfit=float((pr_d - pr_u).sum() * months),
        varian_upper=float((P - c) * dq.sum() * months),
        varian_lower=float(((p - c) * dq).sum() * months),
    )
