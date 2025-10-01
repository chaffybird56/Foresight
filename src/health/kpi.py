import pandas as pd
import numpy as np

def compute_kpis(df_sens: pd.DataFrame, df_evt: pd.DataFrame):
    avail = (df_sens["flow_kg_s"] > 4500).mean()
    low = (df_sens["flow_kg_s"] < 4300).astype(int)
    demand_failures = int(((low.diff().fillna(0) == 1).sum()))
    open_wos = int((df_evt["type"] == "wo_open").sum() - (df_evt["type"] == "wo_close").sum())
    return {
        "availability_pct": round(100 * float(avail), 2),
        "demand_failures": demand_failures,
        "open_work_orders": open_wos,
    }
