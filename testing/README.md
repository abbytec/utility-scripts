# Testing

Scripts para experimentar con colas y mensajeria.

- `rabbit_queue_push.py`: Publica un mensaje en RabbitMQ configurando exchange, cola y binding.
- `rabbit_queue_pull.py`: Consume un mensaje de RabbitMQ y cierra la conexion despues del primer evento recibido.

Requiere `pika` y un servidor RabbitMQ accesible.
