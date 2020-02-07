from functools import wraps


def get_fio(s):
    try:
        return f"{s.split(' ')[0]} {s.split(' ')[1][0]}. {s.split(' ')[2][0]}."
    except IndexError:
        return


def make_student_events_table(stud_dict, group, worksheet, workbook):
    row_counter = 0

    worksheet.write(0, 0, f'КНТ-{group}', workbook.add_format({'bold': True, 'align': 'center'}))
    worksheet.write(0, 1, 'Заходи', workbook.add_format({'bold': True, 'align': 'center'}))

    first_col_width = max([len(stud_fio) for stud_fio in stud_dict.keys()])
    second_col_width = max([len(', '.join(stud_dict[student])) for student, events in stud_dict.items()])

    for student, events in sorted(stud_dict.items(), key=lambda key_value: key_value[0]):
        worksheet.set_column(row_counter + 1, 0, first_col_width)
        worksheet.write(row_counter + 1, 0, student)

        event_list = ', '.join(events)

        worksheet.set_column(row_counter + 1, 1, second_col_width)
        worksheet.write(row_counter + 1, 1, event_list)

        row_counter += 1


def make_event_visitors_table(stud_dict, worksheet, workbook):
    col_counter = 0

    for group, students in sorted(stud_dict.items(), key=lambda key_value: key_value[0]):
        worksheet.write(0, col_counter, group, workbook.add_format({'bold': True, 'align': 'center'}))

        col_width = max([len(stud_fio) for stud_fio in students])

        stud_list = stud_dict[group]
        stud_list.sort()

        for i in range(len(stud_list)):
            worksheet.set_column(i + 1, col_counter, col_width)
            worksheet.write(i + 1, col_counter, stud_list[i])

        col_counter += 1


LIST_OF_ADMINS = [374464076]
# LIST_OF_HEADMANS = Headman.get_all_headmans()
LIST_OF_HEADMANS = []
LIST_OF_DEKANAT = [374464076]


def restricted_studdekan(func):
    @wraps(func)
    def wrapped(message):
        user_id = message.from_user.id
        print(f'You are {user_id}')
        if user_id not in LIST_OF_ADMINS:
            print(f'Denied for {user_id}')
            return
        return func(message)
    return wrapped


def restricted_headman(func):
    @wraps(func)
    def wrapped(message):
        user_id = message.from_user.id
        print(f'You are {user_id}')
        if user_id not in LIST_OF_HEADMANS:
            print(f'Denied for {user_id}')
            return
        return func(message)
    return wrapped


def restricted_dekanat(func):
    @wraps(func)
    def wrapped(message):
        user_id = message.from_user.id
        print(f'You are {user_id}')
        if user_id not in LIST_OF_DEKANAT:
            print(f'Denied for {user_id}')
            return
        return func(message)
    return wrapped
