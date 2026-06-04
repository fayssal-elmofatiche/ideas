# Turnleaf Analytics — Product, Methods, Models, Data & Features

> Research compiled 2026-06-04 from turnleafanalytics.com (public product/method pages), the logged-in
> forecast dashboard at `turnleafanalytics.com/maple/` (incl. a live 17,028-forecast performance run, §5.2),
> and the **MARCOS demo video** (frame-by-frame capture, §6). The MARCOS build-a-model flow and model
> architecture in §6 are read directly off that demo; only its audio narration is uncaptured.

---

## 1. Company at a glance

- **What**: London-based ("60 Cannon Street, London EC4N 6NP") *vertical-AI* macro-forecasting firm — machine learning applied narrowly and deeply to macroeconomic / inflation time series.
- **Tagline**: "Powering Real-Time Macro Decisions with Vertical AI."
- **Customers**: hedge funds, global banks, asset managers, corporates, policy organisations.
- **Named partner**: **Macrobond** ("Proud Partners Of" — i.e. distribution/data integration with the Macrobond analytics platform). No customer logos/testimonials shown publicly.
- **Four pillars**: (1) Forecast products, (2) point-in-time data feeds, (3) **MARCOS** model-factory platform, (4) Bespoke/custom forecasting. A library of trading-strategy white papers sits on top as proof-of-value.

### Team / credibility
| Person | Role | Background |
|---|---|---|
| **Alexander Denev** | CEO / Head of R&D | Ex-Head of AI, Deloitte FS; ex-IHS Markit quant research; co-author *The Book of Alternative Data*, *Portfolio Management under Stress*; Oxford visiting lecturer |
| **Saeed Amen** | CTO / Head of Data | 15+ yrs quant (Lehman, Nomura); founder Cuemacro; co-founder Thalesians; co-author *The Book of Alternative Data* |
| Pierre de Weck | Chairman | Ex-Bank of America board; Chairman Vedra Pensions |
| Paul Bilokon | Scientific Advisor | Quant of the Year 2023; Professor of Mathematics, Imperial College |
| Charles-Albert Lehalle | Scientific Advisor | Ex-Global Head Quant R&D, ADIA; Professor, École Polytechnique |
| Vlasios Voudouris | Scientific Advisor | Ex-CDO Argus Media; ex-Chief Data Scientist ABM Analytics |

---

## 2. Products

### A. Turnleaf Inflation / Macro Forecaster (flagship)
- **Forecasts**: inflation (CPI) for **36 countries**; **GDP & unemployment for US / UK / Euro Area**. Horizon: **next 12 months**.
- **Scale**: "100+ inflation models in production"; "20,000+ tracked forecasts since May 2022"; coverage ≈ **90% of global GDP**.
- **Cadence**: bi-weekly for benchmarked models; **two DAILY no-benchmark nowcast models** (CPI YoY NSA, CPI MoM NSA).
- **Country coverage (36)**: US, Canada, Mexico, Argentina, Brazil, Chile, Colombia, Peru / Eurozone, UK, France, Germany, Italy, Spain, Netherlands, Norway, Sweden, Switzerland, Czechia, Poland, Romania, Hungary / China, Japan, India, South Korea, Israel, Australia, South Africa, Indonesia, Turkey, Thailand, Malaysia, Philippines, Egypt, UAE.
- **Metric matrix per country**:
  - **Inflation** — SA/NSA × MoM/YoY × headline/core (10 variants), incl. 2 daily no-benchmark nowcasts.
  - **Inflation Bottom-Up** (8 sub-components, YoY/MoM SA): **Core Services CPI, Core Goods CPI, Food CPI, Energy CPI**.
  - **Growth** — indicators: **Business Confidence** (country PMIs/ISM/IFO — e.g. China Manufacturing PMI, US ISM Manufacturing & Non-Manufacturing, Germany IFO, Italy Business Confidence) and **GDP**. Horizons 1M/3M/12M.
  - **Labor** — indicators: **Unemployment Rate SA** and **NFP Change SA** (observed for US, Japan…). Horizons 1M/3M/12M.
  - Regions filter across all categories: **DM / EM / LATAM / Asia / CEEMEA**, with an "include hyper-inflation countries" toggle.

