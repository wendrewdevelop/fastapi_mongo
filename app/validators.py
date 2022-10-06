from app.config import app
from fastapi import Request
from fastapi.responses import JSONResponse


class CepNotFoundException(Exception):
    pass


@app.exception_handler(CepNotFoundException)
async def cep_not_found_handler(request: Request, exc: CepNotFoundException):
    return JSONResponse(status_code=404, content={"message": "Cep não encontrado"})