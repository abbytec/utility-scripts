import re

def extract_keys(js_content):
    # Esta expresión regular busca claves en el formato 'clave': o clave:
    keys = re.findall(r"[\s{](\w+):\s*{?", js_content)
    return set(keys)

def compare_files(file_a, file_b):
    with open(file_a, 'r') as f:
        content_a = f.read()
    with open(file_b, 'r') as f:
        content_b = f.read()

    keys_a = extract_keys(content_a)
    keys_b = extract_keys(content_b)

    missing_in_b = keys_a - keys_b
    return missing_in_b

# Rutas de los archivos
file_a = '/home/abby/Escritorio/proyectos/../src/i18n/locales/pt-BR.js'
file_b = '/home/abby/Escritorio/proyectos/../src/i18n/locales/es.js'


# Cambia los nombres de archivo según sea necesario
missing_keys = compare_files(file_a, file_b)
print("Claves faltantes en archivo B:", missing_keys)
