CREATE TABLE sales(
    id SERIAL,
    na decimal,
    eu decimal,
    jp decimal,
    other decimal,
    global_sales decimal
);

CREATE TABLE platforms(
    id SERIAL,
    platform text
);

CREATE TABLE games_platforms(
    games_id integer,
    platforms_id integer,
    sales_id integer,
    user_score decimal,
    critic_score integer
);

CREATE TABLE games(
    id SERIAL,
    name text,
    year integer,
    rating text,
    genre_id integer,
    publisher_id integer
);

CREATE TABLE publishers(
    id SERIAL,
    publisher text
);

CREATE TABLE genres(
    id SERIAL,
    genre text
);
