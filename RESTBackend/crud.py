import sqlite3
from enum import Enum
import uuid 
from projEnums import matchStatus,SQL_DIR, DB,DB_FILE
from db import DBConnection

def load_sql(filename:str):
    file_path = SQL_DIR / filename
    with open(file_path, "r") as f:
        sql = f.read()
    return sql

def init_db(**kwargs):
    conn = kwargs["DBconOBJ"]
    conn.execute_from_file("createTable_matches.sql") 
    conn.execute_from_file("createTable_events.sql")

def insert_match(**kwargs) -> bool:
    conn = kwargs["DBconOBJ"]
    data = kwargs["values"]
    filename = kwargs["filename"]
    conn.execute_from_file(filename,data)

if __name__ == "__main__":
    print("CRUD APP")
    conn = DBConnection(DB)
    init_db(DBconOBJ=conn)
    
    from datetime import datetime
    sttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    endtime = None
    matchid = uuid.uuid4().hex
    event = "Men's Single"
    status = "IN PROGRESS"
    summary = "Player A vs Player B"
    
    data = {
    "sttime": sttime,
    "endtime": endtime,
    "matchid": matchid,
    "event": event,
    "summary": summary,
    "status": status
    }

    filename="insert_matches.sql"
    insert_match(DBconOBJ=conn,values=data,filename=filename)
