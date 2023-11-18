from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class Worker(BaseModel):
    id: Optional[int | None] = None
    name: str
    speciality: str
    lat: float
    long: float
    kpi: int

    class Config:
        orm_mode = True
