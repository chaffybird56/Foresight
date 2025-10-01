from flask import Flask, render_template_string, send_file
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from pathlib import Path
from src.health.kpi import compute_kpis
from src.health.anomaly import detect_anomalies

app = Flask(__name__)

def load():
    df_s = pd.read_csv('data/mock_sensors.csv', parse_dates=['ts'])
    df_e = pd.read_csv('data/events.csv', parse_dates=['start','end'], infer_datetime_format=True)
    return df_s, df_e

TEMPLATE = '''
<!doctype html><html><head><title>System Health</title></head>
<body style="font-family:system-ui;margin:20px;">
<h1>System Health Monitor</h1>
<p><a href="/plot/last24">Last 24h Trend</a> | <a href="/anomalies">Anomalies</a> | <a href="/reliability">Reliability</a></p>
<h2>KPIs</h2>
<ul>
  <li>Availability: {{kpi.availability_pct}}%</li>
  <li>Demand Failures (7d): {{kpi.demand_failures}}</li>
  <li>Open Work Orders (mock): {{kpi.open_work_orders}}</li>
</ul>
<img src="/plot/last24" style="max-width:900px;">
</body></html>
'''

@app.route('/')
def home():
    df_s, df_e = load()
    kpi = compute_kpis(df_s, df_e)
    return render_template_string(TEMPLATE, kpi=kpi)

@app.route('/plot/last24')
def plot_last24():
    df_s, _ = load()
    end = df_s['ts'].max()
    start = end - pd.Timedelta('24h')
    d = df_s[df_s['ts'].between(start, end)]
    fig = plt.figure()
    for col in ['flow_kg_s','dp_kPa','temp_C','vib_mm_s']:
        plt.plot(d['ts'], d[col], label=col)
    plt.legend(); plt.xticks(rotation=30); plt.tight_layout()
    buf = BytesIO(); fig.savefig(buf, format='png', dpi=140); plt.close(fig); buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/anomalies')
def anomalies():
    df_s, _ = load()
    dfa = detect_anomalies(df_s)
    c = int(dfa['is_outlier'].sum())
    # tiny chart
    fig = plt.figure()
    plt.plot(dfa['ts'][-200:], dfa['flow_kg_s'][-200:], label='flow')
    o = dfa[-200:][dfa['is_outlier'][-200:]]
    plt.scatter(o['ts'], o['flow_kg_s'], marker='x', label='outlier')
    plt.legend(); plt.xticks(rotation=30); plt.tight_layout()
    buf = BytesIO(); fig.savefig(buf, format='png', dpi=140); plt.close(fig); buf.seek(0)
    img = ('/plot/last24')  # reuse
    html = f"<h2>Anomalies (last 7d): {c}</h2><img src='data:image/png;base64,'>"  # minimal
    return send_file(buf, mimetype='image/png')

@app.route('/reliability')
def reliability():
    # simple Weibull on mock inter-failure intervals
    import numpy as np
    import pandas as pd
    df = pd.read_csv('data/events.csv', parse_dates=['start','end'])
    t = pd.to_datetime(df['start'])
    failures = t[df['type']=='failure'].sort_values()
    if len(failures) < 3:
        x = np.array([100, 140, 220, 300])  # fallback
    else:
        x = np.diff(failures.values).astype('timedelta64[m]').astype(int)
    # fit via log-linear method on ln(ln(1/(1-F)))
    x = np.sort(x)
    F = (np.arange(1, len(x)+1)-0.3)/(len(x)+0.4)
    y = np.log(np.log(1/(1-F)))
    X = np.vstack([np.log(x), np.ones(len(x))]).T
    beta, a = np.linalg.lstsq(X, y, rcond=None)[0]
    eta = np.exp(-a/beta)
    fig = plt.figure()
    plt.plot(np.log(x), y, 'o'); plt.plot(np.log(x), beta*np.log(x)+a, '-')
    plt.xlabel('ln(time)'); plt.ylabel('ln(ln(1/(1-F)))'); plt.title(f'Weibull fit: beta={beta:.2f}, eta={eta:.1f} min')
    from io import BytesIO
    buf = BytesIO(); fig.savefig(buf, format='png', dpi=140); plt.close(fig); buf.seek(0)
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
