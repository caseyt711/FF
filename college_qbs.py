from types import NoneType
import pandas as pd
from bs4 import BeautifulSoup as BS
import requests
import re
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, MiniBatchKMeans

#Assign URLS
URL2016 = 'https://www.sports-reference.com/cfb/years/2016-passing.html'
URL2017 = 'https://www.sports-reference.com/cfb/years/2017-passing.html'
URL2018 = 'https://www.sports-reference.com/cfb/years/2018-passing.html'
URL2019 = 'https://www.sports-reference.com/cfb/years/2019-passing.html'
URL2020 = 'https://www.sports-reference.com/cfb/years/2020-passing.html'
URL2021 = 'https://www.sports-reference.com/cfb/years/2021-passing.html'

#Use requests module to download the HTML content from each URL
page2016 = requests.get(URL2016)
page2017 = requests.get(URL2017)
page2018 = requests.get(URL2018)
page2019 = requests.get(URL2019)
page2020 = requests.get(URL2020)
page2021 = requests.get(URL2021)

#Convert the HTML into a beautiful soup object
soup2016 = BS(page2016.content, 'html.parser')
soup2017 = BS(page2017.content, 'html.parser')
soup2018 = BS(page2018.content, 'html.parser')
soup2019 = BS(page2019.content, 'html.parser')
soup2020 = BS(page2020.content, 'html.parser')
soup2021 = BS(page2021.content, 'html.parser')

#Use the beautiful soup find method to return the table on each page
table2016 = soup2016.find('table')
table2017 = soup2017.find('table')
table2018 = soup2018.find('table')
table2019 = soup2019.find('table')
table2020 = soup2020.find('table')
table2021 = soup2021.find('table')

#Use the pandas read_html method to convert the table into a dataframe object
df2016 = pd.read_html(str(table2016))[0]
df2017 = pd.read_html(str(table2017))[0]
df2018 = pd.read_html(str(table2018))[0]
df2019 = pd.read_html(str(table2019))[0]
df2020 = pd.read_html(str(table2020))[0]
df2021 = pd.read_html(str(table2021))[0]

#
df2016 = df2016.iloc[:, 1:]
df2017 = df2017.iloc[:, 1:]
df2018 = df2018.iloc[:, 1:]
df2019 = df2019.iloc[:, 1:]
df2020 = df2020.iloc[:, 1:]
df2021 = df2021.iloc[:, 1:]

#Drop the first level of each MultiIndex to make conversions easier
df2016.columns = df2016.columns.droplevel(level=0)
df2017.columns = df2017.columns.droplevel(level=0)
df2018.columns = df2018.columns.droplevel(level=0)
df2019.columns = df2019.columns.droplevel(level=0)
df2020.columns = df2020.columns.droplevel(level=0)
df2021.columns = df2021.columns.droplevel(level=0)

df2016.columns = ['Player','School','Conf','G','Cmp','Att','Pct','Yds','Y/A','AY/A','TD','Int','Rate','RushAtt',
'RushYds','AvgRush','RushTD']
df2017.columns = ['Player','School','Conf','G','Cmp','Att','Pct','Yds','Y/A','AY/A','TD','Int','Rate','RushAtt',
'RushYds','AvgRush','RushTD']
df2018.columns = ['Player','School','Conf','G','Cmp','Att','Pct','Yds','Y/A','AY/A','TD','Int','Rate','RushAtt',
'RushYds','AvgRush','RushTD']
df2019.columns = ['Player','School','Conf','G','Cmp','Att','Pct','Yds','Y/A','AY/A','TD','Int','Rate','RushAtt',
'RushYds','AvgRush','RushTD']
df2020.columns = ['Player','School','Conf','G','Cmp','Att','Pct','Yds','Y/A','AY/A','TD','Int','Rate','RushAtt',
'RushYds','AvgRush','RushTD']
df2021.columns = ['Player','School','Conf','G','Cmp','Att','Pct','Yds','Y/A','AY/A','TD','Int','Rate','RushAtt',
'RushYds','AvgRush','RushTD']

#Create a list of numeric columns
numeric_columns = ['G','Cmp','Att','Pct','Yds','Y/A','AY/A','TD','Int','Rate','RushAtt',
'RushYds','AvgRush','RushTD']

#Convert numeric columns from strings into numeric values
for i in numeric_columns:
    df2016[i] = pd.to_numeric(df2016[i], errors='coerce')
    df2017[i] = pd.to_numeric(df2017[i], errors='coerce')
    df2018[i] = pd.to_numeric(df2018[i], errors='coerce')
    df2019[i] = pd.to_numeric(df2019[i], errors='coerce')
    df2020[i] = pd.to_numeric(df2020[i], errors='coerce')
    df2021[i] = pd.to_numeric(df2021[i], errors='coerce')

