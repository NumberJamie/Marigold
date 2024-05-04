from typing import Any

from source.validators import validators


class BaseField:
    def __init__(self, required: bool = True, unique: bool = False, primary_key: bool = False, default: Any = None,
                 vals: tuple = ()):
        self.required = required
        self.unique = unique
        self.default = default
        self.primary_key = primary_key
        self.validators = [*vals]

    def __set__(self, instance: Any, value: Any) -> None:
        self.run_validators(value)
        instance.__dict__[self.name] = value

    def __get__(self, instance: Any, owner: Any) -> Any:
        i = instance.__dict__.get(self.name)
        if i is None and self.required and self.default is None:
            raise ValueError(f'Required field {self.name} cannot have empty value')
        if i is None and self.default is not None:
            i = self.default
            if callable(self.default):
                i = self.default()
            self.run_validators(i)
            instance.__dict__[self.name] = i
        return i

    def _get_field(self) -> None:
        raise NotImplementedError('Subclasses need to implement _get_field method.')

    def __set_name__(self, owner: Any, name: str):
        self.name = name

    def get_row_query(self) -> str:
        query = [self.name, self._get_field()]
        if self.primary_key:
            query.append('PRIMARY KEY')
        if self.required and not isinstance(self, BooleanField):
            query.append('NOT NULL')
        if self.unique:
            query.append('UNIQUE')
        if self.default is not None and not callable(self.default):
            query.append(f'DEFAULT {self.default}')
        return ' '.join(query)

    def run_validators(self, value) -> None:
        for validator in self.validators:
            validator(value)


# TODO: Foreign key, ManyToMany, OneToOne


class CharField(BaseField):
    def __init__(self, min_length: int = None, max_length: int = None, **kwargs):
        self.max_length = max_length
        self.min_length = min_length
        super().__init__(**kwargs)
        if max_length is not None:
            self.validators.append(validators.MaxLengthValidator(self.max_length))
        if min_length is not None:
            self.validators.append(validators.MinLengthValidator(self.min_length))
        self.validators.append(validators.TypeValidator(str))

    def _get_field(self) -> str:
        return f'VARCHAR({self.max_length})'


class FileField(BaseField):
    def __init__(self, upload_to: str = None, min_length: int = None, max_length: int = 100, **kwargs):
        self.max_length = max_length
        self.min_length = min_length
        self.upload_to = upload_to
        super().__init__(**kwargs)
        if max_length is not None:
            self.validators.append(validators.MaxLengthValidator(self.max_length))
        if min_length is not None:
            self.validators.append(validators.MinLengthValidator(self.min_length))
        self.validators.append(validators.TypeValidator(str))

    def _get_field(self) -> str:
        return f'VARCHAR({self.max_length})'

    def url(self) -> str:
        return self.name


class IntegerField(BaseField):
    def __init__(self, min_length=None, max_length=None, **kwargs):
        self.max_length = max_length
        self.min_length = min_length
        super().__init__(**kwargs)
        if max_length is not None:
            self.validators.append(validators.MaxLengthValidator(self.max_length))
        if min_length is not None:
            self.validators.append(validators.MinLengthValidator(self.min_length))
        self.validators.append(validators.TypeValidator(int))

    def _get_field(self) -> str:
        return 'INTEGER'


class BooleanField(BaseField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators.append(validators.TypeValidator(bool))

    def _get_field(self) -> str:
        return 'BOOLEAN'
