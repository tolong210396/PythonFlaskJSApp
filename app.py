from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask,render_template,jsonify,json,request, url_for, redirect
#from fabric.api import *
import bcrypt

app= Flask(__name__)

client = MongoClient('localhost:27017')
db = client.bankaccount

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/homeadmin')
def homeadmin():
    return render_template('homeadmin.html')

@app.route('/getaccount_one',methods=['POST'])
def getaccount_one():
    try:
        accountId = request.json['id']
        account = db.AC.find_one({'_id':ObjectId(accountId)})
        accountlist1 = []
        for ac in account:
            accountDetail = {
                'id':account['_id'],
                'account_number':account['account_number'],
                'balance':account['balance'],
                'firstname':account['firstname'],
                'lastname':account['lastname'],
                'age':account['age'],
                'gender':account['gender'],
                'address':account['address'],
                'employer': account['employer'],
                'email':account['email'],
                'city':account['city'],
                'state':account['state'],
                'password':account['password'],
                'role':account['role'],
                'id':str(account['_id'])
            }
        accountlist1.append(accountDetail)
    except Exception, e:
        return str(e)
    return json.dumps(accountlist1)

@app.route("/getaccount", methods = ['POST'])
def getaccount():
    try:
        listdb = db.AC.find()
        accountlist = []
        for ac in listdb:
            print ac
            acItem = {
                'account_number':ac['account_number'],
                'firstname':ac['firstname'],
                'lastname':ac['lastname'],
                'email':ac['email'],
                #'address':ac['address'],
                'id': str(ac['_id'])
            }
            accountlist.append(acItem)
    except Exception,e:
        return str(e)
    return json.dumps(accountlist)

@app.route("/addaccount",methods=['POST'])
def addaccount():
    try:
        json_data = request.json['info']
        account_number = json_data['account_number']
        balance = json_data['balance']
        firstname = json_data['firstname']
        lastname = json_data['lastname']
        age = json_data['age']
        gender = json_data['gender']
        address = json_data['address']
        employer = json_data['employer']
        email = json_data['email']
        password = json_data['password']
        city = json_data['city']
        state = json_data['state']
        role = json_data['role']

        db.AC.insert_one({
            'account_number':account_number,'balance':balance,'firstname':firstname,'lastname':lastname,'age':age, 'gender':gender, 'address':address, 'employer':employer, 'email':email, 'city':city, 'state': state, 'password':password, 'role': role
            })
        return jsonify(status='OK',message='inserted successfully')
    except Exception,e:
        return jsonify(status='ERROR',message=str(e))

@app.route('/updateAccount',methods=['POST'])
def updateAccount():
    try:
        accountInfo = request.json['info']
        accountId = accountInfo['_id']
        account_number = accountInfo['account_number']
        balance = accountInfo['balance']
        firstname = accountInfo['firstname']
        lastname = accountInfo['lastname']
        age = accountInfo['age']
        gender = accountInfo['gender']
        address = accountInfo['address']
        employer = accountInfo['employer']
        email = accountInfo['email']
        password = accountInfo['password']
        city = accountInfo['city']
        state = accountInfo['state']
        role = accountInfo['role']
        db.AC.update_one({'account_number': account_number},{'$set': {'balance':balance,'firstname':firstname,'lastname':lastname,'age':age, 'gender':gender, 'address':address, 'employer':employer, 'email':email, 'city':city, 'state': state, 'password':password, 'role': role}})
        return jsonify(status='OK',message='updated successfully')
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))

@app.route('/login', methods = ['POST'])
def login():
    login_user = db.AC.find_one({'email' : request.form['email']})

    if  login_user:
        # if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            passwd = db.AC.find_one({'password' : request.form['pass']})
            if passwd:
                passwd1=db.AC.find_one({'email': request.form['email'], 'role': '1'})
                if passwd1:
                    return redirect(url_for('homeadmin'))
                return redirect(url_for('home'))
    return 'Invalid email/password combination'

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
         existing_user = db.AC.find_one({'username' : request.form['email']})

         if existing_user is None:

             name = request.form['name']
             hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
             users.insert({'name': request.form['name'], 'username' : request.form['email'], 'password' : hashpass})
             session['email'] = request.form['email']
             return redirect(url_for('find'))

         return ('that username already exists!')
    return render_template('register.html')  

@app.route("/deleteAccount",methods=['POST'])
def deleteAccount():
    try:
        accountId = request.json['id']
        db.AC.remove({'_id':ObjectId(accountId)})
        return jsonify(status='OK',message='deletion successful')
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)