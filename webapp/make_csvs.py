# Claire Williams and Luisa Escosteguy
import csv

def make_publishers():
    publisher_dict = {}
    
    with open('static/Video_Games_Sales_as_at_22_Dec_2016.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader)
        for row in csv_reader:
            publisher = row[4]
            if publisher not in publisher_dict:
                publisher_dict[publisher] = [len(publisher_dict) + 1]
                
    with open('static/publishers.csv', 'w', newline='') as new_csv_file:
        writer = csv.writer(new_csv_file, delimiter=',')
        for publisher in publisher_dict:
            writer.writerow([publisher_dict[publisher][0], publisher])
    
    return publisher_dict

def make_platforms():
    platform_dict = {}
    
    with open('static/Video_Games_Sales_as_at_22_Dec_2016.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader)
        for row in csv_reader:
            platform = row[1]
            if platform not in platform_dict:
                platform_dict[platform] = [len(platform_dict) + 1]
                
    with open('static/platforms.csv', 'w', newline='') as new_csv_file:
        writer = csv.writer(new_csv_file, delimiter=',')
        for platform in platform_dict:
            writer.writerow([platform_dict[platform][0], platform])
    
    return platform_dict

def make_genres():
    genre_dict = {}
    
    with open('static/Video_Games_Sales_as_at_22_Dec_2016.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader)
        for row in csv_reader:
            genre = row[3]
            if genre not in genre_dict:
                genre_dict[genre] = [len(genre_dict) + 1]
                
    with open('static/genres.csv', 'w', newline='') as new_csv_file:
        writer = csv.writer(new_csv_file, delimiter=',')
        for genre in genre_dict:
            writer.writerow([genre_dict[genre][0], genre])
    
    return genre_dict

def make_games(genre_dict, publisher_dict):
    games_dict = {}
    
    with open('static/Video_Games_Sales_as_at_22_Dec_2016.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader)
        for row in csv_reader:
            name = row[0]
            year = row[2]
            rating = row[15]
            genre = row[3]
            publisher = row[4]
            if name not in games_dict:
                games_dict[name] = [len(games_dict) + 1, year, rating, genre_dict[genre][0], publisher_dict[publisher][0]]
                
    with open('static/games.csv', 'w', newline='') as new_csv_file:
        writer = csv.writer(new_csv_file, delimiter=',')
        for name in games_dict:
            writer.writerow([games_dict[name][0], name, games_dict[name][1], games_dict[name][2], games_dict[name][3], games_dict[name][4]])
    
    return games_dict

def make_sales():
    sales_dict = {}
    
    with open('static/Video_Games_Sales_as_at_22_Dec_2016.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader)
        for row in csv_reader:
            game = row[0]
            platform = row [1]
            na = row[5]
            eu = row[6]
            jp = row[7]
            other = row[8]
            global_sales = row[9]
            if (game, platform) not in sales_dict:
                sales_dict[(game, platform)] = [len(sales_dict) + 1, na, eu, jp, other, global_sales]
                
    with open('static/sales.csv', 'w', newline='') as new_csv_file:
        writer = csv.writer(new_csv_file, delimiter=',')
        for key in sales_dict:
            writer.writerow(sales_dict[key])
    
    return sales_dict

def make_games_platforms(games_dict, platform_dict, sales_dict):
    games_platforms_dict = {}
    
    with open('static/Video_Games_Sales_as_at_22_Dec_2016.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader)
        for row in csv_reader:
            game = row[0]
            platform = row[1]
            user_score = row[12]
            if user_score == "tbd":
                user_score = ''
            critic_score = row[10]
            if (game, platform) not in games_platforms_dict:
                games_platforms_dict[(game, platform)] = [games_dict[game][0], platform_dict[platform][0], sales_dict[(game, platform)][0], user_score, critic_score]
                
    with open('static/games_platforms.csv', 'w', newline='') as new_csv_file:
        writer = csv.writer(new_csv_file, delimiter=',')
        for key in games_platforms_dict:
            writer.writerow(games_platforms_dict[key])

def main():
    publisher_dict = make_publishers()
    platform_dict = make_platforms()
    genre_dict = make_genres() 

    games_dict = make_games(genre_dict, publisher_dict)
    sales_dict = make_sales()
    
    make_games_platforms(games_dict, platform_dict, sales_dict)

if __name__ == '__main__':
    main()