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


#connecting to the SQL database

mydb = mysql.connector.connect(
  host="localhost",
  user="janice",
  password="Janice@123",
  database='PhonePe'
  
)

mycursor = mydb.cursor(buffered=True)
file_no = 0
#Fetching the Data from the SQL and saving it as DataFrame


if(user_ip1 =='ALL INDIA'):

    if(trans_r_user =='TRANSACTIONS'):
      tab1, tab2, tab3 = st.tabs(["TRANSACTION DETAILS", "TOP 10", "MAP"])
      a = mycursor.execute(f"SELECT  `tr_Name`, `tr_Count`, `tr_Amount` FROM `MAP_TRANS_AGG_INDIA` WHERE tr_Year_val ='{Year}' and tr_Quater='{Quater}'")
      out=mycursor.fetchall()
      Frame1 = pd.DataFrame(out,columns = ['Type_of_Transaction','Count','Amount'])
      for i in range(0,len(list(Frame1['Amount']))):
            t = (Frame1['Amount'][i]).split('.')
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
            a = mycursor.execute(f"SELECT `tr_stat_name`, `tr_count`, `tr_amt` FROM `TOP_TRANS_AGG_INDIA_State` WHERE tr_Year_val ='{Year}' and tr_Quater='{Quater}'")
            out=mycursor.fetchall()
            Frame2 = pd.DataFrame(out,columns = ['State_name','Count','Amount'])
            temp = Frame2.groupby(['State_name'])['Amount','Count'].sum()
            temp.to_csv(f'/Users/joelsanthoshraja/Downloads/temp_{file_no}.csv')
            Frame3 = pd.read_csv(f'/Users/joelsanthoshraja/Downloads/temp_{file_no}.csv')
            Frame3.sort_values(by="Count",ascending=False)
            st.line_chart(Frame3, x = 'State_name',y ='Count')
          
            file_no +=1
            
          elif(radio =='Pincode'):

            a = mycursor.execute(f"SELECT `tr_pincode`, `tr_count`, `tr_amt` FROM `TOP_TRANS_AGG_INDIA_dist_pincode` WHERE tr_Year_val ='{Year}' and tr_Quater='{Quater}'")
            out=mycursor.fetchall()
            Frame2 = pd.DataFrame(out,columns = ['Pincode','Count','Amount'])
            temp = Frame2.groupby(['Pincode'])['Count'].sum()
            temp.to_csv(f'/Users/joelsanthoshraja/Downloads/temp_{file_no}.csv')
            Frame3 = pd.read_csv(f'/Users/joelsanthoshraja/Downloads/temp_{file_no}.csv')
            Frame3 = Frame3.sort_values(by="Count",ascending=False)
            
            val = (Frame3.iloc[0:10].reset_index().drop(['index'],axis=1))
            val['Pincode'] = val['Pincode'].astype(str)
            st.line_chart(val,x ='Pincode',y ='Count')
            file_no +=1
          else:
            a = mycursor.execute(f"SELECT `tr_dist_name`, `tr_count`, `tr_amt` FROM `TOP_TRANS_AGG_dist1` WHERE tr_Year_val ='{Year}' and tr_Quater='{Quater}'")
            out=mycursor.fetchall()
            Frame2 = pd.DataFrame(out,columns = ['District Name','Count','Amount'])


            temp = Frame2.groupby(['District Name'])['Count'].sum()

            temp.to_csv(r'/Users/joelsanthoshraja/Downloads/temp1.csv')
            Frame3 = pd.read_csv(r'/Users/joelsanthoshraja/Downloads/temp1.csv')
            Frame3 = Frame3.sort_values(by="Count",ascending=False)
            val = (Frame3.iloc[0:10].reset_index().drop(['index'],axis=1))
            
            st.line_chart(val,x ='District Name',y ='Count')
            file_no +=1

      with tab3:
            Map_ip = st.selectbox(
                'Select Anyone',
                ("Count",'Amount'))
                

            a = mycursor.execute(f"SELECT `tr_State_name`, `tr_Count`, `tr_amount`, `tr_Map_id` FROM `HOVER_TRANS_AGG_INDIA`  WHERE tr_Year_val ='{Year}' and tr_Quater='{Quater}'")
            out=mycursor.fetchall()
            Frame2 = pd.DataFrame(out,columns = ['State Name','Count','Amount','Map_id'])
            for i in range(0,len(list(Frame2['Amount']))):
                 t = (Frame2['Amount'][i]).split('.')
                 Frame2['Amount'][i] = t[0]
            Frame2['Amount'] = Frame2['Amount'].astype(int)

            india_states = json.load(open("/Users/joelsanthoshraja/Downloads/states_india.geojson", "r"))
                

            
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

              a = mycursor.execute(f"SELECT `us_No_of_Registered_User`, `us_AppOpens`, `us_Count` FROM `MAP_USER_AGG_INDIA` WHERE us_Year_val ='{Year}' and us_Quater='{Quater}'")
              out=mycursor.fetchall()
              Frame1 = pd.DataFrame(out,columns = ['No of Registered User','App_Opens','Count'])
              
              a = Frame1['No of Registered User'][0]
              if(str(Frame1['App_Opens'][0]) == '0'):
                  b = 'Unavailable'
              else:
                  b = Frame1['App_Opens'][0]


              st.metric(label=f'Registered PhonePe users till {Quater} {Year}', value=a,
                delta_color="inverse")

              st.metric(label=f"PhonePe app opens in {Quater} {Year}", value=b,
                delta_color="inverse")
              
            # container1.markdown(f'Registered PhonePe users till {Quater} {Year} : {a}')
             # container1.markdown(f"PhonePe app opens in {Quater} {Year} : {b}")

          with tab2:
        #Top 10: State, District and Pincode
          
              radio = st.radio('Select Any One ',['State','District','Pincode'])
              st.subheader(f'Top 10 Amount of Registered User Based on {radio}')
              if(radio == 'State'):
                a = mycursor.execute(f"SELECT `tr_state_name`, `No_of_Registered_User` FROM `TOP_User_AGG_state` WHERE tr_Year_val ='{Year}' and tr_Quater='{Quater}'")
                out=mycursor.fetchall()
                Frame2 = pd.DataFrame(out,columns = ['State Name','No of reg user'])
                temp = Frame2.groupby(['State Name'])['No of reg user'].sum()
                temp.to_csv(r'/Users/joelsanthoshraja/Downloads/temp1.csv')
                Frame3 = pd.read_csv(r'/Users/joelsanthoshraja/Downloads/temp1.csv')
                Frame3 = Frame3.sort_values(by="No of reg user",ascending=False)
                st.line_chart(Frame3, x = 'State Name',y ='No of reg user')
                file_no +=1

              elif(radio =='District'):

                a = mycursor.execute(f"SELECT `tr_dist_name`, `No_of_Registered_User` FROM `TOP_User_AGG_dist` WHERE tr_Year_val ='{Year}' and tr_Quater='{Quater}'")
                out=mycursor.fetchall()
                Frame2 = pd.DataFrame(out,columns = ['District Name','No Of Registered User'])
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
                a = mycursor.execute(f"SELECT `tr_pincode`, `No_of_Registered_User` FROM `TOP_User_dist_pincode1` WHERE tr_Year_val ='{Year}' and tr_Quater='{Quater}'")
                out=mycursor.fetchall()
                Frame2 = pd.DataFrame(out,columns = ['Pincode','No Of Registered User'])
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
                
                india_states = json.load(open("/Users/joelsanthoshraja/Downloads/states_india.geojson", "r"))
                a = mycursor.execute(f"SELECT `us_state_name`, `us_reg_us`, `us_appOpen`, `us_Map_id` FROM `HOVER_USER_STATE`  WHERE us_Year_val ='{Year}' and us_Quater='{Quater}'")
                out=mycursor.fetchall()
                Frame2 = pd.DataFrame(out,columns = ['State Name','No of Registered User','No of App Open','Map_id'])
                india_states = json.load(open("/Users/joelsanthoshraja/Downloads/states_india.geojson", "r"))

                
                
               
                df = px.data.election()
                geojson = px.data.election_geojson()

                fig = px.choropleth_mapbox(Frame2, geojson=india_states, color=Map_ip,
                    locations="State Name", featureidkey="properties.st_nm",
                    hover_data=[Map_ip],
                    mapbox_style="carto-positron",
                    center={"lat": 24, "lon": 78},zoom = 3, opacity = 0.5

                   )
            
                fig.update_geos(fitbounds="locations", visible=False)
                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                st.plotly_chart(fig)

