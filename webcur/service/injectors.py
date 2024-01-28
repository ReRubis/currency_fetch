from webcur.service.exhachanger import ExchangeRatesService
import multiprocessing

data_queue = multiprocessing.Queue()


def data_queue_injector():
    """
    Returns the data queue
    """
    return data_queue


def main_service_injector():
    """
    Returns the main service
    """
    return ExchangeRatesService(data_queue)
