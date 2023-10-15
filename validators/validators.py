class BaseValidator:
    error = 'Something went wrong.'

    def __init__(self, limit_value, error=None):
        self.limit_value = limit_value
        self.error = error or self.error

    def __call__(self, value):
        if not self.compare(value, self.limit_value):
            raise ValueError(self.error.format(limit_value=self.limit_value))

    @staticmethod
    def compare(value, limit):
        raise NotImplementedError("Subclasses must implement compare method.")


class MaxLengthValidator(BaseValidator):
    error = 'Value exceeds max length of {limit_value}.'

    @staticmethod
    def compare(value, limit):
        return len(value) <= limit


class MinLengthValidator(BaseValidator):
    error = 'Value lower then min length of {limit_value}.'

    @staticmethod
    def compare(value, limit):
        return len(value) >= limit
