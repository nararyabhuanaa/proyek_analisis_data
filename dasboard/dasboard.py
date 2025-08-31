import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Load data
main_df = pd.read_csv("https://raw.githubusercontent.com/nararyabhuanaa/proyek_analisis_data/refs/heads/main/dasboard/main_data.csv")
main_df["dteday"] = pd.to_datetime(main_df["dteday"])
main_df.sort_values("dteday", inplace=True)
main_df.reset_index(drop=True, inplace=True)

min_date = main_df["dteday"].min()
max_date = main_df["dteday"].max()

with st.sidebar:
    st.image("https://i.postimg.cc/4N3JY6bP/bikerental.png")
    start_date, end_date = st.date_input(
        "Rentang Waktu",
        min_value=min_date.date(),
        max_value=max_date.date(),
        value=[min_date.date(), max_date.date()]
    )

# Filter data sesuai rentang tanggal
mainan_df = main_df[(main_df["dteday"].dt.date >= start_date) & 
                    (main_df["dteday"].dt.date <= end_date)]

# --- Chart 1: Peak Bike Rental Seasons ---
st.header('Bike Rental')
st.subheader("Peak Bike Rental Seasons")

# Tambahkan kolom Musim dari data 'season' (1=Spring, 2=Summer, 3=Fall, 4=Winter)
season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
mainan_df["Musim"] = mainan_df["season"].map(season_map)

# Hitung total jumlah per musim
peakbiker = mainan_df.groupby("Musim", as_index=False)["cnt"].sum().rename(columns={"cnt": "Jumlah"})

fig, ax = plt.subplots(figsize=(7, 5))

max_val = peakbiker["Jumlah"].max()
colors = ["#72BCD4" if val == max_val else "#D3D3D3" for val in peakbiker["Jumlah"]]

sns.barplot(x="Musim", y="Jumlah", data=peakbiker, palette=colors, ax=ax)
ax.set_ylabel("Jumlah Penyewaan Sepeda", fontsize=12)
ax.set_xlabel("Musim", fontsize=12)
ax.set_title("Perbandingan Minat Penyewaan Sepeda Antar Musim", fontsize=16)

# Label angka di atas bar
for i, val in enumerate(peakbiker["Jumlah"]):
    ax.text(i, val + (val*0.02), f"{val:,}", ha='center', va='bottom', fontsize=10)

st.pyplot(fig)

# --- Chart 2: Bike Rental Customer Trend ---
st.subheader("Bike Rental Customer Chart")

# Ambil data terakhir sesuai filter
day_last_60 = mainan_df.sort_values("dteday").tail(60)

fig2, ax2 = plt.subplots(figsize=(7, 5))
sns.lineplot(x="dteday", y="cnt", data=day_last_60, ax=ax2)

ax2.set_title("Jumlah Pelanggan Penyewa Sepeda (60 Hari Terakhir)", fontsize=14)
ax2.set_xlabel("Tanggal", fontsize=12)
ax2.set_ylabel("Jumlah Pelanggan", fontsize=12)
plt.setp(ax2.get_xticklabels(), rotation=45)

st.pyplot(fig2)

st.caption('Copyright (c) Bike Rental 2025')
