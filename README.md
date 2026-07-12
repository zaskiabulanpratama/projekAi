# 🌾 Dashboard Harga Pertanian Jawa Timur

Dashboard interaktif berbasis **Streamlit** untuk memvisualisasikan data harga
komoditas pertanian (beras, gabah, jagung, kedelai) di 17 kabupaten/kota
Provinsi Jawa Timur.

## 🚀 Fitur
- Filter interaktif per kabupaten/kota dan komoditas
- Ringkasan metrik (rata-rata, tertinggi, terendah)
- Grafik perbandingan harga antar wilayah
- Grafik perbandingan harga antar komoditas + boxplot distribusi
- Tabel data dengan fitur unduh CSV

## 📁 Struktur Proyek
```
harga-pertanian-jatim/
├── app.py                      # Aplikasi Streamlit utama
├── data/
│   └── harga_pertanian.csv     # Dataset
├── requirements.txt            # Dependensi Python
├── .gitignore
└── README.md
```

## 🖥️ Menjalankan di Lokal

```bash
# 1. Clone repo
git clone https://github.com/USERNAME/harga-pertanian-jatim.git
cd harga-pertanian-jatim

# 2. Buat virtual environment (opsional tapi disarankan)
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependensi
pip install -r requirements.txt

# 4. Jalankan aplikasi
streamlit run app.py
```

Aplikasi akan terbuka otomatis di `http://localhost:8501`.

## ☁️ Cara Deploy ke GitHub + Streamlit Community Cloud (Gratis)

### Langkah 1 — Push proyek ke GitHub
```bash
cd harga-pertanian-jatim
git init
git add .
git commit -m "Initial commit: dashboard harga pertanian Jawa Timur"
git branch -M main
git remote add origin https://github.com/USERNAME/harga-pertanian-jatim.git
git push -u origin main
```
> Ganti `USERNAME` dengan username GitHub kamu. Buat repository kosong terlebih
> dahulu di https://github.com/new (jangan centang "Add README", karena repo
> ini sudah punya).

### Langkah 2 — Deploy ke Streamlit Community Cloud
1. Buka https://share.streamlit.io dan login dengan akun GitHub kamu.
2. Klik **"New app"**.
3. Pilih repository `harga-pertanian-jatim`, branch `main`, dan file utama
   `app.py`.
4. Klik **"Deploy"**.
5. Tunggu beberapa menit — aplikasi akan otomatis online dengan URL seperti:
   `https://harga-pertanian-jatim-USERNAME.streamlit.app`

Setiap kali kamu `git push` perubahan baru ke branch `main`, Streamlit Cloud
akan otomatis redeploy aplikasi.

## 📊 Tentang Data
Data mencakup harga komoditas berikut di 17 kabupaten/kota Jawa Timur pada
periode Januari 2020:
- Beras Medium
- Beras Premium
- Gabah Kering Giling
- Gabah Kering Panen
- Jagung Pipil Kering
- Kedelai

Nilai `0` pada kolom harga menandakan data yang tidak tercatat pada periode
tersebut.

## 🛠️ Teknologi
- [Streamlit](https://streamlit.io) — framework web app
- [Pandas](https://pandas.pydata.org) — pengolahan data
- [Plotly](https://plotly.com/python/) — visualisasi interaktif
