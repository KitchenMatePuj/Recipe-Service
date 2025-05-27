from starlette.middleware.base import BaseHTTPMiddleware
import json, logging, codecs

class LogRequestBody(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        raw = await request.body()
        logging.warning("[API] raw bytes = %s", raw[:120])
        try:
            logging.warning("[API] decoded = %s", raw.decode("utf-8"))
        except UnicodeDecodeError as e:
            logging.error("decode error: %s", e)
        return await call_next(request)
