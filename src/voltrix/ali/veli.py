import time

from voltrix.util import traciraptor


@traciraptor
def print_veli() -> None:
    print("Hello from Veli!")


@traciraptor
def inner_func_1():
    print("Hello from inner_func_1")
    time.sleep(1)


@traciraptor
def inner_func_2():
    print("Hello from inner_func_2")
    time.sleep(1)


@traciraptor
def outer_func():
    print("Hello from outer_func")
    inner_func_1()
    time.sleep(3)
    inner_func_2()


if __name__ == "__main__":
    outer_func()
