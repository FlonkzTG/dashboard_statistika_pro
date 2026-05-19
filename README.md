<div align="center">

```
██████╗  █████╗ ███████╗██╗  ██╗██████╗  ██████╗  █████╗ ██████╗ ██████╗ 
██╔══██╗██╔══██╗██╔════╝██║  ██║██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔══██╗
██║  ██║███████║███████╗███████║██████╔╝██║   ██║███████║██████╔╝██║  ██║
██║  ██║██╔══██║╚════██║██╔══██║██╔══██╗██║   ██║██╔══██║██╔══██╗██║  ██║
██████╔╝██║  ██║███████║██║  ██║██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝
╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ 
```

### 📊 Aplikasi Analisis Distribusi Nilai Mahasiswa

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=flat&logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-FF8C00?style=flat)

*Dashboard interaktif berbasis web untuk analisis dan evaluasi nilai akademik mahasiswa secara real-time.*

---

[🚀 Live Demo](#) · [📸 Screenshot](#-screenshot) · [⚙️ Instalasi](#%EF%B8%8F-instalasi) · [📖 Cara Pakai](#-cara-pakai)

</div>

---

## ✨ Fitur Unggulan

| Fitur | Deskripsi |
|---|---|
| 📥 **Multi Input** | Input manual via teks atau upload file `.xlsx` / `.csv` |
| 📄 **Template Excel** | Download template siap pakai langsung dari aplikasi |
| 🎯 **KKM Dinamis** | Atur batas kelulusan secara real-time dari sidebar |
| 💡 **AI Insight** | Analisis otomatis kinerja kelas dalam satu kalimat |
| ✏️ **Live Editor** | Edit data langsung, grafik otomatis ikut berubah |
| 📊 **Visualisasi Interaktif** | Bar chart sebaran nilai + Pie chart rasio kelulusan |
| 🏷️ **Huruf Mutu Otomatis** | Kalkulasi A/B/C/D-E berdasarkan nilai |
| 💾 **Ekspor Laporan** | Download hasil akhir ke format `.xlsx` |
| 🔬 **Lab Algoritma** | Simulasi Bubble Sort dengan analisis kompleksitas O(N²) |
| 🌗 **Dark/Light Mode** | Mengikuti preferensi sistem pengguna |

---

## 📸 Screenshot

```
┌─────────────────────────────────────────────────────────┐
│  ⚙️ Panel Kontrol   │      📊 Dashboard Analitik        │
│                     │                                    │
│  KKM: [60    ]      │  Mean   Median  Max   Min   Std   │
│                     │  75.3   78.0    95.0  42.0  14.2  │
│  [Download Template]│                                    │
│                     │  ████████████ Bar Chart Nilai      │
│  ○ Ketik Manual     │  ▓▓▓▓▓▓░░░░░░ Pie Kelulusan       │
│  ● Upload File      │                                    │
│                     │  💡 AI Insight: Kinerja memuaskan  │
│  [🚀 Load Data]     │                                    │
└─────────────────────────────────────────────────────────┘
```

---

## ⚙️ Instalasi

### Prasyarat
- Python 3.8+
- pip

### Clone & Setup

```bash
# Clone repository
git clone https://github.com/username/dashboard-akademik.git
cd dashboard-akademik

# Install dependencies
pip install -r requirements.txt

# Jalankan aplikasi
streamlit run app.py
```

Aplikasi akan terbuka otomatis di `http://localhost:8501`

---

## 📦 Dependencies

```txt
streamlit
pandas
plotly
numpy
openpyxl
```

---

## 📖 Cara Pakai

### 1️⃣ Input Data

**Metode A — Ketik Manual:**
```
Budi Santoso, 85
Siti Aminah, 60
Joko Prasetyo, 45
```

**Metode B — Upload File:**
- Download template Excel dari sidebar
- Isi kolom `Nama` dan `Nilai`
- Upload kembali ke aplikasi

### 2️⃣ Atur KKM
Geser atau ketik nilai KKM (default: 60) di Panel Kontrol sebelah kiri.

### 3️⃣ Analisis
Navigasi antar tab:
- **📈 Dashboard Analitik** — Lihat grafik dan statistik kelas
- **📋 Kelola Data & Status** — Edit data dan download laporan
- **🔬 Lab Algoritma** — Simulasi sorting dan kompleksitas

### 4️⃣ Export
Klik **"💾 Download Laporan Akhir"** untuk mendapatkan file `.xlsx` berisi nama, nilai, huruf mutu, dan status kelulusan.

---

## 🗂️ Struktur Proyek

```
📁 dashboard-akademik/
├── app.py                  # Aplikasi utama Streamlit
├── requirements.txt        # Daftar dependencies
└── README.md               # Dokumentasi ini
```

---

## 🧮 Sistem Penilaian

| Rentang Nilai | Huruf Mutu | Status |
|:---:|:---:|:---:|
| 85 – 100 | **A** | ✅ LULUS |
| 70 – 84 | **B** | ✅ LULUS |
| 55 – 69 | **C** | Tergantung KKM |
| 0 – 54 | **D/E** | ❌ TIDAK LULUS |

> Status LULUS/TIDAK LULUS ditentukan oleh nilai KKM yang diatur pengguna.

---

## 🚀 Deploy ke Web (Streamlit Cloud)

1. Push repository ini ke GitHub
2. Buka [share.streamlit.io](https://share.streamlit.io)
3. Login dengan akun GitHub
4. Klik **"New app"** → pilih repo → pilih `app.py`
5. Klik **Deploy** — selesai! 🎉

---

## 🤝 Kontribusi

Pull request sangat diterima! Untuk perubahan besar, buka issue terlebih dahulu.

```bash
git checkout -b feature/fitur-baru
git commit -m "feat: tambah fitur baru"
git push origin feature/fitur-baru
```

---

## 📄 Lisensi

Didistribusikan di bawah **MIT License**. Lihat `LICENSE` untuk informasi lebih lanjut.

---

<div align="center">

Dibuat dengan ❤️ menggunakan [Streamlit](https://streamlit.io) · [Plotly](https://plotly.com) · [Pandas](https://pandas.pydata.org)

⭐ **Jangan lupa kasih bintang kalau project ini membantu!** ⭐

</div>
