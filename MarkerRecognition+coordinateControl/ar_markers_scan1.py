#-*- coding: utf-8 -*-
#!/usr/bin/env python

from __future__ import print_function


try:
	import cv2
	from ar_markers import detect_markers
except ImportError:
	raise Exception('Error: OpenCv is not installed')


if __name__ == '__main__':
	print('Press "q" to quit')
	capture = cv2.VideoCapture(0)

	if capture.isOpened():  # try to get the first frame
		frame_captured, frame = capture.read()
	else:
		frame_captured = False
        
	while frame_captured:
		markers = detect_markers(frame)
		for marker in markers:
					
			marker.highlite_marker(frame)
			#print ('Marker ID:',marker.id)
			#print('Marker center:',marker.center)
			x = marker.center[0]
			y = marker.center[1]
			
			if(marker.id != 1): #찾던마커가 아니면 계속 주행 
				print ("GO")
			elif(marker.id == 1): #마커를 찾을경우 나중에 정지 속도 조정 
				print(marker)

				if( 265 <= x and x <=365 ):
					#if(175 <= y and y <= 275): y축은 높이이므로 무시
						print ("Stop")
				elif( x < 265 ):
					print ("back")

				else:
					print ("go")

		cv2.imshow('Test Frame', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		#print (markers)
		frame_captured, frame = capture.read()
		#print markers
	# When everything done, release the capture
	capture.release()
	cv2.destroyAllWindows()


