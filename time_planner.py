from bs4 import BeautifulSoup
import requests as req
import re
from mdutils.mdutils import MdUtils

def extract_events(url, slipID=None):
    """
    Method to extract events from the alpine world cup and convert this into a markdown betting slip
    param1: the url of the worcls cup wikipedia page
    param2: the id of the slip(what it will be named in the file dir), default: None (will be called betting_slip_empty)
    """
    html = req.get(url)
    assert html.status_code == 200
    soup = BeautifulSoup(html.content, 'lxml')
    #Gets all the race tables from the html
    tables = soup.find_all('table', {"class":"wikitable plainrowheaders"})

    #Stores the venue outside the loop, as not all lines have a venue.
    #If a line dont have a venue it means it uses the previous (saved) venue
    venue = "N/A"
    resultMen = []
    resultWomen = []
    doneMen = False

    #Extracts from the first two tables (mens and ladies races)
    for table in tables[:-1]:
        rows = table.find_all("tr")
        for row in rows[1:]:
            cells = row.find_all(["td", "th"])
            text = [cell.get_text(strip=True) for cell in cells]
            
            """Regex: to be matched in an array
            Date: in the format DMY
            Venue: Starts with a capital letter, continues with all other than capital letters until end of line
            Dicipline: Starts with two capital letters, then continues with lowercase letters or numbers until end of line
            """
            regexDate = r"(?:.*?)(\d*\d \S* \d*)"
            regexVenue = r"^[A-Z][^A-Z]+?.*$"
            regexDicipline = r"^[A-Z][A-Z][^A-Z]*$"


            date = None
            dicipline = None
            
            #Matches the date, venue and dicipline from the extracted text
            for e in text:
                if re.match(regexDate, e):
                    date = re.match(regexDate, e).group(1)
                if re.match(regexVenue, e):
                    venue = e
                if re.match(regexDicipline, e):
                    dicipline = e
                    break

            #Adds men an women in seperate arrays to be displayes later
            if not doneMen and date:
                resultMen.append(date)
                resultMen.append(venue)
                resultMen.append(dicipline)
                resultMen.append("")
            elif doneMen and date:
                resultWomen.append(date)
                resultWomen.append(venue)
                resultWomen.append(dicipline)
                resultWomen.append("")
        doneMen = True

    #Puts all the data nicely formated into a markdown file
    if slipID:
        md = MdUtils(file_name=f'datetime_filter/betting_slip_empty_{slipID}', title='BETTING SLIP')
    else: md = MdUtils(file_name='datetime_filter/betting_slip_empty', title='BETTING SLIP')
    md.new_header(level=1, title='Name:')
    headings = ["Date", "Venue", "Dicipline", "Who Wins"]
    headings.reverse()
    for e in headings:
        resultMen.insert(0, e)
        resultWomen.insert(0, e)
    md.new_paragraph("MEN:\n")
    table = md.new_table(columns=4, rows=int(len(resultMen)/4), text=resultMen, text_align='center')
    md.new_paragraph("WOMEN:\n")
    table = md.new_table(columns=4, rows=int(len(resultMen)/4), text=resultMen, text_align='center')
    md.create_md_file()
    


if __name__ == "__main__":
    extract_events("https://en.wikipedia.org/wiki/2019%E2%80%9320_FIS_Alpine_Ski_World_Cup", "WC1920")
    extract_events("https://en.wikipedia.org/wiki/2020%E2%80%9321_FIS_Alpine_Ski_World_Cup", "WC2021")