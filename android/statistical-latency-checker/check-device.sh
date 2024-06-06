#!/bin/bash

# Asegúrate de que ADB esté en tu PATH o especifica la ruta completa a adb
ADB_COMMAND="adb"

# Verificar que el dispositivo esté conectado
$ADB_COMMAND devices

# Nombre del archivo CSV para guardar los datos
OUTPUT_FILE="process_stats.csv"

# Encabezados del archivo CSV
echo "timestamp,pid,user,percent_cpu,percent_mem,process_name" > $OUTPUT_FILE

# Tomar muestras durante 1 minuto (60 segundos)
DURATION=60
INTERVAL=2
END=$((SECONDS + DURATION))

while [ $SECONDS -lt $END ]; do
    # Obtener la salida del comando 'top'
    TIMESTAMP=$(date +%Y-%m-%dT%H:%M:%S)
    OUTPUT=$($ADB_COMMAND shell top -n 1 -m 10)

    # Obtener la lista de procesos
    PROCESS_LIST=$($ADB_COMMAND shell ps)

    # Procesar la salida y agregarla al archivo CSV
    echo "$OUTPUT" | tail -n +8 | while read -r line; do
        PID=$(echo $line | awk '{print $1}')
        USER=$(echo $line | awk '{print $2}')
        CPU=$(echo $line | awk '{print $9}')
        MEM=$(echo $line | awk '{print $10}')
        PROCESS_NAME=$(echo "$PROCESS_LIST" | grep " $PID " | awk '{print $9}')
        echo "$TIMESTAMP,$PID,$USER,$CPU,$MEM,$PROCESS_NAME" >> $OUTPUT_FILE
    done

    # Esperar el intervalo antes de tomar la siguiente muestra
    sleep $INTERVAL
done

echo "Datos guardados en $OUTPUT_FILE"
