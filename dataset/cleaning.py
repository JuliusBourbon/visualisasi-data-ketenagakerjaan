import pandas as pd
import glob
import os

def clean_pendapatan_files(file_pattern, output_filename):

    all_files = sorted(glob.glob(file_pattern)) # Contoh: "Pendapatan_*.csv"
    combined_data = []

    for file in all_files:
        # Asumsi: Nama file mengandung tahun, misal "Pendapatan_2023.csv"
        # Jika tidak, kita harus manual menambahkan kolom tahun
        try:
            # Baca file
            df = pd.read_csv(file)
            
            # Ambil tahun dari nama file (opsional, sesuaikan logika ini)
            # Contoh sederhana: jika nama file "Data_2023.csv", ambil "2023"
            year = "".join(filter(str.isdigit, file))[-4:] 
            df['Tahun'] = year
            
            combined_data.append(df)
        except Exception as e:
            print(f"Gagal memproses {file}: {e}")

    if combined_data:
        df_final = pd.concat(combined_data, ignore_index=True)
        # Standarisasi nama kolom jika perlu
        df_final.columns = df_final.columns.str.replace(r"\s+\(Rp\)", "", regex=True) # Hapus satuan (Rp) di header
        df_final.to_csv(output_filename, index=False)
        print(f"Berhasil menyimpan: {output_filename}")
    else:
        print("Tidak ada file ditemukan!")

# CONTOH PENGGUNAAN (Sesuaikan nama file kamu):
clean_pendapatan_files("RataRataLapangan*.csv", "clean_RataRataLapangan.csv")
clean_pendapatan_files("RataRataPendidikan*.csv", "clean_RataRataPendidikan.csv")


# ==========================================
# 2. CLEANING PENGANGGURAN PER UMUR
# ==========================================
def clean_pengangguran_umur(filename):
    # Baca tanpa header dulu untuk inspeksi
    df_raw = pd.read_csv(filename, header=None)
    
    # Baris ke-2 (index 2) biasanya berisi Tahun (2023, dst)
    # Baris ke-3 dst adalah data
    
    # Ambil baris tahun
    years = df_raw.iloc[2, 1:].ffill().values # Isi NaN dengan tahun sebelumnya jika merged cell
    
    # Ambil data utama
    df_data = df_raw.iloc[3:].copy()
    df_data.columns = ['Kelompok Umur'] + list(years)
    
    # Ubah dari Wide (Tahun ke samping) ke Long (Tahun ke bawah)
    df_melted = df_data.melt(id_vars=['Kelompok Umur'], var_name='Tahun', value_name='TPT')
    
    # Simpan
    df_melted.to_csv('clean_kelompokUmurPengangguran.csv', index=False)
    print("Berhasil menyimpan: clean_kelompokUmurPengangguran.csv")

clean_pengangguran_umur("kelompokUmurPengangguran.csv")


# ==========================================
# 3. CLEANING JUMLAH & PERSENTASE (COMPLEX)
# ==========================================
def clean_jumlah_pengangguran(filename):
    df_raw = pd.read_csv(filename, header=None)

    # Konstruksi Header Manual dari Baris 2, 3, 4
    header_kategori = df_raw.iloc[2, 1:].ffill() # Penduduk Bekerja / Pengangguran
    header_tahun = df_raw.iloc[3, 1:].ffill()    # 2023, dst
    header_periode = df_raw.iloc[4, 1:].ffill()  # Februari, Agustus, Tahunan

    # Buat MultiIndex untuk kolom
    cols = pd.MultiIndex.from_arrays([header_kategori, header_tahun, header_periode], 
                                     names=['Status', 'Tahun', 'Periode'])

    # Ambil data (Baris 5 dan 6)
    df_data = df_raw.iloc[5:].copy()
    df_data.index = df_raw.iloc[5:, 0] # Index jadi "Persentase" & "Jumlah"
    df_data = df_data.drop(columns=[0])
    df_data.columns = cols

    # Transpose agar Tahun & Status jadi baris (Tidy Data)
    df_tidy = df_data.T.reset_index()
    
    # Rapikan nama kolom
    df_tidy.rename(columns={'Persentase (%)': 'Persentase', 'Jumlah (Ribu orang)': 'Jumlah_Orang'}, inplace=True)
    
    # Simpan
    df_tidy.to_csv('clean_persentaseBekerjaPengangguran.csv', index=False)
    print("Berhasil menyimpan: clean_persentaseBekerjaPengangguran.csv")

clean_jumlah_pengangguran("persentaseBekerjaPengangguran.csv")