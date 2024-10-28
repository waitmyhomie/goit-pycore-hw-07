from collections import UserDict

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
        if self.validate_birthday(value):
            super().__init__(value)
        else:
            raise ValueError("Birthday must be in format YYYY-MM-DD.")
    @staticmethod
    def validate_birthday(value):
        print(len(value) == 10 and value[4] == "-" and value[7] == "-" and value[:4].isdigit() and value[5:7].isdigit() and value[8:].isdigit())
        return len(value) == 10 and value[4] == "-" and value[7] == "-" and value[:4].isdigit() and value[5:7].isdigit() and value[8:].isdigit()


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

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    
    def add_birthday(self, birthday):
        try:
            self.birthday = Birthday.validate_birthday(birthday)
        except ValueError as e:
            print(e)

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


if __name__ == "__main__":
    book = AddressBook()
    # user john
    user_record = Record("John")
    user_record.add_phone("1234567890")
    user_record.add_phone("5555555555")
    #pass a function to add birthday
    user_record.add_birthday("01-01-1990")

  
    book.add_record(user_record)
    #user jane
    user_record = Record("Jane")
    user_record.add_phone("9876543210")
    book.add_record(user_record)

 
    for name, record in book.data.items():
        print(record)

    #search john and edit phone
    john = book.find("John")
    if john:
        john.edit_phone("1234567890", "1112223333")
    
    print(john) 

    found_phone = john.find_phone("5555555555")
    if found_phone:
        print(f"{john.name}: {found_phone}")  

    # delete jane
    book.delete("Jane")

    jane = book.find("Jane")
    if not jane:
        print("Jane not found.")
    else:
        print(jane)
