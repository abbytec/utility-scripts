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

# Mensaje a enviar
message = 'Hello, RabbitMQ!'

# Conexión a RabbitMQ
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials))
channel = connection.channel()

# Declarar el exchange
channel.exchange_declare(exchange=exchange_name, exchange_type='fanout', durable=True)

# Declarar la cola
channel.queue_declare(queue=queue_name, durable=True)

# Enlazar la cola con el exchange usando la routing key
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)

# Publicar el mensaje
channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=message)
print(f"Mensaje enviado: {message}")

# Cerrar la conexión
connection.close()

