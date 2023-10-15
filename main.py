import models


# custom validator test
def validate_length(value):
    if len(value) < 1:
        raise ValueError(f'Value lesser then min length of {1}')


class Person(models.Model):
    name = models.CharField(max_length=8, default='Jennifer')
    age = models.IntegerField(max_length=2)
    is_home = models.BooleanField(default=False)

    def __str__(self):
        return f"Name: {self.name}, Age: {self.age}, Home: {self.is_home}"


person1 = Person.add(age=1, is_home=True)
person2 = Person.add(name="Jane Doe", age=23)

for person in Person.all():
    print(person)
