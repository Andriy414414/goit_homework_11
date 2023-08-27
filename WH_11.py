from collections import UserDict
from datetime import date
import re


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value) -> None:
        self._value = value

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other):
        if hasattr(other, "value"):
            value = other.value
        else:
            value = other
        return self.value == value


class Name(Field):
    pass


class Phone(Field):
    @staticmethod
    def phone_validation(phone: str) -> None:
        if not isinstance(phone, str):
            raise ValueError("Phone have to be str")
        if not phone.isdigit():
            raise ValueError("Phone have to include only digits")
        if 9 >= len(phone) <= 15:
            raise ValueError("Phone is too short or long")

    @Field.value.setter
    def value(self, phone: str) -> None:
        self.phone_validation(phone)
        Field.value.fset(self, phone)


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @staticmethod
    def birthday_validation(birthday: str) -> None:
        if type(birthday) != str: # isinstance
            raise ValueError("Phone have to be str")
        date_pattern = r"^\d{4}-\d{2}-\d{2}$"
        if not re.match(date_pattern, birthday):
            raise ValueError("Invalid birthday format. Please use 'YYYY-MM-DD' format.")

    @Field.value.setter
    def value(self, birthday: str) -> None:
        self.birthday_validation(birthday)
        Field.value.fset(self, birthday)


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = [phone] if phone is not None else []
        self.birthday = birthday

    def add_phone(self, phone: Phone):
        if phone in self.phones:
            raise ValueError(f"phone: {phone} is already in record")
        self.phones.append(phone)

    def delete_phone(self, phone: Phone):
        try:
            self.phones.remove(phone)
        except ValueError:
            raise ValueError(f"phone: {phone} not exists")

    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        try:
            index = self.phones.index(old_phone)
            self.phones[index] = new_phone
        except ValueError:
            raise ValueError(f"old phone: {phone} not exists")

    def days_to_birthday(self):
        current_date = date.today()
        if self.birthday != None:
            birthday_date = date(self.birthday, "%Y-%m-%d")

            next_birthday_date = date(
                current_date.year, birthday_date.month, birthday_date.day
            )
            if current_date > next_birthday_date:
                next_birthday_date = date(
                    current_date.year + 1, birthday_date.month, birthday_date.day
                )

            return (next_birthday_date - current_date).days
        else:
            return f"This contact doesn't have the info about birthday"
    
    def __str__(self):
        str_phones = ", ".join(map(str, self.phones))
                
        return f'{self.name} {str_phones} {self.birthday}'


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find_record(self, key_name: str):
        result = self.data.get(key_name)
        if self.data.get(key_name) == None:
            raise ValueError("There isn't such record")
        return result

    def paginate(self, records_per_page: int):
        counter = 0
        list_rec = []
        for record in self.data.values():
            list_rec.append(record)
            counter += 1
            if not counter % records_per_page: 
                yield list_rec
                list_rec = []
            if counter == len(self.data):
                yield list_rec  


