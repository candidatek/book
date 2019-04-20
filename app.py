from __future__ import print_function # In python 2.7
from flask import Flask, redirect, url_for, session, request, jsonify ,render_template
from flask_oauthlib.client import OAuth
from flask_mysqldb import MySQL
from base64 import b64encode
import json
import datetime , uuid
import smtplib
from flask import send_from_directory
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
mysql = MySQL(app)


app.config['GOOGLE_ID'] = "948658928095-cjmtq3jeds1s2ccgt21dfb6lqrthrsbg.apps.googleusercontent.com"
app.config['GOOGLE_SECRET'] = "XJYg7VSkRLF3T47uoOYcC_2S"
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@app.route('/')
def first():
    try:
        email = session['email']
        print("EMAIL")
        return redirect(url_for('dashboard'))
    except:
        session.pop('google_token' , None)
        print("POP")
        return render_template('index.html')

@app.route('/google')
def index():
    if 'google_token' in session:
        me = google.get('userinfo')
        return jsonify({"data": me.data})
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop('google_token', None)
    session.pop('email' , None)
    return render_template('index.html')


@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    print('Hello world!\n\n', file=sys.stderr)
    email = me.data['email']
    verifiy = me.data['verified_email']
    session['email'] = email
    print(email)
    print(verifiy)
    print(type(email))
    #verify weather it is rvce email # ID
    if "rvce.edu.in" not in email:
        print("User Login not allowed")
    #check weatheer the user is new or world
    cur = mysql.connection.cursor()
    cur.execute("SELECT full_name FROM users WHERE email = %s",[email])
    name = cur.fetchone()
    print (name)
    if name == None :
        print ("new")
        return redirect('/newuser')
    else :
        print("OLD")
        return redirect('/dashboard')

    return redirect('/newuser')
    print("\n\n")
    return jsonify({"data": me.data})

@app.route('/newuser' , methods=['GET' , 'POST'])
def newuser():
    if request.method == 'POST' :
        userDetais = request.form
        name = userDetais['name']
        branch = userDetais['dept']
        email = session['email']
        cur = mysql.connection.cursor()
        print("name = %s , branch = %s \n" % (name , branch))
        cur.execute("INSERT INTO users(email , full_name , branch ) VALUES(%s , %s ,%s)" , (email , name , branch))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('dashboard'))
    return render_template('userDetails.html')


@app.route('/result' , methods=['GET' , 'POST'])
def result():
    key = request.args.get('key')
    cur = mysql.connection.cursor()
    cur.execute("SELECT DISTINCT title , author FROM books WHERE title LIKE %s OR author LIKE %s  LIMIT 5", ("%" + key + "%", "%" + key + "%"))
    res = cur.fetchall()
    try:
        email = session['email']
        cur.execute("SELECT full_name FROM users WHERE email = %s ", [email])
        name = cur.fetchone()[0]
        return render_template('dashboardLogedIn.html' , userDetails = res , name = name )
    except:
        print(key)
        cur = mysql.connection.cursor()
        cur.execute("SELECT DISTINCT title , author FROM books WHERE title LIKE %s OR author LIKE %s  LIMIT 5", ("%" + key + "%", "%" + key + "%"))
        res = cur.fetchall()
        return render_template('dashboards.html' , userDetails = res )


