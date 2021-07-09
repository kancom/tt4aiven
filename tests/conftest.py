
import pytest
import webkpi.producer_tasks as pt
from webkpi.deps import ProducerContainer
from webkpi.settings import FactoryConfig


@pytest.fixture
def producer_container():
    conf_class = FactoryConfig()
    config = conf_class()
    container = ProducerContainer()
    container.config.db_dsn.from_value(config.DB_DSN)

    container.config.schedule_file.from_value(config.SCHEDULE_FILE)

    container.config.stream_uri.from_value(config.STREAM_URI)
    container.config.stream_topic.from_value(config.STREAM_TOPIC)
    container.config.cafile.from_value(config.CA_FILE)
    container.config.certfile.from_value(config.CERT_FILE)
    container.config.keyfile.from_value(config.KEY_FILE)
    container.wire(modules=[pt])
    return container


@pytest.fixture
def mocked_req(mocker):
    req_mock = mocker.patch("webkpi.producer_tasks.requests", autospec=True)
    return req_mock
