#!D:/APP/python.exe
import os
import sys
import urllib.parse

sys.stdout.reconfigure(encoding="utf-8")
print("Content-Type: text/html; charset=utf-8")
print()

method = os.environ.get("REQUEST_METHOD", "GET")
if method == "POST":
    try:
        length = int(os.environ.get("CONTENT_LENGTH", 0))
        body = sys.stdin.read(length) if length > 0 else ""
    except Exception:
        body = ""
    params = urllib.parse.parse_qs(body)
else:
    query = os.environ.get("QUERY_STRING", "")
    params = urllib.parse.parse_qs(query)

nama = params.get("nama", [""])[0].strip()
item = params.get("item", [""])[0].strip()
lama = params.get("lama", [""])[0].strip()

berhasil = False
if nama and item and lama:
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "loans.txt")
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"{nama},{item},{lama}\n")
    berhasil = True

print(f'''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Status Peminjaman</title>
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
        <h2>Konfirmasi Peminjaman</h2>''')

if berhasil:
    print(f'''
        <div class="alert-success">
            <strong>Berhasil!</strong> Data peminjaman berhasil disimpan ke dalam sistem.
        </div>
        <p><strong>Nama Peminjam:</strong> {nama}</p>
        <p><strong>Alat Olahraga:</strong> {item}</p>
        <p><strong>Lama Peminjaman:</strong> {lama} Hari</p>
        <div style="margin-top:25px;">
            <a href="view_loans.py" class="btn btn-primary">Lihat Seluruh Peminjaman -></a>
            <a href="loan_form.py" class="btn btn-secondary">+ Pinjam Alat Lain</a>
        </div>
    ''')
else:
    print('''
        <p style="color:red;">Data gagal diproses. Pastikan seluruh input terisi dengan lengkap.</p>
        <a href="loan_form.py" class="btn btn-primary"><- Kembali ke Form</a>
    ''')

print('''
    </div>
</body>
</html>''')
