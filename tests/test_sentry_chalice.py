from chalice.test import Client


def test_exception_boom(app) -> None:
    with Client(app) as client:
        response = client.http.get('/boom')
        assert response.status_code == 500
        assert response.json_body == dict(
            [
                ('Code', 'InternalServerError'),
                ('Message', 'An internal server error occurred.'),
            ]
        )


def test_has_request(app, capture_events):
    events = capture_events()
    with Client(app) as client:

        response = client.http.get('/context')
        assert response.status_code == 500

        (event,) = events
        assert event["transaction"] == "api_handler"
        assert "data" not in event["request"]
        assert event["request"]["url"] == "awslambda:///api_handler"
        assert event["request"]["headers"] == {}
