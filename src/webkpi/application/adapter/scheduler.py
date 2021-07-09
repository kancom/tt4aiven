import abc

from webkpi.application.domain.kpi import Schedule


class Scheduler(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add_job(self, schedule: Schedule):
        """Schedules job"""

    @abc.abstractmethod
    def start(self):
        pass
