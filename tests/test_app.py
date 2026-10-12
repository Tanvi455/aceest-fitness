import pytest

from app import create_app


@pytest.fixture
def client():
	app = create_app(initial_classes=[])
	app.config["TESTING"] = True
	with app.test_client() as test_client:
		yield test_client


def test_health_check(client):
	response = client.get("/health")

	assert response.status_code == 200
	assert response.get_json() == {"status": "healthy"}


def test_create_and_get_class(client):
	response = client.post(
		"/classes",
		json={"name": "Pilates", "instructor": "Taylor Reed", "capacity": 8},
	)

	assert response.status_code == 201
	created_class = response.get_json()
	assert created_class["id"] == 1
	assert created_class["name"] == "Pilates"
	assert created_class["capacity"] == 8

	detail_response = client.get("/classes/1")
	assert detail_response.status_code == 200
	assert detail_response.get_json() == created_class


def test_create_class_rejects_invalid_capacity(client):
	response = client.post(
		"/classes",
		json={"name": "Pilates", "instructor": "Taylor Reed", "capacity": 0},
	)

	assert response.status_code == 400
	assert response.get_json() == {"error": "Capacity must be a positive integer."}


def test_missing_class_returns_not_found(client):
	response = client.get("/classes/999")

	assert response.status_code == 404
	assert response.get_json() == {"error": "Class not found."}
