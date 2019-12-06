# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 21:18:24 2019

@author: user
"""

from flask import Flask, render_template, request, redirect
#from flask_mysqldb import MySQL
import yaml
import requests
#from flask import jsonify 

app = Flask(__name__)



# Configure db
#db = yaml.load(open('db_add.yaml'))
#app.config['MYSQL_HOST'] = db['mysql_host']
#app.config['MYSQL_USER'] = db['mysql_user']
#app.config['MYSQL_PASSWORD'] = db['mysql_password']
#app.config['MYSQL_DB'] = db['mysql_db']

#mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch form data
        #add_operation = request.form
        n1 = request.form['n1']
        n2 = request.form['n2']
        data = { "n1":n1, "n2":n2 }
        requests.post("http://192.168.43.140:5000/", json=data, headers={"content-type":"application/json"})
        
        #tot=int(n1)+int(n2)
        #cur = mysql.connection.cursor()
        #cur.execute("INSERT INTO add_table(x, y,z) VALUES(%s, %s,%s)",(n1, n2,tot))
        #mysql.connection.commit()
        #cur.close()
        return redirect('/test')
    return render_template('index_add.html')

@app.route('/test')
def test():
    if request.method == 'GET':
        PARAMS = {'key1': 'value1', 'key2': 'value2','key3':'value3'}
        r=requests.get("http://192.168.43.140:5000/users", params = PARAMS)
        #headers={"content-type":"application/json"})
        return r.content
    
#    return render_template('index_add.html')

@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM add_table")
    if resultValue > 0:
        add_operation = cur.fetchall()
        return render_template('display.html',add_operation=add_operation)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)