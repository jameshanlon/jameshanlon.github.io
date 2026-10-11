from pathlib import Path

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--output-dir",
        default="output",
        help="Directory holding the built site to check.",
    )


@pytest.fixture(scope="session")
def output_dir(request):
    path = Path(request.config.getoption("--output-dir"))
    if not path.is_dir():
        pytest.skip(f"{path} does not exist; run 'make html' first")
    return path
