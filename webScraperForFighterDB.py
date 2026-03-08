import csv
import re
from bs4 import BeautifulSoup
import requests
#Open file for writing in write mode
file = open("ListOfFighters.csv", "w")
writer = csv.writer(file)
writer.writerow(["height","name","weight_class","country","age", "losses", "nick_name","stance","total_fights", "wins"])

#There are 26 pages worth of information regarding fighters
for page in range(1, 27):
    #Keep track of what page we are on, was mainly for debugging
    print("Page: "+ str(page))
    #There are list of fighters of each page from 1 to 26
    url = ("https://mma-compass.com/roster/?page=" + str(page))
    response = requests.get(url)
    #Used beautiful soup to webscrape all the html from the page
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find("main", attrs={"flex-grow"})
    #find <a> tag which contained fighter ID
    links = soup.find("a")

    #Used css selectors to choose which elements I wanted to scrape specifically
    links = soup.select('a.text-lg.font-semibold')
    for link in links:
        #href contained the unique fighter web page that I then added onto the main page url
        href = link.get('href')
        completeURL = "https://mma-compass.com" + str(href)
        url = completeURL
        url = requests.get(url)
        statusOfRequest = url.status_code
        #verifies each url, due to somefighter pages not existing but still present in webpage
        if statusOfRequest != 200:
            pass
        else:
            soup = BeautifulSoup(url.text, "html.parser")
            name = soup.find("h1", attrs={"class": "text-xl font-bold lg:text-2xl"})
            nickName = soup.find("h2", attrs={"class": "text-sm italic lg:text-base"})
            infoAboutFighter = soup.find("table", attrs={"class": "w-4/5 h-full mx-auto text-xs text-center lg:text-sm"})
            infoAboutFighter = infoAboutFighter.find_all('tr')
            fightStats = soup.find_all("div", attrs={"class": "text-lg lg:text-xl"})

            #Put all fighter information in a tuple, to parse correctly using indexing
            fighterInfo = []
            fighterName = name.text
            fighterNickName = nickName.text

            #Added information into the list
            for x in infoAboutFighter:
                fighterInfo.append(x.text)

            fighterAge = fighterInfo[0]
            fighterNationality = fighterInfo[1]
            fighterWeight = fighterInfo[2]
            fighterHeight = fighterInfo[3]
            fighterReach = fighterInfo[4]
            fighterStance = fighterInfo[5]

            # remove unnecessary info using basic slicing
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

            print(fighterName)
            print(fighterNickName.strip())
            print(fighterAge.strip())
            #Unicode for flag was also getting parsed which resulted in some formatting errors when I wanted to write to file
            fighterNationality = re.sub(r'[\U000E0000-\U000E007F]', '', fighterNationality)
            print(fighterNationality.strip())
            print(fighterReach.strip())
            print(fighterWeight.strip())
            print(fighterHeight.strip())
            print(fighterStance.strip())
            print(fighterWins.strip())
            print(numberOfFights.strip())
            print(fighterLosses.strip())

            #Write all fields to the csv file
            writer.writerow([fighterHeight.strip(), fighterName, fighterWeight.strip(),
                              fighterNationality.strip(), fighterAge.strip(),
                              fighterLosses.strip(), fighterNickName.strip(),
                              fighterStance.strip(), numberOfFights.strip(), fighterWins.strip()])
file.close()











