import pandas as pd
import matplotlib.pyplot as plt

# Configuración de los umbrales
CPU_THRESHOLD = 11.0  # porcentaje mínimo de uso promedio de CPU
MEM_THRESHOLD = 6.0  # porcentaje mínimo de uso promedio de memoria

# Leer el archivo CSV
df = pd.read_csv("process_stats.csv")

# Filtrar filas que no coinciden con el formato esperado
df = df[df['timestamp'].apply(lambda x: isinstance(x, str) and 'T' in x)]

# Convertir la columna de timestamp a tipo datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Eliminar filas con fechas inválidas
df = df.dropna(subset=['timestamp'])

# Convertir las columnas de uso de CPU y memoria a numéricas
df['percent_cpu'] = pd.to_numeric(df['percent_cpu'], errors='coerce')
df['percent_mem'] = pd.to_numeric(df['percent_mem'], errors='coerce')

# Eliminar filas con valores NaN en percent_cpu o percent_mem
df = df.dropna(subset=['percent_cpu', 'percent_mem'])

# Convertir la columna PID a numérica
df['pid'] = pd.to_numeric(df['pid'], errors='coerce')

# Eliminar filas con PID NaN
df = df.dropna(subset=['pid'])

# Convertir PID a enteros
df['pid'] = df['pid'].astype(int)

# Asegurarse de que 'process_name' sea una cadena
df['process_name'] = df['process_name'].astype(str)

# Agrupar por proceso (PID) y calcular estadísticas
grouped = df.groupby(['pid', 'process_name']).agg({
    'percent_cpu': ['mean', 'max'],
    'percent_mem': ['mean', 'max']
}).reset_index()

# Simplificar los nombres de las columnas
grouped.columns = ['pid', 'process_name', 'cpu_mean', 'cpu_max', 'mem_mean', 'mem_max']

# Filtrar procesos según el umbral de CPU
filtered_grouped_cpu = grouped[grouped['cpu_mean'] >= CPU_THRESHOLD]

# Filtrar procesos según el umbral de memoria
filtered_grouped_mem = grouped[grouped['mem_mean'] >= MEM_THRESHOLD]

# Mostrar las estadísticas filtradas por CPU
print("Procesos filtrados por CPU:")
print(filtered_grouped_cpu)

# Mostrar las estadísticas filtradas por memoria
print("Procesos filtrados por Memoria:")
print(filtered_grouped_mem)

# Graficar el uso de CPU de los procesos a lo largo del tiempo que cumplen el umbral de CPU
plt.figure(figsize=(14, 7))
for _, row in filtered_grouped_cpu.iterrows():
    pid = row['pid']  # Asegurar que pid sea un entero
    process_name = row['process_name'].split(":")[0]  # Limpiar el nombre del proceso
    subset = df[df['pid'] == pid]
    plt.plot(subset['timestamp'], subset['percent_cpu'], label=f'PID {pid} ({process_name})')

plt.xlabel('Time')
plt.ylabel('CPU Usage (%)')
plt.title('CPU Usage Over Time (Filtered by CPU Threshold)')
plt.legend()
plt.show()

# Graficar el uso de memoria de los procesos a lo largo del tiempo que cumplen el umbral de memoria
plt.figure(figsize=(14, 7))
for _, row in filtered_grouped_mem.iterrows():
    pid = row['pid']  # Asegurar que pid sea un entero
    process_name = row['process_name'].split(":")[0]  # Limpiar el nombre del proceso
    subset = df[df['pid'] == pid]
    plt.plot(subset['timestamp'], subset['percent_mem'], label=f'PID {pid} ({process_name})')

plt.xlabel('Time')
plt.ylabel('Memory Usage (%)')
plt.title('Memory Usage Over Time (Filtered by Memory Threshold)')
plt.legend()
plt.show()
