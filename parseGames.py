import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime  


def getDate(date_string):
    months = {
        "januar": 1,
        "februar": 2,
        "marec": 3,
        "april": 4,
        "maj": 5,
        "junij": 6,
        "julij": 7,
        "avgust": 8,
        "september": 9,
        "oktober": 10,
        "november": 11,
        "december": 12
    }

    for key, value in months.items():
        result = re.search(key, date_string)
        if result != None:
            date_string = re.sub(key, str(value), date_string)
            date_obj = datetime.strptime(date_string, "%d.%m %Y")

            return date_obj.strftime("%d/%m/%y")

def main():
    data = []
    URL = "https://www.prvaliga.si/tekmovanja/default.asp?id_menu=101&id_sezone="
    from_year = 1992
    to_year = 2019

    for i in range(from_year, to_year + 1):
        print("Parsing year: " + str(i))
        r = requests.get(URL + str(i))
        soup = BeautifulSoup(r.text, "html.parser")

        # Select all played games
        league_table = soup.find("table", {"class": "tekme"}).find('tbody').select("tr.odigrano.klub_all.hidden-xs")
        
        for j, row in enumerate(league_table):
            # Get data for each game
            home_team = row.find("td", {"class": "text-right"}).get_text().strip()

            away_team = row.find("td", {"class": "text-left"}).get_text().strip()

            score = row.find("td", {"class": "rezultat"}).find("a").find("span").get_text().strip().split(":")
            home_team_goals = int(score[0].strip())
            away_team_goals = int(score[1].strip())

            ftr = "D" if home_team_goals == away_team_goals else ("H" if home_team_goals > away_team_goals else "A")

            date = row.find("td", {"class": "text-left"}).findNext("td").get_text().strip()
            result = re.search("([0-9])(.*)([0-9])", date)
            date = getDate(result.group().strip())

            data.append([date, home_team, away_team, home_team_goals, away_team_goals, ftr])

        # Save current year
        df = pd.DataFrame(data, columns = ["Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR"])
        df.to_csv("output/games/slo_prva_liga_" + str((i - 1)) + "-" + str(i) + ".csv", index=None)


if __name__ == "__main__":
    main()
