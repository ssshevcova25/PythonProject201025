import datetime
from typing import Callable, Any, Optional
import functools


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования выполнения функций
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            func_name = func.__name__

            try:
                result = func(*args, **kwargs)
                log_message = f"{timestamp} - {func_name} ok\n"

                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message)
                else:
                    print(log_message.strip())

                return result

            except Exception as e:
                error_message = f"{timestamp} - {func_name} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n"

                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(error_message)
                else:
                    print(error_message.strip())

                raise

        return wrapper

    return decorator