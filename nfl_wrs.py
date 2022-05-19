import pandas as pd
from bs4 import BeautifulSoup as BS
import requests

#Assign URLS
URL2019 = 'https://www.pro-football-reference.com/years/2019/receiving.htm'
URL2020 = 'https://www.pro-football-reference.com/years/2020/receiving.htm'
URL2021 = 'https://www.pro-football-reference.com/years/2021/receiving.htm'

#Use requests module to download the HTML content from each URL
page2019 = requests.get(URL2019)
page2020 = requests.get(URL2020)
page2021 = requests.get(URL2021)

#Convert the HTML into a beautiful soup object
soup2019 = BS(page2019.content, 'html.parser')
soup2020 = BS(page2020.content, 'html.parser')
soup2021 = BS(page2021.content, 'html.parser')

#Use the beautiful soup find method to return the table on each page
table2019 = soup2019.find('table')
table2020 = soup2020.find('table')
table2021 = soup2021.find('table')

#Use the pandas read_html method to convert the table into a dataframe object
df2019 = pd.read_html(str(table2019))[0]
df2020 = pd.read_html(str(table2020))[0]
df2021 = pd.read_html(str(table2021))[0]

#
df2019 = df2019.iloc[:, 1:]
df2020 = df2020.iloc[:, 1:]
df2021 = df2021.iloc[:, 1:]

#Create a list of numeric columns
numeric_columns = ['Age','G','GS','Tgt','Rec','Yds','Y/R','TD','1D','Lng','Y/Tgt','R/G','Y/G','Fmb']

#Convert numeric columns from strings into numeric values
for i in numeric_columns:
    df2019[i] = pd.to_numeric(df2019[i], errors='coerce')
    df2020[i] = pd.to_numeric(df2020[i], errors='coerce')
    df2021[i] = pd.to_numeric(df2021[i], errors='coerce')

#Create Fantasy Points statistic 
df2019['Fantasy Points'] = (
    ((df2019[('Yds')] * .1) + 
    (df2019[('TD')] * 6) -
    (df2019['Fmb'] * 2)) 
)
df2020['Fantasy Points'] = (
    ((df2020[('Yds')] * .1) + 
    (df2020[('TD')] * 6) -
    (df2020['Fmb'] * 2)) 
)
df2021['Fantasy Points'] = (
    ((df2021[('Yds')] * .1) + 
    (df2021[('TD')] * 6) -
    (df2021['Fmb'] * 2)) 
)

#Sort Dataframes by Fantasy Points
df2019 = df2019.sort_values(by=['Fantasy Points'], ascending=False)
df2020 = df2020.sort_values(by=['Fantasy Points'], ascending=False)
df2021 = df2021.sort_values(by=['Fantasy Points'], ascending=False)

#Create Tiers
wr_tier_1_2019 = df2019[:5]
wr_tier_2_2019 = df2019[5:10]
wr_tier_3_2019 = df2019[10:15]
wr_tier_1_2020 = df2020[:5]
wr_tier_2_2020 = df2020[5:10]
wr_tier_3_2020 = df2020[10:15]
wr_tier_1_2021 = df2021[:5]
wr_tier_2_2021 = df2021[5:10]
wr_tier_3_2021 = df2021[10:15]

print(wr_tier_3_2021)
