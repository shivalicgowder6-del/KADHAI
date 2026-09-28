def test_fixture_story_route_still_works(client):
    response = client.get("/api/stories/fixture-elephant-moon")
    assert response.status_code == 200
    body = response.json()
    assert body["story_id"] == "fixture-elephant-moon"
    assert body["title"]["en"]
    assert body["title"]["ta"]


def test_generic_story_route_returns_same_story(client):
    response = client.get("/api/stories/fixture-elephant-moon")
    assert response.status_code == 200
    assert response.json()["story_id"] == "fixture-elephant-moon"


def test_unknown_story_id_returns_404(client):
    response = client.get("/api/stories/does-not-exist")
    assert response.status_code == 404
