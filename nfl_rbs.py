import pandas as pd
from bs4 import BeautifulSoup as BS
import requests

#Assign URLS
URL2019 = 'https://www.pro-football-reference.com/years/2019/rushing.htm'
URL2020 = 'https://www.pro-football-reference.com/years/2020/rushing.htm'
URL2021 = 'https://www.pro-football-reference.com/years/2021/rushing.htm'
Receiving_URL2019 = 'https://www.pro-football-reference.com/years/2019/receiving.htm'
Receiving_URL2020 = 'https://www.pro-football-reference.com/years/2020/receiving.htm'
Receiving_URL2021 = 'https://www.pro-football-reference.com/years/2021/receiving.htm'

#Use requests module to download the HTML content from each URL
page2019 = requests.get(URL2019)
page2020 = requests.get(URL2020)
page2021 = requests.get(URL2021)
Receiving_page2019 = requests.get(Receiving_URL2019)
Receiving_page2020 = requests.get(Receiving_URL2020)
Receiving_page2021 = requests.get(Receiving_URL2021)

#Convert the HTML into a beautiful soup object
soup2019 = BS(page2019.content, 'html.parser')
soup2020 = BS(page2020.content, 'html.parser')
soup2021 = BS(page2021.content, 'html.parser')
Receiving_soup2019 = BS(Receiving_page2019.content, 'html.parser')
Receiving_soup2020 = BS(Receiving_page2020.content, 'html.parser')
Receiving_soup2021 = BS(Receiving_page2021.content, 'html.parser')

#Use the beautiful soup find method to return the table on each page
table2019 = soup2019.find('table')
table2020 = soup2020.find('table')
table2021 = soup2021.find('table')
Receiving_table2019 = Receiving_soup2019.find('table')
Receiving_table2020 = Receiving_soup2020.find('table')
Receiving_table2021 = Receiving_soup2021.find('table')

#Use the pandas read_html method to convert the table into a dataframe object
df2019 = pd.read_html(str(table2019))[0]
df2020 = pd.read_html(str(table2020))[0]
df2021 = pd.read_html(str(table2021))[0]
Receiving_df2019 = pd.read_html(str(Receiving_table2019))[0]
Receiving_df2020 = pd.read_html(str(Receiving_table2020))[0]
Receiving_df2021 = pd.read_html(str(Receiving_table2021))[0]

#
df2019 = df2019.iloc[:, 1:]
df2020 = df2020.iloc[:, 1:]
df2021 = df2021.iloc[:, 1:]
Receiving_df2019 = Receiving_df2019.iloc[:, 1:]
Receiving_df2020 = Receiving_df2020.iloc[:, 1:]
Receiving_df2021 = Receiving_df2021.iloc[:, 1:]

#Filter receiving Dataframe for only running backs
Receiving_df2019 = Receiving_df2019[(Receiving_df2019['Pos'] =='RB') |
(Receiving_df2019['Pos'] =='rb')]
Receiving_df2020 = Receiving_df2020[(Receiving_df2020['Pos'] =='RB') |
(Receiving_df2020['Pos'] =='rb')]
Receiving_df2021 = Receiving_df2021[(Receiving_df2021['Pos'] =='RB') |
(Receiving_df2021['Pos'] =='rb')]

#Drop the first level of each MultiIndex to make conversions easier
df2019.columns = df2019.columns.droplevel(level=0)
df2020.columns = df2020.columns.droplevel(level=0)
df2021.columns = df2021.columns.droplevel(level=0)

df2019 = df2019.drop(['Tm','GS','1D'], axis=1)
df2020 = df2020.drop(['Tm','GS','1D'], axis=1)
df2021 = df2021.drop(['Tm','GS','1D'], axis=1)
Receiving_df2019 = Receiving_df2019.drop(['Tm','Age','Pos','G','GS','Ctch%','Y/R','1D','Y/Tgt','R/G','Y/G','Fmb'], axis=1)
Receiving_df2020 = Receiving_df2020.drop(['Tm','Age','Pos','G','GS','Ctch%','Y/R','1D','Y/Tgt','R/G','Y/G','Fmb'], axis=1)
Receiving_df2021 = Receiving_df2021.drop(['Tm','Age','Pos','G','GS','Ctch%','Y/R','1D','Y/Tgt','R/G','Y/G','Fmb'], axis=1)

