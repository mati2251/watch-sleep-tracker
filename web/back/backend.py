from flask import Flask, jsonify, g
from flask_cors import CORS
import sqlite3

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

@app.route('/data')
def get_data():
    data = list(zip(*query_db("""SELECT 
                                    hr, ibi, rmssd, sdnn, stress_score, time(datetime(Timestamp, \'unixepoch\', \'localtime\')) 
                                    FROM heart_rate_data WHERE Date in (SELECT max(date(Date)) FROM heart_rate_data) ORDER BY Timestamp""")))
    labels = ['hr', 'ibi', 'rmssd', 'sdnn', 'stress_score', 'timestamp'] 
    return jsonify(dict(zip(labels, data)))

@app.teardown_appcontext
def close_connection(_):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
