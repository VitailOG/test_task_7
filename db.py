import datetime

from pydantic import BaseModel, Field
from beanie import Document


class TotalAdvertisement(BaseModel):
    total: int
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    top_advertisement: list[str] = []


class StatisticRequestSchema(BaseModel):
    region: str
    phrase: str


class Statistic(StatisticRequestSchema, Document):
    data: list[TotalAdvertisement] = []

    class Settings:
        name = "statistic"
