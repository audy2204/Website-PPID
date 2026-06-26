# Website-PPID
Proyek ini dibuat untuk memenuhi tugas akhir semester 6 magang di dinas pendidikan kota surabaya 

├── .streamlit/
│   └── secrets.toml          # Kredensial rahasia Google Sheets API 
├── data/
│   ├── DATA PENGADUAN.xlsx   # Dataset tahun 2025
│   └── DATA ASPIRASI.xlsx
│   └── DATA PERMOHONAN INFORMASI.xlsx
├── assets/
│   └── bg.jpg                # Gambar latar belakang 
├── app.py                    # File utama aplikasi (Konfigurasi halaman & routing antarmuka)
├── data_handler.py           # Logika penarikan, standardisasi kapitalisasi, & manipulasi data Pandas
├── form_input.py             # Form registrasi laporan publik & survei kepuasan pengguna
├── visualisasi.py            # Rendering grafik interaktif Plotly di dalam container glassmorphic
├── requirements.txt          # Daftar dependensi modul Python
└── README.md                 # Dokumentasi proyek
