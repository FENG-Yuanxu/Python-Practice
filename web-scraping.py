# -*- coding: utf-8 -*-
"Web-scraping consists of 3 parts"

#___________________________PART 1 Air Quality__________________________________________________________
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
  
my_path = r'C:\Users\thinkpad\Desktop\MFIN7033\project 9 web-scraping\data'

# Chrome driver access is not allowed by this website, use IE and .send_keys(Keys.ENTER) to visit
driver_path = my_path + os.sep + 'IEDriverServer.exe'
browser = webdriver.Ie(executable_path = driver_path)

url = 'https://www.aqistudy.cn/historydata/'
browser.get(url)

air_quality_output = []

for a in range(1,23): # All cities lists from A to Z
    cities_xpath = '/html/body/div[3]/div/div[1]/div[2]/div[2]/ul[{}]/div[2]/li[position()>=1]/a'.format(a)
    
    # To let the website table fully loaded. (If "阿坝州" is founded, then the table is loaded.)
    try:
        wait_result = WebDriverWait(driver=browser, timeout=60, poll_frequency=1,  ignored_exceptions=None).until(
            EC.text_to_be_present_in_element((By.XPATH, '/html/body/div[3]/div/div[1]/div[2]/div[2]/ul[1]/div[2]/li[1]/a'), '阿坝州'))
    except:
        print("running except 1")
        browser.refresh() # Connection lost sometimes
        wait_result = WebDriverWait(driver=browser, timeout=60, poll_frequency=1,  ignored_exceptions=None).until(
            EC.text_to_be_present_in_element((By.XPATH, '/html/body/div[3]/div/div[1]/div[2]/div[2]/ul[1]/div[2]/li[1]/a'), '阿坝州'))
    
    cities_elements = browser.find_elements_by_xpath(cities_xpath)
    b_range = len(cities_elements)
    
    for b in range(b_range): # All cities in each lists from A to Z
        city_name = cities_elements[b].text
        
        # Website refuse computer access by href, also cannot use .click() function
        # Use following ".send_keys(Keys.ENTER)" to access city Air-Quality webpage successfully!!!
        browser.find_element_by_xpath(
            '/html/body/div[3]/div/div[1]/div[2]/div[2]/ul[{}]/div[2]/li[{}]/a'.format(a,b+1)
            ).send_keys(Keys.ENTER)
        
        # To let the new webpage table fully loaded. (If "-" is founded, then the table is loaded.)
        try:
            try:
                wait_result = WebDriverWait(driver=browser, timeout=60, poll_frequency=1,  ignored_exceptions=None).until(
                    EC.text_to_be_present_in_element((By.XPATH, '/html/body/div[3]/div[1]/div[1]/table/tbody/tr[2]/td[1]/a'), '-'))
            except:
                print("running except 2")
                browser.close() # Connection lost sometimes, browser.refresh() does not work.
                # Restart browser
                browser = webdriver.Ie(executable_path = driver_path)
                browser.get(url)
                browser.find_element_by_xpath(
                    '/html/body/div[3]/div/div[1]/div[2]/div[2]/ul[{}]/div[2]/li[{}]/a'.format(a,b+1)
                    ).send_keys(Keys.ENTER)
                wait_result = WebDriverWait(driver=browser, timeout=60, poll_frequency=1,  ignored_exceptions=None).until(
                    EC.text_to_be_present_in_element((By.XPATH, '/html/body/div[3]/div[1]/div[1]/table/tbody/tr[2]/td[1]/a'), '-'))
        except:
            pass # If the website detected selenium, restart does not work either.
        
        # After entering city Air-Quality webpage, calculate table row number
        table_rows_xpath = '/html/body/div[3]/div[1]/div[1]/table/tbody/tr[position()>=2]/td[1]/a'
        table_rows = len(browser.find_elements_by_xpath(table_rows_xpath))
        
        # Start to copy values
        max_retry = 0
        start_time = time.time() 
        while max_retry < 3:
            try:
                for count in range(table_rows):
                    date_xpath = '/html/body/div[3]/div[1]/div[1]/table/tbody/tr[{}]/td[1]/a'.format(count+2)
                    aqi_xpath = '/html/body/div[3]/div[1]/div[1]/table/tbody/tr[{}]/td[2]'.format(count+2)
                    range_xpath = '/html/body/div[3]/div[1]/div[1]/table/tbody/tr[{}]/td[3]'.format(count+2)
                    air_quality_level_xpath = '/html/body/div[3]/div[1]/div[1]/table/tbody/tr[{}]/td[4]'.format(count+2)
                    PM25_xpath = '/html/body/div[3]/div[1]/div[1]/table/tbody/tr[{}]/td[5]'.format(count+2)
                    PM10_xpath = '/html/body/div[3]/div[1]/div[1]/table/tbody/tr[{}]/td[6]'.format(count+2)
                    SO2_xpath = '/html/body/div[3]/div[1]/div[1]/table/tbody/tr[{}]/td[7]'.format(count+2)
                    CO_xpath = '/html/body/div[3]/div[1]/div[1]/table/tbody/tr[{}]/td[8]'.format(count+2)
                    NO2_xpath = '/html/body/div[3]/div[1]/div[1]/table/tbody/tr[{}]/td[9]'.format(count+2)
                    O3_xpath = '/html/body/div[3]/div[1]/div[1]/table/tbody/tr[{}]/td[10]'.format(count+2)
                    date_element = browser.find_element_by_xpath(date_xpath).text
                    date_year = date_element[:4]
                    date_month = date_element[5:]
                    aqi_element = browser.find_element_by_xpath(aqi_xpath).text
                    range_element = browser.find_element_by_xpath(range_xpath).text
                    air_quality_level_element = browser.find_element_by_xpath(air_quality_level_xpath).text
                    PM25_element = browser.find_element_by_xpath(PM25_xpath).text
                    PM10_element = browser.find_element_by_xpath(PM10_xpath).text
                    SO2_element = browser.find_element_by_xpath(SO2_xpath).text
                    CO_element = browser.find_element_by_xpath(CO_xpath).text
                    NO2_element = browser.find_element_by_xpath(NO2_xpath).text
                    O3_element = browser.find_element_by_xpath(O3_xpath).text
                    air_quality_output.append([city_name, date_year, date_month, aqi_element, range_element,
                                               air_quality_level_element, PM25_element, PM10_element,
                                               SO2_element, CO_element, NO2_element, O3_element])
                break
            except:
                print("running except 3")
                browser.refresh() # Connection lost sometimes
                wait_result = WebDriverWait(driver=browser, timeout=60, poll_frequency=1,  ignored_exceptions=None).until(
                    EC.text_to_be_present_in_element((By.XPATH, '/html/body/div[3]/div[1]/div[1]/table/tbody/tr[2]/td[1]/a'), '-'))  
            max_retry += 1
        # Average time per city: 210 seconds
        print(str(city_name) + "--- %s seconds ---" % (time.time() - start_time))
        
        # Go back to front page (cities list)
        browser.get(url)
        # To let the website table fully loaded. (If "阿坝州" is founded, then the table is loaded.)
        try:
            wait_result = WebDriverWait(driver=browser, timeout=60, poll_frequency=1,  ignored_exceptions=None).until(
                EC.text_to_be_present_in_element((By.XPATH, '/html/body/div[3]/div/div[1]/div[2]/div[2]/ul[1]/div[2]/li[1]/a'), '阿坝州'))
        except:
            print("running except 4")
            browser.refresh() # Connection lost sometimes
            wait_result = WebDriverWait(driver=browser, timeout=60, poll_frequency=1,  ignored_exceptions=None).until(
                EC.text_to_be_present_in_element((By.XPATH, '/html/body/div[3]/div/div[1]/div[2]/div[2]/ul[1]/div[2]/li[1]/a'), '阿坝州'))
        cities_elements = browser.find_elements_by_xpath(cities_xpath)
        
