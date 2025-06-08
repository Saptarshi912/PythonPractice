import threading

class EagerSingleton:
    # Eagerly create the singleton instance at class load time
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        # This method will always return the same instance
        return cls._instance

    def __init__(self, value=None):
        # Optional initialization parameter, only effective once
        if not hasattr(self, '_initialized'):
            self.value = value
            self._initialized = True

# Create the singleton instance eagerly (thread-safe)
with EagerSingleton._lock:
    if EagerSingleton._instance is None:
        EagerSingleton._instance = super().__new__(EagerSingleton)
        # Initialize with default or desired parameters here if needed
        EagerSingleton._instance.__init__(value="Initial Value")

# Usage example
s1 = EagerSingleton()
s2 = EagerSingleton()

print(s1 is s2)           # True
print(s1.value)           # Initial Value
print(s2.value)           # Initial Value

# Changing value via one reference affects the other
s1.value = "Changed"
print(s2.value)           # Changed
