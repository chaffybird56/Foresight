import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(df_sens: pd.DataFrame):
    X = df_sens[["flow_kg_s", "dp_kPa", "temp_C", "vib_mm_s"]].copy()
    model = IsolationForest(contamination=0.01, random_state=0)
    y = model.fit_predict(X)
    df = df_sens.copy()
    df["is_outlier"] = (y == -1)
    return df