> **Coverage is broader than the public site claims.** Marketing says GDP & unemployment for "US/UK/Euro Area" only, but the live Growth/Labor dashboards show forecasts for **China, Germany, Italy, Japan, US** (and more) — i.e. the macro (non-CPI) coverage has expanded beyond the three headline regions.

**Live accuracy table (US, as of 2026-05-27)** — each variant ships a tracked Mean Absolute Error vs a 1-month benchmark, in basis points:

| Metric | Model MAE | Benchmark (1M) |
|---|---|---|
| CPI YoY NSA | 8.0 bp | 13.3 bp |
| CPI MoM SA | 5.5 bp | 13.5 bp |
| Core CPI YoY NSA | 8.5 bp | 9.1 bp |
| Core CPI MoM SA | 6.3 bp | 8.5 bp |
| CPI YoY SA | 7.0 bp | 15.3 bp |
| CPI MoM NSA | 6.0 bp | 11.3 bp |
| Core CPI YoY SA | 8.4 bp | 11.1 bp |
| Core CPI MoM NSA | 5.9 bp | 6.6 bp |
| CPI YoY NSA (no benchmark) **DAILY** | 7.6 bp | 10.0 bp |
| CPI MoM NSA (no benchmark) **DAILY** | 5.4 bp | 6.4 bp |
| *Bottom-Up* Core Services CPI YoY SA | 12.8 bp | 14.8 bp |
| *Bottom-Up* Core Services CPI MoM SA | 6.7 bp | 9.1 bp |
| *Bottom-Up* Core Goods CPI YoY SA | 21.6 bp | 16.5 bp |
| *Bottom-Up* Core Goods CPI MoM SA | 20.0 bp | 14.5 bp |

US named benchmark = **Federal Reserve Bank of Philadelphia / U.S. Energy Information Administration**.

### B. Data Feeds (point-in-time alternative-data indices)
1. **Food Indices** — food-price nowcasts, **22 countries**, "Food MoM" aligned to official statistical-institute releases. Sourcing: "multi-source data ingestion, including APIs, wholesale feeds, and **computer-vision parsing of supermarket fliers**." Daily/weekly/bi-weekly, point-in-time aligned.
2. **Energy Indices** — energy-price nowcasts, **10 countries**, MoM aligned to official CPI energy components. Daily/weekly/bi-weekly, PIT.
3. **Fed Communications Index** — **NLP sentiment index** over a **30-year corpus (back to 1995)** of Fed statements, minutes, press conferences, testimonies, speeches; classifies hawkish/dovish. Clients also get the **underlying cleaned text** for their own analysis. (Live dashboard generalises this to **multi-central-bank** "CScore" — see §5.1.)

> The **High Frequency Indices** catalogue in-app is broader than the two public products: downloadable point-in-time indices for **Alcohol, Apparel, Electricity, Food, Fuel, and Furniture** (§5.1).

### C. MARCOS — "The Model Factory for Macroeconomic AI"
See §6 for the build-a-model flow. Self-serve AutoML platform so institutions industrialise their own macro models.

### D. Bespoke Forecasts
Custom forecasting built on MARCOS for any macro/sector variable, multi-geography, multi-horizon. Six-step process (see §6.B). Delivery in **1–3 months**.

### E. Commercial / access model
Pricing is **not public** ("Request Free Trial" + contact sales; a **30-day free trial** is offered). Products are packaged in **three access tiers** (stated on the data-feed pages):
| Tier | Access | Positioned for |
|---|---|---|
| 1 | **Web view only** | Discretionary traders |
| 2 | Web view **+ historical data download** | Systematic traders |
| 3 | Web view + historical + **API + MCP** | Systematic traders (full integration) |

Delivery channels across tiers: web portal, AWS Cloud Bucket (S3), API, Snowflake, MCP, CSV. Compliance: "all data, its access, and its usage is compliant with industry standards."

