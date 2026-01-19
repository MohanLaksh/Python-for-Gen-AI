import time


def task(name, delay):
    print(f"Task {name} started")
    time.sleep(delay)
    print(f"Task {name} finished")

start_time = time.time()
task("A", 2)
print(time.time() - start_time)
task("B", 2)
print(time.time() - start_time)
task("C", 2)
print(time.time() - start_time)