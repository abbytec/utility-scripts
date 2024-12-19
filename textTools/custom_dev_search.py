import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys

class SearchApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Buscar textos en archivos")
        self.geometry("600x400")

        self.directory = ''
        self.search_text = ''

        # Verificar si 'pathspec' está instalado
        try:
            import pathspec
            self.pathspec = pathspec
        except ImportError:
            messagebox.showerror("Error", "El módulo 'pathspec' no está instalado. Por favor, instálalo con 'pip install pathspec'.")
            self.destroy()
            return

        self.create_widgets()

    def create_widgets(self):
        # Botón para seleccionar directorio
        self.select_dir_button = tk.Button(self, text="Seleccionar carpeta", command=self.select_directory)
        self.select_dir_button.pack(pady=5)

        # Etiqueta para mostrar el directorio seleccionado
        self.dir_label = tk.Label(self, text="Carpeta seleccionada: Ninguna")
        self.dir_label.pack(pady=5)

        # Entrada para ingresar el texto a buscar
        self.search_label = tk.Label(self, text="Texto a buscar:")
        self.search_label.pack(pady=5)
        self.search_entry = tk.Entry(self, width=50)
        self.search_entry.pack(pady=5)

        # Botón para iniciar la búsqueda
        self.search_button = tk.Button(self, text="Iniciar búsqueda", command=self.start_search)
        self.search_button.pack(pady=5)

        # Widget de texto para mostrar los resultados
        self.results_text = tk.Text(self, wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True)

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory = directory
            self.dir_label.config(text=f"Carpeta seleccionada: {directory}")

    def start_search(self):
        if not self.directory:
            messagebox.showerror("Error", "Por favor, selecciona una carpeta.")
            return

        self.search_text = self.search_entry.get()
        if not self.search_text:
            messagebox.showerror("Error", "Por favor, ingresa el texto a buscar.")
            return

        self.results_text.delete(1.0, tk.END)

        # Leer el archivo de exclusión personalizado
        custom_spec = self.read_custom_ignore_patterns()

        # Iniciar la búsqueda
        for root, dirs, files in os.walk(self.directory, topdown=True):
            # Leer .gitignore en el directorio actual
            gitignore_spec = self.read_gitignore_patterns(root)

            # Combinar patrones de exclusión
            combined_spec = self.combine_specs(custom_spec, gitignore_spec)

            # Modificar 'dirs' in-place para ignorar directorios
            dirs[:] = [d for d in dirs if not self.should_ignore(os.path.join(root, d), combined_spec)]
            for file in files:
                file_path = os.path.join(root, file)
                if not self.should_ignore(file_path, combined_spec):
                    try:
                        with open(file_path, 'r', errors='ignore') as f:
                            content = f.read()
                            if self.search_text in content:
                                self.results_text.insert(tk.END, f"Encontrado en: {file_path}\n")
                    except:
                        pass  # Ignorar archivos que no se pueden abrir
        if self.results_text.get(1.0, tk.END).strip() == '':
            self.results_text.insert(tk.END, "No se encontraron resultados.")

    def should_ignore(self, path, spec):
        rel_path = os.path.relpath(path, self.directory)
        if spec.match_file(rel_path):
            return True
        return False

    def read_gitignore_patterns(self, directory):
        patterns = []
        gitignore_path = os.path.join(directory, '.gitignore')
        if os.path.exists(gitignore_path):
            with open(gitignore_path, 'r') as f:
                gitignore_content = f.read()
            patterns.extend(gitignore_content.splitlines())
        # Crear un objeto PathSpec para los patrones del .gitignore
        spec = self.pathspec.PathSpec.from_lines('gitwildmatch', patterns)
        return spec

    def read_custom_ignore_patterns(self):
        patterns = []

        # Leer archivo de exclusión personalizado (debe llamarse 'custom_ignore.txt')
        custom_ignore_path = os.path.join(os.path.dirname(sys.argv[0]), 'custom_ignore.txt')
        if os.path.exists(custom_ignore_path):
            with open(custom_ignore_path, 'r') as f:
                custom_ignore_content = f.read()
            patterns.extend(custom_ignore_content.splitlines())

        # Crear un objeto PathSpec para los patrones personalizados
        spec = self.pathspec.PathSpec.from_lines('gitwildmatch', patterns)
        return spec

    def combine_specs(self, *specs):
        # Combinar múltiples objetos PathSpec en uno solo
        patterns = []
        for spec in specs:
            patterns.extend(spec.patterns)
        combined_spec = self.pathspec.PathSpec(patterns)
        return combined_spec

if __name__ == '__main__':
    app = SearchApp()
    app.mainloop()
