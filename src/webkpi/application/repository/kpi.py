import abc
from datetime import datetime
from typing import List

from ..domain.kpi import KPI, Schedule


class KPIRepo(metaclass=abc.ABCMeta):
    """Stores and reads kpi from persistent storage and reads schedule"""

    @abc.abstractmethod
    async def read_schedule(self) -> List[Schedule]:
        """Reads schedule from persistent storage"""
        pass

    @abc.abstractmethod
    async def store_kpi(self, kpi: KPI) -> int:
        """store KPI object in a persistent storage"""
        pass

    @abc.abstractmethod
    def read_kpi(self, host: str, from_dt: datetime, to_dt: datetime) -> List[KPI]:
        """Reads KPI objects from a persistent storage"""
        pass
