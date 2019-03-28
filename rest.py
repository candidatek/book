from __future__ import print_function # In python 2.7
from flask import Flask, redirect, url_for, session, request, jsonify ,render_template
from flask_oauthlib.client import OAuth
from flask_mysqldb import MySQL
from base64 import b64encode
import json
import datetime
import smtplib
import sys
import config
import yaml
import os


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.debug = True
mysql = MySQL(app)



@app.route('/')
def first():
    return render_template('upload.html')

@app.route('/rest' , methods=['GET' , 'POST'])
def rest():

    key = request.args.get('search')
    cur = mysql.connection.cursor()
    print(key)
    cur.execute("SELECT DISTINCT title , author FROM books WHERE title LIKE %s OR author LIKE %s  LIMIT 5", ("%" + key + "%", "%" + key + "%"))
    #cur.execute("SELECT * FROM books WHERE title LIKE '%s'% " ,[key])
    res = cur.fetchall()
    #print(res)
    jsonResult = jsonify(res)

    return jsonify(res)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM books")
    fname = cur.fetchone()
    folder_name = 'images'
    target = os.path.join(APP_ROOT, 'files/{}'.format(folder_name))
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
        print(request.files.getlist("image"))
    for upload in request.files.getlist("image"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        print(filename)
        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        filename = str(fname[0]) + ext
        if (ext == ".jpg") or (ext == ".png"):
            print("File supported moving on...")
        else:
            render_template("Error.html", message="Files uploaded are not supported...")
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)
    return "DONE"





if __name__ == '__main__':
    app.run()
