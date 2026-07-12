import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# KONFIGURASI HALAMAN
# =========================================================
st.set_page_config(
    page_title="Dashboard Harga Pertanian Jawa Timur",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_data():
    df = pd.read_csv("data/harga_pertanian.csv")
    df["nama_kabupaten_kota"] = df["nama_kabupaten_kota"].str.title()
    df["kategori"] = df["kategori"].str.title()
    return df

df = load_data()

# =========================================================
# SIDEBAR - FILTER
# =========================================================
st.sidebar.title("🌾 Filter Data")
st.sidebar.markdown("Gunakan filter di bawah untuk menyesuaikan tampilan data.")

kabupaten_list = sorted(df["nama_kabupaten_kota"].unique())
kategori_list = sorted(df["kategori"].unique())

selected_kabupaten = st.sidebar.multiselect(
    "Pilih Kabupaten/Kota",
    options=kabupaten_list,
    default=kabupaten_list,
)

selected_kategori = st.sidebar.multiselect(
    "Pilih Komoditas",
    options=kategori_list,
    default=kategori_list,
)

# Filter hanya harga > 0 (opsional, karena beberapa data bernilai 0 / tidak tercatat)
hide_zero = st.sidebar.checkbox("Sembunyikan data dengan harga 0 (belum tercatat)", value=True)

df_filtered = df[
    df["nama_kabupaten_kota"].isin(selected_kabupaten)
    & df["kategori"].isin(selected_kategori)
]

if hide_zero:
    df_filtered = df_filtered[df_filtered["jumlah"] > 0]

st.sidebar.markdown("---")
st.sidebar.caption("Sumber data: Data harga komoditas pertanian, Provinsi Jawa Timur, periode Januari 2020.")

# =========================================================
# HEADER
# =========================================================
st.title("🌾 Dashboard Harga Komoditas Pertanian Jawa Timur")
st.markdown(
    "Visualisasi interaktif data **harga komoditas pertanian** "
    "(beras, gabah, jagung, kedelai) di berbagai kabupaten/kota "
    "Provinsi Jawa Timur."
)

if df_filtered.empty:
    st.warning("Tidak ada data untuk kombinasi filter yang dipilih. Silakan ubah filter di sidebar.")
    st.stop()

# =========================================================
# RINGKASAN METRIK
# =========================================================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Jumlah Data", f"{len(df_filtered):,}")
col2.metric("Rata-rata Harga", f"Rp {df_filtered['jumlah'].mean():,.0f}")
col3.metric("Harga Tertinggi", f"Rp {df_filtered['jumlah'].max():,.0f}")
col4.metric("Harga Terendah", f"Rp {df_filtered[df_filtered['jumlah'] > 0]['jumlah'].min():,.0f}"
            if (df_filtered['jumlah'] > 0).any() else "N/A")

st.markdown("---")

# =========================================================
# TAB LAYOUT
# =========================================================
tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Perbandingan Antar Wilayah", "🌽 Perbandingan Antar Komoditas", "📋 Tabel Data", "ℹ️ Tentang"]
)

# ---------------------------------------------------------
# TAB 1: Perbandingan antar kabupaten/kota
# ---------------------------------------------------------
with tab1:
    st.subheader("Rata-rata Harga per Kabupaten/Kota")

    komoditas_pilihan = st.selectbox(
        "Pilih komoditas untuk dibandingkan antar wilayah:",
        options=kategori_list,
        key="tab1_komoditas",
    )

    data_komoditas = df_filtered[df_filtered["kategori"] == komoditas_pilihan].sort_values(
        "jumlah", ascending=False
    )

    if data_komoditas.empty:
        st.info("Tidak ada data untuk komoditas ini pada filter saat ini.")
    else:
        fig_bar = px.bar(
            data_komoditas,
            x="jumlah",
            y="nama_kabupaten_kota",
            orientation="h",
            color="jumlah",
            color_continuous_scale="Greens",
            labels={"jumlah": "Harga (Rp)", "nama_kabupaten_kota": "Kabupaten/Kota"},
            title=f"Harga {komoditas_pilihan} per Kabupaten/Kota",
        )
        fig_bar.update_layout(yaxis={"categoryorder": "total ascending"}, height=600)
        st.plotly_chart(fig_bar, use_container_width=True)

# ---------------------------------------------------------
# TAB 2: Perbandingan antar komoditas
# ---------------------------------------------------------
with tab2:
    st.subheader("Perbandingan Harga Antar Komoditas")

    wilayah_pilihan = st.selectbox(
        "Pilih wilayah untuk melihat rincian komoditas:",
        options=["Semua Wilayah (Rata-rata)"] + kabupaten_list,
        key="tab2_wilayah",
    )

    if wilayah_pilihan == "Semua Wilayah (Rata-rata)":
        data_agg = df_filtered.groupby("kategori", as_index=False)["jumlah"].mean()
        judul = "Rata-rata Harga Semua Komoditas (Seluruh Wilayah Terpilih)"
    else:
        data_agg = df_filtered[df_filtered["nama_kabupaten_kota"] == wilayah_pilihan]
        judul = f"Harga Komoditas di {wilayah_pilihan}"

    if data_agg.empty:
        st.info("Tidak ada data untuk wilayah ini pada filter saat ini.")
    else:
        fig_kom = px.bar(
            data_agg.sort_values("jumlah", ascending=False),
            x="kategori",
            y="jumlah",
            color="kategori",
            labels={"jumlah": "Harga (Rp)", "kategori": "Komoditas"},
            title=judul,
        )
        fig_kom.update_layout(showlegend=False, height=500)
        st.plotly_chart(fig_kom, use_container_width=True)

    st.markdown("#### Distribusi Harga per Komoditas (Semua Wilayah Terpilih)")
    fig_box = px.box(
        df_filtered,
        x="kategori",
        y="jumlah",
        color="kategori",
        labels={"jumlah": "Harga (Rp)", "kategori": "Komoditas"},
    )
    fig_box.update_layout(showlegend=False, height=450)
    st.plotly_chart(fig_box, use_container_width=True)

# ---------------------------------------------------------
# TAB 3: Tabel data
# ---------------------------------------------------------
with tab3:
    st.subheader("Tabel Data Lengkap")
    st.dataframe(
        df_filtered[
            ["nama_kabupaten_kota", "kategori", "jumlah", "satuan", "periode_update"]
        ].rename(
            columns={
                "nama_kabupaten_kota": "Kabupaten/Kota",
                "kategori": "Komoditas",
                "jumlah": "Harga",
                "satuan": "Satuan",
                "periode_update": "Periode",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    csv_download = df_filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Unduh Data Terfilter (CSV)",
        data=csv_download,
        file_name="harga_pertanian_filtered.csv",
        mime="text/csv",
    )

# ---------------------------------------------------------
# TAB 4: Tentang
# ---------------------------------------------------------
with tab4:
    st.subheader("Tentang Dashboard Ini")
    st.markdown(
        """
        Dashboard ini menampilkan data harga komoditas pertanian di Provinsi Jawa Timur,
        mencakup:

        - **Beras Medium**
        - **Beras Premium**
        - **Gabah Kering Giling**
        - **Gabah Kering Panen**
        - **Jagung Pipil Kering**
        - **Kedelai**

        Data mencakup **17 kabupaten/kota** di Jawa Timur pada periode **Januari 2020**.

        Nilai `0` pada data menunjukkan harga yang **tidak tercatat** pada periode tersebut,
        bukan berarti komoditas tersebut gratis.

        Dibuat dengan [Streamlit](https://streamlit.io) dan [Plotly](https://plotly.com/python/).
        """
    )
