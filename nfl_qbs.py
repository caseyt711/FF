import pandas as pd
from bs4 import BeautifulSoup as BS
import requests

#Assign URLS
URL2019 = 'https://www.pro-football-reference.com/years/2019/passing.htm'
URL2020 = 'https://www.pro-football-reference.com/years/2020/passing.htm'
URL2021 = 'https://www.pro-football-reference.com/years/2021/passing.htm'
Rushing_URL2019 = 'https://www.pro-football-reference.com/years/2019/rushing.htm'
Rushing_URL2020 = 'https://www.pro-football-reference.com/years/2020/rushing.htm'
Rushing_URL2021 = 'https://www.pro-football-reference.com/years/2021/rushing.htm'

#Use requests module to download the HTML content from each URL
page2019 = requests.get(URL2019)
page2020 = requests.get(URL2020)
page2021 = requests.get(URL2021)
Rushing_page2019 = requests.get(Rushing_URL2019)
Rushing_page2020 = requests.get(Rushing_URL2020)
Rushing_page2021 = requests.get(Rushing_URL2021)

#Convert the HTML into a beautiful soup object
soup2019 = BS(page2019.content, 'html.parser')
soup2020 = BS(page2020.content, 'html.parser')
soup2021 = BS(page2021.content, 'html.parser')
Rushing_soup2019 = BS(Rushing_page2019.content, 'html.parser')
Rushing_soup2020 = BS(Rushing_page2020.content, 'html.parser')
Rushing_soup2021 = BS(Rushing_page2021.content, 'html.parser')

#Use the beautiful soup find method to return the table on each page
table2019 = soup2019.find('table')
table2020 = soup2020.find('table')
table2021 = soup2021.find('table')
Rushing_table2019 = Rushing_soup2019.find('table')
Rushing_table2020 = Rushing_soup2020.find('table')
Rushing_table2021 = Rushing_soup2021.find('table')

#Use the pandas read_html method to convert the table into a dataframe object
df2019 = pd.read_html(str(table2019))[0]
df2020 = pd.read_html(str(table2020))[0]
df2021 = pd.read_html(str(table2021))[0]
Rushing_df2019 = pd.read_html(str(Rushing_table2019))[0]
Rushing_df2020 = pd.read_html(str(Rushing_table2020))[0]
Rushing_df2021 = pd.read_html(str(Rushing_table2021))[0]

#
df2019 = df2019.iloc[:, 1:]
df2020 = df2020.iloc[:, 1:]
df2021 = df2021.iloc[:, 1:]
Rushing_df2019 = Rushing_df2019.iloc[:, 1:]
Rushing_df2020 = Rushing_df2020.iloc[:, 1:]
Rushing_df2021 = Rushing_df2021.iloc[:, 1:]

#Drop the first level of each MultiIndex to make conversions easier
Rushing_df2019.columns = Rushing_df2019.columns.droplevel(level=0)
Rushing_df2020.columns = Rushing_df2020.columns.droplevel(level=0)
Rushing_df2021.columns = Rushing_df2021.columns.droplevel(level=0)

#Drop unneeded columns 
df2019 = df2019.drop(['Tm','GS','QBrec','Cmp','Att','TD%','Int%','1D','Lng','Y/A','AY/A','Y/C','Y/G',
'Sk','Yds.1','Sk%','NY/A','ANY/A','4QC','GWD'], axis=1)
df2020 = df2020.drop(['Tm','GS','QBrec','Cmp','Att','TD%','Int%','1D','Lng','Y/A','AY/A','Y/C','Y/G',
'Sk','Yds.1','Sk%','NY/A','ANY/A','4QC','GWD'], axis=1)
df2021 = df2021.drop(['Tm','GS','QBrec','Cmp','Att','TD%','Int%','1D','Lng','Y/A','AY/A','Y/C','Y/G',
'Sk','Yds.1','Sk%','NY/A','ANY/A','4QC','GWD'], axis=1)
Rushing_df2019 = Rushing_df2019.drop(['Tm','Age','Pos','G','GS','1D'], axis=1)
Rushing_df2020 = Rushing_df2020.drop(['Tm','Age','Pos','G','GS','1D'], axis=1)
Rushing_df2021 = Rushing_df2021.drop(['Tm','Age','Pos','G','GS','1D'], axis=1)

