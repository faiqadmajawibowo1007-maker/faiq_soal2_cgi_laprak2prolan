#!D:/APP/python.exe
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
print("Content-Type: text/html; charset=utf-8")
print()

loans = []
file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "loans.txt")
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) >= 3:
                loans.append(parts)

print('''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Daftar Data Peminjaman</title>
    <link rel="icon" type="image/x-icon" href="../favicon.ico">
    <link rel="stylesheet" href="../static/style.css">
</head>
<body>
    <nav class="navbar">
        <a href="../index.html" class="brand">SportLoan Hub</a>
        <div class="nav-links">
            <a href="../index.html">Beranda</a>
            <a href="items.py">Daftar Alat</a>
            <a href="loan_form.py">Form Peminjaman</a>
            <a href="view_loans.py">Data Peminjaman</a>
        </div>
    </nav>
    <div class="container">
        <h2>Daftar Riwayat Peminjaman Alat Olahraga</h2>
        <table class="table">
            <thead>
                <tr>
                    <th>No</th>
                    <th>Nama Peminjam</th>
                    <th>Alat Olahraga</th>
                    <th>Lama Peminjaman</th>
                </tr>
            </thead>
            <tbody>''')

if loans:
    for idx, row in enumerate(loans, 1):
        print(f"<tr><td>{idx}</td><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]} Hari</td></tr>")
else:
    print("<tr><td colspan='4' style='text-align:center;'>Belum ada data peminjaman yang tercatat.</td></tr>")

print('''            </tbody>
        </table>
        <div style="margin-top:25px;">
            <a href="loan_form.py" class="btn btn-primary">+ Tambah Peminjaman Baru</a>
            <a href="../index.html" class="btn btn-secondary"><- Kembali ke Beranda</a>
        </div>
    </div>
</body>
</html>''')
