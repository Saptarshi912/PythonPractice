class SingletonMeta(type):
    _instances = {}
    def __call__(cls,*args,**kwargs):

        if cls not in cls._instances:
            cls._instances[cls]=super().__call__(*args,**kwargs)

        return cls._instances[cls]

class Singleton(metaclass=SingletonMeta):

    def __init__(self,value):
        self.value = value
        self.counter = 0
    def get_value(self):
        return self.value



