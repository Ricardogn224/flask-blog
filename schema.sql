DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS userdata;

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS userdata (
    id INTEGER PRIMARY KEY,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    username VARCHAR (255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
)