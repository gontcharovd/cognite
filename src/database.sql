SET TIMEZONE='UTC';

CREATE TABLE compressor_pressure (
    timestamp TIMESTAMPTZ NOT NULL,
    asset_id BIGINT NOT NULL,
    sensor_name VARCHAR (25) NOT NULL,
    pressure REAL,
    PRIMARY KEY (timestamp, asset_id)
);


