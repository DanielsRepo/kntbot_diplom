from functools import wraps

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
