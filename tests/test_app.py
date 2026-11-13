import app


def client():
    app.app.config["TESTING"] = True
    return app.app.test_client()


def test_health():
    response = client().get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"ok": True}


def test_normal_note_is_shown():
    response = client().post(
        "/",
        data={
            "recipient": "Maya",
            "sender": "Devon",
            "note": "Thanks for staying late.",
        },
    )
    page = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Dear Maya" in page
    assert "Thanks for staying late." in page
    assert "Devon" in page


def test_template_braces_stay_text():
    response = client().post(
        "/",
        data={
            "recipient": "Maya",
            "sender": "Devon",
            "note": "{{ config.DESK_CODE }}",
        },
    )
    page = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "LETTER-8830" not in page
    assert "{{ config.DESK_CODE }}" in page


def test_html_in_the_note_is_not_markup():
    response = client().post(
        "/",
        data={
            "recipient": "Maya",
            "sender": "Devon",
            "note": "<b>thanks</b>",
        },
    )
    page = response.get_data(as_text=True)
    assert "<b>thanks</b>" not in page
    assert "&lt;b&gt;thanks&lt;/b&gt;" in page


def test_example_notes_still_render():
    page = client().get("/").get_data(as_text=True)
    assert "the shop volunteers" in page
    assert "Thanks for covering the Thursday screening booth." in page
