import pandas as pd, numpy as np

def compute_kpis(df_sens: pd.DataFrame, df_evt: pd.DataFrame):
    # Availability proxy: percent time flow above threshold
    avail = (df_sens['flow_kg_s'] > 4500).mean()
    # Demand failures: count of dips below threshold for >= 10 minutes
    low = df_sens['flow_kg_s'] < 4300
    demand_failures = ((low.astype(int).diff().fillna(0)==1).sum())
    open_wos = (df_evt['type']=='wo_open').sum() - (df_evt['type']=='wo_close').sum()
    return {'availability_pct': round(100*avail,2), 'demand_failures': int(demand_failures), 'open_work_orders': int(open_wos)}
