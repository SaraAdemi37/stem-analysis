# Purpose: Create a heatmap showing the correlation between different STEM fields based on female participation percentages across Balkan countries and years.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, '..', 'data', 'balkans_stem.csv')
df = pd.read_csv(file_path)


pivot_df = df.pivot_table(index=['vendi', 'viti'], columns='fusha_stem', values='përqindja_femra_stem')

corr = pivot_df.corr()


plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Between STEM Fields for Female Participation')
plt.tight_layout()
plt.show()
