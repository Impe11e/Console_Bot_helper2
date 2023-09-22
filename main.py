from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, name):
        super().__init__(name)
class Phone(Field):
    def __init__(self, phone):
        if not self.validator(phone):
            raise ValueError('Incorrect phone format was entered!')
        super().__init__(phone)
    def validator(self, phone):
        return phone.isdigit() and len(phone) == 10

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        phone_instance = Phone(phone)
        self.phones.append(phone_instance)
    def remove_phone(self, phone):
        if isinstance(phone, Phone):
            if phone in self.phones:
                self.phones = list(filter(lambda x: x != phone, self.phones))
            else:
                raise ValueError('There is no such phone in Records!')
        else:
            raise ValueError('Invalid phone format')

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def edit_phone(self, old_phone, new_phone):
        old_phone_instance = Phone(old_phone)
        new_phone_instance = Phone(new_phone)

        if old_phone_instance in self.phones:
            for i, phone in enumerate(self.phones):
                if old_phone_instance == phone:
                    self.phones[i] = new_phone_instance
        else:
            return None

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, record):
        if record in self.data.keys():
            return self.data.get(record)


    def delete(self, record):
        if record in self.data:
            del self.data[record]
        # else:
        #     raise ValueError('No such name')

