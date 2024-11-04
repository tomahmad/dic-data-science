import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Mengatur judul dashboard
st.title("Dashboard Penyewaan Sepeda")

# Load dataset dari folder bike-sharing-dataset
day_df = pd.read_csv("data/day.csv")

# Mengubah kolom tanggal menjadi tipe datetime
day_df["dteday"] = pd.to_datetime(day_df["dteday"])

# Sidebar untuk memilih rentang waktu
st.sidebar.header("Filter Rentang Waktu")
start_date = st.sidebar.date_input("Tanggal Mulai", day_df["dteday"].min())
end_date = st.sidebar.date_input("Tanggal Akhir", day_df["dteday"].max())

# Filter data berdasarkan rentang waktu
filtered_df = day_df[
    (day_df["dteday"] >= pd.to_datetime(start_date))
    & (day_df["dteday"] <= pd.to_datetime(end_date))
]

# 1. Distribusi Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda
st.markdown("### 1. Distribusi Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda",)
filtered_df["weathersit"] = filtered_df["weathersit"].map(
    {
        1: "Cerah",
        2: "Berkabut",
        3: "Hujan Ringan",
        4: "Hujan Lebat/Badai",
    }
)

fig, ax = plt.subplots()
sns.boxplot(data=filtered_df, x="weathersit", y="cnt", ax=ax)
ax.set_title("Distribusi Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda")
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)


# 2. Analisis Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda
st.markdown("### 2. Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda",)
weather_data = filtered_df.groupby("weathersit")["cnt"].sum().reset_index()

fig, ax = plt.subplots()
sns.barplot(data=weather_data, x="weathersit", y="cnt", ax=ax)
ax.set_title("Pengaruh Cuaca terhadap Penyewaan Sepeda")
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

# 3. Analisis Pengaruh Hari Kerja, Akhir Pekan, dan Hari Libur
st.markdown("### 3. Pengaruh Hari Libur, Akhir Pekan, dan Hari Kerja terhadap Penyewaan Sepeda")
filtered_df["day_type"] = filtered_df.apply(
    lambda row: (
        "Hari Libur"
        if row["holiday"] == 1
        else ("Akhir Pekan" if row["workingday"] == 0 else "Hari Kerja")
    ),
    axis=1,
)
day_type_data = (
    filtered_df.groupby("day_type")[["casual", "registered"]].sum().reset_index()
)
day_type_data_melted = day_type_data.melt(
    id_vars="day_type", var_name="Pengguna", value_name="Jumlah Penyewaan"
)

fig, ax = plt.subplots()
sns.barplot(
    data=day_type_data_melted, x="day_type", y="Jumlah Penyewaan", hue="Pengguna", ax=ax
)
ax.set_title("Perbandingan Penyewaan Sepeda Berdasarkan Jenis Hari dan Jenis Pengguna")
ax.set_xlabel("Jenis Hari")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

# 4. Tren Penyewaan Sepeda dari Waktu ke Waktu (Bulanan)
st.markdown("### 4. Tren Penyewaan Sepeda dari Waktu ke Waktu")
monthly_data = filtered_df.resample("ME", on="dteday").sum()

fig, ax = plt.subplots()
sns.lineplot(data=monthly_data, x=monthly_data.index, y="cnt", ax=ax, marker="o")
ax.set_title("Tren Penyewaan Sepeda Bulanan")
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Penyewaan")
plt.xticks(rotation=45)
st.pyplot(fig)

# 5. Perbandingan Penggunaan Sepeda antara Pengguna Kasual dan Terdaftar
st.markdown("### 5. Perbandingan Penggunaan Sepeda antara Pengguna Kasual dan Terdaftar")
monthly_casual_registered = monthly_data[["casual", "registered"]]

fig, ax = plt.subplots()
sns.lineplot(data=monthly_casual_registered, ax=ax)
ax.set_title("Penggunaan Sepeda Kasual vs Terdaftar per Bulan")
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Penyewaan")
plt.xticks(rotation=45)
st.pyplot(fig)

# Informasi tambahan untuk memberikan interpretasi kepada pengguna
st.write(
    """
Berikut adalah kesimpulan yang dapat ditarik:

**1. Bagaimana Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda?**
   - Cuaca memiliki pengaruh signifikan terhadap penyewaan sepeda. Cuaca buruk seperti hujan lebat dan badai menurunkan jumlah penyewaan, sementara cuaca cerah dan berawan ringan mendorong lebih banyak orang untuk menyewa sepeda.
   - Dari analisis data, terlihat bahwa jumlah penyewaan cenderung lebih tinggi pada hari-hari dengan cuaca yang baik (kategori cuaca 1: cerah atau sedikit mendung) dibandingkan hari-hari dengan kondisi cuaca yang lebih berat.
   - Kesimpulan: Semakin baik cuaca, semakin tinggi jumlah penyewaan sepeda, karena orang cenderung lebih memilih bersepeda ketika kondisi cuaca mendukung.

**2. Bagaimana Pengaruh Hari Libur, Hari Kerja, dan Akhir Pekan terhadap Penyewaan Sepeda?**
   - Hari Kerja khususnya hari Jumat menunjukkan peningkatan penyewaan sepeda dibandingkan hari libur atau akhir pekan.

**3. Bagaimana Tren Jumlah Penyewaan Sepeda dari Waktu ke Waktu (Year-on-Year, Month-to-Month)? Bulan Berapa Penyewaan Sepeda Tertinggi?**
   - Secara Year-on-Year (y-on-y), tren penyewaan sepeda cenderung meningkat dari tahun 2011 ke tahun 2012.
   - Secara Month-to-Month (m-to-m), bulan-bulan dengan cuaca hangat seperti Juni hingga September menunjukkan jumlah penyewaan sepeda tertinggi, sementara musim dingin (November hingga Februari) menunjukkan penurunan.
   - Bulan dengan Penyewaan Tertinggi: Bulan Juni (tahun 2011) atau September (tahun 2012) menjadi puncak penyewaan sepeda, saat cuaca cerah, suhu hangat, dan waktu siang yang lebih panjang mendorong lebih banyak orang untuk bersepeda.
   - Kesimpulan: Musim dan cuaca sangat memengaruhi jumlah penyewaan sepeda, dengan puncak tertinggi pada bulan-bulan musim panas.

**4. Bagaimana Tren Penggunaan Sepeda antara Pengguna Kasual dan Terdaftar? Apakah Pengguna Terdaftar Menyewa Sepeda Lebih Sering daripada Pengguna Kasual?**
   - Pengguna Terdaftar menyewa sepeda lebih sering dibandingkan dengan pengguna kasual.
"""
)
