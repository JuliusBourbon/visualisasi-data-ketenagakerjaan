import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

icon_barchart = """
<svg width="48" height="48" viewBox="0 0 94 120" fill="#FF4E4C" xmlns="http://www.w3.org/2000/svg" stroke-width="1px" stroke-linecap="round" stroke-linejoin="round"><path d="M90.3318 73.3397L90.1218 73.2397C89.5018 72.9797 88.7518 73.1098 87.8718 73.6198L25.7117 109.51C24.7417 110.07 23.9217 110.92 23.2517 112.07C22.5917 113.21 22.2617 114.34 22.2617 115.46C22.2617 116.58 22.5917 117.33 23.2517 117.71C23.9217 118.09 24.7417 118 25.7117 117.43L87.8718 81.5397C88.8518 80.9797 89.6718 80.1297 90.3318 78.9797C91.0018 77.8397 91.3318 76.7097 91.3318 75.5897C91.3318 74.4697 91.0018 73.7097 90.3318 73.3397Z" stroke="#0B0B0F" stroke-linejoin="round"/><path d="M87.8718 16.1598V63.7099C87.8718 65.3599 87.3718 67.0598 86.3618 68.7898C85.9518 69.4998 85.5117 70.1299 85.0317 70.6899C84.3217 71.4999 83.5419 72.1598 82.6919 72.6498C81.2519 73.4798 80.0317 73.6098 79.0217 73.0298C78.0217 72.4598 77.5117 71.3399 77.5117 69.6899V22.1399C77.5117 20.4899 78.0217 18.7999 79.0217 17.0599C80.0317 15.3199 81.2519 14.0399 82.6919 13.2099C83.9819 12.4599 85.1118 12.2798 86.0518 12.6698L86.3618 12.8199C87.3718 13.3999 87.8718 14.5098 87.8718 16.1598Z" stroke="#0B0B0F" stroke-linejoin="round"/><path d="M90.1218 73.2399C89.5018 72.9799 88.7518 73.1099 87.8718 73.6199L25.7117 109.51C24.7417 110.07 23.9217 110.92 23.2517 112.07C22.5917 113.21 22.2617 114.34 22.2617 115.46C22.2617 116.58 22.5917 117.33 23.2517 117.71L3.46167 107.81L3.25171 107.71C2.59171 107.33 2.26172 106.58 2.26172 105.46C2.26172 104.34 2.59171 103.21 3.25171 102.07C3.92171 100.92 4.74167 100.07 5.71167 99.5099L12.5117 95.5798L19.8618 99.2599L27.2317 102.94C28.2317 103.51 29.4618 103.38 30.8918 102.55C32.3318 101.72 33.5618 100.44 34.5618 98.6998C35.5718 96.9598 36.0718 95.2699 36.0718 93.6199V88.7599L37.1318 89.2898L44.4917 92.9698C45.5017 93.5398 46.7219 93.4098 48.1619 92.5798C49.6019 91.7498 50.8218 90.4699 51.8318 88.7299C52.8418 86.9899 53.3418 85.2998 53.3418 83.6498V78.7898L54.4019 79.3198L61.7617 82.9999C62.7717 83.5699 63.9919 83.4499 65.4319 82.6199C66.8719 81.7799 68.0918 80.4999 69.1018 78.7599C70.1018 77.0299 70.6118 75.3298 70.6118 73.6798V68.8298L79.0217 73.0298C80.0317 73.6098 81.2519 73.4798 82.6919 72.6498C83.5419 72.1598 84.3217 71.4998 85.0317 70.6898L90.1218 73.2399Z" stroke="#0B0B0F" stroke-linejoin="round"/><path d="M70.6121 49.8997V73.6797C70.6121 75.3297 70.1021 77.0298 69.1021 78.7598C68.0921 80.4998 66.8721 81.7798 65.4321 82.6198C63.9921 83.4498 62.772 83.5698 61.762 82.9998C60.752 82.4298 60.252 81.3097 60.252 79.6597V55.8898C60.252 54.2398 60.752 52.5397 61.762 50.7997C62.772 49.0697 63.9921 47.7798 65.4321 46.9498C66.3321 46.4298 67.1421 46.1898 67.8721 46.2198C68.1821 46.2298 68.482 46.2897 68.762 46.3997L69.1021 46.5698C70.1021 47.1398 70.6121 48.2497 70.6121 49.8997Z" stroke="#0B0B0F" stroke-linejoin="round"/><path d="M86.0518 12.6698C85.1118 12.2798 83.9819 12.4598 82.6919 13.2098C81.2519 14.0398 80.0317 15.3198 79.0217 17.0598C78.0217 18.7998 77.5117 20.4899 77.5117 22.1399V69.6898C77.5117 71.3398 78.0217 72.4597 79.0217 73.0297L70.6118 68.8298V49.8997C70.6118 48.2497 70.1018 47.1398 69.1018 46.5698L68.7617 46.3997L67.8718 45.9598L57.5117 40.7797V12.1398C57.5117 10.4898 58.0217 8.79977 59.0217 7.05977C60.0317 5.31977 61.2519 4.0398 62.6919 3.2098C64.1319 2.3798 65.3618 2.24978 66.3618 2.81978L86.0518 12.6698Z" stroke="#0B0B0F" stroke-linejoin="round"/><path d="M53.3425 47.9899V83.6498C53.3425 85.2998 52.8425 86.9899 51.8325 88.7299C50.8225 90.4699 49.6026 91.7498 48.1626 92.5798C46.7226 93.4098 45.5024 93.5398 44.4924 92.9698C43.4824 92.3898 42.9824 91.2799 42.9824 89.6299V53.9698C42.9824 52.3198 43.4824 50.6199 44.4924 48.8799C45.5024 47.1499 46.7226 45.8598 48.1626 45.0298C49.0626 44.5098 49.8825 44.2598 50.6125 44.2998C50.9325 44.3098 51.2325 44.3699 51.5125 44.4899L51.8325 44.6498C52.8425 45.2198 53.3425 46.3299 53.3425 47.9899Z" stroke="#0B0B0F" stroke-linejoin="round"/><path d="M36.071 77.7698V93.6198C36.071 95.2698 35.571 96.9597 34.561 98.6997C33.561 100.44 32.3311 101.72 30.8911 102.55C29.4611 103.38 28.231 103.51 27.231 102.94C26.221 102.36 25.7109 101.25 25.7109 99.5997V83.7498C25.7109 83.6898 25.7109 83.6397 25.7209 83.5797C25.7109 83.4897 25.7209 83.3997 25.7209 83.3097C25.8009 81.7997 26.311 80.2497 27.231 78.6697C28.231 76.9297 29.4611 75.6497 30.8911 74.8097C31.7911 74.2897 32.6011 74.0497 33.3311 74.0897C33.6511 74.0997 33.961 74.1597 34.251 74.2797L34.561 74.4297C35.571 74.9997 36.071 76.1198 36.071 77.7698Z" stroke="#0B0B0F" stroke-linejoin="round"/><path d="M68.7617 46.3999C68.4817 46.2899 68.1818 46.2299 67.8718 46.2199C67.1418 46.1899 66.3319 46.4299 65.4319 46.9499C63.9919 47.7799 62.7717 49.0699 61.7617 50.7999C60.7517 52.5399 60.2517 54.24 60.2517 55.89V79.6599C60.2517 81.3099 60.7517 82.43 61.7617 83L54.4019 79.3199L53.3418 78.7899V47.9899C53.3418 46.3299 52.8418 45.2199 51.8318 44.6499L51.5117 44.4899L50.6118 44.0399L42.3418 39.8999C43.2218 38.6199 44.2519 37.6299 45.4319 36.9499C46.8719 36.1199 48.0918 35.9899 49.1018 36.5699L57.5117 40.7799L67.8718 45.9599L68.7617 46.3999Z" stroke="#0B0B0F" stroke-linejoin="round"/><path d="M51.5125 44.4898C51.2325 44.3698 50.9325 44.3098 50.6125 44.2998C49.8825 44.2598 49.0626 44.5097 48.1626 45.0297C46.7226 45.8597 45.5024 47.1498 44.4924 48.8798C43.4824 50.6198 42.9824 52.3198 42.9824 53.9698V89.6298C42.9824 91.2798 43.4824 92.3898 44.4924 92.9698L37.1326 89.2897L36.0725 88.7598V77.7699C36.0725 76.1199 35.5725 74.9998 34.5625 74.4298L34.2524 74.2797L33.3325 73.8198L22.9824 68.6398V43.9698C22.9824 42.3198 23.4824 40.6198 24.4924 38.8798C25.5024 37.1498 26.7226 35.8597 28.1626 35.0297C29.6026 34.1997 30.8225 34.0697 31.8325 34.6497L42.3425 39.8997L50.6125 44.0398L51.5125 44.4898Z" stroke="#0B0B0F" stroke-linejoin="round"/><path d="M34.251 74.2799C33.961 74.1599 33.6511 74.0999 33.3311 74.0899C32.6011 74.0499 31.7911 74.2899 30.8911 74.8099C29.4611 75.6499 28.231 76.9299 27.231 78.6699C26.311 80.2499 25.8009 81.7999 25.7209 83.3099C25.7209 83.3999 25.7109 83.4899 25.7209 83.5799C25.7109 83.6399 25.7109 83.6899 25.7109 83.7499V99.5999C25.7109 101.25 26.221 102.36 27.231 102.94L19.8611 99.26L12.511 95.5799L7.54102 93.0899L7.23096 92.9399C6.22096 92.3599 5.71094 91.2499 5.71094 89.5999V73.7499C5.71094 72.0999 6.22096 70.3999 7.23096 68.6699C8.23096 66.9299 9.46111 65.6499 10.8911 64.8099C12.3311 63.9799 13.561 63.8599 14.561 64.4299L22.981 68.64L33.3311 73.8199L34.251 74.2799Z" stroke="#0B0B0F" stroke-linejoin="round"/></svg>
"""

