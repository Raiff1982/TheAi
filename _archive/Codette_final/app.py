import tkinter as tk
from tkinter import messagebox
import asyncio
import speech_recognition as sr
import pyttsx3
import ollama  # Ensure Llama 3 local execution
from ai_core_ultimate import AICore  # Ensure it matches latest AI Core

class AIApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.ai = AICore()
        self.speech_recognizer = sr.Recognizer()
        self.speech_engine = pyttsx3.init()
        self.title("Codette AI Assistant - Ultimate Edition")
        self.geometry("1200x700")
        self._init_ui()

    def _init_ui(self):
        self.query_entry = tk.Entry(self, width=100)
        self.query_entry.pack(pady=10)
        tk.Button(self, text="Submit", command=self._submit_query).pack()
        self.response_area = tk.Text(self, width=120, height=30)
        self.response_area.pack(pady=10)
        tk.Button(self, text="Voice Input", command=self._listen_voice_command).pack()

    def _submit_query(self):
        query = self.query_entry.get()
        if not query:
            return
        async def process():
            result = await self.ai.generate_response(query, 1)
            self.response_area.insert(tk.END, f"Response: {result['response']}\n\n")
            self._speak_response(result['response'])
        asyncio.run_coroutine_threadsafe(process(), asyncio.get_event_loop())

    def _listen_voice_command(self):
        with sr.Microphone() as source:
            print("Listening for voice command...")
            audio = self.speech_recognizer.listen(source)
            try:
                command = self.speech_recognizer.recognize_google(audio)
                self.query_entry.delete(0, tk.END)
                self.query_entry.insert(0, command)
                self._submit_query()
            except:
                print("Voice command not recognized.")

    def _speak_response(self, response: str):
        self.speech_engine.say(response)
        self.speech_engine.runAndWait()

if __name__ == "__main__":
    app = AIApplication()
    app.mainloop()
