import mysql.connector
from logs.logger_config import logger


class Db:
    def __init__(self):
        self.conn = self.get_connection()
        self.create_db()
        self.create_tables()


    def get_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="root"
        )

    def create_db(self):

        with self.conn.cursor(dictionary=True) as cursor:

            cursor.execute("CREATE DATABASE IF NOT EXISTS library_db")
            if cursor.warning_count == 0:
                logger.warning("database created")
            
            cursor.execute("USE library_db")
            logger.info("connected to database")

    def create_tables(self):
        with self.conn.cursor(dictionary=True) as cursor:

            query_books = """
                CREATE TABLE IF NOT EXISTS books (
                id INT AUTO_INCREMENT PRIMARY KEY ,
                title VARCHAR(50) NOT NULL ,
                author VARCHAR(50) NOT NULL ,
                genre ENUM("Fiction", "Non-Fiction", "Science", "History", "Other") NOT NULL ,
                is_available BOOLEAN DEFAULT TRUE NOT NULL ,
                borrowed_by_member_id INT)
                """
            
            query_members = """
                CREATE TABLE IF NOT EXISTS members (
                id INT AUTO_INCREMENT PRIMARY KEY ,
                name VARCHAR(50) NOT NULL ,
                email VARCHAR(50) NOT NULL UNIQUE ,
                is_active BOOLEAN DEFAULT TRUE NOT NULL ,
                total_borrows INT NOT NULL)
                """

            cursor.execute(query_books)
            cursor.execute(query_members)
            if cursor.warning_count == 0:
                logger.warning("tables created")

db = Db()









