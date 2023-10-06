from collections import UserDict
import datetime
import pickle

class Field:
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self.value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone_str):
        self._phone = None
        self.phone = phone_str
        super().__init__(self._phone)

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, phone_str):
        if phone_str.isdigit() and len(phone_str) == 10:
            self._phone = phone_str
        else:
            raise ValueError('Incorrect phone format was entered! Correct format is 1234567890')


class Birthday(Field):
    def __init__(self, birthdate_str=None):
        self._birthdate = None
        if birthdate_str is not None:
            super().__init__(birthdate_str)
            self.birthdate = birthdate_str

    @property
    def birthdate(self):
        return self._birthdate

    @birthdate.setter
    def birthdate(self, birthdate_str):
        if birthdate_str is None:
            self._birthdate = None
        else:
            try:
                self._birthdate = datetime.datetime.strptime(birthdate_str, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError('Incorrect birthday date format entered! It must be "[year]-[month]-[day]" ')


class Record:
    def __init__(self, name, birthdate = None):
        self.name = Name(name)
        self.birthdate = Birthday(birthdate)
        self.phones = []

    def __str__(self):
        phone_str = ", ".join(str(i) for i in self.phones)
        return f"Contact name: {self.name}, phones: {phone_str}"

    def days_to_birthday(self):
        if self.birthdate.birthdate:
            today = datetime.date.today()
            next_birthday = self.birthdate.birthdate.replace(year=today.year)
            if today > next_birthday:
                next_birthday = next_birthday.replace(year=today.year + 1)
            days_left = (next_birthday - today).days
            return days_left

    def add_phone(self, phone):
        phone_instance = Phone(phone)
        self.phones.append(phone_instance)

    def remove_phone(self, removed_phone):
        for phone in self.phones:
            if phone.value == removed_phone:
                self.phones = list(filter(lambda x: x != phone, self.phones))

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def edit_phone(self, old_phone, new_phone):
        found = False
        for phone in self.phones:
            if old_phone == phone.value:
                phone.value = new_phone
                found = True
                return found
        if found == False:
            raise ValueError

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, record):
        if record in self.data.keys():
            return self.data.get(record)

    def delete(self, record):
        if record in self.data:
            del self.data[record]

    def packing_data(self, filename):
        with open(filename, 'wb') as fh:
            pickle.dump(self.data, fh)

    def unpacking_data(self, filename):
        try:
            with open(filename, 'rb') as fh:
                file = pickle.load(fh)
                return file
        except Exception as e:
            print(f'Error: {e}')
            return None

    def searching(self, user_info):
        matching_records = []
        for record in self.data.values():
            if (user_info.lower() in record.name.value.lower()) or any(user_info in phone.value for phone in record.phones):
                matching_records.append(str(record))
        if matching_records:
            print(matching_records)
        else:
            print("No matches found!")

    # def __iter__(self):
    #     return iter(self.data.values())


class AddressBookIterator:
    def __init__(self, address_book, n=1):
        self.address_book = address_book
        self.n = n
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= self.n:
            raise StopIteration
        records = list(self.address_book.data.values())[self.index:self.index + self.n]
        self.index += self.n
        return [str(record) for record in records]