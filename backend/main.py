from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from .routes.openapi import api
from .routes.auth import auth
from .routes.connects import connect
from .routes.index import index
from .routes.files import file
from .routes.privategpt import gpt
from .routes.users import usr
from .routes.person import person

app = FastAPI(title="StaffSec", version="0.1.0")

app.include_router(api)
app.include_router(auth)
app.include_router(connect)
app.include_router(index)
app.include_router(file)
app.include_router(gpt)
app.include_router(person)
app.include_router(usr)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="static")

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/{path:path}", response_class=HTMLResponse)
async def catch_all(request: Request, path: str):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )