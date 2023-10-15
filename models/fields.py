import validators


class BaseField:
    default_validators = []
    empty_values = (None, "", [], (), {})

    def __init__(self, required=True, default=None, validators=()):
        self.required = required
        self.default = default
        self.validators = [*self.default_validators, *validators]

    def __set__(self, instance, value):
        self.run_validators(value)
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        i = instance.__dict__.get(self.name)
        if i is None and self.required and self.default is None:
            raise ValueError('Required fields cannot have empty value')
        if i is None and self.default is not None:
            self.run_validators(self.default)
            return self.default
        return i

    def __set_name__(self, owner, name):
        self.name = name

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


class BooleanField(BaseField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators.append(self.validate)

    def validate(self, value):
        if not type(value) == bool and self.required:
            raise ValueError('BooleanField has to be of type bool.')
