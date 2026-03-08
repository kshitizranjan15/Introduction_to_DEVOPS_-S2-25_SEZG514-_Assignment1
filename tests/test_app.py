import json

import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app({})
    app.testing = True
    with app.test_client() as client:
        # Reset stores for each test
        app.config["WORKOUTS"] = []
        app.config["MEMBERS"] = []
        yield client


def test_index_and_health(client):
    rv = client.get("/")
    assert rv.status_code == 200
    assert rv.get_json()["status"] == "ok"

    rv = client.get("/health")
    assert rv.status_code == 200
    assert rv.get_json()["status"] == "healthy"


def test_create_and_get_workout(client):
    # create
    data = {"name": "Morning Cardio", "duration_minutes": 30}
    rv = client.post("/workouts", data=json.dumps(data), content_type="application/json")
    assert rv.status_code == 201
    body = rv.get_json()
    assert body["name"] == data["name"]

    # get
    rv = client.get("/workouts")
    assert rv.status_code == 200
    arr = rv.get_json()
    assert len(arr) == 1


def test_workout_validation(client):
    rv = client.post("/workouts", data=json.dumps({"name": "X"}), content_type="application/json")
    assert rv.status_code == 400


def test_create_and_get_member(client):
    data = {"name": "Alice", "email": "alice@example.com"}
    rv = client.post("/members", data=json.dumps(data), content_type="application/json")
    assert rv.status_code == 201
    body = rv.get_json()
    assert body["email"] == data["email"]

    rv = client.get("/members")
    assert rv.status_code == 200
    arr = rv.get_json()
    assert len(arr) == 1


def test_member_validation(client):
    rv = client.post("/members", data=json.dumps({"name": "Bob", "email": "not-an-email"}), content_type="application/json")
    assert rv.status_code == 400
