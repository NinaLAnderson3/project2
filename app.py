# dependencies
from flask import Flask, render_template, jsonify ,url_for
import pandas as pd
from sqlalchemy import create_engine
import json
import requests

# establishing DB connection 
database_path = "Resources/NJ_CPS.sqlite"
engine = create_engine(f"sqlite:///{database_path}", echo=True)

# table names

school = "NJ_school_rating"
poverty = "NJ_poverty"
crime = "NJ_crime"
population = "NJ_population"

# --- create an instance of the Flask class ---
app = Flask(__name__)

# render index.html
@app.route('/')
def home():
    return render_template("index.html")

# render d3.html 
@app.route('/d3')
def d3():
    return render_template("d3.html")

# get data for d3 plot
@app.route('/api/d3_data')
def d3_data():
    sqlite_connection = engine.connect()
      
    query = '''SELECT POV.county_name, POV.median_hh_income, POV.poverty_rate, POV.county_fips,
               CRM.total AS total_offense, ROUND(CRM2.total,2) AS rate_per_100k, CRM3.total AS total_arrest,
               POP.population, SCH.school_rank, (TAX.general_tax_rate + TAX.effective_tax_rate)/2 AS tax_rate
               FROM NJ_poverty AS POV 
               INNER JOIN NJ_crime AS CRM ON POV.county_name = CRM.county_name AND CRM.report_type = 'Number of Offenses'
               INNER JOIN NJ_crime AS CRM2 ON POV.county_name = CRM2.county_name AND CRM2.report_type = 'Rate Per 100,000'
               INNER JOIN NJ_crime AS CRM3 ON POV.county_name = CRM3.county_name AND CRM3.report_type = 'Number of Arrests'
               INNER JOIN (SELECT county_name, SUM(population) AS population FROM NJ_population GROUP BY county_name) AS POP ON POV.county_name = POP.county_name
               INNER JOIN (SELECT county_name, ROUND(AVG(rating),2) AS school_rank FROM NJ_school_rating GROUP BY county_name) AS SCH ON POV.county_name = SCH.county_name
               INNER JOIN (SELECT county_name, AVG(general_tax_rate) as general_tax_rate, AVG(effective_tax_rate) as effective_tax_rate FROM NJ_tax GROUP BY county_name) AS TAX ON POV.county_name = TAX.county_name'''
    df = pd.read_sql(query, sqlite_connection)

    data_csv = df.to_csv(encoding='utf-8')
    sqlite_connection.close()
    
    print("Data retrieval successfull")
    
    return data_csv

# render plotly.html
@app.route('/plotly')
def plotly():
    return render_template("plotly.html")

# get data for plotly plot
@app.route('/api/plotly_data')
def plotly_data():
    sqlite_connection = engine.connect()
    
    metadata_df = pd.read_sql_query("SELECT T1.*, T2.population, T3.general_tax_rate, T3.effective_tax_rate FROM (SELECT county_name,median_hh_income,poverty_rate FROM NJ_poverty) AS T1 \
                                INNER JOIN (SELECT county_name, SUM(population) as population FROM NJ_population GROUP BY county_name) AS T2\
                                ON T1.county_name = T2.county_name \
                                INNER JOIN (SELECT county_name, AVG(general_tax_rate) as general_tax_rate, AVG(effective_tax_rate) as effective_tax_rate FROM NJ_tax GROUP BY county_name) AS T3 \
                                ON T1.county_name = T3.county_name", sqlite_connection)
    metadata_dict = metadata_df.to_dict(orient='records')
    
    school_df = pd.read_sql_query("SELECT county_name,district_code||school_code AS school_id, school_name, rating AS summativescore FROM NJ_school_rating WHERE county_name <> 'CHARTERS' ORDER BY county_name, summativescore DESC", sqlite_connection)
    school_dict = school_df.to_dict(orient='records')
    
    crime_df = pd.read_sql_query("SELECT county_name, murder,rape, robbery, assault, burglary, larceny, auto_theft, total FROM NJ_crime WHERE report_type = 'Number of Offenses'", sqlite_connection)
    crime_dict = crime_df.to_dict(orient='records')
    
    sqlite_connection.close()
    
    data_json= {}
    data_json["metadata"] = metadata_dict
    data_json["school"] = school_dict
    data_json["crime"] = crime_dict
    with open("static/data/plotly.json", "w",encoding ='utf8') as outfile:  
        json.dump(data_json, outfile, indent = 1) 
    print("Data retrieval successfull")
    
    print("Data retrieval successfull")
    # print(data_json)
    return jsonify(data_json)

