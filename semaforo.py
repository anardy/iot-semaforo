import RPi.GPIO as GPIO
import time
import sys
from multiprocessing import Process, Manager, Value

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pedido = None

def fecha(status):
	global pedido
	if (pedido.value == True):
		pedido.value = False
	GPIO.setup(11, GPIO.OUT)
        GPIO.output(11, status)
        time.sleep(5)
	GPIO.setup(11, GPIO.OUT)
        GPIO.output(11, 0)

def amarela(status):
	GPIO.setup(13, GPIO.OUT)
	GPIO.output(13, status)
	time.sleep(2)
	GPIO.setup(13, GPIO.OUT)
        GPIO.output(13, 0)

def abre(status):
	global pedido
	if (pedido.value == True):
		fecha(1)
	GPIO.setup(18, GPIO.OUT)
	GPIO.output(18, status)
	for i in range (0,10):
		if (pedido.value == True):
			time.sleep(2)
			break
		time.sleep(1)
	GPIO.setup(18, GPIO.OUT)
        GPIO.output(18, 0)

def botao():
	try:
		global pedido
		while True:
			if (GPIO.input(40) == False):
				print('pedido pedestre')
				pedido.value = True
			time.sleep(0.2)
	except KeyboardInterrupt:
		GPIO.cleanup()

def liga():
	try:
		while True:
			fecha(1)
        		abre(1)
		        amarela(1)
	except KeyboardInterrupt:
		GPIO.cleanup()

if __name__ == '__main__':
	try:
		pedido = Value('i', False)
		p1 = Process(target=botao)
		p1.start()
		p2 = Process(target=liga)
		p2.start()
		p1.join()
		p2.join()
	except KeyboardInterrupt:
		GPIO.cleanup()
	        print 'Program terminated'
		p1.terminate()
		p2.terminate()
		p1.join()
		p2.join()
		GPIO.cleanup()
GPIO.cleanup()
