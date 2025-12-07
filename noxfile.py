import nox

nox.options.default_venv_backend = "uv"


@nox.session(python=["3.12", "3.13", "3.14"])
def tests(session: nox.Session) -> None:
    session.run("uv", "sync", "--dev", external=True)
    session.run("pytest", "-q", external=True)


@nox.session
def lint(session: nox.Session) -> None:
    session.run("uv", "run", "ruff", "check", ".", external=True)
    session.run("uv", "run", "ruff", "format", ".", external=True)


@nox.session
def typecheck(session: nox.Session) -> None:
    session.run("uv", "sync", "--dev", external=True)
    session.run("uv", "run", "mypy", "src", external=True)
