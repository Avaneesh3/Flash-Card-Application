from flask import Flask, render_template, request, redirect, url_for, Response
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import io
import csv
import smtplib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///card2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager() 
login_manager.init_app(app)
login_manager.login_view = 'login'
Bootstrap(app)

   
class User(UserMixin,db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    db.relationship = ('Scores')

    def __repr__(self) -> str:
        return f"{self.id } - {self.username}"
#                       - - - - - - - - - - - - MARKS DATABASE FOR PERIODIC TABLE - - - - - - - - - - -
class marksu(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
#                       - - - - - - - - - - - - POINTS DATABASE FOR COMPOUNDS TABLE - - - - - - - - - - -
class pointsu(db.Model): 
    sno = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

#                               - - - - - - - - - -LOGIN  VALIDATION - - - - - - 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message ='Invalid Email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


#     - - - - - - - - - - - - - - - - - - - - - - - -PERIODIC TABLE DATABASE - - - - - - - - - - - - - - - - - 
class QnA(db.Model):
    SrNo = db.Column(db.Integer,primary_key = True)
    question = db.Column(db.String(200),nullable = False)
    answer = db.Column(db.String(500),nullable = False)
 

def __repr__(self) -> str:
        return f"{self.SrNo} - {self.question}"
#                              - - - - - - - - -LIST FOR STORING SCORES IN PYTHON- - - - - - - - - - -   
l= []
k= []
#                                      - - - - - - - -COMPOUNDS DATABASE- - - - - - - - - - - - - 
class Compounds(db.Model):
    SrNo = db.Column(db.Integer,primary_key = True)
    compound_name = db.Column(db.String(200),nullable = False)
    compound_formula = db.Column(db.String(500),nullable = False)
 

def __repr__(self) -> str:
        return f"{self.SrNo} - {self.compound_name}"

#                                        - - - - - - - -COMPOUNDS ROUTES- - - - - - 

@app.route('/compounds', methods=['GET', 'POST'])
def hello_compounds():
    if request.method=='POST':
        compound_name = request.form['compound_name']
        compound_formula = request.form['compound_formula']
        newcompound = Compounds(compound_name = compound_name, compound_formula = compound_formula)
        db.session.add(newcompound)
        db.session.commit()
        
    allcompounds = Compounds.query.all() 
    return render_template('comindex.html', allcompounds = allcompounds)



@app.route('/updatecom/<int:SrNo>', methods=['GET', 'POST'])
def updatecom(SrNo):
    if request.method=='POST':
        compound_name = request.form['compound_name']
        compound_formula = request.form['compound_formula']
        com = Compounds.query.filter_by(SrNo=SrNo).first()
        com.compound_name = compound_name
        com.compound_formula = compound_formula
        db.session.add(com)
        db.session.commit()
        return redirect("/compounds")
        
    com = Compounds.query.filter_by(SrNo=SrNo).first()
    return render_template('comupdate.html', com = com)

@app.route('/deletecom/<int:SrNo>')
def deletecom(SrNo):
    com = Compounds.query.filter_by(SrNo=SrNo).first()
    db.session.delete(com)
    db.session.commit()
    return redirect("/compounds") 
#                               - - - - - - - -COMPOUNDS TABLE CREATE UPDATE DELETE- - - - - - 


@app.route('/com/<int:SrNo>', methods=['GET', 'POST'])
def comupdate(SrNo):
    lll = len(k)
    x = Compounds.query.all()
    yy = len(x)  
    print(yy) 
    com = Compounds.query.filter_by(SrNo=SrNo).first()
    if request.method == 'POST':
        compound_formula1 = request.form['compound_formula'] 
        if com.compound_formula == compound_formula1:
            if com.SrNo == yy:
                f = pointsu(score = lll + 1,name = current_user.username)
                db.session.add(f)
                db.session.commit()
            k.append(1)
            print(lll)                        
            return render_template('comcheck.html', com = com, yy = yy,lll = lll)
        else:
            if com.SrNo == yy:
                f = pointsu(score = lll,name = current_user.username)
                db.session.add(f)
                db.session.commit()           
            return render_template('comcheckagain.html', com = com, yy = yy,lll = lll)
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login("ak3502990@gmail.com","A$123456")
    SUBJECT = "Score Report"  + " for " + current_user.username
    pescore = lll
    TEXT = "You have scored " + str(pescore) + " out of " + str(yy) + " in Compounds flashcards review."
    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    server.sendmail("ak3502990@gmail.com","ak3502990@gmail.com",message)
    server.quit()          
    return render_template('com-n-form.html',com = com, yy = yy)
    
#                               - - - - - - - -PERIODIC TABLE CREATE UPDATE DELETE- - - - - - 

@app.route('/todo', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        question = request.form['question']
        answer = request.form['answer']
        newqna = QnA(question = question, answer = answer)
        db.session.add(newqna)
        db.session.commit()
        
    allqna = QnA.query.all() 
    return render_template('todoindex.html', allqna = allqna)



@app.route('/update/<int:SrNo>', methods=['GET', 'POST'])
def updatetodo(SrNo):
    if request.method=='POST':
        question = request.form['question']
        answer = request.form['answer']
        qna = QnA.query.filter_by(SrNo=SrNo).first()
        qna.question = question
        qna.answer = answer
        db.session.add(qna)
        db.session.commit()
        return redirect("/todo")
        
    qna = QnA.query.filter_by(SrNo=SrNo).first()
    return render_template('todoupdate.html', qna = qna)

@app.route('/delete/<int:SrNo>')
def delete(SrNo):
    qna = QnA.query.filter_by(SrNo=SrNo).first()
    db.session.delete(qna)
    db.session.commit()
    return redirect("/todo") 
#                             - - - - - - - - - - - INDEX/HOME PAGE FOR LOGIN - - - - - - - - - - - -   
@app.route('/') 
def index():   
    return render_template('index.html')

#                             - - - - - - - - - - - START PAGE FOR PERIODIC TABLE - - - - - - - - - - - -     
@app.route("/welcome")
def helloworld():
    all = marksu.query.all()
    return render_template('welcome.html', all = all)

#                             - - - - - - - - - - - START PAGE FOR COMPOUNDS TABLE - - - - - - - - - - - -     
@app.route("/comwelcome")
def hellocom():
    every = pointsu.query.all()
    return render_template('comwelcome.html', every = every)

@app.route("/flashes")
def helloflash():
    return render_template('flashes.html')

@app.route('/login',methods = ['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user, remember=form.remember.data)
                return render_template('dashboard.html')
        return 'Invalid username or password' 


    return render_template('login.html', form = form)

@app.route('/newuser')
def newuser():
    return render_template('newuser.html')

@app.route('/signup',methods = ['GET','POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(username = form.username.data, email = form.email.data, password = form.password.data)
        db.session.add(new_user)
        db.session.commit()

        return render_template('newuser.html')

    return render_template('signup.html', form = form)

#                          - - - - - - - - - - - - -USER DASHBOARD - - - - - - - - - - -
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)
 
@app.route('/downloaddecks')
@login_required
def download_report():  
    try:
            result = Compounds.query.all()
            print(result) 
            
            output = io.StringIO()
            writer = csv.writer(output)
             
            line = ['SrNo,compound_name,compound_formula']
            writer.writerow(line)
            
            for row in result:
                line = [str(row.SrNo) + ", " + row.compound_name + ", " + row.compound_formula]
                writer.writerow(line)
                
                output.seek(1)
                
                return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=compunds_deck.csv"})
    except Exception as e:
        print(e) 
    

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
#                          - - - - - - - - - - - - PERIODIC TABLE FLASHCARD ROUTES- - - - - - - - - - - - 
@app.route('/<int:SrNo>', methods=['GET', 'POST'])
def update(SrNo):
    ll = len(l)  
    x = QnA.query.all()
    y = len(x)  
    print(y) 
    todo = QnA.query.filter_by(SrNo=SrNo).first()
    if request.method == 'POST':
        answer1 = request.form['answer'] 
        if todo.answer == answer1:
            l.append(1)
            if todo.SrNo == y:
                f = marksu(score = ll + 1, name = current_user.username )
                db.session.add(f)
                db.session.commit()
            print(ll)                        
            return render_template('check2.html', todo = todo, y = y,ll = ll)
        else: 
            if todo.SrNo == y:
                f = marksu(score = ll, name = current_user.username )
                db.session.add(f)
                db.session.commit()           
            return render_template('checkagain2.html', todo = todo, y = y,ll = ll)     
    return render_template('qna.html',todo = todo, y = y)
     
            
if __name__ == "__main__":
    app.run(debug = True,port =7000)  
