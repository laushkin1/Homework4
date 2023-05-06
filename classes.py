from collections import UserDict


class Field:
    def __init__(self, value) -> None:
        self.value = value


class Name(Field):
    ...


class Phone(Field):
    def make_list(self, phones: str):
        phones = phones.split(' ')
        return phones


class Record(Field):
    def __init__(self, name: Name, phone: Phone | str | None = None, phones: list[Phone] = []):
        self.name = name
        self.phones = phones
        if phone is not None:
            self.add_phone(phone)

    def add_phone(self, phone: Phone | str):
        if isinstance(phone, str):
            phone = self.create_phone(phone)
        self.phones.append(phone)

    def create_phone(self, phone: str):
        return Phone(phone)

    def change_phone(self, new_phone):
        self.phones = new_phone
        

    def show_rec(self):
        for indx, phone in enumerate(self.phones):
            print(f'{indx + 1}: {phone.value}')

    def get_name(self):
        return self.name.value


class AddressBook(UserDict, Field):

    def __init__(self, record: Record | None = None) -> None:
        self.records = {}
        if record is not None:
            self.add_record(record)

    def add_record(self, record: Record):
        self.records[record.get_name()] = record

    def show_adb(self):
        for name, record in self.records.items():
            print(f'{name}:')
            record.show_rec()
        return 'These are all your contacts.'

    def get_records(self, name: str):
        return self.records[name]
