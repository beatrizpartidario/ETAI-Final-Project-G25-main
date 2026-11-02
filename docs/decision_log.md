# Decision log

Document *why* decisions were made, not only the final settings.

## D-001 — Do not commit raw CSVs (2026-11-02)
**Status:** Adopted for initial repository.  
**Reason:** Prevent accidental public distribution of assignment data. Keep the project reproducible via a documented import command; Git only tracks code and documentation.

## D-002 — Temporal validation (2026-11-02)
**Status:** Proposal, NOT finalized.  
**Proposal:** Expanding-window folds with 90-day label-availability gap, plus a final untouched time-based holdout.  
**Reason:** The test set is later in time, repeated customers occur, and outcomes require up to 90 days to mature.  
**Next checks:** Count valid labels and customers per proposed fold; confirm available historical metadata at each prediction time; compare sliding windows as sensitivity analysis. Final fold boundaries remain subject to EDA.

## D-003 — Baseline selection
**Status:** Pending.  
**Next:** Establish simple classification and conditional-spend baselines before optimizing models.
