# Purpose: Visualize female participation in STEM fields in Kosovo using pie chart and treemap for the latest year.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import squarify


data = pd.read_csv('data/balkans_stem.csv')

data_kosove = data[data['vendi'] == 'Kosovë']


viti_max = data_kosove['viti'].max()
data_latest = data_kosove[data_kosove['viti'] == viti_max]

labels = data_latest['fusha_stem'].tolist()
values = data_latest['femra_ne_stem'].tolist()


pie_colors = sns.color_palette("pastel")
treemap_colors = sns.color_palette("Set3")

def autopct_format(pct):
    total = sum(values)
    val = int(round(pct*total/100.0))
    return f'{pct:.1f}%\n({val})'

# Pie chart
plt.figure(figsize=(8, 8))
plt.pie(values, labels=labels, colors=pie_colors, autopct=autopct_format, startangle=90, textprops={'fontsize': 12})
plt.title(f'Female STEM Distribution in Kosovo ({viti_max}) - Pie Chart', fontsize=16)
plt.axis('equal')
plt.tight_layout()
plt.show()

