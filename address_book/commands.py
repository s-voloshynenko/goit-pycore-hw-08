from .helpers import ContactsError, input_error, input_validate_args
from .address_book import AddressBook, Record

@input_error
@input_validate_args(["name", "phone"])
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."

    if phone:
        record.add_phone(phone)

    return message

@input_error
@input_validate_args(["name", "old_phone", "new_phone"])
def change_contact(args: list, book: AddressBook) -> str:
    name, old_phone, new_phone = args
    record = book.find(name)

    if record is None:
        raise ContactsError("Contact doesn't exist.")

    record.edit_phone(old_phone, new_phone)

    return "Contact updated."

@input_error
@input_validate_args(["name"])
def show_phone(args: list, book: AddressBook) -> str:
    name = args[0]
    record = book.find(name)

    if record is None:
        raise ContactsError("Contact doesn't exist.")

    return record.show_phones()

@input_error
def all_contacts(book: AddressBook) -> str:
    if not book:
        raise ContactsError("Contacts dictionary is empty.")

    command_output = "Contacts list:"

    for name, record in book.items():
        command_output += f"\n{name}: {record.show_phones()}"

    return command_output

@input_error
@input_validate_args(["name", "birthday"])
def add_birthday(args, book: AddressBook) -> str:
    name, birthday = args
    record = book.find(name)

    if record is None:
        raise ContactsError("Contact doesn't exist.")

    record.add_birthday(birthday)

    return "Birthday added."

@input_error
@input_validate_args(["name"])
def show_birthday(args, book: AddressBook) -> str:
    name = args[0]
    record = book.find(name)

    if record is None:
        raise ContactsError("Contact doesn't exist.")

    return record.birthday.value.strftime("%d.%m.%Y")

@input_error
def birthdays(book: AddressBook) -> str:
    output = f"{"Name":<{10}}{" | "}{"Birthday":<{10}}\n" \
                f"{"-" * 10:<{10}}{" | "}{"-" * 10:<{10}}\n" \

    if not book:
        raise ContactsError("Contacts dictionary is empty.")

    birthdays_list = book.get_upcoming_birthdays()

    if not birthdays_list:
        return "No birthdays for the upcoming 7 days."

    for contact in birthdays_list:
        output += f"{contact["name"]:<{10}}{" | "}{contact["congratulation_date"]:<{10}}\n"

    return output
