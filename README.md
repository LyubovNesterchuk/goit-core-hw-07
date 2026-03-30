# 📒 Assistant Bot (Address Book CLI)

A simple command-line assistant bot for managing contacts, phone numbers, and birthdays.

---

## 🚀 Features

- Add contacts with phone numbers
- Support multiple phone numbers per contact
- Edit existing phone numbers
- Search phone numbers by name
- Store birthdays for contacts
- Show upcoming birthdays (within 7 days)
- View all saved contacts
- Friendly CLI interface with colored output

---

## 🛠️ Commands

| Command | Description |
|--------|-------------|
| `hello` | Greet the assistant bot |
| `add <name> <phone>` | Add a new contact |
| `change <name> <old_phone> <new_phone>` | Change a phone number |
| `phone <name>` | Show all phone numbers of a contact |
| `all` | Show all contacts |
| `add-birthday <name> <DD.MM.YYYY>` | Add birthday |
| `show-birthday <name>` | Show birthday |
| `birthdays` | Show upcoming birthdays (7 days) |
| `help` | Show command list |
| `exit` or `close` | Exit the application |

---

## 📦 Project Structure
```assistant_bot/
│
├── main.py # Entry point of the application
├── models.py # Data models (Contact, AddressBook, Fields)
├── handlers.py # Command handlers (add, change, etc.)
├── utils.py # Helper functions (parser, decorators)
├── color_function.py # Colored output functions
└── README.md


```

## ▶️ How to Run

1. Make sure you have Python installed (3.10+ recommended)

2. Clone the repository:
```bash
git clone <your-repo-url>
cd assistant_bot
Run the program:
python main.py


```

## 📌 Example Usage

Enter a command: add John 1234567890
Contact added.

Enter a command: add John 0987654321
Contact updated.

Enter a command: phone John
1234567890; 0987654321

Enter a command: add-birthday John 25.12.1990
Birthday added.


---

## 🧠 Notes

- Each contact can have multiple phone numbers
- Phone numbers must be 10 digits
- Birthday format must be DD.MM.YYYY
- Upcoming birthdays are shown for the next 7 days


---

## 📄 License

This project is created for learning purposes.