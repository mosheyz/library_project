from logs.logger_config import logger
from fastapi import APIRouter, HTTPException
from database.member_db import member
from pydantic import BaseModel


class Member(BaseModel):
        name: str
        email: str


router = APIRouter()

@router.post("", status_code=201)
def create_member(data: Member):
    data = data.model_dump()
    new_member = member.create_member(data)
    return new_member


@router.get("")
def get_members():
    members = member.get_all_members()
    return members


@router.get("/{id}")
def get_member_by_id(id:int):
    _member = member.get_member_by_id(id)
    if not _member:
        logger.warning(f"member {id} not found")
        raise HTTPException(
             status_code=404,
             detail=f"member {id} not found"
        ) 
    return _member


@router.put("/{id}")
def update_member(id:int, data:dict):
    if not member.get_member_by_id(id):
        logger.warning(f"member {id} not found")
        raise HTTPException(
             status_code=404,
             detail=f"member {id} not found"
        )
    
    valid_keys = ["name", "email"]
    checked_data = {k:v for k, v in data.items() if k in valid_keys}
    
    if not checked_data:
        logger.warning("invalid data to update")
        raise HTTPException(
              status_code=422,
              detail="invalid data to update"
         )
    
    update = member.update_member(id, checked_data)
    return update

@router.put("/{id}/deactivate")
def deactivate_member(id:int):
    if not member.get_member_by_id(id):
        logger.warning(f"member {id} not found")
        raise HTTPException(
             status_code=404,
             detail=f"member {id} not found"
        )

    deact = member.deactivate_member(id)
    return deact

@router.put("/{id}/activate")
def activate_member(id:int):
    if not member.get_member_by_id(id):
        logger.warning(f"member {id} not found")
        raise HTTPException(
             status_code=404,
             detail=f"member {id} not found"
        )

    act = member.activate_member(id)
    return act