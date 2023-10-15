class BaseField:
    default_validators = []
    _value = None

    def __init__(self, required=True, validators=()):
        self.required = required
        self.validators = [*self.default_validators, *validators]

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        for validate in self.validators:
            validate(value)
        self._value = value

    def run_validators(self, value):
        for validate in self.validators:
            validate(value)


class CharField(BaseField):
    def __init__(self, max_length, **kwargs):
        self.max_length = max_length
        super().__init__(**kwargs)
        self.validators.append(self.validate_length)

    def validate_length(self, value):
        if len(value) > self.max_length:
            raise ValueError(f'Value exceeds max length of {self.max_length}')