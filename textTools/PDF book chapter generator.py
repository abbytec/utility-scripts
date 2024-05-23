from fpdf import FPDF
import re

class PDFChapterGenerator:
    def __init__(self):
        self.pdf = FPDF(format='A4')
        self.pdf.set_auto_page_break(auto=True, margin=15)

    def crear_pdf(self, titulo, texto):
        # Generar el nombre del archivo a partir del título
        nombre_archivo = re.sub(r'\W+', '_', titulo) + ".pdf"
        
        # Crear la primera página y agregar el título
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=14, style='B')
        self.pdf.multi_cell(0, 10, titulo, align='C')
        self.pdf.ln(8)

        # Agregar el texto del capítulo
        self.pdf.set_font("Arial", size=12)
        self.add_texto(texto)

        # Guardar el PDF
        self.pdf.output(nombre_archivo)

    def add_texto(self, texto):
        # Reemplazar guiones largos y otros caracteres especiales
        texto = texto.replace("—", "-")
        # Dividir el texto en párrafos
        parrafos = texto.split('\n')
        for parrafo in parrafos:
            self.pdf.multi_cell(0, 8, parrafo, align='J')
            self.pdf.ln(2)  # Espacio entre párrafos

""" Ejemplo de uso del módulo
if __name__ == "__main__":
    titulo = "Título del capítulo"
    texto = (
        "Texto del capítulo. Aquí puedes escribir el contenido del capítulo. "
        "El texto debe estar organizado en párrafos bien estructurados, con un buen espacio entre líneas para facilitar la lectura. "
        "Por favor, asegúrate de que todos los elementos del texto se presenten de manera clara y coherente."
    )

    generador = PDFChapterGenerator()
    generador.crear_pdf(titulo, texto) 
"""
