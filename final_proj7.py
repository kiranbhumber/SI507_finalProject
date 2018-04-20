from bs4 import BeautifulSoup
import requests
import sys
import plotly.plotly as py
import plotly.graph_objs as go
import json
import sqlite3




### CLASS ARTIST ###
# param: name, country, member fav number, and number of gigs
class Artist():
    def __init__(self, name, country, member_fav, num_of_gigs):
        self.name = name
        self.country = country
        self.member_fav = member_fav
        self.num_of_gigs = num_of_gigs

# returns: The name, country, member fav and number of gigs in string format
    def __str__(self):
        return "Name: {}, Country: {}, Favourites: {}, Gigs: {} ".format(self.name, self.country, self.member_fav, self.num_of_gigs)

### END OF CLASS ARTIST CODE ###

### BEGINNING OF CACHING CODE ###
CACHE_FNAME = 'RA.json'
CACHE_FNAME_2 = 'RA_artists.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}


# returns a string which represents the unique search url as a key for the cached json file
# param: a search url that will be crawled
# return: a string
def params_unique_combination(search_url):
    return search_url

# returns: a dictionary from the cached file upon making a request to crawl and scrape data from a site
# param: a search url to request data from
# return: data from the cached dictionary where the key is the params_unique_combination
def make_request_using_cache(search_url):
    global header
    unique_ident = params_unique_combination(search_url)
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        print("Making a request for new data...")
# Make the request and cache the new data
        site_res = requests.get(search_url)
        try:
            site_res.raise_for_status()
        except Exception as exc:
            print('google shieet mae: %s' %(exc))
            sys.exit(1)
        CACHE_DICTION[unique_ident] = site_res.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

### GLOBAL VARIABLES ###
BASE_URL = 'https://www.residentadvisor.net/dj.aspx'
list_of_hrefs = []
list_of_artist = []
list_of_gigs = []
my_dict = {}
my_country_dict = {}
reult  = []
DBNAME = 'artists.db'

### END OF GLOBAL VARIABLES ###
# description: crawls the site. Calls the caching function which checks to see if it is already in the cache, if not, it creates a new request using requests.get
# returns: The data from the web page to crawl
# param: The url of the site to crawl

def crawl_site(url):
    page = make_request_using_cache(url)
    site_res = requests.get(url)
    try:
        site_res.raise_for_status()
    except Exception as exc:
        print('uh oh: %s' %(exc))
        sys.exit(1)
    return page

### END OF CACHING CODE ###

# description: crawls the main url and scrapes the 'href' of the artists and the artists names using beautiful soup
# returns a list of artists and a list of the artists '/hrefs'
# param: The page that is returned from the 'crawl_site' function
# returns: a tuple containing two lists
def find_artists_on_page(page):
    soup = BeautifulSoup(page, 'html.parser')
    site_test = soup.find_all('a')
    for link in site_test:
        try:
            end_link = link.get('href')
            artist_name = link.getText('href')
            list_of_hrefs.append(end_link)
            if artist_name == "":
                pass
            else:
                list_of_artist.append(artist_name)
        except:
            print("does not have name")
            pass
    new_list_of_artist = list_of_artist[53:]
    new_list_of_hrefs = list_of_hrefs[53:]

    return new_list_of_hrefs, new_list_of_artist

# description: crawls each artists site and scrapes the neccessary data using beautiful soup
# returns all of the variables of the artist (name, country etc)
# param: the '/href' which points to the artists page
# return: a list of all the class variables
def get_site_for_artist(artist_name):
    url = BASE_URL[:-8] + artist_name
    artist_site = crawl_site(url)
    # print(url)
    soup2 = BeautifulSoup(artist_site, 'html.parser')
    artist_country = soup2.select('span[itemprop="country"]')[0].getText()
    try:
        artist_name = soup2.find_all(class_='position')[0]
        artist = artist_name.find_all('h1')[0].string
    except:
        artist = 'No'
    try:
        fav = soup2.find_all(id ='MembersFavouriteCount')[0].text.strip()
        if len(fav) >= 4:
            fav = fav.replace(',', '')
        else:
            pass
        fav = int(fav)
    except:
        fav = 0
    gigs = soup2.find_all('ul')
    try:
        gigs2 = soup2.select('li[itemtype="http://data-vocabulary.org/Event"]')
        gig_num = len(gigs2)
    except:
        pass

    return Artist(artist, artist_country, fav, gig_num)

