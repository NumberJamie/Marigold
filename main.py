import random
import string

from source.database import models, fields


def generate_stem():
    return ''.join(random.choices(string.digits, k=8))


class Account(models.Model):
    id = fields.CharField(max_length=8, default=generate_stem, primary_key=True)
    name = fields.CharField(max_length=32, unique=True)
    avatar = fields.FileField(upload_to='profile')
    favorite = fields.BooleanField(default=False)


a1 = Account.create(name='marigold', avatar='avatar.png')
a2 = Account.create(name='marigold', avatar='avatar.png', favorite=True)

for account in Account.all():
    print(account)
print(Account.construct_table())
