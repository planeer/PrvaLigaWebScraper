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

    teams_dict = {
        "Olimpija": "Olimpija Ljubljana",
        "KD Olimpija": "Olimpija Ljubljana",
        "Vega Olimpija": "Olimpija Ljubljana",
        "SCT Olimpija": "Olimpija Ljubljana",
        "Rudar": "Rudar Velenje",
        "Rudar V.": "Rudar Velenje",
        "BS Tehnik Domžale": "Domžale",
        "HIT Gorica": "Gorica",
        "Hit Gorica": "Gorica",
        "ND Gorica": "Gorica",
        "SAOP Gorica": "Gorica",
        "Maribor Pivovarna Laško": "Maribor",
        "Maribor Teatanic": "Maribor",
        "Maribor Branik": "Maribor",
        "Triglav": "Triglav Kranj",
        "Živila Triglav": "Triglav Kranj",
        "Triglav Gorenjska": "Triglav Kranj",
        "CM Celje": "Celje",
        "MIK CM Celje": "Celje",
        "CMC Publikum": "Celje",
        "Publikum": "Celje",
        "Protonavto Publikum": "Celje",
        "Biostart Publikum": "Celje",
        "Luka Koper": "Koper",
        "Anet Koper": "Koper",
        "FC Koper": "Koper",
        "Sport Line Koper": "Koper",
        "Istrabenz Koper": "Koper",
        "Krka Novoterm": "Krka",
        "Studio D Novo mesto": "Krka",
        "Nafta Lendava": "Nafta",
        "Labod Drava Ptuj": "Labod Drava",
        "Drava Ptuj": "Labod Drava",
        "Drava": "Labod Drava",
        "Kumho Drava": "Labod Drava",
        "AM Cosmos Ljubljana": "Ljubljana",
        "Eurospekter Ljubljana": "Ljubljana",
        "Železničar Oscar": "Ljubljana",
        "Elektroelement Zagorje": "Zagorje",
        "Era Šmartno": "Šmartno",
        "Dravograd": "Koroška Dravograd",
        "Korotan": "Relax Korotan",
        "Mag Korotan": "Relax Korotan",
        "Korotan Suvel": "Relax Korotan",
        "AS Beltinci": "Potrošnik Beltinci",
        "Beltinci": "Potrošnik Beltinci",
        "Vevče": "Set Vevče",
        "Belvedur Izola": "Izola",
        "Istragas Jadran": "Jadran Dekani",
        "Jadran Lama": "Jadran Dekani",
        "Kompas Holidays Svoboda": "Optimizem Svoboda",
        "Liqui Moly Svoboda": "Optimizem Svoboda",
    }

    URL = "https://www.prvaliga.si/tekmovanja/default.asp?id_menu=101&id_sezone="
    from_year = 1992
    to_year = 2019

    for i in range(from_year, to_year + 1):
        print("Parsing year: " + str(i))
        r = requests.get(URL + str(i))
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, "html.parser")

        # Select all played games
        league_table = soup.find("table", {"class": "tekme"}).find('tbody').select("tr.odigrano.klub_all.hidden-xs")
        
        data = []
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

            home_team_name = teams_dict.get(home_team)
            if home_team_name != None:
                home_team = home_team_name

            away_team_name = teams_dict.get(away_team)
            if away_team_name != None:
                away_team = away_team_name

            data.append([date, home_team, away_team, home_team_goals, away_team_goals, ftr])

        # Save current year
        df = pd.DataFrame(data, columns = ["Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR"])
        df.to_csv("output/games/slo_prva_liga_" + str((i - 1)) + "-" + str(i) + ".csv", index=None)


if __name__ == "__main__":
    main()
