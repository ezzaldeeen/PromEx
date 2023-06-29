from fastapi import FastAPI

from monitoring.middleware import PrometheusMiddleware
from monitoring.endpoint import metrics

app = FastAPI(title="PromEx",
              description="Playing with Prometheus")
# setting the prom middle ware
app.add_middleware(
    PrometheusMiddleware, filter_unhandled_paths=False, prefix='service'
)
# expose the metrics endpoint
app.add_route("/metrics", metrics)
