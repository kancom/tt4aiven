import re
from datetime import datetime
from typing import List

import requests
from dependency_injector.wiring import Provide, inject
from loguru import logger

from webkpi.application import KPI, KPIRepo, RegExpPiece, Scheduler
from webkpi.application.adapter.streamer import StreamerProducer
from webkpi.deps import ProducerContainer as Container


@inject
async def poll_host(
    host: str,
    regexs: List[RegExpPiece],
    streamer: StreamerProducer = Provide[Container.producer],
):
    response = requests.get(url=host)
    event_ts = datetime.utcnow()
    elapsed = response.elapsed
    code = response.status_code
    for regex in regexs:
        regex.is_found = (
            True
            if regex.expression is not None
            and re.search(regex.expression, response.text) is not None
            else False
        )
    kpi = KPI(host=host, timestamp=event_ts, code=code, elapsed=elapsed, regexs=regexs)
    logger.debug(f"kpi created {kpi.dict()}")
    if not streamer.is_started:
        await streamer.start()
    await streamer.push_kpi(kpi)


@inject
async def schedule_tasks(
    repo: KPIRepo = Provide[Container.repo],
    scheduler: Scheduler = Provide[Container.scheduler],
):
    schedules = await repo.read_schedule()
    for schedule in schedules:
        logger.debug(f"adding new schedule {schedule}")
        scheduler.add_job(schedule)
    scheduler.start()
