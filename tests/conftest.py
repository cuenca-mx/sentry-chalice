import pytest
import sentry_sdk
from chalice import BadRequestError, Chalice

from sentry_chalice import ChaliceIntegration

SENTRY_DSN = 'https://111@sentry.io/111'


@pytest.fixture
def app():
    sentry_sdk.init(dsn=SENTRY_DSN, integrations=[ChaliceIntegration()])
    app = Chalice(app_name='sentry_chalice')

    @app.route('/boom')
    def boom():
        raise Exception('boom goes the dynamite!')

    @app.route('/context')
    def has_request():
        raise Exception('boom goes the dynamite!')

    @app.route('/badrequest')
    def badrequest():
        raise BadRequestError('bad-request')

    return app


@pytest.fixture
def capture_events(monkeypatch):
    def inner():
        events = []
        test_client = sentry_sdk.Hub.current.client
        old_capture_event = test_client.transport.capture_event
        old_capture_envelope = test_client.transport.capture_envelope

        def append_event(event):
            events.append(event)
            return old_capture_event(event)

        def append_envelope(envelope):
            for item in envelope:
                if item.headers.get("type") in ("event", "transaction"):
                    events.append(item.payload.json)
            return old_capture_envelope(envelope)

        monkeypatch.setattr(
            test_client.transport, "capture_event", append_event
        )
        monkeypatch.setattr(
            test_client.transport, "capture_envelope", append_envelope
        )
        return events

    return inner


@pytest.fixture
def lambda_context_args():
    # LambdaContext has several positional args before the ones that we
    # care about for the timing tests, this gives reasonable defaults for
    # those arguments. Taken from chalice tests
    return ['lambda_name', 256]
