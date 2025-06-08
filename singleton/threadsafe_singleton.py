import threading

class Singleton:
    _instance = None
    _lock = threading.Lock()  # Lock object to synchronize threads

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                # Double-checked locking
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

# Example usage with threads
def create_singleton_instance():
    instance = Singleton()
    print(f"Instance ID: {id(instance)}")

threads = []
for _ in range(10):
    t = threading.Thread(target=create_singleton_instance)
    threads.append(t)
    t.start()

for t in threads:
    t.join()
# OUTPUT WILL HAVE ONLY ONE INSTANCE ID :-
"""Instance ID: 2793158591120
Instance ID: 2793158591120
Instance ID: 2793158591120
Instance ID: 2793158591120
Instance ID: 2793158591120
Instance ID: 2793158591120
Instance ID: 2793158591120
Instance ID: 2793158591120
Instance ID: 2793158591120
Instance ID: 2793158591120
# All threads share the same instance ID, demonstrating thread-safe singleton behavior."""