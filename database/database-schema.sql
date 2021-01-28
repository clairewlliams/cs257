CREATE TABLE athletes(
    id int,
    athlete_name text,
    sex text,
    height int,
    athlete_weight float
);

CREATE TABLE nations(
    id int,
    NOC text,
    team text
);

CREATE TABLE games(
    id int,
    game_year int,
    season text,
    city text
);

CREATE TABLE contests(
    id int,
    contest text,
    sport text
);

CREATE TABLE athletes_games(
    id int,
    athlete_id int,
    nation_id int,
    game_id int
);

CREATE TABLE contests_medals(
    id int, 
    athletes_games_id int,
    contest_id int,
    medal text
);