#Create empty Dataframes that will be filled with filtered data 
tier_1_2016 = pd.DataFrame(columns = df2016.columns)
tier_2_2016 = pd.DataFrame(columns = df2016.columns)
tier_3_2016 = pd.DataFrame(columns = df2016.columns)
tier_1_2017 = pd.DataFrame(columns = df2017.columns)
tier_2_2017 = pd.DataFrame(columns = df2017.columns)
tier_3_2017 = pd.DataFrame(columns = df2017.columns)
tier_1_2018 = pd.DataFrame(columns = df2018.columns)
tier_2_2018 = pd.DataFrame(columns = df2018.columns)
tier_3_2018 = pd.DataFrame(columns = df2018.columns)
tier_1_2019 = pd.DataFrame(columns = df2019.columns)
tier_2_2019 = pd.DataFrame(columns = df2019.columns)
tier_3_2019 = pd.DataFrame(columns = df2019.columns)
tier_1_2020 = pd.DataFrame(columns = df2020.columns)
tier_2_2020 = pd.DataFrame(columns = df2020.columns)
tier_3_2020 = pd.DataFrame(columns = df2020.columns)

#Create lists that include players that have achieved a fantasy finish in a specific tier in the NFL
nfl_tier_1 = ['Lamar Jackson*', 'Dak Prescott', 'Russell Wilson*', 'Jameis Winston', 'Patrick Mahomes', 'Aaron Rodgers*+', 
'Deshaun Watson*', 'Josh Allen*', 'Tom Brady*', 'Justin Herbert*']
nfl_tier_2 = ['Matt Ryan', 'Kyler Murray*', 'Carson Wentz', 'Ryan Tannehill', 'Kirk Cousins', 'Matthew Stafford',
 'Joe Burrow*', 'Jalen Hurts*']
nfl_tier_3 = ['Jimmy Garoppolo', 'Jared Goff', 'Derek Carr', 'Philip Rivers', 'Ben Roethlisberger']

tier_1_2016 = df2016[df2016['Player'].isin(nfl_tier_1)]
tier_2_2016 = df2016[df2016['Player'].isin(nfl_tier_2)]
tier_3_2016 = df2016[df2016['Player'].isin(nfl_tier_3)]
tier_1_2017 = df2017[df2017['Player'].isin(nfl_tier_1)]
tier_2_2017 = df2017[df2017['Player'].isin(nfl_tier_2)]
tier_3_2017 = df2017[df2017['Player'].isin(nfl_tier_3)]
tier_1_2018 = df2018[df2018['Player'].isin(nfl_tier_1)]
tier_2_2018 = df2018[df2018['Player'].isin(nfl_tier_2)]
tier_3_2018 = df2018[df2018['Player'].isin(nfl_tier_3)]
tier_1_2019 = df2019[df2019['Player'].isin(nfl_tier_1)]
tier_2_2019 = df2019[df2019['Player'].isin(nfl_tier_2)]
tier_3_2019 = df2019[df2019['Player'].isin(nfl_tier_3)]
tier_1_2020 = df2020[df2020['Player'].isin(nfl_tier_1)]
tier_2_2020 = df2020[df2020['Player'].isin(nfl_tier_2)]
tier_3_2020 = df2020[df2020['Player'].isin(nfl_tier_3)]

df2021_list = [df2021,tier_1_2016,tier_1_2017,tier_1_2018,tier_1_2019,tier_1_2020]
df2021_combined = pd.concat(df2021_list)

df2021_combined = df2021_combined.groupby('Player').mean().round(0).reset_index()
df2021_combined = df2021_combined.sort_values(by=['Yds'], ascending=False)
df2021_combined = df2021_combined.drop(89)

#Create new dataframe with the column statistics that seperate top fantasy players and average college players
inertia_scores = []
new_df = df2021_combined[['Cmp','Att','Pct','Yds','TD','Rate','RushYds','RushTD']]

for test_k in sorted(set(np.random.randint(2,100,20))):
    
    tmp_model = MiniBatchKMeans(
        n_clusters=test_k,  
        n_init=16, max_iter=2048, tol=0.5, reassignment_ratio=0.5,
        batch_size = 3072
    )
    tmp_model.fit(new_df)
    
    score = tmp_model.inertia_
    inertia_scores.append((test_k, score))

inertia_df = pd.DataFrame(inertia_scores, columns=["k", "score"])

#Plot for elbow method
fig = plt.figure(figsize=(16,9))
ax = fig.add_subplot(1,1,1)

inertia_df.sort_values(by="k").plot("k", "score", ax=ax)

ax.set_ylabel("Inertia")

#Create 20 clusters after using elbow method
model = KMeans(n_clusters=20)
model.fit(new_df)
new_df['cluster'] = model.labels_
plt.scatter(new_df['RushYds'], new_df['RushTD'], c=new_df['cluster'])


new_df['Player'] = df2021_combined['Player'].values

print(df2021_combined)

