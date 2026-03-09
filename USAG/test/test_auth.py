import pytest

@pytest.mark.asyncio
def test_protected_without_token(client):
    response = client.get("/users")
    assert response.status_code == 401


@pytest.mark.asyncio
def test_protected_with_admin(client, admin_token):
    response = client.get(
        "/users",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200