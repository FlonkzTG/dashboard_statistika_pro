import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import io
import time
import base64
import os

# --- 1. KONFIGURASI TEMA (NATIVE STREAMLIT) ---
st.set_page_config(page_title="Dashboard Evaluasi Akademik", page_icon="🎓", layout="wide")

# CSS Minimalis (Hanya untuk aksen warna teks dan tombol, tidak merusak Dark/Light mode)
st.markdown("""
    <style>
    h1, h2, h3 { color: #FF8C00 !important; }
    div[data-testid="stMetricValue"] { color: #FF8C00; }
    .stButton>button { background-color: #FF8C00; color: #FFFFFF; font-weight: bold; border-radius: 8px; border: none; }
    .stButton>button:hover { background-color: #E67E22; color: #FFFFFF; }
    .insight-box { border-left: 5px solid #FF8C00; padding: 15px; border-radius: 5px; font-style: italic; background-color: rgba(255, 140, 0, 0.1); }
    </style>
""", unsafe_allow_html=True)

# --- 2. FUNGSI QoL & ALGORITMA ---
@st.cache_data
def get_excel_template():
    df_temp = pd.DataFrame({'Nama': ['Budi Santoso', 'Siti Aminah', 'Joko Widodo'], 'Nilai': [85, 60, 45]})
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine='openpyxl') as writer:
        df_temp.to_excel(writer, index=False, sheet_name='Data_Nilai')
    return out.getvalue()

def hitung_status(df, kkm):
    kondisi = [
        (df['Nilai'] >= 85), (df['Nilai'] >= 70) & (df['Nilai'] < 85),
        (df['Nilai'] >= 55) & (df['Nilai'] < 70), (df['Nilai'] < 55)
    ]
    df['Huruf Mutu'] = np.select(kondisi, ['A', 'B', 'C', 'D/E'], default='Error')
    df['Status'] = np.where(df['Nilai'] >= kkm, 'LULUS', 'TIDAK LULUS')
    return df

def warna_status(val):
    """Memberikan warna hijau/merah pada teks di tabel Pandas"""
    color = '#28a745' if val == 'LULUS' else '#dc3545'
    return f'color: {color}; font-weight: bold;'

def generate_insight(df, mean_val, kkm):
    lulus = len(df[df['Status'] == 'LULUS'])
    gagal = len(df) - lulus
    
    teks = f"Rata-rata kelas saat ini adalah **{mean_val:.1f}**. "
    if gagal > (len(df) / 2): teks += f"Terdapat **{gagal} mahasiswa** (mayoritas) yang belum mencapai KKM. Diperlukan evaluasi metode pembelajaran."
    else: teks += f"Kinerja kelas memuaskan, **{lulus} mahasiswa** berhasil lulus ujian."
    return teks

def bubble_sort_demo(arr):
    arr_copy = arr.copy()
    n, langkah = len(arr_copy), 0
    for i in range(n):
        for j in range(0, n-i-1):
            langkah += 1
            if arr_copy[j] > arr_copy[j+1]:
                arr_copy[j], arr_copy[j+1] = arr_copy[j+1], arr_copy[j]
    return arr_copy, langkah

