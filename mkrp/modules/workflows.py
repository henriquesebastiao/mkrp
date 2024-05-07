CI_PYTHON = r"""on: [ push, pull_request ]

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
          task ${{ matrix.check }}"""