# get crime data for plotly sunburst
@app.route('/api/sunburst_crime_data')
def sunburst_crime_data():
    sqlite_connection = engine.connect()
      
    query1 = '''SELECT DISTINCT "NJ-"||county_name AS id , county_name AS label,  '' AS parent, SUM(count) AS value FROM 
            (SELECT county_name, 'murder' AS crime_type, murder AS count FROM NJ_crime WHERE report_type = 'Number of Offenses'
        UNION ALL SELECT county_name, 'rape' AS crime_type, rape AS count FROM NJ_crime WHERE report_type = 'Number of Offenses'
        UNION ALL SELECT county_name, 'robbery' AS crime_type, robbery AS count FROM NJ_crime WHERE report_type = 'Number of Offenses'
        UNION ALL SELECT county_name, 'assault' AS crime_type, assault AS count FROM NJ_crime WHERE report_type = 'Number of Offenses'
        UNION ALL SELECT county_name, 'burglary' AS crime_type, burglary AS count FROM NJ_crime WHERE report_type = 'Number of Offenses'
        UNION ALL SELECT county_name, 'larceny' AS crime_type, larceny AS count FROM NJ_crime WHERE report_type = 'Number of Offenses'
        UNION ALL SELECT county_name, 'auto_theft' AS crime_type, auto_theft AS count FROM NJ_crime WHERE report_type = 'Number of Offenses')
        GROUP BY 1,2,3'''
    df1 = pd.read_sql(query1, sqlite_connection)

    query2 = '''SELECT DISTINCT county_name||"-"||crime_type AS id ,crime_type AS label,  "NJ-"||county_name AS parent, SUM(count) AS value FROM 
            (SELECT county_name, 'murder' AS crime_type, murder AS count FROM NJ_crime WHERE report_type = 'Number of Offenses'
        UNION ALL SELECT county_name, 'rape' AS crime_type, rape AS count FROM NJ_crime WHERE report_type = 'Number of Offenses'
        UNION ALL SELECT county_name, 'robbery' AS crime_type, robbery AS count FROM NJ_crime WHERE report_type = 'Number of Offenses'
        UNION ALL SELECT county_name, 'assault' AS crime_type, assault AS count FROM NJ_crime WHERE report_type = 'Number of Offenses'
        UNION ALL SELECT county_name, 'burglary' AS crime_type, burglary AS count FROM NJ_crime WHERE report_type = 'Number of Offenses'
        UNION ALL SELECT county_name, 'larceny' AS crime_type, larceny AS count FROM NJ_crime WHERE report_type = 'Number of Offenses'
        UNION ALL SELECT county_name, 'auto_theft' AS crime_type, auto_theft AS count FROM NJ_crime WHERE report_type = 'Number of Offenses')
        GROUP BY 1,2,3'''
    df2 = pd.read_sql(query2, sqlite_connection)
    
    df = pd.concat([df1, df2])
    data_csv = df.to_csv(encoding='utf-8')
    sqlite_connection.close()
    
    print("Data retrieval successfull")
    
    return data_csv

# get tax data for plotly sunburst
@app.route('/api/sunburst_tax_data')
def sunburst_tax_data():
    sqlite_connection = engine.connect()
      
    query1 = '''SELECT DISTINCT "NJ-"||county_name AS id , county_name AS label,  '' AS parent, AVG(effective_tax_rate) AS value
                FROM NJ_tax 
                GROUP BY 1,2,3'''
    df1 = pd.read_sql(query1, sqlite_connection)

    query2 = '''SELECT DISTINCT county_name||"-"||district_name AS id ,district_name AS label,  "NJ-"||county_name AS parent, effective_tax_rate AS value
                FROM NJ_tax'''
    df2 = pd.read_sql(query2, sqlite_connection)
    
    df = pd.concat([df1, df2])
    data_csv = df.to_csv(encoding='utf-8')
    sqlite_connection.close()
    
    print("Data retrieval successfull")
    
    return data_csv

