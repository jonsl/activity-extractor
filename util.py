DEFAULT_DECIMAL_PLACES = 2

def spinning_cursor():
    while True:  # around forever
        for cursor in '|/-\\':
            yield cursor

def athlete_fullname(firstname: str, lastname: str) -> str:
    return '{lastname}, {firstname}'.format(
        lastname=lastname,
        firstname=firstname,
    )
