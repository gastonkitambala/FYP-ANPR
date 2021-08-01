#******** Optical Opto-Gate System for Vehicles*********#
#This system automatically extracts vehicle license plate in videostream
#This system was developped by Kitambala Itaka Gaston
#For the award of Bachelor of Science in Computer Engineering
#*******************************************************#

#Importing Libraries used
import cv2
from newFunctions import * #Importing all functions
from sendmsdbig import sender #importing the function for emails
import drivers #Drivers for LCD Display(I2C)
#Importing Libraries for Plate Extraction
from PlateExtraction import extraction 
from OpticalCharacterRecognition import ocr
from OpticalCharacterRecognition import check_if_string_in_file
import RPi.GPIO as GPIO #Gpio library
import time 

#GPIO Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) #Using the GPIO.BOARD setmode
servoPin = 11 #Servo Motor control pin(Yellow)
IR1 = 31 #Parking Slot 1 Infrared Sensor 
IR2 = 33 #parking Slot 2 Infrared Sensor
exitIR = 37 #Exit Infrared for exiting vehicles
#Setting IR1, IR2 and ExitIr as input and ServoPin as Output
GPIO.setup(exitIR, GPIO.IN)
GPIO.setup(IR1, GPIO.IN)
GPIO.setup(IR2, GPIO.IN)
GPIO.setup(servoPin,GPIO.OUT)
#Listening to the IR sensors for input
sensor1 = GPIO.input(IR1)
sensor2 = GPIO.input(IR2)
exitSensor = GPIO.input(exitIR)
display = drivers.Lcd()   # Importing LCD Drivers
#pwm = GPIO.PWM(servoPin, 50) #PWM initialised at 50Hz frequency
availableSlots = 0 #initialising the number of empty slots to 0

