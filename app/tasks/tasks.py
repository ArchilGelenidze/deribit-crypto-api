import asyncio

from app.tasks.celery_app import celery_app
from app.services.deribit import DeribitClient
from app.db.database import async_session_maker, engine
from app.db.models import CurrencyPrice
from app.logger_config.setup_log import logger


async def fetch_and_save_prices():
    client = DeribitClient()

    async_tasks = [asyncio.create_task(client.get_index_price(ticker=ticker)) for ticker in client.NEEDED_CRYPTO]
    data = await asyncio.gather(*async_tasks)

    async with async_session_maker() as session:
        try:
            for crypto in data:
                if not crypto:
                    logger.warning("Пропущено сохранение: нет данных от биржи")
                    continue

                one_record = CurrencyPrice(
                    ticker=crypto.get("ticker"),
                    price=crypto.get("price"),
                    timestamp=crypto.get("timestamp")
                )

                session.add(one_record)

            await session.commit()
            logger.success("Успешно сохранили свежие цены в БД!")

        except Exception as error:
            await session.rollback()
            logger.error(f"Ошибка при сохранении в БД: {error}")

        finally:
            await engine.dispose()


@celery_app.task(name="update_crypto_prices_task")
def update_crypto_prices():
    asyncio.run(fetch_and_save_prices())
