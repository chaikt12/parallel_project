# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 14:49:54 2019

@author: user
"""

from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml
import json
import MySQLdb

app = Flask(__name__)


db = yaml.load(open('db_add.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

#conn=MySQLdb.connect(host="localhost",user="oscar",passwd="welcome1",db="flaskapp")
#cur=conn.cursor()




    


@app.route('/product_price')
def product():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT category,max(price) as max_price from products group by category;")
    if resultValue > 0:
        productPrice = cur.fetchall()
        #print(productPrice)
        #row_headers=[x[0] for x in cur.description]
        #json_data=[]
        #for result in productPrice:
            #json_data.append(dict(zip(row_headers,productPrice)))
        #print(json_data)
        data = list()
        #for row in productPrice:
        for cat,price in productPrice:
            tmp={"category":cat,"max_price":price}
            data.append(tmp)
                
    #return render_template('display_product.html',productPrice=productPrice)#productPrice=productPrice,columns=columns)
    return json.dumps(data)
@app.route('/range_price')
def range_price():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT sub_category,max(price) as max_price,min(price) as min_price from products group by sub_category;")
    if resultValue > 0:
        productPrice = cur.fetchall()
        print(productPrice)
        data=list()
        #row_headers=[x[0] for x in cur.description]
        #json_data=[]
        #for result in productPrice:
            #json_data.append(dict(zip(row_headers,productPrice)))
            
        for cat,max_price,min_price in productPrice:
            tmp={"sub_category":cat,"max_price":max_price,"min_price":min_price}
            data.append(tmp)
        #return render_template('display_range_price.html',productPrice=productPrice)
        return json.dumps(data)
    
@app.route('/count')
def count():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT category,sub_category,count(*) as item_count from products group by category,sub_category;")
    if resultValue > 0:
        productPrice = cur.fetchall()
        data=list()
        for cat,sub_cat,count in productPrice:
            tmp={"category":cat,"sub_category":sub_cat,"item_count":count}
            data.append(tmp)
        #return render_template('display_item_count.html',productPrice=productPrice)
        return json.dumps(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
        
        
    
