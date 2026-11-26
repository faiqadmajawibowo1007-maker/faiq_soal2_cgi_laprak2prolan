#!D:/APP/python.exe
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
print("Content-Type: text/html; charset=utf-8")
print()

items = []
file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "items.txt")
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        items = [line.strip() for line in f if line.strip()]

print('''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Daftar Alat Olahraga Tersedia</title>
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
        <h2>Daftar Alat Olahraga yang Tersedia</h2>
        <p style="margin-bottom:15px; color:gray;">Berikut adalah daftar inventaris alat olahraga kampus yang dapat dipinjam:</p>
        <ul class="item-list">''')

for it in items:
    print(f"<li><strong>{it}</strong></li>")

print('''        </ul>
        <div style="margin-top:25px;">
            <a href="loan_form.py" class="btn btn-primary">Isi Form Peminjaman -></a>
            <a href="../index.html" class="btn btn-secondary"><- Kembali ke Beranda</a>
        </div>
    </div>
</body>
</html>''')