# Output csv file
df = pd.DataFrame(air_quality_output)
df.columns = ['City', 'Year', 'Month', 'AQI', 'Range', 'Air quality level', 'PM2.5', 'PM10', 'SO2', 'CO', 'NO2', 'O3']
df.to_csv(my_path + os.sep + 'Project1_AirQuality_output.csv', index = False, encoding='utf_8_sig')





#____________________PART 2 Douban Movie and IMDb_______________________________________________________
import os
import pandas as pd
from selenium import webdriver

my_path = r'C:\Users\thinkpad\Desktop\MFIN7033\project 9 web-scraping\data'

driver_path = my_path + os.sep + 'chromedriver.exe'
browser = webdriver.Chrome(executable_path = driver_path)

def save_douban_movie_information(movie_name):
    url_search_name = 'https://search.douban.com/movie/subject_search?search_text={}&cat=1002'.format(movie_name)
    browser.get(url_search_name)
    
    # To let the website table fully loaded
    browser.implicitly_wait(60)
    
    # .click() the first movie in the search list
    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div[1]/a').click()
    
    try:
        # Copy values
        movie_name_xpath = '//*[@id="content"]/h1/span[1]'
        movie_name_element = browser.find_element_by_xpath(movie_name_xpath).text
        release_date_xpath = '//*[@id="content"]/h1/span[2]'
        release_date_element = browser.find_element_by_xpath(release_date_xpath).text[1:-1]
        # Automatically record several director(s), actors/actresses
        directors_xpath = '//*[@id="info"]/span[1]/span[2]'
        directors_element = browser.find_element_by_xpath(directors_xpath).text
        actors_xpath = '//*[@id="info"]/span[3]/span[2]'
        actors_element = browser.find_element_by_xpath(actors_xpath).text
        rating_xpath = '//*[@id="interest_sectl"]/div[1]/div[2]/strong'
        rating_element = browser.find_element_by_xpath(rating_xpath).text
        people_rated_xpath = '//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span'
        people_rated_element = browser.find_element_by_xpath(people_rated_xpath).text
        introductions_xpath = '//*[@id="link-report"]/span[1]'
        introductions_element = browser.find_element_by_xpath(introductions_xpath).text
       
        # Output csv file
        movie_information = pd.DataFrame([[movie_name_element, release_date_element,
                                          directors_element, actors_element, rating_element,
                                          people_rated_element, introductions_element]])
        movie_information.columns = ['The name of movie', 'The release date', 'The director(s) of the movie',
                                     'The main actors/actresses of the movie', 'The average rating score',
                                     'The total amount of people who rated the movie', 'The brief introduction of the movie']
        movie_information.to_csv(my_path + os.sep + 'Project2_Douban_output_' + movie_name_element + '.csv', index = False, encoding='utf_8_sig')
    
    except:
        print(str(movie_name) + ' Information is not complete.')

