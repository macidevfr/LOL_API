from riotwatcher import LolWatcher, ApiError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time

currentTimeDate = datetime.now() - relativedelta(years=1)
currentTimeDate = int(currentTimeDate.timestamp())
lol_watcher = LolWatcher('RGAPI-e876743f-de07-48fe-9997-668caa1c2dad')

my_region = 'euw1'
pseudo = 'Vachette Hybride'

me = lol_watcher.summoner.by_name(my_region, pseudo)


def get_last_games(end_time):
    games = lol_watcher.match.matchlist_by_puuid(my_region, me['puuid'], count=100, end_time=end_time)
    return games


def get_time_played(games):
    time_played = 0
    for game in games:

        game = lol_watcher.match.by_id(my_region, game)

        if (int(game['info']['gameCreation'] / 1000) > currentTimeDate) and 600 < int(
                game['info']['gameDuration']) < 3600:
            time_played += game['info']['gameDuration']
            # print time_played converted into minutes and seconds
            print(timedelta(seconds=time_played), timedelta(seconds=game['info']['gameDuration']),
                  datetime.fromtimestamp(int(game['info']['gameCreation']) / 1000))

        else:
            continue
        time.sleep(1.4)
    return time_played


def get_total_time_played():
    time_played = 0
    end_time = int(datetime.now().timestamp())
    while True:
        games = get_last_games(end_time)
        print(games)
        if len(games) > 0:
            last_game = lol_watcher.match.by_id(my_region, games[-1])
            end_time = last_game['info']['gameCreation']
            end_time = int(end_time / 1000)

            time_played += get_time_played(games)

        if end_time < currentTimeDate or len(games) == 0:
            break

    return str(timedelta(seconds=time_played))


print(get_total_time_played())
