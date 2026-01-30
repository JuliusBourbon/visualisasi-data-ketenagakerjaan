import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. KONFIGURASI HALAMAN & CSS (STYLING)
# ==========================================
st.set_page_config(
    page_title="Dashboard Ketenagakerjaan",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Custom untuk Tampilan "Card" yang Elegan
st.markdown("""
    <style>
        .stApp { background-color: #F0F2F6; }
        
        /* Container Styling */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #FFFFFF;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            border: 1px solid #E0E0E0;
            margin-bottom: 20px;
        }

        /* Styling Headers */
        h3 {
            margin-top: 0 !important;
            padding-bottom: 10px;
            border-bottom: 1px solid #eee;
            font-weight: 600;
            color: #333;
        }
        
        /* Metric Value */
        div[data-testid="stMetricValue"] {
            font-size: 24px;
            color: #007BFF;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🇮🇩 Dashboard Eksekutif: Ketenagakerjaan Indonesia")
st.markdown("Analisis strategis pasar tenaga kerja nasional berdasarkan data 2018-2023.")

# ==========================================
# 2. LOAD DATA
# ==========================================
@st.cache_data
def load_data():
    # Load Data Makro
    try:
        df_makro = pd.read_csv("clean_persentaseBekerjaPengangguran.csv")
        df_makro = df_makro.rename(columns={'Status': 'Tahun', 'Tahun': 'Bulan', 'Periode': 'Persentase', 'Jumlah_Orang': 'Jumlah'})
        df_makro['Persentase'] = pd.to_numeric(df_makro['Persentase'], errors='coerce')
        df_makro['Status'] = df_makro['Persentase'].apply(lambda x: 'Bekerja' if x > 50 else 'Pengangguran')
        df_makro = df_makro[df_makro['Bulan'] != 'Tahunan']
    except: df_makro = pd.DataFrame()

    # Load Data Umur
    try:
        df_umur = pd.read_csv("clean_kelompokUmurPengangguran.csv")
        df_umur['TPT'] = pd.to_numeric(df_umur['TPT'], errors='coerce') 
        unique_vals = df_umur['Tahun'].unique()
        mapping_tahun = {val: 2018 + i for i, val in enumerate(unique_vals)} 
        df_umur['Tahun_Real'] = df_umur['Tahun'].map(mapping_tahun)
    except: df_umur = pd.DataFrame()

    # Load Data Lapangan Usaha
    try:
        df_lapangan = pd.read_csv("clean_RataRataLapangan.csv")
        df_lapangan.columns = ['Provinsi', 'Pertanian', 'Industri', 'Jasa', 'Total', 'Tahun']
        for col in ['Pertanian', 'Industri', 'Jasa', 'Total']:
            df_lapangan[col] = pd.to_numeric(df_lapangan[col], errors='coerce')
        df_lapangan = df_lapangan.dropna(subset=['Total', 'Pertanian', 'Industri'])
    except: df_lapangan = pd.DataFrame()

    # Load Data Pendidikan
    try:
        df_pendidikan = pd.read_csv("clean_RataRataPendidikan.csv")
        df_pendidikan.columns = ['Provinsi', 'Tidak_Sekolah', 'SD', 'SMP', 'SMA_Keatas', 'Total', 'Tahun']
        for col in ['Tidak_Sekolah', 'SD', 'SMP', 'SMA_Keatas', 'Total']:
            df_pendidikan[col] = pd.to_numeric(df_pendidikan[col], errors='coerce')
        df_pendidikan = df_pendidikan.dropna(subset=['SD', 'SMA_Keatas'])
    except: df_pendidikan = pd.DataFrame()

    return df_makro, df_umur, df_lapangan, df_pendidikan

df_makro, df_umur, df_lapangan, df_pendidikan = load_data()


# ==========================================
# BARIS 1: TINJAUAN MAKRO EKONOMI (METRIK)
# ==========================================
with st.container(border=True):
    col_h1, col_f1 = st.columns([3, 1])
    with col_h1:
        st.subheader("📈 Tinjauan Makro Ekonomi (KPI)")
    with col_f1:
        filter_tahun_makro = st.slider("Tahun Laporan:", 2019, 2023, 2023, key="slider_makro")

    if not df_makro.empty and not df_lapangan.empty:
        curr_tpt = df_makro[(df_makro['Tahun'] == filter_tahun_makro) & (df_makro['Bulan'] == 'Agustus') & (df_makro['Status'] == 'Pengangguran')]['Persentase'].values
        prev_tpt = df_makro[(df_makro['Tahun'] == filter_tahun_makro-1) & (df_makro['Bulan'] == 'Agustus') & (df_makro['Status'] == 'Pengangguran')]['Persentase'].values
        curr_gaji = df_lapangan[df_lapangan['Tahun'] == filter_tahun_makro]['Total'].mean()
        
        val_tpt = curr_tpt[0] if len(curr_tpt) > 0 else 0
        delta_tpt = val_tpt - prev_tpt[0] if len(prev_tpt) > 0 else 0
        
        m1, m2, m3 = st.columns(3)
        m1.metric("TPT (Agustus)", f"{val_tpt}%", f"{delta_tpt:.2f}%", delta_color="inverse")
        m2.metric("Rata-rata Upah Nasional", f"Rp {curr_gaji/1000000:.2f} Juta", "per bulan")
        m3.metric("Status Data", f"Tahun {filter_tahun_makro}", "Data Tahunan")


# ==========================================
# BARIS 2: INFORMASI PENGANGGURAN (2 KOLOM)
# ==========================================
with st.container(border=True):
    st.subheader("⚠️ Analisis Pengangguran & Demografi")
    
    col_trend, col_age = st.columns(2)

    # --- KOLOM 1: TREN PENGANGGURAN ---
    with col_trend:
        st.markdown("**Tren Tingkat Pengangguran Terbuka (TPT)**")
        if not df_makro.empty:
            df_trend = df_makro[df_makro['Status'] == 'Pengangguran'].sort_values(['Tahun', 'Bulan'])
            df_trend['Waktu'] = df_trend['Tahun'].astype(str) + " - " + df_trend['Bulan']
            
            peak_covid = df_trend[df_trend['Tahun'] == 2020]['Persentase'].max()
            peak_label = df_trend[df_trend['Persentase'] == peak_covid]['Waktu'].values[0]

            fig_trend = px.line(df_trend, x='Waktu', y='Persentase', markers=True)
            fig_trend.update_traces(line_color='#FF4B4B', line_width=3, marker_size=8)
            
            # Anotasi & Garis Referensi
            fig_trend.add_annotation(
                x=peak_label, y=peak_covid, text="Puncak COVID-19",
                showarrow=True, arrowhead=2, ax=0, ay=-30,
                bgcolor="#ffdede", bordercolor="red"
            )
            fig_trend.add_vline(x=f"{filter_tahun_makro} - Agustus", line_width=1, line_dash="dash", line_color="grey")
            fig_trend.update_layout(height=350, margin=dict(l=20, r=20, t=10, b=10))
            st.plotly_chart(fig_trend, use_container_width=True)

    # --- KOLOM 2: DISTRIBUSI UMUR ---
    with col_age:
        # Filter khusus untuk chart umur diletakkan di dalam kolomnya agar rapi
        c_age_head, c_age_filt = st.columns([2, 1])
        with c_age_head:
            st.markdown(f"**Distribusi Umur**")
        with c_age_filt:
            opts_tahun = sorted(df_umur['Tahun_Real'].dropna().unique(), reverse=True) if not df_umur.empty else [2023]
            filter_tahun_demo = st.selectbox("Tahun:", opts_tahun, key="sel_demo_age")

        if not df_umur.empty:
            df_age = df_umur[(df_umur['Tahun_Real'] == filter_tahun_demo) & (df_umur['Kelompok Umur'] != 'Rata-Rata')].copy()
            if not df_age.empty:
                max_val = df_age['TPT'].max()
                colors = ['#FF4B4B' if x == max_val else '#FFB3B3' for x in df_age['TPT']]
                
                fig_age = px.bar(df_age, x='Kelompok Umur', y='TPT', 
                                 text_auto='.1f', title=f"TPT per Umur ({filter_tahun_demo})")
                fig_age.update_traces(marker_color=colors, textposition='outside')
                fig_age.update_layout(height=350, margin=dict(l=0,r=0,t=30,b=0), xaxis_title=None)
                st.plotly_chart(fig_age, use_container_width=True)


# ==========================================
# BARIS 3: SISA INFORMASI (PENDIDIKAN & SEKTOR)
# ==========================================
with st.container(border=True):
    st.subheader("💰 Analisis Upah: Pendidikan & Sektoral")
    
    col_edu, col_sect = st.columns(2)

    # --- KOLOM 1: GAP PENDIDIKAN ---
    with col_edu:
        st.markdown("**Gap Upah Berdasarkan Pendidikan**")
        
        # Filter Pendidikan
        edu_labels = {'Tidak_Sekolah': '🚫 Tidak Sekolah', 'SD': '🎒 SD', 'SMP': '📘 SMP', 'SMA_Keatas': '🎓 SMA+'}
        ce1, ce2 = st.columns(2)
        with ce1:
            edu_1 = st.selectbox("Dasar:", list(edu_labels.keys()), index=1, format_func=lambda x: edu_labels[x], key="e1")
        with ce2:
            edu_2 = st.selectbox("Banding:", list(edu_labels.keys()), index=3, format_func=lambda x: edu_labels[x], key="e2")

        if not df_pendidikan.empty:
            # Gunakan tahun dari filter demografi di atas atau default 2023
            df_edu = df_pendidikan[df_pendidikan['Tahun'] == filter_tahun_demo].copy()
            
            # Multiselect Provinsi (dimasukkan dalam expander agar hemat tempat)
            with st.expander("🔎 Filter Provinsi", expanded=False):
                all_provs = sorted(df_edu['Provinsi'].unique().tolist())
                sel_provs = st.multiselect("Pilih:", all_provs, default=all_provs[:10], key="ms_prov") # Default top 10 agar grafik tidak penuh
            
            if not df_edu.empty:
                target_provs = sel_provs if sel_provs else all_provs
                df_viz = df_edu[df_edu['Provinsi'].isin(target_provs)].copy()
                df_viz['Gap'] = df_viz[edu_2] - df_viz[edu_1]
                df_viz = df_viz.sort_values('Gap')

                fig_gap = go.Figure()
                # Garis
                for i in range(len(df_viz)):
                    fig_gap.add_shape(type='line',
                                    x0=df_viz.iloc[i][edu_1], y0=df_viz.iloc[i]['Provinsi'],
                                    x1=df_viz.iloc[i][edu_2], y1=df_viz.iloc[i]['Provinsi'],
                                    line=dict(color='lightgrey', width=2))
                # Marker
                fig_gap.add_trace(go.Scatter(x=df_viz[edu_1], y=df_viz['Provinsi'], mode='markers', name=edu_labels[edu_1], marker=dict(color='#FFA500', size=8)))
                fig_gap.add_trace(go.Scatter(x=df_viz[edu_2], y=df_viz['Provinsi'], mode='markers', name=edu_labels[edu_2], marker=dict(color='#000080', size=8)))
                
                # Tinggi dinamis berdasarkan jumlah data
                h_dynamic = max(350, len(df_viz) * 25)
                fig_gap.update_layout(height=h_dynamic, margin=dict(l=0,r=0,t=10,b=0), legend=dict(orientation="h", y=1.1))
                st.plotly_chart(fig_gap, use_container_width=True)

    # --- KOLOM 2: ANALISIS SEKTORAL ---
    with col_sect:
        c_sec_head, c_sec_filt = st.columns([2, 1])
        with c_sec_head:
            st.markdown("**Komparasi Upah Sektoral**")
        with c_sec_filt:
            prov_list = sorted(df_lapangan['Provinsi'].unique()) if not df_lapangan.empty else []
            filter_prov = st.selectbox("Wilayah:", ["Nasional (Top 10)"] + prov_list, key="sel_prov_sect")

        if not df_lapangan.empty:
            df_sect = df_lapangan[df_lapangan['Tahun'] == 2023] # Data Terbaru

            if filter_prov == "Nasional (Top 10)":
                df_show = df_sect.sort_values('Industri', ascending=False).head(10)
                fig_sect = px.bar(df_show, x='Industri', y='Provinsi', orientation='h', 
                                 title="Top 10 Prov (Sektor Industri)", color='Industri', color_continuous_scale='Viridis')
                fig_sect.update_layout(yaxis=dict(autorange="reversed"))
            else:
                df_prov_only = df_sect[df_sect['Provinsi'] == filter_prov]
                df_melt = df_prov_only.melt(id_vars=['Provinsi'], value_vars=['Pertanian', 'Industri', 'Jasa'], 
                                     var_name='Sektor', value_name='Upah')
                
                fig_sect = px.bar(df_melt, x='Sektor', y='Upah', color='Sektor', 
                                 title=f"Upah di {filter_prov}", text_auto='.2s',
                                 color_discrete_sequence=px.colors.qualitative.Pastel)
            
            fig_sect.update_layout(height=400, margin=dict(l=0,r=0,t=40,b=0))
            st.plotly_chart(fig_sect, use_container_width=True)