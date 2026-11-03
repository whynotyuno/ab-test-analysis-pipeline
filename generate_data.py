"""Генерирует синтетические данные A/B-теста: 20 000 пользователей, 50/50."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 20_000

df = pd.DataFrame({
    "user_id": np.arange(N),
    "group": rng.choice(["control", "test"], N),
    "platform": rng.choice(["ios", "android", "web"], N, p=[0.35, 0.45, 0.20]),
})

# Базовая конверсия 10%, в тесте заложен эффект +1.5 п.п.
p = np.where(df["group"] == "test", 0.115, 0.10)
df["converted"] = rng.random(N) < p

# Выручка есть только у сконвертившихся, распределение скошенное (lognormal)
df["revenue"] = np.where(df["converted"], rng.lognormal(5, 0.8, N), 0.0).round(2)

df.to_csv("ab_data.csv", index=False)
print(df.groupby("group").agg(users=("user_id", "count"), conv=("converted", "mean")))
