# Make Repository

[![CI](https://github.com/henriquesebastiao/mkrp/actions/workflows/ci.yml/badge.svg)](https://github.com/henriquesebastiao/mkrp/actions/workflows/ci.yml)
[![Coverage](img/coverage.svg)](https://github.com/henriquesebastiao/mkrp)
[![PyPI version](https://badge.fury.io/py/mkrp.svg)](https://badge.fury.io/py/mkrp)

`mkrp` is a command-line tool for initial configuration of tools for a new repository.

`mkrp` was designed to speed up the creation of configurations that I (the author, [@henriquesebastiao](https://twitter.com/hick_hs)) commonly use in my projects (Python preferably). If you see any use in this, feel free to use it and improve it if you want.

## Installation

The CLI is available on PyPI and can be installed using `pip` or `pipx`:

```bash
pipx install mkrp
```

## Usage

The following command creates the following configurations:

- `.gitignore` file for Python projects
- GitHub Actions for Python projects that perform the integration tasks are listed below.
- Add development tool settings to `pyproject.toml` for Python projects

Tools configured for Python projects:
- `ruff` - Linting
- `blue` - Formatting
- `isort` - Sorting imports
- `mypy` - Static type checking
- `radon` - Code complexity checking
- `bandit` - Security checking
- `pydocstyle` - Docstring checking
- `pytest` - Testing
- `taskipy` - Task runner

```bash
mkrp python
```

Also configuring a license for the repository with the flag `-l` or `--license`:

```bash
mkrp python -l
```

By default, the MIT license will be configured.

## Sources

- The `.gitignore` file is generated with the [gitignore.io](https://www.toptal.com/developers/gitignore) api
- GitHub Actions CI configurations are configured according to the following model:

```yaml
on: [ push, pull_request ]

name: CI

jobs:
  checks:
    name: Checks
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [ 3.12 ]
        check: [ ruff, blue, isort, pydocstyle, radon, mypy, bandit ]

    steps:
      - uses: actions/checkout@v4
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install poetry
          poetry config virtualenvs.create false
          poetry install
      - name: Run checks
        run: |
          task ${{ matrix.check }}
```

- The development tool settings are configured in the `pyproject.toml` file according to the following model:

```toml
[tool.mypy]
ignore_missing_imports = true
check_untyped_defs = true

[tool.isort]
profile = "black"
line_length = 79

[tool.ruff]
line-length = 79
indent-width = 4

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F403", "F401"]
"tests/*" = ["F401", "F811"]

[tool.pytest.ini_options]
pythonpath = "."
python_files = "test.py tests.py test_*.py tests_*.py *_test.py *_tests.py"

[tool.taskipy.tasks]
ruff = "ruff check ."
blue = "blue --check . --diff"
isort = "isort --check --diff ."
mypy = "mypy -p <YOUR-PROJECT>"
radon = "radon cc ./<YOUR-PROJECT> -a -na"
bandit = "bandit -r ./<YOUR-PROJECT>"
pydocstyle = "pydocstyle ./<YOUR-PROJECT> --count --convention=google --add-ignore=D100,D104,D105,D107"
lint = "task ruff && task blue && task isort"
format = 'blue .  && isort .'
quality = "task mypy && task radon && task pydocstyle"
pre_test = "task lint"
test = "pytest -s -x --cov=<YOUR-PROJECT> -vv"
post_test = "coverage html"
export-requirements = "rm requirements.txt && poetry export -f requirements.txt --output requirements.txt --without-hashes"
ready = "task lint && task quality && task bandit && pytest -s -x --cov=<YOUR-PROJECT> -vv && task export-requirements"
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.