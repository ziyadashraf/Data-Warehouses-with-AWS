import configparser


config = configparser.ConfigParser()
config.read("dwh.cfg")


iam_role = config.get("IAM_ROLE", "ARN")
log_data = config.get("S3", "LOG_DATA")
json_log = config.get("S3", "LOG_JSONPATH")
song_data = config.get("S3", "SONG_DATA")
s3_region = config.get("S3", "S3_REGION")


staging_events_table_drop = "DROP TABLE IF EXISTS staging_events CASCADE"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs CASCADE"
songplay_table_drop = "DROP TABLE IF EXISTS songplays CASCADE"
user_table_drop = "DROP TABLE IF EXISTS users CASCADE"
song_table_drop = "DROP TABLE IF EXISTS songs CASCADE"
artist_table_drop = "DROP TABLE IF EXISTS artists CASCADE"
time_table_drop = "DROP TABLE IF EXISTS time CASCADE"


staging_events_table_create = """

    CREATE TABLE IF NOT EXISTS staging_events (
        artist          TEXT,
        auth            TEXT,
        firstName       TEXT,
        gender          TEXT,
        itemInSession   INT,
        lastName        TEXT,
        length          TEXT,
        level           TEXT,
        location        TEXT,
        method          TEXT,
        page            TEXT,
        registration    TEXT,
        sessionId       INT,
        song            TEXT,
        status          INT,
        ts              BIGINT,
        userAgent       TEXT,
        userId          INT
    );

"""

staging_songs_table_create = """

CREATE TABLE IF NOT EXISTS staging_songs (
    num_songs          INT,
    artist_id          TEXT,
    artist_latitude    TEXT,
    artist_longitude   TEXT,
    artist_location    TEXT,
    artist_name        TEXT,
    song_id            TEXT,
    title              TEXT,
    duration           TEXT,
    year               INT
);
"""

songplay_table_create = """

    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id   INT         IDENTITY (0,1)   PRIMARY KEY,
        user_id       INT,       
        start_time    TIMESTAMP   SORTKEY,
        level         TEXT  ,    
        song_id       TEXT        DISTKEY,
        artist_id     TEXT,      
        session_id    INT,       
        location      TEXT,    
        user_agent    TEXT,
        FOREIGN KEY(start_time)   REFERENCES time(start_time),
        FOREIGN KEY(user_id)      REFERENCES users(user_id),
        FOREIGN KEY(song_id)      REFERENCES songs(song_id),
        FOREIGN KEY(artist_id)    REFERENCES artists(artist_id)      
    );
                        
"""

user_table_create = """

    CREATE TABLE IF NOT EXISTS users (
        user_id      INT  PRIMARY KEY,
        first_name   TEXT,   
        last_name    TEXT,   
        gender       TEXT,
        level        TEXT     
    );

"""

song_table_create = """

    CREATE TABLE IF NOT EXISTS songs (
            song_id     TEXT    NOT NULL   PRIMARY KEY   DISTKEY,
            title       TEXT    NOT NULL,
            artist_id   TEXT    NOT NULL,
            year        INT,
            duration    FLOAT,  
            FOREIGN KEY(artist_id) REFERENCES artists(artist_id)
);
"""

artist_table_create = """

    CREATE TABLE IF NOT EXISTS artists (
        artist_id   TEXT    NOT NULL   PRIMARY KEY,
        name        TEXT    NOT NULL,
        location    TEXT,
        latitude    FLOAT,  
        longitude   FLOAT
    );
"""

time_table_create = """

    CREATE TABLE IF NOT EXISTS time (
        start_time   TIMESTAMP   NOT NULL   PRIMARY KEY   SORTKEY,
        hour         INT         NOT NULL,
        day          INT         NOT NULL,
        week         INT         NOT NULL,
        month        INT         NOT NULL,
        year         INT         NOT NULL,
        weekday      INT         NOT NULL
    );

"""


staging_events_copy = (
    """

    COPY staging_events FROM {}
    CREDENTIALS 'aws_iam_role={}'
    REGION {} 
    JSON {}
            
"""
).format(log_data, iam_role, s3_region, json_log)


staging_songs_copy = (
    """
    COPY staging_songs FROM {}
    CREDENTIALS 'aws_iam_role={}'
    FORMAT AS JSON 'auto' 
    REGION {}

"""
).format(song_data, iam_role, s3_region)


songplay_table_insert = """
    INSERT INTO songplays(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
        SELECT TIMESTAMP 'epoch' + e.ts/1000 *INTERVAL '1 second',
        e.userId,
        e.level,
        s.song_id,
        s.artist_id,
        e.sessionId,
        e.location,
        e.userAgent
        FROM staging_events as e
        LEFT JOIN staging_songs as s
        ON e.song = s.title 
        AND e.artist = s.artist_name
        AND e.length = s.duration
        WHERE page='NextSong';
        
"""

user_table_insert = """

    INSERT INTO users(user_id, first_name, last_name, gender, level)
    SELECT DISTINCT UserId,
    firstName,
    lastName,
    gender,
    level
    FROM staging_events
    WHERE page='NextSong' AND userId IS NOT NULL;

"""

song_table_insert = """
    INSERT INTO songs(song_id, title, artist_id, year, duration)
        SELECT DISTINCT song_id,
        title,
        artist_id,
        year,
        CONVERT(FLOAT, duration)
        FROM staging_songs;
"""

artist_table_insert = """

    INSERT INTO artists(artist_id, name, location, latitude, longitude)
        SELECT DISTINCT artist_id,
        artist_name,
        artist_location,
        CONVERT(FLOAT, artist_latitude),
        CONVERT(FLOAT, artist_longitude)
        FROM staging_songs;
"""

time_table_insert = """

    INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT DISTINCT TIMESTAMP 'epoch' + e.ts/1000 *INTERVAL '1 second' AS tm,
    EXTRACT(hour FROM tm),
    EXTRACT(day FROM tm),
    EXTRACT(week FROM tm),
    EXTRACT(month FROM tm),
    EXTRACT(year FROM tm),
    EXTRACT(dow FROM tm)
    FROM staging_events as e
    WHERE e.page='NextSong';

"""


create_table_queries = [
    staging_events_table_create,
    staging_songs_table_create,
    user_table_create,
    artist_table_create,
    song_table_create,
    time_table_create,
    songplay_table_create,
]
drop_table_queries = [
    staging_events_table_drop,
    staging_songs_table_drop,
    songplay_table_drop,
    user_table_drop,
    song_table_drop,
    artist_table_drop,
    time_table_drop,
]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [
    songplay_table_insert,
    user_table_insert,
    song_table_insert,
    artist_table_insert,
    time_table_insert,
]
