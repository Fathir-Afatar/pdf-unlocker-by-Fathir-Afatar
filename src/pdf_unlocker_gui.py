import os
import time
import pikepdf
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk # For Progress Bar
import sys

# Show Splash Screen for License
def show_splash_screen():
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.configure(bg="white")

    width, height = 400, 200
    screen_width = splash.winfo_screenmmwidth()
    screen_height = splash.winfo_screenheight()
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)
    splash.geometry(f"{width}x{height}+{x}+{y}")

    tk.Label(splash, text="PDF Unlocker by Fathir Afatar", font=("Segoe UI", 16, "bold"), bg="white").pack(pady=(40, 10))
    tk.Label(splash, text="© 2025 • MIT License", font=("Segoe UI", 10), bg="white").pack()

    splash.update_idletasks() # To show the content directly

    splash.after(2000, splash.destroy)
    splash.mainloop()


# PATH to LICENSE File (from inside folder /src to root)

from tkinter import messagebox, filedialog, ttk

if getattr(sys, 'frozen', False):

    LICENSE_PATH = os.path.join(os.path.dirname(sys.executable), "LICENSE")
else:

    LICENSE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "LICENSE")

# Function to Showing the License
def show_local_license():
    try:
        with open(LICENSE_PATH, "r", encoding="utf-8") as file:
            license_text = file.read()
        messagebox.showinfo("Lisensi MIT", license_text)
    except FileNotFoundError:
        messagebox.showerror("Lisensi Tidak Ditemukan", "File LICENSE tidak ditemukan di folder proyek")

# Start the app

# Build GUI
class PDFUnlockerAPP:
    def __init__(self, master):
        self.master = master
        master.title("PDF Unlocker by Fathir Afatar")
        master.geometry("500x350")
        master.resizable(False, False)

        # Storage Variable

        self.folder_path = ""
        self.password_file = ""
        self.password_list = []

        # UI Elements

        self.create_widgets()

    def create_widgets(self):
        # Select Folder Button

        tk.Button(self.master, text="Pilih Folder PDF", command=self.select_folder).pack(pady=10)

        # Select File Password Button

        tk.Button(self.master, text = "Pilih File Password (.txt)", command=self.select_password_file).pack(padx=5)

        # Path Status Label

        self.folder_label = tk.Label(self.master, text = "Folder belum dipilih")
        self.folder_label.pack()

        self.password_label = tk.Label(self.master, text="File Password belum dipilih")
        self.password_label.pack()

        # Start Process Button

        tk.Button(self.master, text="MULAI PROSES", bg="green", fg="white", command=self.unlock_pdfs).pack(pady=15)

        # Progress bar

        self.progress = ttk.Progressbar(self.master, length=400, mode='determinate')
        self.progress.pack(pady=5)

        # Procress Status Label

        self.status_label = tk.Label(self.master, text="Status: Menunggu input ...")
        self.status_label.pack()

        info_label = tk.Label(
            self.master,
            text="Aplikasi ini 100% Gratis dan terbuka untuk semua pengguna",
            fg="gray",
            font=("Segoi UI", 8))
        info_label.place(relx=1.0, rely=1.0, anchor="se", x=-100, y=-30)

        license_label = tk.Label(self.master, text="MIT License © 2025 Fathir Afatar", fg="blue", cursor="hand2", font=("Segoe UI", 9, "underline"))
        license_label.place(relx=1.0, rely=1.0, anchor="se", x=-145, y=-10)
        license_label.bind("<Button-1>", lambda e: show_local_license())

    def select_folder(self):
        path = filedialog.askdirectory(title="Pilih Folder PDF")
        if path:
            self.folder_path = path
            self.folder_label.config(text=f"Folder: {path}")

    def select_password_file(self):
        path = filedialog.askopenfilename(title="Pilih File Password", filetypes=[("Text Files", "*.txt")])
        if path:
            self.password_file = path
            self.password_label.config(text=f"Password File: {os.path.basename(path)}")

            with open(path, "r") as f:
                self.password_list = [line.strip() for line in f.readlines()]

    def unlock_pdfs(self):
        if not self.folder_path or not self.password_list:
            messagebox.showwarning("Input Belum Lengkap", "Pastikan folder PDF dan fle password sudah dipilih.")
            return
        
        start_time = time.time()
        total_processed = 0
        failed_count = 0

        pdf_files = [f for f in os.listdir(self.folder_path) if f.endswith(".pdf")]
        total_files = len(pdf_files)

        unlocked_folder = os.path.join(self.folder_path, "unlocked_pdfs")
        os.makedirs(unlocked_folder, exist_ok=True)

        self.progress["maximum"] = total_files

        for idx, pdf_file in enumerate(pdf_files, start=1):
            self.status_label.config(text=f"Memproses: {pdf_file}")
            self.master.update()

            pdf_path = os.path.join(self.folder_path, pdf_file)
            found = False
            for password in self.password_list:
                try:
                    with pikepdf.open(pdf_path, password=password) as pdf:
                        save_path = os.path.join(unlocked_folder, pdf_file)
                        pdf.save(save_path)
                        total_processed += 1
                        found = True
                        break
                except pikepdf.PasswordError:
                    continue
            if not found:
                failed_count += 1

        self.progress["value"] = idx
        self.master.update()

        elapsed = time.time() - start_time
        self.status_label.config(
        text=f"Selesai! {total_processed} berhasil, {failed_count} gagal {elapsed: .2f}s")
        messagebox.showinfo("Selesai", "Proses selesai!\nFolder hasil akan dibuka.")
        os.startfile(unlocked_folder)



if __name__ == "__main__":
    show_splash_screen() # Showing Splash

    root = tk.Tk()
    app = PDFUnlockerAPP(root)
    root.mainloop()