---

## 3. Methods & Models

> **Model architecture — revealed by the MARCOS demo video (§6).** The marketing only says "specialized
> temporal AI models," but the demo's Forecast screen exposes the actual default pipeline:
> **a two-stage model — Primary stage `lso_cv` (LASSO with cross-validation) on a `curated` dataset, plus a
> Residual stage `rf` (Random Forest) on an `all_stationary` dataset** — with a rolling **Window** (default 10),
> per-stage **Lags** and **MIDAS** (Mixed-Data-Sampling, for mixed-frequency inputs), and **SHAP attributions**
> on. So: a regularised-linear primary fit + tree-ensemble residual correction, made explainable via SHAP. Index
> construction uses a **"TLA (correlation-weighted)"** method (§6).

- **Core paradigm**: supervised ML on macro time series — a **two-stage LASSO-CV + Random-Forest-residual** ensemble (per the demo), benchmarked against econometric/consensus baselines (e.g. Philadelphia Fed + EIA for US).
- **AutoML machinery** (exposed via MARCOS): automated hyperparameter tuning; **walk-forward / backtesting validation**; performance governance & auditing. Model selection and out-of-sample validation are industrialised pipelines, not one-offs.
- **Point-in-time discipline**: PIT transformations + **data-revision tracking** so backtests carry no look-ahead bias.
- **NLP**: Fed Communications sentiment classification over a 30-yr corpus.
- **Computer vision**: parsing supermarket fliers for the Food indices.
- **Probabilistic output**: forecasts ship with **upper/lower confidence bounds**, not just point estimates.
- **Explainability is first-class**: contribution decomposition into ~16 economic factor groups across short/medium/long-term horizons (see §5).
- **Opacity caveat**: specific model class (boosting / neural / ensemble) is never disclosed ("proprietary ML techniques"); accuracy is self-reported MAE vs a self-chosen benchmark.

---

## 4. Data

- **Breadth**: "thousands of data sources daily"; a **100,000+ variable** universe.
- **Types**: traditional macro + heavy **alternative data** (founders wrote *The Book of Alternative Data*) — wholesale price feeds, scraped retail prices, flier imagery, logistics/airfare/commodity-supply signals, prediction-market aggregation, and **GDELT** news/event volumes & tones (powers the Media Volume dashboard, §5.1).
- **Properties**: point-in-time aligned, revision-tracked, metadata-governed — curated, "AI-ready", reproducible.
- **Research blog** demonstrates the alt-data angle: Strait of Hormuz → airfare transmission; rice-shock propagation across Asia; Mexico fuel-subsidy smoothing; etc.

---

## 5. Features — live forecast dashboard (`/maple/`)

App nav: **Home Page · High Frequency Indices · Forecasts · Performance · Reports · White Papers · Dashboards · Admin · Logout.**

Per country / reference-date / metric, the Forecasts view delivers:
- **Forecast plot** — Model vs Market vs Benchmark vs Realised, 12-month forward path.
- **Forecast table** — month-by-month (1M…12M) Model, Market, **Upper/Lower confidence bounds**. (e.g. US CPI YoY NSA: 4.34% May → ~4.64% Jan-27 → 3.61% Apr-27; market 4.31 → 3.11.)
- **Next-release prediction** — e.g. "On 2026-06-10, CPI for May releases. Model expects 4.34% vs Benchmark 4.02%."
- **Historical Nowcast Progression** — how the nowcast for a target month evolved release-by-release.
- **Model Progression / Benchmark Progression** — how each forecast vintage shifted across calc dates (2026-04-28 → 05-27) — i.e. forecast stability.
- **Contribution Wordcloud** — top drivers (up to 150); red = upward CPI pressure, blue = downward; split **Overall / Short / Medium / Long Term**.
- **Contribution Plot (stacked)** — decomposition into **~16 factor groups**: base, consumer prices, FX/equities/commodities, government, global macro, geopolitical stability, long-term average, labor, money/credit/interest rates, output/production/business activity, producer prices, retail, sentiment & expectations, season, trade & investment, benchmark contribution.
- **Performance tracking** — live MAE-vs-benchmark badge on every metric.
- **Policy Impact analysis** — flags e.g. "Medicare Part D drug prices lowered 2027, ACA Marketplace premiums lowered 2027" as Jan-2027 inputs.
- **Embedded research feed**; **CSV download (single date / all dates)**.
- **Delivery surfaces**: Web portal, **API, AWS S3 bucket, Snowflake, and an MCP (Model Context Protocol) endpoint** (LLM-agent-native channel).

