from webcur.database.repository import DataBaseRepository


class ExchangeRatesService():
    """
    This class

    Args:
        - repository: Any class that implements the
        DataBaseRepository interface

        - queue_value: The value that is stored in the queue
    """

    def __init__(
        self,
        data_queue_value: dict,
        repository: DataBaseRepository | None = None,
    ):
        self.data_queue = data_queue_value
        self.repository = repository

    async def return_rates_list(self) -> dict:
        """
        Returns all rates in the database
        """

        return {'data': self.data_queue}

    async def return_rate(self, pair_name) -> dict:
        """
        Returns rates for the given pair

        Args:
            pair_name (str): The pair to get the exchange rate for
        """
        return self.data_queue[pair_name]

    # def _peek(self):
    #     """
    #     Peeks at the front element of the multiprocessing.Queue
    #     without removing it.
    #     """
    #     try:
    #         front_element = self.data_queue.get()
    #         self.data_queue.put(front_element)
    #         return front_element
    #     except Exception:
    #         # TODO: Add different exceptions
    #         return None
