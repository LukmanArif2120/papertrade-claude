# Academic literature: industry information diffusion (lead-lag), intra-industry short-term reversal, and what they imply for an industry-strength grade (US stocks, 10–21 trading days)

Method note (read first): during this research session WebFetch and curl could not reach any external domain (DNS/proxy errors on SSRN, NBER, OUP, NUS, CXO, RePEc, NY Fed). Every finding below therefore comes from WebSearch result summaries of abstracts, working-paper PDFs and listing pages. I have not read the regression tables myself. Numbers marked "(version-dependent)" differ between working-paper and published versions. Check exact figures against the published PDFs before using them in a final document. Where I give a number from memory without a retrievable source, I put it under Gaps rather than Findings.

Context being tested: our own 2005–2026 test (3,418 US stocks, Moomoo industries) found the industry grade predicts small stocks (A−E spread +0.7% per 21 days, t≈2.3) but not large stocks (≈0).

---

## 1. Hou (2007, RFS): intra-industry lead-lag, big firms lead small firms

### Takeaway
Hou finds the big-to-small lead-lag is mostly an intra-industry effect caused by slow diffusion of industry news. It is stronger for small, less competitive and neglected industries, and is driven mainly by slow reaction to bad news. This directly supports our finding that an industry signal predicts small stocks but not large ones.

