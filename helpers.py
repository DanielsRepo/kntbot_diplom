from functools import wraps


def get_fio(s):
    try:
        return f"{s.split(' ')[0]} {s.split(' ')[1][0]}. {s.split(' ')[2][0]}."
    except IndexError:
        return


def make_student_events_table(stud_dict, group, worksheet, workbook):
    row_counter = 0

    worksheet.write(0, 0, f'КНТ-{group}', workbook.add_format({'bold': True, 'align': 'center'}))
    worksheet.write(0, 1, 'Мероприятия', workbook.add_format({'bold': True, 'align': 'center'}))

    for students, events in sorted(stud_dict.items(), key=lambda key_value: key_value[0]):
        row = row_counter

        col_width = max([len(stud_fio) for stud_fio in stud_dict.keys()])
        worksheet.set_column(row + 1, 0, col_width)
        worksheet.write(row + 1, 0, students)

        events = ', '.join(stud_dict[students])
        col_width = max([len(', '.join(events)) for events in stud_dict.values()])
        worksheet.set_column(row + 1, 1, col_width)
        worksheet.write(row + 1, 1, events)

        row_counter += 1


def make_event_visitors_table(stud_dict, worksheet, workbook):
    col_counter = 0

    for group, students in sorted(stud_dict.items(), key=lambda key_value: key_value[0]):
        col = col_counter

        cell_format = workbook.add_format({'bold': True, 'align': 'center'})
        worksheet.write(0, col, group, cell_format)

        col_width = max([len(stud_fio) for stud_fio in students])

        stud_list = stud_dict[group]
        stud_list.sort()
        for i in range(len(stud_list)):
            worksheet.set_column(i + 1, col, col_width)
            worksheet.write(i + 1, col, stud_list[i])

        col_counter += 1


LIST_OF_ADMINS = [374464076]


def restricted(func):
    @wraps(func)
    def wrapped(message):
        user_id = message.from_user.id
        print(f'You are {user_id}')
        if user_id not in LIST_OF_ADMINS:
            print(f'Denied for {user_id}')
            return
        return func(message)
    return wrapped


students = [
    'Костин Юстин Леонидович',
    'Яковлев Ефрем Якунович',
    'Исаев Мирослав Сергеевич',
    'Николаев Флор Игоревич',
    'Федотов Агафон Богуславович',
    'Артемьев Тимур Филатович',
    'Белозёров Май Игоревич',
    'Денисов Тарас Лукьевич',
    'Беляков Мартин Вадимович',
    'Мамонтов Всеволод Сергеевич',
    'Миронов Геннадий Улебович',
    'Симонов Арсений Георгиевич',
    'Соловьёв Юстин Романович',
    'Трофимов Феликс Альвианович',
    'Михеев Глеб Викторович',
    'Гордеев Азарий Геннадьевич',
    'Молчанов Мечеслав Федотович',
    'Сергеев Корнелий Валерьянович',
    'Поляков Авраам Авдеевич',
    'Пономарёв Богдан Викторович',
    'Горшков Варлам Куприянович',
    'Колесников Эрик Богданович',
    'Лаврентьев Гордий Платонович',
    'Богданов Владимир Донатович',
    'Савельев Нелли Денисович',
    'Наумов Витольд Александрович',
    'Гришин Лукьян Богданович',
    'Мясников Семен Иосифович',
    'Котов Лев Аркадьевич',
    'Шарапов Мирон Егорович',
    'Мартынов Устин Викторович',
    'Денисов Панкратий Владиславович',
    'Авдеев Герасим Богуславович',
    'Степанов Игнатий Иванович',
    'Третьяков Аполлон Павлович',
    'Суханов Степан Тимофеевич',
    'Агафонов Касьян Никитевич',
    'Евсеев Терентий Рудольфович',
    'Шаров Устин Яковлевич',
    'Белозёров Мартин Павлович',
    'Лапин Альфред Антонович',
    'Громов Иван Яковлевич',
    'Павлов Ефрем Юлианович',
    'Пономарёв Карл Борисович',
    'Наумов Филипп Арсеньевич',
    'Лобанов Гордий Артемович',
    'Тимофеев Георгий Валерьянович',
    'Петров Гаянэ Владиславович',
    'Овчинников Юлий Авксентьевич',
    'Беспалов Велор Рудольфович',
    'Субботин Аскольд Мартынович',
    'Савин Максим Антонович',
    'Давыдов Станислав Дмитриевич',
    'Тарасов Алексей Александрович',
    'Иванков Ефрем Богданович',
    'Самойлов Евгений Эльдарович',
    'Осипов Эльдар Фролович',
    'Панов Аркадий Константинович',
    'Логинов Флор Валерьянович',
    'Копылов Рубен Протасьевич',
]
