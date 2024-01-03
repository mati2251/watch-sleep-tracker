import sqlite3
import datetime

class HeartRateTuple:
    def __init__(self, hr, ibi, rmssd, sdnn, stress_score, timestamp, date: datetime.date):
        self.hr = hr
        self.ibi = ibi
        self.rmssd = rmssd
        self.sdnn = sdnn
        self.stress_score = stress_score
        self.timestamp = timestamp
        self.date = date 

    def __str__(self):
        return 'HR: {}, IBI: {}, RMSSD: {}, SDNN: {}, Stress Score: {}, Timestamp: {}'.format(self.hr, self.ibi, self.rmssd, self.sdnn, self.stress_score, self.timestamp)

class HeartRateDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.initialize_db()

    def initialize_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS heart_rate_data (
                    id integer PRIMARY KEY AUTOINCREMENT,
                    HR NUMBER,
                    IBI NUMBER,
                    RMSSD NUMBER,
                    SDNN NUMBER,
                    Stress_Score NUMBER,
                    Timestamp NUMBER,
                    Date TEXT 
                )
            ''')

    def insert(self, hr_data: HeartRateTuple):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO heart_rate_data (HR, IBI, RMSSD, SDNN, Stress_Score, Timestamp, Date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (hr_data.hr, hr_data.ibi, hr_data.rmssd, hr_data.sdnn, hr_data.stress_score, hr_data.timestamp, hr_data.date.isoformat()))
            conn.commit()
