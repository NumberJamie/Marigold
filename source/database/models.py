from source.database.fields import BaseField


class Model:
    data = []

    def __init__(self):
        self.data.append(self)
        
    def __str__(self):
        return f'{self.__dict__}'

    @classmethod
    def create(cls, **kwargs) -> 'Model':
        instance = cls()
        for attr_name, attr_value in cls.__dict__.items():
            if isinstance(attr_value, BaseField):
                if kwargs.get(attr_name):
                    setattr(instance, attr_name, kwargs[attr_name])
                    continue
                setattr(instance, attr_name, getattr(instance, attr_name))
        return instance

    @classmethod
    def all(cls) -> list:
        return cls.data

    @classmethod
    def construct_table(cls) -> str:
        rows = []
        for _, attr_value in cls.__dict__.items():
            if isinstance(attr_value, BaseField):
                rows.append(attr_value.get_row_query())
        return f'CREATE TABLE IF NOT EXISTS {cls.__name__.lower()} ({", ".join(rows)});'
    