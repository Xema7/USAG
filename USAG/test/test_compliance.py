import pytest

@pytest.mark.asyncio
def test_user_cannot_access_audit(client, user_token):
    response = client.get(
        "/audit/logs",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403

@pytest.mark.asyncio
def test_admin_can_access_audit(client, admin_token):
    response = client.get(
        "/audit/logs",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code in [200, 204]