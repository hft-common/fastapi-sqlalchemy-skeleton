from pathlib import Path

import uvicorn
from fastapi.applications import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from api.test.healthcheck import router as test_router

from fastapi.responses import HTMLResponse
import config
from api.user_management.user_basic_api import user_router

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

app.mount("/assets/static", StaticFiles(directory=Path(config.dir_path) / 'static'), name="static")


@app.get('/')
def get_app_angular():
    with open('static/index.html', 'r') as file_index:
        html_content = file_index.read()
    return HTMLResponse(html_content, status_code=200)


@app.on_event("startup")
async def startup():
    # Start threads here
    pass


def create_app():
    return app


if __name__ == '__main__':
    app = create_app()
    uvicorn.run('main:app',
                host=config.fastapi_host, port=config.fastapi_port,
                reload=config.reload)

