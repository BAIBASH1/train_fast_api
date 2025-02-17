from time import time

from fastapi import Request

from app.logger import logger


def setup_middleware(app):
    @app.middleware("http")
    async def record_process_time(request: Request, call_next):
        start_time = time()
        response = await call_next(request)
        logger.info(
            "Request execution time",
            extra={"process_time": round(time() - start_time, 3)},
        )
        return response
