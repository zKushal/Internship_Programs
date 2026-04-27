-- Run this in PostgreSQL after creating/selecting your target database.
-- Example:
--   psql -U postgres -d learn_nepali -f database/postgres_schema.sql

CREATE TABLE IF NOT EXISTS todos (
    id SERIAL PRIMARY KEY,
    task VARCHAR(255) NOT NULL,
    due_date TIMESTAMP NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending'
);

CREATE INDEX IF NOT EXISTS ix_todos_id ON todos (id);
