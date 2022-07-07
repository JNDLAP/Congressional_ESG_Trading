from readline import get_begidx
import string
from token import GREATER
import numpy as np
import pandas as pd
from collections import Counter
import datetime as dt
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import pandas_datareader as web
import plotly.graph_objects as go
import requests
from bs4 import BeautifulSoup
import json
import requests
from matplotlib.collections import EllipseCollection
import altair as alt
import yfinance as yf
import datetime

st.set_page_config(
     page_title="Algo Trading",
     page_icon="",
     layout="wide"
 )
with st.sidebar:
        option =  st.sidebar.selectbox(
     'Granularity of Transaction History',
     ('Year', 'Month', 'Day'))
        less =  st.sidebar.selectbox(
        'Exaime Members with an ESG Rating of Less Than',
        (10, 20, 40))
        great =  st.sidebar.selectbox(
        'Exaime Members with an ESG Rating of Greater Than',
        (90, 80, 60))




df1 = pd.read_csv('all_transactions.csv', error_bad_lines=False)
df2 = pd.read_csv('2021-house-scorecard-grid-export.csv', error_bad_lines=False)










housestatus=df2['Lifetime Score'].mean()


esg=df2[['Member of Congress','Lifetime Score']]

df1.columns = df1.columns.str.replace('district', 'District')


    
st.header('Climate Conconsciousness and Trading Activity in the House')
st.markdown("***")

with st.expander('Why'):
    st.write(" The compliance enviromental commondities market will likely become a trillion dollar relatugated market within the next 50 years. \
        The relationship between climate focused Members and their portfolio could provide insights to their enviromental commitment. I beleived that US Representatives who voted consistently for\
             enviromental protection would have sustainable themed longterm portfolio holdings which were \
            grounded in ESG conviction. However, after combining the House's Envivromental Score-cards\
                and the Stock Watcher historical trading activity of representatives, data suggests \
             that the upper quintile of Climate/ESG rated Representatives traded in greater volume and \
            more frequently than the bottom quintile.  \
              While, much more could be research, it appears when their financial security is on the line, 'climate' Members do not rely on a long-term investment strategy."         
                )
with st.expander(' Methodology'):
    st.write(" The data from Stock Watchers aggergated trades excecuted on behlf of US Representatives. \
            The measurement of the total USD volume of trades was considered; however, the reporting criteria  \
                for trading activity requires equity positions must be reported within a speicifed USD range. \
                    In addition, many congressional members took positions on bothsides of in a particular \
                        equity market. Given that mambers only have to report within a broad range, their final position could range \
                        from a 400% increase to a complete exit, thus a total USD volume metric was deemed too noisy. Only \
                            total transactions were factored into analysis."
                )
df2['R']  = np.where(df2['Party']=='R', 1, -1 )
df2['Black']= df2['Lifetime Score'] < less
df2['Green'] = df2['Lifetime Score'] > great
housestatus=housestatus.round(2)

df1['State']=df1['District'].str[:2]
df2['State']=df2['District'].str[:2]


avg_t=df1.groupby(['State'])['transaction_date'].count()
avg_g = df2.groupby(['State'])['Lifetime Score'].mean()



state =pd.merge(avg_g, avg_t, left_index=True, right_index=True)
state['Transactions']=state['transaction_date']
df = pd.merge(df2,df1,on='District')




df['State']=df['District'].str[:2]
esg2 =df.groupby(['Member of Congress'])['transaction_date'].count()
esg =esg.groupby(['Member of Congress'])['Lifetime Score'].sum()

member = pd.merge(esg, esg2, left_index=True, right_index=True)

member['Transactions']=member['transaction_date']
st.markdown("***")
st.subheader('House Trading and ESG Data by State')
with st.expander(' Full List of States'):
    st.dataframe(state[['Transactions', 'Lifetime Score']])



text = st.text_input('Input a States Abbreviation', 'VA')

col1, col2 = st.columns(2)
df1['search'] = np.where(df1['State']==text,1,0)
search = df1.loc[df1['search']==True]
searcht =search['asset_description']



def most_frequent(searcht):
    occurence_count = Counter(searcht)
    return occurence_count.most_common(1)[0][0]
col2.metric(label = text+'s Most Frequently Traded Asset', value=most_frequent(searcht))

df2['life'] = np.where(df2['State']==text,1,0)
life = df2.loc[df2['life']==True]
life = life['Lifetime Score'] 

col1.metric(label = text+'s Lifetime Score', value=life.mean().round(2))
search['Transactions']=search['transaction_date']


search['transaction_date'] = pd.to_datetime(search['transaction_date']).dt.strftime('%m/%Y')
search['Month']  = search['transaction_date']
search['Year'] = search['disclosure_year']
search['Day'] = search['Transactions']
chart=search.groupby([option])['Transactions'].count()
st.bar_chart(chart)

st.markdown("***")

st.subheader('House Trading and ESG Data by Member')
with st.expander(' Full List of Respresentatives'):
    st.dataframe(member[['Transactions', 'Lifetime Score']])



text = st.text_input('Input a Respresentatives Name: Last, First', 'Fallon, Pat')