def save_IMDb_movie_information(movie_name):
    url_search_name = 'https://www.imdb.com/find?q={}&ref_=nv_sr_sm'.format(movie_name)
    browser.get(url_search_name)
    
    # To let the website table fully loaded
    browser.implicitly_wait(60)
    
    # .click() the first movie in the search list
    browser.find_element_by_xpath('//*[@id="main"]/div/div[2]/table/tbody/tr[1]/td[2]/a').click()
    
    try:
        # Copy values
        movie_name_and_release_date_xpath = '//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[2]/div[2]/h1'
        movie_name_element = browser.find_element_by_xpath(movie_name_and_release_date_xpath).text[:-7]
        release_date_element = browser.find_element_by_xpath(movie_name_and_release_date_xpath).text[-5:-1]
        # Automatically record several director(s), actors/actresses
        directors_xpath = '//*[@id="title-overview-widget"]/div[2]/div[1]/div[2]'
        directors_element = browser.find_element_by_xpath(directors_xpath).text[10:]
        actors_xpath = '//*[@id="title-overview-widget"]/div[2]/div[1]/div[4]'
        actors_element = browser.find_element_by_xpath(actors_xpath).text[7:-25]
        rating_xpath = '//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[1]/div[1]/div[1]/strong/span'
        rating_element = browser.find_element_by_xpath(rating_xpath).text
        people_rated_xpath = '//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[1]/div[1]/a/span'
        people_rated_element = browser.find_element_by_xpath(people_rated_xpath).text
        introductions_xpath = '//*[@id="title-overview-widget"]/div[2]/div[1]/div[1]'
        introductions_element = browser.find_element_by_xpath(introductions_xpath).text
        
        # Output csv file
        movie_information = pd.DataFrame([[movie_name_element, release_date_element,
                                          directors_element, actors_element, rating_element,
                                          people_rated_element, introductions_element]])
        movie_information.columns = ['The name of movie', 'The release date', 'The director(s) of the movie',
                                     'The main actors/actresses of the movie', 'The average rating score',
                                     'The total amount of people who rated the movie', 'The brief introduction of the movie']
        movie_information.to_csv(my_path + os.sep + 'Project2_IMDb_output_' + movie_name_element + '.csv', index = False, encoding='utf_8_sig')
    
    except:
        print(str(movie_name) + ' Information is not complete.')

