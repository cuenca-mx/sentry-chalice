from pytest_chalice.handlers import RequestHandler


def test_exception_boom(app, client: RequestHandler) -> None:
    response = client.get('/boom')
    assert response.status_code == 500
    assert response.json == dict(
        [
            ('Code', 'InternalServerError'),
            ('Message', 'An internal server error occurred.'),
        ]
    )


def test_has_request(app, capture_events, client: RequestHandler):
    events = capture_events()

    response = client.get('/context')
    assert response.status_code == 500

    (event,) = events
    assert event["transaction"] == "api_handler"
    assert "data" not in event["request"]
    assert event["request"]["url"] == "awslambda:///api_handler"
    assert event["request"]["headers"] == {}
