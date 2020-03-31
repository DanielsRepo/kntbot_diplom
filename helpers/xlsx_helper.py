import xlsxwriter
from pprint import pprint


def get_fio(full_name):
    try:
        return f"{full_name.split(' ')[0]} {full_name.split(' ')[1][0]}. {full_name.split(' ')[2][0]}."
    except IndexError:
        return


def make_event_visitors_table(stud_dict, otherfac_list, event_name, file_path):
    workbook = xlsxwriter.Workbook(f'{file_path}{event_name}.xlsx')
    worksheet = workbook.add_worksheet(name=event_name)

    cell_format = workbook.add_format({'bold': True, 'align': 'center'})

    col_counter = 1
    row_number_for_quantity = max([len(stud_dict[group]) for group in stud_dict.keys()]) + 1

    worksheet.write(0, 0, "Група", cell_format)
    worksheet.write(row_number_for_quantity, 0, "Кількість", cell_format)

    for group, students in sorted(stud_dict.items(), key=lambda key_value: key_value[0]):
        worksheet.write(0, col_counter, group, cell_format)

        stud_list = stud_dict[group]
        stud_list.sort()

        col_width = max([len(stud_fio) for stud_fio in stud_list]) + 2

        for i in range(len(stud_list)):
            worksheet.set_column(i + 1, col_counter, col_width)
            worksheet.write(i + 1, col_counter, stud_list[i])

        worksheet.write(row_number_for_quantity, col_counter, len(stud_list))

        col_counter += 1

    chart = workbook.add_chart({'type': 'column'})
    chart.add_series({
        'categories': [f'{worksheet.name}', 0, 1, 0, len(stud_dict.keys())],
        'values':  [f'{worksheet.name}', row_number_for_quantity, 1, row_number_for_quantity, len(stud_dict.keys())]
    })
    chart.set_style(37)
    chart.set_title({'name': 'Гістограма кількості учасників заходу за групами',
                     'name_font': {'name': 'Calibri', 'size': 13}})
    chart.set_legend({'none': True})

    worksheet.insert_chart(f'B{row_number_for_quantity+3}', chart)

    worksheet.write(row_number_for_quantity+2, 0, "Учасники з інших факультетів:", workbook.add_format({'bold': True}))

    for i in range(len(otherfac_list)):
        worksheet.write(i+row_number_for_quantity+3, 0, otherfac_list[i])

    workbook.close()


def make_student_events_table(group_dict, file_name, file_path):
    workbook = xlsxwriter.Workbook(f'{file_path}{file_name}.xlsx')

    cell_format = workbook.add_format({'bold': True, 'align': 'center'})

    for group, stud_dict in sorted(group_dict.items(), key=lambda key_value: key_value[0]):
        worksheet = workbook.add_worksheet(name=f'КНТ-{group}')

        row_counter = 0

        worksheet.write(0, 0, f'КНТ-{group}', cell_format)
        worksheet.write(0, 1, 'Заходи, які відвідував', cell_format)

        first_col_width = max([len(stud_fio) for stud_fio in stud_dict.keys()])
        second_col_width = max([len(', '.join(stud_dict[student])) for student, events in stud_dict.items()])

        for student, events in sorted(stud_dict.items(), key=lambda key_value: key_value[0]):
            worksheet.set_column(row_counter + 1, 0, first_col_width)
            worksheet.write(row_counter + 1, 0, student)

            event_list = ', '.join(events)

            worksheet.set_column(row_counter + 1, 1, second_col_width)
            worksheet.write(row_counter + 1, 1, event_list)

            row_counter += 1

    workbook.close()


def make_student_grades_table(stud_dict, file_name, file_path):
    workbook = xlsxwriter.Workbook(f'{file_path}{file_name}.xlsx')

    cell_format = workbook.add_format({'bold': True, 'align': 'center'})

    worksheet = workbook.add_worksheet(name=f'Рейтинг успішності студентів')

    first_col_width = 30
    other_col_width = 10

    worksheet.write(0, 0, f'П.І.Б', cell_format)
    worksheet.write(0, 1, f'5б', cell_format)
    worksheet.write(0, 2, f'100б', cell_format)
    worksheet.write(0, 3, f'Дод. бал', cell_format)
    worksheet.write(0, 4, f'Група', cell_format)

    row_counter = 0

    for student, score in sorted(stud_dict.items(), key=lambda value: value[1][0], reverse=True):
        worksheet.set_column(row_counter + 1, 0, first_col_width)
        worksheet.write(row_counter + 1, 0, student.split('_')[0])

        worksheet.set_column(row_counter + 1, 1, other_col_width)
        worksheet.write(row_counter + 1, 1, score[0])

        worksheet.set_column(row_counter + 1, 2, other_col_width)
        worksheet.write(row_counter + 1, 2, score[1])

        worksheet.set_column(row_counter + 1, 3, other_col_width)
        worksheet.write(row_counter + 1, 3, score[2])

        worksheet.set_column(row_counter + 1, 4, other_col_width)
        worksheet.write(row_counter + 1, 4, f'КНТ-{student.split("_")[1]}')

        row_counter += 1

    workbook.close()
