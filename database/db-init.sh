#!/usr/bin/env bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE TABLE compressor_pressure (
        timestamp TIMESTAMPTZ NOT NULL,
        asset_id BIGINT NOT NULL,
        sensor_name VARCHAR (25) NOT NULL,
        pressure REAL,
        PRIMARY KEY (timestamp, asset_id)
    );
EOSQL
