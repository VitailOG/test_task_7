from datetime import date

from beanie import PydanticObjectId
from fastapi import FastAPI, Body

from events import main
from db import StatisticRequestSchema, Statistic, TotalAdvertisement
from query import statistic_all, get_statistic_by_id

app = FastAPI()


@app.on_event("startup")
async def startup():
    await main()


@app.post('/add')
async def add(data: StatisticRequestSchema):
    s = await Statistic(**data.dict()).insert()
    return {"id": s.id}


@app.post('/stat', response_model=list[TotalAdvertisement])
async def stat(_id: PydanticObjectId = Body(), d: date = Body()):
    statistic = await get_statistic_by_id(_id)
    if statistic is None:
        return {"Error": True}

    res = []
    for i in statistic.data:
        if i.created_at.date() == d:
            res.append(i)
    return res


@app.post('/all')
async def get_statistics():
    return await statistic_all()
