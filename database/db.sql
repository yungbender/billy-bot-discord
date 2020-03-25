DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
DROP ROLE IF EXISTS billy_bot;

CREATE TABLE client
(
    id VARCHAR(255) PRIMARY KEY,
    current_name VARCHAR(255) NOT NULL
);

CREATE TABLE guild
(
    id VARCHAR(255) PRIMARY KEY,
    guild_name VARCHAR(255) NOT NULL
);

CREATE TABLE karma
(
    id SERIAL PRIMARY KEY,
    karma INTEGER NOT NULL DEFAULT 0,
    avaiable_karma INTEGER NOT NULL DEFAULT 10, 
    guild_id VARCHAR(255) REFERENCES guild(id),
    client_id VARCHAR(255) REFERENCES client(id)
);

CREATE TABLE client_guild
(
    client_id VARCHAR(255) REFERENCES client(id),
    guild_id VARCHAR(255) REFERENCES guild(id)
);

CREATE TABLE prefix_guild
(
    id SERIAL PRIMARY KEY,
    prefix VARCHAR(64) NOT NULL,
    guild_id VARCHAR(255) UNIQUE REFERENCES guild(id)
);

CREATE TABLE copypasta
(
    pasta_name VARCHAR(64) PRIMARY KEY,
    content TEXT NOT NULL
);

CREATE USER billy_bot WITH ENCRYPTED PASSWORD 'billy_pwd';
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO billy_bot;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO billy_bot;
