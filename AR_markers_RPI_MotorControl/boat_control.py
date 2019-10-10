# -*- coding: utf-8 -*-
#!/usr/bin/env python

#카메라 선언부
from __future__ import print_function

try:
	import cv2
	from ar_markers import detect_markers
except ImportError:
	raise Exception('Error: OpenCv is not installed')




#GPIO lib
import RPi.GPIO as GPIO
from time import sleep

#모터 상태
STOP = 0
FORWARD = 1
BACKWARD = 2

# PIN설정
HIGH = 1
LOW = 0

#실제 핀 정의
#PWM pin
PWM_DC = 18 #BCM

#GPIO pin
DC_A = 14
DC_B = 15

#서보모터 PWM핀
B_SERVO = 23

#GPIO 모드설정
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


# 핀 설정 함수

#모터 핀 설정
def setPinConfig(EN, INA, INB):

    GPIO.setup(EN, GPIO.OUT)
    GPIO.setup(INA, GPIO.OUT)
    GPIO.setup(INB, GPIO.OUT)
    # 100khz 로 pwm 제어
    pwm = GPIO.PWM(EN, 100)
    # 우선 pwm 정지
    pwm.start(0)

    return pwm


#SERVO 핀 및 PWM 설정

GPIO.setup(B_SERVO, GPIO.OUT)
S_pwm = GPIO.PWM(B_SERVO, 100)
S_pwm.start(0)


# 모터제어함수
def setMotorControl(pwm, INA, INB, speed, state):

     #모터 속도 제어 PWM
    pwm.ChangeDutyCycle(speed)

    #전진
    if state == FORWARD:
        GPIO.output(INA, HIGH)    
        GPIO.output(INB, LOW)
    #후진
    if state == BACKWARD:
        GPIO.output(INA, LOW)    
        GPIO.output(INB, HIGH)
    #정지
    if state == STOP:
        GPIO.output(INA, LOW)    
        GPIO.output(INB, LOW)

#모터제어함수를 간단히 사용하기위해 한번더 래핑
def setMotor(ch, speed, state):
    if ch == 'DC':
        setMotorControl(pwmA, DC_A, DC_B, speed, state)

#핀 설정후 PWM 얻어옴
pwmA = setPinConfig(PWM_DC, DC_A, DC_B)

#서보제어함수
def setServo (Spwm):
    S_pwm.ChangeDutyCycle(Spwm)
    



 

#제어 부분

if __name__ == '__main__':
	print('Press "q" to quit')
	capture = cv2.VideoCapture(0)

	if capture.isOpened():  # try to get the first frame
		frame_captured, frame = capture.read()
	else:
		frame_captured = False

        setMotor('DC', 50, FORWARD)
	setServo(14) #정방향
	error_cnt = 0
	marker_cnt = 0

	while frame_captured:

		markers = detect_markers(frame)
                
		
		if markers:
			marker_cnt = 1
			error_cnt = 0
			for marker in markers:
				error_cnt = 0	
				marker.highlite_marker(frame)
				#print ('Marker ID:',marker.id)
				#print('Marker center:',marker.center)
				x = marker.center[0]
				y = marker.center[1]
		
				if(marker.id != 1): #찾던마커가 아니면 계속 주행 
					setMotor('DC', 50, FORWARD)
					setServo(14) #정방향
				elif(marker.id == 1): #마커를 찾을경우 나중에 정지 속도 조정 
					print(marker)
	
					if( 265 <= x and x <=365 ):
						#if(175 <= y and y <= 275): y축은 높이이므로 무시
						setMotor('DC', 0, STOP)
					elif( x < 265 ):
						setMotor('DC', 30, BACKWARD)
						setServo(14) #정방향
					else:
						setMotor('DC', 30, FORWARD)
						setServo(14) #정방향

		else:
			error_cnt = 1;

			if marker_cnt == 1 and error_cnt == 1:
				setMotor('DC', 0, STOP)
				setServo(14) #정방향
				print('error!No marker, STOP') 
				marker_cnt = 0

		cv2.imshow('Test Frame', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		#print (markers)
		frame_captured, frame = capture.read()
		#print markers
	# When everything done, release the capture
	capture.release()
	cv2.destroyAllWindows()

       