### 5.1 Additional dashboards (all walked live 2026-06-04)

- **High Frequency Indices** (`/maple/indices`) — downloadable point-in-time index catalogues across **six categories: Alcohol, Apparel, Electricity, Food, Fuel, Furniture** (broader than the public Food/Energy products). Per-index/country/start-date calculator with CSV download.
- **Inflation Reports** (`/maple/reports`) — **cross-country comparison** of forecasts; pick indicator/reference-date/tenor and compare **Model vs Benchmark vs (Model−Benchmark) across all 36 countries** in one table. Snapshot observed (CPI YoY NSA, 1M): Argentina 34.42 (bm 34.02), Turkey 33.27 (32.92), Egypt 16.09 (14.88), US 4.24 (3.96, +0.27), Eurozone 3.22 (1.70, **+1.52**), Italy 3.48 (1.30, +2.18), UAE 3.92 (1.12, +2.80), Japan 1.58, China 0.97 (1.05), Switzerland 0.72 (0.50), Sweden −0.20 (0.61). → model is systematically **above** consensus across most of the panel right now.
- **Performance** (`/maple/performance`) — full **back-test analytics matrix**: 34 countries × forecast horizons (1M…), configurable by Forecast Type / Benchmark Type / Indicator / Since–Until. Tables: **Benchmark Error & Model Error (MAE and RMSE), Benchmark/Model Directional Accuracy, Model-vs-Benchmark Hit Rate** (% of times model beat consensus), **Error-Reduction (MSE/RMSE)**, and **# forecasts analysed**. Row/column/grand averages across countries and horizons.
- **Inflation Market** (`/maple/inflation_market`) — **market-implied inflation** (breakevens/swaps) vs model, by tenor (1M…), history back to ~2013. (US = CPI YoY NSA; Eurozone = CPI Excl-Tobacco YoY NSA.)
- **Central Bank Sentiment** (`/maple/fed_sentiment`) — the live front-end of the Fed Communications Index, **multi-central-bank**. NLP **"CScore"** per communication (speeches, statements, minutes, FOMC, pressers, testimony); plotted as *Continuous CScore (excl. outliers)* vs *UST 10Y recent change*. Includes a dated **event table** (Date · Speaker · Event Type · Title · CScore · source link). Sample CScores: Powell speech 2026-05-31 **+2.14**; Logan 2026-04-02 +1.39; Waller 2026-05-22 **−1.45**; Barr (stablecoins) 2026-03-31 −1.76; FOMC 2026-04-29 minutes −1.18.
- **FOMC Projections** (`/maple/fomc_projections`) — interactive **dot plot** (SEP) for 2026 / 2027 / 2028 / Longer-Term with median + median line.
- **Media Volume** (`/maple/media_volume`) — **GDELT-powered** news/media-volume nowcasting signal ("Powered by GDELT"). Topic datasets: **Prices** (Country CPI, CPI Basket Inflation, Inflation, Deflation), **Labour** (Job Cuts, Labour Shortage, Wages, Unemployment, Unemployment Inc/Dec Ratio), **Production** (GDP, GDP Expansion/Contraction ratio), **Geopolitical** (GDELT Event Volumes, GDELT Event Tones). CPI Basket split into Communication/Education/Entertainment/Clothes/Health/Housing/Transportation/Energy/Food. Configurable rolling window (1wk–3mo), normalised, component breakdown.
- **Diffusion Index** (`/maple/diffusion_index`) — **% of forecasted countries expected to see an inflation uptick over the next 12 months** — a panel-breadth indicator.

