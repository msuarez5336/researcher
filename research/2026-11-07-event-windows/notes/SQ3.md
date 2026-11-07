# SQ3 notes (as of 2026-11-07)
## Answer
Sign convention: VRP = implied minus subsequent realised; it is positive on average and negative mainly at the onset of panics, when VIX lags (GFC: realised above VIX Jul-Nov 2008, then VIX overshot into 2009). Thin direct evidence was obtained that term-structure inversion, VVIX or low-base VIX jumps forecast realised above implied. Most primary PDFs were unparseable, so most items are unverified summaries.
## Findings
- VIX lags then overshoots in panics (GFC, COVID) [E/O] SQ3-1, SQ3-2; slow-moving-belief model [E] SQ3-4; VIX lags realised by ~1 month [E] SQ3-5.
- Falling VIX-premium estimates predict higher subsequent realised risk [E] SQ3-7. Basis/backwardation predicts VIX futures returns (not spot changes) [E] SQ3-6. VVIX forecasts VIX variability, not index vol directly [E] SQ3-8.
- Counter-evidence: after a spike the overshoot makes long vol lose in later phases (SQ3-1: 2009 overshoot); Man: equity-return after VIX spikes mixed (SQ3-3, equity not vol).
## Regime-state definitions (computable; thresholds as used by sources or reported in snippets)
1. Trailing-realised-over-implied gap: RV_fwd30 - VIX > 0 (CFA/GFC exhibit; use trailing RV20 - VIX as an ex-ante proxy since VIX lags RV ~1 month). No numeric threshold given.
2. VIX futures basis (F1 - spot) < 0 = backwardation; EFMA uses sign only (2006-2011).
3. Term-structure slope: VIX3M/VIX or VIX/VIX3M > 1 (inversion); VIX9D/VIX > 1. Sources not retrieved with thresholds; Johnson 2017 not accessed.
4. Falling estimated variance premium (Cheng): change in premium < 0; threshold not retrieved.
5. VIX spike: Man uses top-20 daily VIX jumps in 30 years (example +11 points to 10-month high); percentile definition, not a fixed threshold.
6. VVIX level/change: no threshold sourced.
## Conflicts
Underreaction-then-overshoot means timing matters: long vol pays early in the onset, loses after the catch-up. Man shows mixed equity outcomes.
## Not found
Quantified implied-catch-up speed; episode lists with magnitudes; VVIX or inversion thresholds forecasting RV>IV; Carr-Wu, BTZ, Todorov, Johnson 2017 primary text.
## Blocked
PDFs unsupported by fetch_page (NBER, NY Fed, Hosei, JFQA); CFA blogs.cfainstitute.org 404; EFMA 503; SSRN/core.ac.uk known 403. WebFetch of PDFs returned binary. Items with verified=false rest on search summaries.
## Search log
1 disconfirm buy vol after spike (several C sources); 2 VRP negative/inversion (leads); 3 VVIX forecast (leads); 4 backwardation (EFMA, Cheng); 5 underreaction (CFA, Lochstoer-Muir, Adhikari). 15-call budget: ~13 used.
