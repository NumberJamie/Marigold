import models


class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.CharField(max_length=2)

    def __str__(self):
        return f"Name: {self.name}, Age: {self.age}"


person1 = Person.add(name="John Doe", age="30")
person2 = Person.add(name="Jane Doe", age="25")

for person in Person.all():
    print(person)