# get school data for plotly sunburst
@app.route('/api/sunburst_school_data')
def sunburst_school_data():
    sqlite_connection = engine.connect()

    query1 = '''SELECT DISTINCT "NJ-"||county_name AS id , county_name AS label,  '' AS parent, AVG(rating) AS value FROM 
            (SELECT county_name,district_name,gradespan,school_name,rating
            FROM 
              ( SELECT county_name,district_name,gradespan,school_name, rating,
                       ROW_NUMBER() OVER (PARTITION BY county_name
                                          ORDER BY rating DESC) AS rn
                FROM NJ_school_rating) AS tmp 
            WHERE rn <= 3
            ORDER BY county_name) GROUP BY 1,2,3'''
    df1 = pd.read_sql(query1, sqlite_connection)
    
    query2 = '''SELECT DISTINCT county_name||"-"||gradespan AS id ,gradespan AS label,  "NJ-"||county_name AS parent, AVG(rating) AS value FROM 
            (SELECT county_name,district_name,gradespan,school_name,rating
            FROM 
              ( SELECT county_name,district_name,gradespan,school_name, rating,
                       ROW_NUMBER() OVER (PARTITION BY county_name
                                          ORDER BY rating DESC) AS rn
                FROM NJ_school_rating) AS tmp 
            WHERE rn <= 3
            ORDER BY county_name) GROUP BY 1,2,3'''
    df2 = pd.read_sql(query2, sqlite_connection)

    query3 = '''SELECT DISTINCT gradespan||"-"||district_name AS id ,district_name AS label,  county_name||"-"||gradespan AS parent, AVG(rating) AS value FROM 
            (SELECT county_name,district_name,gradespan,school_name,rating
            FROM 
              ( SELECT county_name,district_name,gradespan,school_name, rating,
                       ROW_NUMBER() OVER (PARTITION BY county_name
                                          ORDER BY rating DESC) AS rn
                FROM NJ_school_rating) AS tmp 
            WHERE rn <= 3
            ORDER BY county_name) GROUP BY 1,2,3'''
    df3 = pd.read_sql(query3, sqlite_connection)
    
    query4 = '''SELECT DISTINCT district_name||"-"||school_name AS id ,school_name AS label,  gradespan||"-"||district_name AS parent, AVG(rating) AS value FROM 
        (SELECT county_name,district_name,gradespan,school_name,rating
        FROM 
            ( SELECT county_name,district_name,gradespan,school_name, rating,
                    ROW_NUMBER() OVER (PARTITION BY county_name
                                        ORDER BY rating DESC) AS rn
            FROM NJ_school_rating) AS tmp 
        WHERE rn <= 3
        ORDER BY county_name) GROUP BY 1,2,3'''
    df4 = pd.read_sql(query4, sqlite_connection)
    
    df = pd.concat([df1, df2, df3, df4])
    
    data_csv = df.to_csv(encoding='utf-8')
    sqlite_connection.close()
    
    print("Data retrieval successfull")
    
    return data_csv

# get population data for plotly sunburst
@app.route('/api/sunburst_pop_data')
def sunburst_pop_data():
    sqlite_connection = engine.connect()
      
    query1 = '''SELECT DISTINCT "NJ-"||county_name AS id , county_name AS label,  '' AS parent, SUM(population) AS value 
                FROM NJ_population                                                                                                  
                GROUP BY 1,2,3'''
    df1 = pd.read_sql(query1, sqlite_connection)

    query2 = '''SELECT DISTINCT county_name||"-"||agency AS id ,agency AS label,  "NJ-"||county_name AS parent, SUM(population) AS value
                FROM NJ_population  GROUP BY 1,2,3'''
    df2 = pd.read_sql(query2, sqlite_connection)
    
    df = pd.concat([df1, df2])
    data_csv = df.to_csv(encoding='utf-8')
    sqlite_connection.close()
    
    print("Data retrieval successfull")
    
    return data_csv

# get median household income data for plotly sunburst
@app.route('/api/sunburst_hi_data')
def sunburst_hi_data():
    sqlite_connection = engine.connect()
      
    query1 = '''SELECT DISTINCT "NJ-"||county_name AS id , county_name AS label,  '' AS parent, median_hh_income AS value 
                FROM NJ_poverty'''
    df = pd.read_sql(query1, sqlite_connection)

    data_csv = df.to_csv(encoding='utf-8')
    sqlite_connection.close()
    
    print("Data retrieval successfull")
    
    return data_csv

