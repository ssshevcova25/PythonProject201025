def filter_by_state(operations: list[dict], state: str = 'EXECUTED') -> list[dict]:
    """Фильтрует операции по статусу"""
    return [op for op in operations if op.get('state') == state]


def sort_by_date(operations: list[dict], reverse: bool = True) -> list[dict]:
    """Сортирует операции по дате"""
    return sorted(operations, key=lambda x: x['date'], reverse=reverse)


# Тесты
if __name__ == "__main__":
    data = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

    print("EXECUTED:", filter_by_state(data))
    print("CANCELED:", filter_by_state(data, 'CANCELED'))
    print("По убыванию:", sort_by_date(data))
    print("По возрастанию:", sort_by_date(data, False))