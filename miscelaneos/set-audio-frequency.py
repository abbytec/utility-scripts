import tkinter as tk
from tkinter import ttk
import re

# Ruta del archivo PipeWire config
config_file_path = '/usr/share/pipewire/pipewire.conf'

def parse_pipewire_config():
    allowed_rates = []
    current_rate = None

    # Expresiones regulares para extraer valores ignorando espacios/tabs
    allowed_rates_pattern = re.compile(r'default\.clock\.allowed-rates\s*=\s*\[(.*)\]')
    current_rate_pattern = re.compile(r'default\.clock\.rate\s*=\s*(\d+)')

    with open(config_file_path, 'r') as file:
        for line in file:
            line = line.strip()
            allowed_match = allowed_rates_pattern.search(line)
            rate_match = current_rate_pattern.search(line)

            if allowed_match:
                # Extraer las frecuencias permitidas
                rates = allowed_match.group(1).strip()
                allowed_rates = [rate.strip() for rate in rates.split(',')]
            elif rate_match:
                # Extraer la frecuencia actual
                current_rate = rate_match.group(1).strip()
    
    return allowed_rates, current_rate

def save_new_rate(new_rate):
    # Leer archivo de configuración
    with open(config_file_path, 'r') as file:
        lines = file.readlines()

    # Reemplazar la línea con la nueva frecuencia
    with open(config_file_path, 'w') as file:
        for line in lines:
            if re.search(r'default\.clock\.rate\s*=', line):
                file.write(f'default.clock.rate = {new_rate}\n')
            else:
                file.write(line)

    # Informar al usuario
    result_label.config(text=f'Frecuencia de muestreo cambiada a {new_rate} Hz')

def on_select(event):
    selected_rate = rate_var.get()
    save_new_rate(selected_rate)

# Crear ventana principal
root = tk.Tk()
root.title('Seleccionar Frecuencia de Muestreo (PipeWire)')

# Cargar configuraciones
allowed_rates, current_rate = parse_pipewire_config()

# Variable para almacenar la selección del dropdown
rate_var = tk.StringVar(value=current_rate)

# Crear dropdown con las opciones de frecuencia de muestreo
rate_label = ttk.Label(root, text="Selecciona la frecuencia de muestreo:")
rate_label.pack(pady=10)

rate_dropdown = ttk.Combobox(root, textvariable=rate_var, values=allowed_rates)
rate_dropdown.pack(pady=10)

# Etiqueta para mostrar el resultado
result_label = ttk.Label(root, text=f'Frecuencia actual: {current_rate} Hz')
result_label.pack(pady=10)

# Detectar selección
rate_dropdown.bind("<<ComboboxSelected>>", on_select)

# Ejecutar la ventana
root.mainloop()

