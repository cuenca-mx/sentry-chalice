import pytest
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
    assert event["request"]["headers"] == {}


def test_scheduled_event(app):
    @app.schedule('rate(1 minutes)')
    def every_hour(event):
        raise Exception('only chalice event!')

    lambda_event = {
        "version": "0",
        "account": "123456789012",
        "region": "us-west-2",
        "detail": {},
        "detail-type": "Scheduled Event",
        "source": "aws.events",
        "time": "1970-01-01T00:00:00Z",
        "id": "event-id",
        "resources": [
            "arn:aws:events:us-west-2:123456789012:rule/my-schedule"
        ],
    }
    with pytest.raises(Exception) as exc_info:
        every_hour(lambda_event, context=None)
    assert str(exc_info.value) == 'only chalice event!'


def test_bad_reques(app) -> None:
    with Client(app) as client:

        response = client.http.get('/badrequest')

        assert response.status_code == 400
        assert response.json_body == dict(
            [
                ('Code', 'BadRequestError'),
                ('Message', 'BadRequestError: bad-request'),
            ]
        )
