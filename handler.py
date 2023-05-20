from classes import AddressBook, Name, Phone, Record, Birthday

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


contacts = AddressBook('data.bin')


def hello() -> str:
    return 'How can I help you?'


@input_error
def add(name: str, phone_number: str, birthday: str =None) -> str:
    phones = Phone(phone_number)
    phones = phones.make_list(phone_number)
    phones = [Phone(val) for val in phones]
    record = Record(name=Name(name), phones=phones, birthday=birthday)
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


@input_error
def iterator(n_rec: int) -> str:
    if len(contacts.records) == 0:
        return 'You have not any contacts.'
    else:
        contacts.add_n_rec(int(n_rec))
        for i in contacts:
            print(i)
        return 'These are all contacts.'
    

@input_error
def birthday(name: str) -> str:
    try:
        a = contacts.get_records(name)
        return a.days_to_birthday()
    except:
        return 'This contact has no birthday.'
    

@input_error
def search(value: str) -> str:
    if contacts.search(value) != {}:
        return contacts.search(value)
    return 'Nothing was found for your search.'
