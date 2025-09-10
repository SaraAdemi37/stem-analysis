# streamlit_app.py
# ------------------------------------------------
# This script provides an interactive demonstration of the project 
# "Women in STEM – Balkan Countries (2015–2025)".
# Users can explore the dataset through filters and visualizations,
# view trends and forecasts up to the year 2030,


# This app is intended for presentation and visualization purposes only.  
# For the full analysis and supporting code, please refer to the rest of the project.

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import squarify
import os
from fpdf import FPDF

st.set_page_config(page_title='Women in STEM Balkan Analysis', layout='wide')
st.title('Women in STEM – Balkan Countries (2015–2025)')

# --- Load dataset ---
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'balkans_stem.csv')
df = pd.read_csv(file_path)

# --- Project description ---
st.markdown("""
**Project Overview:**  
This project explores female participation in STEM across Balkan countries (2015–2025).  
It provides insights on trends, field comparisons, correlations, and forecasts for 2030.
""")

# --- Sidebar filters ---
selected_countries = st.sidebar.multiselect(
    'Select countries', df['vendi'].unique(), default=['Kosovë', 'Shqipëri'])
selected_fields = st.sidebar.multiselect(
    'Select STEM fields', df['fusha_stem'].unique(), default=df['fusha_stem'].unique())

# --- Filter data ---
df_filtered = df[df['vendi'].isin(selected_countries) & df['fusha_stem'].isin(selected_fields)]
st.subheader('Filtered Data')
st.dataframe(df_filtered)

# --- Bar chart: Average female participation per country ---
st.subheader('Average Female Participation per Country')
st.markdown("Shows which countries have higher or lower average female participation in STEM across selected fields.")

avg_country = df_filtered.groupby('vendi')['përqindja_femra_stem'].mean().sort_values(ascending=False)
fig1, ax1 = plt.subplots(figsize=(8,5))
sns.barplot(x=avg_country.values, y=avg_country.index, palette='viridis', ax=ax1)
ax1.set_xlabel('Average %')
ax1.set_ylabel('Country')
st.pyplot(fig1)

# --- Trend line chart per country ---
st.subheader('Trends Over Years')
st.markdown("Line charts display how female participation changes over years in each country and STEM field.")
for country in selected_countries:
    df_country = df_filtered[df_filtered['vendi'] == country]
    fig2, ax2 = plt.subplots(figsize=(10,5))
    sns.lineplot(data=df_country, x='viti', y='përqindja_femra_stem', hue='fusha_stem', marker='o', ax=ax2)
    ax2.set_ylabel('Female %')
    ax2.set_title(f'Trend in {country}')
    st.pyplot(fig2)

# --- Kosovo Pie chart / Treemap ---
st.subheader('Kosovo Female STEM Distribution (Latest Year)')
st.markdown("Pie chart and treemap show the distribution of females in different STEM fields in Kosovo for the latest year.")
df_kosove = df_filtered[df_filtered['vendi'] == 'Kosovë']
viti_max = df_kosove['viti'].max()
df_latest = df_kosove[df_kosove['viti'] == viti_max]
labels = df_latest['fusha_stem'].tolist()
values = df_latest['femra_ne_stem'].tolist()

# Pie chart
fig3, ax3 = plt.subplots(figsize=(6,6))
pie_colors = sns.color_palette('pastel')
ax3.pie(values, labels=labels, colors=pie_colors, autopct=lambda pct: f'{pct:.1f}%\n({int(round(pct*sum(values)/100))})', startangle=90)
st.pyplot(fig3)

# Treemap
fig4, ax4 = plt.subplots(figsize=(10,5))
treemap_colors = sns.color_palette('Set3')
squarify.plot(sizes=values, label=labels, color=treemap_colors, alpha=0.8, text_kwargs={'fontsize':12})
st.pyplot(fig4)

# --- Heatmap ---
st.subheader('Correlation Between STEM Fields')
st.markdown("Heatmap shows correlations between STEM fields based on female participation percentages. Helps identify related trends across fields.")
pivot_df = df_filtered.pivot_table(index=['vendi','viti'], columns='fusha_stem', values='përqindja_femra_stem')
corr = pivot_df.corr()
fig5, ax5 = plt.subplots(figsize=(8,6))
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, ax=ax5)
st.pyplot(fig5)

# --- Forecast 2030 ---
st.subheader('Forecast 2030 – Female STEM Participation')
st.markdown("Predicts female participation in STEM by 2030 using linear regression for selected countries and fields.")

output_folder = os.path.join(current_dir, 'outputs')
os.makedirs(output_folder, exist_ok=True)
rezultate = []
for vendi in selected_countries:
    for fusha in selected_fields:
        df_temp = df_filtered[(df_filtered['vendi'] == vendi) & (df_filtered['fusha_stem'] == fusha)][['viti','femra_ne_stem']]
        X = df_temp['viti'].values.reshape(-1,1)
        y = df_temp['femra_ne_stem'].values
        model = LinearRegression()
        model.fit(X,y)
        pred = model.predict([[2030]])[0]
        rezultate.append({'vendi': vendi, 'fusha_stem': fusha, 'viti':2030, 'predicted': round(pred) if pred>0 else 0})

df_forecast = pd.DataFrame(rezultate)
df_forecast.to_csv(os.path.join(output_folder, 'parashikim_2030_streamlit.csv'), index=False)

fig6, ax6 = plt.subplots(figsize=(12,6))
sns.barplot(x='fusha_stem', y='predicted', hue='vendi', data=df_forecast, ax=ax6)
ax6.set_ylabel('Number of Females')
ax6.set_xlabel('STEM Field')
st.pyplot(fig6)

# --- Conclusion ---
st.subheader('Key Insights and Conclusions')
st.markdown("""
- Kosovo and Albania show varied female participation across STEM fields.
- Engineering and IT fields have fewer females compared to health sciences or natural sciences in some countries.
- Trends are gradually increasing, but some fields need targeted support.
- Forecast for 2030 indicates continued growth, highlighting potential areas for interventions.
""")



