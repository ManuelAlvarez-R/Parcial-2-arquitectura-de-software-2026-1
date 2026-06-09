import time
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import OperationalError

from app.controllers.graphql_controller import graphql_router
from app.database import Base, engine

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "views" / "templates"
STATIC_DIR = BASE_DIR / "views" / "static"

app = FastAPI(
    title="Gestión de Inventarios - Almacén",
    description=(
        "Servicio web monolítico MVC con GraphQL (Strawberry) para gestionar "
        "inventarios de productos en diferentes sedes de almacén."
    ),
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

app.include_router(graphql_router, prefix="/graphql")


def init_database(max_retries: int = 30, delay_seconds: int = 2) -> None:
    for attempt in range(1, max_retries + 1):
        try:
            Base.metadata.create_all(bind=engine)
            return
        except OperationalError:
            if attempt == max_retries:
                raise
            time.sleep(delay_seconds)


@app.on_event("startup")
def on_startup():
    init_database()


@app.get("/", response_class=HTMLResponse, tags=["Vista"])
def pagina_principal(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "titulo": "Gestión de Inventarios"},
    )


@app.get("/health", tags=["Sistema"])
def health_check():
    return {"estado": "ok", "servicio": "inventario-almacen"}
