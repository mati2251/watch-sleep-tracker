from flask import Flask, json, g, render_template, request
from flask_cors import CORS
import sqlite3
import datetime

app = Flask(__name__)
CORS(app)
DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    with app.app_context():
        con = get_db() 
        cur = con.cursor()
        cur.execute(query, args)
        rv = cur.fetchall()
        con.close()
        return (rv[0] if rv else None) if one else rv

@app.route('/', methods=['GET'])
def page():
    date = request.args.get('date') if request.args.get('date') else datetime.date.today().strftime("%Y-%m-%d")
    print(date)
    data = list(zip(*query_db("""
                    SELECT
                    hr, Time(Timestamp - Timestamp%10, \'unixepoch\', \'localtime\')
                    FROM heart_rate_data
                    WHERE Date = ? 
                    GROUP BY Time(Timestamp - Timestamp%10, \'unixepoch\'  )ORDER BY Timestamp 
                    """ , args = [date])))
    stats = query_db("""
                     SELECT round(AVG(hr)), MIN(hr), round(AVG(Stress_Score)) 
                     FROM heart_rate_data WHERE Date = ?;
                    """, args = [date], one=True)
    hr = json.dumps(data[0]) if len(data) > 0 else json.dumps([])
    labels = json.dumps(data[1]) if len(data) > 0 else json.dumps([])
    low = stats[1] if stats[1] is not None else 0
    avg = stats[0] if stats[0] is not None else 0
    stress = stats[2] if stats[2] is not None else 0
    return render_template('index.html', hr=hr, labels=labels, low=low, avg=avg, stress=stress, date=date)

@app.teardown_appcontext
def close_connection(_):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
