import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# tlg

def peakbike():
    musim_name = ('Springer', 'Summer', 'Fall', 'Winter')
    musim = (471348, 918589, 1061129, 841613)
    musim_data = dict(zip(musim_name, musim))
    peakk = pd.DataFrame(list(musim_data.items()), columns=["Musim", "Jumlah"])

    return peakk

main_df = pd.read_csv("main_data.csv")

datetime_columns = ["dteday"]
main_df.sort_values(by="dteday", inplace=True)
main_df.reset_index(inplace=True)

for column in datetime_columns:
    main_df[column] = pd.to_datetime(main_df[column])

min_date = main_df["dteday"].min()
max_date = main_df["dteday"].max()

with st.sidebar:
    st.image("https://i.postimg.cc/4N3JY6bP/bikerental.png")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

mainan_df = main_df[(main_df["dteday"] >= str(start_date)) & 
                (main_df["dteday"] <= str(end_date))]

st.header('Bike Rental')
st.subheader("Peak Bike Rental Seasons")

peakbiker = peakbike()
fig, ax = plt.subplots(figsize=(7, 5))
 
max_val = peakbiker["Jumlah"].max()
colors = ["#72BCD4" if val == max_val else "#D3D3D3" for val in peakbiker["Jumlah"].head(4)]
# colors = colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#72BCD4"]
 
sns.barplot(x="Musim", y="Jumlah", data=peakbiker.head(4), palette=colors, ax=ax)
ax.set_yticks(peakbiker["Jumlah"].head(4))
ax.set_ylabel("Jumlah Penyewaan Sepeda")
ax.set_xlabel("Musim", fontsize=30)
ax.set_title("Perbandingan Minat Penyewaan Sepeda Antar Musim", loc="center", fontsize=14)
 
st.pyplot(fig)

st.subheader("Bike Rental Customer Chart")
fig2, ax2 = plt.subplots(figsize=(7, 5))

day = pd.read_csv("https://raw.githubusercontent.com/nararyabhuanaa/proyek_analisis_data/refs/heads/main/dasboard/main_data.csv")
day["dteday"] = pd.to_datetime(day["dteday"])
day_last_60 = day.sort_values("dteday").tail(60)

sns.lineplot(x="dteday", y="cnt", data=day_last_60, ax=ax2)

ax2.set_title("Jumlah Pelanggan Penyewa Sepeda (60 Hari Terakhir)")
ax2.set_xlabel("Tanggal")
ax2.set_ylabel("Jumlah Pelanggan")

# Rotasi label tanggal
plt.setp(ax2.get_xticklabels(), rotation=45)

st.pyplot(fig2)

st.caption('Copyright (c) Bike Rental 2025')