### CODE TO REMOVE DUPLICATES FROM A LIST ###

# description: removes duplicates from a list. In this case it does it for the countrys list
# param: a list of values
# returns: a list
def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        # If value has not been encountered yet,
        # ... add it to both list and set.
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output

### END OF REMOVE DUPLICATE FUNCTION

# Remove duplicates from this list.



### START OF DATABASE CODE ###
# description: initializes and creates the tables for the database 'artist.db'
# param: db name
# return: none. creates Database using sqlite3
def init_db(DBNAME):
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        print("connected to database")
    except:
        print("Failiure to connect to database")

    # Drop tables
    s1 = '''
        DROP TABLE IF EXISTS 'Artists';
    '''
    s2 = '''
        DROP TABLE IF EXISTS 'Countries';
    '''
    cur.execute(s1)
    cur.execute(s2)
    conn.commit()


    statement2 = '''
            CREATE TABLE 'Countries' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Country' TEXT
                );
         '''

    statement1 = '''
            CREATE TABLE 'Artists' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Name' TEXT NOT NULL,
                'NumOfGigs' INTEGER,
                'NumOfFavs' INTEGER,
                'Country' Text,
                'CountryOfOrigin' TEXT,
                FOREIGN KEY ('CountryOfOrigin') REFERENCES Countries('Id')
                );
        '''

    cur.execute(statement2)
    cur.execute(statement1)

    return

# description: inserts artist and country data into the artist.db database
# param: none
# return: none
def insert_stuff(result):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    for i in range(101):
        insertion2 = (None, my_dict['Name'][i], my_dict['NumGigs'][i], my_dict['NumofFavs'][i], my_dict['Countries'][i], None)
        statement2 = 'INSERT INTO "Artists" '
        statement2 += 'VALUES (?, ?, ?, ?, ?, ?) '
        cur.execute(statement2, insertion2)

    for i in range(len(result)):
        insertion = (None, result[i])
        statement = 'INSERT INTO "Countries" '
        statement += 'VALUES (?, ?) '
        cur.execute(statement, insertion)

    for key in my_country_dict:
        try:
            # print(key)
            # print("=====================")
            print(str(my_country_dict[key]))
            # cur.execute('UPDATE ARTISTS SET CountryOfOrigin =' + str(my_country_dict[key]) + ' WHERE CountryOfOrigin' + "'" + key + "'" )
            cur.execute('UPDATE ARTISTS SET CountryOfOrigin =' + str(my_country_dict[key]) + ' WHERE Country=' + '"' + key + '"')

        except:
            pass

    conn.commit()
    conn.close()


### END OF DATABASE BUILING CODE ###

### MAKING DATA BASE INQUIRIES ###

# description: gets the top 50 artists and how many fan 'favourites' they have
# returns: the list of artist names, and a list of how many fan favourites they have
# param: none
# return: a tuple containing two lists
def get_artists_with_favs():
    artist_names = []
    artist_fav = []
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except:
        print("Failed to Connect to DATABASE")

    statement = 'SELECT Name, NumOfFavs '
    statement += 'FROM ARTISTS '
    statement += 'ORDER BY NumOfFavs DESC '
    statement += 'LIMIT 50'
    result = cur.execute(statement)
    for row in cur:
        artist_names.append(row[0])
        artist_fav.append(row[1])
    conn.commit()
    conn.close()

    return artist_names, artist_fav


def artist_num_of_gigs():
    artist_list = []
    gig_list = []
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except:
        print("Failed to Connect to DATABASE")

    statement = 'SELECT Name, NumOfGigs '
    statement += 'FROM ARTISTS '
    statement += 'ORDER BY NumOfGigs DESC '
    statement += 'LIMIT 50'
    cur.execute(statement)
    for row in cur:
        artist_list.append(row[0])
        gig_list.append(row[1])
    conn.commit()
    conn.close()
    return artist_list, gig_list

