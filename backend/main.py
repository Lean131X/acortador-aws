import os
import uuid
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl

from db import tabla

base_url = os.getenv("BASE_URL", "http://localhost:8000")
origen_front = os.getenv("FRONTEND_ORIGIN", "")

app = FastAPI(title="Acortador de enlaces")

# solo el front de S3 puede llamar a la API desde el navegador
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origen_front],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class EnlaceNuevo(BaseModel):
    original_url: HttpUrl


def buscar_enlace(codigo):
    respuesta = tabla.get_item(Key={"short_code": codigo})
    item = respuesta.get("Item")
    if item is None:
        raise HTTPException(status_code=404, detail="Enlace no encontrado")
    return item


@app.post("/shorten", status_code=201)
def acortar(datos: EnlaceNuevo):
    # el uuid se genera aqui en el backend
    codigo = str(uuid.uuid4())
    url_original = str(datos.original_url)
    fecha = datetime.now(timezone.utc).isoformat()

    tabla.put_item(Item={
        "short_code": codigo,
        "original_url": url_original,
        "created_at": fecha,
    })

    return {
        "short_code": codigo,
        "original_url": url_original,
        "short_url": f"{base_url}/{codigo}",
    }


@app.get("/urls/{short_code}")
def ver_enlace(short_code: str):
    return buscar_enlace(short_code)


# esta va al final porque recibe cualquier codigo
@app.get("/{short_code}")
def redirigir(short_code: str):
    item = buscar_enlace(short_code)
    return RedirectResponse(url=item["original_url"], status_code=307)