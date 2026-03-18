import time
from decimal import Decimal
from typing import Optional, Dict, Any

import aiohttp

from app.logger_config.setup_log import logger


class DeribitClient:
    """
    Клиент для работы с публичным API криптобиржи Deribit.
    """
    BASE_URL = "https://www.deribit.com/api/v2/public"

    async def get_index_price(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Получает текущую индексную цену для указанного тикера.
        """

        url = f"{self.BASE_URL}/get_index_price"
        params = {"index_name": ticker}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url=url, params=params) as response:
                    response.raise_for_status()

                    data = await response.json()

                    price = data.get("result", {}).get("index_price")

                    if price is None:
                        logger.error(f"Не удалось найти index_price в ответе для {ticker}: {data}")
                        return None  # explicitly

                    return {
                        "price": Decimal(str(price)),
                        "timestamp": int(time.time())
                    }

            except aiohttp.ClientError as error:
                logger.error(f"Сетевая ошибка при запросе к Deribit API для {ticker}: {error}")
                return None

            except Exception as error:
                logger.error(f"Неизвестная ошибка при парсинге цены {ticker}: {error}")
                return None
