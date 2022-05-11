from flask import Flask, render_template, request, redirect, session, Response
import os
import db
from db_functions import do_login, get_questions, add_user, add_questions, remove_questions, get_users, add_score, get_score
import  optparse
#app=Flask( __name__ , template_folder="templates")
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'home.sqlite'),
    )

try:
    os.makedirs(app.instance_path)
except OSError:
    pass
db.init_app(app)

#--------------|
#----SETUP-----|
#--------------|


#classes
class QuizItem1:
    question= ""
    choicea= ""
    choiceb= ""
    choicec= ""
    choiced= ""
    answer= ""
    qnum= ""
    
class QuizItem2:
    question= ""
    answer= ""
    qnum= ""

class ResultValue:
    name= ""
    email= ""
    grade= ""


#storage
allemails=[]
allpasswords=[]
allcredentials=[]
email = ""
password = ""
name = ""
authentic = ""


#In textfiles, each line is a new user or a new quiz item. The each component
# of users' credentials or quiz components are separated by commas
#this function separated each item into its constituents

def putItem(line, itemnum):
    
    tempstore=""
    counter=''
    i=0
    commacounter=0   
   
    while ( commacounter < itemnum+1 and i < len(line)):
        
        counter=line[i]
        
        if counter == ',':
            commacounter+=1
        elif commacounter == itemnum:
            tempstore=tempstore+counter
        i+=1    
    return tempstore


#functions for creating models for quiz items, score items

def create_quizitem1(listElement ,itemnum):
    
    quizitem1=QuizItem1()
    quizitem1.question= listElement[0]
    quizitem1.choicea= listElement[1]
    quizitem1.choiceb= listElement[2]
    quizitem1.choicec= listElement [3]
    quizitem1.choiced= listElement[4]
    quizitem1.answer= listElement[5]
    quizitem1.qnum= itemnum
    
    return quizitem1


def create_quizitem2(listElement ,itemnum):
    
    quizitem2=QuizItem2()
    quizitem2.question= putItem(listElement, 0)
    quizitem2.answer= putItem(listElement, 5)
    quizitem2.qnum= itemnum
    
    return quizitem2

def creating_results(listElement):
    r= ResultValue()
    r.name= listElement[2]
    r.email= listElement[0]
    r.grade= listElement[3]
    return r
 
 
#--------------|
#----ROUTES----|
#--------------|

@app.route("/quiz" , methods=["POST","GET"])
def quiz():
    quiz_no = 0
    entire = []
    questions = []
    
    questions = get_questions()
    
    
    for element in questions:
        quiz_no+=1
        obj= create_quizitem1(element, quiz_no)
        entire.append(obj)
    
    quiz_no=0
    page = render_template("quiz.html" , array=entire)
    return Response(page,status=200)

@app.route("/adminq" , methods=["POST","GET"])
def adminq():
    quiz_no = 0
    entire = []
    questions = []

    questions = get_questions()
    
    for element in questions:
        quiz_no+=1
        obj= create_quizitem1(element, quiz_no)
        entire.append(obj)
    
    quiz_no=0
    page = render_template("adminquiz.html" , array=entire)
    return Response(page, status=200)

@app.route("/")
@app.route("/index")
def home():
    
    email = None
    password = None

    if email=="admin@miami.edu" and password == "miam1":
        page = render_template("admin.html")
        return Response(page, status=200)
    elif email == None:
        session['email'] = email
        page = render_template("index.html")
        return Response(page, status=200)
    else:
        authentic = session['uname']
        page = render_template("user.html" , var=authentic)
        return Response(page,status=200)
        

#return render_template("showProd.html" , list= objects_list)

@app.route("/onsignup", methods=["POST","GET"])
def submit():
    
    email = None
    password = None
    name = None
    
    name=request.form.get('name')
    email=request.form.get('email')
    password=request.form.get('password')
    add_user(email, password, name)

    page = render_template("index.html")
    return Response(page, status=200)

@app.route("/onlogin" , methods=["POST","GET"])
def userVerify():
    
    email = None
    password = None

    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']
    else:
        email=request.form.get('email')
        password=str(request.form.get('password'))
    
    if email is not None and password is not None:
        login = do_login(email, password)
    else:
        login = False
    
    if login:
        page = render_template("user.html" , var=authentic)
        return Response(page, status=200)
    
    elif email=="admin@miami.edu" and password== "miami1":
        return render_template("admin.html")
    
    return render_template("invalid.html")
    

@app.route("/showall" , methods=["POST","GET"])
def showll():
    
    objects_list = []
    entire_thing= []
    entire_thing = get_users()

    for element in entire_thing:
        
        obj = creating_results(element)
        objects_list.append(obj)
        
    return render_template("showall.html" , list= objects_list)


@app.route("/addquestion" , methods=["POST","GET"])
def add_question():
    
    #have to edit for second question type
    ques=request.form.get('question')
    op1=request.form.get('op1')
    op2=request.form.get('op2')
    op3=request.form.get('op3')
    op4=request.form.get('op4')
    cor=request.form.get('corop')
    
    add_questions(ques, op1,op2,op3,op4,cor)
    return render_template("admin.html")

@app.route("/removequestion" , methods=["POST","GET"])
def remove_question():
    
    #have to edit for second question type
    ques=request.form.get('question')
    
    remove_questions(ques)
    return render_template("admin.html")
    
    
@app.route("/submit" , methods=["POST","GET"])
def submit_quiz():
    global email_add
    email_add = request.form.get('email_address')
   
    email = session['email']
    attempts = []
    score = 0
    entire= []
    
    questions = get_questions()
    number=0
    
    for item in questions:
        obj= create_quizitem1(item , number)
        entire.append(obj)
    
    for i in range(0,len(entire)):
        mcq="mcq"+str(i+1)
        attempts.append(request.form.get(mcq))
    
    for j in attempts:
        print(j)
    
    for i in range(0,len(entire)):
        if entire[i].answer == attempts[i]:
            score+=1
    
    add_score(score, email)

    print("Your score is:", score)
    return render_template("user.html")


@app.route("/login" , methods=["POST","GET"])
def validation():
    return render_template("login.html")


@app.route("/show" , methods=["POST","GET"])
def results():
    
    email = session['email']
    Credentials = []
    attempts = 0
    
    Credentials = get_users()
    
    score = get_score(email)
    print(email)

    return render_template("result.html" , var1=score, var2=attempts)

@app.route("/register" , methods=["POST","GET"])
def register():
    return render_template("register.html")

@app.route("/quizstrt" , methods=["POST","GET"])
def strt():
    return render_template("quizstrt.html")

@app.route("/add" , methods=["POST","GET"])
def add():
    return render_template("addques.html")

@app.route("/remove" , methods=["POST","GET"])
def remove():
    return render_template("removeques.html")

@app.route("/logout" , methods=["POST","GET"])
def logout():
    session.clear()
    #global email
    #global password
    #email = ""
    #password= ""
    return render_template("index.html")

if __name__ == "__main__":
    #app.run(debug= True , host="0.0.0.0")
    default_port = "8080"
    default_host = "0.0.0.0"
    parser = optparse.OptionParser()
    parser.add_option("-H", "--host",
                      help=f"Hostname of Flask app {default_host}.",
                      default=default_host)

    parser.add_option("-P", "--port",
                      help=f"Port for Flask app {default_port}.",
                      default=default_port)

    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug",
                      help=optparse.SUPPRESS_HELP)

    options, _ = parser.parse_args()

    app.run(
        debug=options.debug,
        host=options.host,
        port=int(options.port)
    )