#Rename rushing columns to avoid duplicate column names
Rushing_df2019.columns = ['Player','RushAtt','RushYds','RushTD','RushLng','RushY/A','RushY/G','Fmb']
Rushing_df2020.columns = ['Player','RushAtt','RushYds','RushTD','RushLng','RushY/A','RushY/G','Fmb']
Rushing_df2021.columns = ['Player','RushAtt','RushYds','RushTD','RushLng','RushY/A','RushY/G','Fmb']

#Create a list of numeric columns
numeric_columns = ['Age','G','Cmp%','Yds','TD','Int','Rate','QBR']
Rushing_numeric_columns = ['RushAtt','RushYds','RushTD','RushLng','RushY/A','RushY/G','Fmb']

#Convert numeric columns from strings into numeric values
for i in numeric_columns:
    df2019[i] = pd.to_numeric(df2019[i], errors='coerce')
    df2020[i] = pd.to_numeric(df2020[i], errors='coerce')
    df2021[i] = pd.to_numeric(df2021[i], errors='coerce')
for i in Rushing_numeric_columns:
    Rushing_df2019[i] = pd.to_numeric(Rushing_df2019[i], errors='coerce')
    Rushing_df2020[i] = pd.to_numeric(Rushing_df2020[i], errors='coerce')
    Rushing_df2021[i] = pd.to_numeric(Rushing_df2021[i], errors='coerce')

#Merge Dataframes together to include quarterback rushing statistics 
df2019Combined = pd.merge(df2019,Rushing_df2019,how='inner',on=['Player'])
df2020Combined = pd.merge(df2020,Rushing_df2020,how='inner',on=['Player'])
df2021Combined = pd.merge(df2021,Rushing_df2021,how='inner',on=['Player'])

#Create Fantasy Points statistic 
df2019Combined['FP'] = (
    ((df2019Combined[('Yds')] * .04) + 
    (df2019Combined[('RushYds')] * .1) +
    (df2019Combined[('RushTD')] * .1) +
    (df2019Combined[('TD')] * 4) -
    (df2019Combined['Int'] * 2) - 
    (df2019Combined['Fmb'] * 2)) 
)

df2020Combined['FP'] = (
    ((df2020Combined[('Yds')] * .04) + 
    (df2020Combined[('RushYds')] * .1) +
    (df2020Combined[('RushTD')] * .1) +
    (df2020Combined[('TD')] * 4) -
    (df2020Combined['Int'] * 2) - 
    (df2020Combined['Fmb'] * 2)) 
)

df2021Combined['FP'] = (
    ((df2021Combined[('Yds')] * .04) + 
    (df2021Combined[('RushYds')] * .1) +
    (df2021Combined[('RushTD')] * 6) +
    (df2021Combined[('TD')] * 4) -
    (df2021Combined['Int'] * 2) - 
    (df2021Combined['Fmb'] * 2)) 
)

#Sort Dataframes by Fantasy Points
df2019Combined = df2019Combined.sort_values(by=['FP'], ascending=False)
df2020Combined = df2020Combined.sort_values(by=['FP'], ascending=False)
df2021Combined = df2021Combined.sort_values(by=['FP'], ascending=False)

#Create Tiers
qb_tier_1_2019 = df2019Combined[:5]
qb_tier_2_2019 = df2019Combined[5:10]
qb_tier_3_2019 = df2019Combined[10:15]
qb_tier_1_2020 = df2020Combined[:5]
qb_tier_2_2020 = df2020Combined[5:10]
qb_tier_3_2020 = df2020Combined[10:15]
qb_tier_1_2021 = df2021Combined[:5]
qb_tier_2_2021 = df2021Combined[5:10]
qb_tier_3_2021 = df2021Combined[10:15]

print(qb_tier_3_2021)