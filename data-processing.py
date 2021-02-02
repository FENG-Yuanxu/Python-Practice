# -*- coding: utf-8 -*-
###############################################################################################################################################################################
"""
01 Data concatenation
"""
#In this question you are required to combine, or concatenate, two years of air pollution data.
#Input - 2014.csv 2015.csv; Output - output.csv
import os
import pandas as pd

#input files
path = r'C:\Users\thinkpad\Desktop\MFIN7033\2020 Fall Projects\Project 2\data'
raw2014csv = pd.read_csv(path + os.sep + '2014.csv')
raw2015csv = pd.read_csv(path + os.sep + '2015.csv')

# check columns
raw2014csv.columns.equals(raw2015csv.columns)

#concatenate
twoyearsconcat = pd.concat([raw2014csv,raw2015csv],ignore_index=True)

#change 1st column name to 'nan'
twoyearsconcat.rename(columns={'Unnamed: 0':float('nan')},inplace=True)

#output
twoyearsconcat.to_csv(path + os.sep + 'output.csv',index=False)

#############################################################################################################################################################################
"""
02 Data transformation
"""
#convert data in deal_level_data.csv to quarter_level_data.csv. 
#Input file: deal_level_data.csv； Output file: quarter_level_data.csv
import os
import pandas as pd

#input files and sort by 'Deal_Number'
path = r'C:\Users\thinkpad\Desktop\MFIN7033\2020 Fall Projects\Project 3\data'
deal_level_data = pd.read_csv(path + os.sep + 'deal_level_data.csv')
deal_level_data.sort_values(by=['Deal_Number'], inplace = True)

#basic information before quarter [:,0:14]                  column 1st to 14th
deal_level_data_basic = deal_level_data.iloc[:, 0:14]

#quarter information [:,14:39]                     column 1st, and 15th to 39th
deal_level_data_quarter = deal_level_data.iloc[:, 0:39]
deal_level_data_quarter.drop(deal_level_data_quarter.columns[1:14],axis=1,inplace=True)

#set index and sort by time series
deal_level_data_quarter.set_index(["Deal_Number"], inplace=True)
deal_level_data_quarter.sort_values(by=0,axis=1,inplace=True)

#stack quarter
quarter_stack = deal_level_data_quarter.stack().reset_index()
quarter_stack.rename(columns={"level_1": "quarter_i", 0: "quarter"},inplace=True)

#add 'quarter_to_the_event_date': -12 -11 -10 ... 10 11 12 ...
rangedict={}           
for i in range(3005):
    for j in range(25):
        rangedict[25*i+j] = j-12
quarter_to_the_event_date = pd.Series(rangedict)
quarter_stack['quarter_to_the_event_date'] = quarter_to_the_event_date

#merge
quarter_level_data1 = quarter_stack.merge(deal_level_data_basic,how='outer',on='Deal_Number')

#get strquarter: quarter__12 quarter__11 quarter__10 ...
strquarter = quarter_stack.iloc[0:25,1]

#stack each strdataname
for strdataname in [
            'Com_Net_Charge_Off', 'Com_Insider_Loan', 'Com_NIE', 'Com_NII',
            'Com_NIM', 'Com_ROA', 'Com_Total_Assets', 'Com_AvgSalary',
            'Com_EmployNum', 'Com_TtlSalary', 'Com_AvgSalary_log',
            'Com_EmployNum_log', 'Com_TtlSalary_log', 'Tar_Net_Charge_Off',
            'Tar_Insider_Loan', 'Tar_NIE', 'Tar_NII', 'Tar_NIM', 'Tar_ROA',
            'Tar_Total_Assets', 'Tar_AvgSalary', 'Tar_EmployNum', 'Tar_TtlSalary',
            'Tar_AvgSalary_log', 'Tar_EmployNum_log', 'Tar_TtlSalary_log']:
    
    #construct datanamelist
    datanamelist = pd.Series(['Deal_Number'])
    
    for i in range(len(strquarter)):
        datanamelist = datanamelist.append(pd.Series([strdataname + strquarter[i][7:]]))
    
    #construct datanametostack
    datanametostack = deal_level_data[datanamelist]
    datanametostack.set_index(["Deal_Number"], inplace=True)
    
    #stack
    dataname_stack = datanametostack.stack(dropna=False).reset_index()
    dataname_stack.rename(columns={0: strdataname},inplace=True)
    
    #concat each strdataname
    quarter_level_data1 = pd.concat([quarter_level_data1, dataname_stack[strdataname]], axis=1)

