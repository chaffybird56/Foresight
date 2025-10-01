import os
os.environ["MPLBACKEND"] = "Agg"

from flask import Flask, render_template, send_file, abort, jsonify
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from pathlib import Path

from src.health.kpi import compute_kpis
from src.health.anomaly import detect_anomalies

app = Flask(__name__)

DATA_DIR = Path("data")
SENSORS_CSV = DATA_DIR / "mock_sensors.csv"
EVENTS_CSV  = DATA_DIR / "events.csv"

def load_data():
    if not SENSORS_CSV.exists() or not EVENTS_CSV.exists():
        raise FileNotFoundError("Missing data files. Run: python scripts/generate_mock_data.py")
    df_s = pd.read_csv(SENSORS_CSV, parse_dates=["ts"])
    df_e = pd.read_csv(EVENTS_CSV,  parse_dates=["start","end"], infer_datetime_format=True)
    return df_s, df_e

# ------------------ Pages ------------------
@app.route("/")
def home():
    # home pulls KPIs via fetch() too, but render once so it's not empty on first load
    df_s, df_e = load_data()
    kpi = compute_kpis(df_s, df_e)
    return render_template("home.html", kpi=kpi)

@app.route("/anomalies")
def anomalies_page():
    return render_template("anomalies.html")

@app.route("/reliability")
def reliability_page():
    return render_template("reliability.html")

# ------------------ JSON APIs (for live charts) ------------------
@app.route("/api/kpis")
def api_kpis():
    df_s, df_e = load_data()
    return jsonify(compute_kpis(df_s, df_e))

@app.route("/api/last24")
def api_last24():
    df_s, _ = load_data()
    end = df_s["ts"].max()
    start = end - pd.Timedelta("24h")
    d = df_s[df_s["ts"].between(start, end)].copy()
    if d.empty:
        return jsonify({"ts": [], "series": {}})

    payload = {
        "ts": d["ts"].astype("int64").div(1_000_000).tolist(),  # ms epoch
        "series": {
            "flow_kg_s": d["flow_kg_s"].tolist(),
            "dp_kPa":    d["dp_kPa"].tolist(),
            "temp_C":    d["temp_C"].tolist(),
            "vib_mm_s":  d["vib_mm_s"].tolist(),
        }
    }
    return jsonify(payload)

@app.route("/api/anomalies")
def api_anomalies():
    df_s, _ = load_data()
    dfa = detect_anomalies(df_s)
    end = dfa["ts"].max()
    start = end - pd.Timedelta("24h")
    d = dfa[dfa["ts"].between(start, end)].copy()
    payload = {
        "ts": d["ts"].astype("int64").div(1_000_000).tolist(),
        "flow_kg_s": d["flow_kg_s"].tolist(),
        "is_outlier": d["is_outlier"].astype(int).tolist()
    }
    return jsonify(payload)

@app.route("/api/weibull")
def api_weibull():
    _, df_e = load_data()
    df = df_e[df_e["type"] == "failure"].copy()

    if df.empty or len(df.sort_values("start")["start"].values) < 3:
        x = np.array([100, 140, 220, 300])
    else:
        t = df.sort_values("start")["start"].values
        x = np.diff(t).astype("timedelta64[m]").astype(int)

    x = np.sort(np.array(x))
    F = (np.arange(1, len(x)+1) - 0.3) / (len(x) + 0.4)
    y = np.log(np.log(1/(1-F)))
    X = np.vstack([np.log(x), np.ones(len(x))]).T
    beta, a = np.linalg.lstsq(X, y, rcond=None)[0]
    eta = float(np.exp(-a/beta))
    return jsonify({
        "interval_minutes": x.tolist(),
        "F": F.tolist(),
        "beta": float(beta),
        "eta": eta
    })

# ------------------ PNG routes (kept for downloads) ------------------
@app.route("/plot/last24.png")
def plot_last24():
    df_s, _ = load_data()
    end = df_s["ts"].max()
    start = end - pd.Timedelta("24h")
    d = df_s[df_s["ts"].between(start, end)]
    if d.empty:
        abort(404, "No data in last 24h")
    fig = plt.figure(figsize=(9,3.6))
    for col in ["flow_kg_s","dp_kPa","temp_C","vib_mm_s"]:
        plt.plot(d["ts"], d[col], label=col)
    plt.legend(loc="upper left", ncol=2, fontsize=8)
    plt.xlabel("Time"); plt.ylabel("Value"); plt.title("Last 24h Trend")
    plt.xticks(rotation=25); plt.tight_layout()
    buf = BytesIO(); fig.savefig(buf, format="png", dpi=140); plt.close(fig); buf.seek(0)
    return send_file(buf, mimetype="image/png")

@app.route("/plot/anomalies.png")
def plot_anomalies():
    df_s, _ = load_data()
    dfa = detect_anomalies(df_s)
    end = dfa["ts"].max()
    start = end - pd.Timedelta("24h")
    d = dfa[dfa["ts"].between(start, end)]
    fig = plt.figure(figsize=(9,3.6))
    plt.plot(d["ts"], d["flow_kg_s"], label="flow")
    outliers = d[d["is_outlier"]]
    if not outliers.empty:
        plt.scatter(outliers["ts"], outliers["flow_kg_s"], marker="x", label="outlier")
    plt.legend(loc="upper left"); plt.xlabel("Time"); plt.ylabel("Flow (kg/s)")
    plt.title("Anomalies (last 24h)"); plt.xticks(rotation=25); plt.tight_layout()
    buf = BytesIO(); fig.savefig(buf, format="png", dpi=140); plt.close(fig); buf.seek(0)
    return send_file(buf, mimetype="image/png")

@app.errorhandler(Exception)
def handle_error(e):
    return f"Error: {str(e)}", getattr(e, "code", 500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
