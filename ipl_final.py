import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt


DATA_URL1 = (
    "deliveries.csv"
)

DATA_URL2 = (
    "matches.csv"
)

DATA_URL3 = (
    "most_runs_average_strikerate.csv"
)

st.title("Indian Premier League Stats")

@st.cache(persist=True)
def load_data(p):
    data = pd.read_csv(p)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    return data

def loadrows(p,nrows):
    data = pd.read_csv(p , nrows = nrows)
    return data

ball_by_ball_data = load_data(DATA_URL1)

matches_data = load_data(DATA_URL2)

batsman_data =load_data(DATA_URL3)

if st.checkbox("Matches Data", False):
    st.subheader('Matches Data')
    st.write(matches_data)

#if st.checkbox("Ball by Ball  Data", False):
    #st.subheader('Ball by Ball Data')
    #st.write(ball_by_ball_data)
teams   =  matches_data.team1.unique()
##Team Stats
seasons=matches_data.season.unique()
l=list(seasons)
l.sort()
l.append('Overall')
st.header("Team Stats")
team   = st.selectbox('Select Team', teams)
select = st.selectbox('Select Season', l)

data =  matches_data.loc[matches_data['team1']==team]
data2 = matches_data.loc[matches_data['team2']==team]
data = pd.concat([data,data2], ignore_index=True)
if select!='Overall':
    data = data.loc[data['season']==select ]
if len(data)==0:
    st.write('No matches played by',team, 'in season ',select)
else:
    x=data['winner'].value_counts()
    st.write('Matches Played :', len(data))
    st.write('Won :',x[team])
    nr=0
    if 'No Result' in x:
        nr=x['No Result']
        lost= len(data)-x[team]-nr
        st.write('Lost :',lost)
        st.write('No result :',nr)
    else:
        lost= len(data)-x[team]-nr
        st.write('Lost :',lost)



#Head to Head
st.header("Head to Head")
select1 = st.selectbox('Team 1', teams)
select2 = st.selectbox('Team 2', teams)
if select1==select2:
    st.write('Teams should not be same')
else:
    matches= matches_data.loc[matches_data['team1']==select1]
    matches1= matches.loc[matches['team2']==select2]
    t=select1
    select1=select2
    select2=t
    matches2=matches_data.loc[matches_data['team1']==select1]
    matches2=matches2.loc[matches2['team2']==select2]
    if len(matches1)==0 and len(matches2)==0:
        st.write('No matches played between these two teams')
    else:
        matches1.append(matches2,ignore_index=True)
        ans=pd.concat([matches1,matches2],axis=0)
        y=ans['winner'].value_counts()
        st.write('Mathes Played :',len(ans))
        if select2 not in y:
            y[select2]=0
        if select1 not in y:
            y[select1]=0
        st.write(y[select2],'   :   ',y[select1])
        if 'No Result' in y:
            st.write('No result :','  ',y['No Result'])


#Leading Run_Scorers
st.header("Top Run Scorers")
select  =  st.slider("Select number of top Run Scorers", 1, 100 )
st.markdown("Top %i Run Scorers" % (select))
ans  =  loadrows(DATA_URL3,select)
st.write(ans)




#Man of the matches
st.header('Top 10 Man Of the Match Players')
select = st.selectbox('Select season',l)
if select=='Overall':
    ans=matches_data['player_of_match'].value_counts()[:10]
else:
    matches=matches_data.loc[matches_data['season']==select]
    ans=matches['player_of_match'].value_counts()[:10]
st.write(ans)


# Most Wicket Holders
st.header('Top Wicket Holders')
select  =  st.slider("Select number of top Wicket Takers", 1, 100 )
q= ball_by_ball_data.dropna(subset=['dismissal_kind'])

q= q.loc[q.dismissal_kind!= 'run out']
q= q.loc[q.dismissal_kind!= 'retired hurt']
ans= q['bowler'].value_counts()[:select]
Rank =np.arange(1,select+1)
st.write(ans)