#output in expected order
quarter_level_data2 = quarter_level_data1[[
        'Deal_Number', 'Date_Announced', 'Year_Announced',
       'Acquirer_Name_clean', 'Acquirer_Primary_SIC', 'Acquirer_State_abbr',
       'Acquirer_CUSIP', 'Acquirer_Ticker', 'Target_Name_clean',
       'Target_Primary_SIC', 'Target_State_abbr', 'Target_CUSIP',
       'Target_Ticker', 'Attitude', 'quarter_to_the_event_date', 'quarter',
       'Com_Net_Charge_Off', 'Com_Insider_Loan', 'Com_NIE', 'Com_NII',
       'Com_NIM', 'Com_ROA', 'Com_Total_Assets', 'Com_AvgSalary',
       'Com_EmployNum', 'Com_TtlSalary', 'Com_AvgSalary_log',
       'Com_EmployNum_log', 'Com_TtlSalary_log', 'Tar_Net_Charge_Off',
       'Tar_Insider_Loan', 'Tar_NIE', 'Tar_NII', 'Tar_NIM', 'Tar_ROA',
       'Tar_Total_Assets', 'Tar_AvgSalary', 'Tar_EmployNum', 'Tar_TtlSalary',
       'Tar_AvgSalary_log', 'Tar_EmployNum_log', 'Tar_TtlSalary_log']]

#output
quarter_level_data2.to_csv(path + os.sep + 'quarter_level_data_new.csv',index=False)

#check
quarter_level_data = pd.read_csv(path + os.sep + 'quarter_level_data.csv')
(quarter_level_data.isnull() == quarter_level_data2.isnull()).all()
(quarter_level_data.fillna(0) == quarter_level_data2.fillna(0)).all() # one false!!!!!

#############################################################################################################################################################################
"""
03 Date time
"""
#extract the last date's data of each month from a time series
#Input: ukpound_exchange.csv ; Output: output.csv
import os
import pandas as pd

#input files
path = r'C:\Users\thinkpad\Desktop\MFIN7033\2020 Fall Projects\Project 4\data'
ukpound_exchange = pd.read_csv(path + os.sep + 'ukpound_exchange.csv')

#convert the date string into a “datetime” object
ukpound_exchange['Date'] = pd.to_datetime(ukpound_exchange['Date'],format="%m/%d/%Y")

#extract the last date's data by dropping others
for i in range(len(ukpound_exchange)-1):
    if ukpound_exchange['Date'][i].year == ukpound_exchange['Date'][i+1].year:
        if ukpound_exchange['Date'][i].month == ukpound_exchange['Date'][i+1].month:
            if ukpound_exchange['Date'][i].day < ukpound_exchange['Date'][i+1].day:
                ukpound_exchange['Date'][i] = float('nan')

#drop and change format
output_ukpound_exchange = ukpound_exchange.dropna()
output_ukpound_exchange['Date'] = output_ukpound_exchange['Date'].dt.strftime('%m/%d/%Y')

#output
output_ukpound_exchange.rename(columns={"Unnamed: 0": float('nan')}, inplace=True)
output_ukpound_exchange.to_csv(path + os.sep + 'output.csv', index=False)

