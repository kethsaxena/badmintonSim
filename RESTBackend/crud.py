import sqlite3
from enum import Enum
import uuid 
from projEnums import matchStatus,SQL_DIR, DB,INSERT_MATCH_SQL,SELECT_MATCHINP_SQL
from db import DBConnection

def load_sql(filename:str):
    file_path = SQL_DIR / filename
    with open(file_path, "r") as f:
        sql = f.read()
    return sql

def init_db(**kwargs):
    conn = kwargs["DBconOBJ"]
    conn.execute_from_file("createTable_matches.sql") 
    conn.connection.commit()
    conn.execute_from_file("createTable_events.sql")
    conn.connection.commit()

def insert_match(**kwargs) -> bool:
    conn = kwargs["DBconOBJ"]
    data = kwargs["values"]
    filename = kwargs["filename"]
    conn.execute_from_file(filename,data)
    conn.connection.commit()

def get_currMatches(**kwargs) -> bool:
    conn = kwargs["DBconOBJ"]
    filename = kwargs["filename"]
    data = conn.execute_from_file(filename).fetchall()
    my_dict = {x:(y, z) for x, y, z in data}
    return my_dict

if __name__ == "__main__":
    # Can be run as a independent Script
    # print("CRUD APP")
    conn = DBConnection(DB)
    # init_db(DBconOBJ=conn)
    
    # from datetime import datetime
    # sttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # endtime = None
    # matchid = uuid.uuid4().hex
    # event = "Men's Single"
    # status = "IN PROGRESS"
    # summary = "Player A vs Player B"
    
    # data = {
    # "sttime": sttime,
    # "endtime": endtime,
    # "matchid": matchid,
    # "event": event,
    # "summary": summary,
    # "status": status
    # }

    # filename=INSERT_MATCH_SQL
    # insert_match(DBconOBJ=conn,values=data,filename=filename)
    print(len(get_currMatches(DBconOBJ=conn,filename=SELECT_MATCHINP_SQL)))
