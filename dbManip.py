# coding: utf-8

import psycopg2

class dbManipulate(object):
    def __init__(self,
                 database = "testdb",
                 user = "postgres",
                 password = "cohondob",
                 host = "127.0.0.1",
                 port = "5432"):
        self.conn = psycopg2.connect(database, user, password, host, port)

    def __del__(self):
        self.conn.close()

    def Insert(self, ID, date, time, erl, updata, downdata, alldata, netType):
        cursor = self.conn.cursor()
        cursor.execute("insert into cell_data (ID, date, time, erl, updata, downdata, alldata, netType)\
                        values(ID, date, time, erl, updata, downdata, alldata, netType)")


if __name__ == "__main__":
    pass