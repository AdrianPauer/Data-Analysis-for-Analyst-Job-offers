from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)

def getSalaries():
    cur = g.db.cursor()
    cur.execute("""SELECT location,avgLow,avgHigh FROM salaries; """)
    toShow = []
    for row in cur:
            toShow.append('    '.join([row[0], str(row[1]), str(row[2])]))
    return toShow
def getPostsperSector():
    cur = g.db.cursor()   
    cur.execute("""SELECT sector,avgPosts FROM postsPerSectors; """)
    toShow = []                  
    for row in cur: 
        toShow.append('    '.join([row[0], str(row[1])]))                          
    return toShow  
def getRequiredTools():
    cur = g.db.cursor()
    cur.execute("""SELECT tool, occurences FROM requiredTools; """)
    toShow = []
    for row in cur:
            toShow.append((row[0], row[1]))
    return toShow

def getRequiredAtributes():
    cur = g.db.cursor()
    cur.execute("""SELECT atribute, occurences FROM requiredAtributes; """)
    toShow = []
    for row in cur:
        toShow.append((row[0],row[1]))
    return toShow

def connect_db():
    return sqlite3.connect('../analyst.db')

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/wat/<random_id>/')
def wat(random_id):
    cur = g.db.cursor()
    return "Random %s" % random_id

@app.route('/')
def home():
    salaries = getSalaries()
    perSector = getPostsperSector()
    tools = sorted(getRequiredTools(),key = lambda x : x[1],reverse = True)
    atributes = sorted(getRequiredAtributes(),key = lambda x : x[1],reverse = True)
    return render_template('main.html', salaries = salaries, perSector = perSector, tools = tools, atributes = atributes)

