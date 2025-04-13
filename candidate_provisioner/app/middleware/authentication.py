from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.settings import settings



class APIKeyMiddleware(BaseHTTPMiddleware):
    # TODO: Implement the authentication through dynamoDB instead of hardcoding the API keys

    def __init__(self, app):
        super().__init__(app)
        self.valid_api_keys = settings.api_keys.split(",")
        print(f"Valid API Keys: {self.valid_api_keys}")
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/candidate/register"]:
            api_key = request.headers.get("x-api-key")

            is_valid = True if api_key in self.valid_api_keys else False
            if not is_valid:
                return JSONResponse(
                    status_code=401, content={"detail": "Invalid API Key"}
                )

        return await call_next(request)
