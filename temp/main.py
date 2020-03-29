import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17 , GPIO.IN, pull_up_down=GPIO.PUD_UP)

count = 0
c = 0
on = 0
def sensorCallback(channel):
      global speed, overall, max, count, c, start, now, end, new, on
      if on:
          if not GPIO.input(channel):
            count += 1
            c+=1
          if c == 0:
            now = time.time()
          if c == 5:
            c = 0
            new = time.time()
            speed = 5 / (new-now)
            if speed > max:
                max = speed
          if GPIO.input(channel):
            end = time.time()
            overall = count/(end - start)
def take():
    global count,on
      # Loop until users quits with CTRL-C
    try:
    # Loop until users quits with CTRL-C
        while True :
            time.sleep(0.1)

    except KeyboardInterrupt:
    # Reset GPIO settings
        GPIO.cleanup()

  # Called if sensor output changes

  GPIO.add_event_detect(17, GPIO.BOTH, callback=sensorCallback, bouncetime=200)
