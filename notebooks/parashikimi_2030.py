# Purpose: Predict the number of females in STEM for Kosovo and Albania by 2030 using linear regression and visualize the predictions.

import pandas as pd
from sklearn.linear_model import LinearRegression
import os
import matplotlib.pyplot as plt
import seaborn as sns


data = pd.read_csv('data/balkans_stem.csv')


output_folder = 'outputs'
os.makedirs(output_folder, exist_ok=True)

rezultate = []

# Loop through Kosovo and Albania
for vendi in ['Kosovë', 'Shqipëri']:
    for fusha in data['fusha_stem'].unique():
     
        df = data[(data['vendi'] == vendi) & (data['fusha_stem'] == fusha)][['viti', 'femra_ne_stem']]

        X = df['viti'].values.reshape(-1, 1)
        y = df['femra_ne_stem'].values

        # Fit Linear Regression model
        model = LinearRegression()
        model.fit(X, y)

        # Predict for year 2030
        pred = model.predict([[2030]])[0]

        rezultate.append({
            'vendi': vendi,
            'fusha_stem': fusha,
            'viti': 2030,
            'parashikim_femra_ne_stem': round(pred) if pred > 0 else 0
        })

df_rezultate = pd.DataFrame(rezultate)
df_rezultate.to_csv(os.path.join(output_folder, 'parashikim_2030.csv'), index=False)

# --- Visualization ---
sns.set(style="whitegrid", palette="pastel")
plt.figure(figsize=(12, 6))
sns.barplot(x='fusha_stem', y='parashikim_femra_ne_stem', hue='vendi', data=df_rezultate)
plt.title('Predicted Number of Females in STEM (2030)')
plt.ylabel('Number of Females')
plt.xlabel('STEM Field')
plt.tight_layout()
plt.show()