# --- 3. ANTARMUKA SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>⚙️ Panel Kontrol</h2>", unsafe_allow_html=True)
    kkm_input = st.number_input("Batas Kelulusan (KKM):", min_value=0, max_value=100, value=60)
    
    st.divider()
    st.subheader("📥 Input Data Kelas")
    st.download_button("📄 Download Template Excel", data=get_excel_template(), file_name="Template_Data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    
    tipe_input = st.radio("Metode Input:", ["Ketik Manual", "Upload File (.xlsx / .csv)"])
    
    if tipe_input == "Ketik Manual":
        raw_text = st.text_area("Format: Nama, Nilai", "Mahasiswa 1, 85\nMahasiswa 2, 45\nMahasiswa 3, 92", height=150)
        if st.button("🚀 Load Data Manual", use_container_width=True):
            baris_data = raw_text.strip().split('\n')
            nama_list, nilai_list = [], []
            for baris in baris_data:
                parts = baris.split(',')
                if len(parts) >= 2:
                    try:
                        nilai_list.append(float(parts[-1].strip()))
                        nama_list.append(",".join(parts[:-1]).strip())
                    except ValueError: pass
            st.session_state['df_raw'] = pd.DataFrame({'Nama': nama_list, 'Nilai': nilai_list})
    else:
        uploaded_file = st.file_uploader("Upload File di sini", type=['xlsx', 'csv'])
        if uploaded_file:
            if uploaded_file.name.endswith('.csv'): df_raw = pd.read_csv(uploaded_file)
            else: df_raw = pd.read_excel(uploaded_file)
            
            kolom_nama = [col for col in df_raw.columns if 'nama' in col.lower()]
            kolom_nilai = [col for col in df_raw.columns if 'nilai' in col.lower() or 'score' in col.lower()]
            
            if kolom_nama and kolom_nilai:
                st.session_state['df_raw'] = df_raw[[kolom_nama[0], kolom_nilai[0]]].rename(columns={kolom_nama[0]: 'Nama', kolom_nilai[0]: 'Nilai'})
            else: st.error("Format kolom tidak dikenali. Gunakan Template.")
            
    if st.button("🔄 Reset Aplikasi", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- 4. DASHBOARD UTAMA ---
st.title("📊 Aplikasi Analisis Distribusi Nilai Mahasiswa")

if 'df_raw' in st.session_state and not st.session_state['df_raw'].empty:
    # --- SISTEM TAB QoL ---
    tab1, tab2, tab3 = st.tabs(["📈 Dashboard Analitik", "📋 Kelola Data & Status", "🔬 Lab Algoritma"])
    
    # Pre-kalkulasi data yang selalu di-update saat user mengedit
    df_raw = st.session_state['df_raw']
    df_final_base = hitung_status(df_raw.dropna(subset=['Nilai']).copy(), kkm_input)
    mean_kelas = df_final_base['Nilai'].mean()

    # == TAB 1: DASHBOARD ==
    with tab1:
        st.markdown("### Ringkasan Eksekutif")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Rata-rata (Mean)", f"{mean_kelas:.2f}")
        col2.metric("Median", f"{df_final_base['Nilai'].median():.2f}")
        col3.metric("Nilai Tertinggi", f"{df_final_base['Nilai'].max():.1f}")
        col4.metric("Nilai Terendah", f"{df_final_base['Nilai'].min():.1f}")
        col5.metric("Std. Deviasi", f"{df_final_base['Nilai'].std():.2f}")
        
        # Area Insight
        st.markdown(f'<div class="insight-box"><b>💡 AI Insight:</b> {generate_insight(df_final_base, mean_kelas, kkm_input)}</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Area Grafik (Transparan & Native)
        c1, c2 = st.columns([6, 4])
        with c1:
            st.markdown("#### Grafik Sebaran Nilai Individu")
            # Bar chart nilai individu + Garis KKM (QoL Tambahan)
            fig_bar_ind = px.bar(df_final_base, x='Nama', y='Nilai', text='Nilai', color='Status',
                                 color_discrete_map={'LULUS':'#28a745', 'TIDAK LULUS':'#dc3545'})
            fig_bar_ind.add_hline(y=kkm_input, line_dash="dash", line_color="red", annotation_text="KKM", annotation_position="top right")
            # Background transparan agar ikut Dark/Light mode sistem
            fig_bar_ind.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_bar_ind, use_container_width=True, theme="streamlit")
            
        with c2:
            st.markdown("#### Rasio Kelulusan")
            status_counts = df_final_base['Status'].value_counts().reset_index()
            fig_pie = px.pie(status_counts, names='Status', values='count', hole=0.4, 
                             color='Status', color_discrete_map={'LULUS':'#28a745', 'TIDAK LULUS':'#dc3545'})
            fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_pie, use_container_width=True, theme="streamlit")

    # == TAB 2: KELOLA DATA & STATUS ==
    with tab2:
        col_edit, col_hasil = st.columns([4, 6])
        
        with col_edit:
            st.markdown("#### ✏️ Live Editor Data")
            st.caption("Ubah nilai/nama di bawah, tabel hasil di sebelah kanan akan otomatis menyesuaikan.")
            df_edited = st.data_editor(st.session_state['df_raw'], num_rows="dynamic", use_container_width=True, height=400)
            
            # Update session state jika ada editan
            if not df_edited.equals(st.session_state['df_raw']):
                st.session_state['df_raw'] = df_edited
                st.rerun() # Refresh instan untuk update grafik
                
        with col_hasil:
            st.markdown("#### 📋 Tabel Status Akhir Mahasiswa")
            st.caption("Tabel otomatis hasil pemrosesan KKM dan Kategori Mutu.")
            
            # Hitung ulang berdasarkan data terbaru dari editor
            df_kalkulasi = hitung_status(df_edited.dropna(subset=['Nilai']).copy(), kkm_input)
            
            if not df_kalkulasi.empty:
                # Terapkan pewarnaan Pandas Styler pada kolom Status
                styled_df = df_kalkulasi.style.map(warna_status, subset=['Status']).format({"Nilai": "{:.1f}"})
                st.dataframe(styled_df, use_container_width=True, height=330)
                
                # Fitur Ekspor
                output_excel = io.BytesIO()
                with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
                    df_kalkulasi.to_excel(writer, index=False, sheet_name='Laporan_Akhir')
                st.download_button("💾 Download Laporan Akhir (.xlsx)", data=output_excel.getvalue(), file_name='Laporan_Kelulusan_Mahasiswa.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', type="primary")

    # == TAB 3: LAB ALGORITMA ==
    with tab3:
        st.markdown("#### 🔬 Pengujian Beban Algoritma (Sorting)")
        st.write("Mensimulasikan cara mesin mengurutkan data nilai menggunakan **Bubble Sort** (Materi Matematika Diskrit / Struktur Data).")
        
        if st.button("Mulai Simulasi Sorting"):
            start_time = time.time()
            data_terurut, iterasi = bubble_sort_demo(df_final_base['Nilai'].tolist())
            waktu_komputasi = time.time() - start_time
            
            st.success(f"Sorting selesai dalam {waktu_komputasi:.5f} detik.")
            st.code(f"Total Data (N): {len(data_terurut)}\nTotal Iterasi Loop: {iterasi} langkah\nKompleksitas: O(N²)\n\nHasil Pengurutan (Terkecil - Terbesar):\n{data_terurut}", language="yaml")

else:
    st.info("👈 Selamat Datang! Silakan masukkan data di Panel Kontrol sebelah kiri untuk memulai aplikasi.")