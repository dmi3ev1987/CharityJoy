from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession


async def invest_donations(return_object, objects, session: AsyncSession):
    for obj in objects:
        money_to_invest = (
            return_object.full_amount - return_object.invested_amount
        )
        money_from_object = obj.full_amount - obj.invested_amount
        if money_from_object <= money_to_invest:
            return_object.invested_amount += money_from_object
            obj.invested_amount += money_from_object
            obj.fully_invested = True
            obj.close_date = datetime.now()
        else:
            return_object.invested_amount += money_to_invest
            obj.invested_amount += money_to_invest
        if return_object.invested_amount == return_object.full_amount:
            return_object.fully_invested = True
            return_object.close_date = datetime.now()
            break

    session.add(return_object)
    await session.commit()
    await session.refresh(return_object)
    return return_object
