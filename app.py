import pandas as pd
import plotly.express as px
import streamlit as st

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="Dashboard PWS-PTM Kemenkes", page_icon="📈", layout="wide"
)

st.title("📈 Dashboard Pemantauan Wilayah Setempat PTM (PWS-PTM)")
st.write(
    "Aplikasi interaktif untuk analisis laporan PWS-PTM (Hipertensi, Diabetes,"
    " Obesitas, SPM, dll) berdasarkan file Excel."
)

# 1. Fitur Upload File Excel PWS PTM oleh Pengguna
uploaded_file = st.file_uploader(
    "Upload file laporan Excel PWS PTM (.xlsx)", type=["xlsx", "csv"]
)

if uploaded_file is not None:
  try:
    # Membaca seluruh sheet yang ada di dalam file Excel PWS PTM
    xls = pd.ExcelFile(uploaded_file)
    sheet_list = xls.sheet_names

    # Membersihkan sheet 'DASBOARD' jika ada
    valid_sheets = [s for s in sheet_list if s.upper() != "DASBOARD"]

    st.success("✅ File PWS PTM berhasil dimuat!")

    # 2. Sidebar Menu Pilihan Program / Sheet
    st.sidebar.header("🗂️ Menu Program PTM")
    pilih_menu = st.sidebar.selectbox("Pilih Kategori / Sheet:", options=valid_sheets)

    st.sidebar.markdown("---")
    st.sidebar.info(
        "💡 Anda sedang memantau indikator program PTM berdasarkan sheet yang"
        " dipilih."
    )

    # Membaca data dari sheet yang dipilih
    df = pd.read_excel(uploaded_file, sheet_name=pilih_menu)

    st.subheader(f"📂 Program / Kategori: {pilih_menu}")

    # 3. Menampilkan Ringkasan & Tabel Data
    if not df.empty:
      st.markdown("### 📋 Pratinjau Tabel Data")
      st.dataframe(df.dropna(how="all"), use_container_width=True)

      # Analisis Khusus Berdasarkan Nama Sheet
      if pilih_menu == "Bulanan":
        st.markdown("### 📊 Analisis Bulanan")
        st.info(
            "Sheet Bulanan merekapitulasi capaian layanan PTM dari Januari"
            " sampai Desember."
        )

      elif pilih_menu == "Tahunan":
        st.markdown("### 📈 Analisis Tahunan")
        st.info(
            "Sheet Tahunan membandingkan target dan capaian antar tahun (2022"
            " - 2026)."
        )

      elif pilih_menu == "Wilayah":
        st.markdown("### 🗺️️ Analisis Per Wilayah (Desa/Kelurahan)")
        st.info(
            "Menampilkan sebaran capaian program PTM di setiap desa/kelurahan"
            " wilayah kerja."
        )

      else:
        st.markdown(f"### 🎯 Indikator Khusus: {pilih_menu}")
        st.success(
            f"Data terperinci untuk program **{pilih_menu}** siap digunakan"
            " untuk pelaporan."
        )

    else:
      st.warning(
          f"Sheet '{pilih_menu}' tidak memiliki data atau format tabel kosong."
      )

  except Exception as e:
    st.error(
        f"Terjadi kesalahan saat membaca file Excel: {e}. Pastikan format file"
        " PWS PTM benar."
    )

else:
  st.info(
      "📁 Silakan upload file Excel laporan PWS PTM Anda melalui tombol di atas"
      " untuk mulai menganalisis."
  )