CREATE TABLE IF NOT EXISTS telegram_user(
    chat_id integer NOT NULL UNIQUE,
    is_bot BOOLEAN NOT NULL,
    first_name VARCHAR(64) NOT NULL,
    last_name VARCHAR(64),
    username VARCHAR(32),
    language_code VARCHAR(35)
);
