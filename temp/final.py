import RPi.GPIO as GPIO
import time
import datetime

def main:        
    class person:
        main1()
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

if __name__=="__main__":
   main()
