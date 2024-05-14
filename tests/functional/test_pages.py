def test_landing_page(client):
    response = client.get("/")
    html = response.data.decode()

    assert response.status_code == 200