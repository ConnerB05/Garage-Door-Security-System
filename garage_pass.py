# importing the needed libraries
from gpiozero import LED, Button, Buzzer
from signal import pause
import time
from time import sleep
import smtplib
from threading import Timer # To close button 
import string
import secrets #to create random number
from datetime import datetime #for the 60 passkey verification
from hashlib import sha256 #to hash
from secrets import compare_digest # to compare two hash values

# this file contains the email credentials
import emailcred

try:
    # create the needed variables and connect them to GPIO pins
    red_LED = LED(25)       # if on, the door is open
    green_LED = LED(23)     # if on, the door is closed
    button = Button(24)
    buzzer = Buzzer(16)

    # initial state of the door is closed
    
    
    is_open = False
    red_LED.off()
    green_LED.on()


    #Function to send open door notification to the email
    def send_msg():
        # add your code here
        # use the Email Notification Block
        # we will use Gmail accounts and SMTP protocol
        server = smtplib.SMTP_SSL( 'smtp.gmail.com', 465)

        # get login credentials from the file "emailcred.py"
        server.login( emailcred.FROM, emailcred.PASS )
        #Compile message string to print and send.
        actionMessage = ''.join([ '\n Garage door was opened at ',
                            time.strftime('%I:%M:%S %p')])
        print(actionMessage)
        server.sendmail(emailcred.FROM, emailcred.TO, actionMessage)
        server.quit()
        
        
    #Function to send passkey in an email to the user
    def send_token():
        server = smtplib.SMTP_SSL( 'smtp.gmail.com', 465)

        # get login credentials from the file "emailcred.py"
        server.login( emailcred.FROM, emailcred.PASS )
        #Compile message string to print and send.
        actionMessage = ''.join(['\n generated passkey expires in 60 seconds ' + rand_token + ' ',
                            time.strftime('%I:%M:%S %p')])
        server.sendmail(emailcred.FROM, emailcred.TO, actionMessage)
        server.quit()
        
    
    # To start a 60 second timer
    def timer():
        global start_time
        start_time = time.time()
        
        
    # Reenable button after 10 seconds
    def reenable():
        button.when_pressed = door_button
        
        
    # creates the salt and salts the password
    def salt():
        global rand_salt
        #creates random salt
        rand_salt = secrets.token_bytes(16)
        #hashes password plus salt
        hashed_pass = sha256(b'roger123' + rand_salt)
        global hexdigest_pass
        hexdigest_pass = hashed_pass.hexdigest()
        
    # hashes the password the user inputed
    def hash_pass():
        user_hash = bytes(pass_input, 'utf-8')
        user_digest = sha256(user_hash + rand_salt)
        global hexdigest_user
        hexdigest_user = user_digest.hexdigest()
        
    def token():
        global rand_token
        #creates 5 digit passkey
        token = string.digits
        rand_token = ''.join(secrets.choice(token) for i in range(5))
        #calls function to send passkey to email
        send_token()
        #calls function to start the timer
        timer()

    def open_door():
        # add your code here
        global pass_input
        #user inputs password
        pass_input = input("Enter the password: ")
        #calls hash function to hash the input
        hash_pass()
        #checks inputed hash versus stored hash
        if hexdigest_user == hexdigest_pass:
            token()
            #takes user input for passkey
            token_input = input("Enter the passkey sent to your email: ")
            # Checks if the start time in the timer function is less the 60 seconds to accpet the input
            while time.time() - start_time < 60:
                #checks generated passkey versus the inputed passkey
                if token_input == rand_token:
                    print("Opening garage door")
                    green_LED.off()
                    buzzer.beep(0.5, 0.5, 5)
                    #blinks red light for 5 seconds
                    for i in range(5):
                        red_LED.on()
                        sleep(0.5)
                        red_LED.off()
                        sleep(0.5)
                        i+1
                    global is_open
                    is_open = True
                    red_LED.on()
                    #sends email about door opened
                    send_msg()
                    print ("pausing for 10 seconds")
                    #closes button for 10 seconds
                    button.when_pressed = None
                    Timer(10, reenable()).start()
                    return
                else: #passkey else
                    print("Incorrect passkey")
                    return
            else: #while else
                print("Passkey expired")
                return
        else: #password else
            print("Incorrect password")
            return
            
            
        
        
        
        
        

    def close_door():
        # add your code here
        print("Closing garage door")
        red_LED.off()
        buzzer.beep(0.5, 0.5, 5)
        #blinks the green led for 5 seconds for door closing
        for i in range(5):
            green_LED.on()
            sleep(0.5)
            green_LED.off()
            sleep(0.5)
            i+1
        global is_open
        is_open = False
        green_LED.on()
        print ("pausing for 10 seconds")
        #closes button for 10 seconds
        button.when_pressed = None
        Timer(10, reenable()).start()
        
        
      

    def door_button():
        if is_open:
            close_door()
        else:
            open_door()

    def main():
        salt() #calls salt function to salt the password as soon as the program runs
        print("Press the button to open/close the door. Press Ctrl+C to exit.")

        button.when_pressed = door_button

        # The pause function forces the program to wait and not exit
        pause()
        
    if __name__ == "__main__":
        main()

except KeyboardInterrupt:
    # Handle Ctrl+C gracefully
    print("\nExiting the program...")

finally:
    # Cleanup resources
    print("Cleaning up GPIO pins...")
    button.close()          # Release the GPIO pin for the button   
    red_LED.off()           # Ensure the red LED is turned off
    red_LED.close()         # Release the GPIO pin for the red LED
    green_LED.off()         # Ensure the green LED is turned off
    green_LED.close()       # Release the GPIO pin for the green LED
    buzzer.off()
    buzzer.close()
    # Release the GPIO pin for the buzzer
