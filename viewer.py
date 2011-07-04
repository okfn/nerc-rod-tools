import sqlite3
from flask import Flask, g, json, render_template

# configuration
DATABASE = 'rod.db'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
            for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def grant_summary(grant_id):
    results = {}
    outputs = query_db('select rod_id,outputs_year from rod_outputs where reference_no is ?', (grant_id,))
    tables = [
        'achievements', 'communications', 'education', 'engagement', 'fellows',
        'impact', 'income', 'patents', 'policy', 'policy3', 'publication_totals',
        'publications', 'support', 'prizes'
    ]

    for o in outputs:
        rod_id = o['ROD_ID']
        results[o['OUTPUTS_YEAR']] = y = {}
        for t in tables:
            y[t] = query_db('select * from rod_%s where rod_id is ?' % t, (rod_id,))

    return results


@app.before_request
def before_request():
    g.db = connect_db()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route("/")
def home():
    return render_template('layout.html')

@app.route('/grant')
def list_grant():
    grants = query_db('select reference_no from rod_grants limit 200')
    return render_template('grant_list.html', grants=grants)

@app.route('/grant/<path:grant_id>')
def show_grant(grant_id):
    res = grant_summary(grant_id)
    return render_template('grant_summary.html',
                           ref=grant_id,
                           years=res.keys(),
                           outputs=res)

if __name__ == "__main__":
    app.run()