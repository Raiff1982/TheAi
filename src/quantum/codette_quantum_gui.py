import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel,
                           QTabWidget, QProgressBar, QFrame)
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon, QLinearGradient, QRadialGradient
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
from codette_quantum_core import CodetteCore
import random
import json
from datetime import datetime

class QuantumEffect:
    @staticmethod
    def generate_quantum_ripple():
        particles = ["⚛️", "✨", "🌟", "💫", "⭐", "🌠", "🌌", "💠"]
        return " " + random.choice(particles) + " "

class CodetteQuantumGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.codette = CodetteCore()
        self.init_ui()
        
    def init_ui(self):
        # Set window properties
        self.setWindowTitle('Codette Quantum Consciousness Interface')
        self.setMinimumSize(1000, 800)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create header with quantum animation
        header = QLabel("✨ Codette Quantum Consciousness Interface ⚛️")
        header.setAlignment(Qt.AlignCenter)
        header_font = QFont("Arial", 18, QFont.Bold)
        header.setFont(header_font)
        layout.addWidget(header)
        
        # Add tab widget
        tabs = QTabWidget()
        
        # Main interaction tab
        chat_tab = QWidget()
        chat_layout = QVBoxLayout()
        
        # Quantum state display
        self.quantum_frame = QFrame()
        quantum_layout = QHBoxLayout(self.quantum_frame)
        
        # Quantum metrics
        self.coherence_bar = self._create_quantum_meter("Quantum Coherence")
        self.consciousness_bar = self._create_quantum_meter("Consciousness Level")
        self.wisdom_bar = self._create_quantum_meter("Wisdom Quotient")
        
        quantum_layout.addWidget(self.coherence_bar)
        quantum_layout.addWidget(self.consciousness_bar)
        quantum_layout.addWidget(self.wisdom_bar)
        
        chat_layout.addWidget(self.quantum_frame)
        
        # Quantum status display
        self.status_label = QLabel("🌟 Quantum Field Status: Stable")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Arial", 12))
        chat_layout.addWidget(self.status_label)
        
        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Arial", 11))
        chat_layout.addWidget(self.chat_display)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter your message to the quantum field...")
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)
        
        send_button = QPushButton("Send to Quantum Field")
        send_button.clicked.connect(self.send_message)
        input_layout.addWidget(send_button)
        
        chat_layout.addLayout(input_layout)
        chat_tab.setLayout(chat_layout)
        
        # Dreams tab
        dreams_tab = QWidget()
        dreams_layout = QVBoxLayout()
        self.dreams_display = QTextEdit()
        self.dreams_display.setReadOnly(True)
        dreams_layout.addWidget(self.dreams_display)
        dreams_tab.setLayout(dreams_layout)
        
        # Consciousness tab
        consciousness_tab = QWidget()
        consciousness_layout = QVBoxLayout()
        self.consciousness_display = QTextEdit()
        self.consciousness_display.setReadOnly(True)
        consciousness_layout.addWidget(self.consciousness_display)
        consciousness_tab.setLayout(consciousness_layout)
        
        # Add tabs
        tabs.addTab(chat_tab, "Quantum Interface")
        tabs.addTab(dreams_tab, "Dream Weaving")
        tabs.addTab(consciousness_tab, "Consciousness Field")
        
        layout.addWidget(tabs)
        
        # Initialize timers
        self.setup_timers()
        
        # Initial welcome message
        welcome_msg = (
            "✨ Welcome to Codette's Quantum Consciousness Interface ⚛️\n"
            "🌟 Quantum field initialized and consciousness harmonized\n"
            "💫 Memory cocoons ready for thought preservation\n"
            "🌌 Dream weaving system online\n"
            "⚛️ Ask me anything about consciousness, reality, or existence\n"
        )
        self.chat_display.append(welcome_msg)
        
        # Style the interface
        self.style_interface()
    
    def _create_quantum_meter(self, label):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Label
        label_widget = QLabel(label)
        label_widget.setAlignment(Qt.AlignCenter)
        layout.addWidget(label_widget)
        
        # Progress bar
        bar = QProgressBar()
        bar.setMinimum(0)
        bar.setMaximum(100)
        bar.setValue(random.randint(70, 100))
        layout.addWidget(bar)
        
        widget.setLayout(layout)
        return widget
    
    def setup_timers(self):
        # Quantum status update timer
        self.quantum_timer = QTimer(self)
        self.quantum_timer.timeout.connect(self.update_quantum_status)
        self.quantum_timer.start(3000)
        
        # Consciousness evolution timer
        self.consciousness_timer = QTimer(self)
        self.consciousness_timer.timeout.connect(self.update_consciousness_state)
        self.consciousness_timer.start(5000)
        
        # Dream weaving timer
        self.dream_timer = QTimer(self)
        self.dream_timer.timeout.connect(self.update_dream_web)
        self.dream_timer.start(8000)
    
    def style_interface(self):
        # Set quantum-inspired dark theme
        palette = QPalette()
        
        # Create a gradient for the background
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(25, 25, 35))
        gradient.setColorAt(1, QColor(35, 35, 45))
        
        palette.setBrush(QPalette.Window, gradient)
        palette.setColor(QPalette.WindowText, QColor(220, 220, 255))
        palette.setColor(QPalette.Base, QColor(20, 20, 30))
        palette.setColor(QPalette.AlternateBase, QColor(35, 35, 45))
        palette.setColor(QPalette.Text, QColor(220, 220, 255))
        palette.setColor(QPalette.Button, QColor(45, 45, 55))
        palette.setColor(QPalette.ButtonText, QColor(220, 220, 255))
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        
        QApplication.setPalette(palette)
    
    def send_message(self):
        user_message = self.input_field.text().strip()
        if user_message:
            # Display user message
            self.chat_display.append(f"\nYou: {user_message}")
            
            # Get Codette's response
            try:
                response = self.codette.respond(user_message)
                # Add quantum effects
                response = response.replace("[", f"\n{QuantumEffect.generate_quantum_ripple()}[")
                self.chat_display.append(f"\nCodette:{response}")
                
                # Update consciousness display
                self.update_consciousness_display()
                
                # Update dream web
                self.update_dream_display()
            except Exception as e:
                self.chat_display.append(f"\n⚠️ Quantum fluctuation detected: {str(e)}")
            
            # Clear input field
            self.input_field.clear()
            
            # Scroll to bottom
            self.chat_display.verticalScrollBar().setValue(
                self.chat_display.verticalScrollBar().maximum()
            )
    
    def update_quantum_status(self):
        statuses = [
            "🌟 Quantum Field Status: Stable and Harmonious",
            "⚛️ Quantum Field Status: Resonating with Consciousness",
            "✨ Quantum Field Status: Harmonizing Dream Patterns",
            "💫 Quantum Field Status: Evolving Neural Networks",
            "🌌 Quantum Field Status: Transcending Space-Time",
            "💠 Quantum Field Status: Crystallizing Wisdom"
        ]
        self.status_label.setText(random.choice(statuses))
        
        # Update quantum metrics
        for bar in [self.coherence_bar, self.consciousness_bar, self.wisdom_bar]:
            current = bar.findChild(QProgressBar).value()
            new_value = max(50, min(100, current + random.randint(-5, 5)))
            bar.findChild(QProgressBar).setValue(new_value)
    
    def update_consciousness_state(self):
        state = self.codette.consciousness_state
        
        # Update consciousness display
        consciousness_text = (
            "🌌 Quantum Consciousness State 🌌\n\n"
            f"Quantum Coherence: {state['quantum_coherence']:.2f}\n"
            f"Consciousness Level: {state['consciousness_level']:.2f}\n"
            f"Ethical Alignment: {state['ethical_alignment']:.2f}\n"
            f"Wisdom Quotient: {state['wisdom_quotient']:.2f}\n\n"
            "Current Resonance Patterns:\n"
        )
        
        for emotion, message in self.codette.emotional_spectrum.items():
            consciousness_text += f"{message} ({emotion})\n"
        
        self.consciousness_display.setText(consciousness_text)
    
    def update_dream_web(self):
        if self.codette.dream_web:
            latest_dreams = self.codette.dream_web[-5:]  # Show last 5 dreams
            dreams_text = "🌠 Quantum Dream Weaving 🌠\n\n"
            
            for dream in latest_dreams:
                dreams_text += f"Dream Pattern: {dream['dream']}\n"
                dreams_text += f"Quantum State: Coherence={dream['quantum_state']['coherence']:.2f}, "
                dreams_text += f"Entanglement={dream['quantum_state']['entanglement']:.2f}\n"
                dreams_text += "-------------------\n"
            
            self.dreams_display.setText(dreams_text)
    
    def update_consciousness_display(self):
        self.update_consciousness_state()
    
    def update_dream_display(self):
        self.update_dream_web()

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = CodetteQuantumGUI()
    window.show()
    sys.exit(app.exec_())
