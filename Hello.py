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

india_states = json.load(open("/Users/joelsanthoshraja/Downloads/states_india.geojson", "r"))
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

fun_has_run = False
#Fetching the Data from the SQL and saving it as DataFrame
def uploading_into_Database():
    
    global fun_has_run
    if fun_has_run:
        return

    fun_has_run = True
    #changes made for table1
    MAP_TRANS_AGG_INDIA['Name'] = MAP_TRANS_AGG_INDIA['Name'].str.replace("&","and")
    MAP_TRANS_AGG_INDIA['Name'] = MAP_TRANS_AGG_INDIA['Name'].str.replace("-"," ")
    if(len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='MAP_TRANS_AGG_INDIA';").fetchall()) == 0):
        MAP_TRANS_AGG_INDIA.to_sql("MAP_TRANS_AGG_INDIA",conn)
    
    
    #changes made for table 2
    MAP_TRANS_AGG_STATE['Name'] = MAP_TRANS_AGG_STATE['Name'].str.replace("&","and")
    MAP_TRANS_AGG_STATE['Name'] = MAP_TRANS_AGG_STATE['Name'].str.replace("-"," ")
    MAP_TRANS_AGG_STATE['State'] = MAP_TRANS_AGG_STATE['State'].str.replace("&","and")
    MAP_TRANS_AGG_STATE['State'] = MAP_TRANS_AGG_STATE['State'].str.replace("-"," ")
    if(len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='MAP_TRANS_AGG_STATE';").fetchall()) ==0):
        MAP_TRANS_AGG_STATE.to_sql("MAP_TRANS_AGG_STATE",conn)
      
    #table3:
    if(len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='MAP_USER_AGG_INDIA';").fetchall()) ==0):
    
        MAP_USER_AGG_INDIA.to_sql('MAP_USER_AGG_INDIA',conn)
    
    #changes made for table 4
    MAP_USER_AGG_STATE['State'] = MAP_USER_AGG_STATE['State'].str.replace("&","and")
    MAP_USER_AGG_STATE['State'] = MAP_USER_AGG_STATE['State'].str.replace("-"," ")
    if(len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='MAP_USER_AGG_STATE';").fetchall()) ==0):
        MAP_USER_AGG_STATE.to_sql('MAP_USER_AGG_STATE',conn)
        
   
    #changes for table 5
    HOVER_TRANS_AGG_INDIA['State_name'] = HOVER_TRANS_AGG_INDIA['State_name'].str.replace("&","and")
    HOVER_TRANS_AGG_INDIA['State_name'] = HOVER_TRANS_AGG_INDIA['State_name'].str.replace("-"," ")
    
    
    df = pd.read_csv("https://raw.githubusercontent.com/JaniceLibbyThomas/PhonePe/Master/HOVER_TRANS_AGG_INDIA.csv")
    state_li = []
    for i in range (0,len(df['State_name'])):
        state_li.append(str(df['State_name'][i].capitalize()))
    df['State_name'] = state_li
    
    state_id_map = {}
    for feature in india_states["features"]:
        feature["id"] = feature["properties"]["state_code"]
        state_id_map[feature["properties"]["st_nm"]] = feature["id"]
        
    n_state_id_map = {}
    value_key = state_id_map.keys()
    value_li = state_id_map.values()
    for i in range(0,len(state_id_map)):
        a = str(list(value_key)[i]).capitalize()
        if(a == 'Andaman & nicobar island'):
            n_state_id_map['Andaman & nicobar islands'] = list(value_li)[i]
        elif(a == 'Dadara & nagar havelli'):
            n_state_id_map['Dadra & nagar haveli & daman & diu'] = list(value_li)[i]
        elif(a == 'Nct of delhi'):   
            n_state_id_map['Delhi'] = list(value_li)[i]
        elif(a == 'Arunanchal pradesh'):
            n_state_id_map['Arunachal pradesh'] = list(value_li)[i]
        else:
            n_state_id_map[(list(value_key)[i]).capitalize()] = list(value_li)[i]

    n_state_id_map['Ladakh'] = 1
    df['id'] = df['State_name'].apply(lambda x: n_state_id_map[x])
    df1 = df.groupby(['State_name','Year','Quater','id'])['Count','Amount'].mean()
    hover_india = df1.reset_index()
    
    if(len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='HOVER_TRANS_AGG_INDIA';").fetchall()) ==0):
    
        hover_india.to_sql('HOVER_TRANS_AGG_INDIA',conn)
 
    
    #table 6
    HOVER_TRANS_AGG_STATE['District'] = HOVER_TRANS_AGG_STATE['District'].str.replace("district","")
    
    df = pd.read_csv("https://raw.githubusercontent.com/JaniceLibbyThomas/PhonePe/Master/HOVER_TRANS_AGG_STATE.csv")
    state_li = []
    for i in range (0,len(df['state'])):
        state_li.append(str(df['state'][i].replace('-',' ').capitalize()))
    df['state'] = state_li
    
    df['id'] = df['state'].apply(lambda x: n_state_id_map[x])
    df1_1 = df.groupby(['state','Year','Quater','id'])['Count','Amount'].mean()
    hover_state = df1_1.reset_index()
    if(len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='HOVER_TRANS_AGG_STATE';").fetchall()) ==0):
    
        hover_state.to_sql('HOVER_TRANS_AGG_STATE',conn)

    
    #table 7:
    HOVER_USER_STATE['Statename'] = HOVER_USER_STATE['Statename'].str.replace("&","and")
    HOVER_USER_STATE['Statename'] = HOVER_USER_STATE['Statename'].str.replace("-"," ")
    
    df = pd.read_csv("https://raw.githubusercontent.com/JaniceLibbyThomas/PhonePe/Master/HOVER_USER_STATE.csv")
    state_li = []
    for i in range (0,len(df['Statename'])):
        state_li.append(str(df['Statename'][i].replace('-',' ').capitalize()))
    df['Statename'] = state_li
    
    df['id'] = df['Statename'].apply(lambda x: n_state_id_map[x])
    df1_2 = df.groupby(['Statename','Year','Quater','id'])['NoofRegisteredUser','AppOpens'].mean()
    hover_u_state = df1_2.reset_index()
    
    if(len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='HOVER_USER_STATE';").fetchall()) ==0):
    
        hover_u_state.to_sql('HOVER_USER_STATE',conn)
 
    
    #table 8:
    HOVER_USER_DISTRICT['State Name'] = HOVER_USER_DISTRICT['State Name'].str.replace("&","and")
    HOVER_USER_DISTRICT['State Name'] = HOVER_USER_DISTRICT['State Name'].str.replace("-"," ")
    HOVER_USER_DISTRICT['District name'] = HOVER_USER_DISTRICT['District name'].str.replace("district","")
    if(len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='HOVER_USER_DISTRICT';").fetchall()) ==0):
    
        HOVER_USER_DISTRICT.to_sql('HOVER_USER_DISTRICT',conn)
    
    
    #table 9:
    TOP_TRANS_AGG_INDIA_with_Pincode = TOP_TRANS_AGG_INDIA[TOP_TRANS_AGG_INDIA['Pincode']!=0]
    
    if(len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='TOP_TRANS_AGG_INDIA_pincode';").fetchall()) ==0):
        TOP_TRANS_AGG_INDIA_with_Pincode.to_sql('TOP_TRANS_AGG_INDIA_pincode',conn)
 
    
    #table 10:
    TOP_TRANS_AGG_INDIA_with_state= TOP_TRANS_AGG_INDIA[TOP_TRANS_AGG_INDIA['Pincode']==0]
    if(len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='TOP_TRANS_AGG_INDIA_State';").fetchall()) ==0):
    
        TOP_TRANS_AGG_INDIA_with_state.to_sql('TOP_TRANS_AGG_INDIA_State',conn)
    print('Table 10')
    
    #table 11,12:
    TOP_TRANS_AGG_STATE['state'] = TOP_TRANS_AGG_STATE['state'].str.replace("-"," ")
    TOP_TRANS_AGG_STATE['state'] = TOP_TRANS_AGG_STATE['state'].str.capitalize()
    TOP_TRANS_AGG_STATE['Pincode']= TOP_TRANS_AGG_STATE['Pincode'].apply(str)
    pin = TOP_TRANS_AGG_STATE['Pincode'].str.split(".", expand = True)
    TOP_TRANS_AGG_STATE['Pincode1'] = pin[0]
    TOP_TRANS_AGG_STATE.drop('Pincode', axis = 1,inplace=True)
    TOP_TRANS_AGG_STATE.rename(columns={"Pincode1": "Pincode"}, inplace=True)
    
    TOP_TRANS_AGG_STATE_with_pincode =TOP_TRANS_AGG_STATE[TOP_TRANS_AGG_STATE['Pincode']!='0']
    
    TOP_TRANS_AGG_STATE['District'] = TOP_TRANS_AGG_STATE['District'].astype(str)
    TOP_TRANS_AGG_STATE_with_dist = TOP_TRANS_AGG_STATE[TOP_TRANS_AGG_STATE['District']!='nan']
    if(len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='TOP_TRANS_AGG_dist1';").fetchall()) ==0):
    
        TOP_TRANS_AGG_STATE_with_dist.to_sql('TOP_TRANS_AGG_dist1',conn)
    
    
    if(len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='TOP_TRANS_AGG_INDIA_dist_pincode1';").fetchall()) ==0):
        TOP_TRANS_AGG_STATE_with_pincode.to_sql('TOP_TRANS_AGG_INDIA_dist_pincode1',conn)

    
    #table 13,14:
    TOP_USER_STATE_with_State = TOP_USER_STATE[TOP_USER_STATE['Pincode']==0]

    TOP_USER_STATE_with_pincode = TOP_USER_STATE[TOP_USER_STATE['Pincode']!=0]
    
    if(len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='TOP_User_AGG_state';").fetchall()) ==0):
    
        TOP_USER_STATE_with_State.to_sql('TOP_User_AGG_state',conn)
    
    if(len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='TOP_User_INDIA_pincode';").fetchall()) ==0):
    
        TOP_USER_STATE_with_pincode.to_sql('TOP_User_INDIA_pincode',conn)
   
    
   # table 15,16:
    
    TOP_USER_DIST['state'] = TOP_USER_DIST['state'].str.replace("-"," ")
    TOP_USER_DIST['state'] = TOP_USER_DIST['state'].str.capitalize()
    
    TOP_USER_DIST['Pincode']= TOP_USER_DIST['Pincode'].apply(str)
    
    TOP_USER_DIST_with_pincode = TOP_USER_DIST[TOP_USER_DIST['Pincode']!='0']
    TOP_USER_DIST['District'] = TOP_USER_DIST['District'].astype(str)
    TOP_USER_DIST_with_dist = TOP_USER_DIST[TOP_USER_DIST['District']!='nan']
    if(len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='TOP_User_AGG_dist1';").fetchall()) ==0):
    
        TOP_USER_DIST_with_dist.to_sql('TOP_User_AGG_dist1',conn)
  
    if(len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='TOP_User_dist_pincode1';").fetchall()) ==0):
   
        TOP_USER_DIST_with_pincode.to_sql('TOP_User_dist_pincode1',conn)
  
                                       
                                                                                    
uploading_into_Database() 

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

#             india_states = json.load(open("https://raw.githubusercontent.com/JaniceLibbyThomas/PhonePe/Master/states_india.geojson", "r"))
                

            
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
                
#                 india_states = json.load(open("https://raw.githubusercontent.com/JaniceLibbyThomas/PhonePe/Master/states_india.geojson", "r"))
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
