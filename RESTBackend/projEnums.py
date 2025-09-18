
from enum import Enum
from pathlib import Path

# Match Status
class matchStatus(str,Enum):
    IP = "IN PRGRESS"
    FINISHED = "FINISHED"

# Match Type
class matchType(str,Enum):
    menSingles = "Men's Singles"
    menDoubles = "Men's Doubles"
    womanSingles = "Women's Singles"
    womenDoubles = "Women's Doubles"
    mixedDoubles = "Mixed Doubles"

DB = "badminton.db"
DB_FILE = Path(__file__).parent / DB
SQL_DIR = Path("sql")

INSERT_MATCH_SQL = "insert_matches.sql"