st.set_page_config(
    page_title="Dashboard Ketenagakerjaan Indonesia",
    page_icon= icon_barchart,
    layout="wide",

)

st.title("Dashboard Ketenagakerjaan Indonesia (2018-2023)")
st.markdown("Mengungkap dinamika pengangguran, kesenjangan pendapatan, dan dampak pandemi melalui Data Storytelling.")

@st.cache_data
def load_data():
    try:
        df_makro = pd.read_csv("clean_persentaseBekerjaPengangguran.csv")
        df_makro = df_makro.rename(columns={'Status': 'Tahun', 'Tahun': 'Bulan', 'Periode': 'Persentase', 'Jumlah_Orang': 'Jumlah'})
        df_makro['Persentase'] = pd.to_numeric(df_makro['Persentase'], errors='coerce')
        df_makro['Status'] = df_makro['Persentase'].apply(lambda x: 'Bekerja' if x > 50 else 'Pengangguran')
        df_makro = df_makro[df_makro['Bulan'] != 'Tahunan']
    except:
        df_makro = pd.DataFrame()

    try:
        df_umur = pd.read_csv("clean_kelompokUmurPengangguran.csv")
        unique_vals = df_umur['Tahun'].unique()
        mapping_tahun = {val: 2018 + i for i, val in enumerate(unique_vals)} 
        df_umur['Tahun_Real'] = df_umur['Tahun'].map(mapping_tahun)
    except:
        df_umur = pd.DataFrame()

    try:
        df_lapangan = pd.read_csv("clean_RataRataLapangan.csv")
        df_lapangan.columns = ['Provinsi', 'Pertanian', 'Industri', 'Jasa', 'Total', 'Tahun']
        cols_num = ['Pertanian', 'Industri', 'Jasa', 'Total']
        for col in cols_num:
            df_lapangan[col] = pd.to_numeric(df_lapangan[col], errors='coerce')
        
        df_lapangan = df_lapangan.dropna(subset=['Total', 'Pertanian', 'Industri'])
    except:
        df_lapangan = pd.DataFrame()

    try:
        df_pendidikan = pd.read_csv("clean_RataRataPendidikan.csv")
        df_pendidikan.columns = ['Provinsi', 'Tidak_Sekolah', 'SD', 'SMP', 'SMA_Keatas', 'Total', 'Tahun']
        for col in ['Tidak_Sekolah', 'SD', 'SMP', 'SMA_Keatas', 'Total']:
            df_pendidikan[col] = pd.to_numeric(df_pendidikan[col], errors='coerce')
        df_pendidikan = df_pendidikan.dropna(subset=['SD', 'SMA_Keatas'])
    except:
        df_pendidikan = pd.DataFrame()

    return df_makro, df_umur, df_lapangan, df_pendidikan

