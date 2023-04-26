def input_error(func):
    def inner(*args):
        try:
            return func(args[0], args[1])

        except KeyError:
            return 'This contact is missing.'
        except ValueError:
            return 'Write numbers as phone please.'
        except IndexError:
            return 'Give me name and phone please.'
    return inner


contacts = {}


def hello(*args) -> str:
    return 'How can I help you?'


@input_error
def add(name: str, phone_number: str) -> str:
    contacts[str(name)] = int(phone_number)
    return 'Done, contact is saved.'


@input_error
def change(name: str, phone_number: str) -> str:
    if name in contacts:
        contacts[str(name)] = int(phone_number)
        return 'Done, number is changed.'
    else:
        raise KeyError


def phone(*name: str) -> str:
    if str(name[0]) in contacts:
        return contacts[str(name[0])]
    else:
        return 'This contact is missing.'


def show_all(*args) -> str:
    res = ''
    for name, phone_number in contacts.items():
        res += f'{name}: {phone_number}\n'
    res = res.removesuffix('\n')
    if res != '':
        return res
    else:
        return 'You have not any contacts.'