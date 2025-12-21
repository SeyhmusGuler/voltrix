import time

from voltrix.util import timed, trace_execution_time, traciraptor


def test_decorator_metadata():
    """Verify decorator preserves function metadata."""

    @trace_execution_time
    def my_func():
        """My docstring."""
        pass

    assert my_func.__name__ == "my_func"
    assert my_func.__doc__ == "My docstring."


def test_output_format(capsys):
    """Verify output format and aliases."""

    @traciraptor
    def quick_func():
        time.sleep(0.001)

    quick_func()

    captured = capsys.readouterr()
    stdout = captured.out

    assert "├── [START] quick_func" in stdout
    assert "└── [" in stdout
    assert "] quick_func" in stdout


def test_nested_scoping(capsys):
    """Verify nested calls produce indented tree structure."""

    @timed
    def outer():
        inner_1()
        inner_2()

    @traciraptor
    def inner_1():
        nested_deep()

    @timed
    def inner_2():
        pass

    @trace_execution_time
    def nested_deep():
        pass

    outer()

    captured = capsys.readouterr()
    stdout = captured.out
    _ = stdout.strip().split("\n")

    # Expected structure roughly:
    # ├── [START] outer
    #   ├── [START] inner_1
    #     ├── [START] nested_deep
    #     └── [...] nested_deep
    #   └── [...] inner_1
    #   ├── [START] inner_2
    #   └── [...] inner_2
    # └── [...] outer

    # Check for START logs
    assert "├── [START] outer" in stdout
    assert "  ├── [START] inner_1" in stdout
    assert "    ├── [START] nested_deep" in stdout

    # Check for END logs (using regex or simple substring for structure)
    # verifying indentation for end logs
    assert "└── [" in stdout
    assert "  └── [" in stdout
    assert "    └── [" in stdout
