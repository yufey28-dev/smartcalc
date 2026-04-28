import sqlite3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import io
import base64
from collections import Counter

def get_top_expressions(limit=10):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT expression FROM history")
    rows = cursor.fetchall()
    conn.close()
    counter = Counter(r[0] for r in rows)
    return counter.most_common(limit)

def generate_chart():
    data = get_top_expressions()

    if not data:
        return None

    labels = [d[0] for d in data]
    values = [d[1] for d in data]

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(labels[::-1], values[::-1], color="#7F77DD")
    ax.set_xlabel("Requests", fontsize=12)
    ax.set_title("Top integrals", fontsize=14, fontweight='bold')
    ax.bar_label(bars, padding=4, fontsize=10)
    ax.set_facecolor("#F8F8FC")
    fig.patch.set_facecolor("#FFFFFF")
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')