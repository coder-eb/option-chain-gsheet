def strip_extra_spaces(data):
    data = [x.strip(' ') for x in data]
    return data


def get_required_data(type):
    data = []

    plural_form = 'indexes' if (type == 'index') else 'equities'
    no_of_items = int(input(f"Enter number of {plural_form}: "))

    for iteration in range(0, no_of_items):
        elm = input(f'Enter {type} {iteration+1}: ')
        data.append(elm)

    return strip_extra_spaces(data)


def get_stocks_from_user():
    return get_required_data('index'), get_required_data('equity')
