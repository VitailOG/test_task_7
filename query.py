from beanie import PydanticObjectId

from db import Statistic


async def statistic_all() -> list[Statistic]:
    return await Statistic.find_all().to_list()


async def get_statistic_by_id(_id: PydanticObjectId) -> Statistic | None:
    return await Statistic.get(_id)
