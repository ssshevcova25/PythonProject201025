import datetime
from typing import Callable, Any, Optional
import functools


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования выполнения функций

    Args:
        filename: Имя файла для записи логов. Если None - вывод в консоль.

    Returns:
        Декорированную функцию
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Формируем базовую информацию
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            func_name = func.__name__

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)

                # Формируем сообщение об успехе
                log_message = f"{timestamp} - {func_name} ok\n"

                # Логируем в файл или консоль
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message)
                else:
                    print(log_message.strip())

                # Возвращаем результат функции
                return result

            except Exception as e:
                # Формируем сообщение об ошибке
                error_message = f"{timestamp} - {func_name} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n"

                # Логируем в файл или консоль
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(error_message)
                else:
                    print(error_message.strip())

                # Пробрасываем исключение дальше
                raise

        return wrapper

    return decorator


# Примеры использования
if __name__ == "__main__":

    @log()
    def add_numbers(a: int, b: int) -> int:
        """Складывает два числа"""
        return a + b


    @log(filename="function_log.txt")
    def multiply_numbers(x: int, y: int) -> int:
        """Умножает два числа"""
        return x * y


    @log()
    def divide_numbers(a: int, b: int) -> float:
        """Делит два числа"""
        return a / b


    # Тестирование успешных операций
    print("Тестирование успешных операций:")
    result1 = add_numbers(5, 3)
    print(f"Результат сложения: {result1}")

    result2 = multiply_numbers(4, 7)
    print(f"Результат умножения: {result2}")

    # Тестирование операции с ошибкой
    print("\nТестирование операции с ошибкой:")
    try:
        divide_numbers(10, 0)
    except Exception as e:
        print(f"Поймано исключение: {e}")