# Automatic detection of pending-deal targets (stock/mixed mergers, tender offers, going-private, SPACs) from free data, to exclude their buy signals from the forward paper-trading system

Method note (read first). Research date: 22 Oct 2026. In this session the network proxy blocked every sec.gov host (www.sec.gov, efts.sec.gov and data.sec.gov all gave CONNECT 403), as well as the law-firm and academic sites (debevoise.com, perkinscoie.com, kslaw.com, johnhcochrane.com). WebFetch also failed DNS on them. **So no SEC endpoint was live-tested from here.** Findings come from three kinds of source:
1. WebSearch summaries of SEC pages, the CFR text, law-firm notes and papers.
2. The **edgartools** source code and docs (github.com/dgunning/edgartools, cloned and read directly). This is an actively maintained EDGAR client, and its code comments include measurements dated as late as 16 Oct 2026, so it is the best evidence available here of how the endpoints behave now.
3. The repo's own files (`BacktestShariah2/data/ambil_alih.csv`, `kod/ambil_alih.py`).

Any number given from memory without a retrievable source is under Gaps, not Findings. Before building, test every endpoint from a GitHub Actions runner.

Context. The current filter, `kod/ambil_alih.py` v1 (21 Oct 2026), catches cash deals through a price-pinning signature: JURANG_MIN 0.10, VOLUM_X 4.0, JULAT_UMUM_MAKS 0.03, JULAT_KUNCI_MAKS 0.015, BAND_KUNCI_MAKS 0.04, BAR_KUNCI 10. It also uses a 9-row manual list `data/ambil_alih.csv` with columns saham, tarikh_umum, tarikh_tamat, pembeli, harga_tawaran, bayaran, sumber. That list already holds one mixed deal (PEN / Boston Scientific, `campuran`), which can serve as a calibration case for the stock-deal detector below.

---

## 1. Which SEC EDGAR form types identify a target, and when? How to query them for free (full-text search, daily index, feeds), and what are the rate-limit and User-Agent rules in 2026?

### Takeaway
A signed deal leaves a predictable trail of EDGAR filings:
- **At signing (day 0 to 4):** an 8-K, plus Form 425 communications for stock deals and SC TO-C/SC 14D9-C pre-commencement communications for tender offers.
- **Weeks later:** PREM14A, then DEFM14A for vote-based mergers, or S-4/F-4 for stock deals.
- **On launch of a tender offer:** SC TO-T plus SC 14D9.
- **Going-private deals:** SC 13E3.

All of these can be pulled free from EDGAR at up to 10 requests/second, provided the request carries a declared User-Agent with contact details. The most useful endpoints are:
- the full-text search API at `https://efts.sec.gov/LATEST/search-index` (undocumented, but stable in 2026);
- the daily index files under `Archives/edgar/daily-index/`;
- the "getcurrent" Atom feed;
- per-company `data.sec.gov/submissions/CIK##########.json`.

