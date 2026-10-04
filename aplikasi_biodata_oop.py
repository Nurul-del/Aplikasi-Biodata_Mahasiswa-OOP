import re
import tkinter as tk
from tkinter import messagebox
import datetime
import logging

# Setup logging
logging.basicConfig(
    filename='aplikasi_biodata.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Membuat kelas utama aplikasi yang mewarisi dari tk.Tk
class AplikasiBiodata(tk.Tk):
    # Metode __init__ adalah constructor yang akan dijalankan saat objek dibuat
    def __init__(self):
        super().__init__()
        self.title("Aplikasi Biodata Mahasiswa")
        self.geometry("600x700")
        self.resizable(True, True)
        
        # Database user sederhana (dalam aplikasi nyata, ini akan di database)
        self.users_db = {
            "admin": "123",
            "user1": "password1",
            "mahasiswa": "123456",
            "Nurul Fatiha(24106050005)": "12345678"
        }
        
        self.tema_user = {
            "admin": "#20b2aa",       
            "user1": "#98f5ff",        
            "mahasiswa": "#ffd700",     
            "Nurul Fatiha(24106050005)": "#ffb6c1"  
        }

        
        # Status login
        self.current_user = None

        # Atribut untuk manajemen frame
        self.frame_aktif = None

        # Buat tampilan
        self._buat_tampilan_login()
        self._buat_tampilan_biodata()

        # Tampilkan frame login di awal
        self._pindah_ke(self.frame_login)
        self._hapus_menu()
        logging.info("Aplikasi dimulai")
        
    def _buat_tampilan_biodata(self):
    # --- Variabel Kontrol Tkinter ---
        self.var_nama = tk.StringVar()
        self.var_nim = tk.StringVar()
        self.var_jurusan = tk.StringVar()
        self.var_jk = tk.StringVar(value="Pria")
        self.var_setuju = tk.IntVar()
        self.var_email = tk.StringVar()
        self.var_telepon = tk.StringVar()
        self.var_tgl = tk.StringVar()
        
        # Aktifkan trace untuk validasi real-time
        self.var_nama.trace_add("write", self.validate_form)
        self.var_nim.trace_add("write", self.validate_form)
        self.var_jurusan.trace_add("write", self.validate_form)
        self.var_email.trace_add("write", self.validate_form)
        self.var_telepon.trace_add("write", self.validate_form)
        self.var_tgl.trace_add("write", self.validate_form)
        
        # --- Frame Biodata ---
        self.frame_biodata = tk.Frame(master=self, padx=20, pady=20, bg="#f0ffff")
        self.frame_biodata.columnconfigure(1, weight=1)
        #self.frame_biodata.pack(fill=tk.BOTH, expand=True)
       
        # --- Membuat dan Menempatkan Widget ---
        # Judul
        self.label_judul = tk.Label(
            master=self.frame_biodata, 
            text="FORM BIODATA MAHASISWA", 
            font=("Arial", 16, "bold"),
            bg="#f0ffff",
            fg="black"
    
        )
        self.label_judul.grid(row=0, column=0, columnspan=2, pady=20)

        # Frame khusus untuk input dengan border
        self.frame_input = tk.Frame(
            master=self.frame_biodata, 
            relief=tk.GROOVE, 
            borderwidth=4, 
            padx=10, 
            pady=10,
            bg="#f0ffff"
        )
        self.frame_input.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)
        
        # Input Nama
        self.label_nama = tk.Label(
            master=self.frame_input, 
            text="Nama Lengkap: ", 
            font=("Arial", 12),
            bg="#f0ffff",
            fg="black"
        )
        self.label_nama.grid(row=0, column=0, sticky="W", pady=2)
        self.entry_nama = tk.Entry(
            master=self.frame_input, 
            width=30, 
            font=("Arial", 12), 
            textvariable=self.var_nama,
            bd=2
        )
        self.entry_nama.grid(row=0, column=1, pady=2)

        # Input NIM
        self.label_nim = tk.Label(
            master=self.frame_input, 
            text="NIM: ", 
            font=("Arial", 12),
            bg="#f0ffff",
            fg="black"
        )
        self.label_nim.grid(row=1, column=0, sticky="W", pady=2)
        self.entry_nim = tk.Entry(
            master=self.frame_input, 
            width=30, 
            font=("Arial", 12), 
            textvariable=self.var_nim,
            bd=2
        )
        self.entry_nim.grid(row=1, column=1, pady=2)
        
        # Input Jurusan
        self.label_jurusan = tk.Label(
            master=self.frame_input, 
            text="Jurusan: ", 
            font=("Arial", 12),
            bg="#f0ffff",
            fg="black"
        )
        self.label_jurusan.grid(row=2, column=0, sticky="W", pady=2)
        self.entry_jurusan = tk.Entry(
            master=self.frame_input, 
            width=30, 
            font=("Arial", 12), 
            textvariable=self.var_jurusan,
            bd=2
        )
        self.entry_jurusan.grid(row=2, column=1, pady=2)

        # Input alamat dengan Text widget
        self.label_alamat = tk.Label(
            master=self.frame_input, 
            text="Alamat: ", 
            font=("Arial", 12),
            bg="#f0ffff",
            fg="black"
        )
        self.label_alamat.grid(row=6, column=0, sticky="NW", pady=2) #Harus Paham di bagian ini

        # Frame untuk Text dan Scrollbar
        self.frame_alamat = tk.Frame(
            master=self.frame_input, 
            relief=tk.SUNKEN, 
            borderwidth=2
        )

        # Scrollbar untuk alamat
        self.scrollbar_alamat = tk.Scrollbar(master=self.frame_alamat)
        self.scrollbar_alamat.pack(side=tk.RIGHT, fill=tk.Y)

        # Text widget untuk alamat
        self.text_alamat = tk.Text(
            master=self.frame_alamat, 
            height=5, 
            width=28, 
            font=("Arial", 12)
        )
        self.text_alamat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Hubungkan scrollbar dengan text
        self.scrollbar_alamat.config(command=self.text_alamat.yview)
        self.text_alamat.config(yscrollcommand=self.scrollbar_alamat.set)
        self.frame_alamat.grid(row=6, column=1, pady=2)
        
        
        # Jenis kelamin
        self.label_jk = tk.Label(
            master=self.frame_input, 
            text="Jenis Kelamin:", 
            font=("Arial", 12),
            bg="#f0ffff",
            fg="black"
        )
        self.label_jk.grid(row=7, column=0, sticky="W", pady=2)

        self.frame_jk = tk.Frame(master=self.frame_input, bg="#f0ffff")
        self.frame_jk.grid(row=7, column=1, sticky="W")

        self.radio_pria = tk.Radiobutton(
            master=self.frame_jk, 
            text="Pria", 
            variable=self.var_jk, 
            value="Pria",
            bg="#f0ffff",
            fg="black",
             activebackground="#f0ffff"
        )
        self.radio_pria.pack(side=tk.LEFT)
        self.radio_wanita = tk.Radiobutton(
            master=self.frame_jk, 
            text="Wanita", 
            variable=self.var_jk, 
            value="Wanita",
            bg="#f0ffff",
            fg="black",
            activebackground="#f0ffff"
        )
        self.radio_wanita.pack(side=tk.LEFT)

        # Checkbox persetujuan
        self.check_setuju = tk.Checkbutton(
            master=self.frame_input,
            text="Saya menyetujui pengumpulan data ini.",
            variable=self.var_setuju,
            font=("Arial", 10),
            bg="#f0ffff",
            fg="black",
            activebackground="#f0ffff",
            command=self.validate_form
        )
        self.check_setuju.grid(row=8, column=0, columnspan=2, pady=10, sticky="W")
                       
        # Tombol submit
        self.btn_submit = tk.Button(
            master=self.frame_biodata, 
            text="Submit Biodata", 
            font=("Arial", 12, "bold"),
            command=self.submit_data,
            state=tk.DISABLED
            
        )
        self.btn_submit.grid(row=6, column=0, columnspan=2, pady=20, sticky="EW")
        self.btn_reset = tk.Button(
            master=self.frame_biodata, text="Reset Form",
            font=("Arial", 10), command=self._konfirmasi_reset
        )
        self.btn_reset.grid(row=7, column=0, columnspan=2, sticky="EW")
        
        # Event bindings untuk hover dan keyboard shortcuts
        self.btn_submit.bind("<Enter>", self.on_enter)
        self.btn_submit.bind("<Leave>", self.on_leave)

        # Keyboard shortcuts
        self.entry_nama.bind("<Return>", self.submit_shortcut)
        self.entry_nim.bind("<Return>", self.submit_shortcut)
        self.entry_jurusan.bind("<Return>", self.submit_shortcut)
        #self.text_alamat.bind("<Return>", self.submit_shortcut)
        self.text_alamat.bind("<KeyRelease>", self.validate_form)

        # Label hasil
        self.label_hasil = tk.Label(
            master=self.frame_biodata, 
            text="", 
            font=("Arial", 12, "italic"), 
            justify=tk.LEFT,
            bg="#f0ffff"
        )
        self.label_hasil.grid(row=8, column=0, columnspan=2, sticky="W", padx=10)      
        
        # Email
        self.label_email = tk.Label(
            master=self.frame_input, text="Email: ",
            font=("Arial", 12), bg="#f0ffff", fg="black"
        )
        self.label_email.grid(row=3, column=0, sticky="W", pady=2)
        self.entry_email = tk.Entry(
            master=self.frame_input, width=30, font=("Arial", 12),
            textvariable=self.var_email, bd=2
        )
        self.entry_email.grid(row=3, column=1, pady=2)

        # Telepon
        self.label_telepon = tk.Label(
            master=self.frame_input, text="No. Telepon: ",
            font=("Arial", 12), bg="#f0ffff", fg="black"
        )
        self.label_telepon.grid(row=4, column=0, sticky="W", pady=2)
        self.entry_telepon = tk.Entry(
            master=self.frame_input, width=30, font=("Arial", 12),
            textvariable=self.var_telepon, bd=2
        )
        self.entry_telepon.grid(row=4, column=1, pady=2)

        # Tanggal lahir
        self.label_tgl = tk.Label(
            master=self.frame_input, text="Tgl Lahir (DD-MM-YYYY): ",
            font=("Arial", 12), bg="#f0ffff", fg="black"
        )
        self.label_tgl.grid(row=5, column=0, sticky="W", pady=2)
        self.entry_tgl = tk.Entry(
            master=self.frame_input, width=30, font=("Arial", 12),
            textvariable=self.var_tgl, bd=2
        )
        self.entry_tgl.grid(row=5, column=1, pady=2)
        
        
        # Membuat menu
        self._buat_menu()
    
                # (Di sini kita akan meletakkan semua kode GUI nantinya)
    def submit_data(self):
        """Submit data biodata dengan validasi lengkap"""
        try:
            # Cek checkbox
            if self.var_setuju.get() == 0:
                messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
                return

            # Ambil data dari form
            nama = self.entry_nama.get().strip()
            nim = self.entry_nim.get().strip()
            jurusan = self.entry_jurusan.get().strip()
            email = self.entry_email.get().strip()
            telepon = self.entry_telepon.get().strip()
            tgl_lahir = self.entry_tgl.get().strip()
            alamat = self.text_alamat.get("1.0", tk.END).strip()
            jenis_kelamin = self.var_jk.get()

            # Validasi field kosong
            if not nama or not nim or not jurusan:
                messagebox.showwarning("Input Kosong", "Nama, NIM, dan Jurusan harus diisi!")
                return

            # Validasi format NIM (harus angka dan minimal 8 digit)
            if not nim.isdigit() or len(nim) < 8:
                messagebox.showwarning("Format NIM Salah", "NIM harus berupa angka minimal 8 digit!")
                self.entry_nim.focus_set()
                return

            # Validasi nama (tidak boleh hanya angka)
            if nama.isdigit():
                messagebox.showwarning("Format Nama Salah", "Nama tidak boleh hanya berupa angka!")
                self.entry_nama.focus_set()
                return

            # Tampilkan hasil
            hasil = (f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\n"
                     f"Email: {email}\nTelepon: {telepon}\nTanggal Lahir: {tgl_lahir}\n"
                     f"Alamat: {alamat}\nJenis Kelamin: {jenis_kelamin}")
            messagebox.showinfo("Data Tersimpan", hasil)

            # Tampilkan hasil di label dengan info user
            hasil_lengkap = f"BIODATA TERSIMPAN:\nDiinput oleh: {self.current_user}\n\n{hasil}"
            self.label_hasil.config(text=hasil_lengkap)
            logging.info(f"Data submitted by user: {self.current_user} - NIM: {nim}")   # <-- baru
        except Exception as e:
            logging.error(f"Error in submit_data by {self.current_user}: {str(e)}")   # <-- baru
            messagebox.showerror("Error", f"Terjadi kesalahan saat memproses data:\n{str(e)}")
        

    def validate_form(self, *args): # tambah warna merah
        nama = self.var_nama.get().strip()
        nim = self.var_nim.get().strip()
        jurusan = self.var_jurusan.get().strip()

        nama_valid = re.fullmatch(r"[A-Za-z .'-]+", nama) is not None
        jurusan_valid = re.fullmatch(r"[A-Za-z .'-]+", jurusan) is not None
        email = self.var_email.get().strip()
        telepon = self.var_telepon.get().strip()
        tgl = self.var_tgl.get().strip()

        email_valid = re.fullmatch(r"[\w.+-]+@[\w-]+(\.[\w-]+)+", email) is not None
        telepon_valid = re.fullmatch(r"(\+62|62|0)8[0-9]{8,11}", telepon) is not None
        tgl_valid = self._tanggal_valid(tgl)

        self._warnai(self.entry_email, email, email_valid)
        self._warnai(self.entry_telepon, telepon, telepon_valid)
        self._warnai(self.entry_tgl, tgl, tgl_valid)
        nim_valid = re.fullmatch(r"[0-9]{8,}", nim) is not None
        
        # ada warna merah kalau salah
        self._warnai(self.entry_nama, nama, nama_valid)
        self._warnai(self.entry_nim, nim, nim_valid)
        self._warnai(self.entry_jurusan, jurusan, jurusan_valid)

        alamat_valid = self.text_alamat.get("1.0", tk.END).strip() != ""
        setuju_valid = self.var_setuju.get() == 1

        if (nama_valid and nim_valid and jurusan_valid and email_valid and telepon_valid and tgl_valid and alamat_valid and setuju_valid):            
            self.btn_submit.config(state=tk.NORMAL)
        else:
            self.btn_submit.config(state=tk.DISABLED)

    def _warnai(self, entry, teks, valid):
        """Merah kalau ada isi tapi tidak valid, putih kalau valid atau masih kosong"""
        entry.config(bg="white" if valid or teks == "" else "#dc143c")
    
    def on_enter(self, event):
        if  self.btn_submit['state'] == tk.NORMAL:
            self.btn_submit.config(bg="#1e90ff")

    def on_leave(self, event):
            self.btn_submit.config(bg="#f0f0f0")

    def submit_shortcut(self, event=None):
        if  self.btn_submit['state'] == tk.NORMAL:
            self.submit_data()
            
    def _buat_tampilan_login(self):
        self.frame_login = tk.Frame(master=self, padx=20, pady=100)
        self.var_ingat = tk.IntVar(value=0)
        tk.Checkbutton(
            
            self.frame_login,
            text="Ingat saya",
            variable=self.var_ingat,
        ).grid(row=3, column=0, sticky="W")
        
        # Konfigurasi grid untuk frame login agar terpusat
        self.frame_login.grid_columnconfigure(0, weight=1)
        self.frame_login.grid_columnconfigure(1, weight=1)

        # Judul Login
        tk.Label(
            self.frame_login, 
            text="HALAMAN LOGIN", 
            font=("Arial", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=20)

        # Input Username
        tk.Label(
            self.frame_login, 
            text="Username:", 
            font=("Arial", 12)
        ).grid(row=1, column=0, sticky="W", pady=5)

        self.entry_username = tk.Entry(self.frame_login, font=("Arial", 12))
        self.entry_username.grid(row=1, column=1, pady=5, sticky="EW")
        
        # Input Password
        tk.Label(
            self.frame_login, 
            text="Password:", 
            font=("Arial", 12)
        ).grid(row=2, column=0, sticky="W", pady=5)

        self.entry_password = tk.Entry(
            self.frame_login, 
            font=("Arial", 12), 
            show="*"
        )
        self.entry_password.grid(row=2, column=1, pady=5, sticky="EW")
        self.var_tampilan_pw =tk.IntVar(value=0)
        tk.Checkbutton(
            self.frame_login, 
            text="Tampilkan Password", 
            variable=self.var_tampilan_pw, 
            command=self._toggle_password
        ).grid(row=3, column=1, sticky="W", pady=5)
        
        # Tombol Login
        self.btn_login = tk.Button(
            self.frame_login, 
            text="Login", 
            font=("Arial", 12, "bold"),
            command=self._coba_login
        )
        self.btn_login.grid(row=4, column=0, columnspan=2, pady=20, sticky="EW")

        # Keyboard shortcuts untuk login
        self.entry_username.bind("<Return>", lambda e: self.entry_password.focus_set())
        self.entry_password.bind("<Return>", lambda e: self._coba_login())

        # Info untuk user
        info_label = tk.Label(
            self.frame_login,
            text="Info: Username yang tersedia:\nadmin (password: 123)\nuser1 (password: password1)\nmahasiswa (password: 123456)\nNurul Fatiha(24106050005) (password: 12345678)",
            font=("Arial", 9),
            fg="gray",
            justify=tk.LEFT
        )
        info_label.grid(row=5, column=0, columnspan=2, pady=10)
        
        self._muat_username()
        
    def _pindah_ke(self, frame_tujuan):
        """Method untuk berpindah antar tampilan"""
        if self.frame_aktif is not None:
            self.frame_aktif.pack_forget()

        self.frame_aktif = frame_tujuan
        self.frame_aktif.pack(fill=tk.BOTH, expand=True)

        # Auto-focus berdasarkan frame yang ditampilkan
        if frame_tujuan == self.frame_login:
            self.after(100, lambda: self.entry_username.focus_set())
        elif frame_tujuan == self.frame_biodata:
            self.after(100, lambda: self.entry_nama.focus_set())        

    def _coba_login(self):
        """Method untuk memproses attempt login"""
        username = self.entry_username.get().strip()
        password = self.entry_password.get()
        
        logging.info(f"Login attempt for username: {username}")         

        # Validasi input kosong
        if not username or not password:
            logging.warning(f"Empty credentials attempt for username: {username}")  
            messagebox.showwarning("Login Gagal", "Username dan Password tidak boleh kosong.")
            self.entry_username.focus_set()
            return

        # Validasi panjang minimum
        if len(username) < 3:
            logging.warning(f"Username too short: {username}")           # <-- baru
            messagebox.showwarning("Login Gagal", "Username minimal 3 karakter.")
            self.entry_username.focus_set()
            return
        
        # Cek kredensial di database
        if username in self.users_db and self.users_db[username] == password:
            self.current_user = username
            logging.info(f"Successful login for user: {username}")       # <-- baru
            messagebox.showinfo("Login Berhasil", f"Selamat Datang, {username}!")
            self._reset_form_biodata()
            self._update_title_with_user()
            self._terapkan_tema(self.tema_user.get(username, "#f0ffff"))
            self._buat_menu()
            self._pindah_ke(self.frame_biodata)
            self._simpan_username(username)
            self.entry_password.delete(0, tk.END)         
            if not self.var_ingat.get():                   
                self.entry_username.delete(0, tk.END)      
        else:
            logging.warning(f"Failed login attempt for username: {username}")   # <-- baru
            messagebox.showerror("Login Gagal", "Username atau Password salah.")
            # Bersihkan password dan focus ke username
            self.entry_password.delete(0, tk.END)
            self.entry_username.focus_set()
            
    def _reset_form_biodata(self):
        """Reset semua field di form biodata"""
        self.var_nama.set("")
        self.var_nim.set("")
        self.var_jurusan.set("")
        self.text_alamat.delete("1.0", tk.END)
        self.var_jk.set("Pria")
        self.var_setuju.set(0)
        self.label_hasil.config(text="")   
        self.var_email.set("")
        self.var_telepon.set("")
        self.var_tgl.set("")
        self.validate_form()  

    def _update_title_with_user(self):
        """Update judul window dengan nama user yang login"""
        if self.current_user:
            self.title(f"Aplikasi Biodata Mahasiswa - User: {self.current_user}")
        else:
            self.title("Aplikasi Biodata Mahasiswa")

    def _terapkan_tema(self, warna):
        """Ganti warna background form biodata"""
        self.frame_biodata.config(bg=warna)
        for frame in (self.frame_biodata, self.frame_input, self.frame_jk):
            for w in frame.winfo_children():
                if isinstance(w, (tk.Frame, tk.Label, tk.Radiobutton, tk.Checkbutton)):
                    w.config(bg=warna)
        self.frame_input.config(bg=warna)
        self.frame_jk.config(bg=warna)
    
    
    def _logout(self):
        """Method untuk logout dan kembali ke halaman login"""
        if messagebox.askyesno("Logout", f"Apakah {self.current_user} yakin ingin logout?"):
            logging.info(f"User logout: {self.current_user}")    # <-- baru
            # Reset status user
            self.current_user = None
            # Hapus menu
            self._hapus_menu()
            # Update title
            self._update_title_with_user()
            # Bersihkan field login
            self.entry_password.delete(0, tk.END)
            if not self.var_ingat.get():
                self.entry_username.delete(0, tk.END)
            # Reset form biodata
            self._reset_form_biodata()
            # Kembali ke halaman login
            self._pindah_ke(self.frame_login)
            # Focus ke username field
            self.entry_username.focus_set()
            self._terapkan_tema("#f0ffff")


    def _buat_menu(self):
        """Membuat menu bar untuk aplikasi"""
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)

        file_menu = tk.Menu(master=menu_bar, tearoff=0)
        file_menu.add_command(label="Simpan Hasil", command=self.simpan_hasil)
        file_menu.add_separator()
        file_menu.add_command(label="Logout", command=self._logout)
        file_menu.add_separator()
        file_menu.add_command(label="Keluar", command=self.keluar_aplikasi)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def _hapus_menu(self):
        """Menghapus menu bar dari window."""
        empty_menu = tk.Menu(self)
        self.config(menu=empty_menu)
        
    def simpan_hasil(self):
        """Simpan hasil biodata ke file dengan error handling"""
        try:
            hasil_tersimpan = self.label_hasil.cget("text")

            if not hasil_tersimpan or "BIODATA TERSIMPAN" not in hasil_tersimpan:
                messagebox.showwarning("Peringatan", "Tidak ada data untuk disimpan. Mohon submit terlebih dahulu.")
                return

            # Buat nama file dengan timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"biodata_{self.current_user}_{timestamp}.txt"

            with open(filename, "w", encoding="utf-8") as file:
                file.write(f"Data disimpan oleh: {self.current_user}\n")
                file.write(f"Waktu penyimpanan: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write("-" * 50 + "\n")
                file.write(hasil_tersimpan)

            messagebox.showinfo("Info", f"Data berhasil disimpan ke file '{filename}'.")

        except PermissionError:
            messagebox.showerror("Error", "Tidak memiliki izin untuk menyimpan file di lokasi ini.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat menyimpan file:\n{str(e)}")
        
    def keluar_aplikasi(self):
        """Keluar dari aplikasi dengan konfirmasi"""
        if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar dari aplikasi?"):
            logging.info(f"Application closed by user: {self.current_user}")
            self.destroy()   
    
    def _toggle_password(self):
        """Tampilkan atau Sembunyikan password"""
        self.entry_password.config(show="" if self.var_tampilan_pw.get() else "*")
    
    def _muat_username(self):
        """Isi username terakhir kalau ada"""
        try:
            with open("remember_me.txt", "r", encoding="utf-8") as f:
                nama = f.read().strip()
            if nama:
                self.entry_username.insert(0, nama)
                self.var_ingat.set(1)
        except FileNotFoundError:
            pass

    def _simpan_username(self, username):
        """Simpan atau hapus username sesuai centang Ingat saya"""
        try:
            if self.var_ingat.get():
                with open("remember_me.txt", "w", encoding="utf-8") as f:
                    f.write(username)
            else:
                import os
                if os.path.exists("remember_me.txt"):
                    os.remove("remember_me.txt")
        except Exception as e:
            logging.error(f"Gagal menyimpan remember me: {e}")
    
    def _konfirmasi_reset(self):
        if messagebox.askyesno("Reset Form", "Kosongkan semua isian?"):
            self._reset_form_biodata()
            self.entry_nama.focus_set()
    
    def _tanggal_valid(self, teks):
        """True kalau format DD-MM-YYYY dan tanggalnya nyata, tidak di masa depan"""
        try:
            tgl = datetime.datetime.strptime(teks, "%d-%m-%Y")
            return datetime.datetime(1900, 1, 1) <= tgl <= datetime.datetime.now()
        except ValueError:
            return False
    
# Blok berikut hanya akan dieksekusi jika file ini dijalankan secara langsung
if __name__ == "__main__":
    # Membuat instance dari kelas aplikasi kita
    app = AplikasiBiodata()
    # Menjalankan mainloop dari instance tersebut
    app.mainloop()