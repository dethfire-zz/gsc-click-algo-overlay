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
<p class="big-font">GSC with Google Algo Overlay</p>
<p>Graph your GSC clicks data with a Google Algo overlay</p>
<p>Inspiration from: <a href="https://ipullrank.com">iPullRank's</a> <a href="https://twitter.com/SignorColt">Colt Silva's</a> <a href="https://ipullrank.com/layered-seo-analysis-for-happy-clients">data layering guide</a></p>
<b>Directions: </b></ br><ol>
<li>Upload GSC performance date CSV. Dates.csv from the performance export zip file.</li>
</ol>
""", unsafe_allow_html=True)

with st.form("data"):
    gsc = st.file_uploader("Upload your GSC Date Performance CSV",type=['csv'])
    metric = st.selectbox("Select GSC Metric", ('Clicks','Impressions','CTR','Position'))
    submitted = st.form_submit_button("Process")
    
    if submitted:
        
        gsc = pd.read_csv(gsc)
        gsc['Date'] = gsc['Date'].astype('datetime64[ns]')
        gsc['Date'] = gsc["Date"].dt.strftime('%-m/%d/%Y')
        
        if metric == 'CTR':
            gsc['CTR'] = gsc['CTR'].str.replace('%','').astype('float')
        
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
        st.write("Hover to zoom. Top right icon.")
        xs = gsc['Date']
        xss = google_dates
        ys = gsc[metric]
        
        figure(figsize=(20, 6), dpi=80)
        plt.plot(xs,ys,'k-')
        plt.gcf().autofmt_xdate()
        plt.ticklabel_format(useOffset=False, style='plain', axis='y')
        
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
        st.title("Detected Algo Updates")
        for x in algo_list:
          index = google_dates.index(x)
          st.write(x + " " + algo_notes[index] +" "+ title[index])

st.write('Author: [Greg Bernhardt](https://twitter.com/GregBernhardt4) | Friends: [importSEM](https://importsem.com) and [Physics Forums](https://www.physicsforums.com)')
