"""Unit test untuk aplikasi Flask menggunakan pytest."""
import pytest
from app import app, init_db


@pytest.fixture
def client():
    """Inisialisasi test client Flask dan database testing."""
    init_db()
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_index_page(client):
    """Memastikan halaman login utama berhasil dimuat (HTTP 200)."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Portal Login" in response.data


def test_login_success(client):
    """Memastikan login berhasil dengan kredensial benar."""
    response = client.post(
        "/",
        data={"username": "admin", "password": "supersecret"},  # nosemgrep
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Login Berhasil!".encode("utf-8") in response.data


def test_login_failed(client):
    """Memastikan login gagal jika kredensial salah."""
    response = client.post(
        "/",
        data={"username": "salah", "password": "salah"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Login Gagal!".encode("utf-8") in response.data
