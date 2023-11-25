from typing import List

from fastapi import APIRouter
from db.db import pets, database
from models.pet import PetIn, Pet

router = APIRouter()


@router.post("/pets/", response_model=Pet)
async def create_pet(pet: PetIn):
    """Создание животного в БД, create"""
    query = pets.insert().values(client_id=pet.client_id,
                                 name=pet.name,
                                 birthday=pet.birthday,)
    last_record_id = await database.execute(query)
    return {**pet.dict(), "pet_id": last_record_id}


@router.get("/pets/", response_model=List[Pet])
async def read_pets():
    """Чтение животных из БД, read"""
    query = pets.select()
    return await database.fetch_all(query)


@router.get("/pets/{pet_id}", response_model=Pet)
async def read_pet_by_id(pet_id: int):
    """Чтение одного животного из БД по id животного, read"""
    query = pets.select().where(pets.c.id == pet_id)
    return await database.fetch_one(query)


@router.get("/pets/{client_id}", response_model=Pet)
async def read_pet_by_client_id(client_id: int):
    """Чтение животных из БД по id клиента, read"""
    query = pets.select().where(pets.c.client_id == client_id)
    return await database.fetch_all(query)


@router.put("/pets/{pet_id}", response_model=Pet)
async def update_pet(pet_id: int, new_pet: PetIn):
    """Обновление животного в БД, update"""
    query = pets.update().where(pets.c.id == pet_id).values(**new_pet.dict())
    await database.execute(query)
    return {**new_pet.dict(), "pet_id": pet_id}


@router.delete("/pets/{pet_id}")
async def delete_pet(pet_id: int):
    """Удаление животного из БД, delete"""
    query = pets.delete().where(pets.c.id == pet_id)
    await database.execute(query)
    return {'message': 'Pet deleted'}