**Admin surfaces** (this account has admin rights): `/users_admin` (user management), `/file_update` (data/file upload), `/white_papers_admin`, `/policy_impact_admin`.

**Full maple route table** (evidence MARCOS is *not* in this account):
`/home · /indices · /forecast-category/{inflation,growth,labor} · /forecasts/<country>/<metric> · /performance · /reports · /white_papers · /inflation_market · /fed_sentiment · /fomc_projections · /media_volume · /diffusion_index · /users_admin · /file_update · /white_papers_admin · /policy_impact_admin · /logout`

### 5.2 Measured performance — live calculation (not marketing claims)

Ran the Performance dashboard with: **Indicator = CPI YoY NSA, Monthly, vs Benchmark, all 34 countries, 2022-05-31 → 2026-05-31**. **17,028 forecasts analysed** (1,419 per horizon × 12 horizons). Errors are in **percentage points** of CPI YoY. Panel-average results:

| Metric (panel avg) | Model | Benchmark | Edge |
|---|---|---|---|
| Mean Absolute Error | **0.743** | 0.909 | model ~**18% lower** |
| Directional Accuracy | **64.8%** | 59.7% | +5.1 pts |
| Model-vs-Benchmark Hit Rate (model closer to realised) | **58.8%** | — | beats consensus most of the time |
| MSE Error-Reduction (negative = model lower error) | **−0.183** | — | model ~18% lower squared error |

**Horizon structure (the key nuance):** the model's edge is **largest at short horizons and erodes with horizon**:
- 1M: Model MAE **0.285** vs Bench 0.485 (−41%); hit-rate 66.3%; dir-acc 74.2%.
- 12M: Model MAE **1.128** vs Bench 1.045 (model now *worse*); hit-rate falls to 48.1%; MSE error-reduction turns positive (+0.079 = model slightly worse).
- Crossover ≈ 9–11M: beyond ~10M the model converges to / slightly trails the benchmark.

**Per-country spread (avg MAE, model vs benchmark):** model clearly wins in **Switzerland** (0.282 vs 0.606), **Malaysia** (0.377 vs 0.708), **Canada** (0.452 vs 0.506), **France** (0.499 vs 0.833), **Italy** (0.683 vs 1.316), **Sweden** (1.080 vs 1.871), **Egypt** (2.314 vs 3.315); roughly even or **trailing** in **Israel** (0.561 vs 0.394) and **Brazil** (0.746 vs 0.625).

**Caveat on the headline 8 bp figure:** the dashboard's per-metric badge (US CPI YoY NSA = 8.0 bp MAE) is a *recent* window; the 2022–2026 panel average for the same US metric is **0.442 pp** (44 bp) — because it spans the 2022–23 inflation spike. Accuracy claims are **highly period- and horizon-dependent.**

---

## 6. MARCOS — Build-a-Model Flow

MARCOS is pitched as *"the world's first end-to-end platform for building, validating, and deploying
macroeconomic time-series models … purpose-built for economic time series, [it] automates data
ingestion, model development, validation, and deployment so institutions can build and industrialize
their own macro forecasting."* It is delivered with **zero infrastructure** (no internal model or
infra build/maintenance), **role-based access**, and **industry-standard compliance**.

### 6.A The documented architecture = the build pipeline (three layers)

```
┌─────────────────────────┐   ┌─────────────────────────┐   ┌─────────────────────────┐
│ 1. DATA INGESTION &     │   │ 2. MODEL FACTORY        │   │ 3. DELIVERY &           │
│    CURATION             │ → │    (AI engine)          │ → │    GOVERNANCE           │
├─────────────────────────┤   ├─────────────────────────┤   ├─────────────────────────┤
│ Automated pipelines for:│   │ • Specialized temporal  │   │ • Role-based access     │
│ • Macro datasets        │   │   AI models             │   │ • Approval workflows    │
│ • Alternative datasets  │   │ • Automated             │   │ • Visual dashboards     │
│ • Revision tracking     │   │   hyperparameter tuning │   │ • API deployment        │
│ • PIT transformations   │   │ • Backtesting &         │   │   endpoints             │
│ • Metadata governance   │   │   walk-forward          │   │                         │
│                         │   │   validation            │   │                         │
│                         │   │ • Performance           │   │                         │
│                         │   │   governance & auditing │   │                         │
└─────────────────────────┘   └─────────────────────────┘   └─────────────────────────┘
   "Creates AI-ready,            "High accuracy and            "Trusted forecasts and
    reproducible datasets"        minimal human bias"           client self-serve models"
```

