import sqlite3
import tkinter as tk 
import tkinter.messagebox as msg

def create_db():
    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS nilai_siswa (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    nama TEXT NOT NULL,
    BIOLOGI INTEGER NOT NULL,
    FISIKA INTEGER NOT NULL,
    BAHASA_INGGRIS INTEGER NOT NULL,
    PREDIKSI_FAKULTAS TEXT NOT NULL
    )''')   
    conn.commit()
    conn.close()

def PREDIKSI_FAKULTAS(biologi, fisika, bahasa_inggris):
    nilai_tertinggi = max(biologi, fisika, bahasa_inggris)

    if [biologi, fisika, bahasa_inggris].count(nilai_tertinggi) > 1:
        return "Nilai Seri"
    elif nilai_tertinggi == biologi:
        return "Fakultas Kedokteran"
    elif nilai_tertinggi == fisika:
        return "Fakultas Teknik"
    else:
        return "Fakultas Bahasa"

def submit_nilai():
    nama = entry_nama.get().strip()

    if not nama:
        msg.showerror("Error", "Nama tidak boleh kosong.")
        return
        
    try:
        biologi = int(entry_biologi.get())
        fisika = int(entry_fisika.get())
        bahasa_inggris = int(entry_bahasa_inggris.get())
    except ValueError:
        msg.showerror("Error", "Nilai harus berupa angka.")
        return
        
    if any(nilai < 0 or nilai > 100 for nilai in [biologi, fisika, bahasa_inggris]):
        msg.showerror("Error", "Nilai harus antara 0 hingga 100.")
        return

    prediksi = PREDIKSI_FAKULTAS(biologi, fisika, bahasa_inggris)
    
    if prediksi == "Nilai Seri":
        msg.showinfo("Hasil Prediksi", "Nilai tertinggi seri, tidak dapat memprediksi fakultas.")
        return

    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute ("INSERT INTO nilai_siswa (nama, BIOLOGI, FISIKA, BAHASA_INGGRIS, PREDIKSI_FAKULTAS) VALUES (?, ?, ?, ?, ?)",
                      (nama, biologi, fisika, bahasa_inggris, prediksi))
    conn.commit()
    conn.close()

    label_hasil.config(text=f"Prediksi Fakultas: {prediksi}")
    msg.showinfo("Hasil Prediksi", f"Data Berhasil Disimpan!\nPrediksi Fakultas: {prediksi}")

    entry_nama.delete(0, tk.END)
    entry_biologi.delete(0, tk.END)
    entry_fisika.delete(0, tk.END)
    entry_bahasa_inggris.delete(0, tk.END)

create_db() # Memanggil fungsi pembuat database saat aplikasi pertama dijalankan

root = tk.Tk()
root.title("Prediksi Fakultas Berdasarkan Nilai Siswa")
root.geometry("400x450") # Sedikit diperbesar ukurannya agar tampilan tidak menumpuk

tk.Label(root, text="PREDIKSI FAKULTAS SISWA", font=("Arial", 16, "bold")).pack(pady=10)

tk.Label(root, text="Nama Siswa", font=("Arial", 12)).pack()
entry_nama = tk.Entry(root, font=("Arial", 12))
entry_nama.pack(pady=5)

tk.Label(root, text="Nilai Biologi", font=("Arial", 12)).pack()
entry_biologi = tk.Entry(root, font=("Arial", 12))
entry_biologi.pack(pady=5)

tk.Label(root, text="Nilai Fisika", font=("Arial", 12)).pack()
entry_fisika = tk.Entry(root, font=("Arial", 12))
entry_fisika.pack(pady=5)

tk.Label(root, text="Nilai Bahasa Inggris", font=("Arial", 12)).pack()
entry_bahasa_inggris = tk.Entry(root, font=("Arial", 12))
entry_bahasa_inggris.pack(pady=5)

tk.Button(root, text="Submit", font=("Arial", 12), command=submit_nilai).pack(pady=10)

label_hasil = tk.Label(root, text="Prediksi Fakultas: ", font=("Arial", 12, "bold"), fg="blue")
label_hasil.pack(pady=10)

root.mainloop()