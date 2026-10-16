from fastapi.testclient import TestClient
from app.api.auth import get_current_user
from app.db.models import User
from app.main import app


def test_dashboard_requires_login():
    with TestClient(app, backend_options={"use_uvloop": True}) as client:
        response = client.get("/api/admin/dashboard")

    assert response.status_code == 401
def test_dashboard_requires_admin():
    def fake_current_user():
        return User(is_admin=False)

    app.dependency_overrides[get_current_user] = fake_current_user

    try:
        with TestClient(app, backend_options={"use_uvloop": True}) as client:
            response = client.get("/api/admin/dashboard")

        assert response.status_code == 403
    finally:
        app.dependency_overrides.pop(get_current_user, None)
    