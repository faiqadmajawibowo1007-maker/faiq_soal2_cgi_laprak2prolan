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
    <title>Formulir Peminjaman Alat Olahraga</title>
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
        <h2>Formulir Peminjaman Alat Olahraga</h2>
        <form action="save_loan.py" method="POST">
            <div class="form-group">
                <label for="nama">Nama Peminjam:</label>
                <input type="text" id="nama" name="nama" required placeholder="Masukkan nama lengkap peminjam">
            </div>
            <div class="form-group">
                <label for="item">Pilih Alat Olahraga:</label>
                <select id="item" name="item" required>
                    <option value="">-- Pilih Alat Olahraga --</option>''')

for it in items:
    print(f'<option value="{it}">{it}</option>')

print('''                </select>
            </div>
            <div class="form-group">
                <label for="lama">Lama Peminjaman (Hari):</label>
                <input type="number" id="lama" name="lama" min="1" max="14" required placeholder="Contoh: 3">
            </div>
            <button type="submit" class="btn btn-primary" style="border:none; cursor:pointer;">Simpan Data Peminjaman -></button>
        </form>
    </div>
</body>
</html>''')
