import time


def task(name, delay):
    print(f"Task {name} started")
    time.sleep(delay)
    print(f"Task {name} finished")


task("A", 2)
task("B", 2)
task("C", 2)
