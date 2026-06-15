from database.book_db import book
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from logs.logger_config import logger
from database.member_db import member
import mysql.connector



class CreateBook(BaseModel):
    title: str
    author: str
    genre: str


router = APIRouter()

@router.post("")
def create_book(data: CreateBook):

    data = data.model_dump()
    book_id = book.create_book(data)
    return book_id


@router.get("")
def get_all_books():
    books = book.get_all_books()
    return books


@router.get("/{id}")
def book_by_id(id:int):
    _book = book.get_book_by_id(id)
    if not _book:
        raise HTTPException(
            status_code=404,
            detail=f"book id {id} not found"
        )

    return _book


@router.put("/{id}")
def update_book(id:int, data:dict):
    valid_fields = ["title", "author", "genre", "borrowed_by_member_id"]
    checked_data = {k:v for k, v in data.items() if k in valid_fields}
    exist = book.get_book_by_id(id)
    
    if not exist:
        raise HTTPException(
            status_code=404,
            detail=f"book id {id} not found"
        )
    
    if not checked_data:
        raise HTTPException(
            status_code=400,
            detail="no valid fields to update"
        )
    
    ok = book.update_book(id, checked_data)
    return ok


@router.put("/{id}/borrow/{member_id}")
def borrow_book(id:int, member_id:int):
    _book = book.get_book_by_id(id)
    _member = member.get_member_by_id(member_id)

    if not _book:
        logger.warning(f"book {id} not found")
        raise HTTPException(
            status_code=404,
            detail=f"book id {id} not found"
        )
    
    if not _member:
        logger.warning(f"member {member_id} not found")
        raise HTTPException(
             status_code=404,
             detail=f"member {member_id} not found"
        )
    
    if not _book["is_available"] or _book["borrowed_by_member_id"]:
        logger.warning(f"book {id} unavailable")
        raise HTTPException(
            status_code=400,
            detail=f"book {id} unavailable"
        )
    
    if not _member["is_active"]:
        logger.error(f"member {member_id} is not active")
        raise HTTPException(
            status_code=400,
            detail=f"member {member_id} is not active"
        )
    
    if book.count_active_borrows_by_member(member_id) > 3:
        logger.error(f"member {member_id} has borrow more than 3 books")
        raise HTTPException(
            status_code=400,
            detail=f"member {member_id} has borrow more than 3 books"
        )
    
    book.set_available(id, False, member_id)
    updated = member.increment_borrows(member_id)

    return updated

@router.put("/{id}/return/{member_id}")
def return_book(id:int, member_id:int):
    _book = book.get_book_by_id(id)
    _member = member.get_member_by_id(member_id)

    if not _book:
        logger.warning(f"book {id} not found")
        raise HTTPException(
            status_code=404,
            detail=f"book id {id} not found"
        )
    
    if not _member:
        logger.warning(f"member {member_id} not found")
        raise HTTPException(
             status_code=404,
             detail=f"member {member_id} not found"
        )
    
    if _book["is_available"]:
        logger.warning(f"book {id} is not borrowed")
        raise HTTPException(
            status_code=400,
            detail=f"book {id} is not borrowed"
        )
    
    if not _member["is_active"]:
        logger.error(f"member {member_id} is not active")
        raise HTTPException(
            status_code=400,
            detail=f"member {member_id} is not active"
        )
    
    if _book["borrowed_by_member_id"] != member_id:
        logger.error(f"member {member_id} cannot return this book")
        raise HTTPException(
            status_code=400,
            detail=f"member {member_id} cannot return this book"
        )
    
    updated = book.set_available(id, True, member_id)

    return updated
    


# @router.put("/{id}/return/{member_id}")
