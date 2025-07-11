import csv, os
from datetime import datetime, date
from collections import deque

produk_file = "produk.csv"
transaksi_file = "transaksi.csv"
antrian = deque()

def buat_file():
    if not os.path.exists(produk_file):
        with open(produk_file, "w", newline='') as f:
            csv.writer(f).writerow(["id", "nama", "harga", "stok", "deskripsi"])
    if not os.path.exists(transaksi_file):
        with open(transaksi_file, "w", newline='') as f:
            csv.writer(f).writerow(["id", "tanggal", "id_produk", "jumlah", "total", "tipe"])

def baca_produk():
    with open(produk_file, newline='') as f:
        data = list(csv.DictReader(f))
        for d in data:
            d["harga"] = int(d["harga"])
            d["stok"] = int(d["stok"])
        return data

def simpan_produk(data):
    with open(produk_file, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["id", "nama", "harga", "stok", "deskripsi"])
        writer.writeheader()
        writer.writerows(data)
        
def tampil_produk(data):
    if not data:
        print("Belum ada produk.")
        return
    print("\n=== Daftar Produk ===")
    for p in data:
        print(f"{p['id']}. {p['nama']} | Rp{p['harga']} | Stok: {p['stok']} | {p['deskripsi']}")

def tambah_produk(data):
    try:
        nama = input("Nama: ")
        harga = int(input("Harga: "))
        stok = int(input("Stok: "))
        deskripsi = input("Deskripsi: ")
        data.append({
            "id": str(len(data)+1),
            "nama": nama, "harga": harga, "stok": stok, "deskripsi": deskripsi
        })
        simpan_produk(data)
        print("Produk berhasil ditambahkan.")
    except:
        print("Input tidak valid.")
        
def hapus_produk(data):
    tampil_produk(data)
    id_hapus = input("ID produk yang ingin dihapus: ")
    for i, p in enumerate(data):
        if p["id"] == id_hapus:
            data.pop(i)
            for j, d in enumerate(data):
                d["id"] = str(j+1)
            simpan_produk(data)
            print("Produk dihapus.")
            return
    print("ID tidak ditemukan.")

def simpan_transaksi(t):
    with open(transaksi_file, "a", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=t.keys())
        if os.stat(transaksi_file).st_size == 0:
            writer.writeheader()
        writer.writerow(t)

def transaksi(data, tipe):
    tampil_produk(data)
    idp = input("Masukkan ID produk: ")
    for p in data:
        if p["id"] == idp:
            try:
                jumlah = int(input("Jumlah: "))
                if tipe == "penjualan":
                    if jumlah > p["stok"]:
                        print("Stok tidak cukup.")
                        return
                    p["stok"] -= jumlah
                    total = jumlah * p["harga"]
                else:  
                    harga_beli = int(input("Harga beli per unit: "))
                    p["stok"] += jumlah
                    total = jumlah * harga_beli

                simpan_produk(data)
                trx = {
                    "id": str(int(datetime.now().timestamp())),
                    "tanggal": datetime.now().strftime("%Y-%m-%d"),
                    "id_produk": idp,
                    "jumlah": jumlah,
                    "total": total,
                    "tipe": tipe
                }
                antrian.append(trx)
                simpan_transaksi(trx)
                print(f"{tipe.capitalize()} berhasil. Total: Rp{total}")
            except:
                print("Input tidak valid.")
            return
    print("Produk tidak ditemukan.")

def laporan():
    if not os.path.exists(transaksi_file):
        print("Belum ada transaksi.")
        return
    jenis = input("Laporan (harian/mingguan/bulanan): ").lower()
    today = date.today()
    total = 0

    with open(transaksi_file, newline='') as f:
        data = list(csv.DictReader(f))
        for t in data:
            tgl = datetime.strptime(t["tanggal"], "%Y-%m-%d").date()
            if (jenis == "harian" and tgl == today) or \
               (jenis == "mingguan" and (today - tgl).days <= 7) or \
               (jenis == "bulanan" and tgl.month == today.month and tgl.year == today.year):
                print(f"{t['tanggal']} | {t['tipe']} | ID {t['id_produk']} | Jumlah: {t['jumlah']} | Rp{t['total']}")
                total += int(t["total"])
    print(f"Total {jenis}: Rp{total}")

def menu():
    buat_file()
    produk = baca_produk()
    while True:
        print("\n=== MENU ===")
        print("1. Lihat Produk\n2. Tambah Produk\n3. Hapus Produk")
        print("4. Jual Produk\n5. Beli Produk\n6. Laporan\n7. Keluar")
        pilih = input("Pilih (1-7): ")

        if pilih == "1": tampil_produk(produk)
        elif pilih == "2": tambah_produk(produk)
        elif pilih == "3": hapus_produk(produk)
        elif pilih == "4": transaksi(produk, "penjualan")
        elif pilih == "5": transaksi(produk, "pembelian")
        elif pilih == "6": laporan()
        elif pilih == "7":
            print("Terima kasih! Program selesai.")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    menu()
