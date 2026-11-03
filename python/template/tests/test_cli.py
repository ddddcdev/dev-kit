import json

import pytest
from typer.testing import CliRunner

from sample_app.cli import app

runner = CliRunner()


@pytest.mark.smoke
def test_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


@pytest.mark.unit
def test_hello_json() -> None:
    result = runner.invoke(app, ["hello", "--name", "x", "--json"])
    assert result.exit_code == 0
    assert json.loads(result.stdout) == {"message": "hello, x"}
