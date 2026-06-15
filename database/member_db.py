from logs.logger_config import logger
from database.db_connection import db


class MemberDB:
    def __init__(self):
        pass

    def create_member(self, data):
        with db.conn.cursor(dictionary=True) as cursor:
            print(f"--- DATABASE RECEIVED EMAIL: {data.get('email')} ---")
            logger.info("start creating member..")
            query = """
                INSERT INTO members (name, email)
                VALUES (%s, %s)
                """
            Values = [data["name"], data["email"]]

            cursor.execute(query, Values)
            member_id = cursor.lastrowid
            db.conn.commit()

            logger.info("member created successfully")
            return self.get_member_by_id(member_id)


    def get_all_members(self):
        with db.conn.cursor(dictionary=True) as cursor:
            logger.info("start getting members table..")
            query = """
                SELECT * FROM members 
                """
            cursor.execute(query)
            members = cursor.fetchall()

            if not members:
                logger.warning("members table is empty")
                return []
            logger.info("getting members table has finished")
            return members


    def get_member_by_id(self, id:int):
        with db.conn.cursor(dictionary=True) as cursor:
            logger.info(f"start getting member {id}..")
            query = """
                SELECT * FROM members WHERE id=%s
                """
            cursor.execute(query, [id])
            member = cursor.fetchall()

            if not member:
                logger.warning(f"member id {id} not found")
                return None
            logger.info(f"getting member id {id} has finished")
            return member[0]


    def update_member(self, id:int, data:dict):
        with db.conn.cursor(dictionary=True) as cursor:
            logger.info(f"start updating for member {id}")

            columns = ", ".join(f"{k}=%s" for k in data.keys())
            values = [v for v in data.values()] + [id]
            query = F"""
                UPDATE members
                SET {columns}
                WHERE id=%s
                """
            cursor.execute(query, values)

            if cursor.rowcount == 0:
                logger.warning("nothing have change")
                return None

            db.conn.commit()
            return data
    

    def deactivate_member(self, id:int):
        with db.conn.cursor(dictionary=True) as cursor:
            logger.info("start deactivate member..")
        
            query = """
                UPDATE members
                SET is_active=FALSE WHERE id=%s
                """
            cursor.execute(query, [id])
            db.conn.commit()
            member = self.get_member_by_id(id)

            logger.info("deactivate member has finished")
            return member
        

    def activate_member(self, id:int):
        with db.conn.cursor(dictionary= True) as cursor:
            logger.info("start activate member..")
            query = """
                UPDATE members
                SET is_active=TRUE
                WHERE id=%s
                """
            cursor.execute(query, [id])
            db.conn.commit()
            member = self.get_member_by_id(id)
            
            logger.info("activate member has finished")
            return member


    def increment_borrows(self, id:int):
        with db.conn.cursor(dictionary=True) as cursor:
            cursor.execute("""
                UPDATE members
                SET total_borrows = total_borrows + 1
                WHERE id=%s
                """, [id])
            
            db.conn.commit()
            member = self.get_member_by_id(id)
            logger.info(f"increment borrows for member {id} has finished")

            return member
        
    
    def count_active_members(self):
        with db.conn.cursor(dictionary=True) as cursor:
            logger.info("start getting active members")
            cursor.execute("""
               SELECT COUNT(*) AS total
               FROM members
               WHERE is_active=TRUE
               """)
            active_num = cursor.fetchall()[0]["total"]

            if not active_num:
                logger.warning("no active members")
                return None
            logger.info("getting active members has finished")
            return active_num
        
    
    def get_top_member(self):
        with db.conn.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT MAX(total_borrows) AS total_borrows FROM members 
                """)
            top = cursor.fetchall()[0]["total_borrows"]
            
            cursor.execute("""
                SELECT id, total_borrows FROM members WHERE total_borrows=%s
               """, [top])
            top_members = cursor.fetchall()
            
            return top_members
            


member = MemberDB()
