import sys
import os
from typing import List, Dict, Any

# Добавляем путь для импорта модулей
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.utils import read_json_file
from src.file_reader import read_csv_file, read_excel_file
from src.processing import filter_by_state, sort_by_date
from src.operations import process_bank_search
from src.external_api import convert_currency
from src.widget import mask_account_card, get_date


def get_user_choice(options: List[str], prompt: str) -> str:
    """
    Получает выбор пользователя из списка вариантов

    Args:
        options: Список доступных вариантов
        prompt: Сообщение для пользователя

    Returns:
        Выбранный вариант
    """
    while True:
        print(prompt)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        try:
            choice = input("Ваш выбор: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(options):
                return options[int(choice) - 1]
            else:
                print("❌ Неверный выбор. Попробуйте снова.\n")
        except (ValueError, KeyboardInterrupt):
            print("\n❌ Неверный ввод. Попробуйте снова.\n")


def get_yes_no_choice(prompt: str) -> bool:
    """
    Получает ответ Да/Нет от пользователя

    Args:
        prompt: Сообщение для пользователя

    Returns:
        True если Да, False если Нет
    """
    while True:
        choice = input(f"{prompt} (Да/Нет): ").strip().lower()
        if choice in ['да', 'д', 'yes', 'y']:
            return True
        elif choice in ['нет', 'н', 'no', 'n']:
            return False
        else:
            print("❌ Пожалуйста, введите 'Да' или 'Нет'\n")


def get_valid_status() -> str:
    """
    Получает валидный статус операции от пользователя

    Returns:
        Валидный статус операции
    """
    valid_statuses = ['EXECUTED', 'CANCELED', 'PENDING']

    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print(f"Доступные для фильтрации статусы: {', '.join(valid_statuses)}")

        status = input("Статус: ").strip().upper()

        if status in valid_statuses:
            return status
        else:
            print(f'❌ Статус операции "{status}" недоступен.\n')


def format_transaction(transaction: Dict[str, Any]) -> str:
    """
    Форматирует транзакцию для красивого вывода

    Args:
        transaction: Словарь с данными о транзакции

    Returns:
        Отформатированная строка с информацией о транзакции
    """
    # Форматируем дату
    date = get_date(transaction['date'])

    # Форматируем отправителя и получателя
    from_account = mask_account_card(transaction.get('from', '')) if transaction.get('from') else ''
    to_account = mask_account_card(transaction.get('to', '')) if transaction.get('to') else ''

    # Получаем сумму в рублях
    amount_rub = convert_currency(transaction)

    # Формируем строку
    result = f"{date} {transaction['description']}\n"

    if from_account and to_account:
        result += f"{from_account} -> {to_account}\n"
    elif to_account:
        result += f"{to_account}\n"

    result += f"Сумма: {amount_rub:.2f} руб.\n"
    result += "-" * 50

    return result


def main():
    """
    Основная функция программы
    """
    print("=" * 60)
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")

    # Выбор типа файла
    file_types = [
        "Получить информацию о транзакциях из JSON-файла",
        "Получить информацию о транзакциях из CSV-файла",
        "Получить информацию о транзакциях из XLSX-файла"
    ]

    file_choice = get_user_choice(file_types, "")

    # Определяем функцию для чтения файла и расширение
    if "JSON" in file_choice:
        read_function = read_json_file
        file_extension = ".json"
        print("\n✅ Для обработки выбран JSON-файл.")
    elif "CSV" in file_choice:
        read_function = read_csv_file
        file_extension = ".csv"
        print("\n✅ Для обработки выбран CSV-файл.")
    else:
        read_function = read_excel_file
        file_extension = ".xlsx"
        print("\n✅ Для обработки выбран XLSX-файл.")

    # Получаем путь к файлу
    file_path = input(
        f"\nВведите путь к {file_extension}-файлу (или нажмите Enter для data/operations{file_extension}): ").strip()
    if not file_path:
        file_path = f"data/operations{file_extension}"

    # Читаем данные
    try:
        transactions = read_function(file_path)
        if not transactions:
            print("❌ Файл пустой или не содержит данных.")
            return
        print(f"✅ Загружено {len(transactions)} транзакций.")
    except Exception as e:
        print(f"❌ Ошибка при чтении файла: {e}")
        return

    # Фильтрация по статусу
    status = get_valid_status()
    filtered_transactions = filter_by_state(transactions, status)
    print(f'✅ Операции отфильтрованы по статусу "{status}"')

    if not filtered_transactions:
        print("❌ Не найдено ни одной транзакции с выбранным статусом.")
        return

    # Сортировка по дате
    if get_yes_no_choice("\nОтсортировать операции по дате?"):
        if get_yes_no_choice("Отсортировать по возрастанию или по убыванию?"):
            sorted_transactions = sort_by_date(filtered_transactions, reverse=False)
            print("✅ Сортировка по возрастанию даты.")
        else:
            sorted_transactions = sort_by_date(filtered_transactions, reverse=True)
            print("✅ Сортировка по убыванию даты.")
    else:
        sorted_transactions = filtered_transactions
        print("✅ Сортировка не применена.")

    # Фильтрация по рублевым транзакциям
    final_transactions = sorted_transactions
    if get_yes_no_choice("\nВыводить только рублевые транзакции?"):
        final_transactions = [t for t in sorted_transactions
                              if t.get('operationAmount', {}).get('currency', {}).get('code') == 'RUB']
        print("✅ Показаны только рублевые транзакции.")

    # Поиск по описанию
    if get_yes_no_choice("\nОтфильтровать список транзакций по определенному слову в описании?"):
        search_word = input("Введите слово для поиска в описании: ").strip()
        if search_word:
            final_transactions = process_bank_search(final_transactions, search_word)
            print(f'✅ Применен поиск по слову "{search_word}".')

    # Вывод результатов
    print("\n" + "=" * 60)
    print("Распечатываю итоговый список транзакций...")
    print("=" * 60)

    if not final_transactions:
        print("❌ Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    print(f"Всего банковских операций в выборке: {len(final_transactions)}\n")

    for transaction in final_transactions:
        print(format_transaction(transaction))
        print()


if __name__ == "__main__":
    main()