# Purpose: Compare and visualize the total number of females in STEM across Balkan countries for the latest year using a horizontal bar chart.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


data = pd.read_csv('data/balkans_stem.csv')


viti_max = data['viti'].max()
data_latest = data[data['viti'] == viti_max]

data_grouped = data_latest.groupby('vendi')['femra_ne_stem'].sum().reset_index()
data_grouped = data_grouped.sort_values(by='femra_ne_stem', ascending=False)


plt.figure(figsize=(10, 6))
sns.barplot(x='femra_ne_stem', y='vendi', data=data_grouped, palette='viridis')
plt.xlabel('Number of Females in STEM')
plt.ylabel('Countries')
plt.title(f'Total Females in STEM Across Balkan Countries ({viti_max})')
plt.tight_layout()
plt.show()
