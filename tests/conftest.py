import pytest
from app import create_app
from app.models import database

@pytest.fixture
def app():
    app = create_app()
    app.config.from_object('config.TestConfig') 
    return app

@pytest.fixture
def client(app):
    print("Creating database")
    with app.test_client() as client:
        with app.app_context():
            database.create_all()
        yield client
        with app.app_context():
            database.drop_all()
    print("Database dropped")
