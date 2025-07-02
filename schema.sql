CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    query TEXT,
    response TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
