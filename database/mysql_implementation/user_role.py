from database.interface.user_role import *
from database.entity.user_role import UserRole

class MysqlUserRole(IUserRole):
    def __init__(self, cnxpool):
        self.cnxpool = cnxpool
        self.tname = 'user_role'

    def read_all(self):
        result = None
        query = f"SELECT * FROM {self.tname};"
        try:
            self.cnx = self.cnxpool.get_connection()
            self.cur = self.cnx.cursor()
            self.cur.execute(query)
            result = [UserRole(*args) for args in self.cur.fetchall()]
            self.cnx.close()
        except Exception as e:
            print(e)
        return result

    def read(self, id):
        result = None
        query = f"SELECT * FROM {self.tname} WHERE id={id};"
        try:
            self.cnx = self.cnxpool.get_connection()
            self.cur = self.cnx.cursor()
            self.cur.execute(query)
            result = UserRole(*self.cur.fetchone())
            self.cnx.close()
        except Exception as e:
            print(e)
        return result
