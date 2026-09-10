# Standard Library
import os
import sys
import time

# Third-party
import pikepdf
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk # For Progress Bar

TEXTS = {
    "id": {
        "title": "PDF Unlocker by Fathir Afatar",
        "btn_select_folder": "Pilih Folder PDF",
        "btn_select_pass": "Pilih File Password (.txt)",
        "folder_not_selected": "Folder belum dipilih",
        "pass_not_selected": "File Password belum dipilih",
        "btn_start": "MULAI PROSES",
        "status_waiting": "Status: Menunggu input . . .",
        "status_processing": "Memproses: {}",
        "status_done": "Selesai! {} berhasil, {} gagal ({:.2f}s)",
        "info_free": "Aplikasi ini 100% Gratis dan terbuka untuk semua pengguna",
        "dialog_folder_title": "Pilih Folder PDF",
        "dialog_pass_title": "Pilih File Password",
        "err_incomplete_title": "Input Belum Lengkap",
        "err_incomplete_msg": (
            "Pastikan folder PDF dan file password sudah dipilih."
        ),
        "done_title": "Selesai",
        "done_msg": "Proses selesai!\nFolder hasil akan dibuka.",
        "err_license_title": "Lisensi Tidak ditemukan",
        "err_license_msg": "File LICENSE tidak ditemukan di folder proyek",
        "license_mit_title": "Lisensi MIT",
    },
    "en": {
        "title": "PDF Unlocker by Fathir Afatar",
        "btn_select_folder": "Select PDF Folder",
        "btn_select_pass": "Select Password File (.txt)",
        "folder_not_selected": "Folder not selected",
        "pass_not_selected": "Password File not selected",
        "btn_start": "START PROCESS",
        "status_waiting": "Status: Waiting for input ...",
        "status_processing": "Processing: {}",
        "status_done": "Done! {} succeed, {} failed ({:.2f}s)",
        "info_free": "This application is 100% Free and open to all users",
        "dialog_folder_title": "Select PDF Folder",
        "dialog_pass_title": "Select Password File",
        "err_incomplete_title": "Incomplete Input",
        "err_incomplete_msg": (
            "Please ensure both PDF folder and password file are selected."
        ),
        "done_title": "Completed",
        "done_msg": "Process finished!\nThe output folder will be opened.",
        "err_license_title": "License Not Found",
        "err_license_msg": "LICENSE file was not found in the project directory",
        "license_mit_title": "MIT License",
    }
}

def show_splash_screen():
    """
    Display a centered splash screen for the application.

    Creates a borderless Tkinter window showing the application title and
    license info, updates the UI immediately, and closes it automatically 
    after 2000 milliseconds (2 seconds).
    """
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.configure(bg="white")

    width, height = 400, 200
    # FIXED: Changed winfo_screenmmwidth() to winfo_screenwidth() for correct pixel calculation
    screen_width = splash.winfo_screenwidth()
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

CURRENT_LANG = "id"

# Function to Showing the License
def show_local_license():
    """
    Read and display the contents of the local LICENSE file.

    Attempts to locate and open the MIT license text file based on the 
    predefined LICENSE_PATH. Shows an information dialog with the license text 
    if successful, or an error dialog if the file is missing.

    Raises:
        FileNotFoundError: If the LICENSE file cannot be found at LICENSE_PATH.
    """
    try:
        with open(LICENSE_PATH, "r", encoding="utf-8") as file:
            license_text = file.read()
        messagebox.showinfo(TEXTS[CURRENT_LANG]["license_mit_title"], license_text)
    except FileNotFoundError:
        messagebox.showerror(
            TEXTS[CURRENT_LANG]["err_license_title"], 
            TEXTS[CURRENT_LANG]["err_license_msg"],)