if __name__ == "__main__":  
    # input movie name(s) to search
    input_movie_name = input("Input movie names as [The Shawshank Redemption, Tenet, ...].\n")[1:-1].split(',')
    # output using map function
    list(map(save_douban_movie_information, input_movie_name))
    list(map(save_IMDb_movie_information, input_movie_name))


# output Douban top 250 movies in one csv file
douban_250_information = pd.DataFrame([])
for douban_webpage_i in range(10):
    douban_250_url = 'https://movie.douban.com/top250?start={}&filter='.format(25 * douban_webpage_i)
    browser.get(douban_250_url)
    browser.implicitly_wait(60)
    # .click() each movie in this page
    for movie_count in range(1,26):
        browser.find_element_by_xpath('//*[@id="content"]/div/div[1]/ol/li[{}]/div/div[2]/div[1]/a'.format(movie_count)).click()
        try:
            # Copy values
            movie_name_xpath = '//*[@id="content"]/h1/span[1]'
            movie_name_element = browser.find_element_by_xpath(movie_name_xpath).text
            release_date_xpath = '//*[@id="content"]/h1/span[2]'
            release_date_element = browser.find_element_by_xpath(release_date_xpath).text[1:-1]
            # Automatically record several director(s), actors/actresses
            directors_xpath = '//*[@id="info"]/span[1]/span[2]'
            directors_element = browser.find_element_by_xpath(directors_xpath).text
            actors_xpath = '//*[@id="info"]/span[3]/span[2]'
            actors_element = browser.find_element_by_xpath(actors_xpath).text
            rating_xpath = '//*[@id="interest_sectl"]/div[1]/div[2]/strong'
            rating_element = browser.find_element_by_xpath(rating_xpath).text
            people_rated_xpath = '//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span'
            people_rated_element = browser.find_element_by_xpath(people_rated_xpath).text
            introductions_xpath = '//*[@id="link-report"]/span[1]'
            introductions_element = browser.find_element_by_xpath(introductions_xpath).text
            # Output
            douban_250_information = douban_250_information.append([[movie_name_element, release_date_element,
                                                                    directors_element, actors_element, rating_element,
                                                                    people_rated_element, introductions_element]])
        except:
            print(str(douban_webpage_i+1) + ' ' + str(movie_count) + ' Information is not complete.')
        browser.get(douban_250_url)

douban_250_information.columns = ['The name of movie', 'The release date', 'The director(s) of the movie',
                                 'The main actors/actresses of the movie', 'The average rating score',
                                 'The total amount of people who rated the movie', 'The brief introduction of the movie']
douban_250_information.to_csv(my_path + os.sep + 'Project2_Douban250_output.csv', index = False, encoding='utf_8_sig')


# output IMDb top 250 movies in one csv file
IMDb_250_information = pd.DataFrame([])
IMDb_webpage_url = 'https://www.imdb.com/chart/top?ref_=nv_mv_250_6'
browser.get(IMDb_webpage_url)
browser.implicitly_wait(60)
for movie_count in range(250):
    browser.find_element_by_xpath('//*[@id="main"]/div/span/div/div/div[3]/table/tbody/tr[{}]/td[2]/a'.format(movie_count+1)).click()
    try:
        # Copy values
        movie_name_and_release_date_xpath = '//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[2]/div[2]/h1'
        movie_name_element = browser.find_element_by_xpath(movie_name_and_release_date_xpath).text[:-7]
        release_date_element = browser.find_element_by_xpath(movie_name_and_release_date_xpath).text[-5:-1]
        # Automatically record several director(s), actors/actresses
        directors_xpath = '//*[@id="title-overview-widget"]/div[2]/div[1]/div[2]'
        directors_element = browser.find_element_by_xpath(directors_xpath).text[10:]
        actors_xpath = '//*[@id="title-overview-widget"]/div[2]/div[1]/div[4]'
        actors_element = browser.find_element_by_xpath(actors_xpath).text[7:-25]
        rating_xpath = '//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[1]/div[1]/div[1]/strong/span'
        rating_element = browser.find_element_by_xpath(rating_xpath).text
        people_rated_xpath = '//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[1]/div[1]/a/span'
        people_rated_element = browser.find_element_by_xpath(people_rated_xpath).text
        introductions_xpath = '//*[@id="title-overview-widget"]/div[2]/div[1]/div[1]'
        introductions_element = browser.find_element_by_xpath(introductions_xpath).text 
        # Output
        IMDb_250_information = IMDb_250_information.append([[movie_name_element, release_date_element,
                                                             directors_element, actors_element, rating_element,
                                                             people_rated_element, introductions_element]])
    except:
        print(str(movie_count+1) + ' Information is not complete.')
    browser.get(IMDb_webpage_url)

