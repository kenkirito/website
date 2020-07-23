from datetime import datetime

from flask import Flask, render_template, request, redirect, session, make_response, send_file, jsonify
from mysql.connector import connect
from flask_mail import Mail, Message
import random
import string
import re

app = Flask (__name__)
app.config.update (
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='nehasharma23156@gmail.com',
    MAIL_PASSWORD='knightsnake1234'
)

app.secret_key = 'ghjhjhq/213763fbf'

mail = Mail (app)


@app.route ('/')
def hello_world():
    return render_template ('index.html')


@app.route ('/<url>')
def dynamicUrl(url):
    connection = connect (host='localhost', port='3306', database='student4', user='root', password='123456789')
    cur = connection.cursor ()
    query1 = "select * from url where encryptedUrl='{}'".format (url)
    cur.execute (query1)
    orignal_url = cur.fetchone ()
    if orignal_url == None:
        return render_template ('index.html')
    else:
        print (orignal_url [ 1 ])
        return redirect (orignal_url [ 1 ])


@app.route ('/urlshortner')
def urlshortner():
    url = request.args.get ('link')
    custom = request.args.get ('customurl')
    print (custom)
    print ("planeteach")
    connection = connect (host='localhost', port='3306', database='student4', user='root', password='123456789')
    cur = connection.cursor ()
    encryptedUrl = ''
    if custom == '':
        while True:
            encryptedUrl = createEncryptedUrl ()
            query1 = "select * from url where encryptedUrl='{}'".format (encryptedUrl)
            cur.execute (query1)
            xyz = cur.fetchone ()
            if xyz == None:
                break
        print (encryptedUrl)
        if 'userid' in session:
            id = session [ 'userid' ]
            query = "insert into url(orignal_url,encryptedUrl,is_Active,created_by) values('{}','{}',1,'{}')".format (
                url, encryptedUrl, id)
        else:
            query = "insert into url(orignal_url,encryptedUrl,is_Active) values('{}','{}',1)".format (url, encryptedUrl)
        cur = connection.cursor ()
        cur.execute (query)
        connection.commit ()
        finalencryptedurl = 'sd.in/' + encryptedUrl
    else:
        query1 = "select * from url where encryptedUrl='{}'".format (custom)
        cur.execute (query1)
        xyz = cur.fetchone ()
        if xyz == None:
            if 'userid' in session:
                id = session [ 'userid' ]
                query = "insert into url(orignal_url,encryptedUrl,is_Active,created_by) values('{}','{}',1,'{}')".format (
                    url, custom, id)
            else:
                query = "insert into url(orignal_url,encryptedUrl,is_Active) values('{}','{}',1)".format (url, custom,
                                                                                                          1)
            cur = connection.cursor ()
            cur.execute (query)
            connection.commit ()
            finalencryptedurl = 'sd.in/' + custom
        else:
            return "url already exists"
    if 'userid' in session:
        return redirect ('/home')
    else:
        return render_template ('index.html', finalencryptedurl=finalencryptedurl, url=url)


def createEncryptedUrl():
    letter = string.ascii_letters + string.digits
    encryptedUrl = ''
    for i in range (6):
        encryptedUrl = encryptedUrl + ''.join (random.choice (letter))
    print (encryptedUrl)
    return encryptedUrl


@app.route ("/signup")
def signup():
    return render_template ('signUp.html')


@app.route ("/login")
def login():
    return render_template ('login.html')


@app.route ('/checkLoginIn')
def checkLogIn():
    email = request.args.get ('email')
    password = request.args.get ('pwd')
    connection = connect (host="localhost", port='3306', database="student4", user="root", password="123456789")
    cur = connection.cursor ()
    query1 = "select * from userdetail where emailId='{}'".format (email)
    cur.execute (query1)
    xyz = cur.fetchone ()
    print (xyz)
    if xyz == None:
        return render_template ('Login.html', xyz='you are not registered')
    else:
        if password == xyz [ 3 ]:
            session [ 'email' ] = email
            session [ 'userid' ] = xyz [ 0 ]
            # return render_template('UserHome.html')
            return redirect ('/home')
        else:
            return render_template ('Login.html', xyz='your password is not correct')


