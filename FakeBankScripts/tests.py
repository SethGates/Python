import requests
import pytest
import os
from dotenv import load_dotenv
load_dotenv()

USER_PORT = os.getenv("USER_PORT")
AUTH = os.getenv("AUTH_TOKEN")
UNDERWRITER_PORT = os.getenv("UNDERWRITER_PORT")
BANK_PORT = os.getenv("BANK_PORT")
TRANSACTION_PORT = os.getenv("TRANSACTION_PORT")


def test_status():
    bank_response = requests.get(f'{BANK_PORT}/health', headers={
        "Authorization": f"{AUTH}"
    })
    user_response = requests.get(f'{USER_PORT}/health', headers={
        "Authorization": f"{AUTH}"
    })
    underwriter_response = requests.get(f'{UNDERWRITER_PORT}/health', headers={
        "Authorization": f"{AUTH}"
    })
    transaction_response = requests.get(f'{TRANSACTION_PORT}/health', headers={
        "Authorization": f"{AUTH}"
    })
    assert bank_response.status_code == 200
    assert user_response.status_code == 200
    assert underwriter_response.status_code == 200
    assert transaction_response.status_code == 200


def test_content():
    bank_response = requests.get(f'{BANK_PORT}/banks', headers={
        "Authorization": f"{AUTH}"
    })
    user_response = requests.get(f'{USER_PORT}/users', headers={
        "Authorization": f"{AUTH}"
    })
    underwriter_response = requests.get(f'{UNDERWRITER_PORT}/applicants', headers={
        "Authorization": f"{AUTH}"
    })
    assert isinstance(bank_response.json()["content"], list) == True
    assert user_response.headers["Content-Type"] == "application/json"
    response = underwriter_response.json()
    assert response["content"][0]["id"] == 1


def test_login():
    user = {
        "username": "Gregory.Robinson",
        "password": "GregoryRobinson57?&"
    }
    user_response = requests.post(f'{USER_PORT}/login', json=user, headers={
        "Authorization": f"{AUTH}"
    })
    response = ["Authorization" in keys for keys in user_response.headers]
    count = response.count(True)
    assert count == 1
