from typing import List

from fastapi import APIRouter
from db.db import clients, database
from models.client import ClientIn, Client

router = APIRouter()


@router.post("/clients/", response_model=Client)
async def create_client(client: ClientIn):
    """Создание клиента в БД, create"""
    query = clients.insert().values(document=client.document,
                                    lastname=client.lastname,
                                    firstname=client.firstname,
                                    midname=client.midname,
                                    birthday=client.birthday,)
    last_record_id = await database.execute(query)
    return {**client.dict(), "client_id": last_record_id}


@router.get("/clients/", response_model=List[Client])
async def read_clients():
    """Чтение клиентов из БД, read"""
    query = clients.select()
    return await database.fetch_all(query)


@router.get("/clients/{client_id}", response_model=Client)
async def read_client_by_id(client_id: int):
    """Чтение одного клиента из БД, read"""
    query = clients.select().where(clients.c.id == client_id)
    return await database.fetch_one(query)


@router.put("/clients/{client_id}", response_model=Client)
async def update_client(client_id: int, new_client: ClientIn):
    """Обновление клиента в БД, update"""
    query = clients.update().where(clients.c.id == client_id).values(**new_client.dict())
    await database.execute(query)
    return {**new_client.dict(), "client_id": client_id}


@router.delete("/clients/{client_id}")
async def delete_client(client_id: int):
    """Удаление клиента из БД, delete"""
    query = clients.delete().where(clients.c.id == client_id)
    await database.execute(query)
    return {'message': 'Client deleted'}
