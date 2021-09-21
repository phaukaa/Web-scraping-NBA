from filter_urls import find_articles

def wikiRace(startPage, endPage):
    """
    Method to find the shortest path from one wikipedia page to another
    param1: the page you want to start on
    param2: tha page you want to fint the path to
    return: an array of all the links from the startpage to the endpage
    """
    path = {}
    path[startPage] = [startPage]
    queue = [startPage]
    #While there is links in the queue, it will search
    while (len(queue) != 0):
        #Takes the first element out of the queue and searches for links in this page
        page = queue.pop(0)
        #Searches for wikipedia links using the fin_articles() methos from the filter_urls file
        links = find_articles(page)

        #For all links in the page, it checks if the endpage is one of them, if not it puts all the new links in the back of the queue
        for link in links:
            if link == endPage:
                return path[page] + [link]
            
            if link not in path and link != page:
                path[link] = path[page] + [link]
                queue.append(link)
    #If the queue is empyt and no paths have been returned, there is no path from startpage to endpage and the methos returns None
    return None

if __name__=="__main__":
    
    startURL1 = "https://en.wikipedia.org/wiki/Parque_18_de_marzo_de_1938"
    endURL1 = "https://en.wikipedia.org/wiki/Bill_Mundell"
    path = wikiRace(startURL1, endURL1)
    file = open("wiki_race_challenge/shortest_way.txt", 'w')
    file.write(f"Shortest path from {startURL1} to {endURL1} is:\n")
    for url in path[:-1]:
        file.write(url + " -> \n")
    file.write(path[-1] + "\n\n")
    startURL2 = "https://en.wikipedia.org/wiki/Nobel_Prize"
    endURL2 = "https://en.wikipedia.org/wiki/Array_data_structure"
    path = wikiRace(startURL1, endURL1)
    file.write(f"Shortest path from {startURL2} to {endURL2} is:\n")
    for url in path[:-1]:
        file.write(url + " -> \n")
    file.write(path[-1] + "\n\n")
    file.close()
