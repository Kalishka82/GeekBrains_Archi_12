from typing import List

from fastapi import APIRouter
from db.db import consultations, database
from models.consultation import ConsultationIn, Consultation

router = APIRouter()


@router.post("/consultations/", response_model=Consultation)
async def create_consultation(consultation: ConsultationIn):
    """Создание консультации в БД, create"""
    query = consultations.insert().values(client_id=consultation.client_id,
                                          pet_id=consultation.pet_id,
                                          date_time=consultation.date_time,
                                          description=consultation.description,)
    last_record_id = await database.execute(query)
    return {**consultation.dict(), "consultation_id": last_record_id}


@router.get("/consultations/", response_model=List[Consultation])
async def read_consultations():
    """Чтение консультаций из БД, read"""
    query = consultations.select()
    return await database.fetch_all(query)


@router.get("/consultations/{consultation_id}", response_model=Consultation)
async def read_consultation_by_id(consultation_id: int):
    """Чтение одной консультации из БД по id консультации, read"""
    query = consultations.select().where(consultations.c.id == consultation_id)
    return await database.fetch_one(query)


@router.get("/consultations/{pet_id}", response_model=Consultation)
async def read_consultation_by_pet_id(pet_id: int):
    """Чтение консультаций из БД по id животного, read"""
    query = consultations.select().where(consultations.c.pet_id == pet_id)
    return await database.fetch_all(query)


@router.get("/consultations/{client_id}", response_model=Consultation)
async def read_pet_by_client_id(client_id: int):
    """Чтение консультаций из БД по id клиента, read"""
    query = consultations.select().where(consultations.c.client_id == client_id)
    return await database.fetch_all(query)


@router.put("/consultations/{consultation_id}", response_model=Consultation)
async def update_consultation(consultation_id: int, new_consultation: ConsultationIn):
    """Обновление консультации в БД, update"""
    query = consultations.update().where(consultations.c.id == consultation_id).values(**new_consultation.dict())
    await database.execute(query)
    return {**new_consultation.dict(), "consultation_id": consultation_id}


@router.delete("/consultations/{consultation_id}")
async def delete_consultation(consultation_id: int):
    """Удаление консультации из БД, delete"""
    query = consultations.delete().where(consultations.c.id == consultation_id)
    await database.execute(query)
    return {'message': 'Consultation deleted'}
