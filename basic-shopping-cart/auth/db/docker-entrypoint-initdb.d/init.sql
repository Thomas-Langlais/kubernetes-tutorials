CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE user_account (
    id uuid default uuid_generate_v4() primary key,
    username varchar(30),
    password varchar(3000),
    email varchar(50)
);