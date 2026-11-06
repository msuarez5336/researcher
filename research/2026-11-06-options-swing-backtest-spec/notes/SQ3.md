# SQ3 notes (as of 2026-11-06)

**Answer:** Primary sources for PBO/CSCV and DSR exist (Bailey et al.), but SSRN and PDFs could not be cached, so formulas are unverified from original text. Walk-forward vs hold-out is argued by Lopez de Prado as both weak without trial-counting. No primary source gives a minimum trade count; 21 DTE / 50% are tastylive opinion/vendor research, and I did not find the underlying measured study text.

## (a) DSR and PBO
- PBO: Bailey, Borwein, Lopez de Prado, Zhu, J. Computational Finance (DOI 10.21314/JCF.2016.322, 2017). CSCV is the nonparametric implementation; abstract says hold-out is unreliable [E/A, SQ3-1]. Detailed CSCV steps (split performance matrix into S even blocks, all C(S,S/2) IS/OOS combinations, PBO = share of combinations where the IS-best strategy ranks below OOS median, via logit) are from my memory, NOT verified (PDF binary, WebFetch failed).
- DSR: Bailey & Lopez de Prado, J. Portfolio Management 40(5), 2014 (SSRN 2460551, unreachable 403). Inputs: observed SR, T, skewness, kurtosis, number of independent trials N, variance of trial SRs [SQ3-3 O/C, SQ3-5 context]. PSR/SR0 formula from memory, unverified: SR0 = sqrt(V)[(1-g)Z^-1(1-1/N)+g Z^-1(1-1/(Ne))], g=0.5772; non-annualised SR.

## (b) Walk-forward vs single split
- Lopez de Prado: simple walk-forward = one train/test path, overfit-prone; count trials and use DSR; 20 repeated WF tests ~ 1 false 95% strategy [SQ3-2, SQ3-4, O, secondary via CXO]. Hold-out also unreliable without controlling for trials [SQ3-1]. Pardo's walk-forward book not located (not searched further). Rolling vs anchored pros/cons: no primary source found.

## (c) Minimum trades
- No primary guidance. Forum 30 / 100+ / hundreds rules are opinion, unverified [SQ3-9]. Bailey's Minimum Backtest Length concerns years vs number of trials, not trade count (via search summary only). The backtest-expert 30/100 claim remains unsupported.

## (d) Early exercise
- Condition: ITM short call at risk when call extrinsic (or same-strike put value) < dividend, assignment typically the day before ex-date [SQ3-8, O/B, unverified: Schwab cache thin]. Hull textbook/OCC page not retrieved.

## (e) 21 DTE / 50%
- 50%: tastylive definition page, vendor opinion with risk/reward rationale [SQ3-6, SQ3-7]. Search snippets say tastylive studies (e.g. 2018 1-SD strangles, 45 DTE, 2005-2017; hold vs 50% vs 21 DTE) exist, but cached episode pages contained no numbers; claims unverified. 21 DTE appears mainly in third-party summaries; origin as measured study not confirmed.

## Conflicts
Lopez de Prado (WF weak) vs practitioners treating WF as standard; arXiv work combining WF with locked hold-out (not cached).

## Not found
Verbatim DSR/CSCV text, Pardo, Hull/OCC early-exercise text, any sourced minimum trade count, tastylive numeric results.

## Blocked
papers.ssrn.com (403); escholarship PDF unsupported; tickertape.tdameritrade.com (502); Schwab page thin.

## Search log
5 searches (DSR; PBO; tastytrade; early exercise; WF criticism [disconfirm]; min trades) ~ new sources each; 3 fetch batches, 1 WebFetch.
