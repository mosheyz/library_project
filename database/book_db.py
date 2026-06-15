from logs.logger_config import logger
from database.db_connection import db
from database.member_db import member


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

            logger.info("book added to the system")
            return self.get_book_by_id(book_id)
    

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
                return []
            logger.info("getting all booksn has finished")
            return books
        

    def get_book_by_id(self, id):
        with db.conn.cursor(dictionary=True) as cursor:
            logger.info("start getting book..")
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
            return book[0]
        

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
                return "nothing was changed"
            
            db.conn.commit()
            logger.info("updated successfully")
            return self.get_book_by_id(id)


    def set_available(self, id: int, val: bool, member_id: int):
        with db.conn.cursor(dictionary=True) as cursor:
            logger.info("start updating book availabillity..")

            query = """
                UPDATE books  SET 
                is_available=%s,
                borrowed_by_member_id=%s
                WHERE id=%s
                """
            cursor.execute(query, [val, member_id if not val else None, id])
            db.conn.commit()

            logger.info("book availabillity was updated")
            _member = member.get_member_by_id(member_id)
            return _member


    def count_total_books(self):
        with db.conn.cursor(dictionary=True) as cursor:
            logger.info("start counting books..")
            query = """
                SELECT COUNT(*) as total FROM books
                """
            cursor.execute(query)

            books_num = cursor.fetchall()
            if books_num == []:
                logger.warning("books table is empty")
                return None
            logger.info("counting books has finished")
            return books_num[0]["total"]
        

    def count_available_books(self):
        with db.conn.cursor(dictionary=True) as cursor:
            logger.info("start counting available books..")
            query = """
                SELECT COUNT(*) as total FROM books
                WHERE is_available=TRUE
                """
            cursor.execute(query)

            av_books_num = cursor.fetchall()
            if av_books_num == []:
                logger.warning("no available books")
                return None
            logger.info("counting available books has finished")
            return av_books_num[0]["total"]


    def count_borrowed_books(self):
         with db.conn.cursor(dictionary=True) as cursor:
            logger.info("start counting borrowed books..")
            query = """
                SELECT COUNT(*) as total FROM books
                WHERE is_available=FALSE
                """
            cursor.execute(query)

            borrowed_books_num = cursor.fetchall()
            if borrowed_books_num == []:
                logger.warning("no borrowed books")
                return None
            logger.info("counting borrowed books has finished")
            return borrowed_books_num[0]["total"]


    def count_by_genre(self):
         with db.conn.cursor(dictionary=True) as cursor:
            logger.info("start counting books by genre..")
            query = """
                SELECT genre, COUNT(*) AS count FROM books
                GROUP BY genre
                """
            cursor.execute(query)

            books_genres = cursor.fetchall()
            if books_genres == []:
                logger.warning("no bookS")
                return None
            logger.info("counting books by genre has comleted")
            return books_genres


    def count_active_borrows_by_member(self, member_id):
        with db.conn.cursor(dictionary=True) as cursor:
            logger.info(f"start counting borrowed books for member {member_id}..")
            query = """
                SELECT COUNT(*) as total FROM books
                WHERE borrowed_by_member_id=%s
                """
            cursor.execute(query, [member_id])

            borrowed_books_num = cursor.fetchall()
            if borrowed_books_num == []:
                logger.info(f"no borrowed booksfor member {member_id}")
                return 0
            
            logger.info(f"counting borrowed books for member {member_id} has finished")
            return borrowed_books_num[0]["total"]


book = BookDb()
