#!/usr/bin/python3

## piheatcontrol, a program to log and report temperatures using Raspberry Pi and 
### DHT22, heat and humidity sensor

## Copyright (C) 2019 Cem Keylan <cem at ckyln dot com>

##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Import statements
import RPi.GPIO as GPIO
import os
try:
    from customs import credentials, heat
except ModuleNotFoundError:
    os.system('./scripts/firstsetup.sh')
    try:
        from customs import credentials, heat, name
    except:
        print('There was an error importing credentials.')
        exit()
import notifymail
import Adafruit_DHT as dht
from time import sleep
import psycopg2 as pg
from socket import gethostname


def gpiosetup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(10, GPIO.OUT, initial=GPIO.HIGH)


def checktemp(temp):      # Checks if the temperature is bigger 
    if temp == None:
        notifymail.send('[%s] Hardware Warning'%gethostname(), 'Hardware is sending temperature as "None". Please make a hardware check.')
    if temp > heat.max:   # than the allowed temperature
        GPIO.output(8, GPIO.HIGH)
        notifymail.send(
                '[%s] Temperature Warning'%gethostname(),
                'Raspberry Pi has recorded a rise in the room temperature\nRoom Temp: %d'%temp)  
        # You have to setup notifymail beforehand
    else:
        GPIO.output(8, GPIO.LOW)


def dbcommit(hum, temp):
   conn = pg.connect(
           dbname=credentials.db,
           user=credentials.username,
           password=credentials.password,
           host=credentials.name,
           port=credentials.port
           )
   c = conn.cursor()
   c.execute('INSERT INTO heat_history (device, heat, humidity) VALUES (%s, %s, %s)', (gethostname(), temp, hum))
   conn.commit()
   c.close()


def main():
    print('Starting Program')
    gpiosetup()
    try:
        while 1:
            hum, temp = dht.read_retry(dht.DHT22, 4)
            checktemp(temp)
            dbcommit(hum, temp)
            sleep(300)
    except KeyboardInterrupt:
        print('Keyboard interrupt, exiting')
        GPIO.output(8, GPIO.LOW)
        GPIO.output(10, GPIO.LOW)
        exit()
    except:
        notifymail.send('[%s] Programming Error'%gethostname(), 'There was an unknown error')
        GPIO.output(8, GPIO.LOW)
        GPIO.output(10, GPIO.LOW)
        exit()


if __name__ == '__main__':
    main()

