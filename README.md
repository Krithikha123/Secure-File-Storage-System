**Secure File Storage System : Using Password-based File Encryption** 
- It is a Python desktop application that allows users to encrypt and decrypt files using a password.
- It also supports processing multiple files and entire folders at once.
- It uses Fernet symmetric encryption to encrypt files and PBKDF2HMAC to generate a secure encryption key from a user-provided password.

The application provides a graphical user interface (GUI) using Tkinter for encryption and decryption, allowing users to select:
- individual files
- multiple files, or folders.

**ENCRYPTION PROCESS**
- Select Files or Folder -> Enter Password -> Generate encryption key using PBKDF2HMAC -> Encrypt file using fernet -> Save encrypted file as (.enc)
        
        
**DECRYPTION PROCESS**
- Select Encrypted (.enc) File -> Enter Original Password -> Derive same encryption key using stored salt -> Decrypt using fernet -> Restore Original File Contents


**TECHNOLOGY**
- Python -> Main Programming Language
- Tkinter -> Graphical User Interface
- Cryptography -> File Encryption and Decryption
- Fernet -> Symmetrical Authenticated Encryption
- PBKDF2HMAC -> Derives an encryption key from a password
- SHA-256 -> Hashing Algorithm used in key derivation
- Base64 -> Converts derived key into Fernet Compatible format








