import cv2
import time
import RPi.GPIO as GPIO
import drivers
from functions import checkEmptySlot, sendEmail
from sendmsdbig import sender
from PlateExtraction import extraction
from OpticalCharacterRecognition import ocr, check_if_string_in_file

# System Configuration
SERVO_PIN = 11
EXIT_IR_PIN = 37
ADMIN_EMAIL = 'gastonkitambala@yahoo.com'
SERVO_OPEN_ANGLE = 7
SERVO_CLOSED_ANGLE = 2
DATABASE_PATH = './Database/Database.txt'

def setup_gpio():
    # Initialize GPIO settings
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(EXIT_IR_PIN, GPIO.IN)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    return GPIO.PWM(SERVO_PIN, 50)

def control_servo(pwm, open_gate=True):
    # Control gate servo motor
    try:
        pwm.start(SERVO_CLOSED_ANGLE)
        time.sleep(0.5)
        if open_gate:
            pwm.ChangeDutyCycle(SERVO_OPEN_ANGLE)
            time.sleep(10)
            pwm.ChangeDutyCycle(SERVO_CLOSED_ANGLE)
        time.sleep(1)
        pwm.stop()
    except Exception as e:
        print(f"Error controlling servo: {e}")

def send_notification(plate_number, access_granted=True):
    # Send email notification about vehicle access
    subject = "APPROACHING VEHICLE!" if access_granted else "ACCESS DENIED!"
    status = "granted" if access_granted else "denied"
    content = f"The vehicle with license number: {plate_number} has been {status} access on:\n {time.ctime()}"
    try:
        sender.sendmail(ADMIN_EMAIL, subject, content)
        print("Email Sent")
    except Exception as e:
        print(f"Error sending email: {e}")

def handle_registered_vehicle(display, pwm, plate_number):
    # Process for registered vehicles
    display.lcd_display_string("WELCOME:", 1)
    display.lcd_display_string(plate_number, 2)
    time.sleep(2)
    
    checkEmptySlot()
    control_servo(pwm, True)
    send_notification(plate_number, True)
    
    time.sleep(1)
    display.lcd_clear()

def handle_unregistered_vehicle(display, plate_number):
    # Process for unregistered vehicles
    display.lcd_display_string(plate_number, 1)
    display.lcd_display_string("NOT REGISTERED", 2)
    time.sleep(3)
    display.lcd_display_string("ACCESS DENIED   ", 2)
    time.sleep(4)
    display.lcd_display_string("Call Admin      ", 2)
    
    send_notification(plate_number, False)
    time.sleep(4)
    display.lcd_clear()

def main():
    try:
        display = drivers.Lcd()
        pwm = setup_gpio()
        
        # ALPR process
        image = cv2.imread('./CarPictures/001.jpg')
        plate = extraction(image)
        text = ocr(plate)
        plate_number = ''.join(e for e in text if e.isalnum())
        print(f"Detected plate: {plate_number}")
        
        if check_if_string_in_file(DATABASE_PATH, plate_number) and plate_number:
            print('Registered')
            handle_registered_vehicle(display, pwm, plate_number)
        else:
            print("Not Registered")
            handle_unregistered_vehicle(display, plate_number)
            
        # Handle exit gate
        if GPIO.input(EXIT_IR_PIN) == 0:
            control_servo(pwm, True)
            
    except Exception as e:
        print(f"Error in main program: {e}")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()


