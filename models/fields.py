import validators


class BaseField:
    default_validators = []

    def __init__(self, required=True, validators=()):
        self.required = required
        self.validators = [*self.default_validators, *validators]

    def __set__(self, instance, value):
        self.run_validators(value)
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name

    def run_validators(self, value):
        for validate in self.validators:
            validate(value)


class CharField(BaseField):
    def __init__(self, min_length=None, max_length=None, **kwargs):
        self.max_length = max_length
        self.min_length = min_length
        super().__init__(**kwargs)
        if max_length is not None:
            self.validators.append(validators.MaxLengthValidator(limit_value=self.max_length))
        if min_length is not None:
            self.validators.append(validators.MinLengthValidator(limit_value=self.min_length))
