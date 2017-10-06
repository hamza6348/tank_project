#Libraries
import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)









GPIO.setmode(GPIO.BOARD)
 
#set GPIO Pins
GPIO_TRIGGER = 8
GPIO_ECHO = 10
GPIO_SIG=18
GPIO_VALVE=24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_SIG, GPIO.OUT)
GPIO.setup(GPIO_VALVE,GPIO.OUT)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, GPIO.HIGH)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, GPIO.LOW)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    lastdist=0
    try:
        while True:
            dist = distance()
	    diff=lastdist-dist
           		
            print "Measured Distance = %.1f cm diff=%.1fcm" % (dist,diff)
	    if(dist>=-50 and dist<=10):
		print 'anamoly'
	    elif(dist>55):
		#print 'exec 1'
	        GPIO.output(GPIO_SIG,GPIO.LOW)
		GPIO.output(GPIO_VALVE,GPIO.LOW)

	    elif(dist<35 and diff<10):
		GPIO.output(GPIO_SIG,GPIO.HIGH)
		GPIO.output(GPIO_VALVE,GPIO.HIGH)
            lastdist=dist	
            time.sleep(5)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")     
        GPIO.cleanup()
