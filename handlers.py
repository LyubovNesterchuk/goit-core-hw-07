from color_function import success, error, info
from datetime import timedelta, date
from models import Record, AddressBook
from ui import commands
from utils import input_error


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


