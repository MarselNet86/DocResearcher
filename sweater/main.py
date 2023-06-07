import openpyxl
import random
from direction import direction_completion
from contract import practice_completion
from concurrent.futures import ThreadPoolExecutor
import os
import zipfile

description = """
______________________________________
______________________________________
______________________________________

Генеральный директор

_______________Е.В.  Дьячков                                            
"""


def read_excel_file(file_path):
    book = openpyxl.open(file_path, read_only=True)
    sheet = book.active
    rows_data = []
    for row in range(2, sheet.max_row + 1):
        row_data = []
        for cell in sheet[row]:
            row_data.append(cell.value)
        rows_data.append(row_data)
    return rows_data


def process_excel_files(file_path):
    rows = read_excel_file(file_path)
    threads = []
    max_threads = 20

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        for row in rows:
            t1 = executor.submit(
                direction_completion,
                str(row[0]),
                row[1],
                row[2],
                row[5],
                row[3],
                row[7],
                row[6],
                row[8]
            )
            threads.append(t1)

            t2 = executor.submit(
                practice_completion,
                row[6],  # Срок практики
                row[7],  # Организация
                row[8],  # Ген. Директор
                row[3],  # Специальность
                str(row[10]),  # Номер телефона
                str(row[11]),  # Факс
                row[13],  # Сайт
                row[14],  # ИНН
                row[15],  # КПП
                row[16],  # ОРГН
                description,
                row[1],
                row[5],
                row[9]
            )
            threads.append(t2)

        for t in threads:
            t.result()

    # Создание архива после обработки папки "Направления"
    zip_filename = create_directions_archive()
    return zip_filename


def create_directions_archive():
    # Путь к папкам "Направления" и "ПП"
    directories = ['students/Направления', 'students/ПП']
    file_id = random.randint(100000, 999999)

    # Создание архива
    zip_filename = f'download/{file_id}_doc.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        # Рекурсивно добавляем все файлы в папках "Направления" и "ПП" в архив
        for directory in directories:
            for root, _, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Используем полный путь от корня архива для сохранения структуры папок
                    arcname = os.path.relpath(file_path)
                    zipf.write(file_path, arcname)
    return file_id



