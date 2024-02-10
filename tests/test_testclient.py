from fastapi.testclient import TestClient
from webcur.main import app_factory


app = app_factory()
client = TestClient(app)
routes = app.routes

print([route.path for route in routes])