@app.route ('/register', methods=[ 'post' ])
def register():
    email = request.form.get ('email')
    username = request.form.get ('uname')
    password = request.form.get ('pwd')
    connection = connect (host='localhost', port='3306', database='student4', user='root', password='123456789')
    cur = connection.cursor ()
    query1 = "select * from userdetail where emailId='{}'".format (email)
    cur.execute (query1)
    xyz = cur.fetchone ()
    if xyz == None:
        file = request.files [ 'file' ]
        print (type (file))
        file.save ('D:/files/' + file.filename)
        query = "insert into userdetail (emailId,userName,password,is_Active,created_Date) values('{}','{}','{}',1,now())".format (
            email, username, password)
        cur = connection.cursor ()
        cur.execute (query)
        connection.commit ()
        return 'you are successfully registered'

    else:
        return 'already register'


@app.route ('/google')
def google():
    path = 'D:/files/billy.jpg'
    return send_file (path, mimetype='image/jpg', as_attachment=True)


@app.route ('/home')
def home():
    if 'userid' in session:
        email = session [ 'email' ]
        print (email)
        id = session [ 'userid' ]
        print (id)
        connection = connect (host="localhost", port='3306', database="student4", user="root", password="123456789")
        cur = connection.cursor ()
        query1 = "select * from url where created_by={}".format (id)
        cur.execute (query1)
        data = cur.fetchall ()
        print (data)
        return render_template ('updateUrl.html', data=data)
    return render_template ('login.html')


@app.route ('/editUrl', methods=[ 'post' ])
def editUrl():
    if 'userid' in session:
        email = session [ 'email' ]
        print (email)
        id = request.form.get ('id')
        url = request.form.get ('orignal_url')
        encrypted = request.form.get ('encryptedUrl')
        print (id)
        print (url)
        print (encrypted)
        return render_template ("editUrl.html", url=url, encrypted=encrypted, id=id)
    return render_template ("login.html")


@app.route ('/updateUrl', methods=[ 'post' ])
def updateUrl():
    if 'userid' in session:
        id = request.form.get ('id')
        url = request.form.get ('orignalurl')
        encrypted = request.form.get ('encrypted')
        connection = connect (host="localhost", port='3306', database="student4", user="root", password="123456789")
        cur = connection.cursor ()
        query = "select * from url where encryptedUrl='{}'and pk_urlId!={}".format (encrypted, id)
        cur.execute (query)
        data = cur.fetchone ()
        if data == None:
            query1 = "update url set orignal_url='{}', encryptedUrl='{}' where pk_urlId={}".format (url, encrypted, id)
            cur.execute (query1)
            connection.commit ()
            return redirect ('/home')
        else:
            return render_template ("editUrl.html", url=url, encrypted=encrypted, id=id,
                                    error='short url already exist')
    return render_template ("login.html")


@app.route ('/deleteUrl', methods=[ 'post' ])
def deleteUrl():
    if 'userid' in session:
        id = request.form.get ('id')
        connection = connect (host="localhost", port='3306', database="student4", user="root", password="123456789")
        cur = connection.cursor ()
        query1 = "delete from url where pk_urlId=" + id
        cur.execute (query1)
        connection.commit ()
        return redirect ('/home')
    return render_template ('login.html')


@app.route ('/mailbhejo')
def mailbhejo():
    msg = Message (subject='mail sender', sender='nehasharma23156@gmail.com',
                   recipients=[ 'lakshyamishra748@gmail.com' ],
                   body="this is my first email through python")
    msg.cc = [ 'lakshya.mishra56@gmail.com' ]
    msg.html = render_template ('index.html')
    with app.open_resource ("C:/Users/mlaks/Pictures/Screenshots/Screenshot (1).png") as f:
        msg.attach ("1.png", "image/png", f.read ())
    mail.send (msg)
    return "mail sent!!"


@app.route ('/logout')
def logout():
    session.pop ('userid', None)
    return render_template ('login.html')


@app.route ('/xyzurl',methods=['post'])
def testapi():
    abc=request.get_json()
    print(abc)
    list=[]
    da={}
    connection = connect (host='localhost', port='3306', database='student4', user='root', password='123456789')
    cur = connection.cursor ()
    query = "select * from url "
    cur.execute (query)
    data=cur.fetchall()
    for i in data:
        da["name"]=i[0]
        da["email"]=i[1]
        list.append(da)
    return jsonify(list)


if __name__ == "__main__":
    app.run ()
