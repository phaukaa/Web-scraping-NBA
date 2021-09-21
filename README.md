# Web scraping NBS statistics #
________________
This program Web-scrapes NBA statistics from Wikipedia, and finds a "Wiki-race"a way of moving from one article to another in the fastest way possible.
## Required dependencies and packages ##
To use the scripts you need to have Python 3.6 (or higher) installed, as well as these python packages:
- requests
- beautifulsoup4
- matplotlib
- numpy
- lxml

All these packages can be installed with the command
```bash
pip3 install {package}
```


## How to run ##
______
### requesting_urls.py ###
This script contains the method get_html() which returns the html page of a given URL. Closer explenation can be found as a docsting in the .py file.\
By running the script itself main will be run, and the script will create five .txt file in the requesting_urls directory, one for each of the URLs given in the task.

### filter_urls.py ###
This script contains the methods find_urls() and find_articles(). find_urls() takes a html page as parameter, and returns a list of all URLs found in the html. find_articles() takes a URL as parameter, and returns a list containg all the wikipedia URLs found in the given page. This method uses the find_articles() method and the get_html() method from the requesting_urls.py file.\
By running the script itselt main will be run, and the script will create three files in the filter_urls directory, containg all wikipedia URLs in the URLs given in the task.

### collect_dates.py ###
This script contains the method find_dates() which returns a list of all dates found in the body of the html given. The dates found can be in the formats: DMY, MDY, YMD and ISO. The returned dates will all be in the same format, YYYY/MM/(DD) where the date not need to have a day to be in the list.\
By running the script itself main will be run, and the script will get the thml from the five given URLs in the task, use the get_html() method to get the html body, and then put all the dates found in seperate .txt files in the filter_dates_regex directory.

### time_planner.py ###
This script contains the method extract_events() which extract events from the alpine world cup wikipedia page and convert this into a markdown betting slip. The parameter of the method is a URL to the wanted FIS alpine world cup wikipedia page. The script saves the slip as "betting:slip_empty.md" by default, and if wanted the methos can take a parameter to add to the name to seperate different betting slips for different years.\
By running the script itself main will be run, and the script will create two betting slips in the datetime_filter directory, one for the 19/20 world cup and one for the 20/21 world cup.

### fetch_player_statistics.py ###
This script contains the method fetch(), plotStats(), extract_url(), extract_player() and sort_players().\
The fetch() method takes the URL of an NBA playoff wikipedia page as parameter, and by using all the other methdos plots the stats nicely by using matplotlib. The stats plotted is the stats of the top three players in the categories: points per game, blocks per game and rebounds per game, by each team who made it to the semifinals of the NBA playoffs.\
The plotStats() method plots tha stats describes over. This method takes a python dictionary with the format:
```python
{
    'Milwaukee Bucks':
        [   
            {   'Giannis Antetokounmpo': 29.5,
                'Khris Middleton': 20.9,
                'Eric Bledsoe': 14.9
            },
            {   'Brook Lopez': 2.4,
                'Giannis Antetokounmpo': 1.0,
                'Robin Lopez': 0.7
            },
            {   'Giannis Antetokounmpo': 13.6,
                'Khris Middleton': 6.2,
                'Ersan İlyasova': 4.8
            }
        ],
    'Miami Heat':
        [
            {   'Jimmy Butler': 19.9,
                'Goran Dragić': 16.2,  
                'Bam Adebayo': 15.9
            },
            {   'Bam Adebayo': 1.3,
                'Andre Iguodala': 1.0,
                'Jimmy Butler': 0.6
            },
            {   'Bam Adebayo': 10.2,
                'Jimmy Butler': 6.7,
                'Jae Crowder': 5.4
            }
        ],
    ...
```
and shows this as a graph.\
The method extract_url() takes the URL of an NBA team as parameter, and returns an array containing three dictionaries. The dictionaries contain the top three players of that team in the mentioned categories, sorted.\
The method extract_player() takes the URL of an NBA players wikipedia page as parameter, and returns a list containing their stats for points per game, blocks per game and rebounds per game.\
The sort_players() method takes a dictionary conaining a teams players and their stats and returns a list conaining three dictionaries, each containg the teams top three players and their stats in each of the three categories.\
By running the script by itself main will be run, and the graphs plotted will be the stats of the eigth best teams in the 2020 NBA playoffs. The graphs are saves as images in the player_statistics directory.

### wiki_race_challenge.py ###
This script contain the method wikiRace(). This method takes two parameters, the start page and the end page. The start page is the URL of the wikipedia page you want to start on, and the end page is the wikipedia pge you want to find the path to. The method uses the find_articles() method to find wikipedia pages, and uses BFS to iterate through each pages wikipedia links. When using BFS the method looks through all wikipedia links found on a page, and if the end page URL is not found, the pages links will be put in tha back of the queue to be searched through later. This algorithm runs until it finds the end page URL and return a list containing the path to get there, or return None if the queue if empty and it still hasn't fount a path to the end page.\
When running the script by itself main will be run, and the script will look for a path between the first two articles and the last two articles given in the task, and put these into the shortest_way.txt document in the wiki_race_challenge directory.
