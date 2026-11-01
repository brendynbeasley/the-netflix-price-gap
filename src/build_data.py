"""Download Netflix and Disney annual reports (Form 10-K) and extract regional prices and subscribers.

Netflix reports, for each of its four regions, streaming revenue, paid net membership additions,
paid memberships at year end, average paying memberships and average monthly revenue per paying
membership (ARM), three years per 10-K, in the "Streaming Revenues" part of Item 7. Disney reports
Disney+ paid subscribers at fiscal year end and average monthly revenue per paid subscriber (ARPU)
for three segments (US and Canada, International excluding Hotstar, and Hotstar) under "Key
Metrics" for Direct-to-Consumer in Item 7.

The 10-K PDFs come from each company's investor-relations site (they are the same documents filed
with the SEC as Form 10-K). They are saved in data/raw/filings/, which git ignores, and the
extracted tables are written to data/raw/netflix_regions.csv and data/raw/disney_plus.csv, which
are committed so the analysis runs offline.

Run from the repository root:
    python src/build_data.py
"""

import re
import time
from pathlib import Path

import pandas as pd
import requests
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
FILINGS = RAW / "filings"
HEADERS = {"User-Agent": "Brendyn Beasley research 83249437+brendynbeasley@users.noreply.github.com"}

# Netflix 10-Ks for 2019, 2022 and 2024 each cover three years (2017-19, 2020-22, 2022-24). Where two
# filings cover the same year, the later one wins.
NETFLIX_FILINGS = {
    2019: "https://s22.q4cdn.com/959853165/files/doc_financials/2019/ar/2019-10-K.pdf",
    2022: "https://s22.q4cdn.com/959853165/files/doc_financials/2022/ar/4e32b45c-a99e-4c7d-b988-4eef8377500c.pdf",
    2024: "https://s22.q4cdn.com/959853165/files/doc_financials/2024/ar/Netflix-10-K-01272025.pdf",
}
# Disney's fiscal 2023 annual report also restates fiscal 2022 and 2021 in a supplemental table.
DISNEY_FILINGS = {
    2023: "https://thewaltdisneycompany.com/app/uploads/2024/02/2023-Annual-Report.pdf",
    2024: "https://thewaltdisneycompany.com/app/uploads/2025/01/2024-Annual-Report.pdf",
}
NETFLIX_REGIONS = {"UCAN": "United States and Canada (UCAN)", "EMEA": "Europe, Middle East, and Africa (EMEA)",
                   "LATAM": "Latin America (LATAM)", "APAC": "Asia-Pacific (APAC)"}
NETFLIX_ROWS = {  # column name: row label as printed (older filings say "Revenues", newer "Streaming revenues")
    "revenue_kusd": re.compile(r"(?:Streaming\s*r|R)evenues"),
    "paid_net_adds_k": "Paid net membership additions",
    "paid_memberships_end_k": "Paid memberships at end of period",
    "avg_paying_memberships_k": "Average paying memberships",
    "arm_usd": "Average monthly revenue per paying membership",
}
DISNEY_ROWS = {"Domestic": "Domestic (U.S. and Canada)", "International": "International (excluding Disney+ Hotstar)",
               "Hotstar": re.compile(r"Disney\+\s*Hotstar(?!\s*\))")}  # not the "(excluding ...)" label
NUMBER = re.compile(r"\(\s*[\d,]+(?:\.\d+)?\s*\)|[\d,]*\d(?:\.\d+)?")


def fetch_text(url, name):
    """Download a PDF once and return the text of each page."""
    FILINGS.mkdir(parents=True, exist_ok=True)
    path = FILINGS / name
    if path.exists() and path.stat().st_size > 100_000:
        print(f"  cached {name} ({path.stat().st_size / 1e6:.1f} MB)")
    else:
        r = requests.get(url, headers=HEADERS, timeout=120)
        r.raise_for_status()
        tmp = path.with_suffix(".part")
        tmp.write_bytes(r.content)
        tmp.rename(path)
        print(f"  downloaded {name} ({len(r.content) / 1e6:.1f} MB) from {url}")
        time.sleep(1)
    return [p.extract_text() or "" for p in PdfReader(path).pages]


def loose(label):
    """Regex for a printed label that tolerates the stray spaces and line breaks PDF text extraction adds."""
    chars = [re.escape(c) for c in label.replace(" ", "")]
    return re.compile(r"\s*".join(chars))


def to_number(tok):
    tok = tok.replace(",", "").replace(" ", "")
    if tok.startswith("("):
        return -float(tok.strip("()"))
    return float(tok)


