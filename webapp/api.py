# Claire Williams and Luisa Escosteguy

import sys
import flask
import json
import psycopg2
from flask import request

from config import password
from config import database
from config import user

api = flask.Blueprint('api', __name__)

@api.route('/games/')
def get_games():
    ''' Returns a JSON list of games dictionaries each of which represents the games with the specified criteria, if any.'''
    platform = request.args.get('platform')
    genre = request.args.get('genre')
    publisher = request.args.get('publisher')
    order_by = request.args.get('order_by')
    query = '''SELECT DISTINCT games.name, sales.global_sales, publishers.publisher, platforms.platform, genres.genre, games.year, sales.na, sales.eu, sales.jp, games_platforms.user_score, games_platforms.critic_score 
                FROM sales, platforms, games_platforms, games, publishers, genres
                WHERE games.publisher_id = publishers.id
                AND games.genre_id = genres.id
                AND games_platforms.games_id = games.id
                AND games_platforms.platforms_id = platforms.id
                AND games_platforms.sales_id = sales.id '''
    if platform:
        query += 'AND platforms.platform = \'%s\' ' % platform 
    if genre:
        query += 'AND genres.genre = \'%s\' ' % genre 
    if publisher:
        query += 'AND publishers.publisher = \'%s\' ' % publisher
    if order_by == 'critic_score' or order_by == 'user_score':
        query += 'ORDER BY games_platforms.%s DESC NULLS LAST LIMIT 400;' % order_by
    else:
        query += "ORDER BY sales.global_sales DESC LIMIT 500;"

    try:
        cursor = connect_database()
        cursor.execute(query, (genre,))
    except Exception as e:
        print(e)
        exit()

    games_dictionary = []
    for row in cursor:
        if row[9] is not None:
            user_score = float(row[9])
        else:
            user_score = None 
        games_dictionary.append({ 'name':row[0], 'sales':float(row[1]),
                'publisher':row[2], 'platform':row[3], 
                'genre':row[4], 'year':row[5], 'na':float(row[6]), 
                'eu':float(row[7]), 'jp':float(row[8]), 'user_score':user_score, 
                'critic_score':row[10] 
        })

    return json.dumps(games_dictionary)

@api.route('/platforms/') 
def get_platforms():
    ''' Returns an alphabetized JSON list of strings, each of which is a platform. '''
    query = '''SELECT DISTINCT platform
                FROM platforms
                ORDER BY platform'''
    try:
        cursor = connect_database()
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    platforms_list = []
    for platform in cursor:
        platforms_list.append(platform[0])

    return json.dumps(platforms_list)

@api.route('/genres/') 
def get_genres():
    ''' Returns an alphabetized JSON list of strings, each of which is a genre. '''
    query = '''SELECT DISTINCT genre
                FROM genres
                WHERE genre IS NOT NULL
                ORDER BY genre;'''
    try:
        cursor = connect_database()
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    genres_list = []
    for genre in cursor:
        genres_list.append(genre[0])

    return json.dumps(genres_list)

@api.route('/publishers/') 
def get_publishers():
    ''' Returns an alphabetized JSON list of strings, each of which is a publisher. '''
    query = '''SELECT DISTINCT publisher
                FROM publishers
                WHERE publisher IS NOT NULL
                ORDER BY publisher;'''
    try:
        cursor = connect_database()
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    publishers_list = []
    for publisher in cursor:
        publishers_list.append(publisher[0])

    return json.dumps(publishers_list)

@api.route('/categories/') 
def get_categories():
    ''' Returns a categories JSON dictionary, representing the top 5 platforms, genres, and publishers '''
    categories = {
        'platforms': ['Wii', 'PS2', 'GB', 'DS', 'X360'],
        'genres': ['Action', 'Sports', 'Shooter', 'Role-Playing', 'Platform'],
        'publishers': ['Electronic Arts', 'Activision', 'Ubisoft', 'Nintendo', 'Namco Bandai Games']
    }
    return json.dumps(categories)

@api.route('/help/') 
def get_help():
    ''' Returns the api documentation '''
    content = ''
    with open('doc/api-design.txt', 'r') as f:
        line = f.readline()
        while line:
            content += line + '<br />'
            line = f.readline()
    return content

def connect_database():
    ''' Connects to the webapp database '''
    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
        cursor = connection.cursor()
        return cursor
    except Exception as e:
        print(e)
        exit()