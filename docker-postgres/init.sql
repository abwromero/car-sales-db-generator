CREATE SCHEMA raw;
DROP SCHEMA public;
SET search_path = raw;
CREATE TABLE raw_values(
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    license VARCHAR(13),
    num VARCHAR(15),
    email VARCHAR(40),
    company VARCHAR(80),
    street VARCHAR(80),
    city VARCHAR(40),
    province VARCHAR(20),
    date VARCHAR(27),
    bank VARCHAR(40),
    terms SMALLINT,
    car VARCHAR(100),
    color VARCHAR(8),
    plate VARCHAR(7)
    );