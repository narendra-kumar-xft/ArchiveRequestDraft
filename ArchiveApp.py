from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
import logging
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion


output = {}
table = 'archives'

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

@app.route("/", methods=['GET', 'POST'])
def home():
    db_conn = connections.Connection(
        host=customhost,
        port=3306,
        user=customuser,
        password=custompass,
        db=customdb
    )
    cursor = db_conn.cursor()
    cursor.execute("select * from archives")
    data = cursor.fetchall()  # data from database
    return render_template('ViewArchiveSummary.html', value=data)

@app.route("/showaddarch", methods=['GET', 'POST'])
def showaddarch():
    db_conn = connections.Connection(
        host=customhost,
        port=3306,
        user=customuser,
        password=custompass,
        db=customdb
    )
    return render_template('AddArchive.html')

@app.route("/showsummary", methods=['GET', 'POST'])
def showsummary():
    db_conn = connections.Connection(
        host=customhost,
        port=3306,
        user=customuser,
        password=custompass,
        db=customdb
    )
    cursor = db_conn.cursor()
    cursor.execute("select * from archives")
    data = cursor.fetchall()  # data from database
    return render_template('ViewArchiveSummary.html', value=data)
    # return render_template('ViewArchiveSummary.html')


@app.route("/addarch", methods=['POST'])
def addarch():
    db_conn = connections.Connection(
        host=customhost,
        port=3306,
        user=customuser,
        password=custompass,
        db=customdb
    )
    contact_name = request.form['contact_name']
    app_name = request.form['app_name']
    product_id = request.form['product_id']
    team_name = request.form['team_name']
    daysin_std_s3 = request.form['daysin_std_s3']
    retention_days = request.form['retention_days']

    insert_sql = "INSERT INTO archives VALUES (%s, %s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:

        cursor.execute(insert_sql, (contact_name, app_name, product_id, team_name, daysin_std_s3, retention_days))
        db_conn.commit()

    except Exception as e:
        print(e)
        logging.info(msg=e);

    finally:
        print("finally")

    cursor.execute("select * from archives")
    data = cursor.fetchall()  # data from database
    return render_template('ViewArchiveSummary.html', value=data)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
