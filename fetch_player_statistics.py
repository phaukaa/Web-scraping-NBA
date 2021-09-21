from bs4 import BeautifulSoup
from requesting_urls import get_html
import re
import matplotlib.pyplot as plt
import numpy as np

def fetch(url):
    """
    Method to extract all team names and urls from the nba playoff wikipedia page
    param: url to the wikipedia page
    """
    html = get_html(url)
    assert html.status_code == 200
    soup = BeautifulSoup(html.content, 'lxml')
    table = soup.find('table', {"cellpadding":"0"})
    rows = table.find_all("tr")
    #Regex: all strings that starts with "/wiki/"
    urlRegex = r"(\/wiki\/.*?)\""
    #Regex: captures all between a digit and the string "season" (which is team names)
    nameRegex = r"\d (.*) season"
    urls = []
    names = []
    baseURL = "https://en.wikipedia.org"
    #Starts at the first relevant row
    for row in rows[2:]:
        cells = row.find_all('a')
        name = re.findall(nameRegex, str(cells))
        if name:
            names.append(name[0])
        url = re.findall(urlRegex, str(row))
        if url:
            teamURL = baseURL + url[0]
            urls.append(teamURL)

    semifinalsURL = []
    semifinalsName = []
    for url in urls:
        if urls.count(url) > 1 and url not in semifinalsURL:
            semifinalsURL.append(url)
    for name in names:
        if names.count(name) > 1 and name not in semifinalsName:
            semifinalsName.append(name)
   
    teamStats = {}
    count = 0
    for url in semifinalsURL:
        stats = extract_url(url)
        if stats:
            teamStats[semifinalsName[count]] = stats
        count+=1
        
    
    plotStats(teamStats)

def plotStats(teamStats):
    """
    Method for plotting the stats of the best players on each team into a nice graph
    param: a dictionary of the teams and their best players in each category
    """
    
    sheets = ["Points per game", "Blocks per game", "Rebounds per game"]

    #Creates a new chart for each category
    for i in range(len(next(iter(teamStats.values())))):
        fig, ax = plt.subplots()
        #Plots the players in the x direction, and their points (or blocks, rebounds) in the y direction
        for team, players in teamStats.items():
            playerNames = players[i].keys()
            playerStats = players[i].values()
            ax.bar(playerNames, playerStats, label=team)

        #Shows the teams in the upper right corner, and the player names vertical for convenience
        ax.legend()
        plt.xticks(rotation='vertical')
        plt.xlabel('Players', fontweight ='bold') 
        plt.ylabel(sheets[i], fontweight ='bold')
        plt.tight_layout()
        plt.show()

def extract_url(url):
    """
    Method to extract the players and their stats from an NBA teams wikipedia page
    param: the URL of the NBA teams wikipedia
    return: an array containing the teams top three players in each category and their stats
    """
    html = get_html(url)
    assert html.status_code == 200
    soup = BeautifulSoup(html.content, 'lxml')
    table = soup.find('table', {"class":"toccolours"})
    rows = table.find_all("tr")

    #Regex: same as earlier
    urlRegex = r"(\/wiki\/.*?)\""
    #Regex: matches all strings between 'title="' and '"' or '(' where there are two (or more words) that dont start with a lowercase letter (player names, including non-[a-z] chars)
    #I also exclude anything after the name (in som cases "(basketball)")
    nameRegex = r"title=\"([^a-z].*? [^a-z\(\)].*?)(?:\"|\()"

    playerNames = []
    playerURLS = []
    baseURL = "https://en.wikipedia.org"

    for row in rows[4:]:
        url = re.findall(urlRegex, str(row))
        #Chooses the player url from the list
        playerURL = url[1]
        playerURLS.append(baseURL + playerURL)
        name = re.findall(nameRegex, str(row))
        if name:
            #Adds the player name from the result (sometimes the uni of the player matches the regex and comes after the name ine the array)
            playerNames.append(name[0])
    
    playerStats = {}
    count = 0
    for url in playerURLS:
        stats = extract_player(url)
        if stats:
            playerStats[playerNames[count]] = stats
        count+=1
    
    topPlayers = sortPlayers(playerStats)

    return topPlayers

def sortPlayers(stats):
    """
    Method to sort the players of the team into three categories:
    most points per game, blocks per game and rebounds per game
    param: dictionary containg the players and their stats
    return: list with three dictionaries, one for each category
    """
    result = []
    #Sort dictionaries by ppg, bpg and rpg
    ppg = list(reversed(sorted(stats.items(), key=lambda item: item[1][0])))
    bpg = list(reversed(sorted(stats.items(), key=lambda item: item[1][1])))
    rpg = list(reversed(sorted(stats.items(), key=lambda item: item[1][2])))

    #Sort the top players of each category into three dictionaries
    points = {}
    for i in ppg[:3]:
        points[i[0]] = i[1][0]
    result.append(points)
    blocks = {}
    for i in bpg[:3]:
        blocks[i[0]] = i[1][1]
    result.append(blocks)
    rebounds = {}
    for i in rpg[:3]:
        rebounds[i[0]] = i[1][2]
    result.append(rebounds)

    #Returns a list cointaing a dictionary for each category, with the top three players in each category
    return result
        

def extract_player(url):
    """
    Method to find the points per game stats of the player in the 2019-20 season
    param: the url of the wikipedia page of the player
    return: a list of the players stats
    """
    html = get_html(url)
    assert html.status_code == 200
    soup = BeautifulSoup(html.content, 'lxml')
    table = soup.find('table', {"class":"wikitable sortable"})
    if not table: return None
    rows = table.find_all("tr")

    #Regex: Matches with the title 2019-20, which means we have found the 2019-20 season row 
    correctSeason = r"title=\"(2019–20)"

    pointsPerGame = 0
    blocksPerGame = 0
    reboundsPerGame = 0

    for row in rows[1:-1]:
        #Tries to match the correctSeason regex to the row
        match = re.findall(correctSeason, str(row))
        if match:
            #Matches all datacells in the row
            tds = row.find_all("td")
            #We want the data of the last datacell
            pointsPerGame = float(tds[-1].get_text().strip("*\n"))
            if tds[-2].get_text().strip("*\n") != "-":
                blocksPerGame = float(tds[-2].get_text().strip("*\n"))
            reboundsPerGame = float(tds[-5].get_text().strip("*\n"))

    return [pointsPerGame, blocksPerGame, reboundsPerGame]

if __name__=="__main__":
    fetch("https://en.wikipedia.org/wiki/2020_NBA_playoffs")
