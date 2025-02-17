import sentry_sdk

from config import settings


def init_sentry():
    sentry_sdk.init(
        dsn=settings.SENTRY_LINK,
        traces_sample_rate=1.0,
    )