### 6.B The actual builder — captured from the demo video (2026-06-04)

The MARCOS app ("Marcos Platform") is a **web SPA** (the demo runs it at `localhost:5173`). Its left nav
is grouped into three sections that map to the architecture layers: **DATAFETCH**, **MARCOS**, **DATAHARVEST**.
Full nav: *Add Tickers · Ticker Metadata · Add Internal Tickers · Aggregate Datasets* (DATAFETCH) → *Pipeline ·
Forecast · Performance · Forecast Results · Performance Results* (MARCOS) → *Index Construction · Index Results*
(DATAHARVEST). End-to-end build flow as shown on screen:

**Step 1 — DATAFETCH: ingest & register data.** *Add Tickers / Ticker Metadata / Add Internal Tickers /
Aggregate Datasets* — register external + internal series and roll them up into datasets.

**Step 2 — DATAHARVEST: construct an alt-data index** (`/dataharvest/index-construction`). "Build an index from
raw features and a dependent series."
- **Inputs**: *X — Raw Features* = a daily price-level DataFrame (drag-drop `.parquet`); *Y — Dependent Series* =
  a lower-frequency target (e.g. monthly `.parquet`).
- **Configuration**: Method = **TLA (correlation-weighted)**; Base value 100; Lookback days 30; Min train years 2;
  Smoothing window 30; PT window years 5; Estimation steps 2.
- **Prepare**: Cutoff date; toggles for **Use lags**, **MAD cleaning**, **MIDAS transform**. → **Build Index**.
- **Index Results** (`/dataharvest/index-results`): level chart (constructed daily index back to ~2015),
  MoM-index-vs-dependent overlay, scatter, and **Univariate Statistics** (Observations, Correlation r, R², RMSE,
  MAE, Slope, Intercept, means). Export New Run / CSV. *(Observed example: a Mexico Food CPI MoM NSA index, TLA
  30-day lookback — r 0.52, R² 0.27, MAE 0.71, 201 obs.)*

**Step 3 — MARCOS → Pipeline: assemble the forecast pipeline.** Ordered, individually-toggleable steps:
① `dailyinputfileslite` (generates daily input files) → ② `dumpsnaplite` (creates forecast snapshot packets) →
③ `featurestores` (feature-engineering pipeline). Each step toggles on/off and runs independently; an **Output**
panel shows results.

**Step 4 — Configure the forecast packet.** Per packet: **Country, Target (e.g. CPI), Season (NSA/SA),
Var type (MoM/YoY), Ref year, Ref month, Forecast date, Proximity, Tenor 1…12** (per-horizon adjustments), with
**+ Add packet** to batch multiple targets.

**Step 5 — MARCOS → Forecast: set the model & run** (`/forecast`). Two panels + **Run Forecast**:
- **Payload** = the packet fields above.
- **Model Settings** — the actual model spec:
  - **Window** (rolling; default 10).
  - **Primary stage**: Data Source (`curated`) · **Model (`lso_cv` = LASSO-CV)** · Lags · MIDAS.
  - **Residual stage**: Data Source (`all_stationary`) · **Model (`rf` = Random Forest)** · Lags · MIDAS.
  - **SHAP attributions** toggle (On).
  - **Export Adjustments**: Tenor 1–12 manual overrides.
- → **Run Summary** echoes the full spec (Country / Target / Var Type / Ref Date / Forecast Date / Proximity /
  Window / Primary `lso_cv / curated` / Residual `rf / all_stationary` / Lags / MIDAS / SHAP).

