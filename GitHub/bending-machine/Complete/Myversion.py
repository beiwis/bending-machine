import time
import logging as log
import pandas as pd

import board
import busio
import RPi.GPIO as GPIO
from hx711 import HX711
import adafruit_ads1x15.ads1115 as ADS
from pyax12.connection import Connection
from adafruit_ads1x15.analog_in import AnalogIn

n_min = 0 
n_max = 100
dynamixel_id = 1

# Function to clean up and exit
def exit(motor):
    """Function to safely close the connections and exit the script"""
    print("commencing exit sequence...")
    motor.goto(dynamixel_id, 150, speed=50, degrees=True) #TODO: what's this?
    time.sleep(0.2)
    GPIO.cleanup() #TODO: what's this?
    motor.close()   # Close the serial connection
    print("done, see ya")

# Function to set the distance
def set_distance(motor, d=0, s=20): 
    dis = (d * 3.2) + 10 #NOTE: we should probably recalibrate all this
    motor.goto(dynamixel_id, dis, speed=s, degrees=True)

# Function to read the force
def read_force(force_sensor, unit="N"):
    if unit == "N":
        return force_sensor.voltage * 8.89644
    elif unit == "K":
        return force_sensor.voltage * 0.907184 #NOTE: is this calibrated?

# Function to read the weight
def read_STG(STG_sensor):
    """function that reads the weight measured by the strain gauge"""
    return STG_sensor.get_weight(5) #TODO: what's this

def format_number(i: int) -> str:
    """method that turns an entire (positive) number into its ordinal string"""
    if i % 10 == 1 and i != 11:
        return f"{i}st"
    elif i % 10 == 2 and i != 12:
        return f"{i}nd"
    elif i % 10 == 3 and i != 13:
        return f"{i}rd"
    else:
        return f"{i}th"

def init():
    """this function allows to initialize the comunication with the sensors"""
    log.info('initializing the motor and sensors communications...')
    # Servo initialization
    motor = Connection(port="/dev/ttyAMA0", baudrate=1000000)

    # HX711 initialization #TODO: and this?
    referenceUnit = 1
    STG_sensor = HX711(5, 6)
    STG_sensor.set_reading_format("MSB", "MSB")
    STG_sensor.set_reference_unit(referenceUnit)
    STG_sensor.reset() #TODO: reset on initialization?
    STG_sensor.tare()

    # ADS1115 initialization #TODO: check this thing
    ads = ADS.ADS1115(busio.I2C(board.SCL, board.SDA))
    ads.gain = 1
    force_sensor = AnalogIn(ads, ADS.P0)
    return[motor, STG_sensor, force_sensor]
    log.info('connections initialized! <3')

def automatic_test(STG_sensor, force_sensor, n = 25):
    """Runs an automatic test, spanning from 0 to 25mm is as many steps specified in the argument (default is 25, must be greater than 0 and less than 100)""" #TODO: what should be the upper liit i feel like 100 is too small
    i = 0
    if ((n > n_min) and (n < n_max)): # we check the n value is appropiate
        log.info('starting the automatic test...')
        data = {'distance [mm]': [], 'STG': [], 'Force [N]': []} #TODO: add units to the column titles
        df = pd.DataFrame(data)
        log.info("calibrating to initial position...") #FIXME: it'd probably be better to calibrate this using the minimal strain position since mechanical tuning isn't that effective specially if it's not done regularely
        set_distance(d=0)
        time.sleep(4) #FIXME: we should use a calibration condition instead of a timer
        log.info("calibrating done, starting now!")
        for i in range(n):
            set_distance(d=i)
            time.sleep(0.5) #TODO: is this the best???
            log.info("distance = {} mm | STG = {} | Force = {} N".format(i, read_STG(STG_sensor), read_force(force_sensor)))
            df.loc[i] = [i, read_STG(STG_sensor), read_force(force_sensor)]
        log.info("going back to initial position...")
        set_distance(d=0)
    else: log.error("please input a valid n value")
    
def manual_test(STG_sensor, force_sensor, n = 0):
    """Runs a manual test, where the user sets the position of the test material for as many points as wanted"""
    i = 0
    if ((n > n_min) and (n < n_max)): # we check the n value is appropiate
        log.info('starting the manual test...')
        data = {'distance [mm]': [], 'STG': [], 'Force [N]': []} #TODO: add units to the column titles
        df = pd.DataFrame(data)
        log.info("calibrating to initial position...") #FIXME: it'd probably be better to calibrate this using the minimal strain position since mechanical tuning isn't that effective specially if it's not done regularely
        set_distance(d=0)
        time.sleep(4) #FIXME: we should use a calibration condition instead of a timer
        log.info("calibrating done, starting now!")
        for i in range(n):
            d = input("Select the distance for the {} measurement: ".format(format_number(i)))
            set_distance(d=i)
            time.sleep(0.5) #TODO: is this the best???
            log.info("distance = {} mm | STG = {} | Force = {} N".format(i, read_STG(STG_sensor), read_force(force_sensor)))
            df.loc[i] = [d, read_STG(STG_sensor), read_force(force_sensor)]
        while not finished:
            finished = (input("do you want to add any other measurements? 'n' to finish") == 'n')
            if not finished:
                i+=1
                d = input("Select the distance for the {} measurement: ".format(format_number(i)))
                set_distance(d=i)
                time.sleep(0.5) #TODO: is this the best???
                log.info("distance = {} mm | STG = {} | Force = {} N".format(i, read_STG(), read_force()))
                df.loc[i] = [d, read_STG(), read_force(unit='N')]
        log.info("manual test finished going back to initial position...")
        set_distance(d=0)
    else: log.error("please input a valid n value")
    
# Main program
def main():
    try:
        [stg_sensor, force_sensor, motor] = init()
        while True:
            sel = ''
            while sel == '': # We make sure a correct answer is given
                sel = input("Select an automatic (a) or manual (m) ... ")
                if (sel != 'a') and (sel != 'm'):
                    log.error("Input a valid value")
                    sel = ''

            if sel == "m": # Manual mode
                n = input("Select the number of measurements (0-100): ")
                #TODO: do the n check here instead of on the method
                manual_test(n)
            else: # Automatic mode
                automatic_test()
    except (KeyboardInterrupt, SystemExit):
        exit()

if __name__ == '__main__':
  main()