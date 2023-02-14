import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector
import json
import numpy as np
import pandas as pd
import plotly.express as px
import babel.numbers
import folium
from streamlit_folium import folium_static
import plotly.graph_objects as go
from sqlite3 import connect

conn = connect("PhonePE.db")
cursor = conn.cursor()
#inital side bar creation for filter

st.sidebar.title('Filter')

# Add a selectbox to the sidebar:
user_ip1 = st.sidebar.selectbox(
    'Select Anyone All India or State',
    ('ALL INDIA',"STATE WISE"))

if(user_ip1 =='ALL INDIA'):
# Add a selectbox to the sidebar:
    trans_r_user = st.sidebar.selectbox(
    'Transaction or User Details',
    ('TRANSACTIONS','USER')
    )

# Add a dropdown to the sidebar:
    Year = st.sidebar.selectbox(
    'YEAR',
    ('2018','2019','2020','2021','2022')
)

# Add a selectbox to the sidebar:
    Quater = st.sidebar.radio(
    'QUATER',
    ('Q1','Q2','Q3','Q4')
    )

else:
 
# Add a selectbox to the sidebar:
    state = st.sidebar.selectbox(
    'Select State Name:',
    (
 'Andhra pradesh',
 'Arunachal pradesh',
 'Assam',
 'Bihar',
 'Chandigarh',
 'Chhattisgarh',
 'Delhi',
 'Goa',
 'Gujarat',
 'Haryana',
 'Himachal pradesh',

 'Jharkhand',
 'Karnataka',
 'Kerala',
 'Ladakh',
 'Lakshadweep',
 'Madhya pradesh',
 'Maharashtra',
 'Manipur',
 'Meghalaya',
 'Mizoram',
 'Nagaland',
 'Odisha',
 'Puducherry',
 'Punjab',
 'Rajasthan',
 'Sikkim',
 'Tamil nadu',
 'Telangana',
 'Tripura',
 'Uttar pradesh',
 'Uttarakhand',
 'West bengal')
    )
# Add a selectbox to the sidebar:
    trans_r_user = st.sidebar.selectbox(
    'Transaction or User Details',
    ('TRANSACTIONS','USER')
    )
# Add a dropdown to the sidebar:
    Year = st.sidebar.selectbox(
    'YEAR',
    ('2018','2019','2020','2021','2022')
)

# Add a selectbox to the sidebar:
    Quater = st.sidebar.radio(
    'QUATER',
    ('Q1','Q2','Q3','Q4')
    )




st.title('PHONEPE DASHBOARD')

#getting the data from the GITHUB to load
MAP_TRANS_AGG_INDIA = pd.read_csv("https://raw.githubusercontent.com/JaniceLibbyThomas/PhonePe/Master/MAP_TRANS_AGG_INDIA.csv")
MAP_TRANS_AGG_STATE= pd.read_csv("https://raw.githubusercontent.com/JaniceLibbyThomas/PhonePe/Master/MAP_TRANS_AGG_STATE.csv")
MAP_USER_AGG_INDIA= pd.read_csv("https://raw.githubusercontent.com/JaniceLibbyThomas/PhonePe/Master/MAP_USER_AGG_INDIA.csv")
MAP_USER_AGG_STATE= pd.read_csv("https://raw.githubusercontent.com/JaniceLibbyThomas/PhonePe/Master/MAP_USER_AGG_STATE.csv")

HOVER_TRANS_AGG_INDIA= pd.read_csv("https://raw.githubusercontent.com/JaniceLibbyThomas/PhonePe/Master/HOVER_TRANS_AGG_INDIA.csv")
HOVER_TRANS_AGG_STATE= pd.read_csv("https://raw.githubusercontent.com/JaniceLibbyThomas/PhonePe/Master/HOVER_TRANS_AGG_STATE.csv")
HOVER_USER_STATE= pd.read_csv("https://raw.githubusercontent.com/JaniceLibbyThomas/PhonePe/Master/HOVER_USER_STATE.csv")
HOVER_USER_DISTRICT= pd.read_csv("https://raw.githubusercontent.com/JaniceLibbyThomas/PhonePe/Master/HOVER_USER_DISTRICT.csv")

TOP_TRANS_AGG_INDIA= pd.read_csv("https://raw.githubusercontent.com/JaniceLibbyThomas/PhonePe/Master/TOP_TRANS_AGG_INDIA%20.csv")
TOP_TRANS_AGG_STATE= pd.read_csv("https://raw.githubusercontent.com/JaniceLibbyThomas/PhonePe/Master/TOP_TRANS_AGG_STATE.csv")
TOP_USER_STATE= pd.read_csv("https://raw.githubusercontent.com/JaniceLibbyThomas/PhonePe/Master/TOP_USER_STATE.csv")
TOP_USER_DIST= pd.read_csv("https://raw.githubusercontent.com/JaniceLibbyThomas/PhonePe/Master/TOP_USER_DIST.csv")

count =0
#Fetching the Data from the SQL and saving it as DataFrame