@app.route('/dashboard')
def dashboard():
    try:
        email = session['email']
    except:
        redirect(url_for('login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT branch FROM users WHERE email = %s " , [email] )
    branch = cur.fetchone();
    print("Dashboard")
    session['dept'] = branch[0]
    cur.execute("SELECT full_name , email ,phone  ,branch FROM users WHERE  email =  %s " , [email] )
    display = cur.fetchall()
    name = display[0][0]
    cur.execute("SELECT  * FROM books INNER JOIN sold ON books.uploader=sold.seller WHERE books.status = 'booked' AND books.book_id = sold.book_id AND books.uploader = %s ",[email])
    notifiy = cur.fetchall()
    cur.execute("SELECT * FROM sold , books  WHERE sold.buyer = %s AND sold.status = 'sold' AND books.status = 'sold'",[email])
    purchased  = cur.fetchall()
    cur.execute("SELECT * FROM sold WHERE buyer = %s AND status = 'booked'",[email])
    request = cur.fetchall()
    #print(display)
    cur.execute("SELECT * FROM sold , books WHERE seller  = %s AND sold.status = 'sold' AND sold.book_id = books.book_id ",[email])
    sold = cur.fetchall()
    cur.execute("SELECT * FROM books WHERE uploader = %s AND status = 'available'",[email])
    toBeSold = cur.fetchall()
    cur.execute("SELECT * FROM sold , books WHERE sold.buyer  = %s AND sold.status = 'booked' AND sold.book_id = books.book_id ",[email])
    requested = cur.fetchall()

    return render_template('payment.html' ,dis = display , notifiy = notifiy ,purchased = purchased ,name = name , sold  = sold , toBeSold = toBeSold  , requested = requested )


@app.route('/profile')
def profile():
    try:
        email = session['email']
    except:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT branch FROM users WHERE email = %s " , [email] )
    branch = cur.fetchone();
    session['dept'] = branch[0]
    cur.execute("SELECT * FROM users WHERE email = %s " , [email] )
    display = cur.fetchall()
    #print(display)
    jsondata = jsonify(display)
    #return jsondata
    return render_template('profile.html' , dis = display )

@app.route('/profile/edit' , methods=['GET' , 'POST'])
def editDetails():
    try:
        email = session['email']
    except:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    if request.method == 'POST' :
        editDetails = request.form
        try:
            cur.execute("SELECT full_name FROM users WHERE email = %s " , [email])
            name = cur.fetchone()[0]
            edit = editDetails['edit']
            print(edit)
            cur.execute("SELECT * FROM books WHERE book_id = %s AND status = 'available' " , [edit] )
            bookDetails = cur.fetchone();
            print("HERE")
            return render_template('editBookDetails.html' , b = bookDetails ,name = name)
        except:
            try:
                bookIdForDelete = editDetails['updateData']
                title  = editDetails['title']
                author = editDetails['author']
                edition = editDetails['edition']
                price = editDetails['price']
                id = editDetails['bookid']
                rating = editDetails['rating']
                branch = editDetails['dept']
                sem = editDetails['sem']
                print(author+" "+id)
                cur.execute("UPDATE books SET title = %s , author = %s , edition = %s , price = %s , rating = %s ,sem = %s WHERE book_id = %s " ,[title , author , edition , price , rating , sem , id])
                mysql.connection.commit()
                return 'Updated Sucessfully'
            except:
                deleteId = editDetails['delete']
                cur.execute("DELETE FROM books WHERE book_id = %s " , [deleteId])
                mysql.connection.commit()
                return deleteId

@app.route('/profile/purchased')
def pruchased():

        email = session['email']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM sold , books  WHERE sold.buyer = %s AND sold.status = 'sold' AND books.status = 'sold'",[email])
        purchased  = cur.fetchall()
        print(purchased)
        return render_template('addreview.html' , purchased = purchased)

@app.route('/test')
def test():
    return render_template('rev.html')

@app.route('/addreview')
def addreview():
    cur = mysql.connection.cursor()
    try:
        email = session['email']
        comments = request.args.get('comments')
        bookid = request.args.get('bookid')
        print("rest api function called")
        print(bookid)
        cur.execute("SELECT title , author FROM books WHERE book_id = %s ", [bookid])
        res = cur.fetchone()
        title = res[0]
        author = res[1]
        cur.execute("INSERT INTO reviews VALUES (%s ,%s ,%s ,%s)" , [title , author ,email , comments])
        #cur.connection.commit()
        str = 'operation Succssful'
        return jsonify(str)
    except:
        str = 'operation Failed'
        return jsonify(str)


@app.route('/profile/purchased/addreview' ,methods = ['GET' , 'POST'])
def addreviews():
    if request.method == 'POST' :
        reviewForm = request.form
        bookid = reviewForm['addpublicreview']
        bookreview= reviewForm['publicreview']
        email = session['email']
        cur = mysql.connection.cursor()
        cur.execute("SELECT title , author FROM books WHERE book_id = %s ", [bookid])
        bookDetails = cur.fetchone()
        title = bookDetails[0]
        author = bookDetails[1]
        cur.execute("INSERT INTO reviews (title , author , reviewby  , comments) VALUES (%s ,%s , %s , %s )  " , [title , author  ,email , bookreview])
        mysql.connection.commit()
        print(bookid)
        print(bookreview)
        return render_template('addreview.html')
    return  "NOT POST"



@app.route('/profile/uploaded')
def uploaded():
    try:
        email = session['email']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM books WHERE uploader = %s AND status = 'available'",[email])
        booksList = cur.fetchall()
        return render_template('listOfMyBooks.html' , booksList = booksList)

    except :
        return redirect(url_for('logout'))
    #email = session['email']
    #cur = mysql.connection.cursor()

@app.route('/profile/pending')
def pending():
    try:
        cur = mysql.connection.cursor()
        email = session['email']
        #cur.execute("SELECT * FROM books WHERE status = 'booked' AND uploader = %s " , [email])
        #notifications = cur.fetchall()
        #cur.execute("SELECT buyer FROM sold WHERE status = 'booked' AND seller = %s " , [email])
        #buyerInfo = cur.execute()
        cur.execute("SELECT  * FROM books INNER JOIN sold ON books.uploader=sold.seller WHERE books.status = 'booked' AND books.book_id = sold.book_id AND books.uploader = %s ",[email])
        notifiy = cur.fetchall()
        return render_template('notifiy.html' ,  notifiy =notifiy )
    except :
            return redirect(url_for('logout'))

@app.route('/profile/sold')
def sold():
    #try:
        email = session['email']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM sold , books WHERE seller  = %s AND status = 'sold' AND sold.book_id = books.book_id ",[email])
        booksList = cur.fetchall()
        return render_template('listOfMyBooks.html' , booksList = booksList)

@app.route('/profile/requested')
def reqquested():
    #try:
        email = session['email']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM sold WHERE buyer = %s AND status = 'booked'",[email])
        booksList = cur.fetchall()
        return render_template('listOfMyBooks.html' , booksList = booksList)
    #except :
    #    return redirect(url_for('logout'))

@app.route('/addcart' , methods=['GET','POST'])
def addcart():
    if request.method == 'POST':
        bookform  = request.form
        email = session['email']
        b_id = bookform['cartid']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO cart VALUES (%s , %s )" , [email , b_id])
        cur.connection.commit()
        #Write some query
        cart = cur.fetchall()
    return render_template('listOfMyBooks.html' , booksList = cart)

@app.route('/bookDetails', methods=['GET' , 'POST'])
def owner():
        print('Book Details  \n')
        bookname = request.args.get('book')
        #email = session['email']
        img = '123'
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM books WHERE title = %s LIMIT 1", [bookname])
        bookDetails = cur.fetchone()
        img = bookDetails[0]
        cur.execute("SELECT uploader , price , book_id FROM books WHERE title = %s AND status = 'available' ORDER BY price ASC" , [bookname])
        bookSellers = cur.fetchall()
        cur.execute("SELECT * FROM reviews WHERE title = %s ", [bookname])
        reviews = cur.fetchall()
        return render_template('bookDetails.html' , display = bookDetails , seller = bookSellers , reviews = reviews ,img = img)
    #return '\nBook Details'
@app.route('/getImage/<filename>')
def getImage(filename):
    cur = mysql.connection.cursor()
    print("filename = %s  " ,filename)
    try:
        return send_from_directory('files/images' ,filename+".jpg")
    except:
        try:
            return send_from_directory('files/images' , filename+".png")
        except:
            try:
                cur.execute("SELECT book_id FROM books WHERE title = %s ",[filename])
                id = cur.fetchone()
                print("id = " , id)
                try:
                    return send_from_directory('files/images' , id[0]+'.png')
                except:
                    return send_from_directory('files/images' , id[0]+'.jpg')
            except:
                return send_from_directory('files/images' , 'dummy.jpg')

@app.route('/requestBook' , methods=['GET' , 'POST'])

def requestBook():
    if request.method  == 'POST' :
        ownerForm = request.form
        req = ownerForm['req']
        cur = mysql.connection.cursor()

        cur.execute("SELECT status FROM books WHERE book_id = %s " ,[req])
        status = cur.fetchone()
        print("status " +status[0])

        if status[0] != 'available':
            return 'SORRY THIS BOOK HAS BEEN BOOKED BUY SOME ONE ELSE'
        else:
            #all details of the user who requested the book
            try:
                reqEmail = session['email']
                cur.execute("SELECT * FROM users WHERE email = %s " , [reqEmail])
                dbObject = cur.fetchone()
                reqName  = dbObject[2]
                reqPhone = dbObject[5]
                server = smtplib.SMTP('smtp.gmail.com:587')
                server.ehlo()
                server.starttls()
                server.login(config.EMAIL , config.PASS)

                #book Details
                cur.execute("SELECT * FROM books WHERE book_id = %s " ,[req])
                dbObject = cur.fetchone()
                bookTitle = dbObject[1]
                bookAuthor = dbObject[2]
                bookEdition = dbObject[3]
                ownerEmail = dbObject[5]
                price = dbObject[4]
                #owner Details
                cur.execute("SELECT * FROM users WHERE email = %s " ,[ownerEmail])
                dbObject = cur.fetchone()
                ownerName = dbObject[2]
                ownerPhone = dbObject[5]

                cur.execute("SELECT * FROM users WHERE email = %s " ,[ownerEmail])
                dbObject = cur.fetchone()
                ownerName = dbObject[2]
                ownerPhone = dbObject[5]


                now = datetime.datetime.now()
                year = (now.year)
                month = (now.month)
                day = (now.day)
                tdate = f"{year}-{month}-{day}"
                print(tdate)
                try:
                    cur.execute("UPDATE books SET status = 'booked' WHERE book_id = %s " , [req] )
                    cur.execute("INSERT INTO `sold` (`book_id`, `buyer`, `seller`, `status`, `date`) VALUES (%s, %s, %s, 'booked', %s)",(req,reqEmail,ownerEmail , tdate))
                    mysql.connection.commit()
                    try:
                        #server = smtplib.SMTP('smtp.gmail.com:587')
                        #server.ehlo()
                        #server.starttls()
                        #server.login(config.EMAIL , config.PASS)
                        subject = "Notification For Book Request"
                        msg = f"Hello ! The user with email id : {reqEmail} has requested you the book Titled = {bookTitle}\nAuthor = {bookAuthor}\nEdition = {bookEdition} \npriced :{price} \nThe Student Details are \nName = {reqName}\nPhone = {reqPhone} "
                        message = 'Subject:{}\n\n{}'.format(subject , msg)
                        server.sendmail(config.EMAIL , ownerEmail , message)
                        msg = f"Hello ! Your request has been sent to the owner of the book \nTitled = {bookTitle}\nAuthor = {bookAuthor}\nEdition = {bookEdition} \npriced :{price} \nThe Details of book owner are \nName = {ownerName}\nPhone = {ownerPhone} \nEmail = {ownerEmail}"
                        subject = "Conformation For Your Book Request"
                        message = 'Subject:{}\n\n{}'.format(subject , msg)
                        server.sendmail(config.EMAIL , reqEmail , message)
                        print("sent")
                        server.quit()
                    except:
                        return 'email not sent !'
                    return 'Email notification has been sent to the user'
                except:
                    return 'Failed'
            except:
                return redirect(url_for('login'))
            #print(cur.fetchone())
    return ' hmmmm Your request has been sent to the seller :)'



@app.route('/notifiy')
def notify():
    #check if logged in or not
    try:
        email = session['email']
    except:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    email = session['email']
    #cur.execute("SELECT * FROM books WHERE status = 'booked' AND uploader = %s " , [email])
    #notifications = cur.fetchall()
    #cur.execute("SELECT buyer FROM sold WHERE status = 'booked' AND seller = %s " , [email])
    #buyerInfo = cur.execute()
    cur.execute("SELECT  * FROM books INNER JOIN sold ON books.uploader=sold.seller WHERE books.status = 'booked' AND books.book_id = sold.book_id AND books.uploader = %s ",[email])
    notifiy = cur.fetchall()

    emailList = list(notifiy)
    nameList = []
    for i in notifiy:
        cur.execute("SELECT full_name FROM users WHERE email = %s " , [i[13]])
        nameList.append(cur.fetchone())
    for i in range(len(nameList)):
        print(emailList[i][13])
        print(nameList[i])
    return render_template('notifiy.html' ,  notifiy = tuple(emailList) , nm = nameList  )#, buyerInfo = buyerInfo)


@app.route('/asd')
def asd():
        cur = mysql.connection.cursor()
        try:
            email = session['email']
            cur.execute("SELECT full_name FROM users WHERE email = %s " , [email])
            name = cur.fetchone()[0]
            cur.execute("SELECT branch FROM users WHERE email = %s " , [email] )
            branch = cur.fetchone();
            print("Dashboard")
            session['dept'] = branch[0]
            cur.execute("SELECT DISTINCT title , author FROM books WHERE branch = %s " , [branch[0]] )
            display = cur.fetchall()
            cur.execute("SELECT * FROM books WHERE status = 'booked' AND uploader = %s " , [email])
            notifications = cur.fetchall()
            #print(display)

            return render_template('dashboardsLogedIn.html' , userDetails = display , notif = notifications , name = name )
        except:
            cur.execute("SELECT DISTINCT title , author FROM books" )
            display = cur.fetchall()
            print("Loged out")
            return render_template('dashboards.html' , userDetails = display )


@app.route('/contact')
def contact():
    try:
        email = session['email']
        return render_template('contact.html')
    except:
        return redirect(url_for('login'))

@app.route('/closeDeal', methods=['GET', 'POST'])
def closeDeal():
    if request.method == 'POST' :
        bookDetaisForm = request.form
        bookid = bookDetaisForm['deal']
        print(bookid)
        cur = mysql.connection.cursor()
        updateQuery = f"UPDATE books SET status = 'sold' WHERE book_id = {bookid}"
        updateQuery2 = f"UPDATE sold SET status = 'sold' WHERE book_id = {bookid}"
        cur.execute(updateQuery)
        cur.execute(updateQuery2)
        mysql.connection.commit()
        cur.execute("SELECT * FROM sold WHERE book_id = '6'")
        json = jsonify(cur.fetchone())
        return render_template( 'ownerDetails.html' ,js = json)
        #cur.close()
        #return bookid


@app.route('/search' , methods=['GET' , 'POST'])
def search():

    key = request.args.get('search')
    cur = mysql.connection.cursor()
    print(key)
    cur.execute("SELECT DISTINCT title , author FROM books WHERE title LIKE %s OR author LIKE %s  LIMIT 5", ("%" + key + "%", "%" + key + "%"))
    #cur.execute("SELECT * FROM books WHERE title LIKE '%s'% " ,[key])
    res = cur.fetchall()
    jsonResult = jsonify(res)

    return jsonify(res)

@app.route('/sell',methods=['GET' , 'POST'])
def sell():
    try:
        cur  = mysql.connection.cursor()
        email = session['email']
        cur.execute("SELECT full_name FROM users WHERE email = %s ", [email])
        name = cur.fetchone()[0]
        print(name)
        if request.method == 'POST' :
            userDetais = request.form
            title  = userDetais['title']
            author = userDetais['author']
            price = userDetais['price']
            uploader = session['email']
            rating = userDetais['rating']
            branch = userDetais['dept']
            sem = userDetais['sem']
            #photo = userDetais['pic']
            #return title + sem + branch
            #email = userDetais['email']
            if title == "" or author == "" or price == "" or uploader == "" or branch == "" or sem == "" :
                return 'Please Enter All the values'

            id = str(uuid.uuid4().fields[-1])[:8]
            cur.execute("INSERT INTO books(book_id , title , author , price , uploader , rating , branch , sem ,status ) VALUES(%s , %s , %s , %s , %s , %s , %s ,%s  ,'available' )" , (id , title , author , price , uploader , rating , branch , sem  ))
            mysql.connection.commit()
            cur.close()

            folder_name = 'images'
            target = os.path.join(APP_ROOT, 'files/{}'.format(folder_name))
            print("target = " + target)
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
                filename = str(id) + ext
                if (ext == ".jpg") or (ext == ".png"):
                    print("File supported moving on...")
                else:
                    render_template("Error.html", message="Files uploaded are not supported...")
                destination = "/".join([target, filename])
                print("Accept incoming file:", filename)
                print("Save it to:", destination)
                upload.save(destination)
                return 'done'
        return render_template('upload.html' ,name = name)
    except:
        return redirect(url_for('login'))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


if __name__ == '__main__':
    app.run()
