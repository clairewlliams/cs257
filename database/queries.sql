SELECT noc 
FROM nations
ORDER BY noc;


SELECT DISTINCT athletes.athlete_name, nations.NOC
FROM nations, athletes_games, athletes
WHERE athletes.id = athletes_games.athlete_id
AND nations.id = athletes_games.nation_id
AND nations.NOC = 'KEN'
ORDER BY athlete_name;


SELECT DISTINCT athletes.athlete_name, contests_medals.medal, games.game_year, games.season, games.city, contests.contest
FROM athletes, contests_medals, games, athletes_games, contests
WHERE athletes.id = athletes_games.athlete_id
AND games.id = athletes_games.game_id
AND athletes_games.id = contests_medals.athletes_nations_games_id
AND contests_medals.medal IS NOT NULL
AND athletes.athlete_name LIKE '%"Greg" Louganis'
AND contests.id = contests_medals.contest_id 
ORDER BY games.game_year;


SELECT nations.noc, COUNT(...)

