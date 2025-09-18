import sqlite3
from enum import Enum
import uuid 
from projEnums import matchStatus,SQL_DIR, DB,DB_FILE
from db import DBConnection

def get_connection():
    try:
        conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        print(f"✅ SQLite connection established to {DB_FILE}")
        return conn
    except sqlite3.Error as e:
        print(f"❌ Failed to connect to SQLite database: {e}")
        return None

def load_sql(filename:str):
    file_path = SQL_DIR / filename
    with open(file_path, "r") as f:
        sql = f.read()
    return sql
#############################################################
# def init_db():
#     try: 
#         STATUS = False
#         conn = get_connection()
#         cursor = conn.cursor()
#         filename="createTable_matches.sql"
#         CREATE_MATCH_SQL = load_sql(filename)
#         cursor.execute(CREATE_MATCH_SQL)
#         conn.commit()
#         print(f"Successfully Created: {filename}")
#         filename="createTable_events.sql"
#         CREATE_MATCH_SQL = load_sql(filename)
#         cursor.execute(CREATE_MATCH_SQL)
#         conn.commit()
#         print(f"Successfully Created: {filename}")
#     except Exception as e:
#         print(f"Error inserting match: {e}")

# def insert_match(*,DBconObj=None,sttime="",endtime=None,matchid="",event="",summary="",status=matchStatus.IP): 
#     STATUS = False
#     conn = get_connection()
#     cursor = conn.cursor()
    
#     INSERT_MATCH_SQL = load_sql("insert_matches.sql")
#     cursor.execute(INSERT_MATCH_SQL, (sttime,endtime,matchid,event,summary,status))
#     conn.commit()

#     # Verify insertion
#     try:
#         SELECT_MATCH_SQL=load_sql("select_match.sql")
#         cursor.execute(SELECT_MATCH_SQL, (matchid,))
#         row = cursor.fetchall()
#         print(row)
#         if row:
#             STATUS = True
#         print(f"{matchid} ROW Inserted")
#     except Exception as e:
#         print(f"Error inserting match: {e}")
    
#     return STATUS

# # THIS WORKS
# if __name__ == "__main__":
#     init_db()
#     from datetime import datetime
#     sttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     endtime = None
#     matchid = uuid.uuid4().hex
#     event = "Men's Single"
#     status = "IN PROGRESS"
#     summary = "Player A vs Player B"
#     success = insert_match(sttime=sttime, endtime=endtime, matchid=matchid, event=event, summary=summary,status=status)
#     if success:
#         print("Insert successful")
#########################################################################

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
    # conn = DBConnection(DB)
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

    # filename="insert_matches.sql"
    # insert_match(DBconOBJ=conn,values=data,filename=filename)

# if __name__ == "__main__":
#     conn = DBConnection(DB)
#     init_db(conn)
#     from datetime import datetime
#     sttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     endtime = None
#     matchid = uuid.uuid4().hex
#     event = "Men's Single"
#     status = "IN PROGRESS"
#     summary = "Player A vs Player B"
#     success = insert_match(DBconObj=conn,sttime=sttime, endtime=endtime, matchid=matchid, event=event, summary=summary,status=status)

   
# def runSQL(filename: str, DBconObj,isScript=False):
#     """Execute SQL from file with commit"""
#     sql = load_sql(filename)  # load the SQL
#     conn = DBconObj
#     cursor = DBconObj.cursor()
#     if isScript:
#         cursor.executescript(sql)       # or conn.executescript(sql) for multiple statements
#     else:
#         cursor.execute(sql)
#     conn.commit()

# CRUD APPS
# def insert_match(*,DBconObj:DBConnection,sttime:str,matchid:str,endtime=None,event="",summary="",status=matchStatus.IP) -> bool: 

#     params = (sttime, endtime, matchid,event,summary,status)
#     print(params)
#     filename="insert_matches.sql"
#     file_path = SQL_DIR / filename
#     with open(file_path, "r") as f:
#         sql = f.read()
#     isTrue=DBconObj.cursor.execute(sql, params)

#     try:
#         if isTrue:
#             print(f"{matchid} ROW Inserted")
#     except Exception as e:
#             print(f"{matchid} Fail to insert ROW")
    
#     return isTrue

# def insert_match(*,DBconObj:DBConnection,sttime:str,matchid:str,endtime=None,event="",summary="",status=matchStatus.IP) -> bool: 
#     params = {
#     "sttime": sttime,
#     "endtime": endtime,
#     "matchid": matchid,
#     "event": event,
#     "summary": summary,
#     "status": status
# }
#     print(params)
#     # isTrue=False
#     isTrue = DBconObj.execute_from_file("insert_matches.sql",params)
#     # Verify insertion
#     try:
#         if isTrue:
#             print(f"{matchid} ROW Inserted")
#     except Exception as e:
#             print(f"{matchid} Fail to insert ROW")
    
#     return isTrue
