# -*- coding: utf-8 -*-
# =================== AGRICULTURE ANALYSIS (Spyder Inline + Auto Save) ===================

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import os

# Force plots inline in Spyder
%matplotlib inline

# Path to Excel file
file_path = r"C:\Users\gold\Documents\python\porject-2\ICRISAT-District Level Data.xlsx"

# Read Excel
df = pd.read_excel(file_path, engine='openpyxl')
df.columns = df.columns.str.strip()  # Remove spaces

# Create folder to save plots
if not os.path.exists("plots"):
    os.makedirs("plots")

# Function to save plots
def save_plot(filename):
    plt.tight_layout()
    plt.savefig(os.path.join("plots", filename), dpi=300)
    plt.show()

# =================== 1. RICE (Top 7 States) ===================
rice_state = df.groupby("State Name")["RICE PRODUCTION (1000 tons)"].sum().sort_values(ascending=False).head(7)
rice_colors = ['lightblue', 'yellow', 'green', 'red', 'orange', 'purple', 'pink']

plt.figure(figsize=(10,6))
bars = plt.bar(rice_state.index, rice_state.values, color=rice_colors)
plt.title("Top 7 Rice Producing States", fontsize=14, fontweight="bold", color="darkgreen")
plt.ylabel("Rice Production (1000 tons)")
plt.xlabel("State")
plt.xticks(rotation=45)
for bar, state in zip(bars, rice_state.index):
    bar.set_label(state)
plt.legend(title="States", bbox_to_anchor=(1.05, 1), loc='upper left')
save_plot("top7_rice.png")

# =================== 2. WHEAT (Top 5 States + Pie) ===================
wheat_state = df.groupby("State Name")["WHEAT PRODUCTION (1000 tons)"].sum().sort_values(ascending=False).head(5)
wheat_colors = ['lightblue', 'yellow', 'green', 'red', 'orange']

# Bar Chart
plt.figure(figsize=(10,6))
bars = plt.bar(wheat_state.index, wheat_state.values, color=wheat_colors)
plt.title("Top 5 Wheat Producing States", fontsize=14, fontweight="bold", color="brown")
plt.ylabel("Wheat Production (1000 tons)")
plt.xlabel("State")
plt.xticks(rotation=45)
for bar, state in zip(bars, wheat_state.index):
    bar.set_label(state)
plt.legend(title="States", bbox_to_anchor=(1.05, 1), loc='upper left')
save_plot("top5_wheat_bar.png")

# Pie Chart (%)
plt.figure(figsize=(8,8))
plt.pie(wheat_state.values, labels=wheat_state.index, autopct='%1.1f%%', colors=wheat_colors, startangle=140)
plt.title("Top 5 Wheat Producing States (% Share)", fontsize=14, fontweight="bold")
save_plot("top5_wheat_pie.png")

# =================== OILSEEDS ANALYSIS ===================
oilseed_state = (
    df.groupby("State Name")["OILSEEDS PRODUCTION (1000 tons)"]
      .sum()
      .sort_values(ascending=False)
      .head(5)
)

colors = ['orange', 'green', 'blue', 'red', 'purple']  # one color per state

plt.figure(figsize=(10,6))
bars = plt.bar(oilseed_state.index, oilseed_state.values, color=colors, edgecolor="black")

plt.title("Top 5 Oilseeds Producing States (Total Production)", fontsize=14, fontweight="bold", color="darkorange")
plt.ylabel("Oilseeds Production (1000 tons)")
plt.xlabel("State")
plt.xticks(rotation=45)

# Annotate each bar
for i, value in enumerate(oilseed_state.values):
    plt.text(oilseed_state.index[i], value + 100, f"{value:.0f}", ha='center', va='bottom', fontweight="bold")

# Correct legend
for bar, state in zip(bars, oilseed_state.index):
    bar.set_label(state)
