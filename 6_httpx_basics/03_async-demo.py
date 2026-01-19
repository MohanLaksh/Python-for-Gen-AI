import asyncio
import time


async def task(name, delay):
    print(f"Task {name} started")
    await asyncio.sleep(delay)
    print(f"Task {name} finished")


async def main():
    start_time = time.time()
    await asyncio.gather(
        task("A", 2),
        task("B", 4),
        task("C", 2)
    )
    print(time.time() - start_time)

asyncio.run(main())
