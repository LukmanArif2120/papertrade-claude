# Daily price-data quality in free US-equity vendors (yfinance, Moomoo, third sources) and automatic bar validation

Scope: daily bars for about 2,000 US stocks (price >= $10). Yahoo/yfinance is the primary source, Moomoo/Futu klines give official opens, and a free third source settles disputes. The research date is 22 Oct 2026. Notes say where a source is older or comes from a third party.

Method note: in this sandbox the agent proxy refused direct HTTPS to Yahoo, Stooq, Nasdaq and Futu (HTTP 403 on CONNECT), and WebFetch could not resolve futunn.com, moomoo.com, tiingo.com, quantconnect.com or wealth-lab.com. I could not test the endpoints live, so several facts rest on search-result summaries of those pages and are marked that way. The Moomoo MCP tool schemas loaded in this session are primary sources. Repo files are cited by path.

## 1. yfinance known issues 2024–2026: which are fixed, which remain, and version pinning

### Takeaway
yfinance changes often, with 1.0 to 1.7.0 shipped in roughly 2025–2026. It still depends on what Yahoo serves. Some Yahoo-side faults, such as whole sessions missing (5 Nov 2025), wrong opens that are corrected later, and missing split adjustment on split day, cannot be fixed by the library. They can only be detected. The repo installs yfinance, curl_cffi and exchange_calendars unpinned in every workflow, so library behaviour can change silently between nightly runs.

