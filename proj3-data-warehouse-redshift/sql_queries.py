import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS  songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events (
    artist varchar,
    auth varchar,
    first_name varchar,
    gender varchar(1),
    item_in_session varchar,
    last_name varchar,
    length varchar,
    level varchar(10),
    location varchar,
    method varchar(10),
    page varchar(30),
    registration varchar,
    session_id varchar,
    song varchar,
    status varchar,
    ts varchar,
    useragent varchar,
    user_id varchar
)
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs (
    num_songs varchar,
    artist_id varchar,
    artist_latitude varchar,
    artist_longitude varchar,
    artist_location varchar,
    artist_name varchar,
    song_id varchar,
    title varchar,
    duration varchar,
    year varchar
)
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id bigint IDENTITY(0,1) PRIMARY KEY,
    start_time timestamp NOT NULL, 
    user_id int NOT NULL, 
    level varchar NOT NULL, 
    song_id varchar, 
    artist_id varchar, 
    session_id int NOT NULL, 
    location varchar, 
    user_agent varchar
) SORTKEY(start_time)
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
    user_id int PRIMARY KEY, 
    first_name varchar NOT NULL, 
    last_name varchar NOT NULL, 
    gender varchar(1) NOT NULL, 
    level varchar
) DISTSTYLE ALL SORTKEY(user_id)
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
    song_id varchar PRIMARY KEY, 
    title varchar NOT NULL, 
    artist_id varchar NOT NULL, 
    year int, 
    duration int NOT NULL
) DISTSTYLE ALL SORTKEY(song_id)
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
    artist_id varchar PRIMARY KEY,
    name varchar NOT NULL,
    location varchar,
    latitude numeric(8, 5),
    longitude numeric(8, 5)
) DISTSTYLE ALL SORTKEY(artist_id)
""")

# start_time in milliseconds
time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
    start_time timestamp PRIMARY KEY, 
    hour int NOT NULL,
    day int NOT NULL, 
    week int NOT NULL, 
    month int NOT NULL, 
    year int NOT NULL, 
    weekday int NOT NULL
) DISTSTYLE ALL SORTKEY(start_time)
""")

# STAGING TABLES

staging_events_copy = ("""
COPY staging_events FROM {}
CREDENTIALS 'aws_iam_role={}'
JSON {}
""").format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'], config['S3']['LOG_JSONPATH'])

staging_songs_copy = ("""
COPY staging_songs FROM {}
CREDENTIALS 'aws_iam_role={}'
JSON 'auto'
""").format(config['S3']['SONG_DATA'], config['IAM_ROLE']['ARN'])

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT 
    (TIMESTAMP 'epoch' + (ts::bigint / 1000) * INTERVAL '1 second') as start_time, 
    user_id::integer, 
    level, 
    song.song_id, 
    artist.artist_id,
    session_id::integer, 
    event.location, 
    useragent as user_agent
FROM staging_events event 
LEFT JOIN artists artist
  ON TRIM(LOWER(artist.name)) = TRIM(LOWER(event.artist))
LEFT JOIN songs song
  ON TRIM(LOWER(song.title)) = TRIM(LOWER(event.song))
WHERE event.page = 'NextSong'
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, level, gender)
  SELECT 
      staging_events.user_id::integer,
      first_name,
      last_name,
      level,
      gender
  FROM staging_events
  INNER JOIN 
      (SELECT user_id, MAX(ts) AS ts
      FROM staging_events
      WHERE user_id IS NOT NULL AND user_id != ''
      GROUP BY 1) AS staging_events_groupped_by_user
    ON staging_events_groupped_by_user.user_id = staging_events.user_id AND
       staging_events_groupped_by_user.ts = staging_events.ts

""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, year, artist_id, duration)
  SELECT
      song_id,
      title,
      CASE year::integer
        WHEN 0 THEN NULL
        ELSE year::integer
        END,
      artist_id,
      duration::numeric
  FROM staging_songs
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, latitude, longitude, location)
  SELECT
      artist_id,
      artist_name,
      artist_latitude,
      artist_longitude,
      artist_location
  FROM staging_songs
""")

time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, weekday, month, year)
  SELECT DISTINCT 
      ts,
      EXTRACT(HOUR FROM ts),
      EXTRACT(DAY FROM ts),
      EXTRACT(WEEK FROM ts),
      EXTRACT(WEEKDAY FROM ts),
      EXTRACT(MONTH FROM ts),
      EXTRACT(YEAR FROM ts)
  FROM (
      SELECT distinct '1970-01-01'::date + ts/1000 * interval '1 second' as ts
      FROM staging_events
  )
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [user_table_insert, song_table_insert, artist_table_insert, time_table_insert, songplay_table_insert]
