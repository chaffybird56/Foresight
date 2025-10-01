import pandas as pd, numpy as np
from pathlib import Path
import datetime as dt
import random

base = Path("data")
base.mkdir(exist_ok=True, parents=True)

start = dt.datetime.now() - dt.timedelta(days=7)
idx = pd.date_range(start, periods=7*24*60, freq="T")
rng = np.random.default_rng(42)
flow = 5000 + 200*rng.standard_normal(len(idx))
dp = 100 + 5*rng.standard_normal(len(idx))
temp = 30 + 2*rng.standard_normal(len(idx))
vib = 2 + 0.2*rng.standard_normal(len(idx))

for _ in range(8):
    k = int(rng.integers(0, len(idx)-30))
    flow[k:k+30] -= rng.uniform(800,1200)
    vib[k:k+10] += rng.uniform(1.0,2.0)

pd.DataFrame({
    "ts": idx,
    "flow_kg_s": flow,
    "dp_kPa": dp,
    "temp_C": temp,
    "vib_mm_s": vib
}).to_csv(base/"mock_sensors.csv", index=False)

events = []
for _ in range(10):
    t0 = start + dt.timedelta(hours=random.uniform(0, 7*24-4))
    t1 = t0 + dt.timedelta(hours=random.uniform(1, 4))
    events.append({
        "type": random.choice(["failure","wo_open","wo_close"]),
        "start": t0.isoformat(),
        "end": t1.isoformat(),
        "system":"ServiceWater"
    })
pd.DataFrame(events).to_csv(base/"events.csv", index=False)

print("Generated data/*.csv")
