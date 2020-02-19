import xlsxwriter


def get_fio(full_name):
    try:
        return f"{full_name.split(' ')[0]} {full_name.split(' ')[1][0]}. {full_name.split(' ')[2][0]}."
    except IndexError:
        return


def make_event_visitors_table(stud_dict, event_name):
    workbook = xlsxwriter.Workbook(f'./tmp/{event_name}.xlsx')
    worksheet = workbook.add_worksheet(name=event_name)

    cell_format = workbook.add_format({'bold': True, 'align': 'center'})

    col_counter = 1
    row_number_for_quantity = max([len(stud_dict[group]) for group in stud_dict.keys()])

    worksheet.write(0, 0, "Група", cell_format)
    worksheet.write(row_number_for_quantity, 0, "Кількість", cell_format)

    for group, students in sorted(stud_dict.items(), key=lambda key_value: key_value[0]):
        worksheet.write(0, col_counter, group, cell_format)

        col_width = max([len(stud_fio) for stud_fio in students])

        stud_list = stud_dict[group]
        stud_list.sort()

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
    workbook.close()


def make_student_events_table(group_dict, file_name):
    workbook = xlsxwriter.Workbook(f'./tmp/{file_name}.xlsx')

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

