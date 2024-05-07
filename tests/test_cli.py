import os
import shutil
from pathlib import Path

from typer.testing import CliRunner

from mkrp.cli import __version__, app

runner = CliRunner()


path = Path(__file__).resolve().parent.parent / 'repo'


def test_message_without_command():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert 'USAGE' in result.stdout


def test_version():
    result = runner.invoke(app, ['--version'])
    assert result.exit_code == 0
    assert 'mkrp' in result.stdout
    assert 'Developed' in result.stdout


def test_comand_python_without_license():
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path)
    os.chdir(path)
    result = runner.invoke(app, ['python'])
    assert result.exit_code == 0
    assert os.path.isfile('.gitignore')
    assert os.path.isfile('.github/workflows/ci.yml')
    assert os.path.isfile('pyproject.toml')
    assert not os.path.isfile('LICENSE')
    assert '.gitignore' in result.stdout
    assert '.github/workflows/ci.yml' in result.stdout
    assert 'LICENSE.md' not in result.stdout
    assert 'pyproject.toml' in result.stdout


def test_comand_python_with_license():
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path)
    os.chdir(path)
    result = runner.invoke(app, ['python', '-l'])
    assert result.exit_code == 0
    assert os.path.isfile('.gitignore')
    assert os.path.isfile('.github/workflows/ci.yml')
    assert os.path.isfile('pyproject.toml')
    assert os.path.isfile('LICENSE')
    assert '.gitignore' in result.stdout
    assert '.github/workflows/ci.yml' in result.stdout
    assert 'LICENSE.md' in result.stdout
    assert 'pyproject.toml' in result.stdout

