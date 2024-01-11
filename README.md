# Watch Sleep Tracker
## Idea
Watch Sleep Tracker is a watch device that can track your sleep quality by monitoring your heart rate and provide advice to improve your sleep.
## Realization
The watch is based on Raspberry Pi Zero 2 W and has a 1.3 inch OLED screen controlled by two buttons. To analyze sleep quality, we use a heart rate sensor that is connected via Bluetooth (in our case, the Lezyne HR Sensor). When the watch detects the sensor, it starts monitoring the heart rate and saves the data to a database. After sleep, the watch analyzes the data and provides advice through a webpage.
## Function
### Watch
- Time
- Countdown
- Alarm
### Sleep Analysis
- Sleep Quality
- Sleep Time
- Sleep Advice
- Avg Heartrate
- Lowest Heartrate
