CREATE TABLE compressor_pressure (
    timestamp TIMESTAMPTZ NOT NULL,
    asset_id BIGINT NOT NULL,
    sensor_name VARCHAR (25) NOT NULL,
    pressure REAL,
    PRIMARY KEY (timestamp, asset_id)
);

VACUUM (VERBOSE, ANALYZE) compressor_pressure;

DELETE FROM compressor_pressure
WHERE timestamp < DATE(CURRENT_DATE - INTERVAL '3 months');