def country_and_favs():
    country_list = []
    fav_list = []
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except:
        print("Failed to Connect to DATABASE")

    statement = 'SELECT Countries.Country, Artists.NumOfFavs '
    statement += 'FROM COUNTRIES '
    statement += 'JOIN ARTISTS '
    statement += 'WHERE Countries.Id = Artists.CountryOfOrigin '
    statement += 'GROUP BY Countries.Country '
    statement += 'LIMIT 50'
    cur.execute(statement)
    for row in cur:
        country_list.append(row[0])
        fav_list.append(row[1])
    conn.commit()
    conn.close()
    return country_list, fav_list

def country_and_num_of_arist():
    country_list = []
    artist_list =[]
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except:
        print("Failed to Connect to DATABASE")

    statement = 'SELECT Countries.Country, COUNT(Artists.Name) '
    statement += 'FROM COUNTRIES '
    statement += 'JOIN ARTISTS '
    statement += 'WHERE Countries.Id = Artists.CountryOfOrigin '
    statement += 'GROUP BY Countries.Country '
    statement += 'LIMIT 50'
    cur.execute(statement)
    for row in cur:
        country_list.append(row[0])
        artist_list.append(row[1])
    conn.commit()
    conn.close()
    return country_list, artist_list



### END OF DATABASE INQUIRIES ###


### PLOTLY CODE NEED FOUR DIFFERENT GRAPHS ###

def plotly_scatter(dataX, dataY):
    data_x = dataX
    data_y = dataY


    # Create a trace
    trace = go.Bar(
        x = data_x,
        y = data_y,
        # mode = 'markers'
        )

    data = [trace]

    layout = go.Layout(
    title='First 50 Artists in RA and How Many Fan "Likes" They Have',
    xaxis=dict(
        title='Artist Names',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#9542f4'
        )
    ),
    yaxis=dict(
        title='Number of Likes',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#9542f4'
        )
    )
)

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='basic-scatter')

def plotly_scatter_two(dataX, dataY):
    # random_x = ["First", "Second"]
    # random_y = [ 5, 7 ]

    data_x = dataX
    data_y = dataY
    # Create a trace
    trace = go.Bar(
        x = data_x,
        y = data_y,
        offset = data_x[0]
        )

    data = [trace]

    layout = go.Layout(
    title='First 50 Artists in RA and The Number of Gigs They Have Listed',
    xaxis=dict(
        title='Artist Names',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#9542f4'
        )
    ),
    yaxis=dict(
        title='Number of Gigs',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#9542f4'
        )
    )
)

    fig = go.Figure(data=data, layout=layout)

    py.plot(fig, filename='basic-scatter_two')

def plotly_pie_chart(c_names, f_num):
    labels = c_names
    values = f_num

    # labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
    # values = [4500,2500,1053,500]

    fig = {
        "data": [
            {
            "values": values,
            "labels": labels,
            "type": "pie"
                    },
                    ],
        "layout": {
            "title":"Percentage of Countries Making up RA Fan's Likes",
            "annotations": [
                {
                    "font": {
                        "size": 20
                        },

                    },

                ]
            }
        }


    py.plot(fig, filename='testthing')
    return

def plotly_pie_chart_two(c_names_two, n_artist):
    labels = c_names_two
    values = n_artist


    fig = {
        "data": [
            {
            "values": values,
            "labels": labels,
            "type": "pie",
            "hoverinfo" : "label+percent",
            "textinfo" : "value"
                    },
                    ],
        "layout": {
            "title":"Number of Artists that Make Up Each Country",
            "annotations": [
                {
                    "font": {
                        "size": 20
                        },

                    },

                ]
            }
        }


    py.plot(fig, filename='pie_chart_2')
    return


### END OF PLOTLY CODE ###