df_makro, df_umur, df_lapangan, df_pendidikan = load_data()

tabs = st.tabs([
    "1. Tren Makro", 
    "2. Demografi Umur", 
    "3. Peta Upah", 
    "4. Jebakan Pendidikan", 
    "5. Disparitas Wilayah", 
    "6. Ketahanan Generasi", 
    "7. Dominasi Ekonomi", 
    "8. Pola Musiman"
])

with tabs[0]:
    st.header("Tren Tingkat Pengangguran Terbuka (TPT)")
    if not df_makro.empty:
        df_tpt = df_makro[df_makro['Status'] == 'Pengangguran'].sort_values(['Tahun', 'Bulan'])
        df_tpt['Waktu'] = df_tpt['Tahun'].astype(str) + " - " + df_tpt['Bulan']
        
        fig = px.line(df_tpt, x='Waktu', y='Persentase', markers=True, 
                      title='Pergerakan TPT Nasional (2018-2023)', template='plotly_white')
        fig.update_traces(line_color='#FF4B4B', line_width=3)
        st.plotly_chart(fig, use_container_width=True)
        st.info("Grafik ini menunjukkan dampak langsung pandemi COVID-19 pada tahun 2020 dan proses pemulihan ekonomi setelahnya.")

with tabs[1]:
    st.header("Distribusi Pengangguran per Kelompok Umur")
    if not df_umur.empty:
        tahun_pilih = st.selectbox("Pilih Tahun:", sorted(df_umur['Tahun_Real'].unique()), key='umur_box')
        df_filt = df_umur[(df_umur['Tahun_Real'] == tahun_pilih) & (df_umur['Kelompok Umur'] != 'Rata-Rata')]
        
        fig = px.bar(df_filt, x='Kelompok Umur', y='TPT', color='TPT', 
                     title=f'TPT Berdasarkan Umur ({tahun_pilih})', color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    st.header("Peta Sebaran Upah Pekerja Informal")
    st.caption("Visualisasi ini menyoroti provinsi dengan tingkat kesejahteraan tertinggi dan terendah.")
    if not df_lapangan.empty:
        col1, col2 = st.columns([1, 3])
        with col1:
            tahun_map = st.selectbox("Tahun:", sorted(df_lapangan['Tahun'].unique()), index=len(df_lapangan['Tahun'].unique())-1, key='map_tahun')
            sektor_map = st.radio("Sektor:", ['Total', 'Pertanian', 'Industri'], key='map_sektor')
        
        with col2:
            df_map = df_lapangan[df_lapangan['Tahun'] == tahun_map]
            fig = px.bar(df_map.sort_values(sektor_map), x=sektor_map, y='Provinsi', orientation='h',
                         title=f'Peringkat Upah Sektor {sektor_map} ({tahun_map})', height=800,
                         color=sektor_map, color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)

with tabs[3]:
    st.header("Analisis 'Education Trap' di Sektor Informal")
    st.markdown("**Pertanyaan Strategis:** Apakah sekolah tinggi menjamin gaji tinggi di sektor informal?")
    
    if not df_pendidikan.empty:
        tahun_edu = st.selectbox("Pilih Tahun Data:", sorted(df_pendidikan['Tahun'].unique()), key='edu_tahun')
        df_edu = df_pendidikan[df_pendidikan['Tahun'] == tahun_edu].copy()
        
        df_edu['Gap_SMA_SD'] = df_edu['SMA_Keatas'] - df_edu['SD']
        df_edu = df_edu.sort_values('Gap_SMA_SD')

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_edu['SD'], y=df_edu['Provinsi'], mode='markers', 
                                 name='Lulusan SD', marker=dict(color='red', size=8)))
        fig.add_trace(go.Scatter(x=df_edu['SMA_Keatas'], y=df_edu['Provinsi'], mode='markers', 
                                 name='Lulusan SMA+', marker=dict(color='blue', size=8)))
        for i in range(len(df_edu)):
            fig.add_shape(type='line',
                          x0=df_edu.iloc[i]['SD'], y0=df_edu.iloc[i]['Provinsi'],
                          x1=df_edu.iloc[i]['SMA_Keatas'], y1=df_edu.iloc[i]['Provinsi'],
                          line=dict(color='gray', width=1))
        
        fig.update_layout(title=f"Gap Gaji: Lulusan SD vs SMA+ ({tahun_edu})", 
                          xaxis_title="Rata-rata Pendapatan (Rp)", height=800)
        st.plotly_chart(fig, use_container_width=True)
        
        st.warning(f"**Insight:** Perhatikan provinsi dengan garis pendek. Di sana, ijazah SMA hampir tidak memberikan keuntungan finansial dibanding SD di sektor informal.")

