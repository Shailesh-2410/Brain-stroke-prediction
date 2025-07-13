from flask import Flask, render_template, Response, request, flash,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, UserMixin, logout_user
import pickle
import numpy as np
import pandas as pd


app = Flask(__name__)

model = pickle.load(open('brainstroke_model.pkl', 'rb'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SECRET_KEY'] = 'thisissecret'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fname = db.Column(db.String(80), nullable=False)
    lname = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    def __repr__(self):
        return '<User %r>' % self.username 
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()


@app.route('/register', methods=['GET', 'POST'])   
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('uname')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        user = User(email=email, password=password, username=username, fname=fname, lname=lname)
        db.session.add(user)
        db.session.commit()
        flash('user has been registered successfully','success')
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login1():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and password == user.password:
            login_user(user)
            return redirect('/stroke')
        else:
            flash('Invalid Credentials', 'warning')
            return redirect('/login')
    return render_template('login.html')




@app.route('/')
def index():
    return render_template("index.html")

@app.route('/aboutus')
def About():
    return render_template("aboutus.html")

@app.route('/abstract')
def abstract():
    return render_template("abstract.html")

@app.route('/contactus')
def contactus():
    return render_template("contactus.html")


@app.route('/Model')
def Model():
    return render_template("Model.html")

@app.route('/stroke')
def Stroke():
    return render_template('stroke.html')

#@app.route('/predict')
#def Predict():
#    return render_template('predict.html')

@app.route('/predict1')
def Predict1():
    return render_template('predict1.html')

@app.route('/predict2')
def Predict2():
    return render_template('predict2.html')





@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        #name = request.form['name']
        age = request.form['age']
        maritalstatus = request.form['maritalstatus']
        worktype = request.form['Worktype']
        residence = request.form['Residence']
        gender = request.form['gender']
        bmi = request.form['bmi']
        gluclevel = request.form['gluclevel']
        smoke = request.form['Smoke']
        hypertension = request.form['Hypertension']
        heartdisease = request.form['Heartdisease']
        #model = pickle.load(open('stroke_new.pkl','wb'))

        res={'urban':1,'rural':0}
        gen={'Female':0,'Male':1}
        msts={'married':1,'not married':0}
        wktype={'privatejob':2,'govtemp':1,'selfemp':3, 'children':0}
        smke={'formerly-smoked':0,'non-smoker':1,'smoker':2, 'Unknown':3}
        hypten={'hypten':1,'nohypten':0}
        hrtdis={'heartdis':1,'noheartdis':0}

        residence=res[residence]
        gender=gen[gender]
        maritalstatus=msts[maritalstatus]
        worktype=wktype[worktype]
        smoke=smke[smoke]
        hypertension=hypten[hypertension]
        heartdisease=hrtdis[heartdisease]


        #model=pd.read_pickle('strokenew.pkl')

        array = [[gender,age,hypertension,heartdisease,maritalstatus,worktype,residence,gluclevel,bmi,smoke]]

        array = [np.array(array[0],dtype = 'float64')]
        pred_stroke = model.predict(array)
        result = int(pred_stroke[0])
        str=""
        if result == 0:
            return render_template('Predict1.html', prediction_text= 'You are not suffering from Brain Stroke')
        else:
            return render_template('Predict2.html', prediction_text= 'Ouch! You are suffering from Brain Stroke')


        # if result==0:
        #     str = name + ", you will not get stroke 😀"
        # else:
        #     str = name + ", you will get stroke 😔"
        # return render_template('predict.html',a = str)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8081, debug=True)