#############################################################################################################################################################################
"""
04 Geolocation
"""
# find coordinates of S&P 1500's addresses
#compute each firms' distances with the White House (38.8976763,-77.0387185)
#Input: coname_addresses.xlsx; Output: output.xlsx
import os
import pandas as pd
from geopy.geocoders import TomTom
from geopy.distance import geodesic

#TomTom API key
geolocator = TomTom(api_key="aZaW7C9Ujz6rVhoqD21GmLRcnayAnIgN")

#input coname_addresses
path = r'C:\Users\thinkpad\Desktop\MFIN7033\2020 Fall Projects\5 TomTom API geolocation\data'
coname_addresses = pd.read_excel(path + os.sep + 'coname_addresses.xlsx') 

#prepare output columns
coname_addresses['lat'] = float('nan')
coname_addresses['lng'] = float('nan')
coname_addresses['distance'] = float('nan')

#White House location
WhiteHouse = (38.8976763,-77.0387185)

#locate coname and find lat, lng, distance
for i in coname_addresses.index:
    try:
        location = geolocator.geocode(coname_addresses['address'][i])
        coname_addresses['lat'][i] = location.latitude
        coname_addresses['lng'][i] = location.longitude
        latandlng = (location.latitude,location.longitude)
        coname_addresses['distance'][i] = geodesic(latandlng, WhiteHouse).km
    except:
        pass

#output
coname_addresses = coname_addresses[['CONAME','address','lat','lng','distance']]
coname_addresses.to_excel(path + os.sep + "output.xlsx", index=False) 

#############################################################################################################################################################################
"""
05 Fuzzy and multiprocessing
"""
#use the “Pool” function in the multiprocessing library, parallelly process each row of the acquirer data
#each acquirer should be matched to five bank names with the highest similarity
#input: acquirers.xlsx, bank_names.csv; output: output.csv
import os, csv, time
from multiprocessing import Pool
from fuzzywuzzy import fuzz
import pandas as pd

#input files
path = r'C:\Users\thinkpad\Desktop\MFIN7033\2020 Fall Projects\6 Fuzzy and multiprocessing\data'
acquirers = pd.read_excel(path + os.sep + 'acquirers.xlsx')
bank_names = pd.read_csv(path + os.sep + 'bank_names.csv')

#prepare output csv file
output = pd.DataFrame(columns=['acquirers', '0', '1', '2', '3', '4'])
output.to_csv(path + os.sep + 'output.csv', index=False)

#calculate fuzzratio by multiprocessing
def mainFunction(index):
    
    #get an acquirer name
    acquirername = acquirers['Acquirer Name'].iloc[index]
    
    #create an empty bank names list
    nameslist = pd.DataFrame([],index=range(len(bank_names)),columns=['Bank Name','Fuzz Ratio'])
    
    #find all bank names and calculate fuzz ratios
    for index2 in range(len(bank_names)):
        banknames = bank_names['bank_names'].iloc[index2]
        nameslist['Bank Name'][index2] = banknames
        
        name1 = acquirername.lower().replace(',',' ').replace('|',' ').replace('&',' ')
        name2 = banknames.lower().replace(',',' ').replace('|',' ').replace('&',' ')
        
        nameslist['Fuzz Ratio'][index2] = (fuzz.ratio(name1, name2)
                                           + fuzz.partial_ratio(name1, name2)
                                           + fuzz.token_sort_ratio(name1, name2) 
                                           + fuzz.token_set_ratio(name1, name2))
    
    #sort the names list by fuzz ratio    
    nameslist.sort_values(by='Fuzz Ratio', axis=0, inplace=True, ascending=False, ignore_index=True)    
    
    #output, write a new line to csv file
    csvfile = open(path + os.sep + 'output.csv', 'a+', newline='')
    linewriter = csv.writer(csvfile)
    linewriter.writerow([acquirername, nameslist['Bank Name'][0], nameslist['Bank Name'][1], 
                         nameslist['Bank Name'][2], nameslist['Bank Name'][3], nameslist['Bank Name'][4]])
    csvfile.close()

