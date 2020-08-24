import pytest
from chalice.local import LambdaContext
from chalice.test import Client


class FakeTimeSource(object):
    # taken from chalice tests
    def __init__(self, times):
        """Create a fake source of second-precision time.
        :type time: List
        :param time: List of times that the time source should return in the
            order it should return them. These should be in seconds.
        """
        self._times = times

    def time(self):
        """Get the next time.
        This is for mimicing the Clock interface used in local.
        """
        time = self._times.pop(0)
        return time


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

    assert event["level"] == "error"
    (exception,) = event["exception"]["values"]
    assert exception["type"] == "Exception"


def test_scheduled_event(app, lambda_context_args):
    @app.schedule('rate(1 minutes)')
    def every_hour(event):
        raise Exception('only chalice event!')

    time_source = FakeTimeSource([0, 5])
    context = LambdaContext(
        *lambda_context_args, max_runtime_ms=10000, time_source=time_source
    )
    # time_remaining = context.get_remaining_time_in_millis()

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
        every_hour(lambda_event, context=context)
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
