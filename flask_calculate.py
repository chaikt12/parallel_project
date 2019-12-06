# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 21:18:24 2019

@author: user
"""

from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml
import json

app = Flask(__name__)



# Configure db
db = yaml.load(open('db_add.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch form data
        add_operation = request.get_json()
        print(add_operation)
        n1 = add_operation['n1']
        n2 = add_operation['n2']
        tot=int(n1)+int(n2)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO add_table(x, y,z) VALUES(%s, %s,%s)",(n1, n2,tot))
        mysql.connection.commit()
        cur.close()
        return redirect('/users')
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        #resultValue = cur.execute("SELECT * FROM add_table")
        return cur.fetchall()
    return render_template('index_add.html')

@app.route('/users', methods=['GET'])
def users():
#    return 'Hello World'
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM add_table")
    resultValue = cur.fetchall()
    row_headers=[x[0] for x in cur.description] #this will extract row headers
    json_data=[]
    for result in resultValue:
        json_data.append(dict(zip(row_headers,result)))
    return json.dumps(json_data)
#    resultValue.content.json()
#    return json.dumps(resultValue)
#    if resultValue > 0:
#        add_operation = cur.fetchall()
#        return render_template('display.html',add_operation=add_operation)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)