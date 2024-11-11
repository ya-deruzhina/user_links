#!/bin/bash

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE shtutgart WITH OWNER postgres;
    GRANT ALL PRIVILEGES ON DATABASE shtutgart TO postgres;
EOSQL
