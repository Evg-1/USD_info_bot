import time


def time_track(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        res = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f'функция "{func.__name__}" выполнялась {end_time - start_time:.2f} сек')
        return res

    return wrapper