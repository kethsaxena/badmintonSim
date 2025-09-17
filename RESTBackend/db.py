import sqlite3
from pathlib import Path
import sqlite3
from threading import Lock
from projEnums import SQL_DIR
import inspect
class DBConnection:
    _instances = {}           # Stores singleton per db_path
    _lock = Lock()            # Global lock for thread safety

    def __new__(cls, db_path: str):
        # Double-checked locking to make thread-safe Singleton
        db_file = Path(db_path).resolve()

        if db_file not in cls._instances:
            with cls._lock:
                if db_file not in cls._instances:  # Re-check inside lock
                    instance = super(DBConnection, cls).__new__(cls)
                    instance._init_connection(db_file)
                    cls._instances[db_file] = instance
                    print(f"✅ [DBConnection] New connection created for {db_file}")
        else:
                cls._instances[db_file]._notify_reuse()
        return cls._instances[db_file]

    def _init_connection(self, db_file):
        """Initialize the DB connection."""
        self.db_file = db_file
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()
    
    def _notify_reuse(self):
        """Notify when existing connection is reused."""
        print(f"✅⚠️ [DBConnection] Existing connection reused {self.db_file}")

    def execute_statement(self, sql: str= None, params: dict = None) -> bool:  
        """
        Execute SQL query or script.
        - If sql contains multiple statements -> executescript
        - If single statement -> execute with optional params
        """

        if not sql:
            raise ValueError("FAIL: ❌ Invalid  `sql` check ")
        
        try:
            self.cursor.execute(sql, params)
            self.connection.commit()
            
            return True
        except sqlite3.Error as e:
            print(f"❌ ERROR:{inspect.stack()[0].function}| SQL execution FAIL: {e}")
            return False
        
    def execute_from_file(self, filename:str, params:dict=None):
        """
        Load SQL from file in SQL_DIR and execute.
        """
        # Detect multi-statement SQL
        isSqlFile = filename.strip().rstrip(".sql")
        
        if not isSqlFile:
            raise TypeError(f"❌ ERROR:{inspect.stack()[0].function}: Check File {filename}")
        
        file_path = SQL_DIR / filename
        with open(file_path, "r") as f:
            sql = f.read()
        try:
            self.cursor.executescript(sql)
            self.connection.commit()
            print(f"✅ SQL execution SUCCESS:{filename}")
        except sqlite3.Error as e:
            print(f"❌ ERROR:{inspect.stack()[0].function} | SQL execution FAIL: {e}")

    def close(self):
        """Close the DB connection."""
        if self.connection:
            self.connection.close()
            DBConnection._instance = None
            print("✅⚠️[DBConnection] Connection closed")
            # Remove from singleton registry
            if self.db_file in DBConnection._instances:
                del DBConnection._instances[self.db_file]

