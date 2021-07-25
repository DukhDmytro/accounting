CREATE TABLE IF NOT EXISTS telegram_user(
    chat_id integer NOT NULL UNIQUE,
    is_bot BOOLEAN NOT NULL,
    first_name VARCHAR(64) NOT NULL,
    last_name VARCHAR(64),
    username VARCHAR(32),
    language_code VARCHAR(35)
);
CREATE TYPE category_type AS ENUM ('expense', 'income');
CREATE TABLE IF NOT EXISTS category(
    codename VARCHAR(15) PRIMARY KEY,
    title VARCHAR(30) UNIQUE NOT NULL,
    description VARCHAR(50) NOT NULL,
    type category_type
);
