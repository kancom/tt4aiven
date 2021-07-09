import json

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.helpers import create_ssl_context
from loguru import logger
from webkpi.application import KPI, StreamerConsumer, StreamerProducer


class KafkaStreamer:
    def __init__(
        self,
        kafka_uri: str,
        stream_topic: str,
        cafile: str,
        certfile: str,
        keyfile: str,
    ) -> None:
        self.uri = kafka_uri
        self.cafile = cafile
        self.certfile = certfile
        self.keyfile = keyfile
        self.topic = stream_topic
        self.ssl_context = create_ssl_context(
            cafile=self.cafile,
            certfile=self.certfile,
            keyfile=self.keyfile,
        )

        self.started = False


class KafkaConsumer(StreamerConsumer, KafkaStreamer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.uri,
            security_protocol="SSL",
            ssl_context=self.ssl_context,
        )

    async def start(self):
        await super().start()
        await self.consumer.start()

    def __aiter__(self):
        assert self.started
        return self

    async def __anext__(self):
        return await self.consumer.__anext__()

    async def stop(self):
        await super().stop()
        await self.consumer.stop()


class KafkaProducer(StreamerProducer, KafkaStreamer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.uri,
            security_protocol="SSL",
            ssl_context=self.ssl_context,
        )

    async def start(self):
        await super().start()
        await self.producer.start()

    async def push_kpi(self, kpi: KPI):
        assert self.started
        msg_json = json.dumps(kpi.dict())
        logger.debug(f"kafka push {msg_json}")
        await self.producer.send_and_wait(
            topic=self.topic, value=str(msg_json).encode("utf-8"), partition=0
        )

    async def stop(self):
        await super().stop()
        await self.producer.stop()
