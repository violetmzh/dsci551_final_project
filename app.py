import json
import os
from functools import reduce
from operator import eq
from flask import Flask, send_from_directory, render_template, request
from flask_cors import CORS
from database import Database
import uuid
import base64
from collections import OrderedDict

db = Database("data/database.db")
db.connect()
db.create_data_table("""
            CREATE TABLE IF NOT EXISTS AirIndex (
                city TEXT,
                year INTEGER,
                value NUMERIC(7,3),
                UNIQUE(city, year)
            );
        """)
db.disconnect()

db1 = Database("data/database1.db")
db1.connect()
db1.create_data_table("""
            CREATE TABLE IF NOT EXISTS AirIndex (
                city TEXT,
                year INTEGER,
                value NUMERIC(7,3),
                UNIQUE(city, year)
            );
        """)
db1.disconnect()

app = Flask(__name__)
CORS(app=app, resources=r'/*')


def deduplicate(data):
    seen = {}
    for item in data:
        seen.setdefault(tuple(item.items()), item)
    return list(seen.values())

# hash function
def encode_hash(data):
    return str(base64.b64encode(data.encode("utf-8")))[2:-1]

# ------------------------------------------------------------------------------------------------------------------------------------------------------------
# Static resources
#
@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "images/favicon.ico")


@app.route("/main.css")
def staticscss():
    return send_from_directory(os.path.join(app.root_path, "static"), "css/main.css")


@app.route("/main.js")
def staticsmainjs():
    return send_from_directory(os.path.join(app.root_path, "static"), "js/chart/echarts.js")


@app.route("/api.js")
def staticsapijs():
    return send_from_directory(os.path.join(app.root_path, "static"), "js/api.js")


@app.get("/")
def get_index():
    return render_template("index.html")


#
#  interface
# ------------------------------------------------------------------------------------------------------------------------------------------------------------
# Backstage


# registration

@app.post("/resign")
def resign():
    account = request.get_json().get("account")
    password = request.get_json().get("password")
    db.connect()
    result = db.query("""
                SELECT * FROM AirUser;
            """)
    user = None
    for item in result:
        if item[2] == account:
            user = item
    if user is None:
        db.add_data(
            """INSERT INTO AirUser(id, name, account, password, role) VALUES (?, ?, ?, ?, ?);""",
            (str(uuid.uuid4()), 'User', account, password, 2))
        db.disconnect()
        back = json.dumps({
            'code': 200,
            'msg': 'Successfully registered'
        })
        return back
    else:
        back = json.dumps({
            'code': 600,
            'msg': 'Account already exists'
        })
        return back


@app.post("/login")
def login():
    account = request.get_json().get("account")
    password = request.get_json().get("password")
    db.connect()
    result = db.query("""
            SELECT * FROM AirUser;
        """)
    db.disconnect()
    user = None
    for item in result:
        if item[2] == account and item[3] == password:
            user = item
    if user is None:
        back = json.dumps({
            'code': 6000,
            'msg': 'User does not exist or wrong password'
        })
        return back
    else:
        back = json.dumps({
            'code': 200,
            'data': user,
            'msg': 'success'
        })
        return back


@app.get("/select-all-user")
def post_query_user():
    db.connect()
    result = db.query("""
            SELECT * FROM AirUser
        """)
    db.disconnect()
    arr = []
    for item in result:
        arr.append({
            'id': item[0],
            'name': item[1],
            'account': item[2],
            'password': item[3],
            'role': item[4],
        })
    back = json.dumps({
        'code': 200,
        'data': arr,
        'msg': 'success'
    })
    return back


# add user
@app.post("/add-user")
def post_add_user():
    name = request.get_json().get("name")
    account = request.get_json().get("account")
    password = request.get_json().get("password")
    role = request.get_json().get("role")
    db.connect()
    result = db.add_data(
        """INSERT INTO AirUser(id, name, account, password, role) VALUES (?, ?, ?, ?, ?);""",
        (str(uuid.uuid4()), name, account, password, role))
    db.disconnect()
    return result


# update user
@app.post("/update-user")
def post_update_user():
    id = request.get_json().get("id")
    name = request.get_json().get("name")
    account = request.get_json().get("account")
    password = request.get_json().get("password")
    role = request.get_json().get("role")
    db.connect()
    result = db.update_data("""
            UPDATE AirUser SET name = ?,account = ?,password = ?,role = ? """ + """WHERE id = '""" + id + "'",
                            (name, account, password, role))
    db.disconnect()
    return result


# delete user
@app.post("/remove-user")
def post_remove_user():
    id = request.get_json().get("id")
    db.connect()
    result = db.remove_data("""
            DELETE FROM AirUser
            WHERE id = '""" + id + "'")
    db.disconnect()
    return result