# get poverty data for plotly sunburst
@app.route('/api/sunburst_poverty_data')
def sunburst_poverty_data():
    sqlite_connection = engine.connect()
      
    query1 = '''SELECT DISTINCT "NJ-"||county_name AS id , county_name AS label,  '' AS parent, poverty_rate AS value 
                FROM NJ_poverty'''
    df = pd.read_sql(query1, sqlite_connection)

    data_csv = df.to_csv(encoding='utf-8')
    sqlite_connection.close()
    
    print("Data retrieval successfull")
    
    return data_csv

# get school data for d3 sunburst
@app.route('/api/d3_sunburst_schools')
def d3_sunburst_schools():
    f = open("static/data/school.json")
    data = json.load(f)
    return data

# @app.route('/api/d3_sunburst_schools')
# def d3_sunburst_schools():
#     sqlite_connection = engine.connect()

#     query = '''SELECT county_name,district_name,gradespan,school_name,rating FROM NJ_school_rating ORDER BY county_name,district_name,gradespan,school_name;'''
#     test = pd.read_sql_query(query, sqlite_connection)
    
#     sqlite_connection.close()
    
#     print("Query successfull")
    
#     data_json = {}
#     data_json["name"] = "school"
#     data_json["description"] = "school"
    
#     counties = list(test['county_name'].unique())
    
#     children = []
#     for i in range(len(counties)):
#         child1 = {}
#         child1["name"] = counties[i]
#         child1["description"] = test['rating'].loc[test['county_name']==counties[i]].mean()
#         district = list(test['district_name'].loc[test['county_name']==counties[i]].unique())
#         child2_list = []
#         for k in range(len(district)):
#             child2 = {}
#             child2["name"] = district[k]
#             child2["description"] = test['rating'].loc[(test['county_name']==counties[i]) & (test['district_name'] == district[k])].mean()
#             child3_list = []
#             gradespan = list(test['gradespan'].loc[(test['county_name']==counties[i]) & (test['district_name'] == district[k])].unique())
#             for j in range(len(gradespan)):
#                 child3 = {}
#                 child3["name"] = gradespan[j]
#                 child3["description"] = test["rating"].loc[(test['county_name']==counties[i]) & (test['district_name'] == district[k]) & (test['gradespan'] == gradespan[j])].mean()
#                 child4_list = []
#                 for index,row in test.loc[(test['county_name']==counties[i]) & (test['district_name'] == district[k]) & (test['gradespan'] == gradespan[j])].iterrows():
#                     child4 = {}
#                     child4["name"] = row["school_name"]
#                     child4["description"] = row["rating"]
#                     child4["size"] = row["rating"]
#                     child4_list.append(child4)
#                 child3["children"] = child4_list
#                 child3_list.append(child3)
#             child2["children"] = child3_list
#             child2_list.append(child2)
#         child1["children"] = child2_list
#         children.append(child1)
        
#     data_json["children"] = children
#     with open("static/data/school.json", "w",encoding ='utf8') as outfile:  
#         json.dump(data_json, outfile, indent = 1) 
#     print("Data retrieval successfull")
#     if data_json:
#         print("Json ready")
#     else:
#         print("Json failed!")
#     return jsonify(data_json)

# get tax data for d3 sunburst
@app.route('/api/d3_sunburst_tax')
def d3_sunburst_tax():
    f = open("static/data/tax_sunburst.json")
    data = json.load(f)
    return data

# @app.route('/api/d3_sunburst_tax')
# def d3_sunburst_tax():
#     sqlite_connection = engine.connect()
    
#     query = '''SELECT DISTINCT * FROM NJ_tax'''
#     test = pd.read_sql_query(query, sqlite_connection)
#     print("Query successfull")
    
#     sqlite_connection.close()
    
#     data_json2 = {}
#     data_json2["name"] = "tax"
#     data_json2["description"] = "tax"
    
#     counties = list(test['county_name'].unique())
    
#     children = []
#     for i in range(len(counties)):
#         child1 = {}
#         child1["name"] = counties[i]
#         child1["description"] = test['effective_tax_rate'].loc[test['county_name']==counties[i]].mean()
#         district = list(test['district_name'].loc[test['county_name']==counties[i]].unique())
#         child2_list = []
#         for k in range(len(district)):
#             for index,row in test.loc[(test['county_name']==counties[i]) & (test['district_name'] == district[k])].iterrows():
#                 child2 = {}
#                 child2["name"] = row["district_name"]
#                 child2["description"] = row["effective_tax_rate"]
#                 child2["size"] = row["effective_tax_rate"]
#                 child2_list.append(child2)
#         child1["children"] = child2_list
#         children.append(child1)
#     data_json2["children"] = children
#     with open("static/data/tax_sunburst.json", "w",encoding ='utf8') as outfile:  
#         json.dump(data_json2, outfile, indent = 1) 
#     print("Data retrieval successfull")
#     if data_json2:
#         print("Json ready")
#     else:
#         print("Json failed!")
#     return jsonify(data_json2)

