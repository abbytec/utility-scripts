import pika

# Configuración de RabbitMQ
rabbitmq_host = '-'
rabbitmq_port = 5672
rabbitmq_user = '-'
rabbitmq_password = '-'

# Configuración de la cola
exchange_name = 'exchange'
routing_key = 'routing-key'
queue_name = 'queue'

# Conexión a RabbitMQ
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials))
channel = connection.channel()

# Declarar la cola con passive=True (si no existe, no la crea)
channel.queue_declare(queue=queue_name, passive=True)
print("Cola declarada.")

# Callback para procesar los mensajes recibidos
def callback(ch, method, properties, body):
    print(f"Mensaje recibido: {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    # Cerrar la conexión después de recibir el mensaje
    connection.close()
    print("Conexión cerrada después de recibir el mensaje.")

# Configurar el consumidor
channel.basic_consume(queue=queue_name, on_message_callback=callback)
print('Esperando mensajes. Presiona Ctrl+C para salir.')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("Consumiendo mensajes interrumpido por el usuario.")
    channel.stop_consuming()

connection.close()
print("Conexión cerrada.")

