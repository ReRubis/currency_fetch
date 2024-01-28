from webcur.database.repository import DataBaseRepository
from functools import lru_cache
import multiprocessing


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
        data_queue: multiprocessing.Queue,
        repository: DataBaseRepository | None = None,
    ):
        self.data_queue = data_queue
        self.repository = repository

    @lru_cache
    async def return_rates_list(self) -> dict:
        """
        Returns all rates in the database
        """
        data = self._peek()
        return {'data': data}

    @lru_cache
    async def return_rate(self, pair_name) -> dict:
        """
        Returns rates for the given pair

        Args:
            pair_name (str): The pair to get the exchange rate for
        """
        data = self._peek()
        return data[pair_name]

    def _peek(self):
        """
        Peeks at the front element of the multiprocessing.Queue
        without removing it.
        """
        try:
            front_element = self.data_queue.get_nowait()
            self.data_queue.put_nowait(front_element)
            return front_element
        except Exception:
            # TODO: Add different exceptions
            return None
