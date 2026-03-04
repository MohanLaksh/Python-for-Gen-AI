


from langserve import RemoteRunnable

SERVER_URL = "http://localhost:8000"

debugger = RemoteRunnable(f"{SERVER_URL}/debug/")


def demo_invoke():
    result = debugger.invoke({
        "code": """def calculate_average(numbers):
    total = sum(numbers)
    return total / len(numbers)""",
        "error_messages": "ZeroDivisionError: division by zero",
        "language": "python",
    })
    print(result)


if __name__ == "__main__":
    demo_invoke()