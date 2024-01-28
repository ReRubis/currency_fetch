from webcur.service.exhachanger import ExchangeRatesService
from functools import wraps
from cachetools import TTLCache
import multiprocessing

# TODO: Move queue logic out of the injectors
# Possibly create a queue logic class
data_queue = multiprocessing.Queue()


def timed_lru_cache(seconds):
    """
    Timed LRU cache decorator
    """
    def decorator(func):
        cache = TTLCache(maxsize=1, ttl=seconds)

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            if key in cache:
                result = cache[key]
            else:
                result = func(*args, **kwargs)
                cache[key] = result
            return result

        return wrapper

    return decorator


def data_queue_injector():
    """
    Returns the data queue.
    """
    return data_queue


def data_queue_value_injector():
    """
    Returns the data queue value.
    """
    return _get_queue_value()


def main_service_injector():
    """
    Returns the main service.
    """
    data_queue_value = data_queue_value_injector()
    return ExchangeRatesService(data_queue_value)


@timed_lru_cache(5)
def _get_queue_value():
    """
    Returns the data queue value.
    """
    try:
        front_element = data_queue.get()
        data_queue.put(front_element)
        return front_element
    except Exception:
        # TODO: Add different exceptions
        return None