**Step 6 — MARCOS → Forecast Results: inspect & explain** (`/results`). Forecast chart + **Variable Importance =
"aggregate absolute SHAP values"**, rendered as a driver word-cloud with **Overall / Short / Medium / Long-term**
tabs. *(This is exactly the contribution word-cloud surfaced in the production forecaster — confirming those
drivers are SHAP-derived. Observed top drivers for a US CPI run: "Seasonality", US inflation-market forecast,
EIA retail-gasoline forecast, gasoline all-grades, WTI/Brent 1st-dated, S&P GSCI, US PPI metals.)*

**Step 7 — Performance / Performance Results.** Back-test/performance views (the in-platform analogue of the
public `/maple/performance` matrix in §5.2).

**Bespoke variant** (human-assisted): same pipeline, but Turnleaf staff drive it — client uploads proprietary
data to a secure env, Turnleaf augments with its 100,000+ variable universe, sources extra alt-data, runs the
build, integrates the feed, and optionally publishes a white-paper backtest. Delivery 1–3 months.

### 6.C Why MARCOS is positioned as defensible
- "Built entirely for economic time-series."
- "Cannot be reproduced by general-purpose LLMs."
- "Integrates directly with [Turnleaf] data feeds and forecast products."
- "Enables client self-serve model development."

### 6.C Source & capture method for §6.B
The build flow above was **read directly off the MARCOS demo video** (`marcos_demo_final.mp4`, ~300 MB,
4:55, 2574×1440 screencast). Capture method: the remote browser throttles media decode in a background
tab, so once the MARCOS tab was brought to the foreground the `<video>` decoded; I then drove it
programmatically (`video.currentTime = t`, `readyState` reached 4) and screenshotted/zoomed frames at
~8/20/45/75/78/120/122/170/220/270 s. **Visuals are verified; the audio narration was not transcribed**, so
any spoken nuance (exact algorithm tuning, governance steps) beyond what's on screen is not captured here.

