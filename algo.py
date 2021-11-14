import requests
import re # regular expressions
from bs4 import BeautifulSoup
from requests.api import options
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd


# path to CHROME DRIVER
CHROME_DRIVER_PATH = r'C:\Users\Loverdrive\Downloads\chromedriver.exe'

# URL FOR PARSING DATA
URL = 'https://www.booking.com/searchresults.ru.html?label=gen173nr-1DCAEoggI46AdIM1gEaIABiAEBmAEhuAEXyAEP2AED6AEBiAIBqAIDuAKGq4yLBsACAdICJDdiODdhOTJlLWE0ZWYtNGY1My1hODYxLWI5ZTFjMmVhMTk5ZtgCBOACAQ&sid=422adcbba58c7f8294bf077eff162d2b&sb=1&src=searchresults&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.ru.html%3Flabel%3Dgen173nr-1DCAEoggI46AdIM1gEaIABiAEBmAEhuAEXyAEP2AED6AEBiAIBqAIDuAKGq4yLBsACAdICJDdiODdhOTJlLWE0ZWYtNGY1My1hODYxLWI5ZTFjMmVhMTk5ZtgCBOACAQ%3Bsid%3D422adcbba58c7f8294bf077eff162d2b%3Btmpl%3Dsearchresults%3Bcheckin_month%3D11%3Bcheckin_monthday%3D8%3Bcheckin_year%3D2021%3Bcheckout_month%3D11%3Bcheckout_monthday%3D28%3Bcheckout_year%3D2021%3Bclass_interval%3D1%3Bdest_id%3D-2343962%3Bdest_type%3Dcity%3Bdtdisc%3D0%3Bfrom_sf%3D1%3Bgroup_adults%3D1%3Bgroup_children%3D0%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Bno_rooms%3D1%3Boffset%3D0%3Bpostcard%3D0%3Braw_dest_type%3Dcity%3Broom1%3DA%3Bsb_price_type%3Dtotal%3Bsearch_selected%3D1%3Bshw_aparth%3D1%3Bslp_r_match%3D0%3Bsrc%3Dindex%3Bsrc_elem%3Dsb%3Bsrpvid%3Df9b97a69e7530078%3Bss%3D%25D0%25A8%25D1%258B%25D0%25BC%25D0%25BA%25D0%25B5%25D0%25BD%25D1%2582%252C%2B%25D0%259A%25D0%25B0%25D0%25B7%25D0%25B0%25D1%2585%25D1%2581%25D1%2582%25D0%25B0%25D0%25BD%3Bss_all%3D0%3Bssb%3Dempty%3Bsshis%3D0%3Btop_ufis%3D1%3Bsig%3Dv1WEnyBfZM%26%3B&ss=%D0%A8%D1%8B%D0%BC%D0%BA%D0%B5%D0%BD%D1%82&is_ski_area=0&ssne=%D0%A8%D1%8B%D0%BC%D0%BA%D0%B5%D0%BD%D1%82&ssne_untouched=%D0%A8%D1%8B%D0%BC%D0%BA%D0%B5%D0%BD%D1%82&city=-2343962&checkin_year=2021&checkin_month=11&checkin_monthday=7&checkout_year=2021&checkout_month=11&checkout_monthday=10&group_adults=1&group_children=0&no_rooms=1&sb_changed_group=1&sb_changed_dates=1&from_sf=1'
driver = webdriver.Chrome(CHROME_DRIVER_PATH)
driver.get(URL)
content = driver.page_source
# GET URL AS DATA
soup = BeautifulSoup(content, "html.parser")

# FIND TO DATA FOR PARSING
result = soup.find('h1', attrs={'class': '_30227359d _0db903e42'}).text

# GET NUMBER OF PAGE FOR PAGINATION
resultSize = result.split()[2]


# PREPARE ARRAYS FOR DATE
names = []
prices = []
descriptions = []
ratings = []
prices = []



i = 0

# ITERATION FOR PAGINATION
while i < int(resultSize):

    driver.get(URL+'&offset='+str(i))
    content = driver.page_source
    soupStr = BeautifulSoup(content, "html.parser")

    # ITERATION FOR EVERY DATA
    for blockStr in soupStr.findAll('div', attrs={'class': '_fe1927d9e _0811a1b54 _a8a1be610 _022ee35ec b9c27d6646 fb3c4512b4 fc21746a73'}):
        
        # GET DATA NAME, PRICE, RATING, DESCRIPTION
        name_str =      blockStr.find('div', attrs={'class': 'fde444d7ef _c445487e2'}).text
        price =         blockStr.find('span', attrs={'class': 'fde444d7ef _e885fdc12'}).text

        # THERA IS "TRY" BECAUSE CAN BE NULL
        try:    rating = blockStr.find( 'div', attrs={'class': '_9c5f726ff bd528f9ea6'}).text
        except: rating = ""

        # THERA IS "TRY" BECAUSE CAN BE NULL
        try:    description = blockStr.find('span', attrs={'class': '_c5d12bf22'}).text
        except: description = ""

        # APPEND TO ARRAY
        names.append(name_str)
        prices.append(price)
        ratings.append(rating)
        descriptions.append(description)
    
    # EVERY PAGE HAS 25 DATA   
    i+=25


# FORMATTIN ALL DATA INTO CLASS
data = {'name': names,'price': prices,"rating": ratings,'description': descriptions }

# PARSING DATACLASS TO AS CSV FILE
df = pd.DataFrame(data)
df.to_csv('booking_data_shymkent.csv', index=False)