plt.legend(title="States", bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()

# Save figure
plt.savefig("top5_oilseeds.png", dpi=300)

# Show figure
plt.show()

# =================== SUNFLOWER ANALYSIS ===================
sunflower_state = (
    df.groupby("State Name")["SUNFLOWER PRODUCTION (1000 tons)"]
      .sum()
      .sort_values(ascending=False)
      .head(7)
)

sunflower_colors = ['gold', 'lightcoral', 'limegreen', 'royalblue', 'violet', 'orange', 'turquoise']

plt.figure(figsize=(10,6))
bars = plt.bar(sunflower_state.index, sunflower_state.values, color=sunflower_colors, edgecolor="black")

plt.title("Top 7 Sunflower Producing States (Total Production)", fontsize=14, fontweight="bold")
plt.ylabel("Sunflower Production (1000 tons)")
plt.xlabel("State")
plt.xticks(rotation=45)

for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, f'{int(bar.get_height())}', 
             ha='center', va='bottom', fontsize=10, fontweight="bold")

for bar, state in zip(bars, sunflower_state.index):
    bar.set_label(state)
plt.legend(title="States", bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.savefig("top7_sunflower.png", dpi=300)
plt.show()

# =================== SUGARCANE ANALYSIS ===================
sugarcane_trend = df.groupby("Year")["SUGARCANE PRODUCTION (1000 tons)"].sum().tail(50)

plt.figure(figsize=(14,7))
plt.plot(sugarcane_trend.index, sugarcane_trend.values, marker="o", markersize=8,
         color="orange", linewidth=3, linestyle="-", label="Sugarcane Production")

max_year = sugarcane_trend.idxmax()
min_year = sugarcane_trend.idxmin()
plt.scatter(max_year, sugarcane_trend[max_year], color="green", s=150, zorder=5, label="Max Production")
plt.scatter(min_year, sugarcane_trend[min_year], color="red", s=150, zorder=5, label="Min Production")

plt.text(max_year, sugarcane_trend[max_year]+5000, f'Max: {sugarcane_trend[max_year]:,}', ha='center', fontweight="bold")
plt.text(min_year, sugarcane_trend[min_year]-5000, f'Min: {sugarcane_trend[min_year]:,}', ha='center', fontweight="bold")

plt.title("India's Sugarcane Production (Last 50 Years)", fontsize=16, fontweight="bold", color="darkblue")
plt.xlabel("Year", fontsize=12, fontweight="bold")
plt.ylabel("Production (1000 tons)", fontsize=12, fontweight="bold")
plt.grid(True, linestyle="--", alpha=0.5)
plt.xticks(rotation=45)
plt.yticks(fontweight="bold")
plt.legend(title="Legend", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig("sugarcane_trend.png", dpi=300)
plt.show()

# =================== RICE VS WHEAT ===================
rice_trend = df.groupby("Year")["RICE PRODUCTION (1000 tons)"].sum().tail(50)
wheat_trend = df.groupby("Year")["WHEAT PRODUCTION (1000 tons)"].sum().tail(50)

plt.figure(figsize=(14,7))
plt.plot(rice_trend.index, rice_trend.values, marker="o", markersize=6, linestyle="-", 
         color="gold", linewidth=3, label="Rice")
plt.plot(wheat_trend.index, wheat_trend.values, marker="o", markersize=6, linestyle="-", 
         color="royalblue", linewidth=3, label="Wheat")

plt.scatter(rice_trend.idxmax(), rice_trend.max(), color="darkorange", s=150, zorder=5, label="Max Rice")
plt.scatter(wheat_trend.idxmax(), wheat_trend.max(), color="navy", s=150, zorder=5, label="Max Wheat")

plt.text(rice_trend.idxmax(), rice_trend.max()+5000, f'{rice_trend.max():,}', ha='center', fontweight="bold")
plt.text(wheat_trend.idxmax(), wheat_trend.max()+5000, f'{wheat_trend.max():,}', ha='center', fontweight="bold")

plt.title("India's Rice Vs Wheat Production (Last 50 Years)", fontsize=16, fontweight="bold", color="darkgreen")
plt.xlabel("Year", fontsize=12, fontweight="bold")
plt.ylabel("Production (1000 tons)",  fontsize=12, fontweight="bold")
plt.grid(True, linestyle="--", alpha=0.5)
plt.xticks(rotation=45)
plt.yticks(fontweight="bold")
plt.legend(title="Legend", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig("rice_vs_wheat.png", dpi=300)
plt.show()

#========================= Rice production (west bengal district)===============

wb_data = df[df["State Name"] == "West Bengal"]

# Group by Year and sum rice production
rice_wb_trend = wb_data.groupby("Year")["RICE PRODUCTION (1000 tons)"].sum()

plt.figure(figsize=(12,6))
plt.plot(
    rice_wb_trend.index, rice_wb_trend.values,
    marker="o", markersize=6, color="seagreen", linewidth=3, label="Rice Production"
)

# Highlight max and min
max_year = rice_wb_trend.idxmax()
min_year = rice_wb_trend.idxmin()
plt.scatter(max_year, rice_wb_trend[max_year], color="darkgreen", s=120, label="Max")
plt.scatter(min_year, rice_wb_trend[min_year], color="red", s=120, label="Min")

# Annotate values
plt.text(max_year, rice_wb_trend[max_year]+500, f'Max: {rice_wb_trend[max_year]:,}', ha="center", fontweight="bold")
plt.text(min_year, rice_wb_trend[min_year]-500, f'Min: {rice_wb_trend[min_year]:,}', ha="center", fontweight="bold")

# Labels and title
plt.title("Rice Production in West Bengal (Over Years)", fontsize=16, fontweight="bold", color="darkgreen")
plt.xlabel("Year", fontsize=12, fontweight="bold")
plt.ylabel("Rice Production (1000 tons)", fontsize=12, fontweight="bold")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("westbengal_rice.png", dpi=300)
plt.show()

# =================== TOP 10 WHEAT PRODUCTION YEARS (Uttar Pradesh) ===================

# Filter for Uttar Pradesh
up_data = df[df["State Name"] == "Uttar Pradesh"]

# Group by Year and sum wheat production
wheat_up = up_data.groupby("Year")["WHEAT PRODUCTION (1000 tons)"].sum()

# Get top 10 years
top10_wheat_up = wheat_up.sort_values(ascending=False).head(10)

# Colorful bars (10 different colors)
colors = ['gold', 'lightcoral', 'limegreen', 'royalblue', 'violet', 
          'orange', 'turquoise', 'pink', 'brown', 'cyan']

plt.figure(figsize=(12,6))
bars = plt.bar(top10_wheat_up.index.astype(str), top10_wheat_up.values, 
               color=colors, edgecolor="black")

# Title and labels
plt.title("Top 10 Wheat Production Years - Uttar Pradesh", fontsize=16, fontweight="bold", color="darkgreen")
plt.xlabel("Year", fontsize=12, fontweight="bold")
plt.ylabel("Wheat Production (1000 tons)", fontsize=12, fontweight="bold")

# Annotate values on bars
for bar in bars:
    plt.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height() + 200, 
        f"{int(bar.get_height()):,}", 
        ha="center", va="bottom", fontsize=10, fontweight="bold"
    )

plt.xticks(rotation=45, fontsize=10, fontweight="bold")
plt.yticks(fontweight="bold")

# Legend mapping each year to color
for bar, year in zip(bars, top10_wheat_up.index.astype(str)):
    bar.set_label(year)
plt.legend(title="Years", bbox_to_anchor=(1.05, 1), loc="upper left")

plt.tight_layout()
plt.savefig("top10_wheat_up_colorful.png", dpi=300)
plt.show()


# =================== MILLET PRODUCTION ANALYSIS ===================

# Create a new "Total Millet Production" column by summing different millet types
df["TOTAL MILLET PRODUCTION (1000 tons)"] = (
    df["PEARL MILLET PRODUCTION (1000 tons)"] +
    df["FINGER MILLET PRODUCTION (1000 tons)"] +
    df["SORGHUM PRODUCTION (1000 tons)"]
)

# Group by year and sum across India
millet_year = (
    df.groupby("Year")["TOTAL MILLET PRODUCTION (1000 tons)"]
      .sum()
      .tail(50)   # last 50 years
)

# --- Line Graph ---
plt.figure(figsize=(12,6))
plt.plot(millet_year.index, millet_year.values, marker="o", color="darkgreen", linewidth=2)

plt.title("Millet Production in India (Last 50 Years)", fontsize=16, fontweight="bold", color="darkblue")
plt.ylabel("Millet Production (1000 tons)")
plt.xlabel("Year")
plt.xticks(rotation=45)

# Annotate values every 10 years for clarity
for i in range(0, len(millet_year), 10):
    plt.text(millet_year.index[i], millet_year.values[i]+50,
             f"{millet_year.values[i]:.0f}",
             ha="center", fontweight="bold", color="black")

plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("millet_last50years.png", dpi=300)
plt.show()

# =================== SORGHUM PRODUCTION (KHARIF vs RABI) ===================

# Group by State and sum both kharif & rabi sorghum
sorghum_region = (
    df.groupby("State Name")[["KHARIF SORGHUM PRODUCTION (1000 tons)", 
                               "RABI SORGHUM PRODUCTION (1000 tons)"]]
      .sum()
      .sort_values("KHARIF SORGHUM PRODUCTION (1000 tons)", ascending=False)
      .head(10)   # top 10 states for clarity
)

# --- Plotting ---
plt.figure(figsize=(12,6))

bar_width = 0.4
x = range(len(sorghum_region))

plt.bar([i - bar_width/2 for i in x], 
        sorghum_region["KHARIF SORGHUM PRODUCTION (1000 tons)"], 
        width=bar_width, color="goldenrod", label="Kharif Sorghum")

plt.bar([i + bar_width/2 for i in x], 
        sorghum_region["RABI SORGHUM PRODUCTION (1000 tons)"], 
        width=bar_width, color="teal", label="Rabi Sorghum")

# Titles & Labels
plt.title("Sorghum Production (Kharif vs Rabi) by Top States", 
          fontsize=16, fontweight="bold", color="darkred")
plt.ylabel("Production (1000 tons)")
plt.xlabel("State")
plt.xticks(x, sorghum_region.index, rotation=45, ha="right")

# Annotate bars with values
for i, val in enumerate(sorghum_region["KHARIF SORGHUM PRODUCTION (1000 tons)"]):
    plt.text(i - bar_width/2, val + 20, f"{int(val)}", ha="center", fontsize=8, fontweight="bold")

for i, val in enumerate(sorghum_region["RABI SORGHUM PRODUCTION (1000 tons)"]):
    plt.text(i + bar_width/2, val + 20, f"{int(val)}", ha="center", fontsize=8, fontweight="bold")

plt.legend(title="Season")
plt.tight_layout()
plt.savefig("sorghum_kharif_rabi.png", dpi=300)
plt.show()

# =================== GROUNDNUT PRODUCTION ANALYSIS ===================

# Group by state and sum groundnut production
groundnut_state = (
    df.groupby("State Name")["GROUNDNUT PRODUCTION (1000 tons)"]
      .sum()
      .sort_values(ascending=False)
      .head(7)   # top 7 states
)

# Colors for each state
groundnut_colors = ['orange', 'green', 'royalblue', 'red', 'purple', 'gold', 'teal']

# --- Plotting ---
plt.figure(figsize=(10,6))
bars = plt.bar(groundnut_state.index, groundnut_state.values, color=groundnut_colors, edgecolor="black")

# Titles & Labels
plt.title("Top 7 Groundnut Producing States (Total Production)", fontsize=16, fontweight="bold", color="brown")
plt.ylabel("Groundnut Production (1000 tons)")
plt.xlabel("State")
plt.xticks(rotation=45)

# Annotate bars with values
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, 
             f"{int(bar.get_height())}", ha='center', va='bottom', fontsize=10, fontweight="bold")

# Add legend
for bar, state in zip(bars, groundnut_state.index):
    bar.set_label(state)
plt.legend(title="States", bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.savefig("top7_groundnut.png", dpi=300)
plt.show()

# =================== SOYABEAN PRODUCTION & YIELD ANALYSIS ===================

# Group by state for production
soyabean_state_prod = (
    df.groupby("State Name")["SOYABEAN PRODUCTION (1000 tons)"]
      .sum()
      .sort_values(ascending=False)
      .head(5)   # Top 5 states by production
)

# Group by state for yield
soyabean_state_yield = (
    df.groupby("State Name")["SOYABEAN YIELD (Kg per ha)"]
      .mean()   # taking average yield efficiency
      .sort_values(ascending=False)
      .head(5)  # Top 5 states by yield
)

# --- Plotting Production ---
plt.figure(figsize=(14,6))

plt.subplot(1,2,1)  # left chart
prod_colors = ['gold', 'royalblue', 'lightcoral', 'limegreen', 'violet']
bars1 = plt.bar(soyabean_state_prod.index, soyabean_state_prod.values, color=prod_colors, edgecolor="black")

plt.title("Top 5 Soyabean Producing States", fontsize=14, fontweight="bold", color="darkgreen")
plt.ylabel("Production (1000 tons)")
plt.xticks(rotation=30)

# Annotate values
for bar in bars1:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height()+50,
             f"{int(bar.get_height())}", ha='center', va='bottom', fontsize=9, fontweight="bold")

# --- Plotting Yield Efficiency ---
plt.subplot(1,2,2)  # right chart
yield_colors = ['orange', 'purple', 'turquoise', 'red', 'green']
bars2 = plt.bar(soyabean_state_yield.index, soyabean_state_yield.values, color=yield_colors, edgecolor="black")

plt.title("Top 5 Soyabean Yield Efficient States", fontsize=14, fontweight="bold", color="darkblue")
plt.ylabel("Yield (Kg per ha)")
plt.xticks(rotation=30)

# Annotate values
for bar in bars2:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height()+20,
             f"{int(bar.get_height())}", ha='center', va='bottom', fontsize=9, fontweight="bold")

