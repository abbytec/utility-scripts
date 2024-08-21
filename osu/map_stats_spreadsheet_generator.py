import os
import zipfile
import pandas as pd
import math

def extract_osz_files(osz_directory, extract_to):
    for file_name in os.listdir(osz_directory):
        if file_name.endswith('.osz'):
            file_path = os.path.join(osz_directory, file_name)
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)

def parse_osu_file(file_path):
    hit_objects = []
    ar = 0
    cs = 0
    in_hit_objects_section = False

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('ApproachRate:'):
                ar = float(line.split(':')[1].strip())
            elif line.startswith('CircleSize:'):
                cs = float(line.split(':')[1].strip())
            elif line == '[HitObjects]':
                in_hit_objects_section = True
            elif in_hit_objects_section and line:
                parts = line.split(',')
                hit_objects.append({
                    'x': int(parts[0]),
                    'y': int(parts[1]),
                    'time': int(parts[2]),
                    'type': int(parts[3]),
                    'object_type': 'circle' if int(parts[3]) & 1 else 'slider' if int(parts[3]) & 2 else 'spinner'
                })
    return hit_objects, ar, cs

def apply_modifiers(ar, cs, mod):
    if mod == 'HR':
        ar = min(10, ar * 1.4)
        cs = min(10, cs * 1.4)
    elif mod == 'DT':
        if ar < 5:
            ar = min(10, ar * 1.5)
        else:
            ar = min(10, 5 + (ar - 5) * 1.5)
    return ar, cs

def calculate_jumps(hit_objects):
    jumps = 0
    for i in range(1, len(hit_objects)):
        distance = ((hit_objects[i]['x'] - hit_objects[i-1]['x']) ** 2 + 
                    (hit_objects[i]['y'] - hit_objects[i-1]['y']) ** 2) ** 0.5
        if distance > 100:
            jumps += 1
    return jumps / len(hit_objects) * 10

def calculate_streams(hit_objects, mod=None):
    streams = 0
    stream_threshold = 200
    if mod == 'DT':
        stream_threshold /= 1.5
    for i in range(1, len(hit_objects)):
        time_diff = hit_objects[i]['time'] - hit_objects[i-1]['time']
        if time_diff < stream_threshold:
            streams += 1
    return streams / len(hit_objects) * 10

def calculate_techniques(hit_objects):
    sliders = sum(1 for obj in hit_objects if obj['object_type'] == 'slider')
    rhythm_variations = 0
    consecutive_hits = 0
    for i in range(1, len(hit_objects) - 1):
        time_diff1 = hit_objects[i]['time'] - hit_objects[i-1]['time']
        time_diff2 = hit_objects[i+1]['time'] - hit_objects[i]['time']
        if (hit_objects[i-1]['object_type'] == 'circle' and hit_objects[i]['object_type'] == 'circle'):
            consecutive_hits += 1
            if abs(time_diff1 - time_diff2) > 20:
                rhythm_variations += 1
    return ((sliders/len(hit_objects)) + (rhythm_variations / consecutive_hits)) * 7.5

def calculate_alt(hit_objects):
    alt_patterns = 0
    for i in range(1, len(hit_objects) - 1):
        angle = calculate_angle(hit_objects[i-1], hit_objects[i], hit_objects[i+1])
        if angle is not None and angle < 90:
            alt_patterns += 1
    return alt_patterns / len(hit_objects) * 10

def calculate_speed(hit_objects, mod=None):
    speed = 0
    threshold = 100
    if mod == 'DT':
        threshold /= 1.5
    for i in range(1, len(hit_objects)):
        time_diff = hit_objects[i]['time'] - hit_objects[i-1]['time']
        if time_diff < threshold:
            speed += 1
    return speed / len(hit_objects) * 10

def calculate_gimmicks(hit_objects, ar, cs):
    gimmicks = 0
    for i in range(1, len(hit_objects) - 1):
        angle = calculate_angle(hit_objects[i-1], hit_objects[i], hit_objects[i+1])
        if (angle is not None and (60 <= angle <= 120 or 240 <= angle <= 300 or 5 <= angle <= 0 or 175 <= angle <= 185)) or angle is None:
            gimmicks += 1
    
    gimmick_score = gimmicks / len(hit_objects) * 10

    # AR and CS bonus multiplier
    ar_multiplier = 1.5 if ar == 1 else (1 if ar >= 9 else (1.5 - 0.0625 * (ar - 1)))
    cs_multiplier = 1.5 if cs == 1 else (1 if cs >= 4 else (1.5 - 0.125 * (cs - 1)))
    
    return gimmick_score * ar_multiplier * cs_multiplier

def calculate_angle(p1, p2, p3):
    a = ((p2['x'] - p1['x']) ** 2 + (p2['y'] - p1['y']) ** 2) ** 0.5
    b = ((p3['x'] - p2['x']) ** 2 + (p3['y'] - p2['y']) ** 2) ** 0.5
    c = ((p3['x'] - p1['x']) ** 2 + (p3['y'] - p1['y']) ** 2) ** 0.5
    if a == 0 or b == 0:
        return None
    try:
        value = (a**2 + b**2 - c**2) / (2 * a * b)
        value = max(-1, min(1, value))  # Ensure value is within [-1, 1]
        angle = math.acos(value)
        return math.degrees(angle)
    except ValueError:
        return None