# air index
# show data on pages
@app.get("/select-all-index")
def post_query_index():
    db.connect()
    result = db.query("""
            SELECT * FROM AirIndex ORDER BY city
        """)
    db.disconnect()
    db1.connect()
    result1 = db1.query("""
                SELECT * FROM AirIndex ORDER BY city
            """)
    db1.disconnect()
    arr = []
    for item in result:
        arr.append({
            'id': item[0],
            'city': item[1],
            'year': item[2],
            'value': item[3],
            'pmtwo': item[4],
            'humidity': item[5],
            'temperature': item[6]
        })
    for item in result1:
        arr.append({
            'id': item[0],
            'city': item[1],
            'year': item[2],
            'value': item[3],
            'pmtwo': item[4],
            'humidity': item[5],
            'temperature': item[6]
        })
    new = deduplicate(arr)
    ar = sorted(new, key=lambda x: x['city'])
    back = json.dumps({
        'code': 200,
        'data': ar,
        'msg': 'success'
    })
    return back


# search city
@app.post("/search-city-index")
def post_search_city_index():
    city = request.get_json().get("city")

    hashcode = str(encode_hash(str(city))) # hash function here

    cur = db1
    if 'A' <= hashcode[0].upper() <= 'M':
        cur = db
    cur.connect()

    result = cur.query("""
            SELECT * FROM AirIndex WHERE city = '""" + city + """'""")
    cur.disconnect()

    arr = []
    for item in result:
        arr.append({
            'id': item[0],
            'city': item[1],
            'year': item[2],
            'value': item[3],
            'pmtwo': item[4],
            'humidity': item[5],
            'temperature': item[6]
        })
    new = deduplicate(arr)
    ar = sorted(new, key=lambda x: x['city'])
    back = json.dumps({
        'code': 200,
        'data': ar,
        'msg': 'success'
    })
    return back


# add air inf
@app.post("/add-index")
def post_add_index():
    city = request.get_json().get("city")
    year = request.get_json().get("year")
    value = request.get_json().get("value")
    pmtwo = request.get_json().get("pmtwo")
    humidity = request.get_json().get("humidity")
    temperature = request.get_json().get("temperature")

    id = str(encode_hash(str(city) + str(year))) # hash function here

    if 'A' <= id[0].upper() <= 'M':
        db.connect()
        result = db.add_data(
            """INSERT INTO AirIndex(id, city, year, value, pmtwo, humidity, temperature) VALUES (?, ?, ?, ?, ?, ?, ? );""",
            (id, city, year, value, pmtwo, humidity, temperature))
        db.disconnect()
        return result
    else:
        db1.connect()
        result = db1.add_data(
            """INSERT INTO AirIndex(id, city, year, value, pmtwo, humidity, temperature) VALUES (?, ?, ?, ?, ?, ?, ? );""",
            (id, city, year, value, pmtwo, humidity, temperature))
        db1.disconnect()
        return result


# update air inf
@app.post("/update-index")
def post_update_index():
    id = request.get_json().get("id")
    city = request.get_json().get("city")
    year = request.get_json().get("year")
    value = request.get_json().get("value")
    pmtwo = request.get_json().get("pmtwo")
    humidity = request.get_json().get("humidity")
    temperature = request.get_json().get("temperature")
    print(request.get_json())

    new_id = str(encode_hash(str(city) + str(year))) # hash function here

    if ('A' <= id[0].upper() <= 'M') and ('A' <= new_id[0].upper() <= 'M'):
        db.connect()
        db.update_data("""
            UPDATE AirIndex SET id = ?,city = ?,year = ?,value = ?,pmtwo = ?,humidity = ?,temperature = ? """ + """WHERE id = '""" + id + "'",
                   (new_id, city, year, value, pmtwo, humidity, temperature))
        db.disconnect()
    elif ('N' <= id[0].upper() <= 'Z') and ('N' <= new_id[0].upper() <= 'Z'):
        db1.connect()
        db1.update_data("""
            UPDATE AirIndex SET id = ?,city = ?,year = ?,value = ?,pmtwo = ?,humidity = ?,temperature = ? """ + """WHERE id = '""" + id + "'",
                   (new_id, city, year, value, pmtwo, humidity, temperature))
        db1.disconnect()
    elif ('A' <= id[0].upper() <= 'M') and ('N' <= new_id[0].upper() <= 'Z'):
        db.connect()
        db1.connect()
        db1.add_data(
            """INSERT INTO AirIndex(id, city, year, value, pmtwo, humidity, temperature) VALUES (?, ?, ?, ?, ?, ?, ? );""",
            (new_id, city, year, value, pmtwo, humidity, temperature))
        db.remove_data("""
            DELETE FROM AirIndex
            WHERE id = '""" + id + "'")
        db.disconnect()
        db1.disconnect()
    elif ('N' <= id[0].upper() <= 'Z') and ('A' <= new_id[0].upper() <= 'M'):
        db1.connect()
        db.connect()
        db.add_data(
            """INSERT INTO AirIndex(id, city, year, value, pmtwo, humidity, temperature) VALUES (?, ?, ?, ?, ?, ?, ? );""",
            (new_id, city, year, value, pmtwo, humidity, temperature))
        db1.remove_data("""
            DELETE FROM AirIndex
            WHERE id = '""" + id + "'")
        db1.disconnect()
        db.disconnect()
    
    return json.dumps({
        'code': 200,
        'msg': 'success'
    })



