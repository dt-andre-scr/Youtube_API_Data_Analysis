
#import packages and setting up API

get_ipython().system('pip install --upgrade google-api-python-client')
from googleapiclient.discovery import build
import pandas as pd
from IPython.display import JSON
import requests
import json

api_key = 'insert_your_api_key'
api_service_name = 'youtube'
api_version = 'v3'

#Get credentials and create an API client
youtube = build(
    api_service_name, api_version, developerKey = api_key)

request = youtube.search().list(
    part="snippet",
    type="channel",
    q="Data Science",
    maxResults=50
)

#Response to get channel ids from results
response = request.execute()

#creating channel list to capture channel ids for next response and channel_titles to use for verifying data
channel_ids = []
counter = 0
channel_titles = []

for item in response['items']:
    channel_id = item['snippet']['channelId']
    channel_title = item['snippet']['title']
    channel_titles.append(channel_title)
    counter +=1
    #print(channel_title, ': ',channel_id, '- ',counter)
    channel_ids.append(channel_id)
    #print(item)
channel_ids


#Request 2 and using channel_ids list as our search
request2 = youtube.channels().list(
    part="snippet,statistics",
    id =','.join(channel_ids)
)

#Response
response2 = request2.execute()

#creating all_data list to hold all data we are going to analyze
#creating channel_checks to hold a dictionary of channel names from response2['items'] output

all_data = []
channel_checks = []

for item2 in response2['items']:
    data = {'ChannelName' : item2['snippet']['title'],
            'Subscribers' : item2['statistics']['subscriberCount'],
            'TotalViews' : item2['statistics']['viewCount'],
            'TotalVideos' : item2['statistics']['videoCount'],
            'CreationDate' : item2['snippet']['publishedAt']
        }
    channel_check = {'ChannelName' : item2['snippet']['title']}
    channel_checks.append(channel_check)
    all_data.append(data)

all_data


#creating channel_titles_check to parse out channel_checks dictionaries and capture the key from title['ChannelName'] in a list

channel_titles_check = []

for title in channel_checks:
    channel_names = (title['ChannelName'])
    channel_titles_check.append(channel_names)
channel_titles_check


#formatting data into dataframes


titles_check1 = pd.DataFrame(channel_titles) #putting channel_titles from first response output in a dataframe
titles_check2 = pd.DataFrame(channel_titles_check) #putting channel_titles_check from response2 output in a dataframe


#creating final_check dataframe by doing a left join on titles_check1 & titles_check2 on the first column..
#..to see if all results to verify response2 has an output for all correct titles from the output of the first response

final_check = pd.merge(titles_check1, titles_check2, on = [0], how = 'left')
final_check

#we confirmed that all_data contains information for all channels from the output of the first response.


#contains all the dictionaries of information of each channel from the output of the first response and is the
#..variable we will be using to start our analysis

all_data

#overwriting variable all_data and putting it into a dataframe with the same name to view data in matrix form
all_data = pd.DataFrame(all_data)
all_data

#--can check for nulls as well if you'd like


#checkpoint

all_data.dtypes


#pre-processing data, converting data types and cleaning up columns

numeric_cols = ['Subscribers', 'TotalViews', 'TotalVideos']
all_data[numeric_cols] = all_data[numeric_cols].apply(pd.to_numeric, errors = 'coerce', axis = 1)
all_data['CreationDate'] = all_data['CreationDate'].str[0:10]
all_data['CreationDate'] = pd.to_datetime(all_data['CreationDate'])

#--if doing string for 'ChannelName', might need to explicitly call astype(str) before manipulating, force the str out

all_data['ChannelAge'] = pd.Timestamp.now().normalize() - all_data['CreationDate']
all_data


#checkpoint

all_data.dtypes


#converting the number of days to an integer by chaning the data type to a str to be able to remove the
#--days text and the converting the leftover numbers into int

all_data['ChannelAgeDay'] = all_data['ChannelAge'].astype(str)
all_data['ChannelAgeDayInt'] = all_data['ChannelAgeDay'].str.split(' ').str.get(0).astype(int)

#checkpoint

all_data


#deleting not needed columns

del all_data['CreationDate']
del all_data['ChannelAge']
del all_data['ChannelAgeDay']
all_data


#finalcheck


all_data.dtypes


#exporting dataframe as csv to your chosen path


all_data.to_csv("insert_your_path")

