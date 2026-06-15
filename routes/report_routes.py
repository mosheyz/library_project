from fastapi import APIRouter
from database.book_db import book
from database.member_db import member


router =APIRouter()

@router.get("/summary")
def general_report():
    report = {
        "total_books": book.count_total_books(),
        "available_books": book.count_available_books(),
        "currently_borrowed": book.count_borrowed_books(),
        "active_members": member.count_active_members()
        }
    return report

@router.get("/books-by-genre")
def books_by_genre():
    return book.count_by_genre()

@router.get("/top-member")
def top_member():
    return member.get_top_member