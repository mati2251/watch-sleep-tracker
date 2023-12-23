from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def query_db(database, query, args=(), one=False):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    con.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/getdata')
def get_data():
    data = query_db('heart_rate_data.db', 'SELECT * FROM heart_rate_data')
    return jsonify(data)

@app.route('/getanalysis')
def get_analysis():
    analysis_data = query_db('sleep_analysis_results.db', 'SELECT * FROM sleep_analysis')
    return jsonify(analysis_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
