import re
from collections import UserDict
from datetime import datetime, timedelta

from .helpers import NotValidPhoneNumberError

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # keep it empty, no overrides
    pass

class Phone(Field):
    PHONE_NUMBER_REGEX = r"\d{10}"

    def __init__(self, value: str):
        if not self.is_valid_phone(value):
            raise NotValidPhoneNumberError("Phone number must be 10 digits.")

        super().__init__(value)

    @staticmethod
    def is_valid_phone(value):
        return re.fullmatch(Phone.PHONE_NUMBER_REGEX, value) is not None

class Birthday(Field):
    def __init__(self, value):
        try:
            date_string = datetime.strptime(value, "%d.%m.%Y")
            super().__init__(date_string)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY.")

class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone_to_remove: str):
        self.phones = [phone for phone in self.phones if phone.value != phone_to_remove]

    def edit_phone(self, phone_to_edit: str, phone_new_value: str):
        if not Phone.is_valid_phone(phone_new_value):
            raise NotValidPhoneNumberError("Phone number must be 10 digits")

        for phone in self.phones:
            if phone.value == phone_to_edit:
                phone.value = phone_new_value
                break # exit from the loop when found the first match

    def find_phone(self, phone_to_find: str):
        for phone in self.phones:
            if phone.value == phone_to_find:
                return phone

    def show_phones(self):
        return "; ".join(phone.value for phone in self.phones)

    def add_birthday(self, date: str):
        self.birthday = Birthday(date)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Phone:
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.now().date()
        congratulations_list = []

        for name, record in self.data.items():
            if not record.birthday:
                continue

            user_birth_date_formatted = record.birthday.value.date()
            user_congratulation_date = user_birth_date_formatted.replace(year=today.year)

            if 0 <= (user_congratulation_date - today).days <= 7:
                # adjust the date if it's on weekends
                if user_congratulation_date.weekday() in [5, 6]:
                    user_congratulation_date = (user_congratulation_date + timedelta(days=2)
                                                if user_congratulation_date.weekday() == 5 else
                                                user_congratulation_date + timedelta(days=1))
                congratulations_list.append({
                    "name": name,
                    "congratulation_date": user_congratulation_date.strftime("%d.%m.%Y")
                })

        return congratulations_list
