from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routes.book_routes import router as books_router
from routes.member_routes import router as members_router
from routes.report_routes import router as reports_router
from mysql.connector import Error
from logs.logger_config import logger
from database.db_connection import db
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("connection start..")

    yield

    logger.info("connection close")
    db.conn.close()


app = FastAPI(lifespan=lifespan)


@app.exception_handler(Error)
def sql_errors(req: Request, e: Error):
    logger.error(f"database error: {e.msg}")
    return JSONResponse(
        status_code=500,
        content=f"{e.errno}, {e.msg}"
    )


app.include_router(books_router, prefix="/books", tags=["books"])
app.include_router(members_router, prefix="/members", tags=["members"])
app.include_router(reports_router, prefix="/reports", tags=["reports"])
