import models


# custom validator test
def validate_length(value):
    if len(value) < 1:
        raise ValueError(f'Value lesser then min length of {1}')


class Person(models.Model):
    name = models.CharField(max_length=8)
    age = models.CharField(max_length=2, validators=(validate_length, ))

    def __str__(self):
        return f"Name: {self.name}, Age: {self.age}"


person1 = Person.add(name="John Doe", age="0")
person2 = Person.add(name="Jane Doe", age="233")

for person in Person.all():
    print(person)
