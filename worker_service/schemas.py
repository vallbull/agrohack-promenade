from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class Worker(BaseModel):
    id: Optional[int | None] = None
    name: str
    speciality: list[str]
    lat: float
    long: float
    kpi: Optional[int] = 0

    class Config:
        orm_mode = True
