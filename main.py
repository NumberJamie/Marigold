import models


# custom validator test
def validate_length(value):
    if len(value) < 1:
        raise ValueError(f'Value lesser then min length of {1}')


class Person(models.Model):
    name = models.CharField(max_length=8, default='Jennifer')
    age = models.CharField(max_length=2, required=False)

    def __str__(self):
        return f"Name: {self.name}, Age: {self.age}"


person1 = Person.add()
person2 = Person.add(name="Jane Doe", age="23")

for person in Person.all():
    print(person)
