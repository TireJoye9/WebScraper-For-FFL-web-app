import csv
import re

from bs4 import BeautifulSoup
import requests
from urllib3.filepost import writer

pageCounter = 1

file = open("ListOfFighters.csv", "w")
writer = csv.writer(file)

writer.writerow(["height","name","weight_class","country","age", "losses", "nick_name","stance","total_fights", "wins"])


for page in range(1, 27):
    url = ("https://mma-compass.com/roster/?page=" + str(page))
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find("main", attrs={"flex-grow"})
    links = soup.find("a")

    links = soup.select('a.text-lg.font-semibold')
    for link in links:
        href = link.get('href')
        completeURL = "https://mma-compass.com" + str(href)
        url = completeURL
        url = requests.get(url)

        soup = BeautifulSoup(url.text, "html.parser")
        name = soup.find("h1", attrs={"class": "text-xl font-bold lg:text-2xl"})
        nickName = soup.find("h2", attrs={"class": "text-sm italic lg:text-base"})
        infoAboutFighter = soup.find("table", attrs={"class": "w-4/5 h-full mx-auto text-xs text-center lg:text-sm"})
        infoAboutFighter = infoAboutFighter.find_all('tr')
        fightStats = soup.find_all("div", attrs={"class": "text-lg lg:text-xl"})

        fighterInfo = []
        fighterName = name.text
        fighterNickName = nickName.text

        for x in infoAboutFighter:
            fighterInfo.append(x.text)

        fighterAge = fighterInfo[0]
        fighterNationality = fighterInfo[1]
        fighterWeight = fighterInfo[2]
        fighterHeight = fighterInfo[3]
        fighterReach = fighterInfo[4]
        fighterStance = fighterInfo[5]

        # remove unecessary info
        fighterAge = fighterAge[3:]
        fighterNationality = fighterNationality[14:]
        fighterWeight = fighterWeight[12:]
        fighterHeight = fighterHeight[6:10]
        fighterReach = fighterReach[5:9]
        fighterStance = fighterStance[6:]

        numberOfFights = 0
        fighterWins = 0
        fighterLosses = 0

        for detail in fightStats:
            # All i need is first 3 pieces of data
            # Matches, wins,losses
            if numberOfFights == 0:
                numberOfFights = detail.text
            elif fighterWins == 0:
                fighterWins = detail.text
            elif fighterLosses == 0:
                fighterLosses = detail.text
                break

        writer.writerow([fighterHeight.strip(),fighterName,fighterWeight.strip(),
                         fighterNationality.strip(),fighterAge.strip(),
                         fighterLosses.strip(), fighterNickName.strip(),
                         fighterStance.strip(),numberOfFights.strip(), fighterWins.strip()])
file.close()











