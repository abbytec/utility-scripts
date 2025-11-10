import csv
import sys
import re
from collections import defaultdict
from git_api_clients import get_pr_details

# Expresión regular para encontrar módulos bajo la carpeta /apps/
# Busca "apps/" seguido de un nombre de carpeta ([^/]+)
MODULE_REGEX = re.compile(r'^(?:./)?apps/([^/]+)/')

def identify_modules(repo_name, file_list):
    """
    Identifica los módulos afectados por una lista de archivos.
    
    Reglas:
    - Si un archivo está en 'apps/modulo_a/archivo.txt', el módulo es 'repo_name/modulo_a'.
    - Un PR puede afectar a múltiples módulos.
    - Si no se encuentra ningún archivo bajo 'apps/', el módulo es 'repo_name'.
    
    MODIFICADO: Si repo_name es 'owner/repo', se usará solo 'repo'.
    """
    app_modules = set()
    
    # Quitar el 'owner' (ej: sbwebservices) si el repo_name es 'owner/repo'
    # 'sbwebservices/coruscant' -> 'coruscant'
    if '/' in repo_name:
        repo_name_short = repo_name.split('/', 1)[1] 
    else:
        repo_name_short = repo_name
    
    for file_path in file_list:
        match = MODULE_REGEX.search(file_path)
        if match:
            # Captura el primer grupo (el nombre de la subcarpeta)
            module_name = match.group(1)
            # Usar repo_name_short
            app_modules.add(f"{repo_name_short}/{module_name}")
            
    if not app_modules:
        # Si no se encontraron módulos de 'apps', se usa solo el nombre del repo corto
        return {repo_name_short}
        
    return app_modules

def print_list_1(modules_commits):
    """
    Imprime la Lista 1: Módulos con sus commits (nuevo formato).
    """
    print("--- Lista 1: Commits por Módulo ---")
    print("-" * 40)
    
    # Ordenamos por nombre de módulo para una salida consistente
    for module in sorted(modules_commits.keys()):
        print(f"{module}:")
        print(" - Lista de commits:") # NUEVO FORMATO
        
        # modules_commits[module] es una lista de strings de commit ya formateados
        # Usamos un set para asegurarnos de que no haya duplicados si se procesa el mismo PR dos veces
        unique_commits = sorted(list(set(modules_commits[module])))
        
        for commit_str in unique_commits:
            # Añadimos indentación extra
            print(f"  {commit_str}")
        print("") # Espacio entre módulos

def generate_list_2_csv(modules_stories):
    """
    Genera la Lista 2 en un archivo CSV (lista_2.csv).
    Formato: Modulo, "tarea-1\ntarea-2"
    """
    output_filename = "lista_2.csv"
    print(f"\n--- Generando {output_filename} ---")
    
    try:
        with open(output_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Modulo", "Tareas"]) # Escribir el encabezado
            
            # Ordenamos por nombre de módulo
            for module in sorted(modules_stories.keys()):
                
                # modules_stories[module] es un set de tuplas: {('STORY-1', 'qa1'), ('STORY-2', 'qa2')}
                # Extraemos solo las historias (item[0]), las hacemos únicas y las ordenamos
                stories = sorted(list(set(item[0] for item in modules_stories[module])))
                
                # Unimos las historias con salto de línea
                tasks_string = "\n".join(stories)
                
                # Escribimos la fila
                writer.writerow([module, tasks_string])
        
        print(f"Archivo '{output_filename}' generado con éxito.")
    except Exception as e:
        print(f"Error al escribir {output_filename}: {e}")

def print_list_3(modules_stories):
    """
    Imprime la Lista 3: URLs de QA únicas.
    """
    print("\n--- Lista 3: URLs de QA ---")
    print("-" * 40)
    
    qa_urls = set()
    # modules_stories[module] es un set de tuplas: {('STORY-1', 'qa1'), ('STORY-2', 'qa2')}
    for module_data in modules_stories.values():
        for _, qa_url in module_data:
            if qa_url: # Solo añadir si no está vacía
                qa_urls.add(qa_url)
    
    if not qa_urls:
        print("No se encontraron URLs de QA.")
        return

    # Imprimir las URLs únicas, una por línea
    for url in sorted(list(qa_urls)):
        print(url)


def main():
    """
    Función principal del script.
    """
    # Corregimos la sintaxis del operador ternario
    csv_file_path = "pr_list.csv" if len(sys.argv) < 2 else sys.argv[1]
    
    # Usamos defaultdict para inicializar automáticamente listas o sets vacíos
    # modules_commits almacenará: {'repo/app': [' - [sha123] msg1', ' - [sha456] msg2']}
    # modules_stories almacenará: {'repo/app': {('STORY-1', 'http://qa1')}}
    modules_commits = defaultdict(list)
    modules_stories = defaultdict(set)
    
    print(f"Procesando archivo: {csv_file_path}...")
    
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as f:
            # Asumimos que no hay header. Si lo hay, usa csv.DictReader
            reader = csv.reader(f)
            
            for i, row in enumerate(reader):
                # CAMBIO: ahora se esperan 3 columnas
                if len(row) < 3:
                    print(f"Advertencia: Fila {i+1} ignorada (datos incompletos, se esperan 3 columnas: url, historia, qa_url)")
                    continue
                    
                pr_url = row[0].strip()
                story_code = row[1].strip()
                qa_url = row[2].strip() # NUEVA COLUMNA
                
                if not pr_url or not story_code: # qa_url puede estar vacía
                    print(f"Advertencia: Fila {i+1} ignorada (url o historia vacíos)")
                    continue
                
                print(f"  Procesando PR: {pr_url} ({story_code})")
                
                try:
                    # Esta es la función clave que llama a las APIs
                    # Devuelve una estructura de datos estándar
                    details = get_pr_details(pr_url)
                    
                    # Identificamos los módulos afectados por este PR
                    repo_name = details['repo_name']
                    modules = identify_modules(repo_name, details['files'])
                    
                    # Agregamos los datos a nuestros diccionarios
                    for module in modules:
                        # Añadimos el código de historia y la URL de QA al set
                        modules_stories[module].add((story_code, qa_url)) # CAMBIO: guardar tupla
                        
                        # Añadimos todos los commits del PR a la lista de este módulo
                        for commit in details['commits']:
                            # Formateamos el string del commit aquí
                            sha_short = commit['sha'][:7]
                            # Limpiamos el mensaje (quitamos saltos de línea)
                            message_first_line = commit['message'].split('\n')[0].strip()
                            commit_str = f" - [{sha_short}] {message_first_line}"
                            
                            # Añadimos el string formateado
                            modules_commits[module].append(commit_str)
                            
                except Exception as e:
                    print(f"  ERROR al procesar {pr_url}: {e}")
                    # Continuamos con el siguiente PR
            
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo: {csv_file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado al leer el archivo: {e}")
        sys.exit(1)

    # Si no se procesó nada, salimos
    if not modules_commits and not modules_stories:
        print("No se procesaron datos.")
        sys.exit(0)

    # Imprimimos los reportes
    print("\n" + "="*40)
    print("REPORTE FINAL GENERADO")
    print("="*40)
    
    print_list_1(modules_commits)
    generate_list_2_csv(modules_stories) # CAMBIADO
    print_list_3(modules_stories) # AÑADIDO

if __name__ == "__main__":
    main()
