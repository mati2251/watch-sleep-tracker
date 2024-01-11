# Watch Sleep Tracker
## Idea
Watch Sleep Tracker is a watch device that can track your sleep quality by monitoring your heart rate and provide advice to improve your sleep.
## Realization
The watch is based on Raspberry Pi Zero 2 W and has a 1.3 inch OLED screen controlled by two buttons. To analyze sleep quality, we use a heart rate sensor that is connected via Bluetooth (in our case, the Lezyne HR Sensor). When the watch detects the sensor, it starts monitoring the heart rate and saves the data to a database. After sleep, the watch analyzes the data and provides advice through a webpage.
![PXL_20240107_084534534](https://github.com/mati2251/watch-sleep-tracker/assets/33762646/c15f68a5-b5a0-470b-9199-f263a03deaca)
![obraz](https://github.com/mati2251/watch-sleep-tracker/assets/33762646/1de6e177-cbd4-41bc-abb8-4f033c4379ac)
### Short video (in Polish)
https://github.com/mati2251/watch-sleep-tracker/assets/33762646/68be3216-b355-4a33-a3db-43ee8126eecc
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
