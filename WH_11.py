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


phone = Phone("12456788756")

print(phone)


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @staticmethod
    def birthday_validation(birthday: str) -> None:
        if type(birthday) != str:
            raise ValueError("Phone have to be str")
        date_pattern = r"^\d{4}-\d{2}-\d{2}$"
        if not re.match(date_pattern, birthday):
            raise ValueError("Invalid birthday format. Please use 'YYYY-MM-DD' format.")

    @Field.value.setter
    def value(self, birthday: str) -> None:
        self.birthday_validation(birthday)
        Field.value.fset(self, birthday)


birthday_A = Birthday("2000-01-01")

print(birthday_A)


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = [phone] if phone else []
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




class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find_record(self, key_name: str):
        result = self.data.get(key_name)
        if self.data.get(key_name) == None:
            raise ValueError("There isn't such record")
        return result

    def paginate(self, records_per_page):
        sorted_contacts = sorted(self.items())
        total_pages = (len(sorted_contacts) + records_per_page - 1) // records_per_page

        start_idx = 0

        for page_num in range(total_pages):
            end_idx = start_idx + records_per_page
            page = sorted_contacts[start_idx:end_idx]
            yield page
            start_idx = page_num * records_per_page + 1

rec = Record("Bob", "777777777777", "2020-01-01")
rec1 = Record("Bob1", "555555555555", "2010-07-02")
rec2 = Record("Bob2", "666666666666", "2001-09-20")
rec3 = Record("Bob3", "111111111111", "2000-04-15")
rec4 = Record("Bob4", "222222222222", "1995-02-08")

ab = AddressBook.add_record(rec)

print(ab)


if __name__ == "__main__":
    name = Name("Bill")
    phone = Phone("1234567890")
    rec = Record(name, phone)
    ab = AddressBook()
    ab.add_record(rec)

    assert isinstance(ab["Bill"], Record)
    assert isinstance(ab["Bill"].name, Name)
    assert isinstance(ab["Bill"].phones, list)
    assert isinstance(ab["Bill"].phones[0], Phone)
    assert ab["Bill"].phones[0].value == "1234567890"

    print("All Ok)")
