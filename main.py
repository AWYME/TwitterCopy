from db.clients import *
from db.posts import *
from db.messages import *
from db.chats import *
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from datetime import datetime, timedelta
import os
import uuid
app = Flask(  
	__name__,
	template_folder='templates',  
	static_folder='static',
)
app.permanent_session_lifetime = timedelta(days=3)
app.secret_key='__AwYmE__'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLD = '\\uploads'
UPLOAD_FOLDER = APP_ROOT + UPLOAD_FOLD
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['GET','POST'])
def post():
    posts=getAllPosts()
    for i in range(len(posts)):
        posts[i].update({"client_email": getUserById(posts[i]["client_id"])["email"]})
    if request.method == 'POST':
        text=request.form['text']
        file=request.files['file']
        if len(text)==0 and file.filename=='':
            return render_template('post.html',posts=posts, error='')
        
        client_id=session['id']
        filename = str(uuid.uuid4())
        date_time = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        createPost(text,filename,date_time,client_id)
        return redirect(url_for('post'))
    return render_template('post.html',posts=posts)

@app.route('/signUp', methods=["POST", "GET"])
def signUp():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        userFromDb = getUserByEmail(email)
        if not userFromDb:
            createUser(email, password)
            user=getUserByEmail(email)
            session['id']=user['id']
            session['email']=user['email']
            return redirect(url_for('post'))
        else:
            return render_template('signUp.html', error="Такой пользователь уже существует")
    return render_template('signUp.html')

@app.route('/logIn', methods=['GET','POST'])
def logIn():
    if request.method=='POST':
        email =request.form['email']
        password =request.form['password']
        user=getUserByEmail(email)
        if user['password']==password and user:
            session['id']=user['id']
            session['email']=user['email']
            return redirect(url_for('post'))
        else: return render_template('logIn.html', error="Неверный пароль")
    return render_template('logIn.html') 

@app.route('/logOut', methods=['GET','POST'])
def logOut():
    session.clear()
    return redirect(url_for('post'))

@app.route('/profile/<email>')
def profile(email):
    user=getUserByEmail(email)
    id=user['id']
    return render_template('profile.html',id=id,email=email)

@app.route('/chat/<email>',methods=['GET','POST'])
def chat(email):
    userId2=getUserByEmail(email)
    chat=getChatBetweenClients(userId2['id'],session.get('id'))
    massages=getMessagesByChatId(chat['id'])
    if request.method=='POST':
        text=request.form['text']
        date_time = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
        createMessage(text,date_time,chat[id],session.get('id'))
        return redirect(url_for('chat',email=email))
    return render_template('chat.html',id=userId2['id'], massages=massages, partnerEmail=email)

@app.route('/chatList',methods=['GET','POST'])
def chatList():
    chats=getChatsWithClientById(session.get('id'))
    client_id=session.get('id')
    for i in range(len(chats)):
        if chats[i]["first_client_id"] == client_id:
            chats[i].update({"chat_with": getUserById(chats[i]["second_client_id"])["email"]})
        elif chats[i]["second_client_id"] == client_id:
            chats[i].update({"chat_with": getUserById(chats[i]["first_client_id"])["email"]})
    return render_template('chatList.html',chats=chats)
app.run(host='0.0.0.0', port=81)