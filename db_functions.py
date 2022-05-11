import sqlite3
from flask import session, g
from db import get_db

def do_login(email, password: str) -> bool:
    loginsuccess = False
    mydb = get_db()
    print("searching for {}".format(email))
    user = mydb.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    if user is not None:
        print("found {}".format(user))
        if user['upassword'] == password:
            loginsuccess = True
            session['email'] = user['email']
            session['uname'] = user['alias']
    return loginsuccess

def add_score(score: int, email):
    uid = session['email']
    print(email)
    print(score)
    mydb = get_db()
    mydb.execute('UPDATE users SET score = ? WHERE email = ? ', (score, email))
    print('score added')
    mydb.commit()

def get_questions() -> list:
    questions = []
    mydb = get_db()
    row = 0
    counter = 1
    for row in mydb.execute('SELECT question, a, b, c, d, answer FROM questions'):
        questions.append(row)
       

    return questions

def get_score(email) ->int:
    mydb = get_db()
    user = mydb.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    grade = user['score']
    print(grade)
    return grade
    
def get_users() -> list:
    users = []
    mydb = get_db()
    for row in mydb.execute('SELECT email, upassword, alias, score FROM users'):
        users.append(row)

    return users

def add_questions(q, choicea, choiceb, choicec, choiced, ans):
    uid = session['email']
    mydb = get_db()
    mydb.execute('INSERT INTO questions (question, a, b, c, d, answer) VALUES(?,?,?,?,?,?)', (q, choicea, choiceb, choicec, choiced, ans))
    mydb.commit()
    print('inserted to questions')


def remove_questions(q):
    uid = session['email']
    mydb = get_db()
    mydb.execute('DELETE FROM questions WHERE question = ?', [q])
    mydb.commit()
    print('deleted question')

def add_user(em, passw, ali):
   
    mydb = get_db()
    mydb.execute('INSERT INTO users (email, upassword, alias, score) VALUES(?,?,?,?)', (em, passw, ali,0))
    mydb.commit()
    print(em)
    print(passw)
    print(ali)
    print('user added')