import pymysql
import sys
from time import sleep
class DB:
    def __init__(self, data):
        try:
            self.db = pymysql.connect(data["host"], data["username"], data["password"], data["dbname"], port=data["port"])
            self.cursor = self.db.cursor()
            self.__tableName = data["table"]
            self.__table_exists()
        except Exception as e:
            print(e)
            sys.exit(0)

    def __detect_tables(self, name):
        self.__execute("show tables;")
        tables = self.cursor.fetchall()
        for i in tables:
            if name == i[0]:
                return False
        return True

    def __table_exists(self):
        if self.__detect_tables(self.__tableName):
            self.createTable()
            print("已创建数据表")

    def __execute(self,query):
        try:
            self.db.ping(reconnect=True)
            self.cursor.execute(query)
            self.db.commit()
        except Exception as e:
            e = str(e)
            if "PRIMARY" in e:
                return
            if "Data" in e:
                print(e, query)
                return
            sleep(2)
            self.__execute(query)

    def createTable(self):
        query = f"""
        CREATE TABLE {self.__tableName}(
            level char(3),
            region varchar(10),
            title varchar(70) not null,
            dramaType varchar(20),
            type varchar(50),
            company varchar(255),
            imgurl varchar(150),
            rank int,
            url varchar(100) not null primary key,
            score varchar(4),
            introduction text,
            translator varchar(100),
            actors varchar(1000),
            formerName varchar(255),
            alias varchar(100),
            screenwriter varchar(500),
            imdb varchar(100),
            premiereDate int,
            language varchar(50),
            directors varchar(1000)
        )
        """
        self.__execute(query)

    def insert(self, val):
        args = []
        result = []
        for i in val:
            v = val[i]
            if not v: continue
            args.append(i)
            result.append(str(v) if isinstance(v, int) else "'{}'".format(str(v).replace("'","''").replace("\\","\\\\")))
        query = f"INSERT INTO {self.__tableName} ({','.join(args)}) VALUES ({','.join(result)})"
        self.__execute(query)


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()