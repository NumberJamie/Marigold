import re

import validators


class BaseField:
    default_validators = []
    empty_values = (None, "", [], (), {})

    def __init__(self, required=True, primary_key=False, default=None, validators=()):
        self.required = required
        self.default = default
        self.primary_key = primary_key
        self.validators = [*self.default_validators, *validators]

    def __set__(self, instance, value):
        self.run_validators(value)
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        i = instance.__dict__.get(self.name)
        if i is None and self.required and self.default is None:
            raise ValueError('Required fields cannot have empty value')
        if i is None and self.default is not None:
            i = self.default
            if callable(self.default):
                i = self.default()
            self.run_validators(i)
            instance.__dict__[self.name] = i
        return i

    def __set_name__(self, owner, name):
        self.name = name

    def get_info(self):
        return {
            "type": self.__class__.__name__,
            "required": self.required,
            "default": self.default,
            "is_primary": self.primary_key,
            "validators": self.validators
        }

    def run_validators(self, value):
        for validator in self.validators:
            validator(value)


class CharField(BaseField):
    def __init__(self, min_length=None, max_length=None, **kwargs):
        self.max_length = max_length
        self.min_length = min_length
        super().__init__(**kwargs)
        if max_length is not None:
            self.validators.append(validators.MaxLengthValidator(limit_value=self.max_length))
        if min_length is not None:
            self.validators.append(validators.MinLengthValidator(limit_value=self.min_length))


class IntegerField(BaseField):
    regex = re.compile(r'^\d+$')

    def __init__(self, min_length=None, max_length=None, **kwargs):
        self.max_length = max_length
        self.min_length = min_length
        super().__init__(**kwargs)
        if max_length is not None:
            self.validators.append(validators.MaxLengthValidator(limit_value=self.max_length))
        if min_length is not None:
            self.validators.append(validators.MinLengthValidator(limit_value=self.min_length))
        self.validators.append(validators.RegexValidator(limit_value=self.regex,
                                                         error='IntegerField needs to be a whole number.'))


class BooleanField(BaseField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators.append(self.validate)

    def validate(self, value):
        if type(value) is not bool and self.required:
            raise ValueError('BooleanField has to be of type bool.')
