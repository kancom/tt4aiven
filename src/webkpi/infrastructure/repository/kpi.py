import csv
import json
from datetime import datetime
from typing import List

from webkpi.application import KPI, KPIRepo, RegExpPiece, Schedule


class PgKPIRepo(KPIRepo):
    def __init__(self, db_connection, schedule_file: str) -> None:
        self.db_connection = db_connection
        self.schedule_file = schedule_file

    async def read_schedule(self) -> List[Schedule]:
        result = []
        with open(self.schedule_file) as sf:
            reader = csv.DictReader(sf)
            for line in reader:
                regexs = []
                if line["regex"] is not None:
                    for expr in json.loads(line["regex"]):
                        regexs.append(
                            RegExpPiece(name=expr["name"], expression=expr["regex"])
                        )
                result.append(
                    Schedule(
                        host=line["host"], interval=line["interval"], regexs=regexs
                    )
                )

        return result

    async def store_kpi(self, kpi: KPI) -> int:
        """store KPI object in a persistent storage"""
        cur = await self.db_connection.cursor()

        sql = "select id from host where name = %s"
        await cur.execute(sql, (kpi.host,))
        host_id = await cur.fetchone()
        if not host_id:
            sql = """insert into host (name) values (%s) returning id"""
            await cur.execute(sql, (kpi.host,))
            host_id = await cur.fetchone()
        sql = "insert into event (host_id,timestamp, elapsed, code) values (%s, %s, %s, %s) returning id"
        await cur.execute(
            sql,
            (host_id, kpi.timestamp.isoformat(), kpi.elapsed.microseconds, kpi.code),
        )
        event_id = await cur.fetchone()

        sql = "insert into regex (event_id, name, is_found) values (%s, %s, %s)"
        for regex in kpi.regexs:
            await cur.execute(sql, (event_id, regex.name, regex.is_found))

        return event_id

    def read_kpi(self, host: str, from_dt: datetime, to_dt: datetime) -> List[KPI]:
        """Reads KPI objects from a persistent storage"""
        raise NotImplementedError("reading is not implemented")
