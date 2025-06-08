from datetime import datetime
import time
class SingletonMeta(type):
    _instances = {}
    def __call__(cls,*args,**kwargs):

        if cls not in cls._instances:
            cls._instances[cls]=super().__call__(*args,**kwargs)

        return cls._instances[cls]

class Singelton_Service_One(metaclass=SingletonMeta):

    def __init__(self,value):
        self.value = value
        self.counter = 0
        self.start_time = datetime.now()
    def get_count_info(self):
        return f"Counter: {self.counter}, " \
               f"Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}," \
               f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

class Singelton_Service_Two(metaclass=SingletonMeta):

    def __init__(self,value):
        self.value = value
        self.counter = 0
        self.start_time = datetime.now()
    def get_count_info(self):
        return f"Counter: {self.counter}, " \
               f"Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}," \
               f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

class Singelton_Service_Three(metaclass=SingletonMeta):

    def __init__(self,value):
        self.value = value
        self.counter = 0
        self.start_time = datetime.now()
    def get_count_info(self):
        return f"Counter: {self.counter}, " \
               f"Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}," \
               f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

s11 = Singelton_Service_One("Singleton Service call One")
s21 = Singelton_Service_Two("Singleton Service call Two")
s31 = Singelton_Service_Three("Singleton Service call Three")
for i in range(10):
    s11.counter += 1
    if i % 2 == 0:
        time.sleep(1)
        s21.counter += 1
    if i % 3 == 0:
        time.sleep(2)
        s31.counter += 1
print(s11.get_count_info())
print(s21.get_count_info())
print(s31.get_count_info())


