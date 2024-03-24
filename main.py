import random
import string

import models


# custom validator test
def validate_length(value):
    if len(value) < 1:
        raise ValueError(f'Value lesser then min length of {1}')


# custom id creator
def generate_token():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=8))


class Person(models.Model):
    id = models.CharField(max_length=8, primary_key=True, default=generate_token)
    name = models.CharField(max_length=8, default='Jennifer', validators=[validate_length])
    age = models.IntegerField(max_length=2)
    is_home = models.BooleanField(default=False)

    def __str__(self):
        return f"Id: {self.id}, Name: {self.name}, Age: {self.age}, Home: {self.is_home}"

    def is_old_enough(self):
        return self.age >= 18


person1 = Person.create(age=1, is_home=True)
person2 = Person.create(name="Jane Doe", age=23)

for person in Person.all():
    print(person)
    print(person.is_old_enough())

fields_info = Person.get_fields_recursively()
print(fields_info)
