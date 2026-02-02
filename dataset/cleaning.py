import pandas as pd
import glob
import os

def clean_pendapatan_files(file_pattern, output_filename):

    all_files = sorted(glob.glob(file_pattern))
    combined_data = []

    for file in all_files:
        try:
            df = pd.read_csv(file)
            
            year = "".join(filter(str.isdigit, file))[-4:] 
            df['Tahun'] = year
            
            combined_data.append(df)
        except Exception as e:
            print(f"Gagal memproses {file}: {e}")

    if combined_data:
        df_final = pd.concat(combined_data, ignore_index=True)
        df_final.columns = df_final.columns.str.replace(r"\s+\(Rp\)", "", regex=True) 
        df_final.to_csv(output_filename, index=False)
        print(f"Berhasil menyimpan: {output_filename}")
    else:
        print("Tidak ada file ditemukan!")

clean_pendapatan_files("RataRataLapangan*.csv", "clean_RataRataLapangan.csv")
clean_pendapatan_files("RataRataPendidikan*.csv", "clean_RataRataPendidikan.csv")


def clean_pengangguran_umur(filename):
    df_raw = pd.read_csv(filename, header=None)
    
    
    years = df_raw.iloc[2, 1:].ffill().values 
    
    df_data = df_raw.iloc[3:].copy()
    df_data.columns = ['Kelompok Umur'] + list(years)
    
    df_melted = df_data.melt(id_vars=['Kelompok Umur'], var_name='Tahun', value_name='TPT')
    
    df_melted.to_csv('clean_kelompokUmurPengangguran.csv', index=False)
    print("Berhasil menyimpan: clean_kelompokUmurPengangguran.csv")

clean_pengangguran_umur("kelompokUmurPengangguran.csv")


def clean_jumlah_pengangguran(filename):
    df_raw = pd.read_csv(filename, header=None)

    header_kategori = df_raw.iloc[2, 1:].ffill() 
    header_tahun = df_raw.iloc[3, 1:].ffill()    
    header_periode = df_raw.iloc[4, 1:].ffill()  

    cols = pd.MultiIndex.from_arrays([header_kategori, header_tahun, header_periode], 
                                     names=['Status', 'Tahun', 'Periode'])

    df_data = df_raw.iloc[5:].copy()
    df_data.index = df_raw.iloc[5:, 0] 
    df_data = df_data.drop(columns=[0])
    df_data.columns = cols

    df_tidy = df_data.T.reset_index()
    
    df_tidy.rename(columns={'Persentase (%)': 'Persentase', 'Jumlah (Ribu orang)': 'Jumlah_Orang'}, inplace=True)
    
    df_tidy.to_csv('clean_persentaseBekerjaPengangguran.csv', index=False)
    print("Berhasil menyimpan: clean_persentaseBekerjaPengangguran.csv")

clean_jumlah_pengangguran("persentaseBekerjaPengangguran.csv")