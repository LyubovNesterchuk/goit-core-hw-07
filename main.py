from models import AddressBook
from handlers import *
from utils import parse_input
from ui import init
from color_function import success, error, info, greet


def main():
    book = AddressBook()

    print(greet("Welcome to the assistant bot!\n"))

    while True:
        user_input = input(info("Enter a command: ").strip())

        if not user_input:
            print(error("Invalid command."))
            continue

        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print(greet("Good bye!"))
            break

        elif command == "hello":
            print(say_hello())

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))
            
        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        elif command == "help":
            print(show_help())

        else:
            print("Invalid command.")


if __name__ == "__main__":
    init()
    main()


# в терміналі: 
# python -m venv .venv
# source .venv/Scripts/activate
# pip install colorama 
# pip freeze > requirements.txt