#Rename receiving columns to avoid duplicate column names
Receiving_df2019.columns = ['Player','Tgt','Rec','RecYds','RecTD','RecLng']
Receiving_df2020.columns = ['Player','Tgt','Rec','RecYds','RecTD','RecLng']
Receiving_df2021.columns = ['Player','Tgt','Rec','RecYds','RecTD','RecLng']

#Create a list of numeric columns
numeric_columns = ['Age','G','Att','Yds','TD','Lng','Y/A','Y/G','Fmb']
Receiving_numeric_columns = ['Tgt','Rec','RecYds','RecTD','RecLng']

#Convert numeric columns from strings into numeric values
for i in numeric_columns:
    df2019[i] = pd.to_numeric(df2019[i], errors='coerce')
    df2020[i] = pd.to_numeric(df2020[i], errors='coerce')
    df2021[i] = pd.to_numeric(df2021[i], errors='coerce')
for i in Receiving_numeric_columns:
    Receiving_df2019[i] = pd.to_numeric(Receiving_df2019[i], errors='coerce')
    Receiving_df2020[i] = pd.to_numeric(Receiving_df2020[i], errors='coerce')
    Receiving_df2021[i] = pd.to_numeric(Receiving_df2021[i], errors='coerce')

#Merge Dataframes together to include running back receiving statistics 
df2019Combined = pd.merge(df2019,Receiving_df2019,how='inner',on=['Player'])
df2020Combined = pd.merge(df2020,Receiving_df2020,how='inner',on=['Player'])
df2021Combined = pd.merge(df2021,Receiving_df2021,how='inner',on=['Player'])

#Create Fantasy Points statistic 
df2019Combined['Fantasy Points'] = (
    ((df2019Combined[('Yds')] * .1) + 
    (df2019Combined[('RecYds')] * .1) + 
    (df2019Combined[('RecTD')] * 6) +
    (df2019Combined[('TD')] * 6) -
    (df2019Combined['Fmb'] * 2)) 
)
df2020Combined['Fantasy Points'] = (
    ((df2020Combined[('Yds')] * .1) + 
    (df2020Combined[('RecYds')] * .1) + 
    (df2020Combined[('RecTD')] * 6) +
    (df2020Combined[('TD')] * 6) -
    (df2020Combined['Fmb'] * 2)) 
)
df2021Combined['Fantasy Points'] = (
    ((df2021Combined[('Yds')] * .1) +
    (df2021Combined[('RecYds')] * .1) + 
    (df2021Combined[('RecTD')] * 6) +
    (df2021Combined[('TD')] * 6) -
    (df2021Combined['Fmb'] * 2)) 
)

#Sort Dataframes by Fantasy Points
df2019Combined = df2019Combined.sort_values(by=['Fantasy Points'], ascending=False)
df2020Combined = df2020Combined.sort_values(by=['Fantasy Points'], ascending=False)
df2021Combined = df2021Combined.sort_values(by=['Fantasy Points'], ascending=False)

#Create Tiers
rb_tier_1_2019 = df2019Combined[:5]
rb_tier_2_2019 = df2019Combined[5:10]
rb_tier_3_2019 = df2019Combined[10:15]
rb_tier_1_2020 = df2020Combined[:5]
rb_tier_2_2020 = df2020Combined[5:10]
rb_tier_3_2020 = df2020Combined[10:15]
rb_tier_1_2021 = df2021Combined[:5]
rb_tier_2_2021 = df2021Combined[5:10]
rb_tier_3_2021 = df2021Combined[10:15]

rb_tier_1_2019.to_clipboard(excel=True)
