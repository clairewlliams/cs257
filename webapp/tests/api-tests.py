# Claire Williams and Luisa Escosteguy

import unittest
import games_api
import json

class APITester(unittest.TestCase):

    def setUp(self):
        self.games_api = games_api.GamesApi() #change depending on how we code it, will it be a class?

    def tearDown(self):
        pass

    def test_games_endpoint(self):
        url = '/games'
        self.assertIsNotNone(self.games_api.get_games(url))
        self.assertEqual(json.load(self.games_api.get_games(url))[0].keys(),
                ['name', 'global_sales', 'publisher', 'platform', 'genre', 'year'])
        
        url_wrong = '/games?random' 
        self.assertEqual(json.load(self.games_api.get_games(url_wrong))[0].keys(),
                ['name', 'global_sales', 'publisher', 'platform', 'genre', 'year'])

    def test_platforms_endpoint(self):
        url = '/platforms'
        self.assertIsNotNone(self.games_api.get_platform(url))

    def test_publishers_endpoint(self):
        url = '/publishers'
        self.assertIsNotNone(self.games_api.get_publisher(url))

    def test_genres_endpoint(self):
        url = '/genres'
        self.assertIsNotNone(self.games_api.get_genre(url))

    def test_categories_endpoint(self):
        url = '/categories'
        self.assertIsNotNone(self.games_api.get_categories(url))
        self.asertEqual(self.games_api.get_categories(url).keys(), ['platforms', 'genres', 'publishers'])
        
        url_wrong = '/categories?random' 
        self.asertEqual(self.games_api.get_categories(url).keys(), ['platforms', 'genres', 'publishers'])
    
    def test_publisher_endpoint(self):
        url = '/publisher?name=Nintendo'
        self.assertIsNotNone(self.games_api.get_publisher_by_name(url))
        self.assertEqual(json.load(self.games_api.get_publisher_by_name(url))[0].keys(),
                ['name', 'global_sales', 'publisher', 'platform', 'genre', 'year', 'na', 'eu', 'jp', 'user_score', 'critic_score'])
        
        url_empty = '/publisher?name='
        self.assertEqual(self.games_api.get_publisher_by_name(url_empty), '[]')
        
        url_publisher_not_in_set = '/publisher?name=ThisDoesNotMakeSense'
        self.assertEqual(self.games_api.get_publisher_by_name(url_publisher_not_in_set), '[]')

    def test_platform_endpoint(self):
        url = '/platform?name=Wii'
        self.assertIsNotNone(self.games_api.get_platform_by_name(url))
        self.assertEqual(json.load(self.games_api.get_platform_by_name(url))[0].keys(),
                ['name', 'global_sales', 'publisher', 'platform', 'genre', 'year', 'na', 'eu', 'jp', 'user_score', 'critic_score'])
        
        url_empty = '/platform?name='
        self.assertEqual(self.games_api.get_platform_by_name(url_empty), '[]')
        
        url_publisher_not_in_set = '/platform?name=ThisDoesNotMakeSense'
        self.assertEqual(self.games_api.get_platform_by_name(url_publisher_not_in_set), '[]')

    def test_genre_endpoint(self):
        url = '/genre?name=Action'
        self.assertIsNotNone(self.games_api.get_genre_by_name(url))
        self.assertEqual(json.load(self.games_api.get_genre_by_name(url))[0].keys(),
                ['name', 'global_sales', 'publisher', 'platform', 'genre', 'year', 'na', 'eu', 'jp', 'user_score', 'critic_score'])
        
        url_empty = '/genre?name='
        self.assertEqual(self.games_api.get_genre_by_name(url_empty), '[]')
        
        url_genre_not_in_set = '/genre?name=ThisDoesNotMakeSense'
        self.assertEqual(self.games_api.get_genre_by_name(url_genre_not_in_set), '[]')

if __name__ == '__main__':
    unittest.main()