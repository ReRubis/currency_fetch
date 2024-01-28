from webcur.database.repository import DataBaseRepository
from webcur.service.external_api.baseapi import BaseAPI
from functools import lru_cache
from typing import Iterable


class ExchangeRatesService():
    """
    This class

    Args:
        - repository: Any class that implements the
        DataBaseRepository interface

        - api: list of any class that implements the
        ExchangeRatesAPI interface
    """

    def __init__(
        self,
        repository: DataBaseRepository,
        api: Iterable[BaseAPI],
    ):
        self.repository = repository
        self.api_list = api

    @lru_cache
    async def return_rates_list(self) -> dict:
        """
        Returns rates for the given pair

        """
        return self.repository.read()

    @lru_cache
    async def return_rates(self, pair_name) -> dict:
        """
        Returns rates for the given pair

        Args:
            pair_name (str): The pair to get the exchange rate for
        """
        return self.repository.read(pair_name)

    async def fetch_data(self) -> None:
        """
        Fetches the data from API and saves it database
        """
        for api in self.api_list:
            rates = api.get_exchange_rates()
            if rates is not None:
                break
        self.repository.write(rates)
