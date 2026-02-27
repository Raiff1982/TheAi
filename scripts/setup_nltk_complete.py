import nltk
import ssl
import os

# Create NLTK data directory in the virtual environment
venv_nltk_data = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.venv', 'nltk_data')
os.makedirs(venv_nltk_data, exist_ok=True)
nltk.data.path.append(venv_nltk_data)

# Setup SSL context for downloading
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download all required NLTK data with detailed error handling
resources = [
    'punkt',
    'averaged_perceptron_tagger',
    'wordnet',
    'tagsets'
]

print("Starting NLTK resource downloads...")
for resource in resources:
    try:
        print(f"Downloading {resource}...")
        nltk.download(resource, download_dir=venv_nltk_data, quiet=True)
        print(f"Successfully downloaded {resource}")
    except Exception as e:
        print(f"Error downloading {resource}: {str(e)}")

print("\nNLTK setup completed!")
print(f"NLTK data directory: {venv_nltk_data}")
print("Available resources:", nltk.data.path)