with tabs[4]:
    st.header("Evolusi Ketimpangan Upah Antar Provinsi")
    st.markdown("**Pertanyaan Strategis:** Apakah jurang antara provinsi kaya dan miskin semakin melebar?")
    
    if not df_lapangan.empty:
        disparitas = df_lapangan.groupby('Tahun')['Total'].agg(['min', 'max', 'mean']).reset_index()
        disparitas['Gap'] = disparitas['max'] - disparitas['min']
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=disparitas['Tahun'], y=disparitas['max'], name='Provinsi Tertinggi', line=dict(color='green')))
        fig.add_trace(go.Scatter(x=disparitas['Tahun'], y=disparitas['mean'], name='Rata-rata Nasional', line=dict(color='orange', dash='dash')))
        fig.add_trace(go.Scatter(x=disparitas['Tahun'], y=disparitas['min'], name='Provinsi Terendah', line=dict(color='red')))
        fig.add_trace(go.Bar(x=disparitas['Tahun'], y=disparitas['Gap'], name='Gap (Selisih)', opacity=0.3, yaxis='y2'))

        fig.update_layout(
            title="Tren Kesenjangan Upah (Tertinggi vs Terendah)",
            yaxis=dict(title="Pendapatan (Rp)"),
            yaxis2=dict(title="Besar Gap (Rp)", overlaying='y', side='right'),
            legend=dict(orientation="h")
        )
        st.plotly_chart(fig, use_container_width=True)