if(user_ip1 =='ALL INDIA'):

    if(trans_r_user =='TRANSACTIONS'):
      tab1, tab2, tab3 = st.tabs(["TRANSACTION DETAILS", "TOP 10", "MAP"])
      
      Frame1 = pd.read_sql(f"SELECT Name,Count,Amount FROM MAP_TRANS_AGG_INDIA where Year = '{Year}' and Quater = '{Quater}'",conn)
      Frame1.rename(columns={"Name": "Type_of_Transaction"}, inplace=True)
      
      for i in range(0,len(list(Frame1['Amount']))):
            t = str(Frame1['Amount'][i]).split('.')
            Frame1['Amount'][i] = t[0]
      Frame1['Amount'] = Frame1['Amount'].astype(int)

      with tab1:
      #Total Online Transaction details
          st.subheader('TRANSACTIONS')
          container1 = st.container()

          sum_count = list(Frame1['Count'])
          amt_sum = list(Frame1['Amount'])
      
          a = sum(sum_count)
          b = round(sum(amt_sum)/10000000)
          c = round(sum(amt_sum)/(sum(sum_count)))
          D = str(babel.numbers.format_currency(b, "INR", locale='en_US'))
          new = D.split('.')
          st.metric(label=f'All PhonePe transactions (UPI + Cards + Wallets)', value=a,
                delta_color="inverse")

          st.metric(label=f"Total payment value in ₹",value =(new[0]+' Cr') ,
                delta_color="inverse")

          st.metric(label=f"Avg. transaction value in ₹", value=babel.numbers.format_currency(c, "INR", locale='en_US'),
                delta_color="inverse")

          #categories - data
          st.subheader('Categories'.upper())
          

          l1 = []
          l2 = []
          for i in range(0,len(list(Frame1['Type_of_Transaction']))):
                l1.append([Frame1['Type_of_Transaction'][i]])
                l2.append(int(Frame1['Count'][i]))

          chart_data = pd.DataFrame(l1,columns=['Type of Transaction'])
          chart_data['Amount of Transaction'] = l2

        #  chart_data = chart_data.set_index('Type of Transaction')

          

          st.bar_chart(chart_data,x="Type of Transaction", y="Amount of Transaction", width=500, height=500)




      with tab2:
        #Top 10: State, District and Pincode
          
          radio = st.radio('Select Any One ',['State','District','Pincode'])
          st.subheader(f'Top 10 Transactions Based on {radio}')
          if(radio == 'State'):
            Frame2 = pd.read_sql(f"SELECT * FROM TOP_TRANS_AGG_INDIA_State where Year = '{Year}' and Quater = '{Quater}'",conn)
            Frame2.rename(columns={"State name": "State_name"}, inplace=True)
            temp = Frame2.groupby(['State_name'])['Amount','Count'].sum()
