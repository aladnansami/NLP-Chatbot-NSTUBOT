# import all required packages

from flask import Flask, render_template, request, redirect, session, flash,request
import mysql.connector
import os
import pymongo
import datetime
# import speech_recognition as sr
import pyttsx3
import nltk
nltk.download('popular')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from keras.models import load_model
model = load_model('model.h5')
import json
import random
intents = json.loads(open('data.json').read())
words = pickle.load(open('texts.pkl','rb'))
classes = pickle.load(open('labels.pkl','rb'))

def clean_up_sentence(sentence):
    # tokenize for the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


###################-------------- creating sessions------------------------------------------ ##########################

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.urandom(24)


###################################------------------MYSQL---------------------########################################

conn = mysql.connector.connect(host="localhost", user="root", password="", database="chatbot_application")
cursor = conn.cursor()


###################------------------rendering first page INDEX PAGE---------------------##############################

@app.route('/')
def index():
    return render_template('index.html')

###################------------------rendering LOGIN PAGE---------------------##############################

@app.route('/login')
def login():
    return render_template('login.html')

#############----------------If LOGIN successful then go to index page-------------------##############################

@app.route("/home")
def home():
    if 'user_id' in session:
        return render_template("/index.html")
    else:
        return redirect('/')


#############---------------- sending and retrieving data and storing in MONGODB -------------------####################

@app.route("/get")
def get_bot_response():

    # userText = request.args.get('msg')
    global USER_TEXT,CHATBOT_RESPONSE
    USER_TEXT = request.args.get('msg')
    
    CHATBOT_RESPONSE=chatbot_response(USER_TEXT)
    cursor.execute("INSERT INTO queries(user_id, user_text, chatbot_response) VALUES (%s,%s,%s)",(session["user_id"],USER_TEXT,CHATBOT_RESPONSE))    
    conn.commit()


    return CHATBOT_RESPONSE
    # client = pymongo.MongoClient(
    # "mongodb + srv: // aladnansami:!87654321Aa@cluster0.d81fvmf.mongodb.net /?retryWrites = true & w = majority"
    # )
    #
    # myDb = client['chat_bot']
    # myDbCol = myDb["qus_ans_data"]
    # userText = request.args.get('msg')
    # myDict = {
    #     "user_data": userText,
    #     "bot_data": str(chatbot_response(userText)),
    #     "date": datetime.datetime.now()
    # }
    # x = myDbCol.insert_one(myDict)


    # reply with voice
    #botResponse = flaskybot_train.chat_response(userText)
    # engine = pyttsx3.init()
    # rate = engine.getProperty("rate")
    # engine.setProperty("rate", 80)
    # engine.say(botResponse)
    # client.close()
    # engine.runAndWait()
    # return str(botResponse)


##########################---------------- AFTER CLICKING MIC : VOICE  -------------------##############################
#
# @app.route('/speech', methods=["POST"])
# def speech():
#     if request.method == "POST":
#         r = sr.Recognizer()
#         engine = pyttsx3.init()
#
#         with sr.Microphone() as source:
#             audio = r.listen(source)
#
#             try:
#                 userText = request.args.get('msg')
#                 text = r.recognize_google(audio)
#                 if text in str(chatbot_response(userText)):
#                     reply = userText
#                     rate = engine.getProperty("rate")
#                     engine.setProperty("rate", 100)
#                     engine.say(reply)
#                     engine.runAndWait()
#                     return render_template('index.html')
#
#             except:
#                             error = "Sorry, can't read"
#                             engine.say(error)
#                             engine.runAndWait()
#                             return render_template('index.html')
#             else:
#                     return render_template('index.html')

###############################----------------LOGIN_VALIDATION--------------------#####################################

@app.route('/login_validation', methods=['POST'])
def login_validation():
    
    if 'admin_id' in session:
        session.pop('admin_id')
    
    email = request.form.get('email')
    pwd = request.form.get('pwd')

    cursor.execute("SELECT * FROM user WHERE email = %s AND pwd = %s ", (email, pwd))
    users = cursor.fetchall()
    if len(users) > 0:

        session['user_id'] = users[0][3]
        flash('Logged in Successfully!')
        return redirect('/home')
    else:
        flash('Entered Details already exists or are  Invalid Password ')
        return redirect('/')


