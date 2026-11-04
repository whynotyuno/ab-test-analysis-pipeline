
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ALPHA = 0.05
df = pd.read_csv("ab_data.csv")
c = df[df["group"] == "control"]
t = df[df["group"] == "test"]

# 1. SRM check: Load data and split into groups
counts = [len(c), len(t)]
chi2, p_srm = stats.chisquare(counts, f_exp=[sum(counts) / 2] * 2)
print(f"[SRM] control={counts[0]}, test={counts[1]}, p-value={p_srm:.4f}",
      "-> OK" if p_srm > 0.001 else "-> ПЕРЕКОС, тест нельзя анализировать")

# 2. Conversion Analysis: Two-proportion z-test
x1, n1 = c["converted"].sum(), len(c)
x2, n2 = t["converted"].sum(), len(t)
p1, p2 = x1 / n1, x2 / n2

# Pooled standard error under H0 for p-value calculation
p_pool = (x1 + x2) / (n1 + n2)
se_pool = np.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
z = (p2 - p1) / se_pool
p_value = 2 * (1 - stats.norm.cdf(abs(z)))

# Unpooled standard error under H1 for confidence interval
se = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
ci = (p2 - p1 - stats.norm.ppf(1 - ALPHA / 2) * se,
      p2 - p1 + stats.norm.ppf(1 - ALPHA / 2) * se)
print(f"[Конверсия] control={p1:.2%}, test={p2:.2%}, "
      f"diff={p2 - p1:+.2%}, 95% ДИ=({ci[0]:+.2%}; {ci[1]:+.2%}), p-value={p_value:.4f}")

# 3. ARPU Analysis: Percentile Bootstrap to handle skewed revenue distribution
rng = np.random.default_rng(0)
rc, rt = c["revenue"].to_numpy(), t["revenue"].to_numpy()
diffs = np.array([
    rng.choice(rt, len(rt)).mean() - rng.choice(rc, len(rc)).mean()
    for _ in range(2000)
])
lo, hi = np.percentile(diffs, [2.5, 97.5])
print(f"[ARPU] control={rc.mean():.2f}, test={rt.mean():.2f}, "
      f"diff={rt.mean() - rc.mean():+.2f}, 95% bootstrap ДИ=({lo:+.2f}; {hi:+.2f})")

# 4. Cross-Platform Audit: Check consistency across segments
seg = df.pivot_table(index="platform", columns="group", values="converted", aggfunc="mean")
seg["diff"] = seg["test"] - seg["control"]
print("\n[Конверсия по платформам]\n", seg.round(4))

# 5. Visualization: Plotting conversion rates with confidence intervals
fig, ax = plt.subplots(figsize=(5, 4))
ax.bar(["control", "test"], [p1, p2], yerr=[1.96 * np.sqrt(p1 * (1 - p1) / n1),
                                            1.96 * np.sqrt(p2 * (1 - p2) / n2)], capsize=6)
ax.set_ylabel("Конверсия")
ax.set_title(f"Конверсия по группам (p={p_value:.4f})")
plt.tight_layout()
plt.savefig("conversion.png", dpi=150)
print("\nГрафик сохранён: conversion.png")
