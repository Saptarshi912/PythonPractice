import threading
import time

class UnsafeSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            # Simulate delay to increase race condition likelihood
            time.sleep(0.1)
            cls._instance = super().__new__(cls)
        return cls._instance

instances = []

def create_instance():
    instance = UnsafeSingleton()
    instances.append(instance)
    print(f"Instance ID: {id(instance)}")

threads = []
for _ in range(10):
    t = threading.Thread(target=create_instance)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

unique_instances = set(instances)
print(f"Number of unique instances created: {len(unique_instances)}")

# OUTPUT MULTIPLE INSTANCES RACE CONDITIONS
"""
Instance ID: 2847695819664
Instance ID: 2847695533008
Instance ID: 2847695774608
Instance ID: 2847695816144
Instance ID: 2847695816464
Instance ID: 2847695817040
Instance ID: 2847695817744
Instance ID: 2847695818256
Instance ID: 2444334711440
Instance ID: 2444334711440
Number of unique instances created: 10"""
