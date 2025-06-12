# BitQuant Auto-Referral Bot
Bot automasi untuk membuat akun referral baru di platform BitQuant secara massal menggunakan satu akun induk.

## 🌟 Fitur Utama

- **Otomatisasi Penuh**: Membuat akun referral dari awal hingga akhir secara otomatis.
- **Pembuatan Dompet Solana**: Menghasilkan dompet Solana baru untuk setiap akun referral.
- **Alur Referral Lengkap**: Mengikuti seluruh alur referral resmi: meminta kode, mengaktivasi kode, login, dan melakukan interaksi pertama.
- **Dukungan Proxy**: Dapat menggunakan proxy gratis dari ProxyScrape atau proxy pribadi dari file `proxy.txt`.
- **Aktivitas Akun Baru**: Secara otomatis melakukan interaksi pertama untuk setiap akun baru agar referral dianggap sah.
- **Penyimpanan Aman**: Menyimpan *private key* dari akun yang baru dibuat ke dalam `generated_accounts.txt`.

##  Prasyarat

- **Python 3.8** atau versi yang lebih baru.
- **Git** (opsional, untuk kloning repositori).

##  Instalasi & Pengaturan

1.  **Kloning Repositori:**
    ```bash
    git clone https://github.com/dlzvy/bitreff.git
    ---
    cd bitreff
    ```

2.  **Instal Dependensi:**
    Buka terminal atau command prompt di dalam folder proyek dan jalankan:
    ```bash
   pip install -r requirements.txt #or pip3 install -r requirements.txt
    ```

##  Cara Menggunakan

1.  **(Opsional) Siapkan Proxy:** Jika Anda ingin menggunakan proxy pribadi (opsi 2), buat file `proxy.txt` dan isi dengan daftar proxy Anda (format: `ip:port`), satu per baris.

2.  **Jalankan Skrip:**
    ```bash
   python bot.py #or python3 bot.py
    ```

3.  **Ikuti Instruksi:**
    - Skrip akan meminta Anda memasukkan **Private Key Akun Induk**.
    - Kemudian, masukkan **Jumlah akun referral** yang ingin dibuat.
    - Terakhir, pilih **Opsi Proxy** (1, 2, atau 3).

4.  **Selesai:** Skrip akan berjalan secara otomatis. Akun-akun baru yang berhasil dibuat akan disimpan di `generated_accounts.txt`.

## 📁 Struktur File

```
.
├── bot.py                  # Skrip utama
├── requirements.txt        # Daftar dependensi Python
├── proxy.txt               # (Opsional) Tempat menyimpan proxy pribadi Anda
├── generated_accounts.txt  # (Dibuat otomatis) Menyimpan akun hasil generate
└── README.md               # File ini
```

## ⚠️ Peringatan

- Penggunaan bot dan automasi mungkin melanggar Syarat dan Ketentuan layanan BitQuant. Risiko ditanggung oleh pengguna.
- **JANGAN PERNAH** membagikan *private key* akun induk Anda atau isi dari `generated_accounts.txt` kepada siapa pun.
- Skrip ini dibuat untuk tujuan edukasi.
