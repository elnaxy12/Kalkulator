import tkinter as tk
import re

def format_input(event=None):
    text = entry.get()

    parts = re.split(r'([+\-*/])', text)

    formatted_parts = []
    for part in parts:
        if part.strip() == "":
            continue
        if part.replace(".", "").isdigit():  
            angka = part.replace(".", "")
            formatted = "{:,}".format(int(angka)).replace(",", ".")
            formatted_parts.append(formatted)
        else:
            formatted_parts.append(part)

    new_text = "".join(formatted_parts)

    entry.delete(0, tk.END)
    entry.insert(0, new_text)

def tekan(t):
    entry.insert(tk.END, t)
    format_input()

def hapus_all():
    entry.delete(0, tk.END)

def hapus_satu():
    if entry.get():
        entry.delete(len(entry.get())-1, tk.END)

def hitung():
    try:
        expr = entry.get().replace(".", "").replace(",", ".")  
        res = eval(expr)
        entry.delete(0, tk.END)

        if isinstance(res, int) or (isinstance(res, float) and res.is_integer()):
            formatted = "{:,}".format(int(res)).replace(",", ".")
        else:
            res = round(res, 2)
            integer, decimal = str(res).split(".")
            formatted = "{:,}".format(int(integer)).replace(",", ".") + "," + decimal

        entry.insert(0, formatted)

    except Exception:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

# ==============================
#  SETUP WINDOW
# ==============================
root = tk.Tk()
root.title("Kalkulator Dark Mode")
root.configure(bg="#1b1b1b")

entry = tk.Entry(root, width=20, font=("Arial", 18), justify="right",
                 bg="#222831", fg="white", insertbackground="white")
entry.grid(row=0, column=0, columnspan=4, padx=5, pady=5, ipady=10)

entry.bind("<KeyRelease>", format_input)

# ==============================
#  FUNGSI BUAT TOMBOL
# ==============================
def buat_tombol(teks, r, c, w=2, h=2, warna="#222831", cmd=None, columnspan=1, rowspan=1):
    lbl = tk.Label(root, text=teks, width=w*2, height=h,
                   bg=warna, fg="white", font=("Arial", 14, "bold"),
                   cursor="hand2", relief="flat", bd=0)
    lbl.grid(row=r, column=c, columnspan=columnspan, rowspan=rowspan,
             padx=3, pady=3, sticky="nsew")
    if cmd:
        lbl.bind("<Button-1>", lambda e: cmd())
    return lbl

# ==============================
#  TOMBOL KALKULATOR
# ==============================

# Baris 1
buat_tombol("C", 1, 0, warna="#FF5722", cmd=hapus_all)
for i, op in enumerate(("/", "*", "-")):
    buat_tombol(op, 1, i+1, cmd=lambda t=op: tekan(t))

# Baris 2-3 angka
for r, nums in enumerate([("7", "8", "9"), ("4", "5", "6")], start=2):
    for c, n in enumerate(nums):
        buat_tombol(n, r, c, cmd=lambda t=n: tekan(t))

# Tombol + panjang (rowspan=2)
buat_tombol("+", 2, 3, cmd=lambda: tekan("+"), rowspan=2)

# Baris 4 angka
for c, n in enumerate(("1", "2", "3")):
    buat_tombol(n, 4, c, cmd=lambda t=n: tekan(t))

# Tombol = panjang (rowspan=2)
buat_tombol("=", 4, 3, h=5, warna="#00ADB5", cmd=hitung, rowspan=2)

# Baris 5
buat_tombol("0", 5, 0, cmd=lambda: tekan("0"))
buat_tombol("⌫", 5, 1, w=2, warna="#FF9800", cmd=hapus_satu, columnspan=2)

# ==============================
#  RESPONSIVE GRID
# ==============================
for i in range(4):  
    root.grid_columnconfigure(i, weight=1)
for j in range(6):  
    root.grid_rowconfigure(j, weight=1)

root.mainloop()
