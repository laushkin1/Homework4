from collections import UserDict
from collections.abc import Iterator
from datetime import datetime
from pathlib import Path
import pickle


class Field:
    def __init__(self, value) -> None:
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Name(Field):
    def __init__(self, name: str) -> None:
        self.value = name

    @Field.value.setter
    def value(self, name):
        if len(name) > 1:
            Field.value.fset(self, name)
        else:
            raise ValueError("The name should be.")



class Phone(Field):
    def __init__(self, phone) -> None:
        self.value = phone
        
        
    @Field.value.setter
    def value(self, phone):
        if phone.replace(' ', '').isdigit():
            Field.value.fset(self, phone)
        else:
            raise ValueError("This number is invalid.\nThe number must be numbers, no other characters")
    
    def make_list(self, phones: str):
        phones = phones.split(' ')
        return phones


class Birthday(Field):
    def __init__(self, birthday: str) -> None:
        self.value = birthday
        self.birthday = self.value.replace(year=datetime.now().year)
        
    @Field.value.setter
    def value(self, birthday):
        try:
            dt = datetime.strptime(birthday, '%d.%m.%Y')
        except (ValueError, TypeError):
            raise Exception("Invalid birthday. Only string format dd.mm.yyyy")
        Field.value.fset(self, dt.date())

    def days_to_birthday(self):
        self.birthday = datetime.combine(
            self.birthday, datetime.min.time())
        
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
        return f"{self.birthday.day}.{self.birthday.month}.{self.value.year}"     
       
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
            for name, numbers, birthday in self.adbook[self.index:self.n_rec]:
                if birthday == None:
                    res += f"{name}: {numbers}\n"
                else:
                    res += f"{name}: {numbers}\t{name}`s birthday: {birthday}\n"
            self.index = self.n_rec
            self.n_rec += self.n_rec
            
            return res
        else:
            raise StopIteration
        


class AddressBook(UserDict, Field):
    def __init__(self, filename, record: Record | None = None, n_rec=5) -> None:
        self.n_rec = n_rec
        self.records = {}
        self.file = Path(filename)
        self.deserialize()
        if record is not None:
            self.add_record(record)

    def add_record(self, record: Record):
        self.records[record.get_name()] = record
        
    def search(self, search_str: str):
        result = {} 
        for name, record in self.records.items():
            if search_str in name or ','.join(record.show_phones()).__contains__(search_str):
                result[name] = record.show_phones()
        return result
    
    def serialize(self):
        with open(self.file, "wb") as file:
            pickle.dump(self.records, file)
            
    def deserialize(self):
        if not self.file.exists():
            return None
        try:
            with open(self.file, "rb") as file:
                self.records = pickle.load(file)
        except EOFError:
            return None

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
            try:
                res.append((name, record.show_phones(), record.get_birthday()))
            except:
                res.append((name, record.show_phones(), None))
        return res

    def get_records(self, name: str):
        return self.records[name]
    
    def add_n_rec(self, n_rec: int) -> None:
        self.n_rec = n_rec
    
    def __iter__(self) -> Iterator:
        return Iterator(n_rec=self.n_rec, adbook=self.get_tuple())
