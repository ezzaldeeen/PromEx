import time
from typing import Tuple

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Match
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from starlette.types import ASGIApp
from starlette.exceptions import HTTPException

from monitoring.metrics import (
    create_request_metric,
    create_response_metric,
    create_requests_processing_time_metric,
    create_requests_in_progress_metric,
    create_exceptions_total_metric
)


class PrometheusMiddleware(BaseHTTPMiddleware):
    """Prometheus middleware"""

    def __init__(self,
                 app: ASGIApp,
                 filter_unhandled_paths: bool = False,
                 prefix: str = '') -> None:
        """
        Args:
            app:
            filter_unhandled_paths:
            prefix: the name of the project to prefix metric name with the project name
        """
        super().__init__(app)
        self.filter_unhandled_paths = filter_unhandled_paths
        self.__prefix: str = prefix

        self.requests_counter = create_request_metric(prefix)
        self.response_counter = create_response_metric(prefix)
        self.requests_processing_time = create_requests_processing_time_metric(prefix)
        self.requests_in_progress = create_requests_in_progress_metric(prefix)
        self.exceptions_total = create_exceptions_total_metric(prefix)

    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """
        actual middleware execution scope
        Args:
            request: request
            call_next: next call in the requests chain
        Returns: Response
        """
        method = request.method
        path_template, is_handled_path = self.get_path_template(request)

        if self._is_path_filtered(is_handled_path):
            return await call_next(request)

        self.requests_in_progress.labels(
            method=method, path_template=path_template
        ).inc()

        self.requests_counter.labels(
            method=method, path_template=path_template
        ).inc()

        before_time = time.perf_counter()
        status_code = None
        try:
            response = await call_next(request)
        except HTTPException as exp:
            status_code = exp.status_code
            self.exceptions_total.labels(
                method=method,
                path_template=path_template,
                exception_type=type(exp).__name__
            ).inc()
            raise exp from None

        else:
            after_time = time.perf_counter()

            self.requests_processing_time.labels(
                method=method, path_template=path_template
            ).observe(after_time - before_time)

        finally:
            # this way we can guarantee that the status code will be set
            status_code = status_code or response.status_code
            self.response_counter.labels(
                method=method,
                path_template=path_template,
                status_code=status_code
            ).inc()

            self.requests_in_progress.labels(
                method=method, path_template=path_template
            ).dec()

        return response

    @staticmethod
    def get_path_template(request: Request) -> Tuple[str, bool]:
        for route in request.app.routes:
            match, child_scope = route.matches(request.scope)
            if match == Match.FULL:
                return route.path, True

        return request.url.path, False

    def _is_path_filtered(self, is_handled_path: bool) -> bool:
        return self.filter_unhandled_paths and not is_handled_path
