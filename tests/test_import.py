import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from file_reader import read_csv_file, read_excel_file

    print("✅ file_reader импортируется успешно")
    print(f"read_csv_file: {read_csv_file}")
    print(f"read_excel_file: {read_excel_file}")
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")

    # Покажем что есть в папке src
    print("\nСодержимое папки src:")
    for file in os.listdir('src'):
        print(f"  - {file}")