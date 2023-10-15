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
        return cls.data
    