#perform parallel computing on fuzzy matching
if __name__ == '__main__':
    start_time = time.time() 
    p = Pool(processes = 7)
    p.map(mainFunction, range(len(acquirers)))
    print("--- %s seconds ---" % (time.time() - start_time))

#############################################################################################################################################################################
"""
06 Create gephi data
"""
import os
import numpy as np
import pandas as pd

path = r'C:\Users\thinkpad\Desktop\MFIN7033\2020 Fall Projects\7 Gephi\data'
names = pd.read_csv(path + os.sep + 'names.csv')

names['rand'] = np.random.lognormal(0,1,80) * 100

repeat1 = names.iloc[np.random.randint(0,20,400)]
project7data = pd.concat([names, repeat1],ignore_index=True)

repeat2 = names.copy()
repeat2['source'] = names['source'][0]
project7data = pd.concat([project7data, repeat2],ignore_index=True)

repeat3 = names.copy()
repeat3['source'] = names['source'][1]
project7data = pd.concat([project7data, repeat3],ignore_index=True)

project7data.to_csv(path + os.sep + 'project7data.csv',index=False)

#############################################################################################################################################################################
"""
07 Curve fit
scipy.optimize.curve_fit
scipy.stats.lognorm.fit
"""
#fit curve: a * np.exp(-b * x) + c
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def func(x, a, b, c):
    return a * np.exp(-b * x) + c

xdata = np.linspace(0, 4, 50)
y = func(xdata, 2.5, 1.3, 0.5)
np.random.seed(1729)
y_noise = 0.2 * np.random.normal(size=xdata.size)
ydata = y + y_noise

plt.plot(xdata, ydata, 'b-', label='data')

popt, pcov = curve_fit(func, xdata, ydata)
plt.plot(xdata, func(xdata, *popt), 'r-',
         label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))

popt, pcov = curve_fit(func, xdata, ydata, bounds=(0, [3., 1., 0.5]))
plt.plot(xdata, func(xdata, *popt), 'g--',
         label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))

plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()

#fit curve: lognormal pdf
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def func(x, mu, sigma):
    return (np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2)) / (x * sigma * np.sqrt(2 * np.pi)))

xdata = np.linspace(0.000001, 10, 50)
y = func(xdata, 0, 1)
y_noise = 0.2 * np.random.normal(size=xdata.size)

ydata = y + y_noise
plt.plot(xdata, ydata, 'b-', label='data')

popt, pcov = curve_fit(func, xdata, ydata)
plt.plot(xdata, func(xdata, *popt), 'r-',
         label='fit: mu=%5.3f, sigma=%5.3f' % tuple(popt))

popt, pcov = curve_fit(func, xdata, ydata, bounds=(0, [2., 1.]))
plt.plot(xdata, func(xdata, *popt), 'g--',
         label='fit: mu=%5.3f, sigma=%5.3f' % tuple(popt))

plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()

#scipy.stats.lognorm.fit
import numpy as np
from scipy.stats import lognorm
import matplotlib.pyplot as plt

mu = 0
sigma = 1

samplenumbers1 = np.random.lognormal(mu,sigma,1000)

samplenumbers2 = lognorm.rvs(sigma,0,np.exp(mu),1000)

shape, loc, scale = lognorm.fit(samplenumbers1, floc=0) 

fit_mu = np.log(scale)
fit_sigma = shape

count, bins, ignored = plt.hist(samplenumbers1, 100, density=True, align='mid')

x = np.linspace(min(bins), max(bins), 10000)

pdf1 = ((np.exp(-(np.log(x) - fit_mu)**2 / (2 * fit_sigma**2)) / 
        (x * fit_sigma * np.sqrt(2 * np.pi))))
pdf2 = lognorm.pdf(x,shape,0,scale)

plt.plot(x, pdf2, linewidth=2, color='r')
plt.axis('tight')
plt.show()