def classify_map(map_stats, mod):
    categories = []
    if map_stats['Jumps'] > 7:
        categories.append('NM1')
    if map_stats['Streams'] > 7:
        categories.append('NM2')
    if map_stats['Técnicas'] > 7:
        categories.append('NM3')
    if map_stats['Alt'] > 7:
        categories.append('NM4')
    if map_stats['Velocidad'] > 7:
        categories.append('NM5')
    if map_stats['Gimmicks'] > 7:
        categories.append('NM6')
    if mod is None:  # HD categories only apply for NM
        if map_stats['AR'] < 8.1:
            categories.append('HD1')
        if map_stats['Streams'] > 7 or map_stats['Jumps'] > 7:
            categories.append('HD2')
        if map_stats['Técnicas'] > 7:
            categories.append('HD3')
    if map_stats['CS'] > 6 and mod == 'HR':
        categories.append('HR1')
    if (map_stats['Técnicas'] > 7 or map_stats['Jumps'] > 7) and mod == 'HR':
        categories.append('HR2')
    if (map_stats['Streams'] > 7 or map_stats['Velocidad'] > 7) and mod == 'HR':
        categories.append('HR3')
    if map_stats['Jumps'] > 7 and mod == 'DT':
        categories.append('DT1')
    if map_stats['Streams'] > 7 and mod == 'DT':
        categories.append('DT2')
    if map_stats['Técnicas'] > 7 and mod == 'DT':
        categories.append('DT3')
    if (map_stats['Velocidad'] > 7) and mod == 'DT':
        categories.append('DT4')
    if (map_stats['Jumps'] > 7 and mod == 'HR') or (map_stats['Jumps'] <= 7 and 7 < map_stats["AR"] <= 8.1 and mod == 'NM'):
        categories.append('FM1')
    if map_stats['Streams'] > 7 and mod == 'HR':
        categories.append('FM2')
    if map_stats['CS'] > 4.6 and map_stats['AR'] < 8.1 and mod == 'NM':
        categories.append('FM3')
    if map_stats['Técnicas'] > 7 and mod == 'HR':
        categories.append('FM4')
    if not categories:  # Si no hay categorías específicas, asignar TB
        categories.append('TB')
    return categories

# Función para leer los datos de un archivo .osu y calcular los niveles de dificultad
def read_map_data(file_path):
    hit_objects, ar, cs = parse_osu_file(file_path)

    map_stats = {
        'map_id': os.path.basename(file_path),
        'Jumps': calculate_jumps(hit_objects),
        'Streams': calculate_streams(hit_objects),
        'Técnicas': calculate_techniques(hit_objects),
        'Alt': calculate_alt(hit_objects),
        'Velocidad': calculate_speed(hit_objects),
        'Gimmicks': calculate_gimmicks(hit_objects, ar, cs),
        'AR': ar,
        'CS': cs,
    }

    # Aplicar modificadores de mods
    ar_hr, cs_hr = apply_modifiers(ar, cs, 'HR')
    ar_dt, _ = apply_modifiers(ar, cs, 'DT')

    map_stats_hr = map_stats.copy()
    map_stats_hr['AR'] = ar_hr
    map_stats_hr['CS'] = cs_hr
    map_stats_hr['Streams'] = calculate_streams(hit_objects, 'HR')
    map_stats_hr['Velocidad'] = calculate_speed(hit_objects, 'HR')

    map_stats_dt = map_stats.copy()
    map_stats_dt['AR'] = ar_dt
    map_stats_dt['Streams'] = calculate_streams(hit_objects, 'DT')
    map_stats_dt['Velocidad'] = calculate_speed(hit_objects, 'DT')

    # Clasificar mapas para mods
    map_stats['Categorías'] = classify_map(map_stats, None)
    map_stats['Mod'] = 'NM'
    map_stats_hr['Categorías'] = classify_map(map_stats_hr, 'HR')
    map_stats_hr['Mod'] = 'HR'
    map_stats_dt['Categorías'] = classify_map(map_stats_dt, 'DT')
    map_stats_dt['Mod'] = 'DT'

    return map_stats, map_stats_hr, map_stats_dt

# Directorios
osz_directory = '/home/abby/Descargas/drive-download-20240703T010213Z-001'
extract_to = '/home/abby/Descargas/drive-download-20240703T010213Z-001/extracted'
maps_directory = extract_to

# Extraer archivos .osz
extract_osz_files(osz_directory, extract_to)

# Lista para almacenar los resultados
results = []

# Leer todos los archivos .osu en el directorio extraído
for root, _, files in os.walk(maps_directory):
    for file_name in files:
        if file_name.endswith('.osu'):
            file_path = os.path.join(root, file_name)
            map_stats, map_stats_hr, map_stats_dt = read_map_data(file_path)
            results.append(map_stats)
            results.append(map_stats_hr)
            results.append(map_stats_dt)

# Convertir los resultados a un DataFrame y guardarlo en un archivo CSV
df = pd.DataFrame(results)
df['Categorías'] = df['Categorías'].apply(lambda x: ', '.join(x))  # Convertir lista de categorías a cadena

df_grouped = df.groupby('map_id')['Categorías'].apply(lambda x: ', '.join(set(', '.join(x).split(', ')))).reset_index()

df_grouped.to_csv('map_classification.csv', index=False)

print("Clasificación de mapas completada y guardada en map_classification.csv")