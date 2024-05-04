from typing import Any


class BaseValidator:
    error = 'Something went wrong.'

    def __init__(self, limit_value: Any, error: str = None):
        self.limit_value = limit_value
        self.error = error or self.error

    def __call__(self, value: Any) -> None:
        if not self.compare(value, self.limit_value):
            raise ValueError(self.error.format(limit_value=self.limit_value, value=value))

    @staticmethod
    def compare(value: Any, limit: Any) -> None:
        raise NotImplementedError('Subclasses must implement compare method.')


class MaxLengthValidator(BaseValidator):
    error = 'Value {value} exceeds max length of {limit_value}.'

    @staticmethod
    def compare(value: Any, limit: Any) -> bool:
        return len(value) <= limit


class MinLengthValidator(BaseValidator):
    error = 'Value {value} lower then min length of {limit_value}.'

    @staticmethod
    def compare(value: Any, limit: Any) -> bool:
        return len(value) >= limit
    
    
class TypeValidator(BaseValidator):
    error = 'Value {value} is not of type {limit_value}.'

    @staticmethod
    def compare(value: Any, limit: Any) -> bool:
        return type(value) is limit