### Cited Findings
**Rate limits and identification**
- The SEC "Accessing EDGAR Data" page sets the fair-access maximum at **10 requests/second** and reserves the right to limit rates. It asks automated clients to declare a User-Agent header with a company name and admin contact email (its sample is "Sample Company Name AdminContact@<sample company domain>.com"). — [SEC: Accessing EDGAR Data](https://www.sec.gov/os/accessing-edgar-data) (via search summary; page not fetched)
- An edgarWebR package page says the limit applies per user, however many machines send the requests. — [edgarWebR README](https://cran.ms.unimelb.edu.au/web/packages/edgarWebR/readme/README.html) (via search summary)
- edgartools defaults to **9 requests/second** (`EDGAR_RATE_LIMIT_PER_SEC`) and retries on HTTP 429. Its doc also says "The SEC doesn't publish specific rate limits", which contradicts the SEC page above; treat the SEC page as authoritative. — [edgartools docs: SEC Rate Limits & Compliance](https://github.com/dgunning/edgartools/blob/main/docs/resources/sec-compliance.md)
- Third-party write-ups report that requests with a generic or empty User-Agent get HTTP 403. — [orthogonal.info: Reverse-engineering EDGAR full-text search](https://orthogonal.info/sec-edgar-full-text-search-api-efts-python/); [dev.to version](https://dev.to/orthogonalinfo/reverse-engineering-sec-edgars-full-text-search-api-one-undocumented-get-request-4ie6)

**Full-text search (EFTS)**
- Endpoint: `GET https://efts.sec.gov/LATEST/search-index`.
  - It is undocumented by the SEC and returns raw Elasticsearch JSON.
  - `/LATEST/` must be upper case; lower case gives 404.
  - Parameters: `q` (wrap a phrase in quotes for an exact match), `forms` (comma-separated form types), `startdt`/`enddt` (YYYY-MM-DD) and `from` (offset).
  - — [orthogonal.info](https://orthogonal.info/sec-edgar-full-text-search-api-efts-python/)
- Paging, date and filter behaviour, from edgartools' client:
  - "EFTS serves 100 hits per request whatever `size` says, and rejects from + 100 > 10,000."
  - `dateRange=custom` applies only when **both** `startdt` and `enddt` are given. In an edgartools test on 2026-10-16, a query with only `startdt` silently searched every year (10,000+ hits led by 2010 and 2003 filings).
  - The client also passes `ciks=` (10-digit CIK) and `items=` (8-K item numbers, e.g. `items=1.01`).
  - Coverage starts in 2001.
  - — [edgartools edgar/search/efts.py](https://github.com/dgunning/edgartools/blob/main/edgar/search/efts.py)
- Each EFTS hit carries `_source` fields: `adsh` (accession), `form`, `file_date`, `display_names[]`, `ciks[]`, `sics[]`, `items[]`, `biz_states[]`, `inc_states[]`, `period_ending`, `file_type`, `file_description`. `_id` is "accession:document_filename". **`ciks`/`display_names` are lists, because a filing can carry several entities, such as a filer and a subject company.** — [edgartools efts.py `_parse_hit`](https://github.com/dgunning/edgartools/blob/main/edgar/search/efts.py)

**Other free endpoints (as built by edgartools)**
- Submissions JSON: `https://data.sec.gov/submissions/CIK{cik:010d}.json`.
- Daily index: `https://www.sec.gov/Archives/edgar/daily-index/{year}/QTR{q}/{name}.{ext}`.
- Full index: `https://www.sec.gov/Archives/edgar/full-index/{year}/QTR{q}/{form|master|company}.{idx|gz}`.
- Raw feed: `https://www.sec.gov/Archives/edgar/Feed/{year}/QTR{q}/`.
- Ticker maps: `https://www.sec.gov/files/company_tickers.json`, `.../company_tickers_exchange.json` and `https://www.sec.gov/include/ticker.txt`.
- — [edgartools edgar/urls.py](https://github.com/dgunning/edgartools/blob/main/edgar/urls.py)
- Real-time feed: `https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type={FORM}&count={n}&start={k}&owner={include|exclude}&output=atom`, served in pages (edgartools uses 100 per page). — [edgartools edgar/current_filings.py](https://github.com/dgunning/edgartools/blob/main/edgar/current_filings.py); [edgartools docs: current filings](https://github.com/dgunning/edgartools/blob/main/docs/guides/current-filings.md)
- Per-filing header (all parties, CIKs, SIC codes, file numbers): `https://www.sec.gov/Archives/edgar/data/{cik}/{acc_no_dashes}/{accession}-index-headers.html`. — [edgartools edgar/headers.py](https://github.com/dgunning/edgartools/blob/main/edgar/headers.py)

**Form types and what they mean (edgartools form lists)**
- edgartools' form lists include "425", "SC TO-I", "SC TO-C", "SC TO-T", "DEFM14A" ("merger proxy"), "PREM14A" ("Preliminary merger proxy"), "S-4" ("Business combinations") and "F-4". — [edgartools edgar/entity/constants.py](https://github.com/dgunning/edgartools/blob/main/edgar/entity/constants.py); [edgartools edgar/enums.py](https://github.com/dgunning/edgartools/blob/main/edgar/enums.py)
- **Schedule 14D-9** is "Filed by a tender offer target company's board of directors, stating whether shareholders should accept, reject, or remain neutral on the offer". The form codes are "SC 14D9" and "SC 14D9/A". The same code notes there were **55 SC 14D9 originals filed in 2025**, i.e. about one new tender-offer target per week. — [edgartools edgar/tender_offers/schedule14d9.py](https://github.com/dgunning/edgartools/blob/main/edgar/tender_offers/schedule14d9.py)
- In the filing header, Schedule TO has "FILER: Bidder making the offer" and "SUBJECT COMPANY: Target company". Schedule 14D-9 is the "Target's response to tender offer". DEFM14A is a "Merger proxy (target company)". Schedule 13E-3 is a "Going-private transaction target". — [edgartools SEC_FILING_HEADER_STRUCTURE.md](https://github.com/dgunning/edgartools/blob/main/edgar/sgml/SEC_FILING_HEADER_STRUCTURE.md)

**Form 425 and Form 8-K rules**
- Under Rule 425 (17 CFR 230.425), business-combination communications relying on Rule 165 "are prospectuses that must be filed ... on the date of first use". Each must identify the filer, the company that is the subject of the offering, and the file number of the related registration statement (or the subject company's Exchange Act file number if the registration number is not known). — [17 CFR 230.425 (customsmobile mirror)](https://www.customsmobile.com/regulations/title17_chapterII_part230_subjgrp41_section230.425)
- Form 8-K timing:
  - Most 8-K items are due within **4 business days** of the event.
  - Item 1.01 = entry into a material definitive agreement.
  - Item 1.02 = termination of one. A compliance FAQ notes that an agreement expiring on its own stated terms does not trigger Item 1.02.
  - — [Wikipedia: Form 8-K](https://en.wikipedia.org/wiki/Form_8-K); [SEC Release 33-8400](https://www.sec.gov/files/rules/final/33-8400.htm); [M2 Compliance 8-K FAQ](https://www.m2compliance.com/8k-form-faq.php)

### Inferences
- **Strongest target-only forms** (filer = target, or target = header SUBJECT COMPANY):
  - SC TO-T and SC TO-T/A: subject company = target.
  - SC 14D9 and SC 14D9-C: filer = target.
  - SC 13E3: subject = going-private target.
  - **Signal timing:** 14D9-C/TO-C can come on announcement day; TO-T/14D9 at launch, normally days to two weeks after signing; 13E3 alongside the proxy.
- **Moderate (role must be resolved):**
  - Form 425: filed from announcement day onward, many times per deal.
  - PREM14A/DEFM14A (and PREM14C/DEFM14C for written-consent deals).
  - 8-K Item 1.01 with merger-agreement text.
  - Both parties file 8-Ks and 425s, and an acquirer that must get its own shareholders to approve a share issuance also files a merger proxy. See Q2.
- **Acquirer-side form:** S-4/F-4 is filed by the issuer of the new shares, i.e. the acquirer, in stock and mixed deals. Its registrant is therefore usually **not** the target, and the target has to be read from the subject company or the text.
- **SC TO-I is an issuer self-tender** (buyback). It is not a takeover unless it comes with an SC 13E3, so it should not trigger exclusion on its own.
- **Practical daily pull for ~2,000 tickers:** one form index file per day, plus about 5–10 EFTS queries over the last 3 days, plus one `-index-headers.html` per relevant hit. That is roughly 20–100 requests/day, far below 10/s. Use a User-Agent of the form "PapertradeClaude research <contact email>".

### Gaps
- **sec.gov reachability:** I could not fetch any sec.gov page from this sandbox, so the exact daily-index file names (`form.YYYYMMDD.idx` / `master.YYYYMMDD.idx`, from memory) and the current wording of the SEC fair-access page are unverified. I also could not test whether EDGAR accepts requests from GitHub-hosted runner IP ranges.
- **EFTS index lag:** I found no source for how quickly a new filing appears in EFTS; it should be measured.
- **Form code renames:** I found no confirmation of whether EDGAR renamed the Schedule TO / 14D-9 codes the way Schedule 13D/G moved to "SCHEDULE 13D/13G" in late 2024. edgartools (Oct 2026) still uses "SC TO-T", "SC 14D9" and "SC 13E3"-style codes, which suggests they are current.
- **Typical lags:** no sourced figures for signing → PREM14A or signing → SC TO-T commencement.
- **sec-edgar-downloader, QuantConnect and QuantRocket:** their M&A datasets were not researched.

---

## 2. How to map a CIK to a ticker, and how to tell the subject company (target) from the filer (acquirer) in Form 425 / SC TO / proxy filings

### Takeaway
Use `company_tickers.json` (fields `cik_str`, `ticker`, `title`) or `company_tickers_exchange.json` (`fields`/`data` layout) to map CIK → ticker. For role, read the filing header:
- In **Schedule TO the SUBJECT COMPANY is the target and the FILER is the bidder**.
- Regulation M-A defines "subject company" as the company whose securities are sought, e.g. the target, so in 425s the SUBJECT COMPANY is normally the target. But real 425s sometimes list the acquirer as a subject company too, or have filer = subject. A role resolver must therefore cross-check against the S-4/F-4 registrant (acquirer) and the 8-K text.

### Cited Findings
- **Ticker maps:**
  - edgartools reads `company_tickers.json` with keys `cik_str` (int) and ticker.
  - It reads `company_tickers_exchange.json` as `pd.DataFrame(data['data'], columns=data['fields'])`.
  - It ships a bundled parquet copy as fallback.
  - — [edgartools edgar/reference/tickers.py](https://github.com/dgunning/edgartools/blob/main/edgar/reference/tickers.py); [edgartools edgar/urls.py](https://github.com/dgunning/edgartools/blob/main/edgar/urls.py)
- **Header blocks:** filings carry `FILER:` and `SUBJECT COMPANY:` blocks, each with COMPANY CONFORMED NAME, CENTRAL INDEX KEY, STANDARD INDUSTRIAL CLASSIFICATION, and FILING VALUES such as FORM TYPE and SEC FILE NUMBER. edgartools' M&A example takes `target = header.subject_companies[0]` and `acquirer = header.filers[0]`. — [edgartools SEC_FILING_HEADER_STRUCTURE.md](https://github.com/dgunning/edgartools/blob/main/edgar/sgml/SEC_FILING_HEADER_STRUCTURE.md)
- **Real SC TO-T/A example:** an edgartools test parses an SC TO-T/A whose SUBJECT COMPANY is CVR ENERGY INC (CIK 0001376139), the target of a tender offer. — [edgartools tests/sgml/test_filing_sgml.py](https://github.com/dgunning/edgartools/blob/main/tests/sgml/test_filing_sgml.py)
- **Legal definition:** Regulation M-A Item 1000(f) defines "subject company" as the company or entity whose securities are sought to be acquired in the transaction (e.g., the target), or that is otherwise the subject of the transaction. — [17 CFR 229.1000, Cornell LII](https://www.law.cornell.edu/cfr/text/17/229.1000); [Deloitte DART copy](https://dart.deloitte.com/USDART/home/accounting/sec/rules-regulations/229-regulation-s-k/229-1000-mergers-acquisitions-regulation-m)
- **Form 425 examples:**
  - PNC's 2003 425 is labelled "Subject Company: United National Bancorp, Commission File No. 000-16931". — [PNC 425 (2003)](https://investor.pnc.com/sec-filings/all-sec-filings/content/0000898822-03-000935/sep2425.txt)
  - Barings BDC's 2020 425 is "Filed by Barings BDC, Inc. pursuant to Rule 425 ... Subject Company: MVC Capital" (file no. 814-00201). — [Barings BDC 425 (2020)](https://ir.barings.com/sec-filings/all-sec-filings/content/0001140361-20-026843/nt10014584x11_425.htm)
  - A 2000 Circle International 425 lists **two** subject companies, Circle and EGL. — [EGL/Circle 425 (2000)](https://www.sec.gov/Archives/edgar/data/0001001718/000095012900003543/e425.txt) (via search summary)
  - A 2015 Cigna 425 shows filer and subject company as the same company (file no. 001-08323). — [Cigna 425 (2015)](https://www.sec.gov/Archives/edgar/data/0000701221/000095015915000227/cign425.htm) (via search summary)
- **EFTS hits** carry `ciks[]` and `display_names[]` arrays, so one 425 hit can list both parties. The arrays do not label roles, so role needs the header. — [edgartools efts.py](https://github.com/dgunning/edgartools/blob/main/edgar/search/efts.py)

### Inferences
- **Role-resolution rules, in priority order:**
  1. SC TO-T(/A), SC TO-C, SC 13E3: target = SUBJECT COMPANY CIK.
  2. SC 14D9(/A), SC 14D9-C: target = FILER, which is also the subject.
  3. 425: candidates = SUBJECT COMPANY CIKs.
     - Drop any candidate that is the registrant of an S-4/F-4 in the same deal (the acquirer issuing shares).
     - If filer = subject and that company has no S-4, it is the target filing about itself, as in the Cigna case: Cigna was the target in Anthem–Cigna (my knowledge, not sourced here).
  4. PREM14A/DEFM14A/PREM14C/DEFM14C:
     - Filer = target, **unless** the filer is also the S-4/F-4 registrant (an acquirer seeking share-issuance approval), or the filing is a joint proxy.
     - For a joint proxy, both companies appear; resolve with rule 3 or 5.
  5. 8-K Item 1.01 with "Agreement and Plan of Merger":
     - The target's 8-K normally says the merger sub "will merge with and into the Company, with the Company surviving as a wholly owned subsidiary of Parent".
     - The acquirer's 8-K describes "the Company" acquiring.
     - A regex on the filer's own name or "the Company" next to "surviving corporation" / "wholly owned subsidiary of" gives the role. This phrasing is standard deal-drafting usage, not taken from a source here; validate it on 20–30 recent 8-Ks.
- **Ticker mapping steps:**
  - Map the target CIK to a ticker through company_tickers.json and keep only tickers in the ~2,000 universe.
  - Store `cik` with the ticker, because tickers change after deals.
  - The acquirer's CIK comes from the same filing (FILER of SC TO-T, S-4 registrant, or the 425 filer when the filer ≠ subject). Store it as `pembeli_cik` so Q3's stock-pair check can run.
- **Multi-class targets:** a target with several share classes has one CIK but several tickers, so map CIK → all tickers. This matters for the repo's `kelas_berganda.csv`.

### Gaps
- No primary SEC text found explaining how EDGAR assigns the SUBJECT COMPANY block in 425 submissions, for example when filer-agent conventions differ. The examples show it varies, so measure it on the 2025–2026 425s for deals in `ambil_alih.csv`.
- I did not verify whether `company_tickers.json` keeps delisted or acquired CIKs. Memory says it holds current tickers only, so map promptly at detection time and cache.

---

## 3. Price-based signatures for stock-for-stock deals: rolling beta/correlation, spread stability, and thresholds from merger-arbitrage research

### Takeaway
In a fixed-exchange-ratio stock deal, the target trades at about the exchange ratio × the acquirer's price, less a spread. Arbitrageurs hold long target / short ratio × acquirer, so the **ratio P_target / P_acquirer becomes nearly constant and the target's daily returns become highly correlated with the acquirer's**. Collars break the fixed hedge ratio. Mitchell & Pulvino (2001) and later work describe the strategy and its risk, but I found **no published, standard numeric threshold** (correlation or ratio-volatility cut-off) for *detecting* a stock deal from prices. Thresholds have to be calibrated in-house on known deals.

### Cited Findings
**How stock deals are priced and hedged**
- Stock-for-stock merger arbitrage buys the target and shorts the acquirer in proportion to the exchange ratio, locking in the spread whatever the acquirer's price does. In a collar the exchange ratio changes with the acquirer's price, so the hedge ratio is not a fixed number. — [Wikipedia: Risk arbitrage](https://en.wikipedia.org/wiki/Risk_arbitrage) (secondary)

**Mitchell & Pulvino (2001)**
- The paper studies **4,750 mergers from 1963 to 1998**.
- Risk-arbitrage returns are correlated with market returns in severely falling markets but uncorrelated in flat and rising markets, a payoff like selling uncovered index puts.
- After transaction costs and a contingent-claims adjustment they estimate excess returns of about **4% per year**. A secondary source quotes 6.2% annualised for the raw portfolio, a different measure.
- — [Mitchell & Pulvino 2001, JF 56(6), IDEAS/RePEc](https://ideas.repec.org/a/bla/jfinan/v56y2001i6p2135-2175.html)

**Spread behaviour**
- Spreads of deals that later failed were wider from the start and widened in the days before failure. — [Alpha Architect: a quantitative strategy for enhancing merger arbitrage](https://alphaarchitect.com/a-quantitative-strategy-for-enhancing-merger-arbitrage/) (secondary summary; the original table was not checked)
- Spread size rises with perceived deal-failure risk. A 2019 study found diseconomies of scale: spreads narrowed as capital flowed into merger arbitrage. — [Alpha Architect: merger spread (2023)](https://alphaarchitect.com/merger-spread/) (secondary)

**Deal failure base rates**
- Giglio & Shue (2014), as cited by the New York Fed: of **5,377 deals (1970–2010), 21% fail, 6% remain pending and 73% succeed within one year** of announcement. Another study in the same report finds about **25% failure** across 6,462 deals (1984–2007). — [NY Fed Staff Report 761](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr761.pdf)
- Analysis Group: the deal success rate fell in 2008–2009 and returned to the pre-2008 level from 2010. — [Analysis Group merger-arbitrage update through Q2 2013](https://www.AnalysisGroup.com/globalassets/uploadedfiles/content/insights/ag_features/merger_arbitrage_spread_-_still_shrinking/merger_arbitrage_update_through_q2_2013.pdf)

### Inferences
- **Proposed stock-deal signature** (needs a known acquirer from Q2; without one the search space is about 2,000 × 2,000 pairs):
  1. An announcement day exists: gap or volume shock, with |return| ≥ 5% and volume ≥ 3× the 50-day median. The thresholds are looser than the cash filter because stock-deal premiums are often smaller.
  2. Over the next 10–20 bars, the standard deviation of daily Δlog(P_T/P_A) is ≪ the pre-deal value. A starting point to calibrate: ≤ 0.5× the pre-announcement 60-bar value, and absolute ≤ about 1%/day.
  3. The rolling 20-bar correlation of daily returns (T vs A) is ≥ about 0.8, against a pre-deal level that is usually ≤ 0.5. Beta T on A is close to 1, because returns, not prices, are compared once the ratio is constant.
  4. **Mixed deals** (cash + stock, e.g. PEN/BSX in `ambil_alih.csv`): beta < 1, about the stock share of value, but the ratio volatility still collapses.
  5. **Collar deals:** inside the collar the target is pinned in dollars like a cash deal (the existing filter catches it); outside it the target tracks the acquirer.
  - These thresholds are untested proposals, not from the literature.
- **Calibration:** run the signature on the stock or mixed deals already announced in 2025–2026 (from EFTS 425 / S-4 hits) and record the distributions. The repo's data store has daily bars, so pre/post windows are easy to compute.
- **Base rate for "lift on failure":** about 20–25% of announced deals fail within a year, so the filter must handle termination (Q7). It must not simply hold the stock out forever.

### Gaps
- No source found with explicit correlation or tracking-error thresholds for detecting stock deals. I could not reach Baker & Savasoglu (2002), Jetley & Ji (2010) or the Mitchell–Pulvino tables.
- No source found for a cash-vs-stock split of failure rates or spreads. The Analysis Group and NYU Shanghai thesis snippets did not show the split.

---

## 4. Headline/NLP heuristics ("to be acquired by", "agrees to be acquired", "to acquire <target>", "take private", "tender offer"): resolving which ticker is the target, and the precision practitioners report

### Takeaway
Target resolution from headlines is a role-labelling problem. The company that is the **object** of an acquisition verb ("X to acquire **Y**", "X buys **Y**") or the **subject of a passive / "be acquired" form** ("**Y** to be acquired by X", "**Y** agrees to be acquired") is the target. A 2026 preprint does exactly this with spaCy NER plus the dependency parse. I found **no published precision/recall for headline-level target identification**, and an academic study notes that predicting targets is hard. Headlines should therefore be an *early trigger to confirm with EDGAR*, not an exclusion source on their own.

### Cited Findings
- A 2026 arXiv preprint labels company roles in M&A headlines:
  - It runs spaCy NER and finds the deal verb (acquire, buy, takeover, …) in the dependency tree.
  - A company that is the subject is the acquirer; one that is the object is the target. Ambiguous cases default to neutral.
  - It reports that acquirer-tagged articles carry a stronger M&A signal.
  - — [arXiv 2608.17223 "Temporal Leakage in Financial News NLP … Regime-Specific M&A Signal"](https://arxiv.org/pdf/2608.17223) (preprint; via search summary)
- A USPTO patent describes a two-stage system: a semi-supervised classifier finds sentences with acquirer–target company pairs, rules attach deal values, and a second classifier assigns deal status (rumour, announced, completed). It gives no accuracy figures. — [US Patent 10,049,100 "Financial event and relationship extraction"](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10049100)
- Routledge et al. (CMU) predict acquirer or target status within one year from word and phrase features in SEC filings. They note that predicting targets accurately has proven difficult. — [AEA 2017 conference paper](https://aeaweb.org/conference/2017/preliminary/paper/BsTQtktS) (via search summary)
- Ahern & Sosyura, "Rumor Has It: Sensationalism in Financial Media", studies how accurate the business press is on merger rumours. A summary notes that mergers have declined while rumours have increased. — [Hedge Fund Alpha summary](https://hedgefundalpha.com/news/merger-acquisitions-reporting/) (secondary)

### Inferences
**Recommended headline rules for the existing per-ticker Yahoo RSS (title + url)**

1. Normalise the ticker's company name from `company_tickers.json` `title`:
   - lower-case it;
   - strip Inc/Corp/Corporation/Holdings/Ltd/plc/Co/Group/"The";
   - keep a 1–3 token alias list, plus the ticker in parentheses or after "NASDAQ:"/"NYSE:".
2. **Target patterns.** A match marks the ticker whose name or alias is NAME:
   - `NAME (agrees|agreed|to|will) be (acquired|bought|taken private) by`
   - `NAME (enters|entered) into (a )?(definitive )?(merger )?agreement to be acquired`
   - `(acquire|acquires|to acquire|buy|buys|to buy|take private|takes private|to take private) NAME`
   - `NAME (to go|goes|going) private`
   - `(tender offer|exchange offer) (for|to acquire) NAME`
   - `NAME (shareholders|stockholders) (approve|vote).*(merger|acquisition)`
   - `NAME to merge with` (ambiguous; mark as "merger-of-equals candidate")
3. **Acquirer patterns.** These must *not* exclude the ticker:
   - `NAME (to acquire|acquires|agrees to acquire|will acquire|buys|to buy|completes acquisition of)`
   - `NAME (offer|bid) for`
   - In the system's example "Salesforce to acquire Braze", the rule tags BRZE (object) as target and CRM (subject) as acquirer.
4. **Rumour words** set state = "rumour", not "pending": explores, exploring, considering, weighs, in talks, approach, approached, interest, rumor, report, sources say, "according to people familiar", "strategic alternatives".
5. **Confirmation gate.** Move to "pending" only if, within 5 business days, an EDGAR filing from Q1/Q2 names the same CIK as target. Otherwise expire.
   - Exception: if the cash-pinning or stock-pair price signature (Q3) fires on the same day, exclude immediately, because the price already confirms it.

**Expected precision (my estimate; no published figure found)**
- For target-pattern headlines from mainstream wires, precision is probably high (>90%) for *who* is the target.
- Precision is lower for *whether a binding deal exists*: rumours, non-binding proposals, and asset or division sales ("X to acquire Y's unit") are common false positives.
- Add an exclusion for possessive/unit phrases: "'s (unit|division|business|assets|stake)".

### Gaps
- No precision/recall figures found for rule-based or NER-based target extraction on headlines.
- The Ahern & Sosyura rumour-to-deal conversion rate (recalled as roughly one-third) could not be verified, so it is not cited as a finding.
- I did not research whether Yahoo RSS headlines lag EDGAR 8-Ks or press releases.

---

## 5. Tender-offer rules (20 business days; the SEC's April 2026 order allowing 10 business days) and price behaviour

### Takeaway
On **16 April 2026** the SEC's Division of Corporation Finance issued an exemptive order, effective immediately, letting qualifying equity tender offers stay open **10 business days** instead of the usual 20. For third-party offers it covers only **all-cash, fixed-price, negotiated (non-hostile) offers under a merger agreement**, where the target files its Schedule 14D-9 by the first business day after commencement. Stock exchange offers stay on the longer timetable. A cash tender can therefore go from launch to close (and delisting) in about two weeks. The filter must catch the target from the SC TO-C/14D9-C or announcement 8-K, not wait for later forms.

### Cited Findings
- The order (16 Apr 2026, Division of Corporation Finance) allows a 10-business-day minimum offer period instead of 20 under Exchange Act Rules 13e-4(f)(1) and 14e-1, effective immediately. — [Debevoise (Apr 2026)](https://www.debevoise.com/insights/publications/2026/04/sec-exemptive-order-reduces-minimum-tender-offer); [Perkins Coie](https://perkinscoie.com/insights/update/sec-exemptive-order-permits-10-business-day-equity-tender-offers); [King & Spalding](https://www.kslaw.com/insights/articles/sec-exemptive-order-permits-10-business-day-offer-periods-for-certain-equity-tender-offers); [Cozen O'Connor](https://www.cozen.com/news-resources/publications/2026/sec-exemptive-order-reduces-minimum-offering-period-for-certain-tender-offers); [Foley Hoag via JD Supra](https://www.jdsupra.com/legalnews/sec-issues-exemptive-order-permitting-9438823/) (all via search summaries; sources differ slightly on the exact rule cites)
- **Conditions for reporting-company targets:**
  - The offer is all cash at a fixed price.
  - Third-party offers must be non-hostile and made under a negotiated merger agreement.
  - The target must file its Schedule 14D-9 by the first business day after commencement.
  - Issuer tender offers must be for less than all of the class.
  - Notice deadlines: a change in percentage sought or consideration must be announced by 9:00 a.m. ET on the 5th business day before expiry, and other material changes by the 2nd business day before.
  - Third-party offers for non-reporting (private) companies are excluded.
  - — same sources as above
- **Stated rationale:** addressing market inefficiencies, reflecting technological change, and reducing exposure to market swings. — [Foley Hoag via JD Supra](https://www.jdsupra.com/legalnews/sec-issues-exemptive-order-permitting-9438823/) (via search summary)
- **Volume:** about 55 original SC 14D9 filings in 2025, a rough count of tender-offer targets per year. — [edgartools schedule14d9.py comment](https://github.com/dgunning/edgartools/blob/main/edgar/tender_offers/schedule14d9.py)

### Inferences
- **Cash tender offers** pin the target just below the offer price from announcement, and the existing pinning filter catches them if the premium is ≥10%. Small-premium cash tenders (below 10%) fail the gap test but are caught deterministically by SC TO-C / SC TO-T / SC 14D9 subject-company detection.
- **Exchange offers** (stock or mixed consideration in a tender) are outside the 10-day relief and track the acquirer (Q3).
- **Detection timing:** a 10-business-day offer means the stock may delist about 3 weeks after announcement. Run the EDGAR pull every evening before the 7:47 pm buy-list build, so a signal is never generated on a pinned or soon-to-delist stock.
- **SC TO-I** (issuer self-tender, often a Dutch auction) is a buyback, not a takeover, and should not exclude unless an SC 13E3 is present (going private).

### Gaps
- The SEC order itself was not read; only law-firm summaries were. Confirm the exact text on sec.gov.
- No figures found on how many 2026 tender offers used the 10-day period.
- I did not find a source for the standard rule text (Rule 14e-1(a), 20 business days); it is cited only through the summaries ("the standard 20").

---

## 6. SPAC detection (SIC 6770, ~$10 trust, unit/warrant suffixes) and de-SPAC risks

### Takeaway
SPACs are easy to flag:
- EDGAR SIC code **6770 (blank checks)**;
- names with "Acquisition Corp/Co/Inc";
- sibling tickers ending in **U (units), W (warrants), R (rights)**;
- a price parked near the **$10.00–$10.10 trust value per share**.

Pre-deal SPAC shares carry no technical information, and their trust is invested in Treasury bills, which is likely a Shariah-screen issue. De-SPACs are filed as S-4/F-4 + 425 + DEFM14A by the SPAC (the SPAC is legally the acquirer, but economically the trust value is the floor).

### Cited Findings
- edgartools classifies SIC **6770 as SPAC** ("Blank Check Companies (SPACs)") and adds high-confidence name patterns 'ACQUISITION CORP', 'ACQUISITION CO', 'ACQUISITION INC' and 'BLANK CHECK'. — [edgartools edgar/entity/categorization.py](https://github.com/dgunning/edgartools/blob/main/edgar/entity/categorization.py)
- On Nasdaq the SPAC unit ticker ends in U, the common share has no suffix, the warrant adds W and the right adds R. — [Nasdaq SPAC explainer](https://www.nasdaq.com/de/node/10899051) (via search summary)
- **Trust and unit terms:**
  - Essentially all IPO proceeds, $10.00 per unit and often slightly more, go into a trust invested in U.S. Treasury bills.
  - Units are customarily priced at $10.00, with warrants struck at about $11.50.
  - The business combination must typically be completed within 18–24 months of the IPO, or the trust is returned to public shareholders.
  - — [Kramer Levin: A SPAC primer](https://kramerlevin.com/en/perspectives-search/a-spac-primer.html); [M&A newsletter: beginner's guide to SPACs](https://mergersandacquisitionsnewsletter.substack.com/p/the-beginners-guide-to-spacs); [CurvedTrading: what is a SPAC](https://curvedtrading.com/articles/en/investing/what-is-a-spac-blank-check-ipos/) (secondary)
- One underwriting agreement puts **$10.10 per unit** in trust, so the trust value is not always $10.00. — [Law Insider: Global SPAC Partners underwriting agreement](https://www.lawinsider.com/contracts/kb6S2ugSUGt)

### Inferences
- **Detector rules:**
  - SIC = 6770 from `data.sec.gov/submissions/CIK….json` (field `sic`) → exclude always.
  - Name regex `ACQUISITION (CORP|CO|INC|COMPANY)|BLANK CHECK|CAPITAL ACQUISITION` → exclude.
  - A sibling ticker with the same CIK ending in U/W/R in `company_tickers_exchange.json` → exclude.
  - Price sanity check: 60-bar close range within $9.8–$11 and 20-bar median daily range < 0.5% → exclude.
- **Price filter:** with the ≥ $10 price filter, pre-deal SPACs pass on price (trust ≈ $10–10.5), so the price floor does not remove them.
- **De-SPAC risks:**
  - After the merger closes, the company changes name, CIK SIC and ticker. Heavy redemptions and low float cause extreme volatility and gaps in the first 1–6 months.
  - Recommend excluding **new tickers whose CIK was SIC 6770 within the last 12 months**. Track this with the submissions JSON `formerNames`, or by keeping a local CIK→SIC history.
- **Shariah:** a pre-deal SPAC's only asset is an interest-bearing Treasury trust, so it would likely already fail the screen. Check whether the Shariah universe source already removes them; if so, SPAC detection is mostly a guard for de-SPACs.

### Gaps
- No source found on de-SPAC redemption rates or price behaviour in 2025–2026.
- NYSE suffix conventions (e.g. ".U", ".WS") were not verified.
- I did not verify that `company_tickers_exchange.json` includes SPAC units and warrants as separate rows (memory says it does).

---

## 7. Detecting deal completion (delisting, Form 25, 15-12B) or termination (8-K Item 1.02) to lift the filter

### Takeaway
- **Completion** shows up in this order:
  1. 8-K Items **2.01** (completion of acquisition, filed by the acquirer), **3.01** (notice of delisting) and **5.01** (change in control, filed by the target).
  2. **Form 25 / 25-NSE**, with delisting effective **10 days** after filing.
  3. **Form 15** (15-12B/15-12G/15-15D), which cannot be filed before the Form 25 is effective; deregistration follows within 90 days.
  4. In price data, the ticker stops printing.
- **Termination** shows up as:
  - an 8-K **Item 1.02** from the target citing the merger agreement;
  - a withdrawal amendment (SC TO-T/A, or SC 14D9/A reporting termination);
  - in price data, the "pin" breaking: the ratio/correlation signature decays and the price gaps back toward its pre-deal level.

### Cited Findings
- **Form 25 timing:** removal from listing is effective **10 days after the Form 25 is filed**. Withdrawal of Section 12(b) registration takes effect in **90 days** (or a shorter period the Commission sets). Under Rule 12d2-2 the SEC may postpone either date. — [SEC Form 25 instructions](https://www.sec.gov/about/forms/form25.pdf) (via search summary); [Willkie Farr 2005 summary of Rule 12d2-2 amendments](https://www.willkie.com/publications/2005/08/sec-adopts-rule-regarding-delisting-and-withdraw__) (older but still the governing framework)
- **Form 15 sequencing:** SEC staff C&DI 144.01 says a Form 15 may not be filed before the Form 25 delisting is effective. C&DI 144.02 says a periodic report falling due before the delisting takes effect must still be filed. — [PwC Viewpoint: Exchange Act Rules C&DI section 144 (Rule 12d2-2)](https://viewpoint.pwc.com/dt/us/en/sec/cdis/cdis_US/exchange_act_rules__1_US/questions_and_answer__13_US/section_144_rule_12d_US.html)
- **8-K items:**
  - Item 1.02 = termination of a material definitive agreement (not triggered when the agreement expires on its own terms).
  - Item 2.01 = completion of acquisition or disposition of assets.
  - Item 3.01 = Notice of Delisting or Failure to Satisfy a Continued Listing Rule or Standard; Transfer of Listing.
  - Item 5.01 = changes in control of registrant.
  - Generally due within 4 business days.
  - — [Wikipedia: Form 8-K](https://en.wikipedia.org/wiki/Form_8-K); [SEC Release 33-8400](https://www.sec.gov/files/rules/final/33-8400.htm); [M2 Compliance FAQ](https://www.m2compliance.com/8k-form-faq.php)
- **Base rate:** about 21% of announced deals fail and 6% are still pending after one year (Giglio & Shue, 5,377 deals 1970–2010). — [NY Fed SR 761](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr761.pdf)

### Inferences
**State machine per target CIK, stored in an extended `data/ambil_alih.csv`.** Suggested new columns: `cik, pembeli_cik, jenis (tunai|saham|campuran|tender|swasta|spac), status (khabar|belum_selesai|selesai|batal), tarikh_status, sumber_borang, nombor_akses`.
- `khabar` (rumour) → `belum_selesai` (pending). Trigger: any Q1 target-form hit, or a headline confirmed by EDGAR. Exclusion starts on the announcement date, the first EDGAR file_date or the headline date, whichever is earliest.
- `belum_selesai` → `selesai` (completed). Any one of:
  - Form 25/25-NSE whose subject or filer is the target CIK;
  - target 8-K Item 3.01 or 5.01;
  - acquirer 8-K Item 2.01 that names the target;
  - Form 15-12B/15-12G;
  - ≥ 5 sessions with no bars. This is already handled by `tidak_layak.py posisi` (delist).
  - Keep excluding until the ticker disappears, since no further buy signals are valid.
- `belum_selesai` → `batal` (terminated). Any one of:
  - target 8-K with Item 1.02 whose text matches "merger agreement|Agreement and Plan of Merger";
  - SC TO-T/A or 14D9/A containing "terminated|withdrawn|expired without";
  - headline "terminate(s|d) (the )?(merger|acquisition) agreement" for the ticker, confirmed by EDGAR within 5 days.
  - Then lift the filter, but keep a **cool-off** (e.g. 20 bars) so the post-break gap-down is not read as a technical setup.
- **Safety expiry:** if no completion or termination evidence appears within 18 months, flag for manual review rather than silently lifting.
- **Form type caution:** filter on "25-NSE" (exchange-filed) *and* "25" (issuer-filed). Both mark delisting, but they can also appear for reasons other than M&A, such as moving exchange or voluntary delisting. Require a matching open deal before marking `selesai`.

### Gaps
- No source found for the typical lag between closing and the Form 25 filing (memory: same day to a few days).
- No source found on how often Item 1.02 is used versus Item 8.01 for merger terminations.
- The current Form 25 / Rule 12d2-2 text was not re-verified beyond the 2005 summary and SEC form instructions.

---

## 8. Overall practical design and expected precision

### Takeaway
A three-layer free detector should close almost all of the listed gaps:
1. **(A) EDGAR form/role rules**, near-deterministic for signed deals;
2. **(B) price signatures:** the existing cash pin plus a new stock-pair tracking test;
3. **(C) headline role-parsing**, as an early trigger confirmed by A or B.

Only rumours and non-binding approaches remain unconfirmed by design. No published precision figure exists for this exact pipeline, so it must be measured on the 2025–2026 deals already known.

### Cited Findings
- **EDGAR side:**
  - EFTS can filter by `forms`, `ciks`, `items` and a closed date range, at 100 hits per page.
  - The `-index-headers.html` file gives the FILER/SUBJECT COMPANY roles.
  - company_tickers maps CIK to ticker.
  - — [edgartools efts.py](https://github.com/dgunning/edgartools/blob/main/edgar/search/efts.py); [edgartools headers.py](https://github.com/dgunning/edgartools/blob/main/edgar/headers.py); [edgartools tickers.py](https://github.com/dgunning/edgartools/blob/main/edgar/reference/tickers.py)
- **Schedule TO:** filer = bidder, subject = target. — [edgartools SEC_FILING_HEADER_STRUCTURE.md](https://github.com/dgunning/edgartools/blob/main/edgar/sgml/SEC_FILING_HEADER_STRUCTURE.md)
- **Rate limit:** 10 requests/second with a declared User-Agent. — [SEC: Accessing EDGAR Data](https://www.sec.gov/os/accessing-edgar-data)
- **Headline role labelling** by verb subject/object is used in current research (2026 preprint), but with no reported accuracy. — [arXiv 2608.17223](https://arxiv.org/pdf/2608.17223)

### Inferences
**Daily job:** `standard/tawaran_edgar.py`, in the evening GitHub Actions run before the buy list.

1. Pull EFTS for the last 3 calendar days, with `dateRange=custom&startdt=…&enddt=…` (both dates required):
   - `forms=SC TO-T,SC TO-C,SC 14D9,SC 14D9-C,SC 13E3` with a broad `q="offer"`. edgartools refuses a search with neither `q` nor `items`, so test on the first run whether EFTS itself accepts a forms-only query. If it does not, use the daily form index for these form types.
   - `forms=425`, `q="merger" OR "business combination"`.
   - `forms=PREM14A,DEFM14A,PREM14C,DEFM14C`, `q="merger"`.
   - `forms=8-K&items=1.01`, `q="Agreement and Plan of Merger"`.
   - `forms=8-K&items=1.02`, `q="merger agreement"` (terminations).
   - `forms=S-4,F-4`, `q="merger"` (to learn acquirer CIKs).
   - Forms `25-NSE,25,15-12B` (completion). As a fallback, read the daily form index instead.
2. For each hit, fetch `-index-headers.html` once and cache it by accession.
3. Apply the role rules (Q2). Map CIK → ticker and keep tickers in the universe.
4. Upsert the state into `data/ambil_alih.csv`, adding the new columns, and let `kod/tidak_layak.py` keep using it as the single gate.
5. For `jenis=saham/campuran` with a known `pembeli_cik` → ticker in the price store, run the Q3 pair test, to log evidence and calibrate.

**Expected request budget:** about 10 EFTS calls plus 10–60 header fetches per day. Using a cache of seen accessions, this stays far below the SEC limit.

**Expected precision and recall (my estimates, to be measured):**
- **Layer A:**
  - Precision ≈ 95%+ for the SC TO-T/14D9/13E3 subject rules.
  - Lower for 425/proxy without the S-4 cross-check. Merger-of-equals and acquirer share-issuance votes are the main false positives, and the S-4 rule removes most of them.
  - Recall is high for US-listed targets of signed deals: every US public-target deal needs a proxy, information statement or Schedule TO. The exceptions are foreign private issuers (6-K, schemes of arrangement) and deals where the target is not the SEC registrant.
- **Layer B (stock-pair test):** precision is good once an acquirer is known. Without an acquirer, run it only as a confirmation.
- **Layer C:** good at naming the target (>90% when the patterns match), poor as evidence of a binding deal.

**Validation plan:**
1. Back-run Layer A over 2025-01-01 → 2026-10-21 via EFTS.
2. Check it against the 9 rows of `ambil_alih.csv` (recall).
3. Hand-check 50 random flagged tickers (precision).
4. Report both numbers before switching the filter on in `lejar.yml` and `harian_c.py`.

### Gaps
- No public benchmark for precision/recall of EDGAR-based target detection was found; the numbers above are reasoned estimates.
- Foreign private issuer targets (F-4, 6-K, schemes of arrangement under foreign law) were not researched.
- Free practitioner deal lists (InsideArbitrage's free tier, etc.) were not reached, so I cannot confirm whether any free, machine-readable pending-deal list exists in 2026 to use as a cross-check.
- Whether sec.gov accepts traffic from GitHub-hosted runners must be tested on the first run. If it is blocked, a fallback (e.g. the existing Moomoo/FMP tools in a Claude session) would be needed.
