#Claire Williams & Matthew Rasmussen
#1/26/2021
#Moves info from one CSV file to other CSV files

#dictionary full of info
import csv

def make_athletes_table():
    '''SOMETHING '''
    athlete_dict = {}
    
    with open('athlete_events.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader)
        for row in csv_reader:
            name = row[1]
            sex = row[2]
            height = row[4]
            weight = row[5]
            if name not in athlete_dict:
                athlete_dict[name] = [len(athlete_dict) + 1, sex, height, weight]
                
    with open('athletes.csv', 'w', newline='') as new_csv_file:
        writer = csv.writer(new_csv_file, delimiter=',')
        for key in athlete_dict:
            writer.writerow([athlete_dict[key][0], key, athlete_dict[key][1], athlete_dict[key][2], athlete_dict[key][3]])
    
    return athlete_dict
    

def make_nations_table():
    nations_dict = {}
    with open ('noc_regions.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader)
        for row in csv_reader:
            noc = row[0]
            region = row[1]
            nations_dict[noc] = [len(nations_dict) + 1, region]
    
    with open ('athlete_events.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader)
        for row in csv_reader:
            noc = row[7]
            team = row[6]
            if noc not in nations_dict:
                nations_dict[noc] = [len(nations_dict) + 1, team]
    
    with open('nations.csv', 'w', newline='') as new_csv_file:
        writer = csv.writer(new_csv_file, delimiter=',')
        for nation in nations_dict:
            writer.writerow([nations_dict[nation][0], nation, nations_dict[nation][1]])
    
    return nations_dict
            
def make_games_table():
    games_dict = {}
    with open ('athlete_events.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader)
        for row in csv_reader:
            game = row[8]
            year = row[9]
            season = row[10]
            city = row[11]
            if game not in games_dict:
                games_dict[game] = [len(games_dict) + 1, year, season, city]
    
    with open('games.csv', 'w', newline='') as new_csv_file:
        writer = csv.writer(new_csv_file, delimiter=',')
        for key in games_dict:
            writer.writerow([games_dict[key][0], games_dict[key][1], games_dict[key][2], games_dict[key][3]])
    
    return games_dict
    
def make_contests_table():
    contest_dict = {}
    with open ('athlete_events.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader)
        for row in csv_reader:
            contest = row[13]
            sport = row[12]
            if contest not in contest_dict:
                contest_dict[contest] = [len(contest_dict) + 1, sport]
    
    with open('contests.csv', 'w', newline='') as new_csv_file:
        writer = csv.writer(new_csv_file, delimiter=',')
        for key in contest_dict:
            writer.writerow([contest_dict[key][0], key, contest_dict[key][1]])
    
    return contest_dict

def make_athletes_games(athelete_dict, nations_dict, games_dict):
    athletes_games_dict = {}
    with open ('athlete_events.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader)
        for row in csv_reader:
            athlete = row[1]
            game_name = row[8]
            noc = row[7]
            if (athlete, game_name) not in athletes_games_dict:
                athletes_games_dict[(athlete, game_name)] = [len(athletes_games_dict) + 1, athelete_dict[athlete][0], nations_dict[noc][0], games_dict[game_name][0]]
    
    with open('athletes_games.csv', 'w', newline='') as new_csv_file:
        writer = csv.writer(new_csv_file, delimiter=',')
        for key in athletes_games_dict:
            writer.writerow(athletes_games_dict[key])
    
    return athletes_games_dict

def make_contests_medals(athletes_games_dict, contests_dict):
    contests_medals_dict = {}
    with open ('athlete_events.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader)
        for row in csv_reader:
            athlete = row[1]
            game_name = row[8]
            contest = row[13]
            medal = row[14]
            contests_medals_dict[len(contests_medals_dict) + 1] = [athletes_games_dict[(athlete, game_name)][0], contests_dict[contest][0], medal]

    with open('contests_medals.csv', 'w', newline='') as new_csv_file:
        writer = csv.writer(new_csv_file, delimiter=',')
        for key in contests_medals_dict:
            writer.writerow([key, contests_medals_dict[key][0], contests_medals_dict[key][1], contests_medals_dict[key][2]])   

def main():
    athelete_dict = make_athletes_table()
    nations_dict = make_nations_table()
    games_dict = make_games_table()
    contests_dict = make_contests_table()
    athletes_games_dict = make_athletes_games(athelete_dict, nations_dict, games_dict)
    make_contests_medals(athletes_games_dict, contests_dict)

main()