# delete air inf
@app.post("/remove-index")
def post_remove_index():
    id = request.get_json().get("id")
    cur = db1 # find the database
    if 'A' <= id[0].upper() <= 'M':
        cur = db
    cur.connect()
    cur.remove_data("""
            DELETE FROM AirIndex
            WHERE id = '""" + id + "'")
    cur.disconnect()
    return json.dumps({
        'code': 200,
        'msg': 'success'
    })



# @app.get("/select-all-set")
# def post_query_set():
#     db1.connect()
#     result = db1.query("""
#             SELECT * FROM AirSet
#         """)
#     db1.disconnect()
#     arr = []
#     for item in result:
#         arr.append({
#             'code': item[0],
#             'hash': item[1]
#         })
#     back = json.dumps({
#         'code': 200,
#         'data': arr,
#         'msg': 'success'
#     })
#     return back


#
# ------------------------------------------------------------------------------------------------------------------------------------------------------------
# data visualization

# get data By year
@app.get("/get-year")
def get_year():
    db.connect()
    db1.connect()
    result = db.query("""
            SELECT * FROM AirIndex
        """)
    result1 = db1.query("""
                SELECT * FROM AirIndex
            """)
    arr = []
    arr1 = []
    for item in result:
        arr.append({
            'id': item[0],
            'city': item[1],
            'year': item[2],
            'value': item[3],
            'pmtwo': item[4],
            'humidity': item[5],
            'temperature': item[6]
        })
    for item in result1:
        arr1.append({
            'id': item[0],
            'city': item[1],
            'year': item[2],
            'value': item[3],
            'pmtwo': item[4],
            'humidity': item[5],
            'temperature': item[6]
        })
    arr.extend(arr1)
    
    years = []
    addresses = []
    for item in arr:
        years.append(item['year'])
        addresses.append(item['city'])
    years = list(OrderedDict.fromkeys(years))
    addresses = list(OrderedDict.fromkeys(addresses))
    peoples = {}
    pmts = {}
    hums = {}
    tems = {}
    for year in years:
        people = []
        pmt = []
        hum = []
        tem = []
        for item in addresses:
            print(year+item)
            result = db.query("""
                        SELECT * FROM AirIndex WHERE city = '""" + item + """' AND year = """ + """'""" + year + """';""")
            result1 = db1.query("""
                                    SELECT * FROM AirIndex WHERE city = '""" + item + """' AND year = """ + """'""" + year + """';""")
            result.extend(result1)
            if len(result) != 0:
                if 'A' <= result[0][0][0].upper() <= 'M':
                    people.append(result[0][3])
                    pmt.append(result[0][4])
                    hum.append(result[0][5])
                    tem.append(result[0][6])
        
                else :
                    people.append(result[0][3])
                    pmt.append(result[0][4])
                    hum.append(result[0][5])
                    tem.append(result[0][6])
            else:
                people.append(0)
                pmt.append(0)
                hum.append(0)
                tem.append(0)
            # if len(result) != 0:
            #     if 'A' <= result[0][0][0].upper() <= 'M':
            #         people.append(result[0][3])
            #         pmt.append(result[0][4])
            #         hum.append(result[0][5])
            #         tem.append(result[0][6])
            # if len(result1) != 0:
            #     print(result1[0])
            #     print(result1[0][1])
            #     if 'M' <= result1[0][0][0].upper() <= 'Z':
            #         people.append(result1[0][3])
            #         pmt.append(result1[0][4])
            #         hum.append(result1[0][5])
            #         tem.append(result1[0][6])
            # if len(result) == 0 and len(result1) == 0:
            #     people.append(0)
            #     pmt.append(0)
            #     hum.append(0)
            #     tem.append(0)

        peoples.update({year: people})
        pmts.update({year: pmt})
        hums.update({year: hum})
        tems.update({year: tem})
    back = json.dumps({
        'code': 200,
        'data': {
            'year': sorted(years),
            'tag': ['Humidity', 'pm2.5', 'Temperature', 'Population'],
            'city': addresses,
            'people': peoples,
            'pmtwo': pmts,
            'humidity': hums,
            'temperature': tems
        },
        'msg': 'success'
    })
    db.disconnect()
    db1.disconnect()
    return back


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
