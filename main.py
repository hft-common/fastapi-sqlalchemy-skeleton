from pathlib import Path

import uvicorn
from fastapi.applications import FastAPI, RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from api.test.healthcheck import router as test_router

from fastapi.responses import HTMLResponse
import config
from api.user_management.user_auth import auth_router
from api.user_management.user_basic_api import user_router
from standard_responses.standard_json_response import standard_json_response



app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:4200",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(test_router)
app.include_router(user_router)
app.include_router(auth_router)

app.mount("/assets/static", StaticFiles(directory=Path(config.dir_path) / 'static'), name="static")



@app.exception_handler(RequestValidationError)
async def default_exception_handler(request: Request, exc: RequestValidationError):
    return standard_json_response(
        status_code=200,
        data={},
        error=True,
        message=str(exc)
    )

@app.get('/')
def get_app_angular(path=None):

    with open('static/templates/index.html', 'r') as file_index:
        html_content = file_index.read()
    return HTMLResponse(html_content, status_code=200)



@app.get('/{path}')
def get_static_file_angular(path):
    try:
        with open(f'static/templates/{path}') as file_index:
            html_content = file_index.read()
    except Exception as ex:
        return RedirectResponse('/')
    media_type = 'text/html'
    if 'js' in path:
        media_type = 'text/javascript'
    if 'css' in path:
        media_type = 'text/css'
    return Response(html_content, status_code=200, media_type=media_type)


@app.on_event("startup")
async def startup():
    # Start threads here
    # results = await asyncio.gather(Foo.get_instance())
    # app.state.ws = results[0][0]
    # asyncio.create_task(expire_time_check())
    pass


def create_app():
    return app


if __name__ == '__main__':
    app = create_app()
    uvicorn.run('main:app',
                host=config.fastapi_host, port=config.fastapi_port,
                reload=config.reload)