### 6.D Still unverified
- **Approval-workflow / role-based-access screens** (named in the marketing's "Delivery & Governance" layer)
  weren't shown in the demo segments captured.
- **Beyond-default model options** — the `lso_cv`/`rf` two-stage and `curated`/`all_stationary` data sources are
  the demo defaults; the full menu of selectable models, data sources, and hyperparameters isn't enumerated.
- **Pricing / packaging for MARCOS** specifically (vs the data-feed tiers in §2.E).
- MARCOS was **not provisioned on this forecast login** (the `/maple/` route table has no MARCOS route), so this
  is from the vendor demo, not hands-on use of a live MARCOS seat.

---

## 7. Trading strategies (proof-of-value layer)

Nine published strategies derived from the forecasts, each with an Information Ratio:

| Strategy | Asset class | IR |
|---|---|---|
| EM-bracing Inflation | EM FX | **1.15** |
| Yielding to Inflation | US + EZ inflation swaps | 1.11 |
| Feel the energy | Energy commodity futures | 1.07 |
| The Time is Now | US CPI (HF nowcast) | 1.06 |
| The loco-modities | Commodities | 1.04 |
| There's Currency in Inflation | DM FX | 1.0 / 0.66 |
| Equitable Path | Equity index futures | 0.88 |
| Surprise, it's inflation | US CPI event | 0.8 |
| Treasuring the Future | US Treasury futures | 0.66 |

(White-paper library is "Page 1 of 21" — far more research than the nine headline strategies.)

---

## 8. Assessment — the moat

1. **Alt-data engineering** (CV on supermarket fliers, wholesale feeds, logistics signals) — the hardest-to-copy input edge.
2. **PIT + revision-tracked data discipline** makes backtests credible — the thing most macro-ML shops get wrong.
3. **Explainability** (factor-decomposed contributions by horizon) makes forecasts usable by risk/PMs, not a black box.
4. **MARCOS productises the pipeline** — moving from selling forecasts to selling the factory is the scalable bet.
5. **Demonstrated accuracy** — verified live (§5.2), not just marketing: across 17,028 CPI-YoY-NSA forecasts the model cut average error ~18% and beat consensus 58.8% of the time, with strong short-horizon and EM/hard-market performance.

**Caveats** (several now evidence-based, not just stated):
- **Horizon decay** — the model edge is real but **front-loaded**: dominant at 1–3M, gone by ~10–12M where it converges to / slightly trails the benchmark. Buyers should treat it as a **short-horizon nowcasting** edge, not a 12-month one.
- **Period dependence** — accuracy figures swing hugely with the window (US CPI YoY NSA: 8 bp recent vs 44 bp over 2022–2026 incl. the inflation spike). Headline badges flatter.
- **Self-chosen benchmark** — "beats benchmark" is vs the consensus/econometric baseline Turnleaf selects (e.g. Philadelphia Fed + EIA for US); not an independent audit.
- **Mixed per-market / per-metric** — trails benchmark in some markets (Israel, Brazil) and on some bottom-up components (Core Goods).
- **Opacity (partly lifted)** — marketing says only "proprietary ML," but the demo reveals the default is a two-stage **LASSO-CV + Random-Forest-residual** model with MIDAS and SHAP (§3, §6); still, the full model/hyperparameter menu and feature set aren't published.
- **New, unbaselined** — the DAILY no-benchmark nowcasts lack a public comparison.

---

## 9. Sources & method note

- Public pages read via fetch: Home, `/turnleaf-macro-forecaster/`, `/marcos/`, `/turnleaf-food-indices/`,
  `/turnleaf-energy-indices/`, `/turnleaf-fed-communications-index/`, `/bespoke-forecasts/`,
  `/strategies/`, `/white-papers/`, `/research/`, `/team/`.
- §5 features, §5.2 measured performance, and §2 metric/coverage detail captured by driving the
  **logged-in dashboard** at `turnleafanalytics.com/maple/` (account already authenticated). Pages
  walked live: `/`, `/indices`, `/forecast-category/{inflation,growth,labor}`, `/performance` (ran a
  Calculate over 17,028 forecasts), `/reports`, `/inflation_market`, `/fed_sentiment`,
  `/fomc_projections`, `/media_volume`, `/diffusion_index`.
- No side-effecting actions taken — only read/expand/select-and-Calculate on read-only dashboards;
  no data submitted, saved, or changed.

---

## 10. Remaining gaps (what's still missing, and why)

**✓ Closed in this pass:** MARCOS build wizard screens (§6.B, from the demo video); model architecture (§3 — two-stage LASSO-CV + RF, MIDAS, SHAP); measured performance (§5.2); access tiers (§2.E); Growth/Labor + Bottom-Up taxonomy (§2.A); partner = Macrobond.

**Still fillable with one more action:**
- **MARCOS demo audio narration** — frames are captured; the spoken commentary (any tuning/governance detail) is not. Would need someone to listen.
- **White-paper methodology depth** — §7 has Information Ratios but not the modelling detail inside each paper; I can fetch individual papers for signal construction, lookbacks, transaction-cost assumptions.
- **Central-bank coverage of the Sentiment dashboard** — confirmed multi-bank with a country selector; specific banks not enumerated.
- **Performance for other indicators** — §5.2 covers CPI YoY NSA only; the same matrix can be run for Core CPI, MoM, Growth, Labor, other benchmark types / windows.
- **Full MARCOS model/hyperparameter menu** — only the demo *defaults* (`lso_cv`, `rf`, `curated`, `all_stationary`) are seen; the complete selectable set isn't.
- **Index-catalogue coverage** — the 6 HF-index catalogues are downloadable PDFs; per-index country lists not yet extracted.

**Not publicly obtainable (would need vendor/sales):**
- **Pricing** numbers (only the 3-tier structure + 30-day trial are public; MARCOS pricing unknown).
- **API technical docs** (endpoints, schemas, auth, rate limits) — not exposed without a key.
- Independent/third-party **accuracy audit** (all figures are Turnleaf's own dashboard vs its own benchmark).
