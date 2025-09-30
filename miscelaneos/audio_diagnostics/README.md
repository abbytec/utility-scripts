# Audio Diagnostics

Scripts para monitorear eventos de audio en entornos PipeWire.

- `audio-watch-pro.sh`: Vigila cambios de volumen en el sink por defecto y loguea streams de salida nuevos o removidos, con notificaciones.
- `communication-watch.sh`: Detecta nodos PipeWire con rol `communication` y avisa cuando aparecen o desaparecen.
- `hdmi-audio-diag.sh`: Recolecta diagnostico extendido para sinks HDMI, incluyendo `dmesg`, volumen y metadatos de nodos.

Requisitos: `pw-dump`, `jq`, `wpctl`, `notify-send` y herramientas basicas de GNU/Linux.
