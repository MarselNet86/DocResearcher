from docx import Document
from docx.shared import Pt

# Краткая хар-ка про СП
unit = '4'
departament = 'Энергетическое отделение'
director_of_sp = 'А.Н. Ниматов'


def direction_completion(direction, stock_full_name, birthday, type_of_practice, specialization, acceptance, practice_period, director_of_practice):
    # Открываем документ
    doc = Document('docs_templates/direction_template.docx')
    # Выбираем параграф и добавляем текст
    par_1 = doc.paragraphs[7]
    run_1 = par_1.add_run(unit)
    run_1.font.size = Pt(12)

    # Выбираем параграф и добавляем текст
    par_2 = doc.paragraphs[8]
    run_2 = par_2.add_run(f'({departament})')
    run_2.font.size = Pt(12)

    # Выбираем параграф и добавляем текст
    par_3 = doc.paragraphs[11]
    run_3 = par_3.add_run(direction)
    run_3.bold = True
    run_3.font.size = Pt(14)

    # Выбираем параграф и добавляем текст
    par_4 = doc.paragraphs[13]
    run_4 = par_4.add_run(stock_full_name)
    run_4.underline = True
    run_4.font.size = Pt(14)

    # Выбираем параграф и добавляем текст
    par_5 = doc.paragraphs[14]
    run_5 = par_5.add_run(birthday)
    run_5.underline = True
    run_5.font.size = Pt(14)

    # Выбираем параграф и добавляем текст
    par_6 = doc.paragraphs[17]
    par_6.add_run(unit).underline = True

    # Выбираем параграф и добавляем текст
    par_7 = doc.paragraphs[21]
    par_7.add_run(type_of_practice).underline = True

    # Выбираем параграф и добавляем текст
    par_8 = doc.paragraphs[24]
    par_8.add_run(specialization).underline = True

    # Выбираем параграф и добавляем текст
    par_9 = doc.paragraphs[27]
    par_9.add_run(acceptance).underline = True

    # Выбираем параграф и добавляем текст
    par_10 = doc.paragraphs[29]
    date = practice_period.split('-')
    text = f'Сроки практики с «{date[0]}» по «{date[1]}»'
    par_10.add_run(text)

    # Выбираем параграф и добавляем текст
    par_11 = doc.paragraphs[32]
    par_11.add_run(director_of_practice)

    # Выбираем параграф и добавляем текст
    par_12 = doc.paragraphs[36]
    par_12.add_run(director_of_sp)

    full_name = stock_full_name.split()
    production_practice = type_of_practice.split()
    data_to_save = f'{full_name[0]} {full_name[1][0]}{full_name[2][0]} напр {production_practice[0]}'
    doc.save(f'students/Направления/{data_to_save}.docx')
