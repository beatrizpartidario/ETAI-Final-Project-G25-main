# ETAI project checklist (working notes from supplied brief)

## Data exploration and cleaning — 3/20
- [ ] Explore distributions, missingness, invalid values and duplicates.
- [ ] Propose, justify and implement appropriate handling in leakage-safe pipelines.
- [ ] Record findings that demonstrably influence modelling decisions.

## Classification — 5/20
- [ ] Document validation strategy and compare at least **five algorithms**.
- [ ] Pipeline-dependent preprocessing and feature engineering.
- [ ] Feature selection strategy.
- [ ] Hyperparameter optimization and metric rationale.
- [ ] Produce Kaggle submission for all 986 test observations.

## Regression — 4/20
- [ ] Analyze conditional spending distribution.
- [ ] Compare at least **four algorithms**.
- [ ] Preprocessing, feature engineering, feature selection and tuning.
- [ ] Ensure consistency with the classification decision.
- [ ] Assess MAE, RMSE and R² for known returners (as specified in brief).

## Explainability and additional objective — 3/20
- [ ] Global **and individual** explainability for both models.
- [ ] Meaningful additional objective/analysis, implementation and business interpretation.

## Structure, code quality and reproducibility — 3/20
- [x] Initial structure, README, YAML configuration and requirements.
- [ ] Save trained models; inference must never retrain.
- [ ] Provide all required source code and relevant experiments in the final ZIP.
- [ ] Document and test every terminal command on macOS and Windows.

## Deployment — 2/20
- [ ] CLI training for each task, batch inference and single-purchase inference.
- [ ] Output Kaggle format (`ID`, `repeat_purchase_90d`).
- [ ] Output regression predictions for predicted returners (`ID`, `repeat_purchase_90d`, `spend_next_90d`).
- [ ] Working interface for new **and** returning customers.

## Explicit restrictions
- [ ] All features available **at purchase time**.
- [ ] Predict each test row using **only itself, training data, clientes.csv**; never other test rows.
- [ ] No target leakage (in particular, `spend_next_90d` is not a classifier feature).
- [ ] Avoid Lazy Predict and other prohibited AutoML tools.
- [ ] Scientific sources should be peer-reviewed; do not cite ChatGPT/other LLMs.
- [ ] All work relevant to assessment appears in repository/ZIP.
- [ ] Prepare 40-minute defense: any team member can be questioned on any code.
- [ ] Submit before **22 Dec 2026, 18:00**.
