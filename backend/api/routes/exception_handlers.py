import starlette
from starlette.responses import JSONResponse

from api.exceptions import ObjectNotFound

from .base import app


@app.exception_handler(ObjectNotFound)
async def not_found_handler(req: starlette.requests.Request, exc: ObjectNotFound):
    return JSONResponse(status_code=404, content="Not found")
