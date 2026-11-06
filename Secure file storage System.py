import os
import base64
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

# ==================== KEY DERIVATION ====================

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

# ==================== ENCRYPTION/DECRYPTION HELPERS ====================

def encrypt_file_with_password(file_path, password):
    try:
        salt = os.urandom(16)
        key = derive_key(password, salt)
        f = Fernet(key)

        with open(file_path, "rb") as file:
            file_data = file.read()

        encrypted_data = f.encrypt(file_data)
        encrypted_file_path = file_path + ".enc"

        with open(encrypted_file_path, "wb") as enc_file:
            enc_file.write(salt + encrypted_data)

        return encrypted_file_path
    except Exception as e:
        return str(e)

def decrypt_file_with_password(file_path, password):
    try:
        with open(file_path, "rb") as file:
            file_data = file.read()

        salt = file_data[:16]
        encrypted_data = file_data[16:]

        key = derive_key(password, salt)
        f = Fernet(key)
        decrypted_data = f.decrypt(encrypted_data)

        decrypted_file_path = "decrypted_" + os.path.basename(file_path).replace(".enc", "")
        with open(decrypted_file_path, "wb") as dec_file:
            dec_file.write(decrypted_data)

        return decrypted_file_path
    except Exception as e:
        return str(e)

# ==================== ENCRYPT FUNCTIONS ====================

def encrypt_multiple_files():
    files = filedialog.askopenfilenames()
    if not files:
        return

    password = simpledialog.askstring("Password", "Enter encryption password:", show="*")
    if not password:
        return

    success = 0
    for file_path in files:
        result = encrypt_file_with_password(file_path, password)
        if os.path.exists(result):
            success += 1

    messagebox.showinfo("Result", f"Encrypted {success}/{len(files)} files.")

def encrypt_folder():
    folder = filedialog.askdirectory()
    if not folder:
        return

    password = simpledialog.askstring("Password", "Enter encryption password:", show="*")
    if not password:
        return

    all_files = [os.path.join(folder, f) for f in os.listdir(folder)
                 if os.path.isfile(os.path.join(folder, f)) and not f.endswith(".enc")]

    success = 0
    for file_path in all_files:
        result = encrypt_file_with_password(file_path, password)
        if os.path.exists(result):
            success += 1

    messagebox.showinfo("Result", f"Encrypted {success}/{len(all_files)} files in folder.")

# ==================== DECRYPT FUNCTIONS ====================

def decrypt_multiple_files():
    files = filedialog.askopenfilenames(filetypes=[("Encrypted Files", "*.enc")])
    if not files:
        return

    password = simpledialog.askstring("Password", "Enter decryption password:", show="*")
    if not password:
        return

    success = 0
    for file_path in files:
        result = decrypt_file_with_password(file_path, password)
        if os.path.exists(result):
            success += 1

    messagebox.showinfo("Result", f"Decrypted {success}/{len(files)} files.")

def decrypt_folder():
    folder = filedialog.askdirectory()
    if not folder:
        return

    password = simpledialog.askstring("Password", "Enter decryption password:", show="*")
    if not password:
        return

    enc_files = [os.path.join(folder, f) for f in os.listdir(folder)
                 if f.endswith(".enc") and os.path.isfile(os.path.join(folder, f))]

    success = 0
    for file_path in enc_files:
        result = decrypt_file_with_password(file_path, password)
        if os.path.exists(result):
            success += 1

    messagebox.showinfo("Result", f"Decrypted {success}/{len(enc_files)} files in folder.")

# ==================== GUI ====================

def create_gui():
    root = tk.Tk()
    root.title("Secure File Storage System (Batch Support)")
    root.geometry("430x400")
    root.resizable(False, False)

    def exit_app():
        print("Exiting...")
        root.destroy()

    tk.Label(root, text="Secure File Storage System", font=("Helvetica", 16, "bold")).pack(pady=20)

    tk.Button(root, text="Encrypt Single File", width=40, command=encrypt_multiple_files).pack(pady=5)
    tk.Button(root, text="Encrypt Folder", width=40, command=encrypt_folder).pack(pady=5)
    tk.Button(root, text="Decrypt File(s)", width=40, command=decrypt_multiple_files).pack(pady=5)
    tk.Button(root, text="Decrypt Folder", width=40, command=decrypt_folder).pack(pady=5)
    tk.Button(root, text="Exit", width=40, command=exit_app).pack(pady=20)

    root.mainloop()

# ==================== MAIN ====================

if __name__ == "__main__":
    create_gui()
