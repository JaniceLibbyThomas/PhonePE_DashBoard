# PhonePE_DashBoard

## Project Description

Analysing PhonePE Dataset and to build a Steamlit dashboard that helps to analyze and improve phonepe business 

### Skills Used:

<a href="https://pandas.pydata.org/docs/reference/index.html">
<img alt="Pandas" src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Pandas_logo.svg/2560px-Pandas_logo.svg.png" width="165"/>
</a>
<a href="https://plotly.com/python-api-reference/">
<img alt="streamlit" src="https://cdn.analyticsvidhya.com/wp-content/uploads/2021/06/39595st.jpeg" width="165"/>
</a>
<a href="https://docs.python.org/3/c-api/index.html">
<img alt="Python" src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png" width="165"/>
</a>

<a href="https://docs.python.org/3/c-api/index.html">
<img alt="SQL" src="https://www.freecodecamp.org/news/content/images/2020/08/Untitled-design-1-.png" width="165"/>
</a>


## Problem Statement
 
The Phonepe pulse Github repository contains a large amount of data related to
various metrics and statistics. The goal is to extract this data and process it to obtain
insights and information that can be visualized in a user-friendly manner.
The solution must include the following steps:
1. Extract data from the Phonepe pulse Github repository through scripting and
clone it..
2. Transform the data into a suitable format and perform any necessary cleaning
and pre-processing steps.
3. Insert the transformed data into a MySQL database for efficient storage and
retrieval.
4. Create a live geo visualization dashboard using Streamlit and Plotly in Python
to display the data in an interactive and visually appealing manner.
5. Fetch the data from the MySQL database to display in the dashboard.
6. Provide at least 10 different dropdown options for users to select different
facts and figures to display on the dashboard.
The solution must be secure, efficient, and user-friendly. The dashboard must be
easily accessible and provide valuable insights and information about the data in the
Phonepe pulse Github repository.

## Work Flow

- **Converting the given data from JSON to CSV**
  - Firstly converting the json format data and converting to Dataframe as saving it as csv file in the github repository.
  
  - Code reference: https://github.com/JaniceLibbyThomas/PhonePE_DashBoard/blob/main/Phonepe_Extracting_data_from_JSON_to_csv.ipynb
  
- _**Uploading the required dataset from**_
   - https://github.com/JaniceLibbyThomas/PhonePe/tree/Master

- _**Data Cleaning & Pre-processing data:**_
  - Transforming the data into a suitable format and performing necessary cleaning
and pre-processing steps.

- _**Uploading the data into Database:**_
Pre- req:

  User should have xampp installed in their system.
  Through xampp server connecting the jupyter notebook to sql localhost using the sql connector.

  - by using my sql connecter data is uploaded into the database.
  
  - Code reference: https://github.com/JaniceLibbyThomas/PhonePE_DashBoard/blob/main/PhonePe_DataEngineering_Uplaoding_into_DB.ipynb.zip
  
  Note: unzip file and upload it to jupyter notebook.
 
- _**Hosting an application using streamlit**_

  - Creating GUI using the streamlit.
  - In GUI user were given option to filter the data using dropdown.
  - Data visualization is also covered in this path, visualization is done by using package called plotly.
  
  code reference: https://github.com/JaniceLibbyThomas/PhonePE_DashBoard/blob/main/Hello.py
  
- _**How to run streamlit**_

  - Step1: Save the Streamlit.py and states_india.geojson file in a local file path.
  - Step2: Open Terminal in your system
  - Step3: Type streamlit run **your_path_where_you_saved__Streamlit.py
  
  it will launch the local host.

## License

The content of this project itself is licensed under the [Creative Commons Attribution 3.0 Unported license](https://creativecommons.org/licenses/by/3.0/), and the underlying source code used to format and display that content is licensed under the [MIT license](LICENSE.md).