#             temp.to_csv(f'/Users/joelsanthoshraja/Downloads/temp_{file_no}.csv')
            Frame3  = temp.reset_index()
            Frame3.sort_values(by="Count",ascending=False)
            st.line_chart(Frame3, x = 'State_name',y ='Count')
          
            file_no +=1
            
          elif(radio =='Pincode'):
            Frame2 = pd.read_sql(f"SELECT * FROM TOP_TRANS_AGG_INDIA_dist_pincode1 where Year = '{Year}' and Quater = '{Quater}'",conn)
            temp = Frame2.groupby(['Pincode'])['Count'].sum()
            Frame3 = temp.reset_index()
            Frame3 = Frame3.sort_values(by="Count",ascending=False)          
            val = (Frame3.iloc[0:10].reset_index().drop(['index'],axis=1))
            val['Pincode'] = val['Pincode'].astype(str)
            st.line_chart(val,x ='Pincode',y ='Count')
            file_no +=1
          else:
            Frame2 = pd.read_sql(f"SELECT * FROM TOP_TRANS_AGG_dist1 where Year = '{Year}' and Quater = '{Quater}'",conn)
            Frame2.rename(columns={"District": "District Name"}, inplace=True)
            temp = Frame2.groupby(['District Name'])['Count'].sum()           
            Frame3 = temp.reset_index()
            Frame3 = Frame3.sort_values(by="Count",ascending=False)
            val = (Frame3.iloc[0:10].reset_index().drop(['index'],axis=1))
            
            st.line_chart(val,x ='District Name',y ='Count')
            file_no +=1

      with tab3:
            Map_ip = st.selectbox(
                'Select Anyone',
                ("Count",'Amount'))
            Frame2 = pd.read_sql(f"SELECT * FROM HOVER_TRANS_AGG_INDIA where Year = '{Year}' and Quater = '{Quater}'",conn)
            Frame2.rename(columns={"State_name": "State Name",'id':'Map_id'}, inplace=True)    

            for i in range(0,len(list(Frame2['Amount']))):
                 t = (Frame2['Amount'][i]).split('.')
                 Frame2['Amount'][i] = t[0]
            Frame2['Amount'] = Frame2['Amount'].astype(int)

            india_states = json.load(open("https://raw.githubusercontent.com/JaniceLibbyThomas/PhonePe/Master/states_india.geojson", "r"))
                

            
            if(Map_ip =='Amount'):
                Frame2['Log_Amount']= np.log2(Frame2['Amount'])
                Map_ip = 'Log_Amount'
              
            fig = px.choropleth_mapbox(Frame2, geojson=india_states, color=Map_ip,
                    locations="State Name", featureidkey="properties.st_nm",
                    hover_data=["Amount"],
                    mapbox_style="carto-positron",
                    center={"lat": 24, "lon": 78},zoom = 3, opacity = 0.5

                   )
            
            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig)


    else:

        if(trans_r_user =='USER'):
          tab1, tab2, tab3 = st.tabs(["USER DETAILS", "TOP 10", "MAP"])
          
          with tab1:
      #Total Online User details
              st.subheader('USERS')
              container1 = st.container()

              Frame1 = pd.read_sql(f"SELECT * FROM MAP_USER_AGG_INDIA where Year = '{Year}' and Quater = '{Quater}'",conn)
              Frame1.rename(columns={"AppOpens": "App_Opens"}, inplace=True)             
              a = Frame1['No of Registered User'][0]
            
              if(str(Frame1['App_Opens'][0]) == '0'):
                  b = 'Unavailable'
              else:
                  b = Frame1['App_Opens'][0]


              st.metric(label=f'Registered PhonePe users till {Quater} {Year}', value=a,
                delta_color="inverse")

              st.metric(label=f"PhonePe app opens in {Quater} {Year}", value=b,
                delta_color="inverse")
              

          with tab2:
        #Top 10: State, District and Pincode
          
              radio = st.radio('Select Any One ',['State','District','Pincode'])
              st.subheader(f'Top 10 Amount of Registered User Based on {radio}')
              if(radio == 'State'):
                Frame2 = pd.read_sql(f"SELECT * FROM TOP_User_AGG_state where Year = '{Year}' and Quater = '{Quater}'",conn)
                Frame2.rename(columns={"State name": "State Name",'No of Registered User':'No of reg user'}, inplace=True)
                temp = Frame2.groupby(['State Name'])['No of reg user'].sum()              
                Frame3 = temp.reset_index()
                Frame3 = Frame3.sort_values(by="No of reg user",ascending=False)
                st.line_chart(Frame3, x = 'State Name',y ='No of reg user')
            

              elif(radio =='District'):
                
                Frame2 = pd.read_sql(f"SELECT * FROM TOP_User_AGG_dist1 where Year = '{Year}' and Quater = '{Quater}'",conn)
                Frame2.rename(columns={"District": "District Name",'No of Registered User':'No Of Registered User'}, inplace=True)
                Frame2['No Of Registered User'] = Frame2['No Of Registered User'].astype(int)
                temp = Frame2.groupby(['District Name'])['No Of Registered User'].sum()
                data = dict(temp)
                df = pd.DataFrame.from_dict([data]).T
                df = df.reset_index()
                df = df.sort_values(by=0,ascending=False)
                df.rename(columns={"index": "District Name",0:'No of Registered User'}, inplace=True)
                val = (df.iloc[0:10].reset_index().drop(['index'],axis=1))
                st.line_chart(val, x = 'District Name',y ='No of Registered User')                      

              else:
                Frame2 = pd.read_sql(f"SELECT * FROM TOP_User_dist_pincode1 where Year = '{Year}' and Quater = '{Quater}'",conn)
                Frame2.rename(columns={'No of Registered User':'No Of Registered User'}, inplace=True)

                Frame2['No Of Registered User'] = Frame2['No Of Registered User'].astype(int)
                temp = Frame2.groupby(['Pincode'])['No Of Registered User'].sum()
                data = dict(temp)
                df = pd.DataFrame.from_dict([data]).T
                df = df.reset_index()
                df = df.sort_values(by=0,ascending=False)
                df.rename(columns={"index": "Pincode",0:'No of Registered User'}, inplace=True)
                         
                val = (df.iloc[0:10].reset_index().drop(['index'],axis=1))
                val['Pincode'] = val['Pincode'].astype(str)
                st.line_chart(val,x ='Pincode',y ='No of Registered User')

          with tab3:
            
                Map_ip = st.selectbox(
                'Select Anyone',
                ('No of Registered User',"No of App Open"))
                
                india_states = json.load(open("https://raw.githubusercontent.com/JaniceLibbyThomas/PhonePe/Master/states_india.geojson", "r"))
                Frame2 = pd.read_sql(f"SELECT * FROM HOVER_USER_STATE where Year = '{Year}' and Quater = '{Quater}'",conn)
                Frame2.rename(columns={'Statename':'State Name','NoofRegisteredUser':'No of Registered User','AppOpens':'No of App Open','id':'Map_id'}, inplace=True)
            
                fig = px.choropleth_mapbox(Frame2, geojson=india_states, color=Map_ip,
                    locations="State Name", featureidkey="properties.st_nm",
                    hover_data=[Map_ip],
                    mapbox_style="carto-positron",
                    center={"lat": 24, "lon": 78},zoom = 3, opacity = 0.5

                   )
            
                fig.update_geos(fitbounds="locations", visible=False)
                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                st.plotly_chart(fig)
