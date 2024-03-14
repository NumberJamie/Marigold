from models.fields import BaseField


class Model:
    data = []

    def __init__(self):
        self.fields = {}
        self.data.append(self)

    @classmethod
    def create(cls, **kwargs):
        instance = cls()
        for key, value in kwargs.items():
            setattr(instance, key, value)
        return instance

    @classmethod
    def all(cls):
        print(cls.__name__)
        return cls.data

    @classmethod
    def get_fields_recursively(cls):
        fields_info = {}
        for subclass in cls.__subclasses__():
            fields_info.update(subclass.get_fields_recursively())
        fields_info.update(cls.get_fields())
        return fields_info

    @classmethod
    def get_fields(cls):
        fields_info = {}
        for attr_name, attr_value in cls.__dict__.items():
            if isinstance(attr_value, BaseField):
                fields_info[attr_name] = attr_value.get_info()
        return fields_info
