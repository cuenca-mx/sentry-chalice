# Sentry-chalice

[![test](https://github.com/cuenca-mx/sentry-chalice/workflows/test/badge.svg)](https://github.com/cuenca-mx/sentry-chalice/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/cuenca-mx/sentry-chalice/branch/main/graph/badge.svg)](https://codecov.io/gh/cuenca-mx/sentry-chalice)
[![PyPI](https://img.shields.io/pypi/v/sentry-chalice.svg)](https://pypi.org/project/sentry-chalice/)

Sentry-Chalice allow the integration of Chalice on sentry.

You can use sentry-chalice integration like this:

```python
import sentry_sdk
from chalice import Chalice

from sentry_chalice import ChaliceIntegration


sentry_sdk.init(
    dsn="https://<key>@<organization>.ingest.sentry.io/<project>",
    integrations=[ChaliceIntegration()]
)

app = Chalice(app_name='appname')

```
sentry-chalice now it works just for views: @app.route.

You can create a route that triggers an error for validate your Sentry installation, like this:

```python
@app.route('/boom')
def boom():
    raise Exception('boom goes the dynamite!')

```

when you enter the route will throw an error that will be captured by Sentry.


## Behavior

- Request data is attached to all events: HTTP method, URL, headers, form data, JSON payloads. Sentry excludes raw bodies and multipart file uploads. Sentry also excludes personally identifiable information (such as user ids, usernames, cookies, authorization headers, IP addresses) unless you set send_default_pii to True.

Each request has a separate scope. Changes to the scope within a view, for example setting a tag, will only apply to events sent as part of the request being handled.
