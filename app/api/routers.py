from enum import Enum
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query, HTTPException, status

from app.db.database import get_db
from app.db.models import CurrencyPrice
from app.schemas import CurrencyPriceResponse


class TickerEnum(str, Enum):
    btc_usd = "btc_usd"
    eth_usd = "eth_usd"


router = APIRouter(prefix="/prices", tags=["Crypto prices"])


@router.get(
    "/all",
    response_model=List[CurrencyPriceResponse],
    status_code=status.HTTP_200_OK
)
async def get_all_prices(
        ticker: TickerEnum = Query(..., description="Выберите тикер из списка", Examples=["btc_usd", "eth_usd"]),
        limit: int = Query(10, ge=1, le=100, description="Количество записей для вывода"),
        offset: int = Query(0, ge=0, description="Смещение (для пагинации)"),
        session: AsyncSession = Depends(get_db)
):
    """
    Возвращает историю цен для тикера с поддержкой пагинации.
    Сортировка от новых к старым.
    """
    stmt = (
        select(CurrencyPrice)
        .where(CurrencyPrice.ticker == ticker.value)
        .order_by(CurrencyPrice.timestamp.desc())
        .limit(limit=limit)
        .offset(offset=offset)
    )

    result = await session.execute(stmt)
    prices = result.scalars().all()

    return prices


@router.get(
    "/latest",
    response_model=CurrencyPriceResponse,
    status_code=status.HTTP_200_OK
)
async def get_latest_price(
        ticker: TickerEnum = Query(..., description="Выберите тикер из списка"),
        session: AsyncSession = Depends(get_db)
):
    """
    Возвращает самую свежую (последнюю) цену для указанного тикера.
    """
    stmt = (
        select(CurrencyPrice)
        .where(CurrencyPrice.ticker == ticker.value)
        .order_by(CurrencyPrice.timestamp.desc())
        .limit(limit=1)
    )

    result = await session.execute(stmt)
    latest_price = result.scalar_one_or_none()

    if latest_price is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Цены для тикера {ticker.value} пока не найдены. Подождите пару минут."
        )

    return latest_price


# Добавь импорт datetime наверх файла
from datetime import datetime


# ... остальные импорты ...

@router.get(
    "/by-date",
    response_model=CurrencyPriceResponse,
    status_code=status.HTTP_200_OK
)
async def get_price_by_date(
        ticker: TickerEnum = Query(..., description="Выберите тикер из списка"),
        target_date: datetime = Query(
            ...,
            description="Дата и время в формате ISO 8601 (например, 2026-03-19T15:30:00)",
            example="2026-06-27T15:30:00"
        ),
        session: AsyncSession = Depends(get_db)
):
    """
    Возвращает цену для указанного тикера на конкретную дату и время.
    Если точного совпадения нет, вернет ближайшую цену до указанного времени.
    """
    target_timestamp = int(target_date.timestamp())

    stmt = (
        select(CurrencyPrice)
        .where(CurrencyPrice.ticker == ticker.value)
        .where(CurrencyPrice.timestamp <= target_timestamp)
        .order_by(CurrencyPrice.timestamp.desc())
        .limit(1)
    )

    result = await session.execute(stmt)
    price_record = result.scalar_one_or_none()

    if price_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Нет данных для {ticker.value} на момент времени {target_date}"
        )

    return price_record
