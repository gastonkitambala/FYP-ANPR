import cv2
from functions import servoOpenClose, checkEmptySlot, sendEmail
from functions import checkEmptySlot
from functions import allowCar
from functions import unauthorised
from sendmsdbig import sender
import drivers
from PlateExtraction import extraction
from OpticalCharacterRecognition import ocr
from OpticalCharacterRecognition import check_if_string_in_file
import RPi.GPIO as GPIO
import time 

GPIO.setmode(GPIO.BOARD)
exitIR = 37
GPIO.setup(exitIR, GPIO.IN)
display = drivers.Lcd()

cap = cv2.VideoCapture(0)
while(True):
    ret,frame = cap.read()
    plate = extraction(frame)
    try:
        text = ocr(plate)
        text = ''.join(e for e in text if e.isalnum())
    except:
        continue
        
    if text != '':
        print(text,end=" ")
        content = str(text)
        if check_if_string_in_file('./Database/Database.txt', text):
            allowCar()
        else:
            unauthorised(text, content)          
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()

#functions

    


