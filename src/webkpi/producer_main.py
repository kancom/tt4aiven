import asyncio
import signal

from loguru import logger

import webkpi.producer_tasks as pt
from webkpi.deps import ProducerContainer as Container
from webkpi.settings import FactoryConfig


class Dispatcher:
    def __init__(self):
        conf_class = FactoryConfig()
        config = conf_class()
        container = Container()

        container.config.db_dsn.from_value(config.DB_DSN)

        container.config.schedule_file.from_value(config.SCHEDULE_FILE)

        container.config.stream_uri.from_value(config.STREAM_URI)
        container.config.stream_topic.from_value(config.STREAM_TOPIC)
        container.config.cafile.from_value(config.CA_FILE)
        container.config.certfile.from_value(config.CERT_FILE)
        container.config.keyfile.from_value(config.KEY_FILE)
        container.wire(modules=[pt])

        self.complete = False

    async def start(self):
        asyncio.get_event_loop().add_signal_handler(signal.SIGTERM, self.stop)
        asyncio.get_event_loop().add_signal_handler(signal.SIGINT, self.stop)
        logger.debug("producer service started")

        await pt.schedule_tasks()
        while not self.complete:
            await asyncio.sleep(1)

    def stop(self):
        self.complete = True


if __name__ == "__main__":
    dispatcher = Dispatcher()
    asyncio.run(dispatcher.start())
