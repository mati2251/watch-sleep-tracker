from screen import TimeScreen, ScreenStrategy
import adafruit_ssd1306
import busio
from board import SCL, SDA


i2c = busio.I2C(SCL, SDA)
display: adafruit_ssd1306.SSD1306_I2C = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
screen: ScreenStrategy = TimeScreen(display)
screen.start()
