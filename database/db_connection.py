import mysql.connector
from logs.logger_config import logger


def get_conection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root"
    )

    cursor = conn.cursor(dictionary=True)

    cursor.execute("CREATE DATABASE IF NOT EXISTS library_db")
    if cursor.warning_count == 0:
        logger.info("database created")
    
    cursor.execute("USE library_db")
    logger.info("connected to database")
    return conn


conn = get_conection()


def create_tables():
    cursor = conn.cursor(dictionary=True)

    qwery_books = """
        CREATE TABLE IF NOT EXISTS books (
        id INT AUTO_INCREMENT PRIMARY KEY ,
        title VARCHAR(50) NOT NULL ,
        author VARCHAR(50) NOT NULL ,
        genre ENUM("Fiction", "Non-Fiction", "Science", "History", "Other") NOT NULL ,
        is_available BOOLEAN DEFAULT TRUE NOT NULL ,
        borrowed_by_member_id INT)
        """
    
    qwery_members = """
        CREATE TABLE IF NOT EXISTS members (
        id INT AUTO_INCREMENT PRIMARY KEY ,
        name VARCHAR(50) NOT NULL ,
        email VARCHAR(50) NOT NULL UNIQUE ,
        is_active BOOLEAN DEFAULT TRUE NOT NULL ,
        total_borrowes INT NOT NULL)
        """

    cursor.execute(qwery_books)
    cursor.execute(qwery_members)
    if cursor.warning_count == 0:
        logger.info("tables created")









