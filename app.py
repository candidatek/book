from flask import Flask, request , redirect , render_template
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']


mysql = MySQL(app)


@app.route('/' , methods=['GET' , 'POST'])
def index():
    if request.method == 'POST' :
        userDetais = request.form
        title  = userDetais['title']
        author = userDetais['author']
        price = userDetais['price']
        uploader = userDetais['owner']
        rating = userDetais['rating']
        branch = userDetais['branch']
        sem = userDetais['sem']

        #return title + sem + branch
        #email = userDetais['email']
        cur  = mysql.connection.cursor()
        cur.execute("INSERT INTO books(title , author , price , uploader , rating , branch , sem) VALUES(%s , %s , %s , %s , %s , %s , %s )" , (title , author , price , uploader , rating , branch , sem ))
        mysql.connection.commit()
        cur.close()
        return redirect('/users')
    return render_template('index.html')
@app.route('/users')
def users():
        return 'asd'
if __name__ == '__main__':
    app.run(debug=True)
