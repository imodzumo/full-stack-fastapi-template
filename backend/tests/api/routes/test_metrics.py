from fastapi.testclient import TestClient

from app.core.config import settings


def test_read_metrics_as_admin(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/metrics/", headers=superuser_token_headers)
    assert r.status_code == 200
    assert r.json()["message"] == "Metrics are available for admin and manager roles."


def test_read_metrics_as_manager(
    client: TestClient, manager_token_headers: dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/metrics/", headers=manager_token_headers)
    assert r.status_code == 200
    assert r.json()["message"] == "Metrics are available for admin and manager roles."


def test_read_metrics_as_member(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/metrics/", headers=normal_user_token_headers)
    assert r.status_code == 403
