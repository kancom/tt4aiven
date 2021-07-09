from datetime import datetime, timedelta
from typing import List, Optional

from pydantic import BaseModel, Field


class RegExpPiece(BaseModel):
    expression: Optional[str] = None
    name: str
    is_found: bool = False


class KPI(BaseModel):
    host: str
    timestamp: datetime
    elapsed: timedelta
    code: int = Field(gt=0)
    regexs: List[RegExpPiece] = Field(default_factory=list)

    def dict(self, *args, **kwargs):
        result = super().dict(*args, **kwargs)
        result["timestamp"] = self.timestamp.isoformat()
        result["elapsed"] = self.elapsed.microseconds
        return result


class Schedule(BaseModel):
    host: str
    regexs: List[RegExpPiece] = Field(default_factory=list)
    interval: str