else:
    

    if(trans_r_user =='TRANSACTIONS'):
      tab1, tab2, tab3 = st.tabs(["TRANSACTION DETAILS", "TOP 10", "MAP"])
    

      with tab1:
      #Total Online Transaction details
        st.subheader('TRANSACTIONS')
        container1 = st.container()  

        a = mycursor.execute(f"SELECT  `tr_Name`,  `tr_Count`, `tr_Amount` FROM `MAP_TRANS_AGG_STATE` WHERE tr_Year_val ='{Year}' and tr_Quater='{Quater}' and tr_state ='{state}'")
        out=mycursor.fetchall()
        Frame1 = pd.DataFrame(out,columns = ['Type_of_Transaction','Count','Amount'])
        for i in range(0,len(list(Frame1['Amount']))):
            t = (Frame1['Amount'][i]).split('.')
            Frame1['Amount'][i] = t[0]
        Frame1['Amount'] = Frame1['Amount'].astype(int)

        sum_count = list(Frame1['Count'])
        amt_sum = list(Frame1['Amount'])
      
        a = sum(sum_count)
        b = round(sum(amt_sum)/1000000)
        c = round(sum(amt_sum)/(sum(sum_count)))
        D = str(babel.numbers.format_currency(b, "INR", locale='en_US'))
        new = D.split('.')
        st.metric(label=f'All PhonePe transactions (UPI + Cards + Wallets)', value=a,
                delta_color="inverse")

        st.metric(label=f"Total payment value in ₹",value =(new[0]+' Cr') ,
                delta_color="inverse")

       
        st.metric(label=f"Avg. transaction value in ₹", value=c,
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
        
        #chart_data = chart_data.sort_values(by=['Amount of Transaction'])
  

        st.bar_chart(chart_data,x="Type of Transaction", y="Amount of Transaction", width=500, height=500) 
           
      with tab2:
        #Top 10: State, District and Pincode
          
          radio = st.radio('Select Any One ',['District','Pincode'])
          st.subheader(f'Top 10 Transactions Based on {radio}')
          if(radio == 'District'):
              
            a = mycursor.execute(f"SELECT `tr_dist_name`, `tr_count`, `tr_amt` FROM `TOP_TRANS_AGG_dist1` WHERE tr_Year_val ='{Year}' and tr_Quater='{Quater}' and tr_state = '{state}'")
            out=mycursor.fetchall()
            Frame2 = pd.DataFrame(out,columns = ['District Name','Count','Amount'])
            temp = Frame2.groupby(['District Name'])['Count'].sum()
            data = dict(temp)
            df = pd.DataFrame.from_dict([data]).T
            
            df = df.sort_values(by=0,ascending=False)
            df = df.reset_index()
            df.rename(columns={"index": "District Name",0:'Count'}, inplace=True)
            val = (df.iloc[0:10].reset_index().drop(['index'],axis=1))
            #val['Pincode'] = val['Pincode'].astype(str)
            st.line_chart(val,x ='District Name',y ='Count')
            
          
          else:


            a = mycursor.execute(f"SELECT `tr_pincode`, `tr_count`, `tr_amt` FROM `TOP_TRANS_AGG_INDIA_dist_pincode1` WHERE tr_Year_val ='{Year}' and tr_Quater='{Quater}' and tr_state = '{state}'")
            out=mycursor.fetchall()
            Frame2 = pd.DataFrame(out,columns = ['Pincode','Count','Amount'])
            temp = Frame2.groupby(['Pincode'])['Count'].sum()
            data = dict(temp)
            df = pd.DataFrame.from_dict([data]).T
            
            df = df.sort_values(by=0,ascending=False)
            df = df.reset_index()
            df.rename(columns={"index": "Pincode",0:'Count'}, inplace=True)
            df['Pincode'] = df['Pincode'].astype(str)
            st.line_chart(df,x ='Pincode',y ='Count')
          

      with tab3:
            
            a = mycursor.execute(f"SELECT `tr_State_name`, `tr_Count`, `tr_amount`, `tr_Map_id` FROM `HOVER_TRANS_AGG_INDIA`  WHERE tr_Year_val ='{Year}' and tr_Quater='{Quater}'")
            out=mycursor.fetchall()
            Frame2 = pd.DataFrame(out,columns = ['State Name','Count','Amount','Map_id'])

            india_states = json.load(open("/Users/joelsanthoshraja/Downloads/states_india.geojson", "r"))
            fig = px.choropleth_mapbox(
                Frame2,
                locations='Map_id',
                geojson=india_states,
                color="Count",

                hover_name="State Name",
                hover_data=["Count",'Amount'],
                title="No of Transaction and Total Amount Transfered",
                mapbox_style="carto-positron",
                center={"lat": 24, "lon": 78},
                zoom=3.5,
                opacity=0.5,
                )
            fig.update_geos(fitbounds="locations",visible = False)
            fig.update_layout(
                autosize=False,
                width=800,
                height=750)
            st.plotly_chart(fig, use_container_width=True)


    else:

        if(trans_r_user =='USER'):
          tab1, tab2, tab3 = st.tabs(["USER DETAILS", "TOP 10", "MAP"])
          
          with tab1:
      #Total Online User details
              st.subheader('USERS')
              container1 = st.container()

              a = mycursor.execute(f"SELECT `us_No_of_Registered_User`, `us_AppOpens`, `us_Count` FROM `MAP_USER_AGG_INDIA` WHERE us_Year_val ='{Year}' and us_Quater='{Quater}'")
              out=mycursor.fetchall()
              Frame1 = pd.DataFrame(out,columns = ['No of Registered User','App_Opens','Count'])
              
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
          
              radio = st.radio('Select Any One ',['District','Pincode'])
              st.subheader(f'Top 10 Amount of Registered User Details Based on {radio}')
              if(radio == 'District'):
                a = mycursor.execute(f"SELECT `tr_dist_name`, `No_of_Registered_User` FROM `TOP_User_AGG_dist1` WHERE tr_Year_val ='{Year}' and tr_Quater='{Quater}' and tr_state = '{state}'")
                out=mycursor.fetchall()
                Frame2 = pd.DataFrame(out,columns = ['District Name','No of Registered User'])
         
                temp = Frame2.groupby(['District Name'])['No of Registered User'].sum()
                data = dict(temp)
                df = pd.DataFrame.from_dict([data]).T
                df[0]=df[0].astype(int)

                df = df.sort_values(by=0,ascending=False)
                df = df.reset_index()
                df.rename(columns={"index": "District Name",0:'No of Registered User'}, inplace=True)
                
                val = (df.iloc[0:10].reset_index().drop(['index'],axis=1))
            
                st.line_chart(val,x ='District Name',y ='No of Registered User')

     

              else:

                a = mycursor.execute(f"SELECT `tr_pincode`, `No_of_Registered_User` FROM `TOP_User_dist_pincode1` WHERE tr_Year_val ='{Year}' and tr_Quater='{Quater}' and tr_state = '{state}'")
                out=mycursor.fetchall()
                Frame2 = pd.DataFrame(out,columns = ['Pincode','No of Registered User'])
# Frame2['No Of Registered User'] = Frame2['No Of Registered User'].astype(int)
                temp = Frame2.groupby(['Pincode'])['No of Registered User'].sum()
                data = dict(temp)
                df = pd.DataFrame.from_dict([data]).T
                df = df.sort_values(by=0,ascending=False)
                df = df.reset_index()
                df.rename(columns={"index": "Pincode",0:'No of Registered User'}, inplace=True)
               
                val = (df.iloc[0:10].reset_index().drop(['index'],axis=1))
                val['Pincode'] = val['Pincode'].astype(str)
                st.line_chart(val,x ='Pincode',y ='No of Registered User')

              
          with tab3:

                Map_ip = st.selectbox(
                'Select Anyone',
                ('No of Registered User',"No of App Open"))
                
                india_states = json.load(open("/Users/joelsanthoshraja/Downloads/states_india.geojson", "r"))
                a = mycursor.execute(f"SELECT `us_state_name`, `us_reg_us`, `us_appOpen`, `us_Map_id` FROM `HOVER_USER_STATE`  WHERE us_Year_val ='{Year}' and us_Quater='{Quater}'")
                out=mycursor.fetchall()
                Frame2 = pd.DataFrame(out,columns = ['State Name','No of Registered User','No of App Open','Map_id'])
                india_states = json.load(open("/Users/joelsanthoshraja/Downloads/states_india.geojson", "r"))

                df = pd.read_csv('/Users/joelsanthoshraja/Downloads/poptable.csv')
                df['State.Name'] = df['State.Name'].str.capitalize()
                df['State.Name'] = df['State.Name'].str.rstrip()

                index = df[df['State.Name']==state].index.values

                lat = df['latitude'][index]
                long = df['longitude'][index]

                
                

                fig = px.choropleth(Frame2, geojson=india_states, color=Map_ip,
                    locations="State Name", featureidkey="properties.st_nm.Delhi",
                    projection="mercator"
                   )
                fig.update_geos(fitbounds="locations", visible=False)
                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                st.plotly_chart(fig)
                
              
