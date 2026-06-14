from logs.logger_config import logger
from database.db_connection import db


class BookDb:
    def __init__(self):
        pass

    def create_book(self, data: dict):
        with db.conn.cursor(dictionary=True) as cursor:
            logger.info("start creating book..")
            query ="""
            INSERT INTO books
            (title, author, genre)
            VALUES (%s, %s, %s)
            """
            values = [data["title"], data["author"], data["genre"]]

            cursor.execute(query, values)        
            book_id = cursor.lastrowid
            db.conn.commit()

            if not book_id:
                logger.warning("invalid data")
                return None

            logger.info("book added to the system")
            return book_id
    

    def get_all_books(self):
        with db.conn.cursor(dictionary=True) as cursor:
            logger.info("start getting books table..")
            query = """
                    SELECT * FROM books
                    """
            cursor.execute(query)
            books = cursor.fetchall()

            if not books:
                logger.warning("book table is empty")
                return None
            logger.info("getting all booksn has finished")
            return books
        

    def get_book_by_id(self, id):
        with db.conn.cursor(dictionary=True) as cursor:
            logger.info("start getting books table..")
            query = """
                    SELECT * FROM books
                    WHERE id=%s
                    """
            cursor.execute(query, [id])
            book = cursor.fetchall()

            if not book:
                logger.warning(f"book id: {id} doesn't exists")
                return None
            logger.info(f"getting book id: {id} has finished")
            return book
        

    def update_book(self, id, data):
        with db.conn.cursor(dictionary=True) as cursor:
            logger.info("start updating book..")
            columns = ", ".join(f"{k}=%s" for k in data.keys())
            values = list(data.values()) + [id]
            query = f"""
                UPDATE books SET {columns} WHERE id=%s
                """
            cursor.execute(query, values)

            if cursor.rowcount == 0:
                logger.warning("nothing to update")
                return None
            
            db.conn.commit()
            logger.info("updated successfully")
            return data


    def set_available(self, id: int, val: bool, member_id: int):
        with db.conn.cursor(dictionary=True) as cursor:
            logger.info("start setting book availabillity..")

            member = member_id
            if val:
                member = None
            
            """
            UPDATE books SET is_available=%s
            borrowed_by_member_id=%s
            WHERE is_available NOT %s AND id=%s
            """, [val, member, val, id]


    def count_total_books(self):
        with db.conn.cursor(dictionary=True) as cursor:
            query = """
                SELECT COUNT(*) as total FROM books
                """
            cursor.execute(query)

            books_num = cursor.fetchall()[0]["total"]
            if books_num == 0:
                logger.warning("books table us empty")
                return None
            
            return books_num
        

    def count_available_books(self):
        with db.conn.cursor(dictionary=True) as cursor:
            query = """
                SELECT COUNT(*) as total FROM books WHERE is_available=TRUE
                """
            cursor.execute(query)

            av_books_num = cursor.fetchall()[0]["total"]
            if av_books_num == 0:
                logger.warning("no available books")
                return None
            
            return av_books_num


    def count_borrowed_books(self):
         with db.conn.cursor(dictionary=True) as cursor:
            query = """
                SELECT COUNT(*) as total FROM books WHERE is_available=FALSE
                """
            cursor.execute(query)

            av_books_num = cursor.fetchall()[0]["total"]
            if av_books_num == 0:
                logger.warning("no borrowed books")
                return None
            
            return av_books_num


    def count_by_genre(self, genre):
         with db.conn.cursor(dictionary=True) as cursor:
            query = """
                SELECT COUNT(*) as total FROM books WHERE genre=%s
                """
            cursor.execute(query, [genre])

            av_books_num = cursor.fetchall()[0]["total"]
            if av_books_num == 0:
                logger.warning(f"no books by genre {genre}")
                return None
            
            return av_books_num


    def count_active_borrows_by_member(self, member_id):
        with db.conn.cursor(dictionary=True) as cursor:
            query = """
                SELECT COUNT(*) as total FROM books WHERE borrowed_by_member_id=%s
                """
            cursor.execute(query, [member_id])

            av_books_num = cursor.fetchall()[0]["total"]
            if av_books_num == 0:
                logger.warning("no available books")
                return None
            
            return av_books_num


book = BookDb()
