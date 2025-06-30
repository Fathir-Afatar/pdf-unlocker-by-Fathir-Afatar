# Riwayat Perubahan (CHANGELOG)

Format : [Versi] - Tanggal

## [v1.1] - 2025-06-23

### Ditambahkan

- Antarmuka GUI dasar untuk unlock banyak file PDF secara otomatis
- Input Folder PDF, input file password '.txt', dan folder output hasil untuk unlock
- Proses pengecekan dan pencocokan password terhadap masing-masing file PDF 
- Notifikasi untuk status unlock: berhasil atau gagal
- File README.md, LICENSE (MIT), dan requirements.txt
- Informasi lisensi MIT ditampilkan di dalam proyek

## Uji Performa (Demo)

- Pengujian berhasil terhadap **50 file PDF dengan password yang berbeda**
- 50 file PDF urutannya *sama* dengan urutan password didalam Sample-Password.txt
- Total waktu pemrosesan hanya 14.10 detik
- File dilindungi password valid, dan kontennya berupa teks acak (~19.6MB @404KB file *sebelum* password @39KB)
- Hasil pengujian disiapkan sebagai dokumenasi & demo di folder 'docs/demo-files/'

### [v1.0] - Internal (belum dirilis)

- Versi awal berbasis command line (CLI), tanpa GUI didalam
- Digunakan pribadi untuk kebutuhan kantor
- Belum didokumentasikan dan belum ada lisensi

### Catatan Etika
- Program hanya berfungsi jika pengguna memang memiliki password file-nya
- Tidak mendukung brute-force atau metode pembobolan
- Dirancang untuk penggunaan pribadi yang etis dan bertanggung jawab