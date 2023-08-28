from sentry_sdk import capture_message, set_tag


class HTTPStatusesSentryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code in (301, 302, 404):
            set_tag("referrer", request.headers.get("referer"))
            capture_message(f"{response.status_code}: {response.reason_phrase}")
        return response
