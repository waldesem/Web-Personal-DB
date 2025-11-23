"""Fixtures."""

import pytest # pyright: ignore[reportMissingImports]

from app import create_app


@pytest.fixture
def app():
    """Create app."""
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        },
    )

    yield app

    # clean up / reset resources here


@pytest.fixture
def client(app):
    """Create client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create runner."""
    return app.test_cli_runner()
