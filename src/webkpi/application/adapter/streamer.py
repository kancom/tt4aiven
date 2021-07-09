import abc
from abc import abstractmethod

from ..domain.kpi import KPI


class Streamer(metaclass=abc.ABCMeta):
    """Provides kpi transfer"""

    @abstractmethod
    async def start(self):
        self.started = True

    @abstractmethod
    async def stop(self):
        self.started = False

    @property
    def is_started(self):
        return self.started


class StreamerProducer(Streamer):
    @abstractmethod
    async def push_kpi(self, kpi: KPI):
        pass


class StreamerConsumer(Streamer):
    @abstractmethod
    async def __aiter__(self):
        pass

    @abstractmethod
    async def __anext__(self):
        pass