plt.tight_layout()
plt.savefig("soyabean_production_yield.png", dpi=300)
plt.show()

# =================== OILSEEDS PRODUCTION MAP ===================
oilseed_state = (
    df.groupby("State Name")["OILSEEDS PRODUCTION (1000 tons)"]
      .sum()
      .sort_values(ascending=False)
      .head(7)
)

# Set modern style
sns.set_style("whitegrid")
plt.figure(figsize=(12,7))

# Pick a bright color palette
colors = sns.color_palette("husl", len(oilseed_state))

# Create bar plot
bars = plt.bar(oilseed_state.index, oilseed_state.values, color=colors, edgecolor="black", linewidth=1.2)

# Title and labels
plt.title("Top Oilseed Producing States in India", fontsize=18, fontweight="bold", color="darkblue")
plt.ylabel("Oilseeds Production (1000 tons)", fontsize=12, fontweight="bold")
plt.xlabel("State", fontsize=12, fontweight="bold")
plt.xticks(rotation=30, ha="right", fontsize=11, fontweight="bold")

# Annotate bars
for bar in bars:
    yval = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2, yval + (yval*0.02),
        f"{int(yval)}", ha="center", va="bottom", fontsize=11, fontweight="bold", color="black"
    )

# Add gridlines for clarity
plt.grid(axis="y", linestyle="--", alpha=0.6)

