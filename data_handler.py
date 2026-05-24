import pandas as pd
import os
import gspread
import streamlit as st
from google.oauth2.service_account import Credentials
import datetime

def get_gsheet_client():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    
    # Membaca kredensial langsung dari Streamlit Secrets (Format TOML)
    secret_credentials = st.secrets["gcp_service_account"]
    creds = Credentials.from_service_account_info(secret_credentials, scopes=scope)
    return gspread.authorize(creds)

def save_to_google_sheets(data, kategory):
    # Menyimpan data ke Google Sheets berdasarkan kategori ke tab yang berbeda.
    SPREADSHEET_ID = "1zkLC0xu87g1R_Er-wu9qnLMkiJJvn9NlPIN06-zySf0"
    
    try:
        client = get_gsheet_client()
        sh = client.open_by_key(SPREADSHEET_ID)
        
        # Pilih nama sheet (Pengaduan / Aspirasi / Permohonan Informasi)
        nama_sheet = kategory 
        
        # Cari worksheet, jika tidak ada maka buat baru
        try:
            worksheet = sh.worksheet(nama_sheet)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = sh.add_worksheet(title=nama_sheet, rows="1000", cols="20")
            # Menambahkan header otomatis berdasarkan kunci dari dictionary data
            worksheet.append_row(list(data.keys()))

        # KIRIM DATA
        values = list(data.values())
        worksheet.append_row(values)
        
        print(f"✅ Data berhasil disimpan ke Tab: {nama_sheet}")
        return True

    except Exception as e:
        print(f"❌ Gagal menyimpan ke Google Sheets: {e}")
        return False

# 🌟 2. FUNGSI UNTUK MEMBACA & MENGGABUNG DATA LANGSUNG DARI GOOGLE SHEETS
def load_all_data():
    SPREADSHEET_ID = "1zkLC0xu87g1R_Er-wu9qnLMkiJJvn9NlPIN06-zySf0"
    tabs = ['Pengaduan', 'Aspirasi', 'Permohonan Informasi']
    
    all_dfs = []
    
    try:
        client = get_gsheet_client()
        sh = client.open_by_key(SPREADSHEET_ID)
        
# ... (kode bagian atas tetap sama) ...

        for tipe in tabs:
            try:
                worksheet = sh.worksheet(tipe)
                records = worksheet.get_all_records()
                
                if not records:
                    continue
                    
                df_temp = pd.DataFrame(records)
                
                # --- PROSES CLEANING DATA ---
                
                # 1. Penyeragaman Kolom bawaan Sheet ke Huruf Kapital Besar
                df_temp.columns = [col.upper() for col in df_temp.columns]
                
                # Tambahkan kolom 'Tipe' di sini setelah fungsi UPPER agar tidak ikut berubah jadi kapital semua
                df_temp['Tipe'] = tipe
                
                if 'WILAYAH' in df_temp.columns:
                    df_temp = df_temp.rename(columns={'WILAYAH': 'Wilayah'})
                
                # 2. Perhitungan Waktu Respon Default
                df_temp['WAKTU RESPON'] = 10 

                # 3. Survey Kepuasan
                if 'KEPUASAN PELANGGAN' in df_temp.columns:
                    df_temp['SURVEY KEPUASAN'] = df_temp['KEPUASAN PELANGGAN'].apply(
                        lambda x: 100.0 if x == "Sangat Puas" else (80.0 if x == "Puas" else 60.0)
                    )
                else:
                    df_temp['SURVEY KEPUASAN'] = 87.9
                
                # 4. Penyeragaman Tanggal & Filter Tahun
                if 'TANGGAL INPUT' in df_temp.columns:
                    df_temp['TANGGAL INPUT'] = pd.to_datetime(df_temp['TANGGAL INPUT'], errors='coerce')
                    df_temp = df_temp.dropna(subset=['TANGGAL INPUT'])
                    df_temp['Bulan'] = df_temp['TANGGAL INPUT'].dt.month_name()
                    df_temp['Tahun'] = df_temp['TANGGAL INPUT'].dt.year
                else:
                    df_temp['Bulan'] = 'January'
                    df_temp['Tahun'] = 2026

                # PERBAIKAN: Gunakan 'JENIS KELAMIN' agar cocok dengan visualisasi.py
                if 'JENIS KELAMIN' not in df_temp.columns:
                    df_temp['JENIS KELAMIN'] = 'Laki-laki'

                all_dfs.append(df_temp)
                
            except gspread.exceptions.WorksheetNotFound:
                continue
            except Exception as e:
                print(f"Error membaca tab {tipe}: {e}")
                
# ... (kode bagian bawah tetap sama) ...
                
    except Exception as e:
        print(f"Gagal koneksi ke Google Sheets saat memuat data: {e}")
        return None
        
    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True)
    return pd.DataFrame()
