from collections import UserDict
from datetime import datetime, date, timedelta
from color_function import success, error, info, greet


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone must be 10 digit")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(parsed_date)
       

class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    
    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def remove_phone(self, phone:str):
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)
        else:
            raise ValueError("Phone not found")
              
    def edit_phone(self, old_phone:str, new_phone: str):
        phone_obj = self.find_phone(old_phone)
        if not phone_obj:
            raise ValueError("Old phone not found")
        new_phone_obj = Phone(new_phone)
        index = self.phones.index(phone_obj)
        self.phones[index] = new_phone_obj


    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)    

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        birthday = (self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "Not available")
        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {birthday}"
    
    
class AddressBook(UserDict):
    def add_record(self, record: Record): 
        self.data[record.name.value] = record 

    def find(self, name: str) -> Record | None:
        return self.data.get(name)
    
    def find_by_phone(self, phone: str) -> Record | None:
        for record in self.data.values(): 
            if record.find_phone(phone):
                return record
        return None
    
    def delete(self, name: str):
        if name in self.data: 
            del self.data[name]
        else:
            raise KeyError("Contact not found")
        
    def __str__(self):
        if not self.data: 
            return "AddressBook is empty" 
        return "\n".join(str(record) for record in self.data.values()) 



welcome_banner = '''
  ___          _     _              _     _           _   
 / _ \        (_)   | |            | |   | |         | |  
/ /_\ \___ ___ _ ___| |_ __ _ _ __ | |_  | |__   ___ | |_ 
|  _  / __/ __| / __| __/ _` | '_ \| __| | '_ \ / _ \| __|
| | | \__ \__ \ \__ \ || (_| | | | | |_  | |_) | (_) | |_ 
\_| |_/___/___/_|___/\__\__,_|_| |_|\__| |_.__/ \___/ \__|
'''

commands = '''
1) hello - greet the assistant bot
2) add username phone - add a new contact with name and phone number
3) change username old_phone new_phone- change the phone number for an existing contact
4) phone username - show the phone number of the contact
5) all - show all saved contacts
6) help - show this help menu
7) add-birthday username DD.MM.YYYY
8) show-birthday username
9) birthdays
10) exit or close - exit the application
''' 
def init():
    print(greet(welcome_banner))
    print(info(commands))
    print()

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.lower()
    return cmd, args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError: 
            return error("Give me name and phone please.")
        except KeyError:
            return error("Contact not found.")
        except IndexError: 
            return error("Enter name.")
    return inner


@input_error
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
    return success(message)


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args

    record = book.find(name)
    if not record:
        return error("Contact not found.")

    record.edit_phone(old_phone, new_phone)
    return success("Contact updated."  )  


@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)

    if not record:
        return error("Contact not found.")

    return success("; ".join(p.value for p in record.phones))

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    
    record = book.find(name)
    if not record:
        return error("Contact not found.")
    
    record.add_birthday(birthday)
    return success("Birthday added.")


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)

    if not record:
        return error("Contact not found.")

    if not record.birthday:
        return error("Birthday not set.")

    return success(record.birthday.value.strftime("%d.%m.%Y"))


@input_error
def birthdays(args, book):
    today = date.today()
    upcoming = []

    for record in book.data.values():
        if not record.birthday:
            continue
        
        bday = record.birthday.value.replace(year=today.year)

        if bday < today:
            bday = bday.replace(year=today.year + 1)

        if bday.weekday() >= 5:  
            bday += timedelta(days=(7 - bday.weekday()))
            
        if 0 <= (bday - today).days <= 7:
            upcoming.append(f"{record.name.value}: {bday.strftime('%d.%m.%Y')}")

    return success("\n".join(upcoming) if upcoming else "No upcoming birthdays.")


@input_error
def show_all(book: AddressBook):
    if not book.data:
        return error("No contacts saved.")
    
    return success("\n".join(str(record) for record in book.data.values()))


@input_error
def say_hello():
    return info("How can I help you?")


@input_error
def show_help():
    return info(commands)


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