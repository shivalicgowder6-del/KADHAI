def test_create_session_lands_on_first_scene(client):
    response = client.post("/api/sessions", json={"story_id": "fixture-elephant-moon"})
    assert response.status_code == 200
    body = response.json()
    assert body["session"]["story_id"] == "fixture-elephant-moon"
    assert body["session"]["current_scene_id"] == "n1"
    assert body["scene"]["scene_id"] == "n1"
    assert body["scene"]["interaction"] is None
    assert body["scene"]["is_ending"] is False


def test_create_session_with_unknown_story_returns_404(client):
    response = client.post("/api/sessions", json={"story_id": "does-not-exist"})
    assert response.status_code == 404


def test_get_session_returns_state(client):
    created = client.post("/api/sessions", json={"story_id": "fixture-elephant-moon"}).json()
    session_id = created["session"]["session_id"]

    response = client.get(f"/api/sessions/{session_id}")
    assert response.status_code == 200
    assert response.json()["current_scene_id"] == "n1"


def test_get_unknown_session_returns_404(client):
    response = client.get("/api/sessions/does-not-exist")
    assert response.status_code == 404


def test_get_session_state_returns_current_scene(client):
    created = client.post("/api/sessions", json={"story_id": "fixture-elephant-moon"}).json()
    session_id = created["session"]["session_id"]

    response = client.get(f"/api/sessions/{session_id}/state")
    assert response.status_code == 200
    assert response.json()["scene_id"] == "n1"


def test_full_deterministic_playthrough_ask_help_branch(client):
    created = client.post("/api/sessions", json={"story_id": "fixture-elephant-moon"}).json()
    session_id = created["session"]["session_id"]

    # n1 is linear -> advance with no option_id
    turn1 = client.post(f"/api/sessions/{session_id}/turns", json={})
    assert turn1.status_code == 200
    assert turn1.json()["scene"]["scene_id"] == "n2"
    assert turn1.json()["scene"]["interaction"] is not None

    # n2 is a branch -> must supply a valid option_id
    turn2 = client.post(f"/api/sessions/{session_id}/turns", json={"option_id": "ask_help"})
    assert turn2.status_code == 200
    body = turn2.json()
    assert body["scene"]["scene_id"] == "n3a"
    assert body["scene"]["is_ending"] is True
    assert body["session"]["completed_at"] is not None
    assert body["session"]["choices"] == ["ask_help"]


def test_full_deterministic_playthrough_find_path_branch(client):
    created = client.post("/api/sessions", json={"story_id": "fixture-elephant-moon"}).json()
    session_id = created["session"]["session_id"]

    client.post(f"/api/sessions/{session_id}/turns", json={})
    turn2 = client.post(f"/api/sessions/{session_id}/turns", json={"option_id": "find_path"})
    assert turn2.status_code == 200
    assert turn2.json()["scene"]["scene_id"] == "n3b"
    assert turn2.json()["scene"]["is_ending"] is True


def test_turn_on_completed_session_is_rejected(client):
    created = client.post("/api/sessions", json={"story_id": "fixture-elephant-moon"}).json()
    session_id = created["session"]["session_id"]

    client.post(f"/api/sessions/{session_id}/turns", json={})
    client.post(f"/api/sessions/{session_id}/turns", json={"option_id": "ask_help"})

    response = client.post(f"/api/sessions/{session_id}/turns", json={})
    assert response.status_code == 400


def test_invalid_option_id_on_branch_scene_is_rejected(client):
    created = client.post("/api/sessions", json={"story_id": "fixture-elephant-moon"}).json()
    session_id = created["session"]["session_id"]

    client.post(f"/api/sessions/{session_id}/turns", json={})
    response = client.post(f"/api/sessions/{session_id}/turns", json={"option_id": "not_a_real_option"})
    assert response.status_code == 400


def test_missing_option_id_on_branch_scene_is_rejected(client):
    created = client.post("/api/sessions", json={"story_id": "fixture-elephant-moon"}).json()
    session_id = created["session"]["session_id"]

    client.post(f"/api/sessions/{session_id}/turns", json={})
    response = client.post(f"/api/sessions/{session_id}/turns", json={})
    assert response.status_code == 400


def test_option_id_on_linear_scene_is_rejected(client):
    created = client.post("/api/sessions", json={"story_id": "fixture-elephant-moon"}).json()
    session_id = created["session"]["session_id"]

    response = client.post(f"/api/sessions/{session_id}/turns", json={"option_id": "ask_help"})
    assert response.status_code == 400


def test_turn_on_unknown_session_returns_404(client):
    response = client.post("/api/sessions/does-not-exist/turns", json={})
    assert response.status_code == 404
