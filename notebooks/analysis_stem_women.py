# Purpose: This file analyzes and visualizes female participation in STEM across Balkan countries (2015–2025) and prepares aggregated data for Power BI.

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.io as pio

pio.renderers.default = "browser"

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, '..', 'data', 'balkans_stem.csv')
df = pd.read_csv(file_path)

sns.set(style="whitegrid", palette="pastel")

# Average female STEM percentage per country
avg_per_country = df.groupby("vendi")["përqindja_femra_stem"].mean().sort_values(ascending=False)
plt.figure(figsize=(10, 6))
sns.barplot(x=avg_per_country.values, y=avg_per_country.index)
plt.title("Average Female STEM Percentage per Country (2015–2025)")
plt.xlabel("Average Percentage (%)")
plt.ylabel("Country")
plt.tight_layout()
plt.show()

# Kosovo trend by STEM field
kosovo = df[df["vendi"] == "Kosovë"]
plt.figure(figsize=(10, 6))
sns.lineplot(data=kosovo, x="viti", y="përqindja_femra_stem", hue="fusha_stem", marker="o")
plt.title("Female STEM Trend in Kosovo (2015–2025)")
plt.xlabel("Year")
plt.ylabel("Female STEM Percentage")
plt.legend(title="STEM Field")
plt.tight_layout()
plt.show()

# Boxplot for STEM fields in 2025
df_2025 = df[df["viti"] == 2025]
fig = px.box(df_2025, x="fusha_stem", y="përqindja_femra_stem", color="fusha_stem",
             title="Distribution of Female STEM Percentage by Field (2025)")
fig.show()


map_data = df.groupby("vendi")[["përqindja_femra_stem"]].mean().reset_index()
output_dir = os.path.join(current_dir, '..', 'outputs')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'mapdata_stem_femra.csv')
map_data.to_csv(output_path, index=False)
