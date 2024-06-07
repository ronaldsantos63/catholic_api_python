import sys
import os

# Adiciona o caminho da aplicação ao sys.path
sys.path.insert(0, os.path.dirname(__file__))

# Importa a aplicação Flask
from app import app as application  # Supondo que sua aplicação esteja no arquivo app.py
