# gui.py
import tkinter as tk
from tkinter import scrolledtext, messagebox
from threading import Thread
import asyncio
import sqlite3
from ai_core_system import AICoreSystem

class AIApplication(tk.Tk):
    """Enhanced GUI with async integration"""
    def __init__(self):
        super().__init__()
        self.ai = AICoreSystem()
        self.title("Advanced AI Assistant")
        self._init_ui()
        self._start_event_loop()

    def _init_ui(self):
        """Initialize user interface components"""
        self.geometry("800x600")
        
        # Authentication Frame
        self.auth_frame = tk.Frame(self)
        self.auth_frame.pack(pady=10)
        tk.Label(self.auth_frame, text="Username:").grid(row=0, column=0)
        self.username = tk.Entry(self.auth_frame, width=30)
        self.username.grid(row=0, column=1)
        tk.Label(self.auth_frame, text="Password:").grid(row=1, column=0)
        self.password = tk.Entry(self.auth_frame, show="*", width=30)
        self.password.grid(row=1, column=1)
        tk.Button(self.auth_frame, text="Login", command=self._login).grid(row=0, column=2)
        tk.Button(self.auth_frame, text="Register", command=self._register).grid(row=1, column=2)

        # Query Interface
        self.query_entry = tk.Entry(self, width=80)
        self.query_entry.pack(pady=10)
        tk.Button(self, text="Submit", command=self._submit_query).pack()

        # Response Display
        self.response_area = scrolledtext.ScrolledText(self, width=100, height=25)
        self.response_area.pack(pady=10)

        # Status Bar
        self.status = tk.Label(self, text="System Ready", bd=1, relief=tk.SUNKEN)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def _start_event_loop(self):
        """Initialize async event processing"""
        self.loop = asyncio.new_event_loop()
        Thread(target=self._run_async_tasks, daemon=True).start()

    def _run_async_tasks(self):
        """Run async tasks in background thread"""
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def _login(self):
        """Handle user login"""
        username = self.username.get()
        password = self.password.get()
        if self.ai.db.authenticate(username, password):
            self.status.config(text=f"Logged in as {username}")
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def _register(self):
        """Handle user registration"""
        username = self.username.get()
        password = self.password.get()
        try:
            self.ai.db.create_user(username, password)
            messagebox.showinfo("Success", "Registration complete")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")

    def _submit_query(self):
        """Handle query submission"""
        query = self.query_entry.get()
        if not query:
            return
            
        async def process():
            result = await self.ai.process_query(query, self.username.get())
            self.response_area.insert(tk.END, f"Response: {result.get('response', '')}\n\n")
            self.status.config(text=f"Security Level: {result.get('security', 0)}")

        asyncio.run_coroutine_threadsafe(process(), self.loop)

    def on_closing(self):
        """Clean shutdown handler"""
        self.ai.running = False
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.destroy()

if __name__ == "__main__":
    app = AIApplication()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