###########################---------------- RENDERING REGISTER PAGE -------------------#################################

@app.route('/register')
def register():
    return render_template('registration.html')


#############################---------------- NEW  REGISTRATION -------------------####################################

@app.route('/register_validation', methods=['POST'])
def register_validation():
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    pwd = request.form.get('pwd')

    if not len(pwd) >= 5:
        flash('Password must be at least 5 characters in length')
        return render_template('registration.html')
    else:

        cursor.execute("INSERT INTO user (fname,lname,email,pwd) VALUES (%s,%s,%s,%s)", (fname, lname, email, pwd))

        conn.commit()
        #conn.close()
        
        # return render_template('index.html')
        flash('Registration Successfully!')
        return redirect('/home')



################################------------------FEED BACK---------------#################################################
@app.route('/user_feedback', methods=['POST'])
def user_feedback():
    feed_back_type = request.form.get('feed_back_type')
    feed_back_msg = request.form.get('feed_back_msg')

    cursor.execute("INSERT INTO feed_back(feed_back_msg,feed_back_type,user_text,bot_response) VALUES (%s,%s,%s,%s)",(feed_back_msg,feed_back_type,USER_TEXT,CHATBOT_RESPONSE))
    
    conn.commit()
    #conn.close()

    flash("Feedback Submitted")
    return redirect('/home')

###########################---------------- RENDERING ADMIN PAGE -------------------#################################

@app.route('/admin')
def admin():
    if 'admin_id' in session:
        cursor.execute("SELECT feed_back_id,feed_back_msg, user_text, bot_response FROM feed_back WHERE feed_back_type=(%s)",("false",))
        feedback_data = cursor.fetchall()
        return render_template('admin.html',feedback_data=feedback_data)
    else:
        return redirect('/')

################################------------------DELETING FEEDBACK---------------#################################################
@app.route('/delete_feedback', methods=['POST'])
def delete_feedback():
    feed_back_id = request.form.get('feed_back_id')

    cursor.execute("DELETE FROM feed_back WHERE feed_back_id=(%s)",(feed_back_id,))
    conn.commit()

    flash("Feedback Deleted")
    return redirect('/admin')

################################------------------ADDING NEW QUERY---------------#################################################
@app.route('/add_query', methods=['POST'])
def add_query():
    tag=request.form.get('tag')
    patterns=request.form.get('patterns')
    responses=request.form.get('responses')
    context=request.form.get('context')
    feedback_id=request.form.get('eidtable_feed_back_id')

    cursor.execute("INSERT INTO new_query_data(feed_back_id, tag, patterns, responses, context) VALUES (%s,%s,%s,%s,%s)",(feedback_id,tag,patterns,responses,context))
    cursor.execute("DELETE FROM feed_back WHERE feed_back_id=(%s)",(feedback_id,))
    
    conn.commit()
    
    flash("Query Added")
    return redirect('/admin')

###########################---------------- RENDERING ADMIN LOGIN PAGE -------------------#################################
@app.route('/admin/login')
def admin_login():
    return render_template('admin_login.html')


################################------------------ADMIN VALIDATION---------------#################################################

@app.route('/admin/login_validation',methods=['POST'])
def admin_login_validation():
    
    if 'user_id' in session:
        session.pop('user_id')
    
    email = request.form.get('email')
    pwd = request.form.get('pwd')

    cursor.execute("SELECT * FROM admin WHERE email = %s AND pwd = %s ", (email, pwd))
    users = cursor.fetchall()
    if len(users) > 0:
        session['admin_id'] = users[0][0]
        flash('Logged in Successfully!')
        return redirect('/admin')
    else:
        flash('Entered Details already exists or are  Invalid Password ')
        return redirect('/')


################################------------------ADMIN LOGOUT---------------#################################################
@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_id')
    return redirect('/admin/login')


################################------------------LOGOUT---------------#################################################

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/login')

#########################################------MAIN-----------##########################################################

if __name__ == "__main__":
    app.run(debug=True)