from prometheus_client import Counter, Gauge, Histogram


def create_request_metric(prefix: str) -> Counter:
    """
    create counter metric for requests
    Args:
        prefix: the name of the project
    Returns: registered counter metric
    """
    return Counter(
        "requests_total",
        "Total count of requests by method and path.",
        ["method", "path_template"],
        namespace=prefix
    )


def create_response_metric(prefix: str) -> Counter:
    """
    create counter metric for responses
    Args:
         prefix: the name of the project
    Returns: registered counter metric
    """
    return Counter(
        "responses_total",
        "Total count of responses by method, path and status codes.",
        ["method", "path_template", "status_code"],
        namespace=prefix
    )


def create_requests_processing_time_metric(prefix: str) -> Histogram:
    """
    create request processing time metric
    Args:
        prefix: the name of the project
    Returns: registered Histogram metric
    """
    return Histogram(
        "requests_processing_time_seconds",
        "Histogram of requests processing time by path (in seconds)",
        ["method", "path_template"],
        namespace=prefix
    )


def create_exceptions_total_metric(prefix: str) -> Counter:
    """
    create counter metric for exceptions
    Args:
        prefix: the name of the project
    Returns: registered counter metric
    """
    return Counter(
        "exceptions_total",
        "Total count of exceptions raised by path and exception type",
        ["method", "path_template", "exception_type"],
        namespace=prefix,
    )


def create_requests_in_progress_metric(prefix: str) -> Gauge:
    """
    create counter metric for in-progress requests
    Args:
       prefix: the name of the project
    Returns: registered counter metric
    """
    return Gauge(
        "requests_in_progress",
        "Gauge of requests by method and path currently being processed",
        ["method", "path_template"],
        namespace=prefix
    )
