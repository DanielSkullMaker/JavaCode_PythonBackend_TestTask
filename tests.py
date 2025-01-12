"""
Тесты для эндпойнтов
"""

from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.api.routers import main_router
import requests

app = FastAPI()
app.include_router(main_router)
client = TestClient(app)

host = "http://localhost:8000"
headers = {'Content-Type': 'application/json'}


def test_read_root():
    """
    Запуск API
    """
    responce = client.get("/docs")
    assert responce.status_code == 200


def test_create_wallet_true():
    """
    Создание корректного кошелька
    """
    data = {
        "amount": 10
    }
    responce = client.post("/api/v1/wallets/", json=data)
    global wallet_uuid  # Тестовый кошелек будет использован другими тестами
    wallet_uuid = responce.json()['id']
    assert responce.status_code == 201


def test_create_wallet_false():
    """
    Попытка создания некорректного кошелька - Баланс не меньше 0
    """
    data = {
        "amount": -1
    }
    responce = client.post("/api/v1/wallets/", json=data)
    assert responce.status_code == 422


def test_get_wallet():
    """
    Получаем баланс запросом
    """
    responce = requests.get(f"{host}/api/v1/wallets/{wallet_uuid}")
    assert float(responce.json()['amount']) == 10.00
    assert responce.status_code == 200


def test_operation_deposit():
    """
    Внести депозит
    """
    data = {
        "amount": 100,
        "operationType": "DEPOSIT"
    }
    responce = requests.post(f"{host}/api/v1/wallets/{wallet_uuid}/operation", json=data, headers=headers)
    assert responce.status_code == 201


def test_operation_withdraw():
    """
    Вывести деньги
    """
    data = {
        "amount": 100,
        "operationType": "WITHDRAW"
    }
    responce = requests.post(f"{host}/api/v1/wallets/{wallet_uuid}/operation", json=data, headers=headers)
    assert responce.status_code == 201


def test_operation_negative_withdraw():
    """
    Попытка вывести с кошелька больше денег чем имеется на счету
    """
    data = {
        "amount": 999,
        "operationType": "WITHDRAW"
    }
    responce = requests.post(f"{host}/api/v1/wallets/{wallet_uuid}/operation", json=data, headers=headers)
    assert responce.status_code == 400
