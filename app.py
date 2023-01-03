# import packages

from flask import Flask, render_template, request, redirect, session, flash,request
#import flaskybot_train
import mysql.connector
import os
import pymongo
import datetime
#import speech_recognition as sr
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
    # tokenize the pattern - split words into array
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

conn = mysql.connector.connect(host="localhost", user="root", password="", database="login_validation")
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
    userText = request.args.get('msg')
    return chatbot_response(userText)
    # client = pymongo.MongoClient(
    #     #"mongodb+srv://demo:demo@cluster0.kll4c.mongodb.net/chat_bot?retryWrites=true&w=majority"
    #     "mongodb+srv://masum1834e:masum1834e@cluster0.avsxlxx.mongodb.net/?retryWrites=true&w=majority"
    # )

    # myDb = client['chat_bot']
    # myDbCol = myDb["qus_ans_data"]
    # userText = request.args.get('msg')
    # myDict = {
    #     "user_data": userText,
    #     #"bot_data": str(flaskybot_train.chat_response(userText)),
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
#                 if text in str(flaskybot_train.chat_response(userText)):
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
        conn.close()
        
        # return render_template('index.html')
        flash('Registration Successfully!')
        return redirect('/home')

################################------------------LOGOUT---------------#################################################

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/login')

#########################################------MAIN-----------##########################################################

if __name__ == "__main__":
    app.run(debug=True)