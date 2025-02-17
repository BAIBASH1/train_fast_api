from prometheus_fastapi_instrumentator import Instrumentator


def setup_instrumentation(app):
    instrumentor = Instrumentator(
        should_group_status_codes=False,
        excluded_handlers=[".*admin.*", "/metrics"],
    )
    instrumentor.instrument(app).expose(app)
