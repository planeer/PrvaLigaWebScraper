import pandas as pd
from os import walk


def main():
    league_loc = "output/games/"

    # Open csv files
    raw_datas = []

    columns_req = ["HomeTeam", "AwayTeam"]

    (_, _, filenames) = next(walk(league_loc))
    filenames.sort()
    for _file in filenames:
        print(_file)
        raw_data = pd.read_csv(league_loc + _file)
        raw_data = raw_data[columns_req]
        raw_datas.append(raw_data)

    teams = ["Team"]

    # Get all teams
    for j, raw_data in enumerate(raw_datas):
        for i in range(len(raw_data)):
            ht = raw_data.iloc[i].HomeTeam
            at = raw_data.iloc[i].AwayTeam

            if ht not in teams:
                teams.append(ht)
            if at not in teams:
                teams.append(at)
        
    with open("output/slo_teams.csv", 'w') as f:
        for team in teams:
            f.write("%s\n" % team)

    with open("output/slo_standings.csv", 'w') as f:
        for team in teams:
            f.write("%s\n" % team)


if __name__ == "__main__":
    main()
