from pathlib import Path

import aiopg
from dependency_injector import containers, providers

from webkpi.infrastructure import (APScheduler, KafkaConsumer, KafkaProducer,
                                   PgKPIRepo)


class Db:
    def __init__(self, db_dsn: str) -> None:
        assert db_dsn is not None
        self.dsn = db_dsn

    async def connection(self) -> aiopg.Connection:
        return await aiopg.connect(dsn=self.dsn)


class ProducerContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    db = providers.Singleton(Db, db_dsn=config.db_dsn)

    repo = providers.Singleton(
        PgKPIRepo,
        db_connection=db.provided.connection.call(),
        schedule_file=config.schedule_file,
    )
    scheduler = providers.Singleton(APScheduler)
    producer = providers.Singleton(
        KafkaProducer,
        kafka_uri=config.stream_uri,
        stream_topic=config.stream_topic,
        cafile=config.cafile,
        certfile=config.certfile,
        keyfile=config.keyfile,
    )


class ConsumerContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    db = providers.Singleton(Db, db_dsn=config.db_dsn)

    repo = providers.Singleton(
        PgKPIRepo,
        db_connection=db.provided.connection.call(),
        schedule_file=config.schedule_file,
    )
    consumer = providers.Singleton(
        KafkaConsumer,
        kafka_uri=config.stream_uri,
        stream_topic=config.stream_topic,
        cafile=config.cafile,
        certfile=config.certfile,
        keyfile=config.keyfile,
    )