### Cited Findings
**Releases and changes (CHANGELOG plus releases page; the releases page shows day and month but no year):**
- Latest release is **1.7.0 (26 Aug)**. Earlier: 1.6.0 (13 Aug), 1.5.2 (23 Jul), 1.5.1 (28 Jun; replaces a *retracted* 1.5.0 "released without a dev-branch merge"), 1.4.1 (28 May), 1.4.0 (23 May), 1.3.0 (16 Apr), 1.2.2 (13 Apr), 1.2.1 (07 Apr), 1.2.0 (16 Feb) — [yfinance releases](https://github.com/ranaroussi/yfinance/releases)
- 1.2.0 "history() DataFrame is now consolidated … might trigger read-only errors in your code" — this is a behaviour change in a minor release — [yfinance releases](https://github.com/ranaroussi/yfinance/releases)
- 1.7.0 "Fixed volume validation in stock-split repair". 1.6.0 "Stopped claiming 'possibly delisted' when Yahoo explains missing data" and "Improved price repair". 1.5.1 "Repaired unit-switch double-application, premarket false-positive dividends, NaN volume errors, and infinite Adj Close". 1.1.0 fixed "stock-split false positives" and added "capital-gains double-counting repair". 1.0 fixed "price-div-repair dropping NaN rows" and added "optional retries for transient network errors" — [yfinance CHANGELOG](https://github.com/ranaroussi/yfinance/blob/main/CHANGELOG.rst)
- Network stack: 0.2.62 moved to curl_cffi. 1.0 blocked curl_cffi 0.14. 1.2.1 forced curl_cffi>=0.15 for a CVE. 1.4.0 made curl_cffi optional with a requests fallback. 1.5.2 fixed "breakage with curl_cffi>=0.16". 1.4.0 added a Yahoo login (`yf.Auth`) — [yfinance CHANGELOG](https://github.com/ranaroussi/yfinance/blob/main/CHANGELOG.rst); [releases](https://github.com/ranaroussi/yfinance/releases)
- **Live-row handling:** 0.2.56 fixed `fix_Yahoo_returning_live_separate()`. Yahoo can return the current (live) session as a separate row that the library has to merge. 0.2.53 added pre/post-market prices — [yfinance CHANGELOG](https://github.com/ranaroussi/yfinance/blob/main/CHANGELOG.rst)
- **Rate limiting:** 0.2.52 added `YfRateLimitError`. 0.2.58/0.2.59 fixed a *false* rate-limit detection. 0.2.62 "detected rate limits during crumb fetch" — [yfinance CHANGELOG](https://github.com/ranaroussi/yfinance/blob/main/CHANGELOG.rst). Users report the 429 often arrives at the cookie/crumb step ([#2480](https://github.com/ranaroussi/yfinance/issues/2480)). A crumb can come back as the literal text "Too Many Requests" and not be treated as a failure ([#2441](https://github.com/ranaroussi/yfinance/issues/2441)). Blocks are "usually temporary", but one user saw more than 24 h. Delays, fewer parallel jobs and caching are recommended ([discussion #2431](https://github.com/ranaroussi/yfinance/discussions/2431)). One user saw the error persist across different IPs ([#2422](https://github.com/ranaroussi/yfinance/issues/2422)). I found no source specific to GitHub Actions IPs.
- **auto_adjust default:** the `download()` default changed to `auto_adjust=True`, and an April 2025 log on yfinance 0.2.57 shows the "default changed to True" notice ([#2422](https://github.com/ranaroussi/yfinance/issues/2422)). With True, adjusted prices sit in "Close" and "Adj Close" disappears. `auto_adjust=False` restores the raw columns ([Kerry Back](https://kerryback.substack.com/p/02-online-data)). 0.2.53 "warned when download() is used without auto_adjust" ([CHANGELOG](https://github.com/ranaroussi/yfinance/blob/main/CHANGELOG.rst)). I did not find the exact version where the default flipped.
- **Missing session 5 Nov 2025:** issue #2621 (opened 6 Nov 2025) reports Yahoo history missing 5 Nov 2025 "prevalent across tickers" (MSFT, GLD), and Yahoo's own website charts also lacked it. Maintainer ValueRaider pointed to price repair: "Price repair needs good data before and after to calibrate. So move start back." Another user said repair did not solve it. A bot closed the issue on 6 Nov 2025. The thread does not record whether Yahoo later back-filled the day — [yfinance #2621](https://github.com/ranaroussi/yfinance/issues/2621)
- Older report: `period='max'` omitted the current day on 0.2.54 — [yfinance #2353](https://github.com/ranaroussi/yfinance/issues/2353)

**What `repair=True` does (wiki):**
- Adds a `Repaired?` column. It fixes missing dividend adjustment (Adj Close only; `Repaired?` *not* set), missing split adjustment ("Yahoo sometimes fails to adjust on split day"; the range must include one day after the split), missing data (rows rebuilt from a finer interval such as 1h, and "reconstructed prices and volume can differ from Yahoo's later corrected data, sometimes significantly"), 100x errors ($/cents, £/pence; scattered errors detected with scipy), and dividend errors (duplicates, 100x, wrong ex-date) — [yfinance wiki: Price repair](https://github.com/ranaroussi/yfinance/wiki/Price-repair)
- The wiki says only US market data "appears error-free" and that errors are common elsewhere. Dividend repair works only on `1d`, and its false positives cluster on very small dividends (about 0.5%). Hourly data for reconstruction is limited to about 2 years — [yfinance wiki: Price repair](https://github.com/ranaroussi/yfinance/wiki/Price-repair)
- The 100x currency fix dates back to 0.2.0rc5. Later releases (1.6.0) stop GBp/ZAc/ILA prices being converted permanently under repair, which is not relevant for USD stocks — [CHANGELOG](https://github.com/ranaroussi/yfinance/blob/main/CHANGELOG.rst)

**Repo state (local):**
- `requirements.txt` lists `exchange_calendars>=4.5` and `pandas>=2.2` and does **not** list yfinance. Workflows run `pip install -q pandas numpy yfinance exchange_calendars …` unpinned (`.github/workflows/harian.yml:46`, `beli.yml:58`, `harga_harian.yml:33`, `gred_kumpulan.yml:53`) — local files `/home/user/papertrade-claude/requirements.txt`, `/home/user/papertrade-claude/.github/workflows/*.yml`
- The store path uses `auto_adjust=False, actions=False` (`BacktestShariah2/standard/harga_yf.py:94`). Its docstring says: "OHLC mentah (auto_adjust=False; split dilaras oleh Yahoo, dividen tidak)". `harian_c.py:747` uses `period='5d'` with `auto_adjust=False`. Other jobs (`gred_kumpulan.py:45`, `sejarah_pemangkin_actions.py:113`) use `auto_adjust=True`, so they hold *different price series* for the same tickers — local repo files

### Inferences
- **Fixed in library:** live-row merge (0.2.56+), false rate-limit detection, the crumb rate-limit raised as `YfRateLimitError`, the misleading "possibly delisted" message (1.6.0), split-repair false positives (1.1.0, 1.7.0), and NaN/inf repair bugs (1.5.1).
- **Not fixable in library (Yahoo-side, remain):** whole sessions missing (5 Nov 2025), wrong or provisional opens, missing split adjustment on split day, volume definitions, IP throttling, and silent back-revision of history.
- **Pinning recommendation:** pin `yfinance==1.7.0` and a curl_cffi version that 1.7.0 supports (>=0.15 for the CVE; 1.5.2+ supports 0.16), and pin pandas and exchange_calendars in one constraints file used by *every* workflow. Upgrade on purpose: run a replay test against stored raw snapshots, compare outputs bar by bar, then bump. Record the library versions in each snapshot's metadata. Without a pin, a release like 1.2.0 (DataFrame consolidation) or the retracted 1.5.0 reaches production unreviewed.
- **Do not use `repair=True` on the store path.** It can write synthetic bars rebuilt from hourly data that differ from Yahoo's later truth, and some repairs (dividend) do not set the flag. Run it separately as a *diagnostic*: a row it would change is a candidate for cross-vendor checking.
- **Delist rule risk:** the delist rule (no bar for 5 or more sessions → close) can be triggered by a fetch failure. A throttled or empty frame looks the same as "no data". The no-bar counter should advance only for sessions where the fetch succeeded for most of the universe *and* a second source (Moomoo) also has no bar or shows the security as delisted.
- **Market-wide gap test:** if more than 30–50% of tickers lack the same XNYS session, it is a vendor outage like 5 Nov 2025, not stock-level missing data. Re-fetch later and never forward-fill.
- **auto_adjust=False still gives split-adjusted O/H/L/C** (per the repo docstring and the wiki's "missing split adjustment" case). Every split therefore rewrites *all earlier* raw bars at Yahoo. This is the main legitimate source of "silent history changes".

### Gaps
- Exact year of each 1.x release (the releases page omits years; 2025–2026 is inferred from the order and the April 2025 0.2.57 report).
- Whether Yahoo back-filled 5 Nov 2025 later. Not stated anywhere I found.
- No yfinance-specific GitHub issue found on "first pull after close has wrong open / partial last bar". The general pattern is documented for other vendors (section 2).
- No source on GitHub Actions runner IPs and Yahoo throttling.

## 2. How reliable are Yahoo daily OHLCV versus consolidated official data (definitions of O/H/L/C/V; odd lots; extended hours)?

### Takeaway
Yahoo daily close usually matches the primary-listing closing auction, and opens are usually the official opening cross. The exception is the day itself: same-day or early values can be provisional and corrected the next day. Yahoo volume is consolidated (all venues, actual shares), so it differs from filtered feeds such as IBKR's by large amounts. Use tolerances, not equality, for volume and high/low.

### Cited Findings
- Yahoo's *Adjusted Close* applies split and dividend multipliers "following CRSP standards". A 2:1 split multiplies earlier data by 0.5, and dividend multipliers are based on the dividend as a share of price — [Yahoo Help SLN28256](https://help.yahoo.com/kb/SLN28256.html)
- Yahoo volume covers all venues in actual shares. IBKR reports in 100-share lots and excludes odd lots, and a feed filtered to Nasdaq trades shows less — [QuantRocket forum](https://support.quantrocket.com/t/daily-volume-discrepancy-between-ib-and-yahoo/417). IBKR's historical feed drops trades away from the NBBO (blocks, combos), which put NVDA volume at roughly half of Yahoo's in June 2024 — [Elite Trader](https://elitetrader.com/et/threads/historical-data-volume-very-low.380050/)
- Anecdote: Nasdaq opening and closing auction prices matched Yahoo historical prices "99.8% of the time". Nasdaq publishes cross (auction) statistics for free, usually the next day — [Elite Trader: NYSE auction data](https://www.elitetrader.com/et/threads/nyse-auction-data.281048/post-3924556)
- A user with Yahoo-sourced quotes saw a wrong open, corrected the next day — [Medved Trader forum](https://forums.medvedtrader.com/topic/1292-low-and-open-quotes-of-the-day/)
- Open definition matters. QuantConnect reprocessed all US equity data since 2007 to use the *primary exchange's official auction price* instead of "the first tick in market hours" for open and close. This produced small (>0.1%) differences from other platforms — [QuantConnect forum #9345](https://www.quantconnect.com/forum/discussion/9345/opening-closing-auction-prices-20tb-200m-files-and-640-cores/p1) (post date not visible; older than 2024)
- Partial last candle: other vendors' guidance is to "ignore the last row" until the candle closes — [Kite forum](https://kite.trade/forum/discussion/10984/historic-data-for-nifty-options-sending-wrong-values-for-low-and-close). Some apps use different intraday and EOD sources, so the displayed close can lag the official close — [Banktivity](https://www.banktivity.com/support/articles/?p=4043)
- Yahoo-derived *monthly* average volume double-counted the last trading day. This was a calculation bug, not a daily-bar bug — [numerics.net](https://numerics.net/blog/yahoo-finance-miscalculates-monthly-average-daily-volume)

### Inferences
- **Field trust:** close is generally the most reliable field (closing auction). Open is reliable only after the opening cross is final and the vendor has replaced any first-trade value. That matches the repo's earlier finding that "provisional 9:35 opens" and early pulls had wrong opens. High and low are the most definition-sensitive fields, because trade-condition filters, odd lots and out-of-sequence prints differ by vendor. Volume is definition-dependent (consolidated or not, odd lots or not, late corrections).
- Regular-session OHLC on Yahoo daily bars excludes pre/post-market. Extended hours appear only with `prepost=True` on intraday intervals. This is not explicitly sourced for daily bars; check it by comparing against Moomoo `extended_time=0`.
- **Practical tolerances (proposal):** close ≤ 0.1% or $0.01; open ≤ 0.5%; high/low ≤ 1%; volume ≤ 15–25% relative, flagged rather than blocked. Use whichever is larger of the relative and the tick-absolute ($0.01–0.02) tolerance.

### Gaps
- No official Yahoo documentation of trade-condition filters, odd-lot inclusion or the OHLC source (SIP consolidated or primary listing) for daily bars.
- No 2025–2026 quantitative study of Yahoo against SIP or official auction prices. The 99.8% figure is anecdotal.

## 3. Moomoo/Futu OpenAPI kline semantics: adjustment (rehab), O/H/L definitions, discrepancies, rate limits

### Takeaway
The Moomoo MCP `quote_history_kline` used by the routines defaults to **forward adjustment (autype=1)**, which in the Futu convention includes cash dividends. Any comparison of older bars with Yahoo (split-only, no dividends) will drift by the cumulative dividend factor unless `autype=0` (none) is requested. Today's bar is not affected, because forward adjustment leaves the latest bars unchanged. Historical kline quota and per-interface rate limits apply, and sources conflict on a 30-day or 7-day quota window.

### Cited Findings
- MCP tool `mcp__Moo_Moo__quote_history_kline` schema: `autype` "0=None / 1=Forward / 2=Backward (默认值: 1)". `extended_time` "0=default (excluded) / 1=include pre/after-hours (US intraday K-line) / 2=include overnight session (US)". `ktype` 2 = day. `num` default and max is **370 bars** per call. Paging goes toward earlier data. "preferred stocks / SPACs / convertibles / CBBCs return empty" — Moomoo MCP tool schema loaded in this session (22 Oct 2026)
- MCP tool `mcp__Moo_Moo__quote_corporate_actions_rehab`: returns ex-rights/ex-dividend events "for client-side price adjustment". `divi_mode`: "exclude_divi = exclude cash dividends (Yahoo/Bloomberg convention); include_divi = include cash dividends (A-share/Futu convention, default)" — Moomoo MCP tool schema loaded in this session
- Futu OpenAPI Python `request_history_kline(code, start, end, ktype, autype, fields, max_count, page_req_key, extended_time, session)`. The adjustment parameter is `autype`, **default QFQ (forward)**. Paging is advised above 1,000 bars to avoid timeouts — [Futu OpenAPI: Get Historical Candlesticks](https://openapi.futunn.com/futu-api-doc/en/quote/request-history-kline.html) (via search summary; page not fetchable from sandbox)
- Each interface has its own frequency limit, listed under "Interface Limitations" at the bottom of each API page. "60 requests every 30 seconds" is the *market snapshot* example, not necessarily the kline limit — [Futu OpenAPI: Authorities and Limitations](https://openapi.futunn.com/futu-api-doc/en/intro/authority.html) (via search summary)
- Historical candlestick quota counts distinct securities pulled per window, and repeat pulls of the same stock in the window are free. Tiers: 100 (basic), 300 (assets > 10,000 HKD), then 1,000 and 2,000 by assets, orders or volume, over **30 days** — [moomoo support topic3_439](https://www.moomoo.com/us/support/topic3_439). This **conflicts with** the moomoo OpenAPI authority docs, which describe the quota as "total number of subjects pulling historical candlesticks per **7 days**" and say different periods for the same stock occupy one quota — [moomoo OpenAPI: Authorities and Quota](https://openapi.moomoo.com/moomoo-api-doc/en/intro/authority.html) (both via search summary). Usage can be checked with `get_history_kl_quota` — [Futu: Get Details of Historical Candlestick Quota](https://openapi.futunn.com/futu-api-doc/en/quote/get-history-kl-quota.html)
- Repo practice: after 10:00 NY the routine checks the official open with `quote_history_kline` (ktype 2, num 1) on a **sample of 5 stocks** (`BacktestShariah2/jadual/beli_0935.md:14`). The 14–21 Oct 2026 logs show every sample "SAMA dengan harga_beli sementara; tiada pembetulan" (`BacktestShariah2/standard/binaan_v2_log_tambahan.md:66,103,123,177,209,230`) — local repo files

### Inferences
- For **today's open**, forward-adjusted equals raw, so the current check is valid. For **any bar before a later dividend or split**, Moomoo autype=1 differs from Yahoo `auto_adjust=False`. Use `autype=0` and convert splits yourself with the rehab factors (`divi_mode=exclude_divi` gives the Yahoo/Bloomberg-compatible factor) before comparing.
- A 5-of-~N sample check cannot detect errors on individual names. Moomoo is the designated "official open" source, so a full-universe open comparison after the session should run where quota allows. Quota counts distinct symbols, so about 2,000 symbols exceeds the 100–2,000 tiers. Options are rotating subsets, or limiting to open positions and new buy candidates (the bars that actually move the Lejar).
- Moomoo's day kline excludes extended hours by default (`extended_time=0`), so its O/H/L/C are regular-session. That makes it a reasonable cross-check for Yahoo regular-session bars. I found no Futu statement on whether open is the official opening cross or the first trade.

### Gaps
- Exact kline frequency limit (requests per 30 s) and whether the quota window is 30 or 7 days in 2026. The pages could not be fetched, and the sources conflict.
- Futu's definition of daily open and high/low (auction or first trade; trade conditions; odd lots) and of volume (consolidated or not). Not documented in anything I found.
- No public reports found of systematic Futu US kline errors.

## 4. Free third sources in 2026: availability, limits, definitions, and which is best for daily-bar arbitration

### Takeaway
No free source covers about 2,000 stocks a day with an official-quality guarantee. The most practical arbitration sources are (a) **Alpaca's free market-data plan** (historical bars since 2016, 200 calls/min, full SIP for data older than 15 minutes per forum reports) and (b) **Massive (ex-Polygon) Basic** (EOD, 5 calls/min, 2 years). If grouped-daily is available on the free tier, one call covers the whole market per date; this is unverified. Tiingo, FMP, Alpha Vantage and EODHD are suited to disputes only (tens to hundreds of calls a day). Stooq has needed an API key since March 2026, and the Nasdaq.com endpoint is unofficial and fragile.

### Cited Findings
- **Alpaca (free):** historical data since 2016. Historical requests cannot cover the "latest 15 minutes". 200 historical calls/min. The paid tier ($99/mo) removes the restriction — [Alpaca docs: About Market Data API](https://docs.alpaca.markets/docs/about-market-data-api). A forum reply says free users "can access full market SIP quotes, trades and bars if less recent than 15 minutes". The official docs describe free *real-time* as IEX-only, and another forum post says free users get only IEX — [Alpaca forum](https://forum.alpaca.markets/t/solutions-for-getting-bars-missing-due-to-15-minute-historical-delay/8913) (conflict noted)
- **Massive (formerly Polygon.io; renamed Oct 2025; api.polygon.io and api.massive.com run in parallel with the same keys):** free Basic = EOD data, 5 calls/min, about 2 years of history, HTTP 429 when exceeded. Starter (~$29/mo) gives unlimited calls with 15-min delay — [quantt.co.uk Polygon tutorial](https://www.quantt.co.uk/resources/polygon-api-tutorial); [qveris pricing guide](https://qveris.ai/zh-cn/guides/polygon-pricing-optimized) (third-party, mid-2026). Day-aggregate flat files hold O/H/L/C/V and transaction count for all US equities (S3 bulk, plan-dependent) — [Massive docs: day aggregates](https://massive.com/docs/flat-files/stocks/day-aggregates.md)
- **Tiingo (free Starter):** there are request/hour and unique-symbol/month caps, but I found no 2026 numbers. Older figures (about 2020) were 500 requests/hour and 500 symbols/month — [Wealth-Lab forum (old)](https://wl6.wealth-lab.com/Forum/Posts/Why-Tiingo-works-on-some-but-fails-on-other-symbols-40475); [apievangelist](https://providers.apievangelist.com/providers/tiingo/). Dividends/splits endpoints need a paid plan per one MCP project's docs — [glama maverick-mcp tiingo config](https://glama.ai/mcp/servers/@wshobson/maverick-mcp/blob/e0e1dd2c7d5833cd01a7168f85f9f268758a8894/scripts/tiingo_config.py)
- **FMP (free Basic):** 250 calls/day, EOD historical, 150+ endpoints, 500 MB trailing-30-day bandwidth, no credit card — [FMP: choosing a plan](https://site.financialmodelingprep.com/insights/platform/how-to-choose-the-right-financial-modeling-prep-plan-for-your-workflow); [NexusFi](https://nexusfi.com/d/data-providers/financial-modeling-prep/). No symbol cap stated. One third-party article claims there is no free tier, which conflicts with FMP's own pages — [lambdafin](https://www.lambdafin.com/articles/financial-data-api-2026)
- **Alpha Vantage:** free is "up to 25 requests per day" — [Alpha Vantage support](https://www.alphavantage.co/support/). A third party adds 5/min — [Macroption](https://www.macroption.com/alpha-vantage-api-limits/). Realtime and 15-min-delayed US data is premium-only.
- **EODHD:** free is 20 calls/day (reset at midnight GMT, 429 when exceeded), 1-year EOD depth, plus a one-time 500-call welcome bonus — [EODHD pricing](https://eodhd.com/pricing?via=kmg); [apis.io rate limits](https://apis.io/rate-limits/eod-historical/eod-historical-rate-limits/). One third party says the 1-year limit applies only to demo tickers, which conflicts with others — [apis.io plans](https://apis.io/plans/eodhd/eodhd-plans-pricing/)
- **Stooq:** since about March 2026, downloads need an API key. Keyless requests return HTML, not CSV, which breaks pandas-datareader. The key comes from `stooq.com/q/d/?s=spy.us&get_apikey` (issue opened 13 Apr 2026) — [pandas-datareader #1012](https://github.com/pydata/pandas-datareader/issues/1012). The key is obtained via CAPTCHA, and there is a daily hit limit ("Exceeded the daily hits limit") — [apievangelist: Stooq](https://providers.apievangelist.com/providers/stooq/). A user reported IP blocking after limits — [Fund Manager forum](https://fundmanagersoftware.com/forum/viewtopic.php?p=28752). Arbitrary date-range selection was blocked "because people were abusing it" (user report) — [AmiBroker forum](https://forum.amibroker.com/t/stooq-pl-excess-bars-downloaded/40687)
- **Nasdaq.com:** unofficial JSON endpoint `api.nasdaq.com/api/quote/{SYM}/historical?assetclass=stocks&fromdate=…&todate=…&limit=…`, which "may change its API structure over time" — [Apify](https://blog.apify.com/scrape-nasdaq-stock-market-data-python/). It needs browser-like headers (`User-Agent`, `accept: application/json`) — [Bright Data](https://brightdata.com/blog/web-data/how-to-scrape-nasdaq.md). The unofficial wrapper warns users to check Nasdaq's ToS — [deepentropy/nasdaqapi](https://github.com/deepentropy/nasdaqapi)

### Inferences
- **Ranking for arbitration (proposal):**
  1. Alpaca free: if SIP historical holds, it has consolidated volume and official-style daily bars, enough throughput for the full universe (multi-symbol bar requests at 200/min), and history since 2016. It needs a free account, and the key is stored as a GitHub secret.
  2. Massive Basic: independent of Yahoo. At 5/min, per-ticker calls take about 7 h for 2,000 tickers, so use it only for disputed tickers unless grouped-daily is allowed on the free tier.
  3. Tiingo, FMP, Alpha Vantage, EODHD: dispute-only budgets (roughly 25–250 per day).
  4. Stooq and Nasdaq: last resort. The CAPTCHA key and limits make Stooq poor for automation, and the Nasdaq endpoint has ToS and fragility issues.
- Vendors often derive their data from the same upstream feeds, so agreement between two vendors is weaker evidence than it looks. Prefer an arbitrator with a different lineage from Yahoo (SIP via Alpaca or Massive).
- The third source should compare **unadjusted** bars. Alpaca and Massive both expose an adjustment parameter. Request raw prices and apply your own split factors.

### Gaps
- 2026 Tiingo free-tier numbers. The pricing page could not be fetched.
- Whether Massive grouped-daily (`/v2/aggs/grouped/...`) is on the free tier, and its adjusted default.
- Whether Alpaca free gives SIP historical *daily* bars today (forum and docs conflict), and whether a free market-data account needs brokerage KYC.
- No live test of any endpoint was possible from the sandbox (proxy 403). A GitHub Actions smoke test is needed.

## 5. Validation best practices: invariants, outliers, calendar, cross-vendor tolerance, snapshots/hashing, adjustment tracking, disagreement policy

### Takeaway
Academic and practitioner evidence agrees that unscreened vendor data can change conclusions, and that screening against a reference fixes most of it. For this system the gaps are: (1) exact-session gating, (2) quarantine instead of silent overwrite, (3) a split-aware revision detector replacing the blunt ">0.3% → rescale" rule, and (4) immutable raw snapshots with hashes so every Lejar rebuild is tied to a known store version.

### Cited Findings
- Ince & Porter (2006) compared Datastream US individual equity returns with CRSP. They found coverage, classification and integrity problems. Naive use "can noticeably change economic conclusions", and after careful screening inferences resemble CRSP's — [Ince & Porter, J. Financial Research 29(4):463–479 (IDEAS)](https://ideas.repec.org/a/bla/jfnres/v29y2006i4p463-479.html)
- Practitioners check spikes against other vendors. In a WealthData review, most flagged spikes were also present elsewhere (real moves), and one missing date was filled — [Wealth-Lab forum](https://wealth-lab.com/Discussion/Are-these-WealthData-data-points-correct-12729)
- Yahoo sometimes fails to adjust on split day, and repair needs at least one day after the split. Reconstructed data can differ from Yahoo's later correction — [yfinance wiki: Price repair](https://github.com/ranaroussi/yfinance/wiki/Price-repair)
- Unscheduled closures happen. NYSE and Nasdaq closed on **9 Jan 2025** (National Day of Mourning, President Carter) — [Nasdaq](https://www.nasdaq.com/articles/stock-market-will-be-closed-january-9-2025). A calendar library must be updated for such days.
- Vendors publish restatements. For example, S&P Global Platts published lists of corrected database records where high and low values had been transposed — [S&P Global Platts subscriber note](https://www.spglobal.com/commodity-insights/en/pricing-benchmarks/our-methodology/subscriber-notes/082517-platts-restates-database-records-for-certain-physical-market-data-categories)
- The repo already publishes sha256 manifests for AUTOTUNE Release data ("sha256 dalam manifest.json") — local `/home/user/papertrade-claude/.github/workflows/autotune_data.yml:87`

### Inferences (proposed validation design, implementable with pandas, exchange_calendars, hashlib and git)
**A. Ingestion gating (before any bar enters the store)**
1. A bar for session D is accepted as *final* only if it was fetched after D's close (use `exchange_calendars` XNYS `session_close`, including 13:00 ET early closes) plus a buffer. The repo's empirical buffer is after 00:20 UTC. Otherwise it is stored as `provisional` and must be overwritten by a later final fetch.
2. The session set must equal the XNYS sessions in the window. A missing session for more than 30% of tickers is a vendor outage: retry later and never forward-fill. A missing session for one ticker counts toward the "no bar" counter only if the fetch for that ticker succeeded (not a 429 or empty frame).
3. Record per fetch: vendor, endpoint, parameters (`auto_adjust`, `autype`), library versions, UTC fetch time, HTTP status, and row count.

**B. Row invariants (hard fail → quarantine, do not write)**
- O, H, L, C finite and > 0. V ≥ 0, integer-valued, not NaN.
- L ≤ min(O, C) ≤ max(O, C) ≤ H, and L ≤ H.
- No duplicate dates, no non-session dates, timezone-naive session dates (America/New_York date).
- For the ≥ $10 universe: C_t/C_{t−1} or O_t/C_{t−1} within [0.0095, 0.0105] or [95, 105] → 100x suspect.

**C. Time-series soft flags (→ cross-vendor check, not auto-fix)**
- Return spike: |ln(C_t/C_{t−1})| > max(25%, 8 × rolling MAD of 60 bars).
- **Reversal test** (Ince-Porter style, thresholds are mine): r_t and r_{t+1} of opposite sign, both > 20%, and |(1+r_t)(1+r_{t+1})−1| < 5% → a likely single-bar error.
- Open gap |O_t/C_{t−1}−1| > 20%, or range H/L−1 > 40%.
- Ratio C_{t−1}/C_t ≈ a common split ratio (2, 3, 4, 5, 10, 20, 1/2, 1/3, 1/5, 1/10, 1/20, 3/2, 2/3; ±2%) with no split recorded → split/adjustment suspect.
- Volume > 20× or < 0.05× the 20-bar median. Zero volume with a price change.
- Flat bar O=H=L=C with V>0 (already partly covered by the illiquidity rule in `kod/tidak_layak.py`).

**D. Cross-vendor tolerance rules (Yahoo against Moomoo `autype=0`, and the arbitrator when needed)**
- Compare raw against raw, after converting for splits only. Never compare Yahoo with Moomoo forward-adjusted older bars.
- Close: |Δ| ≤ max(0.1%, $0.01). Open: ≤ max(0.5%, $0.02). High/Low: ≤ max(1%, $0.02). Volume: ≤ 20% (flag only).
- Classify each mismatch: single-field (likely a definition difference or provisional value) or all-fields-by-a-constant-ratio (an adjustment problem).

**E. Which vendor to trust for which field (proposal)**
- Open: Moomoo `autype=0` day kline, final only after the session ends. Yahoo is the backup.
- Close: Yahoo and Moomoo should agree within 0.1%. If they disagree, the arbitrator decides.
- High/Low: Yahoo, flagged if it differs from Moomoo by more than 1%. The arbitrator decides only when the field feeds a signal or exit (Chandelier uses close, so high/low are lower-stakes except for ATR).
- Volume: Yahoo (consolidated) for liquidity rules. Do not arbitrate small differences.
- Corporate actions (splits): Moomoo `quote_corporate_actions_rehab` (`divi_mode=exclude_divi`) and yfinance `splits` must agree before any history rescale.

**F. Disagreement handling**
- A disputed bar keeps its prior stored value (or is marked `disputed` if new) and is *excluded from new buy or exit decisions* until resolved. Re-fetch from both vendors at T+1 and T+2, since Yahoo often corrects the next day (section 2).
- Still disputed after T+2: take the 2-of-3 majority with the arbitrator. If there is no majority, use the Moomoo value for open and the Yahoo value for close/volume, and log the decision.
- Every correction goes to an append-only log (`ticker, date, field, old, new, source, reason, run_id`). The Lejar rebuild reads only the store plus this log, so changes are explicit.

**G. Snapshots, hashing and silent-revision detection**
- Keep immutable raw pulls (gzip CSV/Parquet per run, or a git-tracked raw directory) with a manifest of sha256 per file and per ticker. Also keep a per-(ticker, date) row hash of OHLCV rounded to 4 dp.
- On each pull, compare the overlapping history (the last 10 sessions; a weekly full 520-bar re-pull of a rotating 1/5 of the universe). Classify any change to a bar older than T−2 as:
  - (i) **split**: a uniform ratio across all overlapping bars (dispersion < 0.05%) that matches a known split → apply the factor to all history and log it;
  - (ii) **dividend-only**: only Adj Close changed → ignore for the raw store;
  - (iii) **anomaly**: a non-uniform change → quarantine, keep the old value, and cross-check.
- **Replace the current rule** ("overlapping closes differ >0.3% → rescale old history"). Under that rule, one bad Yahoo bar (100x, a provisional value, or the split-day missing adjustment) can rescale three years of history. Require ratio uniformity across overlapping bars and a matching split event.
- Tie each Lejar rebuild to a store version (git commit or manifest hash) and record that hash in the Lejar output, so rebuild differences can be traced to specific bar revisions.

**H. Adjustment-factor tracking**
- Store raw unadjusted (or Yahoo split-adjusted with explicit factors) prices plus a separate factors table (ex-date, split ratio, dividend, source). Compute adjusted series on the fly. Never store only adjusted prices. Note that some repo jobs (`gred_kumpulan.py`, `sejarah_pemangkin_actions.py`) use `auto_adjust=True` series that differ from the store.

**I. Library and calendar pinning**
- Pin yfinance, curl_cffi, pandas and exchange_calendars. Update exchange_calendars deliberately when ad-hoc closures are announced (e.g. 9 Jan 2025), and run a test that today's expected session exists.

### Gaps
- Exact Ince & Porter screen thresholds were not retrieved (the paper is behind a DOI). The thresholds above are proposals, not taken from the paper.
- No published, sourced tolerance standards for cross-vendor daily OHLC. The tolerances above are engineering proposals informed by the definitional differences cited (auction against first tick, more than 0.1%; volume filtering up to about 50%).
- I did not confirm which `exchange_calendars` version added 9 Jan 2025.

## 6. How professional pipelines (QuantConnect, Norgate, CRSP-like, zipline, OpenBB) handle vendor errors and reconciliation

### Takeaway
Professional pipelines share four patterns. They define prices canonically (official auction open/close). They keep raw prices separate from adjustment factors. They reprocess history openly instead of patching it silently. And they have an issue-report and verify loop. Survivorship-free coverage (delisted names kept) is treated as part of data quality.

### Cited Findings
- **QuantConnect:** reprocessed all US equity trades and quotes since 2007 so that open and close are the primary exchange's official auction prices, not the first tick. Users report suspected errors through a Data Explorer "Issues" form with a reproducing backtest or notebook. The Data Team verifies and fixes, and users must check open issues first — [QC forum #9345](https://www.quantconnect.com/forum/discussion/9345/opening-closing-auction-prices-20tb-200m-files-and-640-cores/p1); [QC docs: Data Issues](https://www.quantconnect.com/docs/v2/cloud-platform/datasets/data-issues). Mismatches with Yahoo are often explained by split/dividend adjustment or intraday timing of the history request — [QC forum: prices not matching Yahoo](https://www.quantconnect.com/forum/discussion/19519/historic-prices-not-matching-yahoo-historic-reports/)
- **Zipline bundles:** a bundle is "pricing data, adjustment data, and an asset database". Splits and dividends are stored as adjustments, not baked into OHLC — [zipline docs: bundles.rst](https://github.com/quantopian/zipline/blob/master/docs/source/bundles.rst)
- **Norgate:** survivorship-bias-free listed and delisted US data with historical index constituents. Clients can configure how history is adjusted and/or padded (all, special or no dividends) — [Wealth-Lab Norgate extension](https://www.wealth-lab.com/extension/detail/Norgate); [NexusFi](https://nexusfi.com/d/data-providers/norgate-data/). Corrections are reported to Norgate, which fixes its central database, while local data is a cache — [Wealth-Lab forum](https://wealth-lab.com/Discussion/Norgate-Current-amp-Past-DataSets-Have-Wrong-Bar-Count-13140)
- **CRSP standard:** Yahoo's adjusted close follows CRSP multiplier conventions — [Yahoo Help SLN28256](https://help.yahoo.com/kb/SLN28256.html). The Datastream-against-CRSP benchmark shows CRSP used as the reference "gold" source — [Ince & Porter (IDEAS)](https://ideas.repec.org/a/bla/jfnres/v29y2006i4p463-479.html)

### Inferences
- What transfers to this system:
  1. Define "official open" as the auction price, with Moomoo as the reference, and hold the bar as provisional until it is final.
  2. Keep raw and factors separate (zipline-style).
  3. Keep an issue log with a verify step (QuantConnect-style), not ad-hoc overwrites.
  4. Never drop delisted names from the store or Lejar (Norgate-style survivorship-free). This is consistent with the repo's `delist` exit reason.
- Being open about reprocessing (QuantConnect's announcement) fits the repo's need: any history revision that changes the Lejar should be recorded in a commit message or log the user can read.

### Gaps
- I found no primary documentation of Norgate's or CRSP's internal QA or reconciliation processes, and nothing on OpenBB's multi-provider reconciliation (OpenBB appears to pass through provider data without arbitration, but this is unverified).
- No zipline-reloaded documentation was found on OHLC validation at ingest.
