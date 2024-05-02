from typing import Any


class Model:
    @classmethod
    def get_fields(cls):
        fields_info = []
        for attr_name, attr_value in cls.__dict__.items():
            if isinstance(attr_value, BaseField):
                fields_info.append(attr_value.construct_schema(attr_value))
        return fields_info
    

class BaseField:
    sql_name = None
    additional_sql = []
    
    def __init__(self, required: bool = True, primary_key: bool = False, default: Any = None, validators: set = ()):
        self.required = required
        self.primary_key = primary_key
        self.default = default
        self.validators = [*validators]
        
    def __set__(self, instance, value):
        for validator in self.validators:
            validator(value)
        instance.__dict__[self.name] = value
        
    def __set_name__(self, owner, name):
        self.name = name
        
    def construct_schema(self, value: Any) -> str:
        if not self.sql_name:
            raise NotImplementedError('sql_name needs to be implemented in subclasses of BaseField.')
        schema = [self.name, value.sql_name]
        if self.primary_key:
            schema.append('PRIMARY KEY')
        if self.required:
            schema.append('NOT NULL')
        if not callable(self.default) and self.default is not None:
            schema.append(f'DEFAULT {str(self.default)}')
        if self.additional_sql:
            schema.extend(self.additional_sql)
        return ' '.join(schema)
    

class CharField(BaseField):
    def __init__(self, unique: bool = False, max_length: int = 100, **kwargs):
        self.unique = unique
        self.max_length = max_length
        super().__init__(**kwargs)
        if self.max_length:
            self.validators.append(self.validate_charfield)
            self.sql_name = f'VARCHAR({max_length})'
        if self.unique:
            self.additional_sql = ['UNIQUE']
    
    def validate_charfield(self, value):
        if value > self.max_length:
            raise ValueError(f'Charfield exceeds max length of {self.max_length}.')
        if type(value) is not str:
            raise ValueError(f'Charfield can only be of type string.')
        
    
class BooleanField(BaseField):
    sql_name = 'BOOLEAN'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators.append(self.validate_booleanfield)
        
    @staticmethod
    def validate_booleanfield(value):
        if type(value) is not bool:
            raise ValueError(f'BooleanField can only be of type boolean.')
        