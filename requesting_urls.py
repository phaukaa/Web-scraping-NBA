import requests as req

def get_html(url, params=None, output=None):
    """
    Method for getting the html page from an url
    param1: the url you want to fetch
    param2: the arguments you want to pass when getting the url, default None
    param3: the output file you want to write the html page to, default none
    return: if no output file is given, the html page will be returned
    """
    if params:
        response = req.get(url, params)
    else:
        response = req.get(url)
    if output:
        file = open("requesting_urls/"+output, "w")
        file.write(response.text)
        file.close()
    else:
        return response

if __name__=="__main__":
    get_html("https://en.wikipedia.org/wiki/Studio_Ghibli", None, "Studio_Ghibli.txt")
    get_html("https://en.wikipedia.org/wiki/Star_Wars", None, "Star_Wars.txt")
    get_html("https://en.wikipedia.org/wiki/Dungeons_%26_Dragons", None, "D&D.txt")
    get_html("https://en.wikipedia.org/w/index.php",
            {"title":"Main_Page", "action":"info"}, "Main_Page.txt")
    get_html("https://en.wikipedia.org/w/index.php",
            {"title": "Hurricane_Gonzalo", "oldid": "983056166"}, "Hurricane_Gonzalo.txt")
