from webkpi.application import Schedule, Scheduler

from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


class APScheduler(Scheduler):
    misfire_time = 9999

    def __init__(self) -> None:
        jobstores = {"default": MemoryJobStore()}
        executors = {"default": AsyncIOExecutor()}
        job_defaults = {"coalesce": False, "max_instances": 3}
        self._scheduler = AsyncIOScheduler(
            jobstores=jobstores, executors=executors, job_defaults=job_defaults
        )

    def add_job(self, schedule: Schedule):
        """Schedules job"""
        self._scheduler.add_job(
            "webkpi.producer_tasks:poll_host",
            CronTrigger.from_crontab(schedule.interval),
            kwargs={"host": schedule.host, "regexs": schedule.regexs},
            misfire_grace_time=self.misfire_time,
            replace_existing=True,
        )

    def start(self):
        """Start scheduler."""
        if not self._scheduler.running:
            self._scheduler.start()