# get crime data for d3 sunburst
@app.route('/api/d3_sunburst_crime')
def d3_sunburst_crime():
    f = open("static/data/crime.json")
    data = json.load(f)
    return data

# @app.route('/api/d3_sunburst_crime')
# def d3_sunburst_crime():
#     sqlite_connection = engine.connect()
    
#     query = ''' SELECT * FROM (SELECT county_name, police_dept, 'murder' AS crime_type, murder AS count FROM NJ_crime_detail  WHERE report_type = 'Rate Per 100,000' AND total <> 0
#         UNION ALL SELECT county_name, police_dept, 'rape' AS crime_type, rape AS count FROM NJ_crime_detail  WHERE report_type = 'Rate Per 100,000' AND total <> 0
#         UNION ALL SELECT county_name, police_dept, 'robbery' AS crime_type, robbery AS count FROM NJ_crime_detail  WHERE report_type = 'Rate Per 100,000' AND total <> 0
#         UNION ALL SELECT county_name, police_dept, 'assault' AS crime_type, assault AS count FROM NJ_crime_detail  WHERE report_type = 'Rate Per 100,000' AND total <> 0
#         UNION ALL SELECT county_name, police_dept, 'burglary' AS crime_type, burglary AS count FROM NJ_crime_detail  WHERE report_type = 'Rate Per 100,000' AND total <> 0
#         UNION ALL SELECT county_name, police_dept, 'larceny' AS crime_type, larceny AS count FROM NJ_crime_detail  WHERE report_type = 'Rate Per 100,000' AND total <> 0
#         UNION ALL SELECT county_name, police_dept, 'auto_theft' AS crime_type, auto_theft AS count FROM NJ_crime_detail  WHERE report_type = 'Rate Per 100,000' AND total <> 0)
#         ORDER BY 1,2,3'''
#     test = pd.read_sql_query(query, sqlite_connection)
#     print("Query successfull")
    
#     sqlite_connection.close()
    
#     data_json3 = {}
#     data_json3["name"] = "crime"
#     data_json3["description"] = "crime"
    
#     counties = list(test['county_name'].unique())
    
#     children = []
#     children = []
#     for i in range(len(counties)):
#         child1 = {}
#         child1["name"] = counties[i]
#         child1["description"] = test['count'].loc[test['county_name']==counties[i]].mean()
#         police_dept = list(test['police_dept'].loc[test['county_name']==counties[i]].unique())
#         child2_list = []
#         for k in range(len(police_dept)):
#             child2 = {}
#             child2["name"] = police_dept[k]
#             child2["description"] = test['count'].loc[(test['county_name']==counties[i]) & (test['police_dept'] == police_dept[k])].mean()
#             child3_list = []
#             crime_type = list(test['crime_type'].loc[(test['county_name']==counties[i]) & (test['police_dept'] == police_dept[k])].unique())
#             for j in range(len(crime_type)):
#                 for index,row in test.loc[(test['county_name']==counties[i]) & (test['police_dept'] == police_dept[k]) & (test['crime_type'] == crime_type[j])].iterrows():
#                     child3 = {}
#                     child3["name"] = row["crime_type"]
#                     child3["description"] = row["count"]
#                     child3["size"] = row["count"]
#                     child3_list.append(child3)
#                 child2["children"] = child3_list
#             child2_list.append(child2)
#         child1["children"] = child2_list
#         children.append(child1)
#     data_json3["children"] = children
#     with open("static/data/crime.json", "w",encoding ='utf8') as outfile:  
#         json.dump(data_json3, outfile, indent = 1) 
#     print("Data retrieval successfull")
#     if data_json3:
#         print("Json ready")
#     else:
#         print("Json failed!")
#     return jsonify(data_json3)

# @app.route('/tax_json')
# def tax_json():
#     f = open("static/data/tax_sunburst.json")
#     data = json.load(f)
#     return data

# render leaflet.html  
@app.route('/leaflet')
def leaflet():
    return render_template("leaflet.html")

