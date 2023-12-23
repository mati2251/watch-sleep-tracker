import sqlite3
import numpy as np
import datetime
import asyncio
from bleak import BleakClient

class HeartRateDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.initialize_db()

    def initialize_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''DROP TABLE IF EXISTS heart_rate_data''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS heart_rate_data (
                    id integer PRIMARY KEY AUTOINCREMENT,
                    HR NUMBER,
                    IBI NUMBER,
                    RMSSD NUMBER,
                    SDNN NUMBER,
                    Stress_Score NUMBER,
                    Timestamp NUMBER
                )
            ''')

    def insert_data(self, hr_data):

        hr_data['Timestamp'] = int(datetime.datetime.now().timestamp())


        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO heart_rate_data (HR, IBI, RMSSD, SDNN, Stress_Score, Timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (hr_data['HR'], hr_data['IBI'], hr_data['RMSSD'], hr_data['SDNN'], hr_data['Stress_Score'], hr_data['Timestamp']))
            conn.commit()

class SleepAnalysisDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.initialize_db()

    def initialize_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            # Check if the table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sleep_analysis_results'")
            if cursor.fetchone():
                # If the table exists, drop it
                cursor.execute('DROP TABLE sleep_analysis_results')

            # Create the table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sleep_analysis_results (
                    Date NUMBER,
                    Analysis VARCHAR2
                )
            ''')

    def insert_analysis(self, date, analysis):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sleep_analysis (Date, Analysis)
                VALUES (?, ?)
            ''', (date, analysis))
            conn.commit()

class HeartRateAnalyzer:
    @staticmethod
    def analyze_sleep(hr_data):
        avg_hr_threshold = 60
        sdnn_threshold = 50
        rmssd_threshold = 30

        avgHr = np.mean(hr_data['HR'])
        avgSdnn = np.mean(hr_data['SDNN'])
        avgRmssd = np.mean(hr_data['RMSSD'])

        if avgHr < avg_hr_threshold and avgSdnn > sdnn_threshold and avgRmssd > rmssd_threshold:
            return "Wygląda na to, że miałeś spokojny sen w zeszłej nocy! Twoje dane dotyczące tętna wskazują na dobrą jakość snu."
        elif avgHr > avg_hr_threshold and avgSdnn < sdnn_threshold and avgRmssd < rmssd_threshold:
            return "Twój sen może nie był bardzo spokojny. Dane dotyczące tętna sugerują, że twoje ciało mogło nie być zrelaksowane w nocy."
        else:
            return "Twoja analiza snu jest nieco mieszana. Chociaż średnie tętno było niskie, co jest dobre, wskaźniki zmienności tętna nie były optymalne, co może wskazywać na pewne zakłócenia snu."

    @staticmethod
    def calculate_rmssd(ibi_values):
        if len(ibi_values) < 2:
            return None
        squared_differences = np.diff(ibi_values) ** 2
        mean_squared_diff = np.mean(squared_differences)
        return np.sqrt(mean_squared_diff)

    @staticmethod
    def calculate_sdnn(ibi_values):
        if len(ibi_values) < 2:
            return None
        return np.std(ibi_values)

    @staticmethod
    def calculate_stress_score(hr, rmssd, sdnn, max_hr=110, max_rmssd=50, max_sdnn=50):
        normalized_hr = min((hr - 45) / (max_hr - 45), 1)
        normalized_rmssd = min((rmssd - 5) / (max_rmssd - 5), 1)
        normalized_sdnn = min(sdnn / max_sdnn, 1)

        stress_from_hr = normalized_hr
        stress_from_rmssd = 1 - normalized_rmssd
        stress_from_sdnn = 1 - normalized_sdnn

        final_stress_score = (stress_from_hr * 0.4 + stress_from_rmssd * 0.3 + stress_from_sdnn * 0.3) * 100

        return final_stress_score

class HeartRateMonitor:
    def __init__(self, address, hr_measurement_char_uuid):
        self.address = address
        self.hr_measurement_char_uuid = hr_measurement_char_uuid
        self.ibi_values = []
        self.ibi_timestamps = []
        self.all_heart_rate_data = []
        self.hr_db = HeartRateDatabase('heart_rate_data.db')
        self.analysis_db = SleepAnalysisDatabase('sleep_analysis_results.db')




    async def start_monitoring(self):
        while True:
            try:
                async with BleakClient(self.address) as client:
                    connected = await client.is_connected()
                    print(f"Connected: {connected}")

                    if connected:
                        await client.start_notify(self.hr_measurement_char_uuid, self.handle_rr_intervals)

                        while await client.is_connected():
                            await asyncio.sleep(1)

                        await client.stop_notify(self.hr_measurement_char_uuid)

                        if self.is_data_same_last_five_minutes():
                            aggregated_data = {
                                "HR": [data["HR"] for data in self.all_heart_rate_data],
                                "RMSSD": [data["RMSSD"] for data in self.all_heart_rate_data],
                                "SDNN": [data["SDNN"] for data in self.all_heart_rate_data]
                            }
                            analysis = HeartRateAnalyzer.analyze_sleep(aggregated_data)
                            self.analysis_db.insert_analysis(int(datetime.datetime.now().timestamp()), analysis)
                            print("Analysis inserted to SQLite:", analysis)

            except Exception as e:
                print(f"An error occurred: {e}")

            print("Trying to reconnect in 5 minutes...")
            await asyncio.sleep(10)

    def handle_rr_intervals(self, sender, data):
        if data[1] != 0:
            interval = int(60000 / data[1])
            current_timestamp = int(datetime.datetime.now().timestamp())
            self.ibi_values.append(interval)
            self.ibi_timestamps.append(current_timestamp)

            rmssd = HeartRateAnalyzer.calculate_rmssd(self.ibi_values)
            sdnn = HeartRateAnalyzer.calculate_sdnn(self.ibi_values)

            stress_score = HeartRateAnalyzer.calculate_stress_score(data[1], rmssd, sdnn)

            heart_rate_data = {
                "HR": data[1],
                "IBI": interval,
                "RMSSD": rmssd,
                "SDNN": sdnn,
                "Stress_Score": stress_score,
                "Timestamp": int(datetime.datetime.now().timestamp())
            }

            self.all_heart_rate_data.append(heart_rate_data)

            self.hr_db.insert_data(heart_rate_data)
            print("Data inserted to SQLite:", heart_rate_data)
        else:
            print("Skipping division by zero")
        print("----------")

        def is_data_same_last_five_minutes(self):
            current_time = int(datetime.datetime.now().timestamp())
            five_minutes_ago = current_time - 300  #

            recent_data = [hr for timestamp, hr in self.all_heart_rate_data if timestamp >= five_minutes_ago]

            return len(set(recent_data)) == 1

monitor = HeartRateMonitor("D3:B2:8E:7E:AA:C5", "00002a37-0000-1000-8000-00805f9b34fb")
asyncio.run(monitor.start_monitoring())
