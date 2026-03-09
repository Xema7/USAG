import pytest

@pytest.mark.asyncio
def test_rate_limit(client, admin_token):

    headers = {"Authorization": f"Bearer {admin_token}"}

    # First 3 requests should pass
    for _ in range(5):
        response = client.get("/users", headers=headers)
        assert response.status_code == 200

    # Next request should fail
    response = client.get("/users", headers=headers)
    assert response.status_code == 429