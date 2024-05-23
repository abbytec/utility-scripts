from fpdf import FPDF
import re

def crear_pdf(titulo, texto):
    # Generar el nombre del archivo a partir del título
    nombre_archivo = re.sub(r'\W+', '_', titulo) + ".pdf"
    
    # Crear un objeto PDF
    pdf = FPDF(format='A4')
    pdf.add_page()

    # Configuración de la fuente
    pdf.set_font("Arial", size=12)

    # Título del capítulo en negrita
    pdf.set_font("Arial", size=14, style='B')
    pdf.multi_cell(0, 10, titulo, align='C')

    # Espacio después del título
    pdf.ln(10)

    # Texto del capítulo justificado
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, texto, align='J')

    # Guardar el PDF
    pdf.output(nombre_archivo)

# Ejemplo de uso del script con placeholders
titulo = "Título del capítulo"
texto = (
    "Texto del capítulo. Aquí puedes escribir el contenido del capítulo. "
    "El texto debe estar organizado en párrafos bien estructurados, con un buen espacio entre líneas para facilitar la lectura. "
    "Por favor, asegúrate de que todos los elementos del texto se presenten de manera clara y coherente."
)

crear_pdf(titulo, texto)
