import unittest
import final_proj7 as f

# Your tests should show that you are able to access data from all of your sources, that your database is correctly constructed and can satisfy queries that are necessary for your program, and that your data processing produces the results and data structures you need for presentation.

class TestRA(unittest.TestCase):


    def testRAscrape(self):
        t = f.crawl_site(f.BASE_URL)
        tt = f.find_artists_on_page(t)
        hrefs = tt[0]
        names = tt[1]
        self.assertIn('/dj/aguycalledgerald', hrefs) # Testing that we are getting the right type of data (artist link)
        self.assertIn('Autechre', names) # Testing that we are getting the right type of data (artist name)

    def testArtistClass(self):
        t = f.crawl_site(f.BASE_URL)
        tt = f.find_artists_on_page(t)
        hrefs = tt[0]
        first_one = tt[0][0]
        names = tt[1]
        art_st = f.get_site_for_artist(first_one)
        self.assertEqual('Name: A Guy Called Gerald, Country: United Kingdom, Favourites: 4875, Gigs: 2 ', art_st.__str__())
        self.assertEqual(art_st.name, "A Guy Called Gerald")
        self.assertEqual(art_st.country, "United Kingdom")
        self.assertEqual(art_st.member_fav, 4875)
        self.assertEqual(art_st.num_of_gigs, 2)

    def testDataBase(self):
        thing = f.crawl_site(f.BASE_URL)
        thing2 = f.find_artists_on_page(thing)
        first = thing2[0]
        clean = [x for x in first if x != None] #cleaning out list and removing 'NoneTypes'
        list_of_names = []
        list_of_gigs = []
        list_of_favs = []
        list_of_countrys = []
        for i in range(101):
            thing3 = f.get_site_for_artist(clean[i])
            list_of_names.append(thing3.name)
            list_of_gigs.append(thing3.num_of_gigs)
            list_of_favs.append(thing3.member_fav)
            list_of_countrys.append(thing3.country)
        self.assertEqual(len(list_of_names), 101)
        self.assertEqual(len(list_of_gigs), 101)
        self.assertEqual(len(list_of_favs), 101)
        self.assertEqual(len(list_of_countrys), 101)




unittest.main(verbosity=2)