def first_values(block, label, n):
    """The first n numbers printed after `label` in `block` (footnote markers like '(1)' skipped).

    `label` is either the printed text or a ready-made regular expression."""
    m = (label if isinstance(label, re.Pattern) else loose(label)).search(block)
    if m is None:
        return None
    rest = block[m.end():].replace("$", " ")
    rest = re.sub(r"^\s*\(losses\)", "", rest)
    rest = re.sub(r"^\s*\([12]\)", "", rest)
    vals = [to_number(t) for t in NUMBER.findall(rest[:400])]
    return vals[:n] if len(vals) >= n else None


def netflix():
    records = []
    for filing_year, url in NETFLIX_FILINGS.items():
        print(f"Netflix 10-K for {filing_year}:")
        text = "\n".join(fetch_text(url, f"netflix_10k_{filing_year}.pdf"))
        for code, header in NETFLIX_REGIONS.items():
            block = None
            for m in loose(header).finditer(text):
                cand = text[m.end():m.end() + 1500]
                if loose(NETFLIX_ROWS["arm_usd"]).search(cand):
                    block = cand
                    break
            if block is None:
                print(f"  {code}: regional table not found")
                continue
            years = [int(y) for y in re.search(r"(20\d\d)\s+(20\d\d)\s+(20\d\d)", block).groups()]
            vals = {k: first_values(block, lab, 3) for k, lab in NETFLIX_ROWS.items()}
            missing = [k for k, v in vals.items() if v is None]
            if missing:
                print(f"  {code}: could not read {missing}")
                continue
            for j, y in enumerate(years):
                records.append(dict(fiscal_year=y, region=code, filing_year=filing_year, source=url,
                                    **{k: v[j] for k, v in vals.items()}))
            print(f"  {code}: years {years}")
    df = pd.DataFrame(records)
    before = len(df)
    df = df.sort_values("filing_year").drop_duplicates(["fiscal_year", "region"], keep="last")
    print(f"  {before} region-years read, {before - len(df)} overlapping years from older filings dropped")
    out = pd.DataFrame({
        "fiscal_year": df.fiscal_year, "region": df.region,
        "revenue_musd": df.revenue_kusd / 1000, "paid_net_adds_m": df.paid_net_adds_k / 1000,
        "paid_memberships_end_m": df.paid_memberships_end_k / 1000,
        "avg_paying_memberships_m": df.avg_paying_memberships_k / 1000,
        "arm_usd": df.arm_usd, "source": df.source,
    }).sort_values(["fiscal_year", "region"])
    out.to_csv(RAW / "netflix_regions.csv", index=False)
    print(f"Wrote data/raw/netflix_regions.csv: {len(out)} rows, {out.fiscal_year.min()}-{out.fiscal_year.max()}")
    return out


def disney_tables(page, title, kind, url):
    """Read every Disney+ table on a page that starts with `title` (subscribers or ARPU)."""
    rows = []
    for m in loose(title).finditer(page):
        block = page[m.end():m.end() + 900]
        years = [int(y) for y in re.findall(r"\b(20\d\d)\b", block[:120])][:2]
        hulu = block.find("Hulu")
        block = block[:hulu] if hulu > 0 else block
        if len(years) < 2:
            continue
        for seg, label in DISNEY_ROWS.items():
            v = first_values(block, label, 2)
            if v is None:
                continue
            for j in range(2):
                rows.append(dict(fiscal_year=years[j], segment=seg, kind=kind, value=v[j], source=url))
    return rows


def disney():
    records = []
    for filing_year, url in DISNEY_FILINGS.items():
        print(f"Disney annual report for fiscal {filing_year}:")
        for page in fetch_text(url, f"disney_annual_report_{filing_year}.pdf"):
            if "Hotstar" not in page:
                continue
            records += disney_tables(page, "Paid subscribers", "paid_subs_end_m", url)
            records += disney_tables(page, "Average Monthly Revenue Per Paid Subscriber", "arpu_usd", url)
    df = pd.DataFrame(records)
    df["filing"] = df.source.map({u: y for y, u in DISNEY_FILINGS.items()})
    before = len(df)
    df = df.sort_values("filing").drop_duplicates(["fiscal_year", "segment", "kind"], keep="last")
    print(f"  {before} values read, {before - len(df)} repeated in a later report dropped")
    wide = df.pivot_table(index=["fiscal_year", "segment"], columns="kind", values="value", aggfunc="first")
    wide = wide.reset_index().merge(df.groupby(["fiscal_year", "segment"]).source.last().reset_index(),
                                    on=["fiscal_year", "segment"])
    wide = wide[["fiscal_year", "segment", "paid_subs_end_m", "arpu_usd", "source"]]
    wide = wide.sort_values(["fiscal_year", "segment"])
    wide.to_csv(RAW / "disney_plus.csv", index=False)
    print(f"Wrote data/raw/disney_plus.csv: {len(wide)} rows")
    return wide


if __name__ == "__main__":
    nf = netflix()
    print(nf.drop(columns="source").to_string(index=False))
    ds = disney()
    print(ds.drop(columns="source").to_string(index=False))
