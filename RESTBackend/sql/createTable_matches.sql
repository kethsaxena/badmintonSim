CREATE TABLE IF NOT EXISTS matches (
        sttime TEXT NOT NULL,
        endtime TEXT,
        matchid TEXT PRIMARY KEY,
        event TEXT NOT NULL,
        status TEXT NOT NULL,
        summary BLOB       
    )
