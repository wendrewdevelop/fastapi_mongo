import requests
import uvicorn
from pymongo import errors
from typing import Any, List, Optional
from fastapi import (
    FastAPI, 
    Path, 
    Request, 
    status, 
    Query,
    APIRouter
)
from fastapi.responses import JSONResponse
from app import schema
from bootstrap import mongodb
from app.validators import CepNotFoundException
from app.config import app
from app.functions import save_address


router = APIRouter(
    prefix="/address",
    tags=["address"],
    responses={
        404: {
            "description": "Not found"
        }
    },
)


@router.get("/{cep}", response_model=schema.AddressOutput)
async def search_address_by_cep(cep: str = Path(default=Any, max_length=9, min_length=9)):
    """
        Se passarmos um cep com um caracter a menos, 
        vamos receber uma mensagem de erro, 
        dizendo que é preciso 8 caracteres.
    """
    address = app.db.find_one({"cep": cep})
    if not address:
        response = requests.get(f"http://viacep.com.br/ws/{cep}/json/")
        address = response.json()

        if "erro" in address:
            raise CepNotFoundException()

        await save_address(address)

    return address


@router.post("/", response_model=schema.AddressOutput, status_code=201)
async def create_address(address: schema.AddressInput):
    try:
        await save_address(address.dict()) 
        return address
    except errors.DuplicateKeyError:
        return JSONResponse(status_code=409, content={"message": "Cep já existe"})


@router.put("/{cep}", status_code=status.HTTP_204_NO_CONTENT)
async def update_address(cep: str, address: schema.AddressInput):
    old_address = app.db.find_one({"cep": cep})
    update_address = {"$set": address.dict()} # isso é uma particularidade do pymongo
    app.db.update_one(old_address, update_address)


@router.get("/", response_model=schema.AddressOutput)
async def search_address(uf: Optional[str] = Query(None, max_length=2, min_length=2)):
    if uf:
        return list(app.db.find({"uf": uf}))

    return list(app.db.find({}))