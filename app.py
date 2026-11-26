import os
import shutil
import zipfile
from flask import Flask, request, send_from_directory, Response

app = Flask(__name__)

base_dir = os.path.dirname(os.path.abspath(__file__))

def get_loans_file():
    local_path = os.path.join(base_dir, "loans.txt")
    tmp_path = "/tmp/loans.txt"
    try:
        with open(local_path, "a", encoding="utf-8") as f:
            pass
        return local_path
    except (OSError, PermissionError):
        if not os.path.exists(tmp_path) and os.path.exists(local_path):
            try:
                shutil.copyfile(local_path, tmp_path)
            except Exception:
                pass
        return tmp_path

def get_items():
    items = []
    file_path = os.path.join(base_dir, "items.txt")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            items = [line.strip() for line in f if line.strip()]
    return items

def get_loans():
    loans = []
    file_path = get_loans_file()
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 3:
                    loans.append(parts)
    return loans

@app.route("/")
@app.route("/index.html")
def index():
    path = os.path.join(base_dir, "index.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return Response(content, mimetype="text/html")

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(os.path.join(base_dir, "static"), filename)

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(base_dir, "favicon.ico")

@app.route("/cgi-bin/items.py")
def cgi_items():
    items = get_items()
    html = '''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Daftar Alat Olahraga Tersedia</title>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <nav class="navbar">
        <a href="/index.html" class="brand"> SportLoan Hub</a>
        <div class="nav-links">
            <a href="/index.html">Beranda</a>
            <a href="/cgi-bin/items.py">Daftar Alat</a>
            <a href="/cgi-bin/loan_form.py">Form Peminjaman</a>
            <a href="/cgi-bin/view_loans.py">Data Peminjaman</a>
        </div>
    </nav>
    <div class="container">
        <h2>Daftar Alat Olahraga yang Tersedia</h2>
        <p style="margin-bottom:15px; color:gray;">Berikut adalah daftar inventaris alat olahraga kampus yang dapat dipinjam:</p>
        <ul class="item-list">'''
    for it in items:
        html += f"<li><strong>{it}</strong></li>"
    html += '''</ul>
        <div style="margin-top:25px;">
            <a href="/cgi-bin/loan_form.py" class="btn btn-primary">Isi Form Peminjaman -></a>
            <a href="/index.html" class="btn btn-secondary"><- Kembali ke Beranda</a>
        </div>
    </div>
</body>
</html>'''
    return Response(html, mimetype="text/html")

@app.route("/cgi-bin/loan_form.py")
def cgi_loan_form():
    items = get_items()
    html = '''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Formulir Peminjaman Alat Olahraga</title>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <nav class="navbar">
        <a href="/index.html" class="brand"> SportLoan Hub</a>
        <div class="nav-links">
            <a href="/index.html">Beranda</a>
            <a href="/cgi-bin/items.py">Daftar Alat</a>
            <a href="/cgi-bin/loan_form.py">Form Peminjaman</a>
            <a href="/cgi-bin/view_loans.py">Data Peminjaman</a>
        </div>
    </nav>
    <div class="container">
        <h2>Formulir Peminjaman Alat Olahraga</h2>
        <form action="/cgi-bin/save_loan.py" method="POST">
            <div class="form-group">
                <label for="nama">Nama Peminjam:</label>
                <input type="text" id="nama" name="nama" required placeholder="Masukkan nama lengkap peminjam">
            </div>
            <div class="form-group">
                <label for="item">Pilih Alat Olahraga:</label>
                <select id="item" name="item" required>
                    <option value="">-- Pilih Alat Olahraga --</option>'''
    for it in items:
        html += f'<option value="{it}">{it}</option>'
    html += '''</select>
            </div>
            <div class="form-group">
                <label for="lama">Lama Peminjaman (Hari):</label>
                <input type="number" id="lama" name="lama" min="1" max="14" required placeholder="Contoh: 3">
            </div>
            <button type="submit" class="btn btn-primary" style="border:none; cursor:pointer;">Simpan Data Peminjaman </button>
        </form>
    </div>
</body>
</html>'''
    return Response(html, mimetype="text/html")

@app.route("/cgi-bin/save_loan.py", methods=["GET", "POST"])
def cgi_save_loan():
    if request.method == "POST":
        nama = request.form.get("nama", "").strip()
        item = request.form.get("item", "").strip()
        lama = request.form.get("lama", "").strip()
    else:
        nama = request.args.get("nama", "").strip()
        item = request.args.get("item", "").strip()
        lama = request.args.get("lama", "").strip()

    berhasil = False
    if nama and item and lama:
        target_file = get_loans_file()
        try:
            with open(target_file, "a", encoding="utf-8") as f:
                f.write(f"{nama},{item},{lama}\n")
            berhasil = True
        except Exception:
            berhasil = False

    html = f'''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Status Peminjaman</title>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <nav class="navbar">
        <a href="/index.html" class="brand"> SportLoan Hub</a>
        <div class="nav-links">
            <a href="/index.html">Beranda</a>
            <a href="/cgi-bin/items.py">Daftar Alat</a>
            <a href="/cgi-bin/loan_form.py">Form Peminjaman</a>
            <a href="/cgi-bin/view_loans.py">Data Peminjaman</a>
        </div>
    </nav>
    <div class="container">
        <h2>Konfirmasi Peminjaman</h2>'''

    if berhasil:
        html += f'''
        <div class="alert-success">
            <strong>Berhasil!</strong> Data peminjaman berhasil disimpan ke dalam sistem.
        </div>
        <p><strong>Nama Peminjam:</strong> {nama}</p>
        <p><strong>Alat Olahraga:</strong> {item}</p>
        <p><strong>Lama Peminjaman:</strong> {lama} Hari</p>
        <div style="margin-top:25px;">
            <a href="/cgi-bin/view_loans.py" class="btn btn-primary">Lihat Seluruh Peminjaman -></a>
            <a href="/cgi-bin/loan_form.py" class="btn btn-secondary">+ Pinjam Alat Lain</a>
        </div>'''
    else:
        html += '''
        <p style="color:red;">Data gagal diproses. Pastikan seluruh input terisi dengan lengkap.</p>
        <a href="/cgi-bin/loan_form.py" class="btn btn-primary"><- Kembali ke Form</a>'''

    html += '''
    </div>
</body>
</html>'''
    return Response(html, mimetype="text/html")

@app.route("/cgi-bin/view_loans.py")
def cgi_view_loans():
    loans = get_loans()
    html = '''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Daftar Data Peminjaman</title>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <nav class="navbar">
        <a href="/index.html" class="brand"> SportLoan Hub</a>
        <div class="nav-links">
            <a href="/index.html">Beranda</a>
            <a href="/cgi-bin/items.py">Daftar Alat</a>
            <a href="/cgi-bin/loan_form.py">Form Peminjaman</a>
            <a href="/cgi-bin/view_loans.py">Data Peminjaman</a>
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
            <tbody>'''

    if loans:
        for idx, row in enumerate(loans, 1):
            html += f"<tr><td>{idx}</td><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]} Hari</td></tr>"
    else:
        html += "<tr><td colspan='4' style='text-align:center;'>Belum ada data peminjaman yang tercatat.</td></tr>"

    html += '''            </tbody>
        </table>
        <div style="margin-top:25px;">
            <a href="/cgi-bin/loan_form.py" class="btn btn-primary">+ Tambah Peminjaman Baru</a>
            <a href="/index.html" class="btn btn-secondary"><- Kembali ke Beranda</a>
        </div>
    </div>
</body>
</html>'''
    return Response(html, mimetype="text/html")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
