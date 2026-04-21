from app import create_app, db


def _register_and_login(client, email: str, role: str = "doctor"):
    client.post(
        "/api/auth/register",
        json={"email": email, "password": "password123", "role": role},
    )
    res = client.post("/api/auth/login", json={"email": email, "password": "password123"})
    token = res.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_catalog_endpoints_empty_then_build(tmp_path, monkeypatch):
    # Force testing config (in-memory sqlite).
    app = create_app("testing")
    with app.app_context():
        db.create_all()

    client = app.test_client()
    headers = _register_and_login(client, "doctor@test.com", "doctor")

    # Initially empty
    res = client.get("/api/catalog/symptoms", headers=headers)
    assert res.status_code == 200
    assert res.get_json()["total"] == 0

    res = client.get("/api/catalog/diseases", headers=headers)
    assert res.status_code == 200
    assert res.get_json()["total"] == 0

