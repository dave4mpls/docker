from flask import Flask, request
from redis import Redis, RedisError
import os
import socket
import nextbus
import cgi
import mysql.connector

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)
app.debug = True

def opendb():
    mydb = mysql.connector.connect(host="mysql",user="testuser",password="testpassword",database="buslist")
    # we also make sure the schema is there
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS busrequests (id INT AUTO_INCREMENT PRIMARY KEY, route VARCHAR(255), stop VARCHAR(255), direction VARCHAR(30));")
    return mydb

def addToDatabase(mydb, route, stop, direction):
    mycursor = mydb.cursor()
    sql = "INSERT INTO busrequests (route, stop, direction) VALUES (%s, %s, %s);"
    val = (route, stop, direction)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()
    return

def listDatabase(mydb):
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT id, route, stop, direction FROM busrequests ORDER BY id DESC;"
    outstr = '<table style="border-collapse: collapse;">'
    tdstr = '<td style="border: thin solid black; padding: 10px">'
    mycursor.execute(sql)
    row = mycursor.fetchone()
    while row is not None:
        outstr += '<tr>' + tdstr + cgi.escape(row['route']) + '</td>' \
            + tdstr + cgi.escape(row['stop']) + '</td>' \
            + tdstr + cgi.escape(row['direction']) + '</td>' \
            + tdstr + '<a href="/busresultsid?id=' + cgi.escape(str(row['id'])) + '">Check</a>' \
            + '</tr>'
        row = mycursor.fetchone()
    outstr += '</table>'
    return outstr

def getFromDatabase(mydb,i):
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT route, stop, direction FROM busrequests WHERE id=%s;"
    mycursor.execute(sql,(i,))
    row = mycursor.fetchone()
    if row is None: raise Exception("ID not found")
    return row

def getBackLinks():
    return '<a href="/">Return to Main Page</a><br>' \
           '<a href="/bus">Return to Bus Route Entry</a><br>'

@app.route("/")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
	   '<b>Link to NextBus Example:</b> <a href="/bus">NextBus</a><br>' \
           "<b>Visits:</b> {visits}"
    return html.format(name=os.getenv("NAME", "universe"), hostname=socket.gethostname(), visits=visits)

@app.route("/bus")
def busroute():
    html = '<h3>NextBus</h3>' + getBackLinks() + \
           '<form method=get action="/busresults">' \
           'Route: <input name=route><br>' \
           'Stop: <input name=stop><br>' \
           'Direction (North, South, East, West): <input name=direction><br>'\
           '<input type=submit name=View value=View></form>'
    try:
        mydb = opendb()
        html += listDatabase(mydb)
    except Exception as e:
        html += "An error occurred listing from the database: " + cgi.escape(str(e))
    return html.format(name=os.getenv("NAME", "universe"), hostname=socket.gethostname())

@app.route("/busresults",methods=["GET"])
def busrouteresults():
    error = ""
    try:
      mydb = opendb()
      addToDatabase(mydb, request.args.get('route',''),request.args.get('stop',''),request.args.get('direction',''))
      mydb.close()
    except Exception as e:
      error = "An error occurred adding to the database: " + cgi.escape(str(e))
    busresult = nextbus.nextBus(request.args.get('route',''),request.args.get('stop',''),request.args.get('direction',''))
    resultencoded = cgi.escape(busresult)
    html = '<h3>NextBus Results</h3>' + getBackLinks() + \
           '<span style="color: red">' + error + '</span><br>' \
           'Result: ' + resultencoded;
    return html

@app.route("/busresultsid",methods=["GET"])
def busresultsid():
    error = ""; resultencoded = ""
    try:
      mydb = opendb()
      rowresult = getFromDatabase(mydb, request.args.get('id',''))
      mydb.close()
      busresult = nextbus.nextBus(rowresult['route'],rowresult['stop'],rowresult['direction'])
      resultencoded = cgi.escape(busresult)
    except Exception as e:
      error = "An error occurred retrieving from the database: " + cgi.escape(str(e))
    html = '<h3>NextBus Results</h3>' + getBackLinks() + \
           '<span style="color: red">' + error + '</span><br>' \
           'Result: ' + resultencoded;
    return html
               
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

