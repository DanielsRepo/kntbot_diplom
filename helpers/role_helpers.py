from functools import wraps

LIST_OF_ADMINS = [374464076]
# LIST_OF_HEADMANS = Headman.get_all_headmans()
LIST_OF_HEADMANS = [374464076]
LIST_OF_DEKANAT = [374464076]


def restricted_studdekan(func):
    @wraps(func)
    def wrapped(message):
        user_id = message.from_user.id
        if user_id not in LIST_OF_ADMINS:
            print(f'Denied for {user_id}')
            return
        return func(message)
    return wrapped


def restricted_headman(func):
    @wraps(func)
    def wrapped(message):
        user_id = message.from_user.id
        if user_id not in LIST_OF_HEADMANS:
            print(f'Denied for {user_id}')
            return
        return func(message)
    return wrapped


def restricted_dekanat(func):
    @wraps(func)
    def wrapped(message):
        user_id = message.from_user.id
        if user_id not in LIST_OF_DEKANAT:
            print(f'Denied for {user_id}')
            return
        return func(message)
    return wrapped