col1, col2 = st.columns(2)
df1['search'] = np.where(df1['State']==text,1,0)
search = df1.loc[df1['search']==True]
searcht =search['ticker']

df['search'] = np.where(df['Member of Congress']==text,1,0)
search = df.loc[df['search']==True]
searchg =search['asset_description']

def most_frequent(searchg):
    occurence_count = Counter(searchg)
    return occurence_count.most_common(1)[0][0]
col2.metric(label = text+'s Most Frequently Traded Asset', value=most_frequent(searchg))

df2['life'] = np.where(df2['Member of Congress']==text,1,0)
life = df2.loc[df2['life']==True]
life = life['Lifetime Score'] 


col1.metric(label = text+'s Lifetime Score', value=life.mean().round(2))
search['Transactions']=search['transaction_date']
search['transaction_date'] = pd.to_datetime(search['transaction_date']).dt.strftime('%m/%Y')

search['Month']  = search['transaction_date']
search['Year'] = search['disclosure_year']
search['Day'] = search['Transactions']
chart=search.groupby([option])['Transactions'].count()
st.bar_chart(chart)







df['sell'] = np.where(df['type']=='sale_full', 1, 0 )

black = df.loc[df['Black']==True]
green = df.loc[df['Green']==True]


green['disclosure_date'] = pd.to_datetime(green['disclosure_date']).dt.strftime('%m/%Y')
black['disclosure_date'] = pd.to_datetime(black['disclosure_date']).dt.strftime('%m/%Y')


green["date"] = pd.to_datetime(df["disclosure_date"])
black["date"] = pd.to_datetime(df["disclosure_date"])
green['Transaction'] = green['transaction_date']
black['Transaction'] = black['transaction_date']

# green=green[['date', 'amount', 'Transactions', 'Member of Congress']]
# black=black[['date', 'amount', 'Transactions', 'Member of Congress']]


g_count = green['Member of Congress'].nunique()
b_count = black['Member of Congress'].nunique()

black['Month']  = black['disclosure_date']
black['Year'] = black['disclosure_year']
black['Day'] = black['date']

black_sell = black.groupby([option])['sell'].sum()
black = black.groupby([option])['Transaction'].count()


green['Month']  = green['disclosure_date']
green['Year'] = green['disclosure_year']
green['Day'] = green['date']

green_sell = green.groupby([option])['sell'].sum()
green = green.groupby([option])['Transaction'].count()

black = pd.merge(black_sell, black, left_index=True, right_index=True)
black['buy'] = black['Transaction'] - black['sell']
black = black[['sell','buy']]
black['sell'] = black['sell'] * -1

green = pd.merge(green_sell, green, left_index=True, right_index=True)
green['buy'] = green['Transaction'] - green['sell']

green['sell'] = green['sell'] * -1


green= green[['sell','buy']]


st.markdown("***")

st.subheader('Trading Activity of Members with ESG Ratings Less Than ...' )
st.bar_chart(black)
black['total']=black['buy']+(black['sell']*-1)
black['total']=black['total'].cumsum()

black['buy']=black['buy'].cumsum()
black['sell']=black['sell'].cumsum()

col1, col2,col3 = st.columns(3)
col1.metric(label='Total Number of Buys', value =black['buy'].max()  )
col2.metric(label='Total Number of Sells', value =(black['sell'].min()*-1) )
col3.metric(label='Total Number of Transactions', value=black['total'].max() )




col1,col2, col3,col4 = st.columns(4)
col2.metric(label='Number of Members', value =b_count )
col3.metric(label='Buy/Sell Ratio', value = (black['buy'].max() / (black['sell'].min()*-1 )).round(2) )


st.markdown("***")

st.subheader('Trading Activity of Members with ESG Ratings Greater Than ...')
st.bar_chart(green)
green['total']=green['buy']+(green['sell']*-1)
green['total']=green['total'].cumsum()



green['buy']= green['buy'].cumsum()
green['sell']= green['sell'].cumsum()
col1, col2,col3 = st.columns(3)
col1.metric(label='Total Number of Buys', value =green['buy'].max()  )
col2.metric(label='Total Number of Sells', value =(green['sell'].min()*-1) )
col3.metric(label='Total Number of Transactions', value =green['total'].max())




col1,col2, col3,col4 = st.columns(4)

col2.metric(label='Number of Members', value =g_count )
col3.metric(label='Buy/Sell Ratio', value = (green['buy'].max() / (green['sell'].min()*-1 )).round(2) )

st.markdown("***")

with st.expander('Findings'):
    st.write(" Portfolio trading activity mirrors modern liberal and conservative tendencies. In addition, there was a distinct spike in trading activity at the begining of covid. \
            This uptick was most pronounced in the bottom Quintile, possibly indictating\
                conservatives serve as better signals for capital preservation oppertunities."
                )
with st.expander('Moving Forward'):
    st.write(" Further research should be done to investigate sector speific activity within these reported trades. \
            While many Members do not directly control their portfolio, they are still are still human. Cross-referencing these positions with committee hearings could provide unique insights.\
                "
                )