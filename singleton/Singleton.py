from datetime import datetime
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
        self.start_time = datetime.now()
    def get_count_info(self):
        return f"Counter: {self.counter}, " \
               f"Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}," \
               f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"





