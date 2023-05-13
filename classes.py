from collections import UserDict
from collections.abc import Iterator
from datetime import datetime
import re


class Field:
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value
    
    @property
    def val(self):
        return self.__value
    
    @val.setter
    def val(self, value):
        self.__value = value


class Name(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        
    @Field.val.setter
    def name(self, value):
        if len(value) > 0:
            Field.val.fset(self, value)
        else:
            raise ValueError("The name should be.")



class Phone(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        
    @Field.val.setter
    def phone(self, value: str):
        if value.replace(' ', '').isdigit():
            Field.val.fset(self, value)
        else:
            raise ValueError("This number is invalid.")
    
    def make_list(self, phones: str):
        phones = phones.split(' ')
        return phones


class Birthday(Field):
    def __init__(self, birthday: str) -> None:
        super().__init__(birthday)
        birthday = birthday.split('.')

        self.day = int(birthday[0])
        self.month = int(birthday[1])
        self.year = int(birthday[2])                            # Not used

        self.birthday = datetime(
            year=int(datetime.now().year),
            month=int(birthday[1]), day=int(birthday[0]))
        
    @Field.val.setter
    def birth(self, value):
        current_datetime = datetime.now()
        if re.search("^\d\d\.\d\d\.\d\d\d\d$", value):
            value = value.split('.')
            try:
                birthday = datetime(
                    year=int(value[2]),
                    month=int(value[1]),
                    day=int(value[0]))
            except ValueError:
                raise ValueError("This birthday is invalid.")
        else:
            birthday = current_datetime

        if birthday < current_datetime:
            return Field.val.fset(self, value)
        else:
            raise ValueError("This birthday is invalid.")

    def days_to_birthday(self):
        if (self.birthday - datetime.now()).days >= 0:
            return (self.birthday - datetime.now()).days

        else:
            if datetime.now().year % 4:
                # 365 days for year
                return (self.birthday - datetime.now()).days + 365 + 1
            else:
                # 366 days for a leap year
                return (self.birthday - datetime.now()).days + 366 + 1


class Record(Birthday, Field):
    def __init__(self, name: Name, 
                 phone: Phone | str | None = None, 
                 phones: list[Phone] = [], 
                 birthday: str = None):
        if birthday is not None:
            super().__init__(birthday)
        
        self.name = name
        self.phones = phones
        if phone is not None:
            self.add_phone(phone)
            
    def get_birthday(self):
        return f"{self.birthday.day}.{self.birthday.month}.{self.year}"
            
        
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
            
    def show_phones(self):
        cont = []
        for phone in self.phones:
            cont.append(phone.value)
        return cont

    def get_name(self):
        return self.name.value


class Iterator:
    def __init__(self, n_rec, adbook) -> None:
        self.n_rec = n_rec
        self.index = 0
        self.adbook = adbook
    
    def __next__(self):
        if self.index <= len(self.adbook):
            res = ''
            for name, numbers in self.adbook[self.index:self.n_rec]:
                res += f"{name}: {numbers}\n"
            self.index = self.n_rec
            self.n_rec += self.n_rec
            return res
        else:
            raise StopIteration
        


class AddressBook(UserDict, Field):

    def __init__(self, record: Record | None = None, n_rec=5) -> None:
        self.n_rec = n_rec
        self.records = {}
        if record is not None:
            self.add_record(record)

    def add_record(self, record: Record):
        self.records[record.get_name()] = record

    def show_adb(self):
        for name, record in self.records.items():
            print(f'{name}:')
            record.show_rec()
            try:
                print(f"{name}`s birthday: {record.get_birthday()}")
            except:
                pass
        return 'These are all your contacts.'
    
    def get_tuple(self):
        res = []
        for name, record in self.records.items():
            res.append((name, record.show_phones()))
        return res

    def get_records(self, name: str):
        return self.records[name]
    
    def add_n_rec(self, n_rec: int) -> None:
        self.n_rec = n_rec
    
    def __iter__(self) -> Iterator:
        return Iterator(n_rec=self.n_rec, adbook=self.get_tuple())