IMDb_250_information.columns = ['The name of movie', 'The release date', 'The director(s) of the movie',
                                 'The main actors/actresses of the movie', 'The average rating score',
                                 'The total amount of people who rated the movie', 'The brief introduction of the movie']
IMDb_250_information.to_csv(my_path + os.sep + 'Project2_IMDb250_output.csv', index = False, encoding='utf_8_sig')





#_____________________________________PART 3 HKEX_______________________________________________________
import os
import datetime
import pandas as pd
from selenium import webdriver # Use selenium to execute js script
import bs4 as bs # Use bs4 to analyze table

my_path = r'C:\Users\thinkpad\Desktop\MFIN7033\project 9 web-scraping\data'

driver_path = my_path + os.sep + 'chromedriver.exe'
browser = webdriver.Chrome(executable_path = driver_path)
browser.implicitly_wait(60)

# Ask the user which type of shareholding he or she wants to download:
ask_type = input("Which type (a, b or c) of shareholding you want to download:\na. Southbound shareholding through Shanghai and Shenzhen Connect\nb. Northbound shareholding through Shenzhen Connect\nc. Northbound shareholding through Shanghai Connect\n")

if ask_type == 'a':
    url_type = 'http://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=hk'
elif ask_type == 'b':
    url_type = 'http://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=sz'
elif ask_type == 'c':
    url_type = 'http://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=sh'
else:
    print("Please input a, b or c.")

# Ask the user how much data he or she wants to download:
ask_amount = input("How much data (a or b) you want to download:\na. All the data in one year start from yesterday\nb. Customized period, specified by you\n")

if ask_amount == 'a':
    start_date = (datetime.date.today() - datetime.timedelta(days=365+1))
    end_date = (datetime.date.today() - datetime.timedelta(days=1))
elif ask_amount == 'b':
    start_date_input = input("Please input the start date as (YYYYMMDD) 20191202:\n")
    end_date_input = input("Please input the end date as (YYYYMMDD) 20201201:\n")
    start_date = datetime.datetime(int(start_date_input[:4]), int(start_date_input[4:6]), int(start_date_input[6:]))
    end_date = datetime.datetime(int(end_date_input[:4]), int(end_date_input[4:6]), int(end_date_input[6:]))

browser.get(url_type)
search_date = start_date

while search_date <= end_date:
    output = pd.DataFrame([])
    
    # Use selenium to execute_script and remove "readonly" attribute
    txtShareholdingDate = browser.find_element_by_xpath('//*[@id="txtShareholdingDate"]')
    browser.execute_script("arguments[0].removeAttribute('readonly','readonly')", txtShareholdingDate)
    
    # Use selenium to execute js script and input date
    js_date = 'document.getElementById("txtShareholdingDate").value="'+ search_date.strftime("%Y/%m/%d") + '";'
    browser.execute_script(js_date)
    
    # Use selenium to click search (Alternative way resp.post() is more complicated)
    browser.find_element_by_xpath('//*[@id="btnSearch"]').click()
    
    # Use bs4 to analyze table
    html_source = browser.page_source
    soup = bs.BeautifulSoup(html_source, 'lxml')
    table = soup.find('table', {'id': "mutualmarket-result"})
    
    # Copy values for each row
    for search_row in range(1, len(table.findAll('tr'))):
        this_row = table.findAll('tr')[search_row]
        
        Stock_code = this_row.findAll('td')[0].findAll('div')[1].text.strip()
        Stock_Name = this_row.findAll('td')[1].findAll('div')[1].text
        Shareholding_in_CCASS = this_row.findAll('td')[2].findAll('div')[1].text
        Shares_Percentage = this_row.findAll('td')[3].findAll('div')[1].text
        
        output = output.append([[Stock_code, Stock_Name, Shareholding_in_CCASS, Shares_Percentage]])
        
    # output
    output.columns=['Stock_code', 'Stock_Name', 'Shareholding_in_CCASS', 'Shares_Percentage']
    output.to_csv(my_path + os.sep + 'Project3_HKEX_' + search_date.strftime("%Y%m%d") + '_output.csv', index = False)
    
    # Loop
    search_date = search_date + datetime.timedelta(days=1)
