from enum import Enum

from .address_book import AddressBook
from .commands import (
    add_birthday, add_contact, all_contacts,
    birthdays, change_contact, show_birthday, show_phone
)

class Commands(Enum):
    EXIT = "exit"
    CLOSE = "close"
    HELLO = "hello"
    ADD = "add"
    CHANGE = "change"
    PHONE = "phone"
    ALL = "all"
    ADD_BIRTHDAY = "add-birthday"
    SHOW_BIRTHDAY = "show-birthday"
    BIRTHDAYS = "birthdays"

    def __eq__(self, value: object) -> bool:
        return self.value == value

def parse_input(user_input: str):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def listen_commands(book: AddressBook, on_exit=callable):
    try:
        print("Welcome to the assistant bot!")

        while True:
            user_input = input("Enter a command: ")
            command, args = parse_input(user_input)

            if command in (Commands.EXIT, Commands.CLOSE):
                on_exit(book)
                print("Good bye!")
                break

            elif command == Commands.HELLO:
                print("How can I help you?")

            elif command == Commands.ADD:
                print(add_contact(args, book))

            elif command == Commands.CHANGE:
                print(change_contact(args, book))

            elif command == Commands.PHONE:
                print(show_phone(args, book))

            elif command == Commands.ALL:
                print(all_contacts(book))

            elif command == Commands.ADD_BIRTHDAY:
                print(add_birthday(args, book))

            elif command == Commands.SHOW_BIRTHDAY:
                print(show_birthday(args, book))

            elif command == Commands.BIRTHDAYS:
                print(birthdays(book))

            else:
                print("Invalid command.")
    except KeyboardInterrupt:
        on_exit(book)
