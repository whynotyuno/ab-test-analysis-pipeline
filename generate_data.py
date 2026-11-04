import numpy as np
import pandas as pd

# Setup random generator and sample size
rng = np.random.default_rng(42)
N = 20_000

# Generate baseline user dataframe
df = pd.DataFrame({
    "user_id": np.arange(N),
    "group": rng.choice(["control", "test"], N),
    "platform": rng.choice(["ios", "android", "web"], N, p=[0.35, 0.45, 0.20]),
})

# Define conversion probabilities (baseline 10% vs test 11.5%)
p = np.where(df["group"] == "test", 0.115, 0.10)
df["converted"] = rng.random(N) < p

# Generate skewed lognormal revenue for converted users only
df["revenue"] = np.where(df["converted"], rng.lognormal(5, 0.8, N), 0.0).round(2)

# Save data and display summary
df.to_csv("ab_data.csv", index=False)
print(df.groupby("group").agg(users=("user_id", "count"), conv=("converted", "mean")))
