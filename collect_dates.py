import re
from requesting_urls import get_html

def find_dates(html, output=None):
    """
    Method for finding all dates in a html page
    param1: the html you want to find dates in
    param2: the name of the output file you want the reaults in, default: None
    return: list of all the dates in the html
    """
    dates = []

    """Regex:
    Day: all dates having one or tow numbers (if two, first must start with 0-3)
    Month: all months listed
    Monthe number: 0-12
    Year: all years containg 4 digits, first must be 1 or 2 (year 1000 to 2999) 
    """ 
    day = r"[0-3]*\d{1}"
    month = r"January|February|March|April|May|June|July|August|September|October|November|December"
    abbr = r"Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec"
    monthNum = r"[0-12]\d"
    year = r"[1-2]\d{3}"

    #Concatinating the regex string to form the different date formats
    dmy = "(?:"+day+" |)" + "(?:"+month+"|"+abbr+")" + "(?: "+year+")"
    mdy = "(?:"+month+"|"+abbr+")"+"(?: "+day+",)"+"(?: "+year+")"
    ymd = "(?:"+year+" )"+"(?:"+month+"|"+abbr+")"+"(?: "+day+")"
    iso = "(?:"+year+"-)"+"(?:"+monthNum+"-)"+"(?:"+day+")"

    #Finding all the different dates in the html
    dmyDates = re.findall(dmy, html)
    mdyDates = re.findall(mdy, html)
    ymdDates = re.findall(ymd, html)
    isoDates = re.findall(iso, html)

    dates = []

    """
    For all loops below:
    Dates are wtitten in the yyyy/mm/dd format
    """
    #Converting all dates to the same format
    for date in dmyDates:
        day = month = year = "??"
        listed = date.split(" ")
        if len(listed) > 2:
            day = listed[0]
            month = monthToNumber(listed[1])
            year = listed[2]
        else:
            month = monthToNumber(listed[0])
            year = listed[1]
        dates.append(year+"/"+month+"/"+day)

    for date in mdyDates:
        day = month = year = "??"
        listed = date.split(" ")
        day = listed[1].strip(",")
        month = monthToNumber(listed[0])
        year = listed[2]
        dates.append(year+"/"+month+"/"+day)

    for date in ymdDates:
        day = month = year = "??"
        listed = date.split(" ")
        day = listed[2]
        month = monthToNumber(listed[1])
        year = listed[0]
        dates.append(year+"/"+month+"/"+day)

    for date in isoDates:
        day = month = year = "??"
        listed = date.split("-")
        day = listed[2]
        month = listed[1]
        year = listed[0]
        dates.append(year+"/"+month+"/"+day)

    #Sorting the dates and writes to file if output is given
    dates.sort()
    if output:
        file = open('filter_dates_regex/{}'.format(output), 'w')
        counter = 1
        for i in dates:
            file.write(str(counter) + ") " + i + "\n")
            counter += 1
        file.close()
    
    return dates

def monthToNumber(s):
    """
    Method to convert a moth (string) to the number representation of it
    param: month string
    return month int
    """
    dic = { 'January': 1,
            'February': 2,
            'March': 3,
            'April':4,
            'May':5,
            'June':6,
            'July':7,
            'August':8,
            'September':9,
            'October':10,
            'November':11,
            'December':12,
            'Jan': 1,
            'Feb': 2,
            'Mar': 3,
            'Apr':4,
            'May':5,
            'Jun':6,
            'Jul':7,
            'Aug':8,
            'Sep':9,
            'Oct':10,
            'Nov':11,
            'Dec':12}
    return str(dic[s])


if __name__ == "__main__":
    lp = get_html("https://en.wikipedia.org/wiki/Linus_Pauling")
    rn = get_html("https://en.wikipedia.org/wiki/Rafael_Nadal")
    jk = get_html("https://en.wikipedia.org/wiki/J._K._Rowling")
    rf = get_html("https://en.wikipedia.org/wiki/Richard_Feynman")
    hr = get_html("https://en.wikipedia.org/wiki/Hans_Rosling")

    lpDates = find_dates(lp.text, output="Linus_Pauling.txt")
    rnDates = find_dates(rn.text, output="Rafael_Nadal.txt")
    jkDates = find_dates(jk.text, output="J._K._Rowling.txt")
    rfDates = find_dates(rf.text, output="Richard_Feynman.txt")
    hrDates = find_dates(hr.text, output="Hans_Rosling.txt")