from color_function import success, error, info
from datetime import timedelta, date, datetime
from models import Record, AddressBook
from ui import commands
from utils import input_error


def get_record_or_fail(book: AddressBook, name: str) -> Record:
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    return record


@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Give me name and phone please.")

    name, phone = args

    temp_record = Record(name)
    temp_record.add_phone(phone)  

    record = book.find(name)
    message = "Contact updated."

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."

    record.add_phone(phone)

    return success(message)

@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args

    record = get_record_or_fail(book, name)
    record.edit_phone(old_phone, new_phone)

    return success("Contact updated.")


@input_error
def show_phone(args, book: AddressBook):
    name = args[0]

    record = get_record_or_fail(book, name)
    return success("; ".join(p.value for p in record.phones))


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args

    record = get_record_or_fail(book, name)
    record.add_birthday(birthday)

    return success("Birthday added.")


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]

    record = get_record_or_fail(book, name)

    if not record.birthday:
        return error("Birthday not set.")

    return success(record.birthday.value)


@input_error
def birthdays(args, book: AddressBook):
    today = date.today()
    upcoming = []

    for record in book.data.values():
        if not record.birthday:
            continue

        birthday_str = record.birthday.value
        bday = datetime.strptime(birthday_str, "%d.%m.%Y").date()
        bday = bday.replace(year=today.year)

        if bday < today:
            bday = bday.replace(year=today.year + 1)

        if bday.weekday() >= 5:
            bday += timedelta(days=(7 - bday.weekday()))

        if 0 <= (bday - today).days <= 7:
            upcoming.append(
                f"{record.name.value}: {bday.strftime('%d.%m.%Y')}"
            )

    return success(
        "\n".join(upcoming) if upcoming else "No upcoming birthdays."
    )


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


