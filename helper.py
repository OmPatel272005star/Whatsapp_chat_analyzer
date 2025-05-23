from urlextract import URLExtract
import matplotlib as plt
from wordcloud import WordCloud
import  pandas as pd
from collections import Counter
import emoji

extract=URLExtract()
def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df=df[df['users']==selected_user]
    #fetch number of messages
    num_users=df.shape[0]
    #fetch total number of words
    words=[]
    for messages in df['messages']:
        words.extend(messages.split())

    #fetch number of media messages
    num_media_messages=df[df['messages']=='<Media omitted>'].shape[0]

    #fetch the no of links sharednkd
    links=[]
    for message in df['messages']:
        links.extend(extract.find_urls(message))
    return num_users,len(words),num_media_messages,len(links)

#most busy users data col1:first 5 most busy user , col2:percetage wise ciinversation
def most_busy_users(df):
    x=df['users'].value_counts().head()
    df=round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','users':'percent'})
    return x,df

def create_wordcloud(selected_user,df):
    if selected_user!='Overall':
        df=df[df['users']==selected_user]

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    wc.generate(df['messages'].str.cat(sep=" "))
    return wc

def most_common_words(selected_user,df):
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    if selected_user!='Overall':
        df=df[df['users']==selected_user]

    temp=df[df['users']!='group_notification']
    temp=temp[temp['messages']!='<Media omitted>']

    words=[]
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(5), columns=['Emoji', 'Count'])
    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        label = str(timeline['month'][i]) + "-" + str(timeline['year'][i])
        time.append(label)

    timeline['time'] = time
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()
    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    heatmap = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)
    return heatmap