with tabs[5]:
    st.header("Siapa yang Paling Rentan Saat Krisis?")
    st.markdown("**Fokus:** Membandingkan dampak pandemi (2019 vs 2020) antar generasi.")
    
    if not df_umur.empty:
        df_gen = df_umur[df_umur['Kelompok Umur'] != 'Rata-Rata']
        
        fig = px.line(df_gen, x='Tahun_Real', y='TPT', color='Kelompok Umur', markers=True,
                      title="Tren Pengangguran per Kelompok Umur (Multi-Series)",
                      labels={'TPT': 'Tingkat Pengangguran (%)'})
        
        fig.add_vrect(x0=2019.5, x1=2020.5, annotation_text="Dampak COVID-19", 
                      annotation_position="top left", fillcolor="red", opacity=0.1, line_width=0)
        
        st.plotly_chart(fig, use_container_width=True)
        st.info("Perhatikan garis kelompok umur 15-24 tahun. Lonjakannya biasanya paling tajam saat krisis, menunjukkan kerentanan tenaga kerja muda.")

with tabs[6]:
    st.header("Peta Kuadran Ekonomi: Pertanian vs Industri")
    st.markdown("Analisis untuk melihat pergeseran struktur ekonomi daerah.")
    
    if not df_lapangan.empty:
        tahun_dom = st.slider("Geser Tahun:", 2018, 2023, 2023, key='dom_slider_baru')
        
        df_scat = df_lapangan[df_lapangan['Tahun'] == tahun_dom].copy()
        df_scat = df_scat.dropna(subset=['Pertanian', 'Industri', 'Total'])
        
        if not df_scat.empty:
            fig = px.scatter(df_scat, x='Pertanian', y='Industri', hover_name='Provinsi',
                             size='Total', color='Total', 
                             title=f"Korelasi Upah: Pertanian vs Industri ({tahun_dom})",
                             labels={'Pertanian': 'Upah Sektor Pertanian (Rp)', 'Industri': 'Upah Sektor Industri (Rp)'})
            
            fig.add_shape(type="line", x0=0, y0=0, x1=4000000, y1=4000000, line=dict(color="grey", dash="dash"))
            
            st.plotly_chart(fig, use_container_width=True)
            st.caption("**Cara Baca:** Titik di atas garis putus-putus berarti provinsi tersebut memberikan upah Industri lebih tinggi dibanding Pertanian (Potensi Urbanisasi Tinggi).")
        else:
            st.warning(f"Data lengkap untuk tahun {tahun_dom} tidak tersedia untuk semua provinsi.")
    else:
        st.error("Data Lapangan Usaha gagal dimuat.")
    st.header("Peta Kuadran Ekonomi: Pertanian vs Industri")
    st.markdown("Analisis untuk melihat pergeseran struktur ekonomi daerah.")
    
    if not df_lapangan.empty:
        tahun_dom = st.slider("Geser Tahun:", 2018, 2023, 2023, key='dom_slider')
        df_scat = df_lapangan[df_lapangan['Tahun'] == tahun_dom]
        
        fig = px.scatter(df_scat, x='Pertanian', y='Industri', hover_name='Provinsi',
                         size='Total', color='Total', 
                         title=f"Korelasi Upah: Pertanian vs Industri ({tahun_dom})",
                         labels={'Pertanian': 'Upah Sektor Pertanian (Rp)', 'Industri': 'Upah Sektor Industri (Rp)'})
        
        fig.add_shape(type="line", x0=0, y0=0, x1=4000000, y1=4000000, line=dict(color="grey", dash="dash"))
        
        st.plotly_chart(fig, use_container_width=True, key="chart6")
        st.caption("**Cara Baca:** Titik di atas garis putus-putus berarti provinsi tersebut memberikan upah Industri lebih tinggi dibanding Pertanian (Potensi Urbanisasi Tinggi).")

with tabs[7]:
    st.header("Siklus Tahunan: Februari vs Agustus")
    st.markdown("Menganalisis apakah ada pola musiman (misal: lulusan baru masuk pasar kerja di bulan Agustus).")
    
    if not df_makro.empty:
        df_season = df_makro[df_makro['Status'] == 'Pengangguran']
        
        fig = px.bar(df_season, x='Tahun', y='Persentase', color='Bulan', barmode='group',
                     title="Perbandingan TPT: Februari vs Agustus",
                     labels={'Persentase': 'TPT (%)'})
        st.plotly_chart(fig, use_container_width=True)
        st.success("Jika batang Agustus (biasanya oranye) lebih tinggi dari Februari, itu indikasi masuknya angkatan kerja baru (lulusan sekolah) yang belum terserap.")