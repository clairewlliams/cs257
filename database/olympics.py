#Claire Williams
import sys
import argparse
import psycopg2
from config import password
from config import database
from config import user

def get_parsed_arguments():
    '''
    Returns parsed arguments
    '''
    parser = argparse.ArgumentParser(description='Queries olympics database')
    parser.add_argument('--athletes', '-a', nargs=1, metavar='NOC', help='Lists the names of athletes from a given NOC')
    parser.add_argument('--medals', '-m', action="store_true", help='Lists NOCs in decreasing order by number of gold medals they have won')
    parser.add_argument('--name', '-n', nargs=1, metavar='name', help='Lists the medals won by a given athlete')
    parser.add_argument('--limit', '-l', nargs=1, metavar='limit', type=int, help='Limits results to a given limit')
    parsed_arguments = parser.parse_args()
    return parsed_arguments

def get_database_connection():
    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
    except Exception as e:
        print(e)
        exit()
    return connection

def list_athletes(noc, limit, cursor):
    query = '''SELECT DISTINCT athletes.athlete_name
                FROM athletes, nations, athletes_games
                WHERE athletes_games.athlete_id = athletes.id
                AND athletes_games.nation_id = nations.id
                AND nations.noc = %s
                ORDER BY athletes.athlete_name
            '''
    if limit > 0:
        query += ''' LIMIT ''' + str(limit) + ''';'''
    else:
        query += ''';'''
    try:
        cursor.execute(query, (noc,))
    except Exception as e:
        print(e)
        exit()

    print('===== Athletes from {0} ====='.format(noc))
    for row in cursor:
        print(row[0])
    print()

def list_medals(limit, cursor):
    '''
    Prints NOCs in decreasing order by number of gold medals won
    '''
    query = '''SELECT nations.NOC, COUNT(contests_medals.medal)
            FROM nations, athletes_games, contests_medals
            WHERE contests_medals.medal = 'Gold'
            AND contests_medals.athletes_games_id = athletes_games.id
            AND athletes_games.nation_id = nations.id
            GROUP BY nations.NOC         
            ORDER BY COUNT (contests_medals.medal) DESC
            '''
    if limit > 0:
        query += ''' LIMIT ''' + str(limit) + ''';'''
    else:
        query += ''';'''
    try:
        cursor.execute(query, ())
    except Exception as e:
        print(e)
        exit()

    print('===== NOCs in decreasing order by gold medal count =====')
    for row in cursor:
        print(row[0] + " | " + str(row[1]))
    print()

def list_name(name, limit, cursor):
    '''
    Prints medals won by a given athlete
    '''
    query = '''SELECT DISTINCT athletes.athlete_name, contests_medals.medal, games.game_year, games.season, games.city, contests.contest
            FROM athletes, contests_medals, games, athletes_games, contests
            WHERE athletes.id = athletes_games.athlete_id
            AND games.id = athletes_games.game_id
            AND athletes_games.id = contests_medals.athletes_games_id
            AND contests_medals.medal IS NOT NULL
            AND athletes.athlete_name = %s
            AND contests.id = contests_medals.contest_id 
            ORDER BY games.game_year
            '''
    if limit > 0:
        query += ''' LIMIT ''' + str(limit) + ''';'''
    else:
        query += ''';'''
    try:
        cursor.execute(query, (name,))
    except Exception as e:
        print(e)
        exit()

    print('===== Medals won by {0} ====='.format(name))
    for row in cursor:
        print(row[1] + " | " + row[4], row[2], row[3] + " | " + row[5])
    print()

def main():
    arguments = get_parsed_arguments()
    if not (arguments.athletes or arguments.medals or arguments.name) :
        print("Please enter a flag to search the olympics database.", file=sys.stderr)
        print("For additional information, enter python3 olympics.py --help", file=sys.stderr)
        exit()
    limit = -1
    connection = get_database_connection()
    cursor = connection.cursor()
    if arguments:
        if arguments.limit:
            limit = arguments.limit[0]
        if arguments.athletes:
            list_athletes(arguments.athletes[0], limit, cursor)
        if arguments.medals:
            list_medals(limit, cursor)
        if arguments.name:
            list_name(arguments.name[0], limit, cursor)
    connection.close()

if __name__ == '__main__':
    main()
