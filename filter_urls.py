from requesting_urls import get_html
import re

def find_urls(html, base_url=None):
    """
    Method for finding links to other web pages in a web page
    param1: the html of the page you want to find urls in
    param2: the base url you want to add to the relative urls found, default None
    return: a list of all urls found
    """

    #Regex to find URLs
    # skips all between the a tag (to know it is an anchor) and the href, 
    #   then groups all between the first " and the second " or a #. This return the url (without the fragment identifiers)
    reg = r"<a.*?href=\"([^#].*?)(\"|#)" 
    result = re.findall(reg, html)
    result = [x[0] for x in result]
    if base_url:
        newResult = []
        https = False
        # if the fifth character in an url is "s" then it is a https url
        if base_url[4] == "s":
            https = True

        for url in result:
            # if the url starts with a single or double / it is a relative url
            if url[0] == "/":
                if url[1] == "/":
                    #if it starts with a double // we will just add http/https to the link
                    newResult.append('https:' + url)
                else:
                    #else we will add the base url to the relative url
                    newResult.append(base_url + url)
            else:
                newResult.append(url)
        return newResult
    else:
        return result 

    


def find_articles(url):
    """
    Method for finding all wikipedia links in web pages
    param: the url of the web page you want to search in
    return: a list of all the wikipedia links found
    """
    response = get_html(url).text
    base_url="https://en.wikipedia.org"
    r = find_urls(response, base_url)

    wiki_urls = []
    for url in r:
        #Regex to find wikipedia links.
        #The regex matches with all urls that have a body containing wikipedia.org/wiki, and dont contain any ":" (articles with namespaces)    
        match = re.match(r"^.*?wikipedia.org/wiki[^\:]*$", url)
        if match:
            wiki_urls.append(match.group(0))
    return wiki_urls

if __name__ == "__main__":
    urls1 = find_articles('https://en.wikipedia.org/wiki/Nobel_Prize')
    urls2 = find_articles('https://en.wikipedia.org/wiki/Bundesliga')
    urls3 = find_articles('https://en.wikipedia.org/wiki/2019%E2%80%9320_FIS_Alpine_Ski_World_Cup')

    file1 = open('filter_urls/Nobel_Prize.txt', 'w')
    for url in urls1:
        file1.write(url + "\n") 

    file2 = open('filter_urls/Bundesliga.txt', 'w')
    for url in urls2:
        file2.write(url + "\n")  

    file3 = open('filter_urls/Ski_World_cup.txt', 'w')
    for url in urls3:
        file3.write(url + "\n")   
        