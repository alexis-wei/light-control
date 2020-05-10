from machine import Neopixel, I2C, Pin, Timer
from board import SDA, SCL
from umqtt.simple import MQTTClient
from time import sleep
import machine
import time
import adafruit_bme680


STATUS = "TEMP"
HEX_COLOR = "#000000"

# create NeoPixel driver on GPIO0 for 60 pixels
np_count = 60
np = machine.Neopixel(machine.Pin(27), np_count, 0)


myMqttClient = b"Hello"
BROKER = b"io.adafruit.com"
adafruitUsername = b"alexiswei"
adafruitAioKey = b"82c482a0b0d14defaeccfaecae62ae36"
mqtt = MQTTClient(myMqttClient, BROKER, 0, adafruitUsername, adafruitAioKey)


def sub_cb(topic, msg):
    global STATUS, HEX_COLOR
    print((topic, msg))
    if topic == b'alexiswei/feeds/mode':
        if msg == b'TEMP':
            print('changed to temp')
            #read from the temperature sensor
            STATUS = 'TEMP'
        elif msg == b'COLOR':
            print('changed to color')
            STATUS = 'COLOR'
    elif topic == b'alexiswei/feeds/hello':
        if STATUS == 'COLOR':
            #print(msg)
            HEX_COLOR = msg.decode("utf-8")



#mqtt = MQTTClient(BROKER)

# This will set the function sub_cb to be called when c.check_msg() checks
# that there is a message pending
mqtt.set_callback(sub_cb)
mqtt.connect()
print("Connected!")

#list of items that we are subscribed to
#i.e. the list of things that the user can interact with to change the behaviour
# mqtt.subscribe("alexiswei/feeds/​mode")
# mqtt.subscribe("alexiswei/feeds/​hello")
mqtt.subscribe(b"alexiswei/feeds/mode")
mqtt.subscribe(b"alexiswei/feeds/hello")
print("Subscribed!")

# every second, we want a new value of temp, pressure, etc...


# message = str(100)
# # publish (topic, message)
# mqtt.publish("alexiswei/feeds/test", message)
# print("Published {} to test.".format(message))
#
#


# Create library object using our Bus I2C port
i2c = I2C(id=0, scl=Pin(SCL), sda=Pin(SDA), freq=100000)
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)
# change this to match the location's pressure (hPa) at sea level
#
bme680.sea_level_pressure = 1013.25

def status():
    global STATUS
    print(STATUS)
    if STATUS == 'TEMP':
        tempChange()
    elif STATUS == 'COLOR':
        colorChange()

def check(timer):
    print("check")
    mqtt.check_msg()
    status()


def get_temp():
    temp = bme680.temperature
    print(temp)
    np.setHSB(1, 360*(temp - 20.0)/10, 1.0, 0.3, np_count, True)
    return temp


def tempChange():
    mqtt.publish("alexiswei/feeds/temperature", str(get_temp()))

def colorChange():
    global HEX_COLOR
    # h = HEX_COLOR
    # colorRGB = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    # R = colorRGB(0)
    # G = colorRGB(1)
    # B = colorRGB(2)
    hex = HEX_COLOR.lstrip('#')
    rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
    print(rgb)

    r = rgb[0]
    g = rgb[1]
    b = rgb[2]

    # r = format(int(bin(int(rgb[0]))[2:]), '08d')
    # g = format(int(bin(int(rgb[1]))[2:]), '08d')
    # b = format(int(bin(int(rgb[2]))[2:]), '08d')
    print((r << 16) + (g << 8) + b)
    #print(int(str(r) + str(g) + str(b)))

    # R = bin(int(rgb[0]))[2:].zfill(8)
    # G = bin(int(rgb[1]))[2:].zfill(8)
    # B = bin(int(rgb[2]))[2:].zfill(8)
    # bits = str(R) + str(G) + str(B)
    # print(HEX_COLOR)
    (h, s ,b) = np.RGBtoHSB((r << 16) + (g << 8) + b)
    print([h, s , b ])
    np.setHSB(1, h, s , b, np_count, True)
    #np.set(1, int(bits), 0, np_count, True)


sensor_timer = machine.Timer(1)
sensor_timer.init(period=3000, mode=sensor_timer.PERIODIC, callback=check)




#print(get_temp())
