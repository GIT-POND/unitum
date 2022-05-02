from App import pydanticModels
from Tests.database import client, last_client, session

#               TEST CASES              #


def test_check_username_availability(client):
    response = client.post(
        "/auth/username_available", json={"username": "random_user"})
    assert response.status_code == 200


def test_create_account(client):
    response = client.post(
        "/auth/create_account", json={
            "username": "test_user",
            "first_name": "john",
            "last_name": "doe",
            "email": "johndoe@gmail.com",
            "password": "password123"
        })
    response_data = pydanticModels.UserAccResponse(** response.json())
    assert response_data
    assert response.status_code == 201


def test_login_account(last_client):
    response = last_client.post(
        "/auth/login_account", json={
            "email": "johndoe@gmail.com",
            "password": "password123"
        })
    assert response.status_code == 200
