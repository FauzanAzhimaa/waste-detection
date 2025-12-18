# src/make_heatmap.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, '..', 'outputs', 'records.csv')
OUT_PNG = os.path.join(BASE_DIR, '..', 'outputs', 'heatmap.png')

def main():
    if not os.path.exists(CSV_PATH):
        print('No records.csv found. Run infer_and_save.py first.')
        return
    df = pd.read_csv(CSV_PATH)
    # Jika zone_id adalah struktur A1..C3, map to grid. For now let's group by zone_id counts weighted by priority
    agg = df.groupby('zone_id')['priority_score'].sum().reset_index()
    print('Aggregated zone scores:\n', agg)
    # Simple bar-chart per zone
    plt.figure(figsize=(8,4))
    agg_sorted = agg.sort_values(by='priority_score', ascending=False)
    plt.bar(agg_sorted['zone_id'], agg_sorted['priority_score'])
    plt.xlabel('Zone ID'); plt.ylabel('Priority Score Sum')
    plt.title('Zone priority summary (for heatmap)')
    plt.tight_layout()
    os.makedirs(os.path.dirname(OUT_PNG), exist_ok=True)
    plt.savefig(OUT_PNG, dpi=200)
    print('Saved', OUT_PNG)

if __name__ == '__main__':
    main()