# Build GUI
class PDFUnlockerAPP:
    """
    The main Graphical User Interface (GUI) application for PDF Unlocker.

    This class manages the application window, handles user inputs for directory
    and file selection, reads wordlists, and orchestrates the PDF decryption 
    process using a brute-force approach with provided passwords.

    Attributes:
        master (tk.Tk): The root Tkinter window object.
        folder_path (str): Absolute path to the directory containing locked PDFs.
        password_file (str): Absolute path to the selected password text file.
        password_list (list[str]): List of password strings loaded from the file.
    """
    def __init__(self, master):
        """
        Initialize the application main windows and instance variables.

        Args:
            master (tk.TK): The root Tkinter windows instance.
        """
        self.master = master
        master.title("PDF Unlocker by Fathir Afatar")
        master.geometry("530x400")
        master.resizable(False, False)

        self.folder_path = ""
        self.password_file = ""
        self.password_list = []

        self.lang_frame = tk.Frame(self.master)
        self.lang_frame.pack(anchor="ne", padx=10, pady=5)

        self.btn_lang = tk.Button(
            self.lang_frame,
            text="🌐 EN / ID",
            command=self.toggle_language,
            font=("Segoe UI", 8, "bold")
        )
        self.btn_lang.pack()

        self.create_widgets()
        self.update_language()

    def create_widgets(self):
        """
        Create, configure, and place all GUI elements in the main window.

        Sets up interaction buttons, status labels, progress bar, information
        labels, and binds the license text click event.
        """
        self.app_title_label = tk.Label(
            self.master, font=("Segoe UI", 16, "bold"), fg="#333333"
        )
        self.app_title_label.pack(pady=(0, 15))

        self.version_label = tk.Label(
            self.master,
            text="v2.0",
            font=("Segoe UI", 9, "bold"),
            fg="#666666",
        )
        self.version_label.pack(pady=(0, 15))

        # Select Folder Button
        self.btn_folder = tk.Button(
            self.master, command=self.select_folder, width=30)
        self.btn_folder.pack(pady=5)

        # Select File Password Button
        self.btn_pass = tk.Button(
            self.master, command=self.select_password_file, width=30)
        self.btn_pass.pack(pady=5)

        # Path Status Label
        self.folder_label = tk.Label(self.master)
        self.folder_label.pack()

        self.password_label = tk.Label(self.master)
        self.password_label.pack()

        # Start Process Button
        self.btn_start = tk.Button(
            self.master, bg="green", fg="white", command=self.unlock_pdfs, width=25,)
        self.btn_start.pack(pady=15)

        # Progress bar
        self.progress = ttk.Progressbar(self.master, length=400, mode='determinate')
        self.progress.pack(pady=5)

        # Process Status Label
        self.status_label = tk.Label(self.master)
        self.status_label.pack()

        self.info_label = tk.Label(self.master, fg="gray", font=("Segoe UI", 8)) # FIXED: Typo "Segoi UI" to "Segoe UI"
        self.info_label.place(relx=1.0, rely=1.0, anchor="se", x=-100, y=-30)

        self.license_label = tk.Label(self.master, text="MIT License © 2025 Fathir Afatar", fg="blue", cursor="hand2", font=("Segoe UI", 9, "underline"))
        self.license_label.place(relx=1.0, rely=1.0, anchor="se", x=-145, y=-10)
        self.license_label.bind("<Button-1>", lambda e: show_local_license())

    def toggle_language(self):
        """Change active language between ID and EN."""
        global CURRENT_LANG
        CURRENT_LANG = "en" if CURRENT_LANG == "id" else "id"
        self.update_language()

    def update_language(self):
        """Renew all widgets text in accordance active language"""
        lang = TEXTS[CURRENT_LANG]

        self.master.title(lang["title"])
        self.app_title_label.config(text=lang["title"])

        self.btn_folder.config(text=lang["btn_select_folder"])
        self.btn_pass.config(text=lang["btn_select_pass"])
        self.btn_start.config(text=lang["btn_start"])
        self.info_label.config(text=lang["info_free"])

        # Update dynamic text if there is no chosen path
        if not self.folder_path:
            self.folder_label.config(text=lang["folder_not_selected"])
        if not self.password_file:
            self.password_label.config(text=lang["pass_not_selected"])

        self.status_label.config(text=lang["status_waiting"])

    def select_folder(self):
        """
        Open a directory dialog to let the user select the source PDF folder.

        Updates the internal folder path state and changes the corresponding
        label text if a directory is successfully chosen.
        """
        path = filedialog.askdirectory(title=TEXTS[CURRENT_LANG]["dialog_folder_title"])

        if path:
            self.folder_path = path
            self.folder_label.config(text=f"Folder: {path}")

    def select_password_file(self):
        """
        Open a file dialog to select a text file containing password.
        
        Reads the file line-by-line, strips whitespaces characters, and populates
        the internal password list variable for the unlock process.
        """
        path = filedialog.askopenfilename(title=TEXTS[CURRENT_LANG]["dialog_pass_title"], filetypes=[("Text Files", "*.txt")],)
        if path:
            self.password_file = path
            self.password_label.config(text=f"Password File: {os.path.basename(path)}")

            with open(path, "r") as f:
                self.password_list = [line.strip() for line in f.readlines()]

    def unlock_pdfs(self):
        """
        Iterate through PDFs and attempt decryption using loaded passwords
        
        Validates user inputs, creates a target folder for saved output files,
        updates progress bars dynamically, handles pikepdf password exceptions,
        and opens the destination directory upon completion.
        """
        lang = TEXTS[CURRENT_LANG]

        if not self.folder_path or not self.password_list:
            messagebox.showwarning(lang["err_incomplete_title"], lang["err_incomplete_msg"])
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
            self.status_label.config(text=lang["status_processing"].format(pdf_file))
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
        text=lang["status_done"].format(total_processed, failed_count, elapsed))
        messagebox.showinfo(lang["done_title"], lang["done_msg"])
        os.startfile(unlocked_folder)

if __name__ == "__main__":
    show_splash_screen() # Showing Splash

    root = tk.Tk()
    app = PDFUnlockerAPP(root)
    root.mainloop()