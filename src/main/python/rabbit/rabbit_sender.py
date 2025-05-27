import asyncio
import aio_pika
import json
from src.main.python.ApplicationProperties import ApplicationProperties


class RabbitMQClient:
    def __init__(self):
        self.url = ApplicationProperties.RABBITMQ_URL
        self.queue_name = ApplicationProperties.RABBITMQ_QUEUE
        self.connection = None
        self.channel = None

    async def connect(self):
        """Establece la conexión con RabbitMQ y declara la cola."""
        self.connection = await aio_pika.connect_robust(self.url)
        self.channel = await self.connection.channel()

        # Declaramos la cola
        await self.channel.declare_queue(self.queue_name, durable=True)
        print(f"Conectado a RabbitMQ - Cola: {self.queue_name}")

    async def send_message(self, message: dict):
        """Publica un mensaje en la cola."""
        if not self.channel:
            await self.connect()

        body = json.dumps(message).encode()
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=body),
            routing_key=self.queue_name,
        )
        print(f"Mensaje enviado: {message}")

    async def consume_messages(self, callback):
        """Consume mensajes de la cola y ejecuta el callback."""
        if not self.channel:
            await self.connect()

        queue = await self.channel.get_queue(self.queue_name)
        async for message in queue:
            async with message.process():
                data = json.loads(message.body)
                print(f"Mensaje recibido: {data}")
                await callback(data)

    async def close(self):
        """Cierra la conexión con RabbitMQ."""
        if self.connection:
            await self.connection.close()
            print("Conexión cerrada")


rabbit_client = RabbitMQClient()

