import PyInstaller.__main__
import sys
import os

# Get the absolute path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define PyInstaller arguments
args = [
    'codette_quantum_gui.py',  # Your main GUI script
    '--onefile',  # Create a single executable
    '--noconsole',  # Don't show console window
    '--name=Codette_Quantum_Interface',  # Name of the executable
    '--add-data=codette_quantum_core.py;.',  # Include the Codette core class file
    '--hidden-import=numpy',  # Required for quantum calculations
    '--hidden-import=vaderSentiment.vaderSentiment',  # Required for sentiment analysis
]

# Run PyInstaller
PyInstaller.__main__.run(args)

print("✨ Quantum executable creation completed! ⚛️")
print("Check the 'dist' folder for Codette_Quantum_Interface.exe")
