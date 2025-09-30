# Statistical Latency Checker

Conjunto de scripts para obtener mediciones de rendimiento desde un dispositivo Android y graficarlas.

- `check-device.sh`: Toma muestras de `top` via ADB durante un minuto y guarda CPU y memoria en `process_stats.csv`.
- `process_stats.csv`: Archivo generado con los datos crudos; se sobreescribe en cada captura.
- `show-data.py`: Analiza el CSV, aplica filtros por CPU y RAM y muestra graficas con matplotlib.

Requisitos: tener `adb`, Python con `pandas` y `matplotlib` instalados.
