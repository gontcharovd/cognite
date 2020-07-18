CREATE TABLE pressure (
    timestamp TIMESTAMPTZ NOT NULL,
    asset_id BIGINT NOT NULL,
    name VARCHAR (25) NOT NULL,
    pressure REAL
);


