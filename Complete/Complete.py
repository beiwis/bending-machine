
import time
import RPi.GPIO as GPIO
from hx711 import HX711
from pyax12.connection import Connection
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Function to clean up and exit
def cleanAndExit():
    print("Cleaning...")
    serial_connection.goto(dynamixel_id, 150, speed=50, degrees=True)
    time.sleep(0.2)
    GPIO.cleanup()
    
    # Close the serial connection <3
    serial_connection.close()
    file.close()
        
    print("Bye!")
    sys.exit()

# Function to set the distance
def set_distance(d=0, sp=20):
    dis = (d * 3.2) + 10 
    serial_connection.goto(dynamixel_id, dis, speed=sp, degrees=True)

# Function to read the force
def read_force(unit="N"):
    if unit == "N":
        return chan.voltage * 8.89644
    elif unit == "K":
        return chan.voltage * 0.907184

# Function to read the weight
def read_STG():
    return hx.get_weight(5)

# Main program
try:
    # Servo initialization
    serial_connection = Connection(port="/dev/ttyAMA0", baudrate=1000000)
    dynamixel_id = 1

    # HX711 initialization
    referenceUnit = 1
    hx = HX711(5, 6)
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(referenceUnit)
    hx.reset()
    hx.tare()

    # ADS1115 initialization
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    ads.gain = 1
    chan = AnalogIn(ads, ADS.P0)

    while True:
        print("Select an automatic (a) or manual (m) ... ")
        sel = input()

        if sel == "m":
            while True:
                print("Select the distance (0-25mm):")
                dis = input()
                try:
                    dis = float(dis)
                    if 0 <= dis <= 25:
                        set_distance(d=dis)
                        time.sleep(1.5)
                        print(f"distance={dis}mm\tSTG={read_STG()}\tForce={read_force(unit='N')}N")
                    else:
                        print("Distance should be between 0 and 25mm.")
                except ValueError:
                    print("Invalid input. Please enter a valid distance value.")
                except KeyboardInterrupt:
                    cleanAndExit()

        if sel == "a":
            print("Starting")
            file = open('report.csv', 'w')
            print("Go to Zero")
            set_distance(d=0)
            time.sleep(4)
            zero_stg = hx.get_weight(5)
            zero_force = chan.voltage
            file.write(f"distance,STG,Force\n")
            for i in range(25):
                print(f"distance={i}mm\tSTG={read_STG()}\tForce={read_force(unit='N')}N")
                file.write(f"{i},{read_STG()},{read_force(unit='N')}\n")
                time.sleep(0.5)
                set_distance(d=i)
            file.close()
            print("Finishing ...")
            set_distance(d=0)

except (KeyboardInterrupt, SystemExit):
    cleanAndExit()
