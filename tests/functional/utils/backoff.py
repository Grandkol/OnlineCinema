import time
from functools import wraps
import logging

logger = logging.get_logger("utils_tests")


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10, retries=10):
    """Функция для повторного подключения к базе данных.
        Постоянно увеличивает время ожидания.

    Args:
        start_sleep_time (float, optional): Начальное время ожидания. Defaults to 0.1.
        factor (int, optional): Величина, от которой зависит увеличение ожидания. Defaults to 2.
        border_sleep_time (int, optional): Максимальное время ожидания. Defaults to 10.
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            time_to_sleep = 0
            counter = 0
            while True:
                res_func = func(*args, **kwargs)
                if res_func:
                    return res_func
                time_to_sleep = start_sleep_time * (factor**counter)
                time_to_sleep = min(time_to_sleep, border_sleep_time)
                counter += 1
                logger.info(
                    f"Функция {func.__qualname__} завершилась с ошибкой. Повторяю попытку, жду {time_to_sleep}"
                )
                if counter > retries:
                    logger.info(
                        f"Функция {func.__qualname__} превысила количество попыток ({retries}). Завершено!"
                    )
                    break
                time.sleep(time_to_sleep)

        return inner

    return func_wrapper
