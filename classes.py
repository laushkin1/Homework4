from collections import UserDict

class Field:
    ...


class Name(Field):
    def name_user(self, name):
        return name


class Phone(Field):
    def phone_number(self, phone):
        return phone


class Record(Field):
    def record_date(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number
        


class AddressBook(UserDict, Field):
    def add_record(self, record):
        self.data[record.name] = record.phone_number