if __name__ == '__main__':



    #### TEST CODE ####
    # test1 = thing2[0]
    # test2 = thing2[1]
    # print(len(test1))
    # print(len(test2))
    # get_site_for_artist(test1)

    ### END OF TEST CODE ###

    ### COMPLETE SCRAPING/CRAWLING AND BUILDING DATABASE CODE ###
    thing = crawl_site(BASE_URL)
    thing2 = find_artists_on_page(thing)


    ### CODE TO BUILD DATA BASE ###
    first = thing2[0]
    clean = [x for x in first if x != None] #cleaning out list and removing 'NoneTypes'
    list_of_names = []
    list_of_gigs = []
    list_of_favs = []
    list_of_countrys = []
    #
    for i in range(101):
        thing3 = get_site_for_artist(clean[i])

        list_of_names.append(thing3.name)
        list_of_gigs.append(thing3.num_of_gigs)
        list_of_favs.append(thing3.member_fav)
        list_of_countrys.append(thing3.country)

    # print(list_of_favs)
    result = remove_duplicates(list_of_countrys)
    # print(result)
    my_dict['Name'] = list_of_names
    my_dict['NumGigs'] = list_of_gigs
    my_dict['NumofFavs'] = list_of_favs
    my_dict['Countries'] = list_of_countrys
    # print(my_dict)


    start_key = 1
    for i in range(len(result)):
        my_country_dict[result[i]] = start_key
        start_key = start_key + 1
    # print(my_country_dict)

    data = init_db(DBNAME)
    dataagain = insert_stuff(result)

    ### END OF COMPLETE SCRAPING/CRAWLING AND BUILDING DATABASE CODE ###

    ### INTERACTIVE CODE STARTS HERE ###

    while (True):
        x = input("Welcome to The 'Resident Advisor' Program. You will be able to explore\nrelationships between the First TOP 100 Artists listed on RA.\n(Enter a command or 'Help' for Options) \nTo exit the program, enter 'exit': ")
        print("\n")

        if x == 'help':
            print(" DATA VISUALIZATIONS YOU CAN CHOOSE FROM")
            print("*******************************************************")
            print("1. First 50 Artists in RA and How Many Fan 'Likes' They Have (Press '1')")
            # print("\n")
            print("2. First 50 Artists in RA and The Number of Gigs They Have Listed (Press '2')")
            # print("\n")
            print("3. Percentage of Countries Making up RA Fan's Likes (Press '3')")
            # print("\n")
            print("4. Number of Artists that Make Up Each Country (Press '4')")
            print("*******************************************************")
            print("\n")

        elif x == '1':
            print("You Chose Option 1")
            x = get_artists_with_favs()
            artists = x[0]
            fav_nums = x[1]
            plotly_scatter(artists, fav_nums)

        elif x == '2':
            print("You Chose Option 2")
            y = artist_num_of_gigs()
            art_names = y[0]
            gig_nums = y[1]
            plotly_scatter_two(art_names, gig_nums)
        elif x == '3':
            print("You Chose Option 3")
            z = country_and_favs()
            # print(z)
            c_names = z[0]
            # print(c_names)
            f_num = z[1]
            # print(f_num)
            plotly_pie_chart(c_names, f_num)
        elif x == '4':
            print("You Chose Option 4")
            zz = country_and_num_of_arist()
            c_names_two = zz[0]
            n_artist = zz[1]
            # print(zz[0])
            # print(zz[1])
            plotly_pie_chart_two(c_names_two, n_artist)
        elif x == 'exit':
            break
        else:
            print("I'm sorry, that is not a command")



    ### INTERACTIVE CODE ENDS HERE ###

    # x = get_artists_with_favs()
    # artists = x[0]
    # fav_nums = x[1]
    # plotly_scatter(artists, fav_nums)
    # #
    # y = artist_num_of_gigs()
    # art_names = y[0]
    # gig_nums = y[1]
    # #plotly_scatter_two(art_names, gig_nums)
    # z = country_and_favs()
    # # print(z)
    # c_names = z[0]
    # # print(c_names)
    # f_num = z[1]
    # # print(f_num)
    # # plotly_pie_chart(c_names, f_num)
    #
    # zz = country_and_num_of_arist()
    # c_names_two = zz[0]
    # n_artist = zz[1]
    # # print(zz[0])
    # # print(zz[1])
    # plotly_pie_chart_two(c_names_two, n_artist)
