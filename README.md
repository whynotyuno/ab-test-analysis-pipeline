# A/B-Test Analysis Pipeline

A comprehensive pipeline for analytical evaluation and validation of A/B test results, featuring automated data quality controls and robust statistical estimation for skewed financial metrics.

## 🎯 Project Overview
This project implements an end-to-end analytical pipeline designed to ingest raw experimental user activity logs and perform a rigorous statistical assessment. The architecture is built to mitigate the risks of making flawed product decisions caused by sample allocation bugs or extreme user behavior ("whales").

## ⚙️ Tech Stack
*   **Python 3.14**
*   **NumPy** (vectorized computations, synthetic data generation)
*   **Pandas** (data aggregation, segmentation, pivot tables)
*   **SciPy** (`stats.chisquare`, `stats.norm`) — statistical testing framework
*   **Matplotlib** (visualization of conversion metrics and confidence intervals)

## 🧠 Methodology & Core Components

### 1. Data Quality Guard (SRM Detection)
Before computing core metrics, the pipeline executes a **Sample Ratio Mismatch (SRM)** check using **Pearson's Chi-Square ($\chi^2$) Goodness-of-Fit test**. This automatically detects technical issues in the traffic split mechanism or potential bot activity. The significance threshold is set at a strict conservative level of $\alpha = 0.001$.

### 2. Conversion Rate Analysis (Binomial Metrics)
For the binary conversion metric, a **Two-Proportion Z-Test** is applied.
*   **p-value** is calculated using a **pooled standard error**, operating under the null hypothesis ($H_0$) framework where group proportions are assumed equal.
*   **95% Confidence Interval** of the difference is constructed using **unpooled (separate) standard errors**, aligning with the alternative hypothesis ($H_1$) framework.

### 3. Financial Metrics Analysis (ARPU)
Revenue distribution in digital products typically exhibits a severe right skew (lognormal distribution) with a heavy inflation of zeros and a long tail driven by high-spending users ("whales"). Standard parametric tests (like the T-test) lose statistical power under these conditions. The pipeline addresses this by implementing a **non-parametric percentile Bootstrap (2,000 resamples)** to generate unbiased point estimates and confidence intervals for ARPU variance.

### 4. Cross-Platform Audit (Sanity Check)
To isolate platform-specific anomalies or OS-level rendering bugs, the pipeline automatically breaks down the experimental effects across `iOS`, `Android`, and `Web` segments.

## 📊 Experimental Results

When evaluated against the generated sample size of 20,000 users, the pipeline yielded the following insights:

*   **[SRM]:** Traffic split is mathematically sound (`p-value = 0.3086 -> OK`).
*   **[Conversion]:** Statistically significant increase in the test group by **+1.52%** (`p-value = 0.0006`, 95% CI: `+0.66%` to `+2.38%`).
*   **[ARPU]:** Statistically significant lift in average revenue per user by **+3.96** units (95% bootstrap CI: `+1.25` to `+6.56`).

### Conversion Rate Visualization
The script automatically exports a `conversion.png` plot displaying confidence intervals to back up the data when presenting to product stakeholders.

![Conversion Rate](conversion.png)

## 🚀 Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com
   cd ab-test-analysis-pipeline
   ```
2. Install dependencies:
   ```bash
   pip install numpy pandas scipy matplotlib
   ```
3. Generate synthetic experimental data:
   ```bash
   python generate_data.py
   ```
4. Run the comprehensive analysis suite:
   ```bash
   python analyze.py
   ```
