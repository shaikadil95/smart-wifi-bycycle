import RPi.GPIO as GPIO
import time
import datetime
from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)

app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'pythonlogin'
mysql = MySQL(app)


def main():
    class person:
        def sensorCallback(channel):
          global sensorCounter
          global sensorStatus
          sensorStatus = True
          sensorCounter += 1

        def main1():
          try:
            global sensorCounter
            global sensorStatus
            sensorStatus = True
            sensorCounter = 0
            while True :
              if sensorStatus == True:
                print ("Sensor Counter   ", sensorCounter)
                sensorStatus = False

          except KeyboardInterrupt:
            # Reset GPIO settings
            GPIO.cleanup()
        # Tell GPIO library to use GPIO references
        GPIO.setmode(GPIO.BCM)

	# Set Switch GPIO as input
        GPIO.setup(17 , GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setwarnings(False)
        GPIO.add_event_detect(17, GPIO.RISING, callback=sensorCallback)
        main1()
if __name__ == '__main__':
    app.debug = True
    app.run(host = '127.0.0.1')
