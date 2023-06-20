import openpyxl
import random
from direction import direction_completion
from contract import practice_completion
from concurrent.futures import ThreadPoolExecutor
import os
import zipfile


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
    try:
        rows = read_excel_file(file_path)
        futures = []
        max_processes = 20

        with ThreadPoolExecutor(max_workers=max_processes) as executor:
            for row in rows:
                futures.append(executor.submit(direction_completion, row))
                futures.append(executor.submit(practice_completion, row))

            for future in futures:
                future.result()

        # Создание архива после обработки папки "Направления"
        zip_filename = create_directions_archive(rows)
        return zip_filename
    except (IndexError, AttributeError) as e: # обрабатываем ошибки IndexError и AttributeError
        raise e # переопределяем ошибку для последующего отлова в декораторе



def create_directions_archive(rows):
    directories = ['students/Направления', 'students/ПП']
    file_id = random.randint(100000, 999999)

    zip_filename = f'download/{str(rows[0][0])}_{file_id}_doc.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for directory in directories:
            for root, _, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path)
                    zipf.write(file_path, arcname)
    return file_id, str(rows[0][0]) # возвращаем имя файла и значение группы