plt.tight_layout()
plt.savefig("oilseeds_top_states_bar.png", dpi=300)
plt.show()

# =================== IMPACT OF CULTIVATED AREA ON PRODUCTION ===================
area_prod = pd.DataFrame({
    "Rice Area": df["RICE AREA (1000 ha)"],
    "Rice Production": df["RICE PRODUCTION (1000 tons)"],
    "Wheat Area": df["WHEAT AREA (1000 ha)"],
    "Wheat Production": df["WHEAT PRODUCTION (1000 tons)"],
    "Maize Area": df["MAIZE AREA (1000 ha)"],
    "Maize Production": df["MAIZE PRODUCTION (1000 tons)"]
})

# Convert into long format for plotting
long_df = pd.DataFrame({
    "Crop": ["Rice"] * len(area_prod) + ["Wheat"] * len(area_prod) + ["Maize"] * len(area_prod),
    "Area": pd.concat([area_prod["Rice Area"], area_prod["Wheat Area"], area_prod["Maize Area"]], ignore_index=True),
    "Production": pd.concat([area_prod["Rice Production"], area_prod["Wheat Production"], area_prod["Maize Production"]], ignore_index=True)
})

plt.figure(figsize=(12,7))
sns.set_style("whitegrid")

# Scatter with regression line for each crop
sns.scatterplot(data=long_df, x="Area", y="Production", hue="Crop", palette="Set2", s=60, alpha=0.7, edgecolor="black")
sns.regplot(data=long_df[long_df["Crop"]=="Rice"], x="Area", y="Production", scatter=False, color="green", label="Rice Trend")
sns.regplot(data=long_df[long_df["Crop"]=="Wheat"], x="Area", y="Production", scatter=False, color="orange", label="Wheat Trend")
sns.regplot(data=long_df[long_df["Crop"]=="Maize"], x="Area", y="Production", scatter=False, color="blue", label="Maize Trend")

