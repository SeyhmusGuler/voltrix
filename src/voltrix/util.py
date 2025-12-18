import functools
import threading
import time
from collections.abc import Callable
from typing import Any

# Trace context to track recursion depth for indentation
_trace_context = threading.local()


def trace_execution_time[F: Callable[..., Any]](func: F) -> F:
    """
    Decorator that traces the execution time of a function.
    Logs the start and end of the function call with an indented scope tree.
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Initialize depth if not set
        if not hasattr(_trace_context, "depth"):
            _trace_context.depth = 0

        depth = _trace_context.depth
        indent = "  " * depth

        # Start log
        print(f"{indent}├── [START] {func.__name__}")

        _trace_context.depth += 1
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
        finally:
            end_time = time.perf_counter()
            _trace_context.depth -= 1

            # End log
            elapsed = end_time - start_time
            print(f"{indent}└── [{elapsed:.4f}s] {func.__name__}")

        return result

    return wrapper  # type: ignore


def print_hello() -> None:
    print("Hello, World!")


# Aliases
timed = trace_execution_time
traciraptor = trace_execution_time
