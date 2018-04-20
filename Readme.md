######READ ME FOR FINAL PROJECT###### Kiran Bhumber



#### CODE STRUCTURE ####

This project crawls and scrapes the first top 100 Artists in Resident Advisor <https://www.residentadvisor.net/>.

It first does this by extracting all of the links to the artist in the 1000 DJS page here:
<https://www.residentadvisor.net/dj.aspx>

And then proceeds to crawl each artist page from there to collect the Artist's Name, Current Country, Member's Favourite Count, and How Many Gigs They Have Listed.

The code is structured by three main crawling and scraping functions (crawl_site, find_artists_on_page and get_site_for_artist).
The crawl_site function calls on the main caching function (make_request_using_cache) which stores each page's data that is crawled and scraped.

After the desired data has been collected (using BeautifulSoup), it is passed into the Artist class constructor, which stores each data component into corresponding class variables.

These class variables are stored in subsequent lists and used to create the database 'artists.db'.

artist.db consists of two tables:
'Artists', which lists all of the artists information. 'CountryOfOrigin' consists of a foreign key which points to the 'Country' table.

The 'Country' table lists the different Country of Origins of the artists.

#### INSTRUCTIONS ####

1. This project utilizes Plotly, a graphing service which works with Python.
You will need to create an account at <https://plot.ly/> You must verify your account through email.

2. install all of the requirements listed in the requirements.txt file


3. The main program is called 'final_proj7.py' When this is run, it will load and create the database from the RA.json file (This takes awhile.. approx 4 mins). You will then be prompted to enter a command, or to select 'help' which will give you four commands to choose from that contain different visualizations of the data that is being presented. These are as follows:

First 50 Artists in RA and How Many Fan 'Likes' They Have (Press '1')

First 50 Artists in RA and The Number of Gigs They Have Listed (Press '2')

Percentage of Countries Making up RA Fan's Likes (Press '3')

Number of Artists that Make Up Each Country (Press '4')

To exit the program, simply type exit.
