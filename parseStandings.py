import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from team_dict import teams_dict


def main():
    data = []
    URL = "https://www.prvaliga.si/tekmovanja/default.asp?action=lestvica&id_menu=102&id_sezone="
    from_year = 1992
    to_year = 2019

    seasons = pd.read_csv("output/slo_standings.csv")

    for i in range(from_year, to_year + 1):
        print("Parsing year: " + str(i))
        r = requests.get(URL + str(i))
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, "html.parser")

        # Select all teams
        league_table = soup.find("table", {"class": "Tabela1"}).find_all("tr")
        
        for j, row in enumerate(league_table):
            if j != 0:
                # Get team position
                position = row.findNext("td").get_text().strip()[:-1]

                # Get team name
                team_td = row.find("td", {"class": "title"})
                if team_td != None:
                    team = team_td.get_text().strip()
                    if team[0] == "*":
                        team = team[1:].strip()

                    team_name = teams_dict.get(team)
                    if team_name != None:
                        team = team_name

                    if not seasons.loc[seasons["Team"] == team].empty:
                        seasons.loc[seasons["Team"] == team, ((i-1) % 100)] = int(position)
                    else:
                        raise Exception("Not found team: " + team)

        # Save seasons standings
        seasons.to_csv("output/slo_standings.csv", index=None)


if __name__ == "__main__":
    main()