# get leaflet geojson
@app.route('/api/leaflet_data')
def leaflet_data():
    f = open("static/data/final.geojson")
    data = json.load(f)
    return data

# @app.route('/api/leaflet_data')
# def leaflet_data():
#     #  SQLite DB creation and establishing connection
#     database_path = "Resources/NJ_CPS.sqlite"
#     engine = create_engine(f"sqlite:///{database_path}", echo=True)


#     sqlite_connection = engine.connect()
#     print("Data retrieval successfull")
#     query = '''SELECT T1.*, T2.school_rating, T3.tax_rate, T4.poverty_rate, T5.median_hh_income, T6.population
#             FROM
#             (SELECT county_name, total as crime_rate from NJ_crime WHERE report_type = 'Rate Per 100,000') AS T1
#             INNER JOIN (SELECT county_name, AVG(rating) AS school_rating FROM NJ_school_rating  GROUP BY 1) AS T2 
#             ON T1.county_name = T2.county_name
#             INNER JOIN (SELECT county_name, AVG(effective_tax_rate) AS tax_rate FROM NJ_tax GROUP BY 1) AS T3
#             ON T1.county_name = T3.county_name
#             INNER JOIN (SELECT county_name, AVG(poverty_rate) AS poverty_rate FROM NJ_poverty GROUP BY 1) AS T4
#             ON T1.county_name = T4.county_name
#             INNER JOIN (SELECT county_name, AVG(median_hh_income) AS median_hh_income FROM NJ_poverty GROUP BY 1) AS T5
#             ON T1.county_name = T5.county_name
#             INNER JOIN (SELECT county_name, SUM(population) AS population FROM NJ_population GROUP BY 1) AS T6
#             ON T1.county_name = T6.county_name
#     '''
#     test = pd.read_sql_query(query, sqlite_connection)

#     geojson_url = 'https://opendata.arcgis.com/datasets/5f45e1ece6e14ef5866974a7b57d3b95_1.geojson'
#     geojson = requests.get(geojson_url).json()
#     print("Geojson retrieval successfull")

#     for i in range(len(geojson['features'])):
#         county = geojson['features'][i]['properties']['COUNTY']
#         geojson['features'][i]['properties']['crime_rate'] = test['crime_rate'].loc[test['county_name']==county].item()
#         geojson['features'][i]['properties']['school_rating'] = test['school_rating'].loc[test['county_name']==county].item()
#         geojson['features'][i]['properties']['tax_rate'] = test['tax_rate'].loc[test['county_name']==county].item()
#         geojson['features'][i]['properties']['poverty_rate'] = test['poverty_rate'].loc[test['county_name']==county].item()
#         geojson['features'][i]['properties']['median_hh_income'] = test['median_hh_income'].loc[test['county_name']==county].item()
#         geojson['features'][i]['properties']['population'] = test['crime_rate'].loc[test['county_name']==county].item()
#     print("Geojson modification successfull")
#     with open("static/data/final.geojson", "w",encoding ='utf8') as outfile:  
#         json.dump(geojson, outfile) 
#     return jsonify(geojson)

# render bonus.html  
@app.route('/bonus')
def bonus():
    return render_template("bonus.html")

# render bonus.html and get data for population
@app.route("/data_pop")
def data_pop():
    sqlite_connection = engine.connect()
    table = "NJ_population"
    query = "SELECT * from NJ_population"
    df = pd.read_sql(query, sqlite_connection)
    sqlite_connection.close()
    html_table = df.to_html(index=False, header=True, border=1, justify = 'left',classes="bg-light table table-striped table-bordered")
    results = html_table
    print("Data retrieval successfull")
    return render_template("data.html", info = results, table = table)

# render bonus.html and get data for crime
@app.route("/data_crime")
def data_crime():
    sqlite_connection = engine.connect()
    table = "NJ_crime"
    query = "SELECT * from NJ_crime"
    df = pd.read_sql(query, sqlite_connection)
    sqlite_connection.close()
    html_table = df.to_html(index=False, header=True, border=1, justify = 'left',classes="bg-light table table-striped table-bordered")
    results = html_table
    print("Data retrieval successfull")
    return render_template("data.html", info = results, table = table)

