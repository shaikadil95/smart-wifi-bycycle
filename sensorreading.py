import RPi.GPIO as GPIO
import time
import datetime
import MySQLdb


db = MySQLdb.connect(host="localhost",  # your host
                     user="user",       # username
                     passwd="root",     # password
                     db="pythonlogin")   # name of the database

cur = db.cursor()
cur.execute("SELECT sessionid FROM testtable")
data = cur.fetchone()
for id in data:
    print (id)
criteria_info = db.cursor()
criteria_info.execute("SELECT timeavailable, criteria FROM accounts WHERE id = %s", (id,))
criteria_data = criteria_info.fetchall()
for timeleft, criterian in criteria_data:
    print (timeleft, criterian)

def sensorCallback(channel):
  global sensorCounter
  global sensorStatus
  sensorStatus = True
  #timestamp = time.time()
  #stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
  sensorCounter += 1
  #print "Sensor LOW " + stamp

def main():

  try:
    global sensorCounter
    global sensorStatus
    sensorStatus = True
    sensorCounter = 0
    while True :
      if sensorStatus == True:
        print ("Sensor Counter   ", sensorCounter)
        sensorStatus = False
        time.sleep(10)
        calculation()

  except KeyboardInterrupt:
    # Reset GPIO settings
    GPIO.cleanup()

def calculation():
    print (sensorCounter)
    time_convert = sensorCounter/10
    calc_result = criterian * time_convert
    final_time = timeleft + calc_result
    curs = db.cursor()
    curs.execute("UPDATE accounts SET timeavailable = %s WHERE id=%s", (final_time, id))
    db.commit()
    print ("SAVED!")

# Tell GPIO library to use GPIO references
GPIO.setmode(GPIO.BCM)

print ("Hall sensor test program \n")

# Set Switch GPIO as input
GPIO.setup(17 , GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setwarnings(False)
GPIO.add_event_detect(17, GPIO.RISING, callback=sensorCallback)

if __name__=="__main__":
   main()
