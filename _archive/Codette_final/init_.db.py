import sqlite3
import bcrypt
import tkinter as tk
from tkinter import messagebox

class SecureDatabase:
    def __init__(self, db_path: str = "secure_ai_agix.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    password_hash TEXT
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    query TEXT,
                    response TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
    
    def create_user(self, username: str, password: str):
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password))

    def authenticate(self, username: str, password: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            return result and bcrypt.checkpw(password.encode(), result[0])

class UserAuthApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.db = SecureDatabase()
        self.title("User Authentication")
        self.geometry("400x300")
        self._init_ui()

    def _init_ui(self):
        tk.Label(self, text="Username:").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()
        
        tk.Label(self, text="Password:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()
        
        tk.Button(self, text="Register", command=self._register_user).pack(pady=5)
        tk.Button(self, text="Login", command=self._authenticate_user).pack(pady=5)

    def _register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            self.db.create_user(username, password)
            messagebox.showinfo("Success", "User registered successfully!")
        else:
            messagebox.showerror("Error", "Username and Password cannot be empty!")

    def _authenticate_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.db.authenticate(username, password):
            messagebox.showinfo("Success", "Authentication successful!")
        else:
            messagebox.showerror("Error", "Invalid credentials!")

if __name__ == "__main__":
    app = UserAuthApp()
    app.mainloop()