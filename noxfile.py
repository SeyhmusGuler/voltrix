import glob

import nox

nox.options.default_venv_backend = "uv"


@nox.session(python=["3.12", "3.13"])
def tests(session: nox.Session) -> None:
    session.install("build", "pytest", "pytest-cov")
    # Build the project, then install the wheel to test the installed artifact
    session.run("python", "-m", "build", "--wheel", "--sdist")
    session.run("uv", "pip", "install", *glob.glob("dist/*.whl"))
    session.run("pytest", "-q")


@nox.session
def lint(session: nox.Session) -> None:
    session.install("ruff")
    session.run("ruff", "check", ".")
    session.run("ruff", "format", ".")


@nox.session
def typecheck(session: nox.Session) -> None:
    session.install(".", "mypy", "pandas-stubs")
    session.run("mypy", "src")