### Cited Findings
- Citation: Kewei Hou, "Industry Information Diffusion and the Lead-Lag Effect in Stock Returns", *Review of Financial Studies* 20(4), 2007, pp. 1113–1138 — [IDEAS/RePEc](https://ideas.repec.org/a/oup/rfinst/v20y2007i4p1113-1138.html); [SSRN 463005](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=463005)
- Abstract claims: "the slow diffusion of industry information is a leading cause of the lead-lag effect in stock returns"; "the lead-lag effect between big firms and small firms is predominantly an intra-industry phenomenon" — [IDEAS](https://ideas.repec.org/a/oup/rfinst/v20y2007i4p1113-1138.html); [SUFE academic newsletter summary](https://academicnewsletter.sufe.edu.cn/info/355345)
- Little evidence of cross-industry predictability remains once the within-industry effect is accounted for — [SSRN abstract](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=463005) (via search summary)
- The effect "is driven by sluggish adjustment to negative information" — [IDEAS](https://ideas.repec.org/a/oup/rfinst/v20y2007i4p1113-1138.html)
- "Small, less competitive and neglected industries experience a more pronounced lead-lag effect" — [IDEAS](https://ideas.repec.org/a/oup/rfinst/v20y2007i4p1113-1138.html)
- The lead-lag "is related to the post-announcement drift of small firms following the earnings releases of big firms within the industry" — [IDEAS](https://ideas.repec.org/a/oup/rfinst/v20y2007i4p1113-1138.html)
- Sample described by a secondary source as US stocks, July 1963 – December 2001 — [Financial Innovation (2022), industry lead-lag US vs other countries](https://jfin-swufe.springeropen.com/articles/10.1186/s40854-022-00439-1)
- Replicated outside the US: within the same industry, big-firm returns significantly lead small-firm returns on the Taiwan Stock Exchange — [NTU thesis listing](https://tdr.lib.ntu.edu.tw/jspui/handle/123456789/37601) (via search summary)

### Inferences
- The lead-lag runs one way: big firms' returns contain the industry news first and small firms catch up later. An industry signal should therefore help forecast small/lagging stocks and add little for large stocks, which already price the news. This matches our small-versus-large split.
- An industry grade may be more informative if it is computed from the industry's **large/leader firms** (value-weighted or top-N by market cap) and then applied to the industry's **small** members, instead of being an equal-weighted average that mixes leaders and laggards.
- Because the effect is "driven by sluggish adjustment to negative information", the grade may carry more information on the weak side (D/E industries: avoid small stocks) than on the strong side (A: buy). For a long-only Shariah strategy, this means the grade may work better as a **filter** (exclude small stocks in E industries) than as a ranking for buys. Our A−E spread should be split into A-vs-middle and middle-vs-E legs to test this.
- Hou's horizon is short (the lead-lag is usually measured on weekly returns). That is compatible with a 10–21 trading-day hold, and suggests the edge is front-loaded in the first one or two weeks after signal formation.

### Gaps
- I could not retrieve Hou's regression coefficients, the weekly horizon specification, or the size of results split by analyst coverage or institutional ownership. The full text (OUP, SSRN) was unreachable. My recollection is that Hou uses weekly returns, but I could not verify it here.

---

## 2. Hong, Torous & Valkanov (2007, JFE): do industries lead the market?

### Takeaway
Some industry returns (retail, services, commercial real estate, metal, petroleum) forecast the aggregate market by up to two months. This is consistent with gradual diffusion **across** markets, but it is a market-timing result, not a cross-sectional stock-picking result.

### Cited Findings
- Harrison Hong, Walter Torous, Rossen Valkanov, "Do industries lead stock markets?", *Journal of Financial Economics* (2007): "a significant number of industry returns, including retail, services, commercial real estate, metal, and petroleum, forecast the stock market by up to two months" — [SUFE academic newsletter summary](https://academicnewsletter.sufe.edu.cn/info/357378)
- An industry's ability to forecast the market is correlated with its propensity to forecast indicators of economic activity; the eight largest non-US markets show "remarkably similar patterns"; the authors conclude that "information diffuses only gradually across markets" — [SUFE summary](https://academicnewsletter.sufe.edu.cn/info/357378)

### Inferences
- This paper supports the "slow diffusion" mechanism in general. It does not show that a stock's own industry grade predicts that stock's return relative to other stocks. It is only indirectly relevant to designing a stock-level grade.
- A possible secondary use: aggregate strength in certain leading industries could serve as a market-regime input (risk-on/risk-off). That is a separate design question.

### Gaps
- I could not verify the often-quoted "14 of 34 industries" count or the coefficient magnitudes; no retrieved source stated them.
- Later papers dispute how robust the result is out of sample, but I did not retrieve one in this session.

---

## 3. Cross-industry and economic-link predictability: Menzly & Ozbas (2010), Cohen & Frazzini (2008), Cohen & Lou (2012)

### Takeaway
News spreads slowly along supplier/customer and conglomerate links. The predictability is larger where fewer informed investors are present (low analyst coverage and institutional ownership). Monthly long-short alphas are about 1–1.5%, horizons are about one month, and these effects are distinct from a stock's own industry.

### Cited Findings
- Menzly & Ozbas, "Market Segmentation and Cross-predictability of Returns", *Journal of Finance* 65(4), 2010, pp. 1555–1580: returns of stocks in economically related **supplier and customer industries** cross-predict each other, and "the degree of cross-predictability decreases with the number of informed investors in the market as approximated by analyst coverage and institutional ownership"; changes in institutional holdings line up with how the model says informed investors should trade — [IDEAS/RePEc](https://ideas.repec.org/a/bla/jfinan/v65y2010i4p1555-1580.html); [SUFE summary](https://academicnewsletter.sufe.edu.cn/info/360512); [JF Internet Appendix](https://afajof.org/wp-content/uploads/files/supplements/Internet_Appendix_to_Market_.pdf)
- Cohen & Frazzini, "Economic Links and Predictable Returns", *Journal of Finance* 63(4), 2008: stocks sorted on the **prior month's** return of their principal customers. The abstract reports a long/short alpha of "over 150 basis points per month"; the text describes abnormal returns of **1.55% per month (18.6% per year)**; one version reports a baseline customer-momentum alpha of **1.3% per month (t = 4.93)** (version-dependent) — [Frazzini NYU PDF](https://pages.stern.nyu.edu/~afrazzin/pdf/Economic%20Links%20and%20Predictable%20Returns%20-%20Cohen%20and%20Frazzini.pdf); [Yale working paper](http://www.econ.yale.edu/~shiller/behfin/2006-04/cohen-frazzini.pdf); [SSRN 2758776](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2758776)
- Out-of-sample: a 2023 replication finds customer momentum persists after the original sample period, with monthly raw returns of **122 bp (equal-weighted) and 106 bp (value-weighted)**, which "do not decrease significantly after controlling for traditional asset pricing factors" — [arXiv 2301.11394, "Customer Momentum"](https://arxiv.org/pdf/2301.11394)
- Cohen & Lou, "Complicated Firms", *JFE* 104(2), 2012, pp. 383–400: a pseudo-conglomerate built from stand-alone firms in each conglomerate's segment industries predicts conglomerate returns. Long-short return reported as **95 bp per month value-weighted (t = 3.18)** in the LSE working-paper version and **118 bp per month before transaction costs** in another copy (version-dependent) — [LSE working paper](https://personal.lse.ac.uk/loud/coh_lou.pdf); [Colorado copy](https://leeds-faculty.colorado.edu/bhagat/Complicated%20Firms.pdf); [IDEAS](https://ideas.repec.org/a/eee/jfinec/v104y2012i2p383-400.html)

### Inferences
- The mechanism is limited attention and specialization (Menzly-Ozbas). It predicts that **stocks with low analyst coverage and low institutional ownership** lag their linked industries the most. This again points to small or neglected stocks as where an industry or linked-industry grade should work.
- Cohen-Lou implies the information flows **from easy-to-analyse firms (single-segment, pure-play) to hard-to-analyse firms (multi-segment)**. An industry grade built from pure-play firms could be applied to conglomerates whose segments span several Moomoo industries, but that needs segment data.
- These links all have roughly one-month horizons, which matches our 10–21 trading-day hold.

### Gaps
- I could not retrieve Menzly-Ozbas's return magnitudes (monthly alpha of the cross-industry strategy) or its results by size group.
- Out-of-sample decay of Menzly-Ozbas and Cohen-Lou after 2010 was not found.

---

## 4. Short-term reversal within industries: Hameed & Mian (2015), Da, Liu & Schaumburg (2014), Moskowitz & Grinblatt (1999)

### Takeaway
At a one-month horizon, **industries show momentum but individual stocks reverse relative to their industry**. Intra-industry reversals are larger than the conventional reversal and are present in large, liquid stocks too. The same industry signal can therefore help small stocks (lead-lag catch-up) while being offset in large stocks by within-industry reversal. A good industry grade should separate the industry component from the stock-minus-industry component.

### Cited Findings
- Hameed & Mian, "Industries and Stock Return Reversals", *JFQA* 50(1–2), 2015, pp. 89–117 (doi:10.1017/S0022109014000404): reversals within industries at the monthly horizon are "larger in magnitude, consistently present over time, and prevalent across subgroups of stocks, including large and liquid stocks" — [Cambridge abstract](https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/abs/industries-and-stock-return-reversals/92B5101FBEA7B40717D46DB60913BF41); [IDEAS](https://ideas.repec.org/a/cup/jfinqa/v50y2015i1-2p89-117_00.html); [PolyU listing](https://research.polyu.edu.hk/en/publications/industries-and-stock-return-reversals/)
- Mechanism: reversals are attributed to order imbalances and non-informational shocks, i.e. compensation for providing liquidity. They are stronger after aggregate market declines and in volatile periods — [Cambridge abstract](https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/abs/industries-and-stock-return-reversals/92B5101FBEA7B40717D46DB60913BF41)
- Decomposition: the unconditional reversal is split into a within-industry and an inter-industry component; the intra-industry reversal exceeds the unconditional one when the inter-industry component has momentum — [Cambridge abstract via search](https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/abs/industries-and-stock-return-reversals/92B5101FBEA7B40717D46DB60913BF41)
- Early draft (Hameed, Huang & Mian, about 2010, 24 industries), as summarized by CXO Advisory: intra-industry long-short reversal of about **1.46% per month** versus about **1.05%** for the same strategy across the whole market (draft numbers; published figures may differ) — [CXO Advisory](https://www.cxoadvisory.com/momentum-investing/short-term-reversal-by-industry)
- Later work builds industry-adjusted contrarian portfolios by sorting on industry-adjusted returns — [Cheng, Hameed, Subrahmanyam & Titman (2017, JFQA)](https://si-cheng.net/wp-content/uploads/2018/12/2017-JFQA-Cheng_Hameed_Subrahmanyam_Titman-Short-Term-Reversals.pdf)
- Da, Liu & Schaumburg, "A Closer Look at the Short-Term Return Reversal", *Management Science* 60(3), 2014, pp. 658–674 (working paper: NY Fed Staff Report 513, "Decomposing Short-Term Return Reversal", 2011). The standard reversal profit is split into (i) **across-industry momentum**, (ii) within-industry variation in expected returns, (iii) under-reaction to within-industry cash-flow news (analyst forecast revisions), and (iv) a residual. Only the residual (reaction to non-fundamental price moves) is significant and positive. The residual-based strategy earns a risk-adjusted return about **three times** (working paper, 1982–2009) or **four times** (published version) that of the standard reversal (version-dependent) — [NY Fed SR513](https://newyorkfed.org/medialibrary/media/research/staff_reports/sr513.html); [EconPapers](https://econpapers.repec.org/RePEc:fip:fednsr:513); [SUFE summary](https://academicnewsletter.sufe.edu.cn/info/393770)
- NY Fed report: because of industry momentum, "implementing the short-term reversal strategy within an industry is more profitable than implementing it across the board" — [NY Fed SR513 PDF](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr513.pdf) (via search summary)
- Moskowitz & Grinblatt, "Do Industries Explain Momentum?", *JF* 54(4), 1999, pp. 1249–1290: industry momentum accounts for much of individual-stock momentum, and industry strategies stay profitable after controlling for stock momentum — [IDEAS](https://ideas.repec.org/a/bla/jfinan/v54y1999i4p1249-1290.html). Arnott, Clements, Kalesnik & Linnainmaa cite them for the point that industry return predictability is **strongest at the one-month horizon**, and argue industry momentum derives from factor momentum — [Research Affiliates](https://www.researchaffiliates.com/insights/journal-papers/709-factor-momentum); [Linnainmaa et al. WP](https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2018/03/Juhani.pdf)
- At the industry level, buying one-month loser industries and selling one-month winners earns a **negative** profit, i.e. one-month momentum, while individual stocks reverse — [search summary of academic work; see Georgia Southern listing on simultaneous reversal and momentum](https://scholars.georgiasouthern.edu/en/publications/the-role-of-industry-effects-in-simultaneous-reversal-and-momentu-4/)
- Contrary international evidence: in Australia, intra-industry reversals were found in large stocks, but industry momentum dominated — [Chai & Do (2016), Monash](https://research.monash.edu/en/publications/co-existence-of-short-term-reversals-and-momentum-in-the-australi/)

### Inferences
- **Key design point.** A stock's one-month return = industry component (which continues) + stock-minus-industry component (which reverses, and does so in large stocks too). If the grade or its companion signals use the stock's own recent return, the two components partly cancel. For **large stocks** a plausible reading of our near-zero result is: (a) large stocks already priced the industry news (Hou: they lead), and (b) any large stock that has outrun its strong industry tends to give some back (Hameed-Mian). Both push the industry-grade payoff for large caps toward zero.
- Practical implication: for large stocks, the industry grade may still help when **combined with intra-industry reversal**: prefer large stocks in strong (A/B) industries that have **lagged** their industry over the past 1–4 weeks, and avoid ones that have led it. That combines industry momentum with within-industry reversal, which DLS suggest is cleaner than either alone.
- For small stocks, the industry grade captures lead-lag catch-up, which is the effect our test found.
- Liquidity-driven reversal is stronger after market declines and in volatile periods (Hameed-Mian). After sell-offs, "buy the laggard in a strong industry" should work better; in calm trending markets, plain industry momentum should dominate. A regime conditioner (VIX or recent market drawdown) is worth testing.
- Moskowitz-Grinblatt's finding that industry predictability is strongest at the **one-month** horizon matches a 10–21 trading-day hold. The industry grade should be weighted toward recent returns (1 month, perhaps 1–3 months), not only 6–12 months.

### Gaps
- I could not verify the published Hameed-Mian monthly profits, t-statistics, or size-quintile breakdown (the NUS PDF and Cambridge full text were unreachable). The 1.46% vs 1.05% figures are from a draft, via a secondary source.
- I could not retrieve exact Moskowitz-Grinblatt one-month industry momentum numbers or their within-industry stock reversal tables.
- I did not find Da-Liu-Schaumburg's component magnitudes (monthly bp per component).

---

## 5. Better peer definitions: Hoberg & Phillips text-based industries (TNIC), Lee-Sun-Wang-Zhang technological links, Ali & Hirshleifer shared analyst coverage

### Takeaway
Peer momentum is much stronger when peers are **less visible** (text-based product peers, technology peers, shared-analyst peers) than with standard SIC-type industries. Shocks to visible SIC peers transmit within **1–2 months** and are small and short-lived. Connected-firm (shared-analyst) momentum subsumes industry momentum in spanning tests. A standard, visible industry classification such as Moomoo's should give only a modest and fast-fading edge, which fits our modest t≈2.3 for small stocks.

### Cited Findings
- Hoberg & Phillips, "Text-Based Industry Momentum", *JFQA* 53(6), 2018: using 10-K TNIC peers, "industry momentum profits are highly robust and substantially larger than previously documented"; shocks to **less visible** peers generate large momentum profits, stronger than own-firm momentum; **more visible traditional SIC-based peers generate only small, short-lived momentum profits**; SIC-peer shocks transmit to the focal firm **in 1 to 2 months**, while TNIC-peer shocks take **up to 12 months** — [Dartmouth WP PDF](https://faculty.tuck.dartmouth.edu/images/uploads/faculty/gordon-phillips/hoberg_phillips_TNICmomJFQA_FinV1.pdf); [Cambridge published PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/6E04891A7AD30C24C21CBDE37EC06BF4/S0022109018000479a.pdf/textbased_industry_momentum.pdf)
- Working-paper magnitudes (early draft; check published tables): 6-month impact of a TNIC-3 peer's monthly return = **0.008 per sigma**, vs **0.004** for Fama-French 48 peers; TNIC-3 cumulative coefficient **0.013** over one year. Only shocks to less visible **horizontal** peers (not vertical) explain own-firm momentum — [Dartmouth WP PDF](https://faculty.tuck.dartmouth.edu/images/uploads/faculty/gordon-phillips/hoberg_phillips_TNICmomJFQA_FinV1.pdf) (via search summary)
- Lee, Sun, Wang & Zhang, "Technological Links and Predictable Returns", *JFE* 132(3), 2019, pp. 76–96: a long-short strategy based on returns of technology-linked firms (patent-based closeness) earns a **monthly alpha of 117 bp**. The effect is distinct from industry momentum and strongest for firms with a more concentrated technology focus and **lower investor attention** — [CityU Scholars](https://scholars.cityu.edu.hk/en/publications/technological-links-and-predictable-returns/); [Semantic Scholar](https://www.semanticscholar.org/paper/Technological-Links-and-Predictable-Returns-Lee-Sun/a459bd6eadfb69a88408ee5d1097755885a0e899)
- Ali & Hirshleifer, "Shared Analyst Coverage: Unifying Momentum Spillover Effects", *JFE* 136(3), 2020, pp. 649–675: a connected-firm (CF) momentum factor earns a **monthly alpha of 1.68% (t = 9.67)**. After controlling for CF momentum, the alphas of **industry**, geographic, customer, customer/supplier industry, single-to-multi-segment and technology momentum factors are **insignificant or negative**. Effects are stronger for complex and indirect links, and similar results hold in developed international markets. Mechanism: slow updating by analysts and investors — [SSRN 3015582](https://papers.ssrn.com/abstract=3015582); [NBER w25201](https://www.nber.org/system/files/working_papers/w25201/w25201.pdf); [published JFE PDF (author site)](https://cpb-us-e2.wpmucdn.com/sites.uci.edu/dist/c/362/files/2020/07/SharedAnalystCoverage-UnifyingMomentumSpilloverEffects-AliHirshleifer-PUBLISHED-JFE2020.pdf); [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0304405X19302533)
- Recent JFQA paper "Decoding Momentum Spillover Effects": spillover from linked firms comes from an overnight/intraday "tug of war". Peer overnight returns carry into the focal stock's overnight return and then reverse intraday; peer intraday returns predict focal intraday returns. Attributed to persistent individual-investor demand distorting opening prices, with slow professional arbitrage. The internet appendix finds spillover weakens with longer formation horizons and no spillover for connected-firm overnight returns — [Cambridge](https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/decoding-momentum-spillover-effects/EB6BE5A096753108881E1514E54035DF); [Internet Appendix](https://static.cambridge.org/content/id/urn:cambridge.org:id:article:S002210902510238X/resource/name/S002210902510238Xsup001.pdf)

### Inferences
- Moomoo industries are a visible, SIC-type grouping. Hoberg-Phillips predict a **small and quick** payoff (1–2 months) from such peers. That matches a 10–21 day hold, and suggests a 21-day hold may already capture most of what is available; longer holds should add little.
- Ali-Hirshleifer suggest the industry grade is a noisy proxy for a richer "connected firm" network. If data allow, weighting peers by shared analyst coverage (or by return correlation/co-movement as a cheap proxy) could raise the signal. Without analyst-coverage data, this is a possible later upgrade, not a first step.
- For the grade, measure the **intraday** part of industry returns separately from the overnight part (Decoding Momentum Spillover). If we only have daily close-to-close data, that is not feasible; note it as a limitation.

### Gaps
- Published TNIC momentum alphas (monthly, by size) were not retrieved.
- I could not confirm whether Ali-Hirshleifer report CF momentum separately for large-cap and small-cap stocks; the NBER/SSRN PDFs were unreachable.

---

## 6. Do these effects persist for large caps and after 2010?

### Takeaway
The literature consistently finds industry lead-lag concentrated in **small, thinly traded, low-coverage** stocks. Within-industry reversal is the effect documented to hold in large, liquid stocks. Direct evidence on post-2010 decay of industry lead-lag in US large caps is thin. Practitioner evidence suggests 12-month industry momentum weakened after 2009 while one-month reversal became stronger. Overall, our result (works for small stocks, about zero for large stocks) is **confirmed, not contradicted**, by the literature.

### Cited Findings
- Parsons, Sabbatucci & Titman, "Geographic Lead-Lag Effects", *RFS* 33(10), 2020, pp. 4721–4770: **industry lead-lag effects are concentrated in small, thinly traded stocks with low analyst coverage**, while geographic lead-lags are unrelated to these scrutiny proxies. Geographic lead-lags earn risk-adjusted returns of **5–6% per year, half that observed for industry lead-lag effects**. Analysts covering both leader and lagger matter, which they relate to the sector-based organization of sell-side research — [IDEAS](https://ideas.repec.org/a/oup/rfinst/v33y2020i10p4721-4770..html); [AEA 2020 preliminary version](https://www.aeaweb.org/conference/2020/preliminary/paper/SfTyaRaf); [SSE research listing](https://research.hhs.se/esploro/outputs/journalArticle/Geographic-lead-lag-effects/991001480691206056)
- Hou (2007): lead-lag stronger in small, less competitive, neglected industries — [IDEAS](https://ideas.repec.org/a/oup/rfinst/v20y2007i4p1113-1138.html)
- Menzly & Ozbas (2010): cross-predictability decreases with analyst coverage and institutional ownership — [IDEAS](https://ideas.repec.org/a/bla/jfinan/v65y2010i4p1555-1580.html)
- Lee et al. (2019): tech-link predictability stronger with lower investor attention — [CityU Scholars](https://scholars.cityu.edu.hk/en/publications/technological-links-and-predictable-returns/)
- Hameed & Mian (2015): intra-industry reversals present "including large and liquid stocks" — [Cambridge](https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/abs/industries-and-stock-return-reversals/92B5101FBEA7B40717D46DB60913BF41)
- Customer momentum persists out of sample (122 bp EW / 106 bp VW per month raw) — [arXiv 2301.11394](https://arxiv.org/pdf/2301.11394)
- Practitioner/secondary: State Street reports that short-term reversal "has intensified post-2010" and that winning sectors tend to crash more than winning factors — [State Street Global Markets insight](https://globalmarkets.statestreet.com/research/portal/insights/article/72d25d12-4788-4e7f-9993-ff1d302f891b). Quantpedia: in the decade after the 2008–09 crisis, 12-month momentum in sectors/industries diminished while one-month reversals became more pronounced — [Quantpedia](https://quantpedia.com/an-important-analysis-of-stock-momentum-and-reversal-factors/)
- Industry momentum is most profitable in trending markets and weaker or negative during sharp reversals (2009–2013 cited) — [vLex, "Industry momentum and reversals in stock markets"](https://international.vlex.com/vid/industry-momentum-and-reversals-1049449277) (via search summary)
- The general momentum decline after publication is partly due to in-sample overfitting plus post-publication arbitrage (McLean-Pontiff); together with the 2008–09 crash these account for about 40% of the decline — [NBER w28624](https://www.nber.org/system/files/working_papers/w28624/revisions/w28624.rev2.pdf) (via search summary; this is about stock momentum, not industry lead-lag)

### Inferences
- **Confirmation of our test.** Hou, Menzly-Ozbas, Parsons-Sabbatucci-Titman and Lee et al. all locate industry/linked-firm predictability in small, neglected, low-coverage stocks. Our small-stock spread (+0.7% per 21 days, about 8–9% per year gross on an A−E basis) is economically plausible next to Parsons et al.'s roughly 10–12% per year industry lead-lag (twice the 5–6% geographic figure). Our large-stock result (≈0) is what the literature predicts.
- **Design implications for the grade:**
  1. Apply the industry grade mainly to small caps, or to stocks with low analyst coverage, low institutional ownership or low turnover, if those fields exist. For large caps, give it zero or low weight, or use it only together with within-industry reversal.
  2. Compute industry strength from **leaders** (large-cap, value-weighted returns), and test the grade's predictive power on the industry's **small members**.
  3. Use short look-backs (1 week to 1 month, maybe up to 3 months) and short holds (≤21 days); SIC-type peer information transmits within 1–2 months.
  4. Within each industry, add a short-term reversal tilt: prefer stocks that have lagged their industry recently, especially after market sell-offs or in volatile periods.
  5. Test the asymmetry: the weak side (E) may carry more information than the strong side (A) because of slow reaction to bad news. For a long-only, buy-only Shariah strategy, that makes "exclude E-industry small caps" a candidate rule.
  6. Expect lower payoff after 2010, and in trending versus reversing regimes; report results by sub-period (2005–2009, 2010–2019, 2020–2026).
- Transaction costs: the effect sits in small, thinly traded stocks, so realistic spreads and slippage could absorb a large share of +0.7% per 21 days. Net-of-cost testing is necessary.

### Gaps
- I found **no direct US study** of industry lead-lag in large caps after 2010, and no post-publication decay estimate specifically for Hou-type intra-industry lead-lag. The State Street and Quantpedia evidence is practitioner-level and about industry momentum or reversal factors, not big-to-small lead-lag.
- I found no study that tests a Moomoo-style (or GICS-style) industry grade on the 10–21 day horizon split by size. Our own test fills that gap; the literature only supports the direction of the result.
