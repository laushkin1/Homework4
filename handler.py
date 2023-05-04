from classes import AddressBook, Name, Phone, Record

def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except KeyError:
            return 'This contact is missing.'
        except ValueError:
            return 'Write numbers as phone please.'
        except IndexError:
            return 'Give me name and phone please.'
        except TypeError:
            return 'Give me name and phone please.'
    return inner


contacts = AddressBook()


def hello(*args) -> str:
    return 'How can I help you?'


@input_error
def add(name: str, phone_number: str) -> str:
    namE = Name()
    phone_Number = Phone()
    record = Record()
    record.record_date(namE.name_user(
        name), phone_Number.phone_number(phone_number))
    contacts.add_record(record)
    return 'Done, contact is saved.'


@input_error
def change(name: str, phone_number: str) -> str:
    if name in contacts:
        contacts[name] = phone_number
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
