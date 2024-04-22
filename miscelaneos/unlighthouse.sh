#!/bin/bash

# Configura las variables
SITE_URL="http://uploy.dev/"
CONFIG_FILE_PATH="./unlighthouse.config.ts"
OUTPUT_PATH="./.output/output.json"
ENDPOINT_URL="http://"

# Ejecuta unlighthouse-ci
npx unlighthouse --site "$SITE_URL" --config-file "$CONFIG_FILE_PATH" --reporter json --output-path "$OUTPUT_PATH"

# Verifica si hay errores y los envía
if [ $? -ne 0 ]; then
    curl -X POST -H "Content-Type: application/json" -H "Host: status-unlighthouse" -d @"$OUTPUT_PATH" "$ENDPOINT_URL"
fi
