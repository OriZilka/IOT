import RPi.GPIO as GPIO
import wiringpi
import random
from time import sleep

user_pressed = []
def button_callback(channel):
    user_pressed.append(channel)

# declare numbers in matrix for each button
gpioRedButton = 25
gpioYellowButton = 6
gpioGreenButton = 19
gpioBlueButton = 20

# declare number in matrix for each led
gpioRedLed = 5
gpioYellowLed = 13
gpioGreenLed = 26
gpioBlueLed = 21

# declare number in matrix for mini-speaker
gpioSpeaker = 12

# declare all four leds in an array to randomize between them
leds = [gpioRedLed, gpioYellowLed, gpioGreenLed, gpioBlueLed]

# declare corresponding sound frequencies for each led
frequencies = [440, 523, 659, 784]

# set up BCM GPIO numbering
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# set each button as input according to a number in matrix
GPIO.setup(gpioRedButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(gpioYellowButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(gpioGreenButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(gpioBlueButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# set each LED as output according to a number in matrix
GPIO.setup(gpioRedLed, GPIO.OUT)
GPIO.setup(gpioYellowLed, GPIO.OUT)
GPIO.setup(gpioGreenLed, GPIO.OUT)
GPIO.setup(gpioBlueLed, GPIO.OUT)

# declare callback function foreach button
GPIO.add_event_detect(gpioRedButton, GPIO.RISING, callback=button_callback, bouncetime=300)
GPIO.add_event_detect(gpioYellowButton, GPIO.RISING, callback=button_callback, bouncetime=300)
GPIO.add_event_detect(gpioGreenButton, GPIO.RISING, callback=button_callback, bouncetime=300)
GPIO.add_event_detect(gpioBlueButton, GPIO.RISING, callback=button_callback, bouncetime=300)

# set mini-speaker
wiringpi.wiringPiSetupGpio()
wiringpi.softToneCreate(gpioSpeaker)

try:
    count = 1

    # this will carry on until CTRL+C
    while True:
        choices = []
        user_pressed = []

        # light up leds according to the difficulty
        for led in range(0, count):
            # choose random led
            choice = random.choice(leds)
            freIndex = leds.index(choice)

            # saving the random choice
            choices.append(choice)

            # light up led
            GPIO.output(choice, GPIO.HIGH)
            wiringpi.softToneWrite(gpioSpeaker, frequencies[freIndex])
            sleep(0.1)
            GPIO.output(choice, GPIO.LOW)
            wiringpi.softToneWrite(gpioSpeaker, 0)
            sleep(0.4)

        # wait for user input
        sleep(1 * len(choices))

        # if user didn't press enough buttons in time -> fail
        if len(choices) != len(user_pressed):
            print('Tough luck! Please try again...')
            break

        # if user didn't press the correct order of buttons -> fail
        isSuccessful = True
        for index in range(0, len(choices)):
            if choices[index] == gpioRedLed and user_pressed[index] != gpioRedButton:
                print('Tough luck! Please try again...')
                isSuccessful = False
                break

            if choices[index] == gpioBlueLed and user_pressed[index] != gpioBlueButton:
                print('Tough luck! Please try again...')
                isSuccessful = False
                break

            if choices[index] == gpioYellowLed and user_pressed[index] != gpioYellowButton:
                print('Tough luck! Please try again...')
                isSuccessful = False
                break

            if choices[index] == gpioGreenLed and user_pressed[index] != gpioGreenButton:
                print('Tough luck! Please try again...')
                isSuccessful = False
                break

        if not isSuccessful:
            break

        # otherwise, continue for another round
        count = count + 1
        print('Good job! Get ready for the next round...')
        sleep(2)

# run when program is finished (CTRL+C)
finally:
    GPIO.cleanup()