plt.title("Impact of Cultivated Area on Production (Rice, Wheat, Maize)", fontsize=16, fontweight="bold", color="darkblue")
plt.xlabel("Cultivated Area (1000 ha)", fontsize=12, fontweight="bold")
plt.ylabel("Production (1000 tons)", fontsize=12, fontweight="bold")
plt.legend(title="Crop", fontsize=11)
plt.grid(alpha=0.4)

plt.tight_layout()
plt.savefig("impact_area_vs_production.png", dpi=300)
plt.show()

#================= RICE VS WHEAT ======================================

yield_state = df.groupby("State Name")[["RICE YIELD (Kg per ha)", "WHEAT YIELD (Kg per ha)"]].mean()

yield_state = yield_state.sort_values("RICE YIELD (Kg per ha)", ascending=False)

x = np.arange(len(yield_state.index))  # states
width = 0.35

plt.figure(figsize=(14,7))
bars1 = plt.bar(x - width/2, yield_state["RICE YIELD (Kg per ha)"], width, label="Rice Yield", color="gold")
bars2 = plt.bar(x + width/2, yield_state["WHEAT YIELD (Kg per ha)"], width, label="Wheat Yield", color="royalblue")

# Titles and labels
plt.title("Rice vs Wheat Yield Across States (Kg per ha)", fontsize=16, fontweight="bold", color="darkgreen")
plt.ylabel("Yield (Kg per ha)", fontsize=12, fontweight="bold")
plt.xlabel("State", fontsize=12, fontweight="bold")
plt.xticks(x, yield_state.index, rotation=45, ha="right")

# Annotate values on top of bars
for bar in bars1 + bars2:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
             f"{int(bar.get_height())}", ha='center', va='bottom', fontsize=8, fontweight="bold")

# Grid and legend
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.legend(title="Crop", fontsize=10)

plt.tight_layout()
plt.savefig("rice_vs_wheat_yield.png", dpi=300)
plt.show()