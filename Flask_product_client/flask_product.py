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

@app.route('/', methods=['GET', 'POST'])
def front():
    if request.method == 'POST':
        productPrice=request.form
        if productPrice.get('price',None)=="highest_price":
            return redirect('/product_price')
        #if productPrice['price']=='highest_price':
            #return redirect('/product_price')
        elif productPrice.get('rangeprice',None)=="range_price":
            return redirect('/range_price')
        elif productPrice.get('itemcount',None)=="item_count":
            return redirect('/count')
    return render_template('index_product.html')


    


@app.route('/product_price')
def product():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT category,max(price) as max_price from products group by category;")
    if resultValue > 0:
        productPrice = cur.fetchall()
    return render_template('display_product.html',productPrice=productPrice)#productPrice=productPrice,columns=columns)

@app.route('/range_price')
def range_price():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT sub_category,max(price) as max_price,min(price) as min_price from products group by sub_category;")
    if resultValue > 0:
        productPrice = cur.fetchall()
        return render_template('display_range_price.html',productPrice=productPrice)
    
@app.route('/count')
def count():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT category,sub_category,count(*) as item_count from products group by category,sub_category;")
    if resultValue > 0:
        productPrice = cur.fetchall()
        return render_template('display_item_count.html',productPrice=productPrice)

if __name__ == '__main__':
    app.run(debug=True)
        
        
    
