from collections import UserDict
from datetime import datetime


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
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)


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
        phones = "; ".join(p.value for p in self.phones) if self.phones else "No phones"
        birthday = self.birthday.value if self.birthday else "Not available"
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
    
   