#beginning of OpenCv for License Plate recognition
cap = cv2.VideoCapture(0) #Starting Video Capture
#Entering The endless loop for repetitive function
while(True):
    ret,frame = cap.read() #Read Frames
    plate = extraction(frame) #take a picture
    try:
        text = ocr(plate) #Do Optical Character Recognition
        text = ''.join(e for e in text if e.isalnum()) #Remove spaces from extracted text
    except:
        continue
        
    if text != '': #If extracted text is not null
        print(text,end=" ") #print the license plate
        content = str(text) #convert text to string format
    ##########Email server configuration for email notifications##########
        sendTo = 'gastonkitambala@yahoo.com' #Receiver of email notifications
        emailSubject = "VEHICLE AUTHORISED!" #Email subject
        emailContent = "The vehicle with license number: " + content +" "+"has been granted access on:\n " + time.ctime() #Email Content
        if len(content) >= 5: #if the length of number plate is greater than 5 letters 
            if check_if_string_in_file('./Database/Database.txt', text): #Check if the license plate is in the Database
                print('Registered') 
        #Printing on LCD
                display.lcd_display_string("WELCOME:", 1)
                display.lcd_display_string(text, 2)
                time.sleep(2)
        #If both parking lots are free
                if sensor1 == 1 and sensor2 == 1:
                    availableSlots = 2
                    print("The Available Slots are :", availableSlots)
                    display.lcd_display_string("AVAILABLE LOTS: ", 1)
                    display.lcd_display_string(str(availableSlots), 2)
                    time.sleep(3)
                    display.lcd_display_string("AVAILABLE LOTS: ", 1)
                    display.lcd_display_string("1:FREE - 2:FREE", 2)
                    servoOpenClose() #Open and Close the Gate(Servo Motor)
            #Send Email With vehicle Details
                    sender.sendmail(sendTo, emailSubject, emailContent)
                    print("Email Sent")
                    time.sleep(3)
                    slotsAvailable() #Check Available pakring Space
                    break
                    #continue
        
        #If PArking 1 occupied and paring 2 is free
                elif sensor1 == 0 and sensor2 == 1:
                    availableSlots = 1
                    print("The Available Slots are :", availableSlots)
                    display.lcd_display_string("AVAILABLE LOTS: ", 1)
                    display.lcd_display_string(str(availableSlots), 2)
                    time.sleep(3)
                    display.lcd_display_string("AVAILABLE LOTS: ", 1)
                    display.lcd_display_string("1:USED - 2:FREE", 2)
                    servoOpenClose() #Open and Close Gate(Sevro Motor)
            #Sending Email with vehicle Details
                    sender.sendmail(sendTo, emailSubject, emailContent)
                    print("Email Sent")
                    time.sleep(3)
                    slotsAvailable()
                    break
        #If Parking 1  is free and parking 2 is used
                elif sensor1 == 1 and sensor2 == 0:
                    availableSlots = 1
                    print("The Available Slots are :", availableSlots)
                    display.lcd_display_string("AVAILABLE LOTS: ", 1)
                    display.lcd_display_string(str(availableSlots), 2)
                    time.sleep(3)
                    display.lcd_display_string("AVAILABLE LOTS: ", 1)
                    display.lcd_display_string("1:OPEN - 2:USED", 2)
                    servoOpenClose() #Open and Close Gate(Servo Motor)
            #Sending Email with Vehicle Details
                    sender.sendmail(sendTo, emailSubject, emailContent)
                    print("Email Sent")
                    time.sleep(3)
                    slotsAvailable()
        #If all parking lots are used = Parking is Full
                elif sensor1 == 0 and sensor2 == 0:
                    availableSlots = 0
                    print("No Parking Slot available")
                    display.lcd_display_string("PARKING FULL", 1)
                    display.lcd_display_string("No Parking", 2)
                    time.sleep(3)
                    slotsAvailable()
                    print("PARKING FULL")
                #When all fail    
                else:
                    display.lcd_display_string("Issue Found..", 1)
                    display.lcd_display_string("Retrying...", 2)
                    time.sleep(3)
                    print("Retrying......")

                time.sleep(1)
                GPIO.cleanup() #Cleaning up GIPIO Ports
                time.sleep(1)
                display.lcd_clear()

       #When the extracted Vehicle License Plate is not in the database
            else:
                print('Not Registered')
                time.sleep(3)
                print("ACCESS DENIED")
                time.sleep(2)
                display.lcd_display_string(text, 1)
                display.lcd_display_string("NOT REGISTERED", 2)
                time.sleep(3)
                display.lcd_display_string("ACCESS DENIED   ", 2)
                time.sleep(4)
                display.lcd_display_string("Call Admin      ", 2)
                time.sleep(4)
        #Send email with the vehicle that has been denied access
                sendTo = 'gastonkitambala@yahoo.com'
                emailSubject = "ACCESS DENIED!"
                emailContent = "The vehicle with license number: " + content +" "+"has been denied access on:\n " + time.ctime()
                sender.sendmail(sendTo, emailSubject, emailContent)
                print("Email Sent")
                time.sleep(3)
                display.lcd_clear()
                break

            #####Exit  Section of the System(To be improved, currently not working)
            #if exitSensor == 0:
                #if sensor1 or sensor2 == 0:
                    #availableSlots = 1
                    #servoOpenClose()
                    #availableSlots -=1
                    #display.lcd_display_string("AVAILABLE LOTS: ", 1)
                    #display.lcd_display_string(availableSlots, 2)
                #if sensor1 ==1 and sensor2 ==1:
                    #availableSlots = 2
                    #continue
                #if sensor1 == 0 and sensor2 == 0:
                    #availableSlots = 0
                    #servoOpenClose()
                    #availableSlots -=1
                    #display.lcd_display_string("AVAILABLE LOTS: ", 1)
                    #display.lcd_display_string(availableSlots, 2)
       ###******** End of exit Section *****###

    #When the length of the extracted license Plate is less than 5, Keep retrying until better quality is gotten
            
        else:
            print("Retrying.....")
        
    cv2.imshow('frame',frame) #Show the Video Frame
    if cv2.waitKey(1) & 0xFF == ord('q'): #Stopping the program if an exception happens
        break
    
cap.release() #Release the Capture
cv2.destroyAllWindows() #Close all windows