# render bonus.html and get data for poverty
@app.route("/data_poverty")
def data_poverty():
    sqlite_connection = engine.connect()
    table = "NJ_poverty"
    query = "SELECT * from NJ_poverty"
    df = pd.read_sql(query, sqlite_connection)
    sqlite_connection.close()
    html_table = df.to_html(index=False, header=True, border=1, justify = 'left',classes="bg-light table table-striped table-bordered")
    results = html_table
    print("Data retrieval successfull")
    return render_template("data.html", info = results, table = table)

# render bonus.html and get data for school
@app.route("/data_school")
def data_school():
    sqlite_connection = engine.connect()
    table = "NJ_school_rating"
    query = "SELECT * from NJ_school_rating"
    df = pd.read_sql(query, sqlite_connection)
    sqlite_connection.close()
    html_table = df.to_html(index=False, header=True, border=1, justify = 'left',classes="bg-light table table-striped table-bordered")
    results = html_table
    print("Data retrieval successfull")
    return render_template("data.html", info = results, table = table)

# render bonus.html and get data for crime detail
@app.route("/data_crime_detail")
def data_crime_detail():
    sqlite_connection = engine.connect()
    table = "NJ_crime_detail"
    query = "SELECT * from NJ_crime_detail"
    df = pd.read_sql(query, sqlite_connection)
    sqlite_connection.close()
    html_table = df.to_html(index=False, header=True, border=1, justify = 'left',classes="bg-light table table-striped table-bordered")
    results = html_table
    print("Data retrieval successfull")
    return render_template("data.html", info = results, table = table)

# render bonus.html and get data for tax
@app.route("/data_tax")
def data_tax():
    sqlite_connection = engine.connect()
    table = "NJ_tax"
    query = "SELECT * from NJ_tax"
    df = pd.read_sql(query, sqlite_connection)
    sqlite_connection.close()
    html_table = df.to_html(index=False, header=True, border=1, justify = 'left',classes="bg-light table table-striped table-bordered")
    results = html_table
    print("Data retrieval successfull")
    return render_template("data.html", info = results, table = table)

# render filter.html  
@app.route('/filter')
def filter():
    return render_template("filter.html")

# get data from population for filtering
@app.route("/api/data_pop_filter")
def data_pop_filter():
    sqlite_connection = engine.connect()
    query = "SELECT * from NJ_population"
    df = pd.read_sql(query, sqlite_connection)
    sqlite_connection.close()
    data_csv = df.to_csv(header=True, index = False, encoding='utf-8')  
    print("Data retrieval successfull")
    return data_csv

# get data from poverty for filtering
@app.route("/api/data_pov_filter")
def data_pov_filter():
    sqlite_connection = engine.connect()
    query = "SELECT * from NJ_poverty"
    df = pd.read_sql(query, sqlite_connection)
    sqlite_connection.close()
    data_csv = df.to_csv(header=True, index = False, encoding='utf-8')  
    print("Data retrieval successfull")
    return data_csv

# get data from tax for filtering
@app.route("/api/data_tax_filter")
def data_tax_filter():
    sqlite_connection = engine.connect()
    query = "SELECT * from NJ_tax"
    df = pd.read_sql(query, sqlite_connection)
    sqlite_connection.close()
    data_csv = df.to_csv(header=True, index = False, encoding='utf-8')  
    print("Data retrieval successfull")
    return data_csv

# get data from crime for filtering
@app.route("/api/data_crime_filter")
def data_crime_filter():
    sqlite_connection = engine.connect()
    query = "SELECT * from NJ_crime"
    df = pd.read_sql(query, sqlite_connection)
    sqlite_connection.close()
    data_csv = df.to_csv(header=True, index = False, encoding='utf-8')  
    print("Data retrieval successfull")
    return data_csv

# get data from crime detail for filtering
@app.route("/api/data_crime_det_filter")
def data_crime_det_filter():
    sqlite_connection = engine.connect()
    query = "SELECT * from NJ_crime_detail"
    df = pd.read_sql(query, sqlite_connection)
    sqlite_connection.close()
    data_csv = df.to_csv(header=True, index = False, encoding='utf-8')  
    print("Data retrieval successfull")
    return data_csv

# get data from school for filtering
@app.route("/api/data_school_filter")
def data_school_filter():
    sqlite_connection = engine.connect()
    query = "SELECT * from NJ_school_rating"
    df = pd.read_sql(query, sqlite_connection)
    sqlite_connection.close()
    data_csv = df.to_csv(header=True, index = False, encoding='utf-8')  
    print("Data retrieval successfull")
    return data_csv

if __name__ == "__main__":
    app.run(debug = True)
