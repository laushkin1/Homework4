from classes import AddressBook, Name, Phone, Record

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'This contact is missing.'
        except ValueError:
            return 'Write numbers as phone please.'
        except IndexError:
            return 'Give me name and phone please.'
        except TypeError:
            return 'Error of arguments in function.'
    return inner


contacts = AddressBook()


def hello() -> str:
    return 'How can I help you?'


@input_error
def add(name: str, phone_number: str) -> str:
    name_ = Name(name)
    phones = Phone(phone_number)
    phones = phones.make_list(phone_number)
    phones = [Phone(val) for val in phones]
    record = Record(name=name_, phones=phones)
    contacts.add_record(record)
    return f'Done, contact is saved.'


@input_error
def change(name: str, new_phone: str) -> str:
    record = contacts.get_records(name)
    phones = Phone(new_phone)
    phones = phones.make_list(new_phone)
    phones = [Phone(val) for val in phones]
    record.change_phone(phones)
    return 'Done, number is changed.'


@input_error
def phone(name: str) -> str:
    res = contacts.get_records(name)
    res.show_rec()
    return f'These are {name}\'s phone numbers.'


def show() -> str:
    if len(contacts.records) == 0:
        return 'You have not any contacts.'
    else:
        return contacts.show_adb()
