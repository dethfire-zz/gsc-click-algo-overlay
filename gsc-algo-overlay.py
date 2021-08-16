import streamlit as st
import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from datetime import datetime
#from matplotlib.dates import DateFormatter
#import matplotlib.dates as mdates
import numpy as np

st.set_option('deprecation.showPyplotGlobalUse', False)

st.markdown("""
<style>
.big-font {
    font-size:50px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<p class="big-font">GSC Clicks with Google Algo Overlay</p>
<p>Graph your GSC clicks data with a Google Algo overlay</p>
<p>Inspiration from: <a href="https://ipullrank.com">iPullRank</a>'s <a href="https://github.com/csliva/SEOgre/blob/main/main.py">Colt Silva</a></p>
<b>Directions: </b></ br><ol>
<li>Upload GSC performance date CSV</li>
</ol>
""", unsafe_allow_html=True)

with st.form("data"):
    gsc = st.file_uploader("Upload your GSC Date Performance CSV",type=['csv'])
    metric = st.selectbox("Select GSC Metric", ('Clicks','Impressions','CTR','Positions'))
    submitted = st.form_submit_button("Process")
    
    if submitted:
        
        gsc = pd.read_csv(gsc)
        gsc['Date'] = gsc['Date'].astype('datetime64[ns]')
        gsc['Date'] = gsc["Date"].dt.strftime('%-m/%d/%Y')
        gsc = gsc.sort_values('Date',ascending=True)

        ###### GET ALTO API

        updates = requests.get("https://ipullrank-dev.github.io/algo-worker/")
        updates_dict = json.loads(updates.text)

        google_dates =[]
        algo_notes = []
        title = []

        for x in updates_dict:
          google_dates.append(x['date'])
          algo_notes.append(x['title'])
          title.append(x['source'])

        ####### PLOT DATA
        st.title("Graph Output")
        xs = gsc['Date']
        xss = google_dates
        ys = gsc[metric]
        figure(figsize=(20, 6), dpi=80)
        plt.plot(xs,ys,'k-')
        plt.gcf().autofmt_xdate()

        algo_list = []
        for x,y in zip(xs,ys):

          label = x

          if x in google_dates:
            algo_list.append(x)
            plt.axvline(x=x, color="lightgray", linestyle="--")
            plt.plot(x,y,'ro')
            plt.xlabel("Dates")
            plt.ylabel(metric)
            plt.title("GSC "+metric+" Time Series with Algo Overlay")
            plt.annotate(label, 
                         (x,y),
                         color='white', 
                         textcoords="offset points", 
                         xytext=(0,50),
                         ha='center',
                         bbox=dict(boxstyle='square,pad=.2', fc='k', ec='none'))

        ind = np.arange(0, len(xs.index), 10)
        plt.xticks(ind, xs[::10])
        plt.show()
        st.pyplot()

        ##### PRINT ALGO LEGEND
        st.title("Relevant Algo Legend")
        for x in algo_list:
          index = google_dates.index(x)
          st.write(x + " " + algo_notes[index] +" "+ title[index])

st.write('Author: [Greg Bernhardt](https://twitter.com/GregBernhardt4) | Friends: [Rocket Clicks](https://www.rocketclicks.com) and [Physics Forums](https://www.physicsforums.com)')
