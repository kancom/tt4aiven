import json
from datetime import timedelta

from dependency_injector.wiring import Provide, inject
from loguru import logger

from webkpi.application import KPI, KPIRepo, RegExpPiece, Scheduler
from webkpi.application.adapter.streamer import StreamerConsumer
from webkpi.deps import ConsumerContainer as Container

tables = [
    """create table IF NOT EXISTS host (
    id serial,
    name varchar(100) NOT NULL
    )""",
    """create table IF NOT EXISTS event (
    id serial,
    host_id integer,
    timestamp timestamp,
    elapsed integer,
    code integer
    )
    """,
    """create table IF NOT EXISTS regex (
    id serial,
    event_id integer,
    name varchar(50),
    is_found boolean
    )
    """,
]


@inject
async def create_db(
    db=Provide[Container.db],
):
    connection = await db.connection()
    cur = await connection.cursor()
    for table in tables:
        await cur.execute(table)
    # ret = await cur.fetchall()


@inject
async def process_messages(
    repo: KPIRepo = Provide[Container.repo],
    streamer: StreamerConsumer = Provide[Container.consumer],
):
    await streamer.start()
    async for msg in streamer:
        msg_str = msg.value.decode("utf-8")
        logger.debug(f"msg received: {msg_str}")
        msg_dict = json.loads(msg_str)
        regexs = []
        for regex in msg_dict["regexs"]:
            regexs.append(RegExpPiece(**regex))
        kpi = KPI(
            host=msg_dict["host"],
            timestamp=msg_dict["timestamp"],
            elapsed=timedelta(microseconds=int(msg_dict["elapsed"])),
            code=msg_dict["code"],
            regexs=regexs,
        )
        event_id = await repo.store_kpi(kpi)
