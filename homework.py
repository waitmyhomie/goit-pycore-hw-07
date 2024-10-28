from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if self.validate_phone(value):
            super().__init__(value)
        else:
            raise ValueError("Phone number must be exactly 10 digits.")

    @staticmethod
    def validate_phone(value):
        return value.isdigit() and len(value) == 10
    
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value=datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Birthday must be in format DD.MM.YYYY")  
            
    @staticmethod
    def validate_birthday(value):
        try:
            day, month, year = value.split(".")
            if len(year) == 4 and len(day) == 2 and len(month) == 2:
                return True
            else:
                return False
        except ValueError:
            return False
        
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        try:
            self.phones.append(Phone(phone))
        except ValueError as e:
            print(e)

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        print("Phone not found.")
        return False
    
    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                try:
                    self.phones[i] = Phone(new_phone)
                    return True
                except ValueError as e:
                    print(e)
                    return False
        print("Old phone not found.")
        return False

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    def add_birthday(self, birthday):
        try:
            self.birthday = Birthday(birthday)
        except ValueError as e:
            print(e)
            
    def change_birthday(self, birthday):
        try:
            self.birthday = Birthday(birthday)
        except ValueError as e:
            print(e)
            
    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        print("Record not found.")
        return False
    
    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = datetime.now()
        next_week = today + timedelta(days=days)
        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)
                if today <= birthday_this_year <= next_week:
                    upcoming_birthdays.append(record)
        return upcoming_birthdays

if __name__ == "__main__":
    book = AddressBook()
    # user john
    user_record = book.find("John")
    if not user_record:
        user_record = Record("John")
    user_record.add_phone("1234567890")
    user_record.add_phone("5555555555")
    user_record.add_birthday("01.02.1990")

  
    book.add_record(user_record)
    
    #user jane
    user_record = book.find("Jane")
    if not user_record:
        user_record = Record("Jane")
    user_record.add_phone("1234567892")
    user_record.add_phone("1234567891")
    user_record.add_birthday("30.10.1993")

    book.add_record(user_record)
    
    jane = book.find("Jane")
    if jane:
        jane.change_birthday("01.11.1993")
 
    for name, record in book.data.items():
        print(record)

    john = book.find("John")
    if john:
        john.edit_phone("1234567890", "1112223333")
    
    print(john)  

    found_phone = john.find_phone("5555555555")
    if found_phone:
        print(f"{john.name}: {found_phone}")  

    # book.delete("Jane")

    upcoming_birthdays = book.get_upcoming_birthdays()
    for record in upcoming_birthdays:
        print(f"Upcoming birthday: {record.name.value} on {record.birthday.value.strftime('%d.%m.%Y')}")