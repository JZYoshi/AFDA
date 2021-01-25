DROP TABLE IF EXISTS climb;
DROP TABLE IF EXISTS cruise;
DROP TABLE IF EXISTS descent;
DROP TABLE IF EXISTS general_info;

CREATE TABLE general_info (
    flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
    airline TEXT,
    icao TEXT,
    icao_airline TEXT
);

CREATE TABLE cruise (
    flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
    duration FLOAT,
    avg_speed FLOAT,
    std_speed FLOAT,
    avg_vertrate_speed FLOAT,
    std_vertrate_speed FLOAT,
    max_spd FLOAT,
    min_spd FLOAT,
    max_vertrate_speed FLOAT,
    min_vertrate_speed FLOAT,
    mean_altitude FLOAT,
    std_altitude FLOAT
);

CREATE TABLE climb (
    flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
    duration FLOAT,
    avg_speed FLOAT,
    std_speed FLOAT,
    avg_vertrate_speed FLOAT,
    std_vertrate_speed FLOAT,
    max_spd FLOAT,
    min_spd FLOAT,
    max_vertrate_speed FLOAT,
    min_vertrate_speed FLOAT
);

CREATE TABLE descent (
    flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
    duration FLOAT,
    avg_speed FLOAT,
    std_speed FLOAT,
    avg_vertrate_speed FLOAT,
    std_vertrate_speed FLOAT,
    max_spd FLOAT,
    min_spd FLOAT,
    max_vertrate_speed FLOAT,
    min_vertrate_speed FLOAT
);