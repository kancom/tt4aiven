from datetime import timedelta
from unittest.mock import AsyncMock

import pytest
from webkpi.application import RegExpPiece
from webkpi.deps import Db
from webkpi.infrastructure import APScheduler, KafkaProducer
from webkpi.producer_tasks import poll_host


@pytest.mark.asyncio
async def test_produce(mocker, mocked_req, producer_container):
    host = "some"
    regexs = [RegExpPiece(name="reg1", expression="expr1")]
    resp_mock = mocker.patch("requests.Response", autospec=True)
    resp_mock.status_code = 200
    resp_mock.text = "blah-blah"
    resp_mock.elapsed = timedelta(microseconds=1000)
    mocked_req.get.return_value = resp_mock

    db = AsyncMock(Db, autospec=True)
    scheduler = AsyncMock(APScheduler, autospec=True)
    producer = AsyncMock(KafkaProducer, autospec=True)
    with producer_container.db.override(db), producer_container.scheduler.override(
        scheduler
    ), producer_container.producer.override(producer):
        await poll_host(host, regexs)

    producer.push_kpi.assert_called()


@pytest.mark.asyncio
async def test_produce(mocker, mocked_req, producer_container):
    host = "some"
    regexs = [RegExpPiece(name="reg1", expression="expr1")]
    resp_mock = mocker.patch("requests.Response", autospec=True)
    resp_mock.status_code = 200
    resp_mock.text = "blah-blah"
    resp_mock.elapsed = timedelta(microseconds=1000)
    mocked_req.get.return_value = resp_mock

    db = AsyncMock(Db, autospec=True)
    scheduler = AsyncMock(APScheduler, autospec=True)
    producer = AsyncMock(KafkaProducer, autospec=True)
    with producer_container.db.override(db), producer_container.scheduler.override(
        scheduler
    ), producer_container.producer.override(producer):
        await poll_host(host, regexs)

    producer.push_kpi.assert_called()
